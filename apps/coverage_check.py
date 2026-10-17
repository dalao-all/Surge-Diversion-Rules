#!/usr/bin/env python3
"""覆盖检查：
  1. dist/v4 中所有海外类条目必须被某个海外 App 表覆盖（国内 CN-* 表不算）；
  2. dist/v4/cn.list 的每一条必须落入某个国内 CN-* 表（域名按后缀/关键词覆盖，IP 按网段包含，关键词/通配按原文）；
     被海外 App 表接管的条目（仓库 v4 把海外 App 误收进国内，如 Tableau/Speedtest）单列报告，不算遗漏；
  3. 可追加额外文件（如主配置）检查内联规则。
用法：python3 apps/coverage_check.py [额外配置文件...]   未覆盖条目输出到 stdout，存在时退出码 1。"""
import glob, os, re, sys, ipaddress
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTL = ['ai', 'protect-ai', 'google', 'protect-google', 'tiktok', 'protect-tiktok', 'stream', 'protect-stream', 'global',
        'protect-global', 'uk', 'protect-uk', 'paypal', 'protect-paypal', 'wise', 'protect-wise', 'binance', 'protect-binance', 'okx', 'protect-okx']
def load(f):
    out = []
    for l in open(f, encoding='utf-8'):
        l = l.strip()
        if not l or l[0] == '#': continue
        p = l.split(',')
        if len(p) > 1: out.append((p[0], p[1].lower()))
    return out
def index(cn):
    sfx, ex, kw, raw, nets = {}, {}, {}, {}, []
    for f in sorted(glob.glob(os.path.join(ROOT, 'dist', 'apps', '*.list'))):
        a = os.path.basename(f)[:-5]
        if a.startswith('CN-') != cn or a == 'CN-Reject': continue
        for t, v in load(f):
            {'DOMAIN-SUFFIX': sfx, 'DOMAIN': ex, 'DOMAIN-KEYWORD': kw}.get(t, {})[v] = a
            raw[(t, v)] = a
            if t in ('IP-CIDR', 'IP-CIDR6'): nets.append((ipaddress.ip_network(v, strict=False), a))
    return sfx, ex, kw, raw, nets
sfx, ex, kw, raw, nets = index(False)
def cov(t, v):
    if t == 'DOMAIN' and v in ex: return ex[v]
    if t == 'DOMAIN-KEYWORD': return kw.get(v)
    if t in ('DOMAIN', 'DOMAIN-SUFFIX'):
        ps = v.split('.')
        for i in range(len(ps)):
            if '.'.join(ps[i:]) in sfx: return sfx['.'.join(ps[i:])]
        for k in kw:
            if k in v: return kw[k]
    return None
miss = []
for c in INTL:
    p = os.path.join(ROOT, 'dist', 'v4', c + '.list')
    if not os.path.exists(p): continue
    for t, v in load(p):
        if t in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD') and not cov(t, v): miss.append(f'{c}\t{t},{v}')
# ---- 国内：cn.list 每条都要归属某个 CN-* 表 ----
I_IDX = (sfx, ex, kw, raw, nets)
sfx, ex, kw, raw, nets = index(True)
def cov_any(t, v):
    if t in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD'): return cov(t, v)
    if t in ('IP-CIDR', 'IP-CIDR6'):
        n = ipaddress.ip_network(v, strict=False)
        return next((a for m, a in nets if m.version == n.version and n.subnet_of(m)), None)
    return raw.get((t, v))
cn_rules = load(os.path.join(ROOT, 'dist', 'v4', 'cn.list'))
cn_ok, intl_over, owners = 0, [], {}
for t, v in cn_rules:
    a = cov_any(t, v)
    if a: cn_ok += 1; owners[a] = owners.get(a, 0) + 1; continue
    sfx, ex, kw, raw, nets = I_IDX
    b = cov(t, v) if t in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD') else None
    sfx, ex, kw, raw, nets = index(True)
    if b: intl_over.append(f'{t},{v}\t→ {b}')
    else: miss.append(f'cn\t{t},{v}')
print(f'cn.list：{len(cn_rules)} 条，{cn_ok} 条落入 {len(owners)} 个 CN-* 表；{len(intl_over)} 条由海外 App 表接管：')
for x in intl_over: print('   ', x)
sfx, ex, kw, raw, nets = I_IDX
SKIP = {'"🍎 Apple兜底"', '🍎 Apple兜底',  # Apple 条件分流（AND GEOIP）有意保留在配置内联
        'DIRECT', 'REJECT', 'REJECT-DROP', 'REJECT-TINYGIF', 'REJECT-NO-DROP'}
for conf in sys.argv[1:]:
    for l in open(conf, encoding='utf-8'):
        m = re.match(r'^(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD),([^,]+),([^,\n]+)', l.strip())
        if m and m.group(3).strip() not in SKIP and not cov(m.group(1), m.group(2).lower()):
            miss.append(f'{os.path.basename(conf)}\t{m.group(1)},{m.group(2)}\t-> {m.group(3)}')
ex_p = os.path.join(ROOT, 'apps', 'coverage_exempt.txt')
exempt = {l.rstrip('\n') for l in open(ex_p, encoding='utf-8') if l.strip() and not l.startswith('#')} if os.path.exists(ex_p) else set()
miss = [x for x in miss if x not in exempt]
print('\n'.join(miss) if miss else f'OK: 全部覆盖（豁免 {len(exempt)} 条，见 apps/coverage_exempt.txt）')
sys.exit(1 if miss else 0)
