# surge-V3.0.0 规则维护（内部引擎 v4）

手机端下载 `profiles/surge-V3.0.0.conf`。IPv6 已禁用，`[Proxy]` 按要求留空；填入自己的节点，并确认策略组引用的节点名称对应后使用。对外文件名与内部 v4 引擎/资源路径独立，当前主配置引用 24 个资源地址。

## 固定的手机配置

24 个自有远程规则资源（23 个 RULE-SET 与 1 个 DOMAIN-SET）：11 个关键业务保护表、1 个早拦表、1 个 DOMAIN-SET 广告表、11 个应用分类表。按 paypal / wise / binance / okx / ai / tiktok / stream / google / uk / global / cn 的顺序匹配，普通保护表先于完整广告表。专用早拦表使用 `REJECT-DROP,pre-matching`，优先于普通白名单，因此生成器必须排除全部当前及历史保护范围，并只保留最终广告表命中的精确域名。Google账户默认跟随AI当前出口。空的保护表保留固定 URL，后续可以只更新 GitHub 增加例外。

## 新增、删除与修正规则

- `apps.json` 是完整 164 项清单。把 `enabled` 改为 false 会移除仅由此应用引用的规则；共享依赖仍由其他应用保留，未知流量仍由 FINAL 处理。
- 新增应用：添加稳定 ID、category、source_ids/dependency_ids，向 `sources.json` 登记其来源和许可证，向 `probes.json` 添加已知真实业务端点。没有可信源时明确写缺口，不编造域名。
- 出口类别调整：同时核对应用 category 和所引用 source 的 category；共享来源不能任意按单一应用改出口。十一类之外的新出口需要改手机配置。
- 人工补域名放 `custom/*.list` 并登记 source；只有 manifest 引用的文件进入构建。共享云供应商不是某一个 App 的完整域名表。
- 紧急误拦：把有业务证据的精确主机或最小后缀加入 `protection.json` 对应类别。构建器会从广告表物理移除所有与当前和历史保护范围相交的广告规则。历史保护范围单调保留，避免不同时间下载的资源相互冲突。不要随意清空 `protected-history.json`。
- `exclude_rules` 只用于有说明的精确上游规则排除，原文/原因会进入报告。全集团白名单和裸关键词广告均不自动接受。

## 自动更新

`.github/workflows/rulekit-v4.yml` 每天北京时间 05:37 运行，也可从 Actions 手动 Run workflow。GitHub 的定时任务可能延迟，并非时刻保证。没有日常 AI 调用。

每次先锁定每个上游仓库的单一 commit，再并发下载、解析、检查 PSL、广告冲突、来源集合变化和真实域名探针。失败不会 push 产物，手机继续使用上一已发布版本。关键来源失败直接阻断，不用过期缓存假装更新成功。`--offline` 仅用于本地重放最后完整验证的缓存。

新规则有效项的增加/删除过大、同量全替换、空表、未知格式、关键探针失败均需检查原因。确认大规模变化属于正常迁移时，通过一次明确的人工审查提交更新相应 `dist/v4/source-rules.json` 基线，而不是使用跳过语法检查的 force 开关。

正常更新提交 dist/v4 和由真实清单生成的 repository-status.json；推送前比较输入 commit 与 main 最新 HEAD，不做盲目 rebase。没有变化时不改规则文件时间戳。`sources.lock.json` 的上游 commit/hash 可能因上游头提交改变，运行时 list 内容保持稳定。

`.github/workflows/rulekit-v4-health.yml` 在更新工作流完成后以及每天北京时间 21:17 检查最近 36 小时是否有成功运行；部署时不再与首次构建抢跑，最近更新失败不会被旧成功记录掩盖；失败显示为 Actions 红色检查。它仍依赖 GitHub 调度，不能检测整个平台或账号调度共同停用。通知是否送达取决于账号通知设置；公开仓库长期无活动可能需要恢复定时任务。

## 本地验证

```sh
python3 -m unittest discover -s rulekit_v4 -p 'test_*.py' -v
python3 rulekit_v4/build.py
python3 rulekit_v4/validate_release.py
```

只使用 Python 标准库与 git。首次构建需要网络。首次云端发布还必须匹配 bootstrap.json 中的本地审查语义哈希；已有产物后以最近发布的逐源基线为准。已验证缓存可以 `python3 rulekit_v4/build.py --offline` 重放。构建缓存不提交。

`dist/v4/report.json` 有匹配结果、排除项与跨类别遮蔽的具体域名证据；`provenance.ndjson.gz` 可解压逐条追溯源 URL、行号、原规则、所属应用、是否最终发布。`sources.lock.json` 与 `source-rules.json` 提供版本/hash与语义差分基线。PSL固定版本见 `data/psl-source.json`，更新需单独审查。

静态探针只验证规则命中，不证明应用业务、住宅出口或所有动态域名已实际可用。浏览器按目标站分流；未知/本地工具的覆盖缺口保存在清单中。v2 regexp、iOS无法可靠使用的进程规则与明确排除项都进入报告。

## 回滚

从 Git 历史选择最近已验证的 v4 产物提交，在新提交中恢复其 dist/v4 列表、lock/source-rules/report/溯源文件。回滚时必须把当前 protected-history 与旧版本合并，并重新构建，避免旧广告表恢复已修复的误拦。不要 reset --hard/force push 覆盖其他人的更新。发布后在手机更新外部资源。

旧版 rulekit/mirrors/modules/patches 继续保留兼容；旧自动工作流已改为手动运行，与当前 v4 自动更新路径隔离。英文仓库每天北京时间06:07从中文仓库已验证快照同步引擎/规则，保留英文说明；不需要跨仓库PAT。

## 许可与来源

编译器/自写规则与第三方数据分开归属。上游许可证与通知保存在 `licenses/`、`sources.json` 与发布 lock 中；生成表按来源保留相应权利和署名，不声明统一占有第三方数据。

## 审计修复

原160项之外，按本轮要求新增PayPal、Wise、Binance、OKX（INT029—INT032），共164项。金融固定select，Google账户默认跟随AI实际出口。233条微信数字关键词改为精确/24，属于有意纠正匹配范围。旧allow.list的67条例外逐项迁移并作为构建门禁。ads.domainset用于新版，ads.list继续兼容旧版。详见docs/REVIEW_FIXES.zh.md。

[iPhone 请求密集与下载排障](../docs/IOS_TROUBLESHOOTING.zh.md).
