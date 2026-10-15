#!/usr/bin/env python3
"""Validate the published files against the exact public main-profile layout."""
import gzip, hashlib, json, re
from pathlib import Path
from build import CATEGORIES, ROOT, BuildError, normal_rule

def validate(root=ROOT):
    dist=root/'dist/v4'; profile=(root/'profiles/Surge-v4.template.conf').read_text()
    section=''; routes=[]
    policies={'ai':'🤖 AI住宅','tiktok':'🎵 TikTok住宅','stream':'🎬 流媒体','google':'🌍 国际网络','uk':'🇬🇧 英国专属','global':'🌍 国际网络','cn':'DIRECT','ads':'REJECT'}
    for raw in profile.splitlines():
        line=raw.strip()
        if line.startswith('['): section=line
        if not line or line.startswith(('#',';','//')): continue
        if section=='[Proxy]' and '=' in line: raise BuildError('Public template must contain no node definitions')
        if section=='[Rule]' and line.startswith('RULE-SET,https://'):
            parts=line.split(','); url=parts[1];name=url.rsplit('/',1)[-1]
            if not url.startswith('https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/dist/v4/'): raise BuildError('Unexpected resource origin')
            if not (dist/name).is_file(): raise BuildError('Missing external resource '+name)
            if 'pre-matching' in parts: raise BuildError('V4 deliberately forbids pre-matching rejection')
            key=name.removesuffix('.list')
            category=key.removeprefix('protect-')
            if len(parts)<3 or parts[2]!=policies.get(category): raise BuildError('Wrong profile policy for '+name)
            routes.append(key)
    expected=['protect-'+c for c in CATEGORIES]+['ads']+list(CATEGORIES)
    if routes!=expected: raise BuildError(f'Profile/compiler routing order mismatch: {routes}')
    count=0
    for name in expected:
        for raw in (dist/(name+'.list')).read_text().splitlines():
            if not raw.strip() or raw.startswith('#'): continue
            parts=raw.split(',');normal_rule(parts[0],parts[1],parts[2:]);count+=1
    checks=(dist/'SHA256SUMS').read_text().splitlines()
    names=[line.split('  ')[-1] for line in checks]
    if sorted(names)!=sorted(c+'.list' for c in expected): raise BuildError('Incomplete/duplicate checksum manifest')
    for line in checks:
        digest,name=line.split('  ')
        if hashlib.sha256((dist/name).read_bytes()).hexdigest()!=digest: raise BuildError('Hash mismatch '+name)
    report=json.loads((dist/'report.json').read_text())
    if not report['probes'] or not all(p['passed'] for p in report['probes']): raise BuildError('Probe report failed or empty')
    if re.search(r'(?im)^.*password\s*=\s*[^\s#]+',profile): raise BuildError('Possible password in template')
    print(f'PASS: 15 public resource links, {count} rules, {len(report["probes"])} probes, SHA256, profile ordering and no public node definitions')
if __name__=='__main__': validate()
