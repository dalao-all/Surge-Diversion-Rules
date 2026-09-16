中文 | [English](https://github.com/dalao-all/Surge-Diversion-Rules-EN)

# 你的订阅 Surge V6.0 — 分流规则

我维护的 **Surge 策略 / 规则集**公开仓库：自有镜像、小型补丁、去敏感分享配置与规则可视化。  
**本项目不含任何订阅密钥或节点。** 仅供技术交流与个人学习；不是代理服务，也不提供接入。

- 描述页：[`index.html`](./index.html)
- 交互规则图：[`rule-map.html`](./rule-map.html)
- 规则分层说明：[`docs/RULES_OVERVIEW.zh.md`](docs/RULES_OVERVIEW.zh.md)
- 入门：[`docs/GETTING_STARTED.zh.md`](docs/GETTING_STARTED.zh.md)

![规则图预览](assets/rule-map-preview.png)

## 安装（分享版）

1. 下载我提供的 [`profiles/Your-Subscription-Surge-V6.0.share.conf`](profiles/Your-Subscription-Surge-V6.0.share.conf)
2. 下载 [`profiles/Your-Subscription-AdBlock-V6.0.sgmodule`](profiles/Your-Subscription-AdBlock-V6.0.sgmodule)
3. 用文本编辑器打开 conf，把  
   `https://subscription.example.invalid/REPLACE_WITH_YOUR_SUBSCRIPTION`  
   换成你自己有权使用的 Surge 订阅链接；按需把 `your-subscribe-host.example` 换成你的订阅域名
4. 导入 Surge，并安装模块；手动更新「📦 你的订阅」

规则与去广告脚本均指向本仓库：

| 路径 | 我放什么 |
|------|----------|
| `mirrors/skk/` | SKK 公开列表的自有镜像 |
| `mirrors/scripts/` | AdBlock 脚本自有镜像 |
| `mirrors/blackmatrix7/` | 历史远程 list 镜像（对照用） |
| `patches/` | 关键例外补丁（AI / 金融 / DIRECT / ads） |
| `profiles/` | 去敏感分享 conf + 模块 |
| `docs/` / `scripts/` | 说明文档与维护脚本 |

## 规则分层（摘要）

匹配自上而下。我把规则分成四层，详细见 [`docs/RULES_OVERVIEW.zh.md`](docs/RULES_OVERVIEW.zh.md)：

1. **patches/** — 关键前置例外（必须先于广告底座）
2. **mirrors/skk/** — 主体分流与广告索引
3. **mirrors/scripts/** — 模块用的去广告脚本
4. **主 conf 内联例外** — 不宜进 list 的精确域名 / 协议规则

`rule-map.html` 用交互图表达同一套策略组意图与匹配顺序，便于对照学习。

## 策略组意图（摘要）

| 组 | 意图 |
|----|------|
| 🤖 AI住宅 | 敏感 AI / 身份业务，家宽优先 |
| 🎵 TikTok | 美国机房 Smart，排除家宽与低倍 |
| 🪙 / 💳 / 🇩🇪 / 💰 | 数字资产与支付分区出口 |
| 🎬 流媒体 | 高带宽 Smart |
| 🌍 国际网络 | 通讯与一般国际兜底 |
| DIRECT / REJECT* | 国内直连与广告/泄漏防护 |

## 目录

| 路径 | 说明 |
|------|------|
| `profiles/*.share.conf` / `*.sgmodule` | 我提供的去敏感分享配置 |
| `mirrors/` | 自有规则 / 脚本镜像 |
| `patches/` | 小型可审计补丁 |
| `docs/` | 中文文档 |
| `scripts/` | 兴趣驱动同步工具 |
| `index.html` / `rule-map.html` / `assets/` | 说明页与规则图 |

## 更新

我会把上游变更同步进 `mirrors/` / `patches/`，并保持分享版 conf 与之一致。  
**带真实订阅的私用配置我不会提交本仓库。**

> 仅供技术交流与个人学习。不是代理服务，不提供节点。请遵守当地法律与 GitHub 条款。
