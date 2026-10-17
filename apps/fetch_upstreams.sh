#!/usr/bin/env bash
# 拉取全部上游到 $UPSTREAM_DIR（默认 ./.upstream），浅克隆 + 稀疏检出，并把实际使用的提交写入 dist/apps/sources.lock.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
UP="${UPSTREAM_DIR:-$ROOT/.upstream}"
mkdir -p "$UP" "$ROOT/dist/apps"
clone() { # name url sparse-paths...
  local name=$1 url=$2; shift 2
  rm -rf "$UP/$name"
  git clone -q --depth 1 --filter=blob:none --sparse "$url" "$UP/$name"
  if [ $# -gt 0 ]; then git -C "$UP/$name" sparse-checkout set "$@"; else git -C "$UP/$name" sparse-checkout disable; fi
}
clone v2fly   https://github.com/v2fly/domain-list-community.git data
clone bm      https://github.com/blackmatrix7/ios_rule_script.git rule/Surge
clone acl     https://github.com/ACL4SSR/ACL4SSR.git Clash/Ruleset
clone vpsd    https://github.com/VPSDance/ai-proxy-rules.git rules/surge
clone xiaolai https://github.com/xiaolai/anthropic-claude-surge-rules-set.git
clone sukka   https://github.com/SukkaW/Surge.git Source
mkdir -p "$UP/official"
curl -fsSL --retry 3 https://core.telegram.org/resources/cidr.txt -o "$UP/official/telegram-cidr.txt"
python3 - "$UP" "$ROOT/dist/apps/sources.lock.json" <<'PY'
import json, subprocess, sys, datetime
up, out = sys.argv[1], sys.argv[2]
lock = {}
for n in ['v2fly', 'bm', 'acl', 'vpsd', 'xiaolai', 'sukka']:
    g = lambda *a: subprocess.check_output(['git', '-C', f'{up}/{n}', *a], text=True).strip()
    lock[n] = {'url': g('remote', 'get-url', 'origin'), 'commit': g('rev-parse', 'HEAD'), 'date': g('log', '-1', '--format=%cs')}
lock['official:telegram'] = {'url': 'https://core.telegram.org/resources/cidr.txt', 'fetched': datetime.date.today().isoformat()}
json.dump(lock, open(out, 'w'), indent=1)
PY
echo "upstreams ready in $UP"
