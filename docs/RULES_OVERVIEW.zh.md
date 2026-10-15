# surge-V3.0.0 规则顺序与出口

[正式配置](../profiles/surge-V3.0.0.conf) · [应用矩阵](APP_POLICY_MATRIX.md) · [审计修复](REVIEW_FIXES.zh.md) · [维护](MAINTENANCE.md)

配置按首条命中处理，资源固定在dist/v4，内部引擎4.1.0不改变文件名版本。新版23个挂载为11个保护RULE-SET、1个广告DOMAIN-SET、11个功能RULE-SET；ads.list继续作为旧配置兼容导出。广告域名表与兼容表必须完全同义。

顺序：本地网络 → 各类关键业务保护 → 广告 → 应用功能 → CN/GEOIP/FINAL。分类依次paypal / wise / binance / okx / ai / tiktok / stream / google / uk / global / cn。

| 分类 | 实际策略 |
| --- | --- |
| paypal | 固定select，美国12家宽默认 |
| wise / binance / okx | 各自固定select，台湾07家宽默认 |
| ai / tiktok | 各自美国住宅fallback |
| stream | 流媒体Smart |
| google | Google账户select，默认跟随AI实际组 |
| uk | 英国住宅优先、同国机房fallback |
| global | 国际Smart，含普通Meta |
| cn | DIRECT |

节点国家只来自原标签，不等于已测出口。Proxy空白，IPv6=false，填入自己的节点后使用。Google登录、oauth2、Gmail、Drive、搜索默认同一账户组，AI Studio精确AI，YouTube视频仍stream。

apps.json登记164项（原160＋本轮新增4金融）、114来源、28依赖。13项unresolved与5项local-only不编造域名。源存在不等于全覆盖；浏览器按目标站分流，未知目标由兜底处理。

旧allow.list的67条业务例外逐条迁移并验证。保护历史单调保留，广告表物理剔除与新旧保护范围相交项。233条WeChat数字关键词按明确/24纠正，原行、原因、输出类别保存在provenance.ndjson.gz。输出修正不改上游原规则集合的差分基线。

report.json记录201静态探针、各表数量、旧例外迁移和源修正；sources.lock.json固定源commit/hash；source-rules.json保留解析后的源语义；SHA256SUMS覆盖23个兼容RULE-SET导出与广告DOMAIN-SET。57项引擎/健康回归和9项同步回归仍不能代替手机业务验收。

旧v6.x、rulekit、mirrors、patches、modules保留历史兼容，旧自动写入改手动，不再是当前安装入口。新增出口国家、节点命名或DNS仍可能需要改主配置。
