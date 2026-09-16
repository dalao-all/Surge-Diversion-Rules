# mirrors/

本目录存放从上游公开规则源**原样镜像**的列表，便于后续把 Surge 配置里的远程 URL 改为本仓库 `raw.githubusercontent.com` 地址。

## mirrors/skk

- **来源**：`https://ruleset.skk.moe/List/...`（Sukka / SKK 公开规则集）
- **用途**：供 MESL Surge 等配置在第二步把 `ruleset.skk.moe` 引用改为自有 raw URL
- **同步**：由维护例程负责；内容应与现网 SKK 列表一致，不在此目录做语义改写
- **映射**：见同目录 `SOURCE_MAP.json`（`upstream_url` → `repo_relative_path` / sha256 / bytes / fetched_at）

路径保持 SKK 的 `List/domainset|non_ip|ip/...` 相对结构，与上游一一对应。

> STEP 1（本目录就绪）只做镜像；**第二步才会改用户配置里的 URL**。
