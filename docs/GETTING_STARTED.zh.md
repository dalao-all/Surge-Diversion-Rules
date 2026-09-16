# MESL Surge V6.0 — 小白向入门

时区说明：下文「每天 09:00 / 21:00」指 **Asia/Shanghai（CST，UTC+8）**。  
GitHub Actions 的 cron 写成 UTC：`0 1,13 * * *` = 北京时间 09:00 与 21:00。

> 免责声明：本配置仅供技术交流与个人学习调试，不是代理服务。请遵守当地法律与各平台条款。

---

## 你需要准备什么

1. 已购买并安装 **Surge iOS / Mac**（本配置面向 iOS 日常使用说明为主）。
2. 一份可用的 **Surge 专用节点订阅**（机场提供的 `policy-path` 链接）。
3. （可选）GitHub 账号，用于拉取本仓库或开启自动维护 Actions。

---

## 第一步：导入主配置

1. 打开本仓库的 `profiles/MESL-Surge-V6.0.conf`（或已发布到 GitHub raw 的同名文件）。
2. 在 Surge 中：**配置 → 导入**（或「从 URL 下载」）。
3. 导入后先不要急着开代理：先改订阅（下一步）。

---

## 第二步：替换订阅占位（必须）

主配置里有类似一行：

```text
📦 MESL节点 = select, policy-path=https://subscription.example.invalid/REPLACE_WITH_YOUR_SUBSCRIPTION, update-interval=-1
```

把 `https://subscription.example.invalid/REPLACE_WITH_YOUR_SUBSCRIPTION` **整段**换成你自己的真实订阅 URL。

**重要安全规则：**

- **禁止**把含真实 token / 订阅密钥的配置提交到公开 GitHub。
- 公开仓库里的主配置必须保持脱敏占位；真实文件只放在本机 / iCloud 私有位置。
- 若你 fork 本仓库，请用 Surge 本地覆盖或私有 gist，不要把 token 推进 PR。

改完后：Surge → 外部资源 / 策略组 → 手动「更新」`📦 MESL节点`，确认节点列表非空。

---

## 第三步：安装去广告模块

1. 安装 / 启用 `profiles/MESL-AdBlock-V6.0.sgmodule`（本地文件或 raw URL）。
2. 模块提供 B站/酷安开屏、淘宝/京东/小红书/高德等**精确**去广告；**不会**扩大到「MITM 全部主机」。
3. 主配置本身保持轻 MITM（空主机名单 + 由模块按需追加）。

---

## 第四步：信任 CA（仅在需要模块解密时）

若模块要改写 HTTPS 正文，Surge 会要求安装并信任其 CA 证书：

1. Surge → MITM → 生成/安装 CA。
2. 系统设置中对 Surge CA 选择「信任」。
3. **日常不要**开启「捕获流量」或「MITM 全部主机名 / capture override *`」。
4. 排障抓包时再临时打开捕获；用完关闭。

不需要解密的功能（纯分流）可以不装 CA，但模块里依赖 MITM 的去广告会失效。

---

## 第五步：确认 patches RULE-SET

主配置在 SKK 广告拒绝规则**之前**引用 6 个自有 list，例如：

```text
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ai-critical.list,"🤖 AI住宅",update-interval=86400
```

- 默认从 GitHub raw 每天最多更新一次（86400 秒）。
- 若你使用 iCloud/本地目录，可改成相对路径，例如：

```text
RULE-SET,patches/ai-critical.list,"🤖 AI住宅",update-interval=86400
```

（需保证 Surge 能解析到该相对路径。）

在 Surge 执行「配置检查」，确认无红色错误。

---

## 第六步：打开 GitHub Actions（可选）

若你使用本仓库的公开维护流：

1. GitHub → Actions → 启用 workflows。
2. 找到 `mesl-interest-bot`：每天北京时间 09:00 / 21:00 自动跑；也可 `Run workflow` 手动触发。
3. 机器人会：`checkout` → `python3 scripts/daily_patch_bot.py --mode pr --fetch-upstream` → 有候选时用 `GITHUB_TOKEN` 开 PR；**无候选则成功退出（no-op）**。
4. 合并 PR 前请人工看一眼；不要无脑点 Merge。

时区换算备忘：

| Asia/Shanghai | UTC（cron） |
|---------------|-------------|
| 09:00         | 01:00       |
| 21:00         | 13:00       |
| cron 表达式   | `0 1,13 * * *` |

---

## 日常使用注意

| 建议 | 原因 |
|------|------|
| 不要开全局 MITM | 费电、费内存、易踩证书坑；本方案是轻 MITM |
| 不要开「捕获流量」日常常开 | 同上 |
| 不要提交真实订阅 token | 泄露等于节点被盗用 |
| 不要整包拷贝 SKK/Loyalsoldier/AllInOne 进仓 | 仓库只维护自有小型 patches |
| pangle / tiktokpangle 广告域不要手写放行 | 应交交广告集拒绝 |

冒烟可对照 `scripts/regression_cases.json`（Claude、TikTok、B站、微信、支付宝、YouTube、财务第 2 页等）。

---

## 还需要读什么

- 维护日程与门禁：`docs/MAINTENANCE.md`
- 兴趣如何判定：`docs/INTEREST_MODEL.md`
- 机器人规格：`docs/BOT_REQUIREMENTS.md`
- App → 策略矩阵：`docs/APP_POLICY_MATRIX.md`
