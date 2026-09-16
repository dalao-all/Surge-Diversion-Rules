# Surge Diversion Rules（仅规则集）

本仓库**只存放**可被 Surge `RULE-SET` / `DOMAIN-SET` 引用的规则列表与维护脚本。  
**不存放**完整 Surge 配置、订阅链接或 AdBlock 模块（那些只留在你自己的设备上）。

## 给 Surge 用的地址（合并进 main 后）

把主配置里的补丁引用写成（示例）：

```text
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ai-critical.list,"🤖 AI住宅",update-interval=86400
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/finance-critical.list,"🪙 数字资产",update-interval=86400
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/finance-bybit-eu.list,"🇩🇪 Bybit 欧洲",update-interval=86400
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/finance-bybit-global.list,"💳 Bybit 全球",update-interval=86400
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ads-patch.list,REJECT,update-interval=86400
RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/direct-patch.list,DIRECT,update-interval=86400
```

## 目录

- `patches/` — 自有小型规则集与兴趣种子（由上游增量筛选维护）
- `scripts/` — 兴趣更新机器人
- `docs/` — 维护说明（给维护者看）

## 更新方式

上游（如 SKK）有相关新增时，由维护机器人或助手**直接更新** `patches/` 并推送到 `main`，不要求仓库主人每天审 PR。

> 技术交流用途。不是代理服务，不提供节点。
