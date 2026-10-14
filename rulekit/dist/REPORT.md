# rulekit 构建报告 2026-10-14 03:32 UTC

## ads → ads.domainset（REJECT）：153332 条
- https://ruleset.skk.moe/List/domainset/reject.conf: 140602
- mc:bytedance@ads: 44
- mc:tencent@ads: 71
- mc:tencent-tme@ads: 13
- mc:alibaba@ads: 87
- mc:amap@ads: 5
- mc:eleme@ads: 3
- mc:jd@ads: 8
- mc:kuaishou@ads: 8
- mc:iqiyi@ads: 10
- mc:sina@ads: 24
- mc:netease@ads: 13
- mc:xiaomi@ads: 21
- mc:huawei@ads: 1
- mc:umeng@ads: 22
- mc:google@ads: 54
- mc:facebook@ads: 3
- mc:tiktok@ads: 1
- mc:x@ads: 1
- mc:youtube@ads: 1
- mc:microsoft@ads: 7
- https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/Filters/AWAvenue-Ads-Rule-Surge-RULE-SET.list: 965
- https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ads-supplement.list: 230
- https://raw.githubusercontent.com/Thelongdarkorg/ad-rules-merged/main/merged.txt: 17700
## ai → apps-ai.list（🤖 AI住宅）：747 条，让给更高优先级 7 条
- bm:OpenAI: 35
- bm:Claude: 3
- bm:Gemini: 13
- bm:Copilot: 51
- mc:openai: 22
- mc:anthropic: 9
- mc:xai: 4
- mc:cursor: 4
- https://ruleset.skk.moe/List/non_ip/ai.conf: 54
- https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ai-critical.list: 24
- https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/patches/ai-extended.list: 28
- bm:Facebook: 570
- bm:Instagram: 4
- bm:Stripe: 1
- custom/ai-extra.list: 93
## tiktok → apps-tiktok.list（🎵 TikTok）：64 条，让给更高优先级 1 条
- bm:TikTok: 32
- mc:tiktok: 37
- custom/tiktok-extra.list: 43
## stream → apps-stream.list（🎬 流媒体）：1352 条，让给更高优先级 1 条
- bm:YouTube: 189
- bm:Netflix: 1157
- bm:Viki: 8
## google → apps-google.list（🤖 AI住宅）：686 条，让给更高优先级 39 条
- bm:Google: 698
- bm:GoogleSearch: 1
- bm:GoogleDrive: 8
- bm:GoogleFCM: 41
## uk → apps-uk.list（🇬🇧 英国专属）：2 条
- mc:giffgaff: 2
## global → apps-global.list（🌍 国际网络）：124 条，让给更高优先级 3 条
- bm:Twitter: 33
- bm:Whatsapp: 17
- bm:Telegram: 40
- bm:Discord: 29
- custom/global-extra.list: 11
## cn → apps-cn.list（DIRECT）：6269 条，让给更高优先级 52 条
- bm:AliPay: 20
- bm:UnionPay: 16
- bm:ICBC: 57
- bm:CCB: 18
- bm:CMB: 38
- mc:citic: 15
- bm:WeChat: 99
- bm:DingTalk: 11
- bm:Tencent: 25
- bm:DouYin: 13
- bm:KuaiShou: 678
- bm:XiaoHongShu: 4
- bm:BiliBili: 127
- bm:Weibo: 4
- bm:NetEaseMusic: 30
- bm:TencentVideo: 51
- bm:iQIYI: 62
- bm:ByteDance: 372
- bm:Coolapk: 3
- bm:Alibaba: 54
- bm:JingDong: 249
- bm:Pinduoduo: 3
- bm:XianYu: 16
- bm:MeiTuan: 7
- bm:Eleme: 13
- bm:ZhuanZhuan: 4
- mc:dewu: 45
- bm:GaoDe: 9
- bm:12306: 15
- bm:XieCheng: 29
- mc:dongchedi: 8
- bm:Geely: 50
- mc:deepseek: 2
- bm:ChinaMobile: 38
- bm:XiaoMi: 157
- bm:Huawei: 160
- bm:NetEase: 146
- mc:liepin: 3
- mc:qcc: 2
- mc:lianjia: 5
- mc:intsig: 5
- custom/cn-extra.list: 36
- bm:Alibaba_Domain: 1263
- bm:Tencent_Domain: 2498

白名单从拒绝表删除 130 条；ABP 例外 2614 条
前置放行：pre-cn.list 49 条，pre-tiktok.list 2 条，pre-ai.list 1 条
自动推断策略的放行主机：aisite.wejianzhan.com→cn，alps.51y5.net→cn，app.huabao.360.cn→cn，assets.giocdn.com→cn，audiopay.pcdn.xmcdn.com→cn，audiopaydl.pcdn.xmcdn.com→cn，channel.shouji.sogou.com→cn，d.bmcx.com→cn，dianfeijisuanqi.bmcx.com→cn，f.bmcx.com→cn，get.shouji.sogou.com→cn，input.shouji.sogou.com→cn，ip.rtbasia.com→cn，laohuangli.bmcx.com→cn，lf3-card-system.searchpstatp.com→cn，lf3-search.searchpstatp.com→cn，localads.chengzijianzhan.cn→cn，mac.bmcx.com→cn，map.bmcx.com→cn，mm1.365dmp.com→cn，mm3.365dmp.com→cn，mvconf.f.360.cn→cn，openap-alps.51y5.net→cn，s.mvconf.f.360.cn→cn，saomiao.bmcx.com→cn，scan.call.f.360.cn→cn，shenfenzheng.bmcx.com→cn，shouji.bmcx.com→cn，wannianrili.bmcx.com→cn，www.bmcx.com→cn

## 回归测试
全部通过

## 变化量保护
正常

## 日志
[ads] ads.domainset
[ai] apps-ai.list
[tiktok] apps-tiktok.list
[stream] apps-stream.list
[google] apps-google.list
[uk] apps-uk.list
[global] apps-global.list
[cn] apps-cn.list