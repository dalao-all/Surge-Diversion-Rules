# 2026-10-16 规则内容交叉核验

本次修改仓库规则与构建约束，保留用户手机 V3.3.0 的分流顺序、节点分组、IPv6 关闭及空 Proxy。内部编译器版本为 4.2.0，资源地址仍为 dist/v4。

## 修正范围

- 删除 OpenAI 上游的 AS20473 整网归类：该 ASN 是 Vultr 共享托管网络，并非 OpenAI 专网。删除六条过宽的 AI/TikTok 关键词匹配，以域名边界和明确服务端点替代。
- 根据 OpenAI、Claude 官方网络说明与 v2fly 分类交叉核验，补充认证、静态资源、内容服务及必要的精确 WorkOS 端点；不将整个共享 WorkOS 域名放行。新增补充源只接受本轮审查集合，上游未知增量进入遗漏报告等待复核。
- 将 Google 通用下载 gvt1.com 从流媒体归入 Google；将混入 TikTok 集的 TRAE 国际端点归入 AI，国内端点保留原分类。保护 Discord 的精确上传存储端点，避免被 googleapis.com 大后缀抢先匹配。
- 为天府通、无忧行、汽车之家、UU远程、交管12123、个人所得税补上官方站点或开发者隐私页可证实的域名，并关联应用清单。官网身份验证仅证明域名归属，不代表已穷尽 App 私有 API；覆盖状态仍为部分覆盖。
- 腾讯视频中 29 条 IPv4 映射 IPv6 的变化是相同地址的十六进制/点分表示差异。固定规范化表示后保留原变更阈值；另外剔除其中三条 198.18.0.0/15 基准测试网段映射地址，它们不能作为腾讯业务归属证据。
- 重新抓取所有启用远程源并固定提交。广告源本轮增加 688、删除 278，净增 410；更新未绕过 PSL、保护规则、数量变化与业务探针检查。

## 三轮核验

1. 来源与归属：比较 blackmatrix、Sukka、v2fly、AWA 清单，结合厂商文档与 App 开发者/官方隐私页核实争议项。来源可能相互引用，不把同源复制当独立证据。
2. 广告反向核验：下载 AdGuard 官方 DNS 过滤表，限定比较无修饰的 184315 条后缀拦截与 11 条例外。当前 141417 条广告规则中，128196 个域名见证也被其简单后缀覆盖；没有覆盖的规则不因此认定为错误。两个 TVB 例外候选暂不放行，因为不在用户应用范围且用途证据不足。没有把 ABP 正则、修饰符或整份列表直接转换合并。
3. 结果核验：237 个静态业务/广告探针、8 个反向域名探针、69 项解析与失败隔离测试、完整资源校验；同时检查旧版广告优先与用户 V3.3.0 业务优先的业务命中结果。原生 Surge 语法验收使用临时虚构节点，不导出用户凭据、不连接节点。

## 明确限制

V3.3.0 业务规则排在广告之前，本轮沿用该顺序。18 个旧广告样本中有 17 个被业务规则先命中，包括此前的重试域名。这是既有兼容性取舍，不能声称这些请求在手机上会被广告表拦截。详细结果见 dist/v4/content-audit.json。

自动校验覆盖全部导出行的语法、范围、来源和冲突处理；并不等于人工查明 14 万个域名的每个业务用途。没有 iPhone 实机登录、视频、耗电或速度验收。未知小众应用及加密流量中未观察到的域名仍需实际请求记录补证。每日更新遇到失败保留上一版，并不承诺外部服务永不出错。

## 证据与可追溯文件

- [Vultr AS20473](https://docs.vultr.com/products/network/bgp/asn-information/as20473)
- [OpenAI 网络要求](https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps)
- [Claude Desktop 网络要求](https://code.claude.com/docs/en/desktop#network-access-requirements)
- [Google Chrome 下载地址](https://support.google.com/chrome/a/answer/6334001)
- [Google Gemini API](https://ai.google.dev/api/models)
- [IANA 特殊 IPv4 网段](https://www.iana.org/assignments/iana-ipv4-special-registry/iana-ipv4-special-registry.xhtml)
- [AdGuard DNS 规则源](https://github.com/AdguardTeam/AdGuardSDNSFilter)

逐项理由与链接：rulekit_v4/content-review.json；应用归属：rulekit_v4/apps.json；源提交与校验和：dist/v4/sources.lock.json；逐规则来源：dist/v4/provenance.ndjson.gz；实际分类：dist/v4/content-audit.json。以上内容由构建结果与审查记录共同提供，不将文档宣传当验证证据。
