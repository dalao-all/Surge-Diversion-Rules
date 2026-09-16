# MESL Surge V6.0

日期：2026-09-16（Asia/Shanghai）

脱敏分享副本：订阅为占位地址，**必须自行替换**才能加载节点。

> **免责声明**：本仓库仅供技术交流与个人网络调试学习，**不是**代理服务、机场推广或任何形式的商业代理产品。请遵守当地法律法规与服务条款；风险自负。

## 目录

```
profiles/MESL-Surge-V6.0.conf          # 主配置（脱敏订阅 + patches RULE-SET）
profiles/MESL-AdBlock-V6.0.sgmodule    # 日常去广告模块（MITM/脚本范围同 V5.3，仅升版）
patches/                               # 自有可审计 list（公开库可进；不整包上游）
  ai-critical.list
  finance-critical.list
  finance-bybit-eu.list / finance-bybit-global.list
  ads-patch.list / direct-patch.list
  manifest.json / selectors.yaml / upstream_watch.yaml
  app_catalog.yaml                     # App 兴趣目录（含财务第 2 页）
  interest_seed.json                   # V6.0 正式兴趣种子
  interest_seed_from_apps.json         # 溯源草案（可选）
docs/GETTING_STARTED.zh.md             # 小白向安装指南
docs/BOT_REQUIREMENTS.md
docs/INTEREST_MODEL.md
docs/MAINTENANCE.md
docs/APP_POLICY_MATRIX.md
scripts/daily_patch_bot.py
scripts/export_interest_seed.py
scripts/regression_cases.json
docs/github-actions/mesl-interest-bot.yml.example  # 09:00 & 21:00 Asia/Shanghai
CHANGELOG-V6.0.md
```

## 相对 V5.3 的变更摘要

1. **RULE-SET URL** 全部指向 `https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/<file>`（`update-interval=86400`）；注释说明也可改本地相对路径。
2. **财务第 2 页**写入 `app_catalog`：欧易 OKX、Bybit、Bybit EU、UU Wallet、Plasma One、Bitget Wallet、PayPal、Authenticator（按 Google Authenticator 假设）、Wise。
3. **正式 `interest_seed.json`**：合并 apps + 财务第 2 页 + critical domains；`interest_seed_from_apps.json` 保留为溯源。
4. **GitHub Actions** 兴趣机器人：UTC `0 1,13 * * *` = Asia/Shanghai 09:00 / 21:00；`workflow_dispatch` 可手动；用 `GITHUB_TOKEN` 开 PR，无候选则 no-op 成功。
5. **新手文档** `docs/GETTING_STARTED.zh.md`；README 中文为主。
6. **AdBlock** 仅版本升 V6.0，**不扩大** MITM/脚本。
7. 保留 V5.3 正确行为：轻 MITM、patches 在 SKK reject 前、`tobapplog`、无死后 pangle 放行、AppsFlyer 金融在 list、脱敏订阅。

未引入 AllInOne / Loyalsoldier / 第二套通用广告或分流底座。**禁止**整包拷贝 SKK / Loyalsoldier / AllInOne 进仓库。

## 快速开始

请读 **[docs/GETTING_STARTED.zh.md](docs/GETTING_STARTED.zh.md)**。摘要：

1. 导入 `profiles/MESL-Surge-V6.0.conf`，把 `policy-path` 占位换成你的真实订阅（**禁止**把真实 token 提交进公开库）。
2. 安装模块 `profiles/MESL-AdBlock-V6.0.sgmodule`；信任 Surge CA（仅在需要模块解密时）。
3. 确认 6 个 patches RULE-SET 可更新（或改本地 `RULE-SET,patches/xxx.list,...`）。
4. 日常**不要**开全局 MITM /「MITM 全部主机名」；保持「捕获流量」关闭。
5. 可选：打开仓库 Actions，启用 `mesl-interest-bot`。

## 维护（兴趣驱动）

每天 **Asia/Shanghai 09:00 / 21:00**（Actions cron：`0 1,13 * * *` UTC）拉取已引用频繁上游 → diff 新增 → seed/selectors 筛选 → 自有 list 候选 + PR。

```bash
python3 scripts/daily_patch_bot.py --mode pr --skip-fetch
python3 scripts/daily_patch_bot.py --mode pr --fetch-upstream
python3 scripts/export_interest_seed.py -o patches/interest_seed.draft.json
```

详情：[docs/MAINTENANCE.md](docs/MAINTENANCE.md) · [docs/INTEREST_MODEL.md](docs/INTEREST_MODEL.md) · [docs/BOT_REQUIREMENTS.md](docs/BOT_REQUIREMENTS.md)
