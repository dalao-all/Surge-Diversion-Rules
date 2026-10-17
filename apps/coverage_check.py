#!/usr/bin/env python3
"""覆盖检查：dist/v4 中所有海外类条目必须被某个 dist/apps/<App>.list 覆盖；可追加额外文件（如主配置）检查内联规则。
用法：python3 apps/coverage_check.py [额外配置文件...]   未覆盖条目输出到 stdout，存在时退出码 1。"""
import glob, os, re, sys
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
sfx, ex, kw = {}, {}, {}
for f in glob.glob(os.path.join(ROOT, 'dist', 'apps', '*.list')):
    a = os.path.basename(f)[:-5]
    for t, v in load(f):
        {'DOMAIN-SUFFIX': sfx, 'DOMAIN': ex, 'DOMAIN-KEYWORD': kw}.get(t, {})[v] = a
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
SKIP = {'DIRECT', 'REJECT', 'REJECT-DROP', 'REJECT-TINYGIF', 'REJECT-NO-DROP'}
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
