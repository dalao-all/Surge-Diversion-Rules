# mirrors：历史镜像与兼容路径

> **历史兼容目录，不是 Surge V3.0.0 的规则发布入口。** 当前配置见 [`profiles/surge-V3.0.0.conf`](../profiles/surge-V3.0.0.conf)，规则位于 [`dist/v4/`](../dist/v4/)，维护见[维护手册](../docs/MAINTENANCE.md)。本目录旧路径不保证每日更新。

保留这些文件是为避免旧配置断链并提供历史对照；不要把“路径还存在”理解为内容仍与上游现网一致。

- `skk/`：历史 SKK 列表缓存与来源映射，保持 `List/domainset|non_ip|ip/...` 结构；旧 SOURCE_MAP 记录的是当时的获取信息。
- [`owned/`](owned/README.md)：旧 v6.x 的兴趣精简 reject 与 tombstones 产物。它不是完整上游，也不是当前广告表。
- `blackmatrix7/`：旧配置使用过的列表镜像，供历史核对。
- `scripts/`：旧 AdBlock 模块引用的脚本镜像。当前版本不要求安装该模块。

当前引擎从 `rulekit_v4/sources.json` 获取登记来源，经验证后生成 `dist/v4/`。旧目录和脚本继续保留兼容，历史维护作业改为按需手动运行；不要误将旧脚本输出覆盖当前目录。旧配置使用者应检查实际引用路径和各自的更新结果。
