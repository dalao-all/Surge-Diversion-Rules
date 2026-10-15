# 本轮用户审计：解释、修复与后续验收

对外配置为 surge-V3.0.0；内部引擎升级为4.1.0，v4资源路径不变。以下是已核实的问题及本次修复，不把静态命中当作手机业务已验收。

## 1. 金融固定出口

PayPal、Wise、Binance、OKX不在最初160项清单中，上一轮严格按清单整理时未独立收录。这次用户明确补充，登记为INT029—INT032，总164项。四个select组分别固定：PayPal默认原美国12家宽，另外三个默认原台湾07家宽。select不会因Smart测速而逐请求换国家；用户主动改选或节点自身出口变化仍会改变实际IP。国家只按现有节点标签选择，本次未连接手机验证，固定出口不保证账户风控结果。固定策略覆盖已知业务域名；未知或多应用共享的认证/CDN请求不能仅凭域名保证归属于某个金融App，仍需真实请求日志验收。

## 2. 流媒体泛域误伤

Netflix源的cookielaw.org、onetrust.com、us-west-2.amazonaws.com及Viki源的twemoji.maxcdn.com确实进入stream。明确排除整个AWS区域；公共同意管理/表情服务改普通国际策略。保留独立Netflix端点，不臆测整个AWS区域都属于Netflix。共享服务出现新专属子域后，以上游/实际请求证据再补。

## 3. 旧版保护迁移遗漏

旧allow.list未被完整作为迁移验收基线，确有回归。旧67条例外现逐条显式保留或记录有意改策略，并在每次构建检查首条命中。Meta相关例外使用普通国际组，Google认证使用统一账户组；这是保留业务同时作明确分类调整。

fengkongcloud恢复CN业务保护；Substack、msedge.net、FossHub、openinstall.io移除整域广告误拦。B站国际域和两个upos-bstar视频CDN移流媒体，国内B站继续CN。statsig.anthropic.com恢复精确AI保护：它不是statsig.com的子域，不能靠后者覆盖。广告源中与当前和历史业务保护相交的阻断项会物理移除，兼容旧保护表与新广告表的混合下载。

## 4. Apple明确分流

新增apple.com与apple.cn后缀直连，覆盖裸域、www、swcdn、TestFlight、developer等，不再等待GEOIP解析结果决定。原server:system负责DNS选择，它本身不是DIRECT策略；17/8,no-resolve也不能替代域名直连。更精确的已知AI端点仍可以放到更靠前的专用例外。

## 5. Google登录与使用一致

新增Google账户select，默认选择AI住宅组这个实际策略对象，Google登录、oauth2、Gmail、Drive和搜索统一使用它；AI Studio补精确AI保护。默认情况下即使AI住宅发生故障切换，认证与普通Google业务也跟随同一组决策。用户若手动给Google账户另选节点，就主动改变了这种一致性。YouTube媒体仍独立走流媒体。单靠域名规则无法把同一个accounts.google.com按来源App分配给多个不同出口。

## 6. 数字关键词与测速

233条均来自WeChat源，都是三段数字加末尾点。关键词是主机字符串子串匹配，不是网段判断；它不会自动检查DNS解析后的IP。已按原前缀有意修正为精确/24,no-resolve，逐条保留原行和纠正说明；这不是严格语义等价转换，226条扩大了旧CIDR表的覆盖范围。新增反例检查14.22.0.0/24不会匹配114.22.0.x。speedtest宽关键词删除，只保留明确Ookla业务域；测速看到哪个出口取决于实际测试流量的规则，不拿站名强制全部直连。

## 7. 遥测独立处理

按用户要求补Amplitude公开上报API精确主机、Google Tag Manager域的拒绝。未把所有SDK都当广告：Statsig在已知AI功能链路中的例外继续保留。网站个别标签功能可能受遥测拒绝影响，真实业务异常用精确例外处理。

## 8. General与广告格式

IPv6保持false，Proxy保持空白。删除无功能使用的replica=false旧项（当前官方General页未收录，不能把[Replica]章节废弃当成该key的已证实废弃声明）；移除无效的Wi-Fi访问端口。CGNAT网段从skip-proxy/tun-excluded-routes中移除，保留在Surge可见的正常路由路径；这不会自动配置Tailscale可达性。

新版广告挂载ads.domainset，保留ads.list作为旧配置兼容导出，两者由构建器验证完全同义。官方把DOMAIN-SET用于大量纯域名；RULE-SET域名也会索引，未经手机实测不承诺具体节省多少内存。

## 后续验收顺序

1. 中英文仓库通过同一套编译/迁移/健康检查，确认23个新版外部资源与兼容导出可下载。
2. 导入新版配置，填入节点并确认金融与Google账户组当前选择；核验真实出口IP和国家标签一致。
3. 在Wi-Fi、蜂窝分别检查金融登录、国内滑块/B站、国际视频、Google登录与AI Studio。保留失败请求和首条命中日志；不反复登录或切国家试错。
4. 后续GitHub更新失败保留上一版；健康检查改为更新完成后触发并每日巡检，首次部署不再抢跑。

证据：Surge官方规则语义 https://manual.nssurge.com/rules/domain.html 、RULE-SET https://manual.nssurge.com/rules/ruleset.html 、General https://manual.nssurge.com/profile/general.html；每条源行和转换原因保存在dist/v4/provenance.ndjson.gz及report.json。
