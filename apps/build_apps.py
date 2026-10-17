#!/usr/bin/env python3
"""按 App 聚合规则：把多个上游（不完整）的同一 App 规则取并集 → dist/apps/<id>.list

来源格式（manifest.json 中 sources / ip_sources）：
  v2:<file>            v2fly/domain-list-community data/<file>（递归 include，丢弃 @cn/@ads，regexp 跳过并报告）
  bm:<Name>            blackmatrix7/ios_rule_script rule/Surge/<Name>/<Name>.list
  acl:<file>           ACL4SSR/ACL4SSR Clash/Ruleset/<file>
  vpsd:<name>          VPSDance/ai-proxy-rules rules/surge/<name>.list
  xiaolai:<name>       xiaolai/anthropic-claude-surge-rules-set <name>.list
  sukka-ai:<section>   SukkaW/Surge Source/non_ip/ai.conf  “# >> <section>” 段
  sukka-gl:<section>   SukkaW/Surge Source/non_ip/global.conf 段
  sukka-global:<KEY>   SukkaW/Surge Source/non_ip/global.ts <KEY>.domains
  sukka-stream:<name>  SukkaW/Surge Source/stream.ts  name:'<name>' 的 rules/ip
  sukka-ip:<file>      SukkaW/Surge Source/ip/<file>.conf
  official:telegram    https://core.telegram.org/resources/cidr.txt
  repo-custom:<name>   本仓库 rulekit_v4/custom/<name>.list
  repo-patch:<name>    本仓库 patches/<name>.list
  custom               本仓库 apps/custom/<id>.list（人工审核/抓包补充）
  v4own                本仓库 dist/v4/cn.list 中归属本表 v4_app_ids 的条目（多个表共同认领 → 归 family 集团表）（provenance：用户 159 App 抓包、protect-cn 业务端点、
                       rulekit_v4/custom/app-*.list、reviewed-*.list 与上游专属表；不含集团共享依赖）
  v4dep:<依赖组>        dist/v4/cn.list 中来自集团共享依赖组（如 tencent-shared）的条目
  v4common             dist/v4/cn.list 中没有任何 App/依赖组归属的条目（Sukka domestic/direct 等基础设施）
IP 规则只从 ip_sources 列出的来源收取，其它来源的 IP 一律丢弃。
上游目录：环境变量 UPSTREAM_DIR（默认 ./.upstream），子目录 v2fly bm acl vpsd xiaolai sukka official。
"""
import json, os, re, sys, datetime, ipaddress
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UP = os.environ.get('UPSTREAM_DIR', os.path.join(ROOT, '.upstream'))
OUT = os.path.join(ROOT, 'dist', 'apps')
MAN = json.load(open(os.path.join(ROOT, 'apps', 'manifest.json'), encoding='utf-8'))
DOMAIN_RE = re.compile(r'^[a-z0-9_*]([a-z0-9_*-]*[a-z0-9_*])?(\.[a-z0-9_*]([a-z0-9_*-]*[a-z0-9_*])?)*$')
warnings = []

def rd(p):
    try:
        return open(p, encoding='utf-8', errors='ignore').read()
    except FileNotFoundError:
        return None

# ---------- 规则规范化 ----------
KEEP = {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'DOMAIN-WILDCARD', 'IP-CIDR', 'IP-CIDR6', 'IP-ASN'}
def norm_rule(line):
    line = line.split('//')[0] if line.lstrip().startswith('//') else line
    line = line.strip().strip("'\",")
    if not line or line.startswith('#') or line.startswith(';'):
        return None
    if line.startswith('+.') or line.startswith('.'):   # domainset 写法
        return ('DOMAIN-SUFFIX', line.lstrip('+').lstrip('.').lower())
    parts = [x.strip() for x in line.split(',')]
    t = parts[0].upper()
    if t == 'IP6-CIDR': t = 'IP-CIDR6'
    if t not in KEEP or len(parts) < 2:
        return ('DROP', line)
    v = parts[1]
    if t.startswith('DOMAIN'):
        v = v.lower().rstrip('.')
        if t != 'DOMAIN-KEYWORD' and t != 'DOMAIN-WILDCARD' and not DOMAIN_RE.match(v):
            return ('DROP', line)
    elif t in ('IP-CIDR', 'IP-CIDR6'):
        try:
            n = ipaddress.ip_network(v, strict=False)
            t = 'IP-CIDR' if n.version == 4 else 'IP-CIDR6'
            v = str(n)
        except ValueError:
            return ('DROP', line)
    return (t, v)

def parse_list_text(txt):
    out = []
    for l in (txt or '').splitlines():
        r = norm_rule(l)
        if r: out.append(r)
    return out

# ---------- v2fly ----------
def v2_load(name, want=None, seen=None, cn=False):
    seen = seen or set()
    if name in seen: return []
    seen.add(name)
    txt = rd(os.path.join(UP, 'v2fly', 'data', name))
    if txt is None:
        warnings.append(f'v2fly 缺少文件 {name}')
        return []
    out = []
    for l in txt.splitlines():
        l = l.split('#')[0].strip()
        if not l: continue
        toks = l.split()
        body, attrs = toks[0], [t[1:] for t in toks[1:] if t.startswith('@')]
        if body.startswith('include:'):
            inc = body[8:]
            out += v2_load(inc, [a for a in attrs], seen, cn)
            continue
        if 'ads' in attrs: continue
        if (not cn and 'cn' in attrs) or (cn and '!cn' in attrs): continue
        if want:   # include:x @attr / @-attr
            ok = True
            for w in want:
                if w.startswith('-'):
                    if w[1:] in attrs: ok = False
                elif w not in attrs: ok = False
            if not ok: continue
        if ':' in body:
            k, v = body.split(':', 1)
        else:
            k, v = 'domain', body
        v = v.lower()
        if k == 'domain': out.append(('DOMAIN-SUFFIX', v))
        elif k == 'full': out.append(('DOMAIN', v))
        elif k == 'keyword': out.append(('DOMAIN-KEYWORD', v))
        elif k == 'regexp': warnings.append(f'v2fly {name} regexp 跳过: {v}')
    return out

# ---------- Sukka ----------
def sukka_section(fname, sec):
    txt = rd(os.path.join(UP, 'sukka', 'Source', 'non_ip', fname)) or ''
    out, on, found = [], False, False
    for l in txt.splitlines():
        if l.startswith('# >>'):
            on = l[4:].strip() == sec
            found = found or on
            continue
        if on:
            r = norm_rule(l)
            if r: out.append(r)
    if not found: warnings.append(f'sukka {fname} 无段落 {sec}')
    return out

def sukka_global(key):
    txt = rd(os.path.join(UP, 'sukka', 'Source', 'non_ip', 'global.ts')) or ''
    m = re.search(r'\n  ' + key + r': \{.*?domains: \[(.*?)\]', txt, re.S)
    if not m:
        warnings.append(f'sukka global.ts 无 {key}'); return []
    out = []
    for s in re.findall(r"'([^']+)'", m.group(1)):
        if s.startswith('$'): out.append(('DOMAIN', s[1:]))       # $ = 精确
        else: out.append(('DOMAIN-SUFFIX', s.lstrip('+.')))
    return out

def sukka_stream(name):
    txt = rd(os.path.join(UP, 'sukka', 'Source', 'stream.ts')) or ''
    txt = re.sub(r'//[^\n]*', '', txt)
    blocks = re.split(r'\n(?:export )?const [A-Za-z0-9_$]+(?:: StreamService)? = ', txt)
    for b in blocks:
        if re.search(r"^\{\s*name: '" + re.escape(name) + "'", b):
            out = [norm_rule(s) for s in re.findall(r"'([A-Z0-9-]+,[^']+)'", b)]
            ipm = re.search(r'ip: \{(.*?)\n  \}', b, re.S)
            if ipm:
                for s in re.findall(r"'([0-9a-fA-F:.]+/\d+)'", ipm.group(1)):
                    out.append(norm_rule('IP-CIDR,' + s))
            return [r for r in out if r]
    warnings.append(f'sukka stream 无 {name}'); return []

# ---------- 仓库 v4 国内表（按 App 拆分） ----------
_V4 = None
def v4_index():
    """把 dist/v4/cn.list 的每条规则按 provenance 归属到 App / 依赖组；海外 App(INT*) 的认领不算（除非上游明确更正为 cn）。"""
    global _V4
    if _V4 is not None: return _V4
    import gzip
    cn = [r for r in parse_list_text(rd(os.path.join(ROOT, 'dist', 'v4', 'cn.list'))) if r[0] != 'DROP']
    universe = set(cn)
    claims = defaultdict(lambda: {'own': set(), 'dep': set(), 'intl': set()})
    pv = os.path.join(ROOT, 'dist', 'v4', 'provenance.ndjson.gz')
    for line in gzip.open(pv, 'rt', encoding='utf-8'):
        rec = json.loads(line)
        if rec.get('category') not in ('cn', 'protect-cn') or not rec.get('published'): continue
        r = norm_rule(rec['rule'])
        if not r or r not in universe: continue
        c = claims[r]
        for o in rec.get('origins', []):
            deps = o.get('dependency_ids') or []
            ids = o.get('app_ids') or []
            fixed_cn = (o.get('correction') or {}).get('output_category') == 'cn'
            for d in deps: c['dep'].add(d)
            if deps: continue
            for i in ids:
                if i.startswith('INT') and not fixed_cn: c['intl'].add(i)
                elif not i.startswith('INT'): c['own'].add(i)
    # App → 输出表；多个表的 App 共同认领的条目 → 共同的集团表（family），否则归排序最前的表
    lst, fam, pos = {}, {}, {}
    for n, a in enumerate(MAN['apps']):
        pos[a['id']] = n
        for i in a.get('v4_app_ids', []): lst[i] = a['id']
        if a.get('family'): fam[a['id']] = a['family']
    own, dep, common, intl_only, unmapped = defaultdict(list), defaultdict(list), [], [], defaultdict(int)
    for r in cn:
        c = claims.get(r)
        if not c or not (c['own'] or c['dep'] or c['intl']): common.append(r); continue
        if not c['own'] and not c['dep']: intl_only.append((r, sorted(c['intl']))); continue
        ls = set()
        for i in c['own']:
            if i in lst: ls.add(lst[i])
            else: unmapped[i] += 1
        if len(ls) > 1:
            fs = {fam.get(x, x) for x in ls}
            ls = fs if len(fs) == 1 else {min(ls, key=pos.get)}
        for x in ls: own[x].append(r)
        for d in c['dep']: dep[d].append(r)
        if not ls and not c['dep']: common.append(r)
    if unmapped: warnings.append(f'v4 App 未映射到任何输出表: {dict(unmapped)}')
    _V4 = {'universe': cn, 'own': own, 'dep': dep, 'common': common, 'intl_only': intl_only}
    return _V4

IP_FRAGMENT = re.compile(r'^[0-9.]+$')

# ---------- 来源分发 ----------
def load_source(src, app_id, cn=False):
    kind, _, arg = src.partition(':')
    if kind == 'v2': return v2_load(arg, cn=cn)
    if kind == 'v4own': return list(v4_index()['own'].get(app_id, []))
    if kind == 'v4dep': return list(v4_index()['dep'].get(arg, []))
    if kind == 'v4common': return list(v4_index()['common'])
    p = {
        'bm': lambda: os.path.join(UP, 'bm', 'rule', 'Surge', arg, arg + '.list'),
        'acl': lambda: os.path.join(UP, 'acl', 'Clash', 'Ruleset', arg),
        'vpsd': lambda: os.path.join(UP, 'vpsd', 'rules', 'surge', arg + '.list'),
        'xiaolai': lambda: os.path.join(UP, 'xiaolai', arg + '.list'),
        'sukka-ip': lambda: os.path.join(UP, 'sukka', 'Source', 'ip', arg + '.conf'),
        'official': lambda: os.path.join(UP, 'official', arg + '-cidr.txt'),
        'repo-custom': lambda: os.path.join(ROOT, 'rulekit_v4', 'custom', arg + '.list'),
        'repo-patch': lambda: os.path.join(ROOT, 'patches', arg + '.list'),
        'custom': lambda: os.path.join(ROOT, 'apps', 'custom', app_id + '.list'),
    }
    if kind == 'sukka-ai': return sukka_section('ai.conf', arg)
    if kind == 'sukka-gl': return sukka_section('global.conf', arg)
    if kind == 'sukka-global': return sukka_global(arg)
    if kind == 'sukka-stream': return sukka_stream(arg)
    if kind not in p:
        warnings.append(f'未知来源类型 {src}'); return []
    txt = rd(p[kind]())
    if txt is None:
        if kind != 'custom': warnings.append(f'{app_id}: 来源文件缺失 {src}')
        return []
    if kind == 'official':
        return [norm_rule('IP-CIDR,' + l.strip()) for l in txt.splitlines() if l.strip()]
    return parse_list_text(txt)

# ---------- 覆盖判断 ----------
def covered_by(rule, suffixes, exacts=()):
    t, v = rule
    if t not in ('DOMAIN', 'DOMAIN-SUFFIX'): return None
    if t == 'DOMAIN' and v in exacts: return ('DOMAIN', v)
    parts = v.split('.')
    for i in range(len(parts)):
        s = '.'.join(parts[i:])
        if s in suffixes and not (t == 'DOMAIN-SUFFIX' and i == 0 and False):
            return ('DOMAIN-SUFFIX', s)
    return None

def kw_hit(rule, kws):
    t, v = rule
    if t not in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD'): return None
    for k in kws:
        if k in v: return k
    return None

def dedupe(rules):
    sfx = {v for t, v in rules if t == 'DOMAIN-SUFFIX'}
    kws = {v for t, v in rules if t == 'DOMAIN-KEYWORD'}
    out, seen = [], set()
    for r in rules:
        if r in seen: continue
        seen.add(r)
        t, v = r
        if t == 'DOMAIN-SUFFIX':
            parent = '.'.join(v.split('.')[1:])
            ps = v.split('.')
            if any('.'.join(ps[i:]) in sfx for i in range(1, len(ps))): continue
        if t == 'DOMAIN' and covered_by(r, sfx): continue
        out.append(r)
    return out

def load_cn_ref():
    """国内参考：dist/v4/cn.list + Sukka domestic/direct。用于发现“App 表里混入国内共用域名”。"""
    sfx, ex = {}, {}
    for f in ('dist/v4/cn.list', 'mirrors/skk/List/non_ip/domestic.conf', 'mirrors/skk/List/non_ip/direct.conf'):
        for r in parse_list_text(rd(os.path.join(ROOT, f))):
            if r[0] == 'DOMAIN-SUFFIX': sfx.setdefault(r[1], f)
            elif r[0] == 'DOMAIN': ex.setdefault(r[1], f)
    return sfx, ex

def load_domestic():
    """protect-cn 在配置中位于所有 App 之前 → 被它覆盖的条目是死规则，剔除。"""
    sfx, ex = set(), set()
    for f in ('protect-cn.list',):
        for t, v in [r for r in parse_list_text(rd(os.path.join(ROOT, 'dist', 'v4', f))) if r[0] != 'DROP']:
            if t == 'DOMAIN-SUFFIX': sfx.add(v)
            elif t == 'DOMAIN': ex.add(v)
    return sfx, ex

KW_DENY = set(MAN.get('keyword_denylist', []))
ORDER = {'DOMAIN': 0, 'DOMAIN-SUFFIX': 1, 'DOMAIN-KEYWORD': 2, 'DOMAIN-WILDCARD': 3, 'IP-CIDR': 4, 'IP-CIDR6': 5, 'IP-ASN': 6}

def main():
    os.makedirs(OUT, exist_ok=True)
    dom_sfx, dom_ex = load_domestic()
    cn_sfx, cn_ex = load_cn_ref()
    apps = MAN['apps']
    built, report = OrderedDict(), OrderedDict()
    for a in apps:
        aid = a['id']
        per_src, union, dropped = OrderedDict(), [], defaultdict(int)
        ipsrc = set(a.get('ip_sources', []))
        excl = set(x.lower() for x in a.get('exclude', []))
        for s in a['sources'] + [x for x in a.get('ip_sources', []) if x not in a['sources']]:
            rules = load_source(s, aid, a.get('category') == 'cn')
            kept = []
            for r in rules:
                if r[0] == 'DROP': dropped['不支持的类型/非法'] += 1; continue
                if r[0].startswith('IP') and s not in ipsrc: dropped['IP(来源未列入 ip_sources)'] += 1; continue
                if not r[0].startswith('IP') and s not in a['sources']: continue
                if r[1] in excl: dropped['exclude'] += 1; continue
                if r[0] == 'DOMAIN-KEYWORD' and IP_FRAGMENT.match(r[1]): dropped['IP 片段关键词(应为 IP-CIDR)'] += 1; continue
                if r[0] == 'DOMAIN-KEYWORD' and r[1] in KW_DENY: dropped['泛关键词(keyword_denylist)'] += 1; warnings.append(f'{aid}: 丢弃泛关键词 {r[1]} (来自 {s})'); continue
                kept.append(r)
            per_src[s] = len(set(kept))
            union += kept
        rules = dedupe(union)
        # 剔除被 protect-cn 覆盖的条目
        dead = [] if a.get('override_protect_cn') or a.get('category') == 'cn' else [r for r in rules if covered_by(r, dom_sfx, dom_ex)]
        rules = [r for r in rules if r not in dead]
        # 与国内表重叠：上游条目剔除（防止把国内 App 拉去代理）；custom 人工条目保留但报告
        custom_set = set(r for r in load_source('custom', aid) if r[0] != 'DROP')
        cn_hit, cn_kept = [], []
        for r in list(rules):
            c = covered_by(r, cn_sfx, cn_ex)
            if c:
                if a.get('category') == 'cn': break
                if r in custom_set or a.get('override_protect_cn'): cn_kept.append(f'{r[0]},{r[1]}')
                else: cn_hit.append(f'{r[0]},{r[1]}'); rules.remove(r)
        built[aid] = rules
        # 每个来源的“独有贡献”
        uniq = {}
        sets = {s: set(r for r in parse_src_cache.get((s, aid), [])) for s in per_src}
        report[aid] = {'name': a['name'], 'total': len(rules), 'per_source_raw': per_src,
                       'dropped': dict(dropped), 'dead_by_protect_cn': [f'{t},{v}' for t, v in dead], 'removed_overlap_cn': cn_hit, 'kept_overlap_cn_custom': cn_kept}
    # ---------- 海外 App 与国内 App 表重叠：剔除海外侧（custom 人工条目除外） ----------
    cn_ids = [a['id'] for a in apps if a.get('category') == 'cn']
    csfx = {v for i in cn_ids for t, v in built[i] if t == 'DOMAIN-SUFFIX'}
    cex = {v for i in cn_ids for t, v in built[i] if t == 'DOMAIN'}
    for a in apps:
        if a.get('category') == 'cn' or a.get('override_protect_cn'): continue
        cs = set(r for r in load_source('custom', a['id']) if r[0] != 'DROP')
        keep = []
        for r in built[a['id']]:
            if r not in cs and covered_by(r, csfx, cex):
                report[a['id']]['removed_overlap_cn'].append(f'{r[0]},{r[1]}（国内 App 表）'); continue
            keep.append(r)
        built[a['id']] = keep
    # ---------- 跨 App 冲突 ----------
    owner = {}
    conflicts = []
    ids = list(built)
    CAT = {a['id']: a.get('category') for a in apps}
    for aid in ids:
        keep = []
        for r in built[aid]:
            if r in owner:
                conflicts.append({'rule': f'{r[0]},{r[1]}', 'kept_in': owner[r], 'removed_from': aid, 'reason': '完全重复，归优先级更高的 App'})
                continue
            owner[r] = aid
            keep.append(r)
        built[aid] = keep
    # 后序 App 的条目若被前序 App 的后缀/关键词覆盖 → 死规则（报告并移除）
    for i, aid in enumerate(ids):
        prev_sfx = {}
        prev_kw = {}
        for pid in ids[:i]:
            for t, v in built[pid]:
                if t == 'DOMAIN-SUFFIX': prev_sfx.setdefault(v, pid)
                if t == 'DOMAIN-KEYWORD': prev_kw.setdefault(v, pid)
        keep = []
        for r in built[aid]:
            c = covered_by(r, prev_sfx)
            k = kw_hit(r, prev_kw) if r[0] != 'DOMAIN-KEYWORD' else None
            if c:
                conflicts.append({'rule': f'{r[0]},{r[1]}', 'kept_in': prev_sfx[c[1]], 'removed_from': aid, 'reason': f'被前序 {c[1]} 后缀覆盖（死规则）'}); continue
            if k and CAT[aid] == 'cn' and CAT[prev_kw[k]] != 'cn':
                conflicts.append({'rule': f'{r[0]},{r[1]}', 'kept_in': aid, 'removed_from': None, 'reason': f'国内条目含海外 App 关键词 {k}（配置中会先命中 {prev_kw[k]}，保留在国内表并报告）'})
                keep.append(r); continue
            if k:
                conflicts.append({'rule': f'{r[0]},{r[1]}', 'kept_in': prev_kw[k], 'removed_from': aid, 'reason': f'含前序 App 关键词 {k} → 移入该 App'})
                if r not in built[prev_kw[k]]: built[prev_kw[k]].append(r)
                continue
            keep.append(r)
        built[aid] = keep
    # ---------- 国内表新增条目不得压过广告层：被新增条目“罩住”的广告域名 → CN-Reject（配置中放在国内单表之前） ----------
    ads = []   # (类型, 值)
    for f, dset in (('patches/ads-patch.domainset', True), ('mirrors/owned/List/domainset/reject.conf', True),
                    ('mirrors/owned/List/domainset/reject_phishing.conf', True), ('patches/ads-supplement.list', False),
                    ('mirrors/owned/List/non_ip/reject.conf', False), ('mirrors/owned/List/non_ip/reject-drop.conf', False),
                    ('mirrors/owned/List/non_ip/reject-no-drop.conf', False)):
        txt = rd(os.path.join(ROOT, f)) or ''
        for l in txt.splitlines():
            l = l.strip()
            if not l or l[0] in '#;': continue
            if dset:
                ads.append(('DOMAIN-SUFFIX', l.lstrip('+').lstrip('.').lower()) if l[0] in '.+' else ('DOMAIN', l.lower()))
            else:
                r = norm_rule(l)
                if r and r[0] in ('DOMAIN', 'DOMAIN-SUFFIX'): ads.append(r)
    ad_sfx = {v for t, v in ads if t == 'DOMAIN-SUFFIX'}; ad_ex = {v for t, v in ads if t == 'DOMAIN'}
    old_cover_sfx = set(cn_sfx) | dom_sfx; old_cover_ex = set(cn_ex) | dom_ex
    # ads_trust：V3.5.5 起就在国内层（广告层之前）的 27 个表，其上游条目视同已审核，不做广告过滤，保持原行为
    trust = {a['id'] for a in apps if a.get('ads_trust')}
    for aid in trust:
        for t, v in built[aid]:
            if t == 'DOMAIN-SUFFIX': old_cover_sfx.add(v)
            elif t == 'DOMAIN': old_cover_ex.add(v)
    new_sfx = {}
    ads_dropped, cn_reject = [], []
    for aid in ids:
        if CAT[aid] != 'cn': continue
        keep = []
        for r in built[aid]:
            if r[0] in ('DOMAIN', 'DOMAIN-SUFFIX') and not covered_by(r, old_cover_sfx, old_cover_ex) and covered_by(r, ad_sfx, ad_ex):
                ads_dropped.append({'rule': f'{r[0]},{r[1]}', 'app': aid}); continue   # 条目本身就是广告域名
            if r[0] == 'DOMAIN-SUFFIX' and not covered_by(r, old_cover_sfx, old_cover_ex): new_sfx[r[1]] = aid
            keep.append(r)
        built[aid] = keep
    seen_rej = set()
    for t, v in sorted(set(ads)):
        if covered_by((t, v), old_cover_sfx, old_cover_ex): continue      # 旧版就已被国内层放行，保持不变
        ps = v.split('.')
        hit = next(('.'.join(ps[i:]) for i in range(1 if t == 'DOMAIN-SUFFIX' else 0, len(ps)) if '.'.join(ps[i:]) in new_sfx), None)
        if hit and (t, v) not in seen_rej:
            seen_rej.add((t, v)); cn_reject.append(((t, v), new_sfx[hit], hit))
    today = datetime.date.today().isoformat()
    rj_hdr = ['# NAME: CN-Reject — 国内单表新增后缀下的广告/追踪域名（保持广告层原有拦截）', '# REPO: https://github.com/dalao-all/Surge-Diversion-Rules',
              f'# BUILT: {today}', '# SUGGESTED POLICY: REJECT（必须放在国内 App 单表之前）', f'# COUNT: TOTAL={len(cn_reject)}']
    rj_body = []
    for (t, v), aid, hit in cn_reject: rj_body += [f'# {aid} 的 {hit} 会罩住它', f'{t},{v}']
    open(os.path.join(OUT, 'CN-Reject.list'), 'w', encoding='utf-8').write('\n'.join(rj_hdr + rj_body) + '\n')
    # ---------- 国内条目被海外 App 关键词误吸 → 生成 CN-Guard（配置中放在海外 App 层之前 DIRECT） ----------
    i_sfx, i_ex, i_kw = {}, set(), {}
    for aid in ids:
        if CAT[aid] == 'cn': continue
        for t, v in built[aid]:
            if t == 'DOMAIN-SUFFIX': i_sfx[v] = aid
            elif t == 'DOMAIN': i_ex.add(v)
            elif t == 'DOMAIN-KEYWORD': i_kw[v] = aid
    guard, guard_skipped = [], []
    for aid in ids:
        if CAT[aid] != 'cn': continue
        for r in built[aid]:
            if r[0] not in ('DOMAIN', 'DOMAIN-SUFFIX'): continue
            k = kw_hit(r, i_kw)
            if k and not covered_by(r, i_sfx, i_ex):
                # CN-Common 是无归属的通用条目（含 Ookla 等海外服务的“国内测速”标注），只对 .cn 域名做防误吸，其余保持海外 App 优先
                if aid == 'CN-Common' and not r[1].endswith('.cn'):
                    guard_skipped.append((r, aid, i_kw[k], k)); continue
                guard.append((r, aid, i_kw[k], k))
    today = datetime.date.today().isoformat()
    g_hdr = ['# NAME: CN-Guard — 国内条目防误吸（被海外 App 的 DOMAIN-KEYWORD 命中的国内域名）', '# REPO: https://github.com/dalao-all/Surge-Diversion-Rules',
             f'# BUILT: {today}', '# SUGGESTED POLICY: DIRECT（必须放在海外 App 规则之前）', '# 自动生成：每条注明所属国内 App 与会误吸它的海外 App 关键词',
             f'# COUNT: TOTAL={len(guard)}']
    g_body = []
    for (t, v), aid, iaid, k in guard:
        g_body += [f'# {aid} ← 被 {iaid} 关键词 {k} 误吸', f'{t},{v}']
    open(os.path.join(OUT, 'CN-Guard.list'), 'w', encoding='utf-8').write('\n'.join(g_hdr + g_body) + '\n')
    for a in apps:
        aid = a['id']
        ips = [ipaddress.ip_network(v) for t, v in built[aid] if t in ('IP-CIDR', 'IP-CIDR6')]
        merged = [('IP-CIDR' if n.version == 4 else 'IP-CIDR6', str(n)) for v in (4, 6) for n in ipaddress.collapse_addresses([x for x in ips if x.version == v])]
        rest = [r for r in built[aid] if r[0] not in ('IP-CIDR', 'IP-CIDR6')]
        def sk(r):
            if r[0] in ('IP-CIDR', 'IP-CIDR6'): n = ipaddress.ip_network(r[1]); return (ORDER[r[0]], n.network_address.packed, n.prefixlen)
            return (ORDER[r[0]], tuple(reversed(r[1].split('.'))) if r[0] in ('DOMAIN', 'DOMAIN-SUFFIX') else r[1])
        rules = sorted(rest + merged, key=sk)
        cnt = defaultdict(int)
        for t, _ in rules: cnt[t] += 1
        hdr = [f'# NAME: {aid} — {a["name"]}', '# REPO: https://github.com/dalao-all/Surge-Diversion-Rules',
               f'# BUILT: {today}', f'# SUGGESTED POLICY: {a.get("suggested_policy", "")}',
               '# SOURCES: ' + ' | '.join(a['sources']),
               '# COUNT: ' + ' '.join(f'{k}={cnt[k]}' for k in sorted(cnt, key=ORDER.get)) + f' TOTAL={len(rules)}']
        if a.get('v4_app_ids'): hdr.append('# V4 APPS: ' + '、'.join(f'{i} {n}' for i, n in zip(a['v4_app_ids'], a.get('v4_app_names', []))))
        if a.get('family'): hdr.append(f'# FAMILY: 与同集团其它 App 共用的域名在 {a["family"]}')
        if a.get('note'): hdr.append('# NOTE: ' + a['note'])
        body = [f'{t},{v},no-resolve' if t.startswith('IP') else f'{t},{v}' for t, v in rules]
        open(os.path.join(OUT, aid + '.list'), 'w', encoding='utf-8').write('\n'.join(hdr + body) + '\n')
        report[aid]['total'] = len(rules)
        report[aid]['count'] = dict(cnt)
    v4 = v4_index()
    json.dump({'built': today, 'order': ids, 'apps': report, 'conflicts': conflicts, 'warnings': warnings,
               'cn_ads_dropped': ads_dropped,
               'cn_reject': [{'rule': f'{t},{v}', 'app': aid, 'shadowed_by': hit} for (t, v), aid, hit in cn_reject],
               'cn_guard': [{'rule': f'{t},{v}', 'cn_app': aid, 'intl_app': iaid, 'keyword': k} for (t, v), aid, iaid, k in guard],
               'cn_guard_skipped': [{'rule': f'{t},{v}', 'cn_app': aid, 'intl_app': iaid, 'keyword': k} for (t, v), aid, iaid, k in guard_skipped],
               'v4_cn_intl_only': [{'rule': f'{t},{v}', 'claimed_by': c} for (t, v), c in v4['intl_only']]},
              open(os.path.join(OUT, 'report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    md = ['# 按 App 规则集（dist/apps）', '', f'构建日期：{today}。每个 App 一个文件，内容为多个上游同名规则的并集（去重、剔除国内共用域名、跨 App 冲突按优先级归属）。',
          '', '引用格式：`RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/dist/apps/<App>.list,<策略>`', '',
          '表格顺序即推荐的规则顺序（共享域名只归属排在前面的 App）。详细来源统计见 report.json，上游提交见 sources.lock.json。', '',
          '另有两个自动生成的辅助表（不在下表）：`CN-Guard.list`（被海外关键词误吸的国内域名，放海外 App 层之前 DIRECT）、`CN-Reject.list`（被新扩国内后缀罩住的广告域名，放国内单表之前 REJECT）。', '',
          '| # | App | 文件 | 条目 | 最大单一上游 | 建议策略 | 覆盖的 v4 App | 上游 |', '|---|---|---|---|---|---|---|---|']
    for n, a in enumerate(apps, 1):
        r = report[a['id']]; best = max([v for k, v in r['per_source_raw'].items() if k != 'custom'] or [0])
        md.append(f"| {n} | {a['name']} | [{a['id']}.list]({a['id']}.list) | {r['total']} | {best} | {a.get('surge_policy', a.get('suggested_policy', ''))} | {'、'.join(f'{i} {n}' for i, n in zip(a.get('v4_app_ids', []), a.get('v4_app_names', [])))} | {', '.join(x for x in a['sources'])} |")
    open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print(f'apps={len(ids)} conflicts={len(conflicts)} warnings={len(warnings)}')
    for aid in ids:
        r = report[aid]
        print(f"{aid:14s} {r['total']:5d}  " + ' '.join(f"{k}={v}" for k, v in r['per_source_raw'].items()))

parse_src_cache = {}
if __name__ == '__main__':
    main()
