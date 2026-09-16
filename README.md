# Surge Diversion Rules（MESL）

公开仓库：**规则集 + 去敏感分享配置**。别人可以 fork / 直接用分享版；**不含任何订阅密钥**。

仓库地址：https://github.com/dalao-all/Surge-Diversion-Rules

## 别人怎么用（分享版）

1. 下载 [`profiles/MESL-Surge-V6.0.share.conf`](profiles/MESL-Surge-V6.0.share.conf)
2. 下载 [`profiles/MESL-AdBlock-V6.0.sgmodule`](profiles/MESL-AdBlock-V6.0.sgmodule)
3. 用文本编辑器打开 conf，把  
   `https://subscription.example.invalid/REPLACE_WITH_YOUR_SUBSCRIPTION`  
   换成**自己的** Surge 订阅链接
4. 导入 Surge，并安装模块

规则与去广告脚本均指向本仓库：

- `mirrors/skk/` — 自有镜像（原 SKK 列表）
- `mirrors/scripts/` — 自有镜像（AdBlock 脚本）
- `patches/` — 关键例外补丁（AI / 金融等）

## 目录

| 路径 | 说明 |
|------|------|
| `profiles/*.share.conf` / `*.sgmodule` | 去敏感分享配置（可公开） |
| `mirrors/` | 自有规则/脚本镜像 |
| `patches/` | 小型补丁集 |
| `docs/` / `scripts/` | 维护说明与同步工具 |

## 更新

维护者会定期把上游变更同步进 `mirrors/` / `patches/`，并保持分享版 conf 与之一致。  
**带真实订阅的私用配置永不提交本仓库。**

> 仅供技术交流与个人学习。不是代理服务，不提供节点。
