# 公开配置

**正式下载：[`surge-V3.0.0.conf`](surge-V3.0.0.conf)** · [入门](../docs/GETTING_STARTED.zh.md) · [规则说明](../docs/RULES_OVERVIEW.zh.md)

正式配置 `[Proxy]` 为空、`ipv6 = false`，不含真实节点或订阅凭据。用户需要在本地填入节点，并核对策略组中保留的住宅优先等节点名称引用。空节点配置无法提供代理出口。

AI / TikTok 使用美国住宅优先 fallback，英国使用英国住宅优先和同国机房备选，Google账户默认跟随AI出口，global使用普通国际Smart，国内 DIRECT。实际节点与出口需要用户验收。

23 个运行时资源统一引用 `dist/v4/`；v4 是内部引擎路径，用户版本为 V3.0.0。`Surge-v4.template.conf` 保留为同内容兼容别名，建议新安装使用正式文件名。

当前方案不需要额外 AdBlock 模块，不使用 MITM、URL rewrite 或 pre-matching。旧 `Surge-v6.x.conf`、`Your-Subscription-*.conf` 与 `*.sgmodule` 留作历史兼容，不再主推，也不保证其旧规则路径每日更新。旧模块说明不适用于当前版本。

不要将填入真实节点、密码或订阅令牌后的本地配置提交公开仓库。
