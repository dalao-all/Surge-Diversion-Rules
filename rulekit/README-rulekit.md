---
title: Surge 分流规则深度审计与「按 App 自建规则集」方案
subtitle: 基于 Surge-1.3.6-final 与 APP 排序清单（159 个）· 2026-10-14
---

# 一、结论先说

**"偶尔抽风"的主因不是规则不够细，而是广告表误杀了正常业务域名，而且这种误杀是结构性的、每天都可能变。**

1. **ads-patch.domainset（17,295 条，现在的主力广告表）把很多正常服务整域拦掉了。** 按 1.3.6-final 实际顺序模拟，下列请求现在全部是 REJECT：

| 被拦主机 | 是什么 | 影响你哪个 App |
|---|---|---|
| graph.facebook.com / connect.facebook.net | Facebook 核心 API / SDK | Facebook、Instagram 登录与信息流；大量 App 的"用 Facebook 登录" |
| firebaseremoteconfig / firebaseinstallations.googleapis.com | Firebase 远程配置与实例注册 | 大量国外 App 启动时拉配置，拒绝后反复重试 → 启动慢、偶发卡死 |
| update.googleapis.com | Chrome / Google App 组件更新 | Chrome、Google |
| statsigapi.net | ChatGPT 功能开关（你决定保留的） | ChatGPT 部分功能缺失 |
| haohuo.jinritemai.com | 抖音商城商品页 | 抖音 |
| *.volces.com | 火山引擎（豆包 / 抖音云服务） | 豆包、抖音、剪映 |
| s1 / w1.kskwai.com | 快手静态资源 | 快手 |
| api.jpush.cn / tsis.jpush.cn | 极光推送 | 很多国内 App 收不到推送 |
| ocsp.godaddy.com | 证书吊销检查 | 部分 HTTPS 网站首次打开变慢 |
| static.wixstatic.com / cdn.jwplayer.com | Wix 建站图片 / 网页视频播放器 | 部分网页图片、视频加载不出 |
| ttwebview.com | TikTok 内置浏览器 | TikTok |
| ipinfo.io | 出口 IP 查询（你放在 AI 组的探针） | 自查探针失效 |

2. **根因是转换方式本身有问题，不是哪几条写错了。** 浮风上游是 ABP 格式，靠 **3,118 条 `@@` 例外** 抵消根域拦截（比如 `||biliapi.net^` 配 `@@||grpc.biliapi.net^`）。转换成 Surge 域名集时例外被整条丢弃，其中 **87 条被父域拦截"吞掉"**（grpc.biliapi.net、haohuo.jinritemai.com、p3.bdxiguaimg.com、tsis.jpush.cn、s1/w1/w2.kskwai.com、gator.volces.com、ingest.sentry.io…）。你在 1.1 节和 direct-patch 里手工补的白名单，其实就是在一条一条打这个洞，**上游每天变，洞也每天变**——这就是"偶尔"的来源。

3. **我拿同一组 94 个"必须能用"的业务主机测了 6 个常见广告源**（误杀数越少越好）：

| 广告源 | 条目 | 误杀 | 备注 |
|---|---|---|---|
| ads-patch（现用） | 17,295 | **28** | 见上表 |
| anti-AD | 102,535 | 8 | 会拦 statsig、branch.io、graph.instagram.com |
| SKK reject | 140,608 | 6 | 其中 4 条在业界本来就有争议（kskwai、wxs.qq.com、jpush） |
| AWAvenue（秋风） | 961 | 4 | 专拦国内 App SDK 广告 |
| 217heidai | 233,039 | 4 | 体量过大 |
| v2fly 各公司 @ads | 44～902 | 0～2 | 社区人工标注，最精准，但覆盖面小 |

**→ 广告底座换成 SKK reject，加上 v2fly「你用到的公司 @ads」子集和秋风，再用你自己的白名单兜底**，是误杀最少、覆盖面最大的组合。

4. **你的想法（按 App 抓上游 → 合并成自有规则集 → 每天自动更新 → 先广告后 App）方向是对的**，但有三处要调整，否则会更不稳：
   - **按"策略"合并输出，不要一 App 一文件。** Surge 一个 RULE-SET 只能挂一个策略；159 个国内 App 最终都是 DIRECT，拆成 159 个文件只会多 159 个下载失败点。合并成 8 个文件，文件里保留来源注释。
   - **上游会带进旧坑。** 实测：blackmatrix7 的 TikTok.list 里有 `snssdk.com`（抖音/头条国内 API，你 V1.3.2 修过的同一个坑），Facebook.list 把整个 WhatsApp 算进 Meta（你让 WhatsApp 走国际网络）。所以合并脚本必须有排除表和优先级。
   - **每天跑的应该是 GitHub Action 脚本，不是 AI。** 抓取、合并、去重、测试都是确定性的工作，用脚本才可复现；AI 适合做"每周看一眼变化报告"。10-12 的事故就是自动同步没有任何保险导致的，新方案必须有保险（见第四节）。

---

# 二、现有规则逐节审计（1.3.6-final，展开后共 37,976 条）

> 方法：78 个远程规则集全部重新拉取（今天 09:25 版本，全部 HTTP 200），按 Surge 实际匹配顺序展开（pre-matching 提前），逐条做遮蔽/冲突检测。共发现 **229 组遮蔽，涉及 3,214 条规则；其中 132 组是策略冲突**（后面的规则永远不会生效，而且策略和你想要的不一样）。

## 2.1 内联规则（514 条）

| 节 | 内容 | 判定 |
|---|---|---|
| 0a | 853 端口 + 6 个 DoH 域名 REJECT | ✅ 保留 |
| 0b | 王者/微信语音打洞直连、Apple 17.0.0.0/8、STUN 规则 | ⚠️ `PROTOCOL,STUN,REJECT` 会拒绝 WhatsApp / Telegram / Discord 打国外 IP 的 STUN，通话只能走中继，**国外语音偶尔接不通/延迟大很可能和它有关**。防 WebRTC 泄露是你的选择；如果在乎通话质量，可以给这三个 App 的 STUN 放行（需要抓包确认 IP 段） |
| Apple 段 | 6 个 AND+GEOIP 条件、apps.apple.com 直连、Apple_cn/apple_cdn | ✅ 保留（10-13 已修好），不并入自动构建 |
| 死域名快速失败 | 6 条 | ✅ 保留 |
| 1 pre-matching | Private Relay、STUN 服务器、New Relic/Akamai mPulse 等遥测 | ✅ 保留 |
| 1.1 兼容例外 | 32 条手工白名单 | ♻️ 迁入 allow.list，自动生效、自动判断是否还需要 |
| 1.2 精确开屏 DROP | 穿山甲日志、爱奇艺 msg、小红书 tracker、tanx 等 | ✅ 保留（精准、有抓包依据） |
| 1.3 / 1.4 | ads-patch + ads-supplement + 6 个 SKK 镜像 | ❌ 换掉，见第三节。注意：你仓库 mirrors/owned 下的 SKK reject 只有 **536 条**，而 SKK 官方 reject 有 **140,608 条**——你以为在用 SKK 底座，其实几乎没用上 |
| 2 金融 | Bybit / OKX / Binance / PayPal / giffgaff | ✅ 保留内联（高敏，手工维护更可控） |
| 3 AI | Claude / OpenAI / Grok / 编程工具 / 人机验证 / 遥测拒绝 | ♻️ 迁入 apps-ai（custom/ai-extra.list 已迁好 89 条） |
| 3h-3i Google | YouTube→流媒体；accounts/gmail/drive/**整个 googleapis.com 和 gstatic.com**→AI 住宅 | ⚠️ 所有 App 的 Firebase、Google Fonts、地图 SDK 都会走住宅出口（贵、慢）。建议只把账号/Gmail/Drive 留在住宅，其余走国际网络。新方案单独做了 apps-google，策略你一行就能改 |
| 3j TikTok | 43 条 | ♻️ 迁入 apps-tiktok |
| 3k Meta | Facebook / Instagram → AI 住宅 | ♻️ 迁入 apps-ai（WhatsApp 已排除） |
| 4 国内 | 公司内网、微软更新、阿里海外节点、国内 AI、视频 | 公司内网/微软/阿里 IP 段保留内联；其余迁入 apps-cn |
| 5/6 | Netflix/Viki、Discord/Telegram/WhatsApp/X/GitHub | ♻️ 迁入 apps-stream / apps-global |
| 7 | IP 兜底、GEOIP CN、FINAL dns-failed | ✅ 保留 |

## 2.2 远程规则集（78 个）

| 规则集 | 条目 | 策略 | 判定 |
|---|---|---|---|
| ads-patch.domainset | 17,295 | REJECT | ❌ 误杀源头，替换 |
| ads-supplement.list | 230 | REJECT | ✅ 并入新 ads（其中 iadmat.nosdn.127.net、pgdt.gtimg.cn 会挡网易云/腾讯视频的部分素材，可接受） |
| owned reject / extra / phishing / non_ip | 536 / 43 / 356 / 85 | REJECT | ❌ 只是 SKK 的极小子集，换官方完整版 |
| ai-critical / ai-extended | 24 / 28 | AI | ✅ 作为 apps-ai 的源 |
| direct-patch.list | 19 | DIRECT | ♻️ 并入 allow.list |
| finance-*.list | 6 / 1 / 1 | 金融组 | ✅ 保留 |
| blackmatrix7 国内 26 个（AliPay…ChinaMobile） | 4～2,498 | DIRECT | ✅ 作为 apps-cn 的源。注意：WeChat.list 里 **233 条是把 IP 前缀写成 DOMAIN-KEYWORD**（如 `101.91.5.`），关键词规则逐条线性匹配、还会误中 `101.91.50.x`，构建时自动丢弃 |
| Alibaba_Domain（你的镜像） | 1,248 | DIRECT | ✅ 改用 blackmatrix7 官方（1,263 条，今天刚更新） |
| SKK domestic / direct / microsoft_cdn / apple_cdn | 872 / 220 / 54 / 160 | DIRECT | ✅ 保留作 L4 兜底；direct.conf 的 36 条 PROCESS-NAME 是 macOS 专用，iOS 无效 |
| SKK cdn / download / global / microsoft / telegram | 4,765 / 1,982 / 1,272 / 84 / 15 | 国际网络 | ✅ 保留作兜底 |
| SKK stream + 6 个地区 | 336 + 173 | 流媒体各池 | ⚠️ 遮蔽 69 条：stream.conf 排在 stream_jp/tw/eu 后面没问题，但 **stream.conf 把 tiktok.com、bilibili.tv 等也算流媒体**，靠你前置规则才没出错 |
| SKK ai.conf（域名 + IP） | 52 + 24 | AI | ✅ 并入 apps-ai（api.github.com 已排除） |
| sogouinput / gitlab | 15 / 2 | REJECT / 国际 | ✅ 保留 |
| china_ip / domestic IP / neteasemusic IP / reject IP | 3,901 / 3 / 18 / 779 | — | ✅ 保留 |

## 2.3 典型的"写了但不生效"（策略冲突，摘录）

- **ByteDance.list 想直连、被广告表先拦**：volces.com、jinritemai.com、bdxiguaimg.com、dailygn.com、oceanengine.com 等 15 个
- **Alibaba_Domain 想直连、被广告表先拦**：umeng.com、cnzz.com、mmstat.com、alimama.com 等 22 个（这些本身就是统计/广告，拦掉是对的，属于"良性冲突"）
- **SKK cdn/global 想走国际网络、被广告表先拦**：graph.facebook.com、firebase 三件套、sentry.io、mailchimp.com、sendgrid.net、opencollective.com、wixstatic.com 等 70 个
- **domestic.conf 想直连、被广告表先拦**：cnnic.cn、oschina.net（开源中国）、youzanyun.com（有赞小店）、oppopay.com、jpush.cn、in-addr.arpa（反向 DNS）等 17 个

---

# 三、新方案：rulekit

## 3.1 规则顺序（先广告、后 App、再兜底）

```
L0  内联：DNS 防泄漏 / 语音打洞 / Apple / pre-matching 隐私 / 精确开屏 DROP   ← 原样保留
L1  前置放行 pre-*.list（allow.list 自动生成，平时 0～10 条）+ 金融补丁
L2  广告  ads.domainset（SKK + v2fly@ads + 秋风 + 你的补充，减去白名单）
L3  App   apps-ai / tiktok / stream / google / uk / global / cn
L4  通用  .cn、SKK domestic / direct / cdn / global
L5  IP    china_ip / GEOIP CN / FINAL
```

## 3.2 你的 159 个 App 怎么覆盖

| 组 | App | 上游来源（每日更新） |
|---|---|---|
| 银行与支付 | 支付宝、云闪付、工行、建行、招行/掌上生活、京东金融、动卡空间 | blackmatrix7 AliPay/UnionPay/ICBC/CCB/CMB/JingDong，v2fly citic |
| | 四川农信、兴业银行 | 上游无；主要用 .cn 域名，已被 `DOMAIN-SUFFIX,cn` 覆盖，另补 scrcu.com / cib.com |
| 通讯 | 微信、钉钉、QQ | blackmatrix7 WeChat/DingTalk/Tencent(+Tencent_Domain 2,498 条) |
| 娱乐 | 抖音、快手(极速版)、小红书、B 站、微博、网易云、腾讯视频、爱奇艺、剪映、酷安 | blackmatrix7 同名 + ByteDance |
| | 王者荣耀、掌上英雄联盟 | Tencent（语音打洞已在 L0） |
| | 猫眼、飞智、淘票票 | 手工补 maoyan.com / flydigi.com；淘票票走 Alibaba |
| 购物 | 淘宝、闪购、闲鱼、1688、一淘、盒马 | blackmatrix7 Alibaba + Alibaba_Domain、XianYu、Eleme |
| | 京东、京东 AI 购、京粉 | JingDong |
| | 拼多多、美团、大众点评、转转、得物 | Pinduoduo、MeiTuan、ZhuanZhuan、v2fly dewu |
| | 山姆、省钱快报 | 山姆用 .cn；手工补 sqkb.com |
| 地图 | 高德 | GaoDe |
| 国内 AI | DeepSeek、豆包、千问、ima、TRAE | v2fly deepseek；ByteDance + 手工 doubao.com/volces.com；Alibaba；手工 ima.qq.com、trae.com.cn |
| 出行/汽车 | 12306、携程、懂车帝、吉利 | blackmatrix7 12306/XieCheng/Geely，v2fly dongchedi |
| | 航旅纵横、哈啰、九号、汽车之家、天府通、无忧行 | 手工 umetrip.com / hellobike.com / ninebot.com；后三者用 .cn |
| 工作/办事 | 有道、BOSS、智联、猎聘、企查查、贝壳、扫描全能王、中国移动、UU 远程 | 手工 youdao/zhipin/zhaopin；v2fly liepin/qcc/lianjia/intsig；ChinaMobile；NetEase |
| | 个税、交管 12123、国家网络身份认证、天府通 | 全是 .gov.cn / .cn |
| 智能家居 | 米家、华为智慧生活 | XiaoMi、Huawei |
| Apple 系统 App（约 40 个） | 电话、照片、App Store、iCloud、地图、音乐、播客、TV… | **不进自动构建**，沿用你 L0 那套已经调好的 Apple 规则 |
| 记账小工具 | MONO、Cookie、上岛记、iCost、GestaltEdit… | 基本只用 iCloud 同步，无需单独规则 |
| 国外 AI | ChatGPT、Claude、Gemini、Cursor、Grok | blackmatrix7 OpenAI/Claude/Gemini/Copilot，v2fly openai/anthropic/xai/cursor，SKK ai，你的 ai-critical/extended |
| 国外娱乐 | X、YouTube、TikTok、Instagram、Facebook、Netflix、Viki | Twitter、YouTube、TikTok(排除 snssdk.com)、Instagram、Facebook(排除 WhatsApp)、Netflix、Viki |
| 国外通讯 | WhatsApp、Telegram、Discord | blackmatrix7 同名 |
| 谷歌 | Google、Chrome、Gmail、Drive、Maps | Google、GoogleSearch、GoogleDrive、GoogleFCM |
| 其他 | Obsidian、DejaVocab、Tableau、Sanas、giffgaff、Surge | 手工补；giffgaff 用 v2fly → 英国专属；Tableau 按你的选择直连 |

## 3.3 今天在沙盒里的实际构建结果

| 输出 | 策略 | 条目 |
|---|---|---|
| ads.domainset | REJECT | 141,046 |
| apps-ai.list | 🤖 AI住宅 | 747 |
| apps-tiktok.list | 🎵 TikTok | 64 |
| apps-stream.list | 🎬 流媒体 | 1,352 |
| apps-google.list | 🤖 AI住宅 | 689 |
| apps-uk.list | 🇬🇧 英国专属 | 2 |
| apps-global.list | 🌍 国际网络 | 124 |
| apps-cn.list | DIRECT | 6,287 |
| pre-cn.list | DIRECT | 5（kskwai ×3、jpush ×2） |

60 个探针**全部通过**；第一次构建时探针当场抓出了 2 个上游问题（TikTok.list 带 snssdk.com、Facebook.list 带 WhatsApp），加了排除规则才放行——保险就是这么起作用的。

# 四、每日自动更新与三道保险

**流程**：GitHub Action 每天北京时间 05:30 → 抓所有上游 → 解析/去重/排优先级 → 套白名单 → 跑探针 → 通过才提交到 `rulekit/dist/` → Surge 每 24 小时拉一次。

| 保险 | 防什么 | 怎么做 |
|---|---|---|
| ① 上游异常用缓存 | 上游 404、被清空、缩水一半 | 每个源保留上一版；抓取失败或体积缩水超 50% 就用缓存 |
| ② 变化量闸门 | 10-12 那种一夜多出 3,550 条 | 任何输出变化超过 10%（且超 300 条）就不发布，发邮件；确认正常后手动 Run workflow 勾选 force |
| ③ 探针回归测试 | 误杀业务、广告漏拦 | probes.toml 里写"这个域名必须走哪"；有一条不对就不发布 |
| 格式保险 | 截成顶级域、hosts 格式误转 | 单标签、公共后缀（com/cn/co.uk/in-addr.arpa…）一律丢弃；hosts 格式不收 |

**AI 的位置**：不用 AI 每天抓。可以让我每周一读一次 REPORT.md 的变化，告诉你上游新增了什么、要不要加进白名单或探针。

# 五、迁移步骤

1. 把附件 rulekit 文件夹整个放到仓库根目录，把 `rulekit/.github/workflows/rulekit.yml` 移到仓库的 `.github/workflows/`。
2. 在 GitHub 仓库 Actions 里手动 Run 一次，确认 `rulekit/dist/` 生成、REPORT.md 显示探针全部通过。
3. 复制 1.3.6-final 为 1.4.0，按 surge-rules-v2.conf 替换 1.1/1.3/1.4/3/4/5/6 节，L0、金融、IP 兜底原样保留。
4. 先在 Surge 里用 1.4.0 跑两三天，遇到打不开的，把主机名加进 allow.list（带策略）**和** probes.toml，推送后 Action 自动重建。
5. 稳定后删除仓库里旧的 patches/ads-patch.*、mirrors/owned、ads_sync.py 和对应 Action。

# 六、需要你拍板的

1. **Google 流量**：要不要把 apps-google 从 AI 住宅改成国际网络（只留账号/Gmail/Drive 在住宅）？
2. **国外语音通话**：要不要给 WhatsApp / Telegram / Discord 的 STUN 放行？
3. **广告强度**：现在是 SKK reject 底座。想更狠可以加 SKK reject_extra（77,426 条，探针测试 0 误杀），代价是规则文件再大 1.5 MB、Surge 占用内存略增。

# 附录 A：被 ads-patch 父域吞掉的 87 条上游例外

miaozhen.com, ad.doubleclick.net, ads.privacy.qq.com, aisite.wejianzhan.com, alps.51y5.net, android.bugly.qq.com, api.airpush.com, api.developer.xiaomi.com, api.flash.cn, api.tuisong.baidu.com, app.huabao.360.cn, article.zlink.toutiao.com, assets.giocdn.com, at.umeng.com, audiopay.pcdn.xmcdn.com, audiopaydl.pcdn.xmcdn.com, broadcastlv.chat.bilibili.com, cainiao-app-logs.cn-zhangjiakou.log.aliyuncs.com, channel.shouji.sogou.com, cl2.webterren.com, cn.ultraiso.net, d.bmcx.com, data.flurry.com, dc.sigmob.cn, f.bmcx.com, gator.volces.com, get.shouji.sogou.com, grpc.biliapi.net, h.trace.qq.com, haohuo.jinritemai.com, ii.gdt.qq.com, imgx.mediav.com, ingest.sentry.io, input.shouji.sogou.com, ios.bugly.qq.com, ip.rtbasia.com, lf-ad-convert-feedback.oceanengine.com, lf3-card-system.searchpstatp.com, lf3-search.searchpstatp.com, lf6-mgsdk-sign.dailygn.com, lf9-mgsdk-sign.dailygn.com, localads.chengzijianzhan.cn, log-api.pangolin-sdk-toutiao(-b).com, m2.da.mgtv.com, mm1/mm3.365dmp.com, novelfm.zlink.toutiao.com, openap-alps.51y5.net, otheve.beacon.qq.com, p1/p2/p4-lm/ad.adukwai.com, p2-game.kskwai.com, p26-sign/p3-sign/p3.bdxiguaimg.com, pro.bugly.qq.com, s1/w1/w2.kskwai.com, sdk-api.beizi.biz, sdk.open.talk.gepush.com, sdkapi.sms.mob.com, sf6-fe-tos.pglstatp-toutiao.com, t7z.cupid.iqiyi.com, tangram.e.qq.com, tongji.flash.cn, tsis.jpush.cn, tube.e.kuaishou.com, v.gdt.qq.com, v2/v4-tube.adukwai.com, video.da.mgtv.com, wm.makeding.com，以及 bmcx.com 下 11 个工具页。

# 附录 B：附件清单

| 文件 | 作用 |
|---|---|
| build.py | 构建脚本（抓取、解析、去重、优先级、白名单、探针、闸门） |
| sources.toml | App → 上游映射，改这里就能增删 App |
| allow.list | 白名单（永不被拦的业务主机） |
| probes.toml | 回归测试 |
| custom/*.list | 上游没有的 App 手工域名（含从 1.3.6 迁出的 AI/TikTok 内联规则） |
| .github/workflows/rulekit.yml | 每日 05:30 自动构建 |
| surge-rules-v2.conf | Surge [Rule] 新骨架 |
| dist/ | 今天的构建产物样例 + REPORT.md |
