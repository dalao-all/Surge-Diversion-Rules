# CHANGELOG — MESL Surge V6.0

日期：2026-09-16（Asia/Shanghai）

## 相对 V5.3

- RULE-SET raw URL 固定为 `dalao-all/Surge-Diversion-Rules`（`update-interval=86400`）；注释允许本地相对路径。
- 财务软件第 2 页写入 `patches/app_catalog.yaml`：欧易 OKX、Bybit、Bybit EU、UU Wallet、Plasma One（用户拼写 plamma one→Plasma One）、Bitget Wallet、PayPal、Authenticator（按 Google Authenticator 假设，不编造未核实域名）、Wise。
- 策略提示对齐：OKX/UU/Plasma/Bitget/Wise→🪙 数字资产；Bybit→💳 Bybit 全球；Bybit EU→🇩🇪 Bybit 欧洲；PayPal→💰 PayPal；Authenticator→与 Google/AI 登录亲和。
- 正式 `patches/interest_seed.json`；`interest_seed_from_apps.json` 改为溯源说明可选。
- 新增 `docs/GETTING_STARTED.zh.md`；目录改为 `profiles/` + `patches/` + `docs/` + `scripts/` + `.github/workflows/`。
- GitHub Actions `mesl-interest-bot.yml`：cron `0 1,13 * * *` UTC（= 09:00/21:00 CST）；`workflow_dispatch`；`daily_patch_bot.py --mode pr --fetch-upstream`；`GITHUB_TOKEN` 开 PR，无候选 no-op 成功。
- AdBlock 模块版本升 V6.0；MITM/脚本范围不扩大。
- `regression_cases.json` 覆盖财务第 2 页 + Claude / TikTok / B站 / 微信 / 支付宝 / YouTube。
- 保留：轻 MITM、patches 先于 SKK reject、`tobapplog.tobsnssdk.com`、无死后 pangle 放行、AppsFlyer 金融前缀在 list、脱敏订阅。

## 继承自 V5.3（相对 V5.2 修订 2）

- 补前置 `tobapplog`；删除无效 pangle 放行；关键例外 RULE-SET 化；Bybit EU/Global 伴生极小 list；兴趣驱动维护骨架。
