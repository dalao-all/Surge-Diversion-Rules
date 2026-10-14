#!/usr/bin/env python3
"""
rulekit：把你用的 App 对应的上游规则（广告 + 功能）每天抓下来，合并成按 Surge 策略划分的自有规则集。

  python3 build.py            # 构建到 dist/，失败时退出码非 0、不覆盖 dist/
  FORCE=1 python3 build.py    # 跳过「变化量保护」与「缓存过期检查」（确认上游大改是正常的之后用）

设计要点
  1. 按策略合并输出（ads / ai / tiktok / stream / google / uk / global / cn），不是一 App 一文件：
     Surge 一个 RULE-SET 只能挂一个策略，159 个文件只会增加下载失败点。
  2. 跨输出去重有固定优先级：allow > ads > ai > tiktok > stream > google > uk > global > cn。
  3. ABP 源的 @@ 例外不再丢：父域被拦、子域被放行时，子域写进 pre-<输出>.list，放在广告表之前。
  4. 三道保险：上游异常用 7 天内缓存（缓存过期则构建失败告警，不悄悄用旧数据）/
     输出变化量超阈值不发布 / probes.toml 回归测试不过不发布。
"""
import hashlib, json, os, re, sys, time, tomllib, urllib.request
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST, CACHE = os.path.join(ROOT, "dist"), os.path.join(ROOT, "cache")
ORDER = ["ads", "ai", "tiktok", "stream", "google", "uk", "global", "cn"]
BM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/{d}/{f}.list"
MC = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/classical/{n}.list"
KEEP = {"DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-WILDCARD",
        "IP-CIDR", "IP-CIDR6", "IP-ASN", "USER-AGENT"}
DOMAIN_TYPES = {"DOMAIN", "DOMAIN-SUFFIX"}
# 绝不允许出现在任何输出里的「后缀」：整顶级域 / 公共后缀（10-12 那次 .at/.click 事故的保险）
PUBLIC_SUFFIX = set("""com net org cn io co me app dev ai info biz xyz top site online club tv cc
com.cn net.cn org.cn gov.cn edu.cn co.uk org.uk co.jp ne.jp com.hk com.tw com.sg co.kr
github.io githubusercontent.com cloudfront.net amazonaws.com akamaized.net azureedge.net
in-addr.arpa ip6.arpa arpa local lan""".split())
HOST_RE = re.compile(r"^[a-z0-9*]([a-z0-9\-*]*[a-z0-9*])?(\.[a-z0-9*]([a-z0-9\-*]*[a-z0-9*])?)*$")
IPV4_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
# 上游缓存最长有效期：超过 7 天的缓存不再兜底，上游改名/下线时直接让构建失败告警，
# 而不是悄悄沿用旧数据（blackmatrix7 改目录名那次的教训）
CACHE_MAX_AGE = 7 * 86400
def cache_fresh(cp):
    return os.path.exists(cp) and (time.time() - os.path.getmtime(cp)) < CACHE_MAX_AGE

log_lines = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); log_lines.append(s)

# ---------------- 抓取（带缓存与缩水保护） ----------------
def expand(src):
    if src.startswith("bm:"):
        name = src[3:]; d = name.split("_")[0]
        return BM.format(d=d, f=name)
    if src.startswith("mc:"):
        return MC.format(n=src[3:])
    return src

def fetch(src, shrink):
    if src.startswith("custom/") or src.endswith("allow.list"):
        return open(os.path.join(ROOT, src), encoding="utf-8").read()
    url = expand(src)
    cp = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest()[:16] + ".txt")
    cached = open(cp, encoding="utf-8").read() if os.path.exists(cp) else None
    text, err = None, None
    for i in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "rulekit/1.0", "Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode("utf-8", "ignore"); break
        except Exception as e:
            err = e; time.sleep(2 * (i + 1))
    if text is None:
        if cached is None: raise SystemExit(f"[致命] 抓取失败且无缓存：{src} ({err})")
        if not cache_fresh(cp) and os.environ.get("FORCE") != "1":
            raise SystemExit(f"[致命] 抓取失败且缓存已过期（>7 天）：{src} ({err})；确认上游正常变更后可用 force 重跑")
        log(f"  [警告] 抓取失败，用缓存：{src} ({err})"); return cached
    if cached and len(text) < len(cached) * (1 - shrink):
        if not cache_fresh(cp) and os.environ.get("FORCE") != "1":
            raise SystemExit(f"[致命] 上游疑似缩水且缓存已过期（>7 天）：{src}；确认正常后可用 force 重跑")
        log(f"  [警告] 上游缩水 {len(cached)}→{len(text)} 字节，疑似异常，用缓存：{src}"); return cached
    os.makedirs(CACHE, exist_ok=True); open(cp, "w", encoding="utf-8").write(text)
    return text

# ---------------- 解析 ----------------
def valid_domain(v, t):
    if not HOST_RE.match(v) or "." not in v: return False          # 单标签（at / click …）
    if t == "DOMAIN-SUFFIX" and v in PUBLIC_SUFFIX: return False
    return True

def parse(text):
    """返回 [(type, value)]；兼容 Surge list / Surge domainset / mihomo classical / 纯域名行。"""
    out = []
    for raw in text.splitlines():
        l = raw.split("#")[0].strip() if not raw.lstrip().startswith("#") else ""
        if not l or l.startswith(("!", "//", ";", "[")): continue
        if "," not in l:                                   # domainset 或纯域名
            l = l.lower()
            if l.startswith("+."): t, v = "DOMAIN-SUFFIX", l[2:]
            elif l.startswith("."): t, v = "DOMAIN-SUFFIX", l[1:]
            else: t, v = "DOMAIN", l
            if IPV4_RE.match(v):                           # 纯 IPv4（如浮风 ||IP^）：转 CIDR，走 -extra 表
                out.append(("IP-CIDR", v + "/32")); continue
        else:
            p = [x.strip() for x in l.split(",")]
            t, v = p[0].upper(), p[1]
            if t == "HOST": t = "DOMAIN"
            if t == "HOST-SUFFIX": t = "DOMAIN-SUFFIX"
            if t == "HOST-KEYWORD": t = "DOMAIN-KEYWORD"
            if t not in KEEP: continue                      # PROCESS-NAME / URL-REGEX / AND … 丢弃
            if t.startswith("DOMAIN"): v = v.lower()
        if t in DOMAIN_TYPES and not valid_domain(v, t): continue
        if t == "DOMAIN-KEYWORD" and (re.fullmatch(r"[\d.]+", v) or len(v) < 4): continue  # WeChat 的 IP 前缀"关键词"等
        if t == "DOMAIN" and ("5ukk4w" in v or v.endswith("skk.moe")): continue  # SKK 占位条目
        out.append((t, v))
    return out

def parse_abp(text):
    block, allow = [], []
    for l in text.splitlines():
        l = l.strip()
        m = re.match(r"^(@@)?\|\|([a-z0-9.\-]+)\^(\$(important|all|document|third-party|~third-party))?$", l)
        if not m: continue
        host = m.group(2)
        if IPV4_RE.match(host):                             # ||1.2.3.4^ 这类：转 CIDR，不写进 domainset
            (allow if m.group(1) else block).append(("IP-CIDR", host + "/32")); continue
        if not valid_domain(host, "DOMAIN-SUFFIX"): continue
        (allow if m.group(1) else block).append(("DOMAIN-SUFFIX", host))
    # hosts 格式（0.0.0.0 x）一律不收：10-12 事故根源
    return block, allow

# ---------------- 匹配 ----------------
def suffixes(h):
    p = h.split("."); return [".".join(p[i:]) for i in range(len(p))]

class Matcher:
    def __init__(self, rules):
        self.exact, self.suf, self.kw, self.wc = set(), set(), [], []
        for t, v in rules:
            if t == "DOMAIN": self.exact.add(v)
            elif t == "DOMAIN-SUFFIX": self.suf.add(v)
            elif t == "DOMAIN-KEYWORD": self.kw.append(v)
            elif t == "DOMAIN-WILDCARD": self.wc.append(re.compile("^" + re.escape(v).replace(r"\*", ".*").replace(r"\?", ".") + "$"))
    def hit(self, h):
        if h in self.exact or any(s in self.suf for s in suffixes(h)): return True
        if any(k in h for k in self.kw): return True
        return any(w.match(h) for w in self.wc)

def dedupe(rules):
    """去重 + 删掉被同文件后缀覆盖的子条目。"""
    rules = list(OrderedDict.fromkeys(rules))
    suf = {v for t, v in rules if t == "DOMAIN-SUFFIX"}
    out = []
    for t, v in rules:
        if t == "DOMAIN" and any(s in suf for s in suffixes(v)): continue
        if t == "DOMAIN-SUFFIX" and any(s in suf for s in suffixes(v)[1:]): continue
        out.append((t, v))
    return out

# ---------------- 主流程 ----------------
def main():
    cfg = tomllib.load(open(os.path.join(ROOT, "sources.toml"), "rb"))
    st = cfg["settings"]; outs = cfg["outputs"]
    per_src = defaultdict(dict); data = {}; abp_allow = []; nonabp_ads = []
    for key in ORDER:
        o = outs[key]; rules = []
        log(f"[{key}] {o['file']}")
        for s in o.get("sources", []) + o.get("extra_files", []):
            r = parse(fetch(s, st["max_source_shrink"])); per_src[key][s] = len(r); rules += r
        if key == "ads": nonabp_ads = list(rules)
        for s in o.get("abp_sources", []):
            b, a = parse_abp(fetch(s, st["max_source_shrink"]))
            per_src[key][s] = len(b); rules += b; abp_allow += a
        ex = set(o.get("exclude", []))
        # exclude 按后缀生效：写 whatsapp.com 会同时去掉 *.whatsapp.com
        rules = [(t, v) for t, v in rules if not any(v == e or v.endswith("." + e) for e in ex)]
        data[key] = dedupe(rules)

    # 白名单：手工 allow.list + ABP 例外
    allow = []  # (type, value, key or None)
    for raw in open(os.path.join(ROOT, "allow.list"), encoding="utf-8"):
        l = raw.split("#")[0].strip()
        if not l: continue
        p = [x.strip() for x in l.split(",")]
        allow.append((p[0], p[1].lower(), p[2] if len(p) > 2 else None))
    # ABP 例外只用来抵消 ABP 源自己的根域拦截：SKK/v2fly/秋风 本身就拦的，例外不生效（不削弱其他源）
    nm = Matcher(nonabp_ads)
    curated = {v for _, v, _ in allow}
    ign = cfg["outputs"]["ads"].get("ignore_exceptions", [])
    abp_allow = [(t, v) for t, v in dict.fromkeys(abp_allow)
                 if not nm.hit(v) and v not in curated and not any(v == e or v.endswith("." + e) for e in ign)]
    allow += [("DOMAIN", v, "abp") for _, v in abp_allow]

    # 1) 拒绝表：删掉与白名单相同或位于白名单后缀之下的条目
    am_suffix = {v for t, v, _ in allow if t == "DOMAIN-SUFFIX"}
    am_exact = {v for t, v, _ in allow if t == "DOMAIN"}
    before = len(data["ads"])
    data["ads"] = [(t, v) for t, v in data["ads"]
                   if not (v in am_exact or any(s in am_suffix for s in suffixes(v)))]
    removed_by_allow = before - len(data["ads"])

    infer_m = {k: Matcher(data[k]) for k in ORDER[1:]}   # 去重前的完整 App 表，用于推断放行主机的策略
    cn_cls = Matcher(parse(fetch(st["cn_classifier"], st["max_source_shrink"]))) if st.get("cn_classifier") else None
    # 2) 跨输出优先级去重（只处理精确/后缀；关键词保留）
    moved = defaultdict(int); claimed = set()
    for key in ORDER:
        keep = []
        for t, v in data[key]:
            if t in DOMAIN_TYPES and (t, v) in claimed: moved[key] += 1; continue
            keep.append((t, v)); claimed.add((t, v))
        data[key] = keep

    # 3) 白名单主机：父域仍被拦 → 写 pre-<key>
    ads_m = Matcher(data["ads"])
    app_m = {k: Matcher(data[k]) for k in ORDER[1:]}
    pre = defaultdict(list); unresolved = []
    for t, v, k in allow:
        probe = v
        if not ads_m.hit(probe): continue
        abp_origin = (k == "abp")
        if abp_origin: k = None
        if not k:
            k = next((kk for kk in ORDER[1:] if infer_m[kk].hit(probe)), None)
            if not k:
                # 浮风是国内向列表，它的例外推断不出时默认直连
                k = "cn" if (abp_origin or probe.endswith(".cn") or (cn_cls and cn_cls.hit(probe))) else "global"
                unresolved.append(f"{v}→{k}")
        pre[k].append((t, v))
    for k in pre: pre[k] = dedupe(pre[k])

    # 4) 回归测试（按 Surge 里的实际顺序：pre-* → ads → 各 App 表）
    pre_m = {k: Matcher(v) for k, v in pre.items()}
    def classify(h):
        for k in ORDER[1:]:
            if k in pre_m and pre_m[k].hit(h): return k
        if ads_m.hit(h): return "ads"
        for k in ORDER[1:]:
            if app_m[k].hit(h): return k
        return "none"
    probes = tomllib.load(open(os.path.join(ROOT, "probes.toml"), "rb"))["expect"]
    fails = []
    for h, exp in probes.items():
        got = classify(h)
        ok = (got != exp[1:]) if exp.startswith("!") else (got == exp)
        if not ok: fails.append(f"{h}: 期望 {exp}，实际 {got}")

    # 5) 变化量保护
    guard = []
    for key in ORDER:
        path = os.path.join(DIST, outs[key]["file"])
        if not os.path.exists(path): continue
        prev = sum(1 for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#"))
        cur = len(data[key]); d = abs(cur - prev)
        if d > max(st["min_change_abs"], prev * st["max_change_ratio"]):
            guard.append(f"{outs[key]['file']}: {prev} → {cur}")

    # 报告
    rep = [f"# rulekit 构建报告 {time.strftime('%Y-%m-%d %H:%M %Z')}", ""]
    for key in ORDER:
        o = outs[key]
        # domainset 主表只写入域名类条目：报告显示实际写入数，关键词/IP 在 -extra 表另有表头
        n_written = sum(1 for t, _ in data[key] if o["kind"] != "domainset" or t in DOMAIN_TYPES)
        rep.append(f"## {key} → {o['file']}（{o['policy']}）：{n_written} 条"
                   + (f"，让给更高优先级 {moved[key]} 条" if moved[key] else ""))
        for s, n in per_src[key].items(): rep.append(f"- {s}: {n}")
    rep += ["", f"白名单从拒绝表删除 {removed_by_allow} 条；ABP 例外 {len(abp_allow)} 条",
            "前置放行：" + "，".join(f"pre-{k}.list {len(v)} 条" for k, v in pre.items()),
            "自动推断策略的放行主机：" + ("，".join(unresolved) or "无"), "",
            "## 回归测试", *(fails or ["全部通过"]), "", "## 变化量保护", *(guard or ["正常"]), "", "## 日志", *log_lines]

    if fails or (guard and os.environ.get("FORCE") != "1"):
        os.makedirs(DIST, exist_ok=True)
        open(os.path.join(DIST, "REPORT.failed.md"), "w", encoding="utf-8").write("\n".join(rep))
        print("\n".join(rep[-40:])); sys.exit("构建未通过：dist/ 保持上一版不变")

    # 写出
    os.makedirs(DIST, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M")
    def write(name, policy, rules, kind):
        main = [rv for rv in rules if kind != "domainset" or rv[0] in DOMAIN_TYPES]
        lines = [f"# {name} | 策略 {policy} | {len(main)} 条 | 生成 {stamp} | rulekit"]
        for t, v in main:
            if kind == "domainset":
                lines.append(("." if t == "DOMAIN-SUFFIX" else "") + v)
            else:
                lines.append(f"{t},{v}" + (",no-resolve" if t.startswith("IP-") else ""))
        open(os.path.join(DIST, name), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    for key in ORDER:
        o = outs[key]
        write(o["file"], o["policy"], data[key], o["kind"])
        if o["kind"] == "domainset":   # domainset 放不下的关键词/通配/IP 另存
            extra = [(t, v) for t, v in data[key] if t not in DOMAIN_TYPES]
            write(o["file"].replace(".domainset", "-extra.list"), o["policy"], extra, "list")
    for k, v in pre.items():
        write(f"pre-{k}.list", outs[k]["policy"], v, "list")
    for k in ORDER[1:]:
        if k not in pre: write(f"pre-{k}.list", outs[k]["policy"], [], "list")
    open(os.path.join(DIST, "REPORT.md"), "w", encoding="utf-8").write("\n".join(rep))
    if os.path.exists(os.path.join(DIST, "REPORT.failed.md")): os.remove(os.path.join(DIST, "REPORT.failed.md"))
    print("\n".join(rep[:60]))

if __name__ == "__main__":
    main()
