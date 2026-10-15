中文 | [English](https://github.com/dalao-all/Surge-Diversion-Rules-EN)

# Surge V3.0.0 分流规则

面向个人 Surge 配置的公开规则项目：按真实应用清单整理上游来源，生成可追溯的分流与保守域名去广告规则。**本仓库不含节点、订阅凭据或代理服务。**

**下载：[surge-V3.0.0.conf](profiles/surge-V3.0.0.conf)** · [入门](docs/GETTING_STARTED.zh.md) · [规则分层](docs/RULES_OVERVIEW.zh.md) · [164 项应用矩阵](docs/APP_POLICY_MATRIX.md) · [维护与回滚](docs/MAINTENANCE.md)

公开配置的 `[Proxy]` 为空，需要自行填入有权使用的节点，并核对策略组对节点名称的引用。`ipv6 = false`。仅导入空节点配置不能获得代理出口。当前方案不要求安装去广告模块，不使用 MITM 或 URL rewrite；仅专用 `ads-storm.list` 使用 pre-matching。

## 安装

1. 下载正式配置，在本地保存副本；按[入门说明](docs/GETTING_STARTED.zh.md)填写节点、检查策略组。
2. 导入 Surge，运行配置检查，更新外部资源。
3. 确认 24 个远程规则资源下载成功；在自己的设备上检查应用启动、登录、主要业务和实际出口。

`profiles/Surge-v4.template.conf` 仅保留为兼容别名。**用户版本是 V3.0.0；`rulekit_v4/`、`dist/v4/` 和工作流名称中的 v4 是内部引擎/产物路径，不是另一份用户版本。**

## 当前策略

- `ai`：美国住宅优先的 fallback，用于国外 AI 业务与必要的精确共享登录端点。
- `tiktok`：美国住宅优先的 fallback。
- `stream`：流媒体 Smart。
- `google`：Google账户select默认跟随AI；`global`：普通国际Smart；金融四项用固定select。
- `uk`：英国住宅优先，同国机房 fallback。
- `cn`：DIRECT。

上述均为配置意图，实际出口取决于用户配置的节点和可用性。保留的原住宅优先节点名称也需要与自己的节点对应。

## 规则与覆盖边界

运行时只引用 `dist/v4/` 的 **11 个分类保护表 + 1 个早拦表 + 1 个广告 DOMAIN-SET + 11 个应用分类表**。专用早拦优先于所有普通白名单，因此构建时排除全部现有与历史保护范围。其余普通规则先匹配分类保护，再广告，再按 `ai / tiktok / stream / google / uk / global / cn` 分类，最后由主配置兜底。当前 191 条业务保护规则既进入前置保护表，也从广告表物理清除相交项；历史保护范围保留以减轻资源下载时间不同带来的误拦。

应用清单来自 [`rulekit_v4/apps.json`](rulekit_v4/apps.json)：CN001–CN132 与 INT001–INT032，共 **164 个稳定 ID**；114 个登记来源、28 个共享依赖。包含 **13 个 unresolved 和 5 个 local-only** 项，其他行也仅表示来源或服务候选。共享集团域、官方网站与浏览器目标站分流都不等于单个应用全业务覆盖。

编译器回归测试与当前 210 个真实域名的静态路由探针用于发布门禁；它们不证明手机端启动、登录、通话、付款或节点出口已经实测通过。规则总量随上游变化，查看当前 [report.json](dist/v4/report.json)，不以文档里的旧数量作承诺。

## 自动维护

- 中文仓库：计划每天北京时间 **05:37** 锁定上游版本并抓取、编译、验证，通过才发布。
- 英文仓库：计划每天北京时间 **06:07** 同步中文仓库已经验证的快照，不独立抓一套上游，也不需要跨仓库 PAT。
- 健康检查：计划每天北京时间 **21:17** 检查近期成功运行记录。

GitHub 定时任务可能延迟或停用；失败时保留上次已发布产物，不能把计划时间当作每天成功更新的保证。详情、故障处理与回滚见[维护手册](docs/MAINTENANCE.md)。

## 文件入口

- [`profiles/`](profiles/README.md)：正式公开配置与历史兼容文件。
- [`rulekit_v4/`](rulekit_v4/README.md)：当前编译器、清单、来源、保护与探针。
- [`dist/v4/`](dist/v4/)：当前运行时规则、版本锁、差分报告与逐条溯源。
- [`index.html`](index.html)、[`rule-map.html`](rule-map.html)：发布说明页与交互规则图；配置和实际生成产物为最终依据。
- [`mirrors/`](mirrors/README.md)、`patches/`、`scripts/`、[`rulekit/`](rulekit/README-rulekit.md)：保留旧配置兼容与历史资料，不保证每日更新；旧版 v6.x 与模块不再作为推荐安装入口。

第三方规则权利与署名见 [`rulekit_v4/sources.json`](rulekit_v4/sources.json) 及 [`licenses/`](rulekit_v4/licenses/)。请勿提交带真实节点、订阅令牌或私有地址的配置。

## 本轮补充

金融四项为用户在原160项之后明确新增，总164项；24个新版资源含11保护、1早拦、1广告DOMAIN-SET、11功能。Google账户默认同AI实际出口。修复解释与后续手机验收见[审计记录](docs/REVIEW_FIXES.zh.md)。

[iPhone 请求密集与下载排障](docs/IOS_TROUBLESHOOTING.zh.md).
