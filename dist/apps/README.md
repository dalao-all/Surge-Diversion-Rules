# 按 App 规则集（dist/apps）

构建日期：2026-10-19。每个 App 一个文件，内容为多个上游同名规则的并集（去重、剔除国内共用域名、跨 App 冲突按优先级归属）。

引用格式：`RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/dist/apps/<App>.list,<策略>`

表格顺序即推荐的规则顺序（共享域名只归属排在前面的 App）。详细来源统计见 report.json，上游提交见 sources.lock.json。

另有两个自动生成的辅助表（不在下表）：`CN-Guard.list`（被海外关键词误吸的国内域名，放海外 App 层之前 DIRECT）、`CN-Reject.list`（被新扩国内后缀罩住的广告域名，放国内单表之前 REJECT）。

| # | App | 文件 | 条目 | 最大单一上游 | 建议策略 | 覆盖的 v4 App | 上游 |
|---|---|---|---|---|---|---|---|
| 1 | OKX | [OKX.list](OKX.list) | 21 | 9 | 🪙 OKX 台湾 |  | v2:okx, bm:OKX, custom |
| 2 | Binance | [Binance.list](Binance.list) | 48 | 45 | 🪙 Binance 台湾 |  | v2:binance, bm:Binance, acl:Binance.list, custom |
| 3 | Bybit | [Bybit.list](Bybit.list) | 35 | 16 | 💳 Bybit 全球 |  | v2:bybit, repo-patch:finance-bybit-global, custom |
| 4 | Bybit EU | [BybitEU.list](BybitEU.list) | 7 | 1 | 🇩🇪 Bybit 欧洲 |  | repo-patch:finance-bybit-eu, custom |
| 5 | Bitget Wallet | [BitgetWallet.list](BitgetWallet.list) | 8 | 0 | 🪙 数字资产 |  | custom |
| 6 | UU Wallet | [UUWallet.list](UUWallet.list) | 1 | 0 | 🪙 数字资产 |  | custom |
| 7 | Plasma One | [PlasmaOne.list](PlasmaOne.list) | 3 | 0 | 🪙 数字资产 |  | custom |
| 8 | 其他交易所/钱包/链上工具 + WalletConnect/Reown | [Crypto-Common.list](Crypto-Common.list) | 197 | 197 | 🪙 数字资产 |  | bm:Crypto, bm:Cryptocurrency, custom |
| 9 | PayPal | [PayPal.list](PayPal.list) | 241 | 247 | 💳 PayPal 美国 |  | v2:paypal, bm:PayPal, custom |
| 10 | Wise | [Wise.list](Wise.list) | 2 | 2 | 💸 Wise 台湾 |  | v2:wise, custom |
| 11 | AI 通用依赖（验证码/风控/特性开关/登录） | [AI-Common.list](AI-Common.list) | 28 | 7 | 🤖 AI住宅 |  | repo-custom:reviewed-ai-auth, repo-custom:ai-login-endpoints, repo-custom:ai-challenge, repo-custom:ai-featureflags, custom |
| 12 | Claude | [Claude.list](Claude.list) | 39 | 34 | 🤖 AI住宅 |  | v2:anthropic, bm:Claude, acl:Claude.list, acl:ClaudeAI.list, vpsd:anthropic, xiaolai:anthropic, sukka-ai:Anthropic / Claude, bm:Anthropic, custom |
| 13 | ChatGPT / OpenAI | [ChatGPT.list](ChatGPT.list) | 31 | 31 | 🤖 AI住宅 |  | v2:openai, bm:OpenAI, acl:OpenAi.list, vpsd:openai, sukka-ai:OpenAI / ChatGPT, custom |
| 14 | Gemini / Google AI | [Gemini.list](Gemini.list) | 50 | 47 | 🤖 AI住宅 |  | v2:google-gemini, v2:google-deepmind, bm:Gemini, acl:Gemini.list, vpsd:google-ai, sukka-ai:Google, bm:BardAI, custom |
| 15 | Grok / xAI | [Grok.list](Grok.list) | 6 | 4 | 🤖 AI住宅 |  | v2:xai, vpsd:x-ai, sukka-ai:Grok, custom |
| 16 | Cursor | [Cursor.list](Cursor.list) | 8 | 5 | 🤖 AI住宅 |  | v2:cursor, vpsd:cursor, sukka-ai:Cursor, custom |
| 17 | 其他 AI（Perplexity/Copilot/HuggingFace/Mistral/OpenRouter/Windsurf/Poe/Groq/…） | [AI-Other.list](AI-Other.list) | 76 | 40 | 🤖 AI住宅 |  | vpsd:perplexity, vpsd:copilot, vpsd:huggingface, vpsd:mistral-ai, vpsd:openrouter, vpsd:windsurf, vpsd:poe, vpsd:groq, vpsd:cohere, vpsd:midjourney, vpsd:replit, vpsd:sourcegraph, vpsd:zed, vpsd:augment-code, vpsd:meta-ai, v2:perplexity, v2:github-copilot, v2:huggingface, v2:poe, v2:windsurf, v2:groq, sukka-ai:Perplexity, sukka-ai:POE, sukka-ai:GitHub Copilot, sukka-ai:groq, sukka-ai:OpenRouter AI - Unified Relay, sukka-ai:Windsurf (formerly Codeium), sukka-ai:Meta AI, bm:Copilot, sukka-ai:Cloudflare AI Gateway, sukka-ai:Dify.AI, sukka-ai:Jasper, sukka-ai:OpenArt, sukka-ai:JetBrains AI, custom |
| 18 | Notion | [Notion.list](Notion.list) | 9 | 7 | 🤖 AI住宅 |  | v2:notion, bm:Notion, custom |
| 19 | IP 检测站点 | [IPCheck.list](IPCheck.list) | 9 | 0 | 🤖 AI住宅 |  | custom |
| 20 | YouTube | [YouTube.list](YouTube.list) | 179 | 178 | 📺 YouTube |  | v2:youtube, bm:YouTube, bm:YouTubeMusic, acl:YouTube.list, acl:YouTubeMusic.list, sukka-stream:YouTube, sukka-stream:YouTube Music, custom |
| 21 | Google（搜索/Chrome/Gmail/地图/云端硬盘/Play/FCM/Authenticator） | [Google.list](Google.list) | 735 | 942 | 🤖 AI住宅 |  | v2:google, bm:Google, bm:GoogleDrive, bm:GoogleEarth, bm:GoogleFCM, acl:Google.list, acl:GoogleFCM.list, acl:GoogleEarth.list, sukka-global:GOOGLE, sukka-gl:Google, bm:GoogleSearch, bm:GoogleVoice, custom |
| 22 | TikTok（国际版） | [TikTok.list](TikTok.list) | 67 | 36 | 🎵 TikTok |  | v2:tiktok, bm:TikTok, acl:TikTok.list, sukka-stream:TikTok, custom |
| 23 | WhatsApp | [WhatsApp.list](WhatsApp.list) | 13 | 11 | 💬 WhatsApp |  | v2:whatsapp, bm:Whatsapp, acl:Whatsapp.list, custom |
| 24 | Instagram | [Instagram.list](Instagram.list) | 74 | 72 | 📘 Meta |  | v2:instagram, bm:Instagram, acl:Instagram.list, custom |
| 25 | Threads | [Threads.list](Threads.list) | 2 | 2 | 📘 Meta |  | v2:threads, bm:Threads, custom |
| 26 | Facebook / Messenger | [Facebook.list](Facebook.list) | 491 | 570 | 📘 Meta |  | v2:facebook, v2:messenger, v2:facebook-dev, bm:Facebook, acl:Facebook.list, sukka-gl:Facebook, custom |
| 27 | Reddit | [Reddit.list](Reddit.list) | 13 | 12 | 👽 Reddit |  | v2:reddit, bm:Reddit, acl:Reddit.list, sukka-gl:Reddit, custom |
| 28 | Netflix | [Netflix.list](Netflix.list) | 1154 | 1156 | 🎬 Netflix |  | v2:netflix, bm:Netflix, acl:Netflix.list, acl:NetflixIP.list, sukka-stream:Netflix, custom |
| 29 | Telegram | [Telegram.list](Telegram.list) | 47 | 40 | ✈️ Telegram |  | v2:telegram, bm:Telegram, acl:Telegram.list, bm:TelegramNL, bm:TelegramSG, bm:TelegramUS, custom |
| 30 | X / Twitter | [X.list](X.list) | 39 | 33 | 🐦 X |  | v2:twitter, bm:Twitter, acl:Twitter.list, sukka-gl:Twitter, custom |
| 31 | Discord | [Discord.list](Discord.list) | 29 | 29 | 🎮 Discord |  | v2:discord, bm:Discord, acl:Discord.list, sukka-gl:Discord, custom |
| 32 | Viki | [Viki.list](Viki.list) | 7 | 7 | 🎬 流媒体 |  | bm:Viki, custom |
| 33 | Bilibili 国际版 | [BilibiliIntl.list](BilibiliIntl.list) | 7 | 4 | 🎬 流媒体 |  | sukka-stream:Bilibili International, bm:BiliBiliIntl, custom |
| 34 | GitHub | [GitHub.list](GitHub.list) | 61 | 65 | 🌍 国际网络 |  | v2:github, bm:GitHub, acl:Github.list, sukka-gl:GitHub, custom |
| 35 | Obsidian | [Obsidian.list](Obsidian.list) | 1 | 1 | 🌍 国际网络 |  | repo-custom:app-INT022, custom |
| 36 | DejaVocab | [DejaVocab.list](DejaVocab.list) | 1 | 1 | 🌍 国际网络 |  | repo-custom:app-INT023, custom |
| 37 | Sanas | [Sanas.list](Sanas.list) | 1 | 2 | 🌍 国际网络 |  | repo-custom:app-INT025, custom |
| 38 | Tableau | [Tableau.list](Tableau.list) | 5 | 4 | 🌍 国际网络 |  | repo-custom:app-INT024, custom |
| 39 | Surge / Shadowrocket（代理工具自身） | [Surge.list](Surge.list) | 5 | 1 | 🌍 国际网络 |  | repo-custom:app-INT028, custom |
| 40 | Speedtest | [Speedtest.list](Speedtest.list) | 10 | 13 | 🌍 国际网络 |  | v2:ookla-speedtest, bm:Speedtest, sukka-gl:Speedtest, custom |
| 41 | giffgaff | [giffgaff.list](giffgaff.list) | 4 | 2 | 🇬🇧 英国专属 |  | v2:giffgaff, custom |
| 42 | 通用海外服务（非单一 App） | [Global-Misc.list](Global-Misc.list) | 16 | 0 | 🌍 国际网络 |  | custom |
| 43 | 支付宝 | [CN-AliPay.list](CN-AliPay.list) | 23 | 24 | DIRECT | CN001 支付宝 | bm:AliPay, v4own, custom |
| 44 | 云闪付 | [CN-UnionPay.list](CN-UnionPay.list) | 17 | 18 | DIRECT | CN002 云闪付 | bm:UnionPay, v2:unionpay, v4own, custom |
| 45 | 中国工商银行 | [CN-ICBC.list](CN-ICBC.list) | 59 | 60 | DIRECT | CN003 中国工商银行 | bm:ICBC, v2:icbc, v4own, custom |
| 46 | 中国建设银行 | [CN-CCB.list](CN-CCB.list) | 18 | 19 | DIRECT | CN004 中国建设银行 | bm:CCB, v2:ccb, v4own, custom |
| 47 | 个人手机银行（四川农信） | [CN-SCRCU.list](CN-SCRCU.list) | 4 | 5 | DIRECT | CN005 个人手机银行（四川农信） | v4own, custom |
| 48 | 掌上生活（招行信用卡） | [CN-CMBLife.list](CN-CMBLife.list) | 5 | 6 | DIRECT | CN009 掌上生活 | v4own, custom |
| 49 | 招商银行 | [CN-CMB.list](CN-CMB.list) | 37 | 38 | DIRECT | CN006 招商银行 | bm:CMB, v2:cmb, v4dep:cmb-shared, v4own, custom |
| 50 | 兴业银行 | [CN-CIB.list](CN-CIB.list) | 7 | 8 | DIRECT | CN007 兴业银行 | v4own, custom |
| 51 | 动卡空间（中信银行） | [CN-CITIC.list](CN-CITIC.list) | 18 | 17 | DIRECT | CN008 动卡空间 | v2:citic, v4dep:citic-shared, v4own, custom |
| 52 | 京东金融 | [CN-JDFinance.list](CN-JDFinance.list) | 5 | 6 | DIRECT | CN010 京东金融 | v4own, custom |
| 53 | 微信 | [CN-WeChat.list](CN-WeChat.list) | 315 | 336 | DIRECT | CN011 微信 | bm:WeChat, v4own, custom |
| 54 | QQ | [CN-QQ.list](CN-QQ.list) | 23 | 24 | DIRECT | CN013 QQ | v4own, custom |
| 55 | 钉钉 | [CN-DingTalk.list](CN-DingTalk.list) | 14 | 15 | DIRECT | CN012 钉钉 | bm:DingTalk, v2:dingtalk, v4own, custom |
| 56 | 抖音 | [CN-DouYin.list](CN-DouYin.list) | 82 | 71 | DIRECT | CN014 抖音 | bm:DouYin, v2:douyin, v4own, custom |
| 57 | 剪映 | [CN-JianYing.list](CN-JianYing.list) | 7 | 7 | DIRECT | CN024 剪映 | v4own, custom |
| 58 | 快手 / 快手极速版 | [CN-KuaiShou.list](CN-KuaiShou.list) | 689 | 681 | DIRECT | CN015 快手、CN019 快手极速版 | bm:KuaiShou, v2:kuaishou, v4own, custom |
| 59 | 小红书 | [CN-XiaoHongShu.list](CN-XiaoHongShu.list) | 13 | 9 | DIRECT | CN016 小红书 | bm:XiaoHongShu, v2:xiaohongshu, v4own, custom |
| 60 | 哔哩哔哩 | [CN-BiliBili.list](CN-BiliBili.list) | 122 | 123 | DIRECT | CN017 哔哩哔哩 | bm:BiliBili, v2:bilibili, v4own, custom |
| 61 | 微博 | [CN-Weibo.list](CN-Weibo.list) | 15 | 10 | DIRECT | CN018 微博 | bm:Weibo, v4own, custom |
| 62 | 黑猫投诉 | [CN-HeiMao.list](CN-HeiMao.list) | 5 | 5 | DIRECT | CN110 黑猫投诉 | v4own, custom |
| 63 | 网易云音乐 | [CN-NetEaseMusic.list](CN-NetEaseMusic.list) | 31 | 32 | DIRECT | CN020 网易云音乐 | bm:NetEaseMusic, v4own, custom |
| 64 | 网易有道词典 | [CN-Youdao.list](CN-Youdao.list) | 4 | 5 | DIRECT | CN091 网易有道词典 | v4own, custom |
| 65 | 腾讯视频 | [CN-TencentVideo.list](CN-TencentVideo.list) | 51 | 55 | DIRECT | CN021 腾讯视频 | bm:TencentVideo, v4own, custom |
| 66 | 爱奇艺 | [CN-iQIYI.list](CN-iQIYI.list) | 57 | 65 | DIRECT | CN022 爱奇艺 | bm:iQIYI, v2:iqiyi, v4own, custom |
| 67 | 王者荣耀 | [CN-HonorOfKings.list](CN-HonorOfKings.list) | 7 | 7 | DIRECT | CN025 王者荣耀 | v4own, custom |
| 68 | 掌上英雄联盟 | [CN-LOLMobile.list](CN-LOLMobile.list) | 7 | 8 | DIRECT | CN026 掌上英雄联盟 | v4own, custom |
| 69 | 飞智游戏厅 | [CN-FlyDigi.list](CN-FlyDigi.list) | 4 | 4 | DIRECT | CN027 飞智游戏厅 | v4own, custom |
| 70 | 酷安 | [CN-Coolapk.list](CN-Coolapk.list) | 4 | 5 | DIRECT | CN028 酷安 | bm:Coolapk, v2:coolapk, v4own, custom |
| 71 | 猫眼 | [CN-Maoyan.list](CN-Maoyan.list) | 5 | 5 | DIRECT | CN029 猫眼 | v4own, custom |
| 72 | 淘票票 | [CN-Taopiaopiao.list](CN-Taopiaopiao.list) | 10 | 10 | DIRECT | CN030 淘票票 | v4own, custom |
| 73 | 淘宝 | [CN-Taobao.list](CN-Taobao.list) | 25 | 25 | DIRECT | CN033 淘宝 | v4own, custom |
| 74 | 京东AI购 | [CN-JDAI.list](CN-JDAI.list) | 7 | 7 | DIRECT | CN045 京东AI购 | v4own, custom |
| 75 | 京粉 | [CN-JingFen.list](CN-JingFen.list) | 4 | 5 | DIRECT | CN047 京粉 | v4own, custom |
| 76 | 京东 | [CN-JingDong.list](CN-JingDong.list) | 261 | 249 | DIRECT | CN034 京东 | bm:JingDong, v2:jd, v4dep:jd-shared, v4own, custom |
| 77 | 拼多多 | [CN-Pinduoduo.list](CN-Pinduoduo.list) | 8 | 7 | DIRECT | CN035 拼多多 | bm:Pinduoduo, v2:pinduoduo, v4own, custom |
| 78 | 闲鱼 | [CN-XianYu.list](CN-XianYu.list) | 20 | 23 | DIRECT | CN036 闲鱼 | bm:XianYu, v4own, custom |
| 79 | 淘宝闪购（饿了么） | [CN-Eleme.list](CN-Eleme.list) | 22 | 20 | DIRECT | CN038 淘宝闪购 | bm:Eleme, v2:eleme, v4own, custom |
| 80 | 美团 | [CN-MeiTuan.list](CN-MeiTuan.list) | 19 | 19 | DIRECT | CN037 美团 | bm:MeiTuan, v2:meituan, v4dep:meituan-shared, v4own, custom |
| 81 | 大众点评 | [CN-DianPing.list](CN-DianPing.list) | 3 | 6 | DIRECT | CN039 大众点评 | v4own, custom |
| 82 | 盒马 | [CN-HeMa.list](CN-HeMa.list) | 14 | 14 | DIRECT | CN040 盒马 | bm:HeMa, v4own, custom |
| 83 | 山姆会员商店 | [CN-SamsClub.list](CN-SamsClub.list) | 16 | 10 | DIRECT | CN041 山姆会员商店 | v4dep:walmart-shared, v4own, custom |
| 84 | 得物 | [CN-DeWu.list](CN-DeWu.list) | 49 | 49 | DIRECT | CN042 得物 | v2:dewu, v4own, custom |
| 85 | 转转 | [CN-ZhuanZhuan.list](CN-ZhuanZhuan.list) | 6 | 6 | DIRECT | CN043 转转 | bm:ZhuanZhuan, v4own, custom |
| 86 | 阿里巴巴（1688） | [CN-1688.list](CN-1688.list) | 6 | 10 | DIRECT | CN044 阿里巴巴（1688） | v4own, custom |
| 87 | 一淘 | [CN-YiTao.list](CN-YiTao.list) | 3 | 3 | DIRECT | CN046 一淘 | v4own, custom |
| 88 | 省钱快报 | [CN-ShengQian.list](CN-ShengQian.list) | 5 | 5 | DIRECT | CN048 省钱快报 | v4own, custom |
| 89 | 高德地图 | [CN-GaoDe.list](CN-GaoDe.list) | 9 | 11 | DIRECT | CN049 高德地图 | bm:GaoDe, v4own, custom |
| 90 | DeepSeek | [CN-DeepSeek.list](CN-DeepSeek.list) | 2 | 6 | DIRECT | CN051 DeepSeek | v2:deepseek, v4own, custom |
| 91 | 豆包 | [CN-Doubao.list](CN-Doubao.list) | 35 | 37 | DIRECT | CN052 豆包 | v2:doubao, v4own, custom |
| 92 | 千问 | [CN-Qwen.list](CN-Qwen.list) | 9 | 9 | DIRECT | CN053 千问 | v4own, custom |
| 93 | ima | [CN-ima.list](CN-ima.list) | 3 | 4 | DIRECT | CN054 ima | v4own, custom |
| 94 | TRAE | [CN-TRAE.list](CN-TRAE.list) | 16 | 19 | DIRECT | CN055 TRAE | v2:trae, v4own, custom |
| 95 | Marvis | [CN-Marvis.list](CN-Marvis.list) | 4 | 5 | DIRECT | CN056 Marvis | v4own, custom |
| 96 | 铁路12306 | [CN-12306.list](CN-12306.list) | 16 | 16 | DIRECT | CN057 铁路12306 | bm:12306, v4own, custom |
| 97 | 携程旅行 | [CN-XieCheng.list](CN-XieCheng.list) | 37 | 31 | DIRECT | CN058 携程旅行 | bm:XieCheng, v2:ctrip, v4own, custom |
| 98 | 航旅纵横 | [CN-Umetrip.list](CN-Umetrip.list) | 6 | 6 | DIRECT | CN059 航旅纵横 | v4own, custom |
| 99 | 哈啰 | [CN-HelloBike.list](CN-HelloBike.list) | 4 | 4 | DIRECT | CN060 哈啰 | v4own, custom |
| 100 | 天府通 | [CN-TianFuTong.list](CN-TianFuTong.list) | 4 | 4 | DIRECT | CN061 天府通 | v4own, custom |
| 101 | 无忧行 | [CN-JegoTrip.list](CN-JegoTrip.list) | 4 | 4 | DIRECT | CN062 无忧行 | v4own, custom |
| 102 | 懂车帝 | [CN-DongCheDi.list](CN-DongCheDi.list) | 8 | 8 | DIRECT | CN063 懂车帝 | v2:dongchedi, v4own, custom |
| 103 | 汽车之家 | [CN-AutoHome.list](CN-AutoHome.list) | 9 | 9 | DIRECT | CN064 汽车之家 | v4own, custom |
| 104 | 吉利汽车 | [CN-Geely.list](CN-Geely.list) | 50 | 50 | DIRECT | CN065 吉利汽车 | bm:Geely, v4own, custom |
| 105 | 九号出行 | [CN-Ninebot.list](CN-Ninebot.list) | 6 | 6 | DIRECT | CN066 九号出行 | v4own, custom |
| 106 | Grow | [CN-Grow.list](CN-Grow.list) | 2 | 3 | DIRECT | CN086 Grow | v4own, custom |
| 107 | 米家 | [CN-MiHome.list](CN-MiHome.list) | 7 | 12 | DIRECT | CN087 米家 | v4own, custom |
| 108 | 华为智慧生活 | [CN-HuaweiSmartLife.list](CN-HuaweiSmartLife.list) | 11 | 11 | DIRECT | CN088 华为智慧生活 | v4own, custom |
| 109 | BOSS直聘 | [CN-BOSS.list](CN-BOSS.list) | 4 | 4 | DIRECT | CN093 BOSS直聘 | v4own, custom |
| 110 | 智联招聘 | [CN-Zhaopin.list](CN-Zhaopin.list) | 4 | 4 | DIRECT | CN094 智联招聘 | v4own, custom |
| 111 | 猎聘 | [CN-Liepin.list](CN-Liepin.list) | 4 | 4 | DIRECT | CN095 猎聘 | v2:liepin, v4own, custom |
| 112 | 企查查 | [CN-QCC.list](CN-QCC.list) | 3 | 3 | DIRECT | CN096 企查查 | v2:qcc, v4own, custom |
| 113 | 贝壳找房 | [CN-Beike.list](CN-Beike.list) | 8 | 8 | DIRECT | CN097 贝壳找房 | v4own, custom |
| 114 | 国家网络身份认证 | [CN-CTID.list](CN-CTID.list) | 3 | 5 | DIRECT | CN098 国家网络身份认证 | v4own, custom |
| 115 | 悦通行 | [CN-YueTongXing.list](CN-YueTongXing.list) | 3 | 4 | DIRECT | CN099 悦通行 | v4own, custom |
| 116 | 去上网（去哒） | [CN-QuShangWang.list](CN-QuShangWang.list) | 5 | 5 | DIRECT | CN100 去上网（去哒） | v4own, custom |
| 117 | 中国移动 | [CN-ChinaMobile.list](CN-ChinaMobile.list) | 50 | 38 | DIRECT | CN101 中国移动 | bm:ChinaMobile, v2:chinamobile, v4own, custom |
| 118 | UU远程 | [CN-UUYC.list](CN-UUYC.list) | 6 | 6 | DIRECT | CN102 UU远程 | v4own, custom |
| 119 | 交管12123 | [CN-Traffic12123.list](CN-Traffic12123.list) | 4 | 4 | DIRECT | CN103 交管12123 | v4own, custom |
| 120 | 个人所得税 | [CN-IncomeTax.list](CN-IncomeTax.list) | 4 | 5 | DIRECT | CN104 个人所得税 | v4own, custom |
| 121 | MONO记账 | [CN-MONO.list](CN-MONO.list) | 2 | 4 | DIRECT | CN105 MONO记账 | v4own, custom |
| 122 | Cookie | [CN-Cookie.list](CN-Cookie.list) | 2 | 3 | DIRECT | CN106 Cookie | v4own, custom |
| 123 | 上岛记 | [CN-ShangDaoJi.list](CN-ShangDaoJi.list) | 2 | 2 | DIRECT | CN107 上岛记 | v4own, custom |
| 124 | iCost | [CN-iCost.list](CN-iCost.list) | 4 | 4 | DIRECT | CN108 iCost | v4own, custom |
| 125 | 扫描全能王 | [CN-CamScanner.list](CN-CamScanner.list) | 10 | 10 | DIRECT | CN109 扫描全能王 | v4own, custom |
| 126 | 爱思全能版 | [CN-AiSi.list](CN-AiSi.list) | 5 | 5 | DIRECT | CN111 爱思全能版 | v4own, custom |
| 127 | GestaltEdit | [CN-GestaltEdit.list](CN-GestaltEdit.list) | 4 | 4 | DIRECT | CN124 GestaltEdit | v4own, custom |
| 128 | 全球网测 | [CN-NetSpeed.list](CN-NetSpeed.list) | 5 | 5 | DIRECT | CN130 全球网测 | v4own, custom |
| 129 | 彩云天气PRO | [CN-ColorfulClouds.list](CN-ColorfulClouds.list) | 6 | 6 | DIRECT | CN132 彩云天气PRO | v2:colorfulclouds, v4own, custom |
| 130 | Apple 音乐 | [CN-AppleMusic.list](CN-AppleMusic.list) | 7 | 7 | DIRECT | CN023 音乐 | v4own, custom |
| 131 | Apple 播客 | [CN-ApplePodcasts.list](CN-ApplePodcasts.list) | 3 | 5 | DIRECT | CN031 播客 | v4own, custom |
| 132 | Apple 视频（Apple TV） | [CN-AppleTV.list](CN-AppleTV.list) | 6 | 8 | DIRECT | CN032 视频（Apple TV） | v4own, custom |
| 133 | Apple 查找 | [CN-FindMy.list](CN-FindMy.list) | 6 | 6 | DIRECT | CN084 查找 | v4own, custom |
| 134 | Apple 健身 | [CN-FitnessPlus.list](CN-FitnessPlus.list) | 3 | 3 | DIRECT | CN085 健身 | v4own, custom |
| 135 | iTunes Store | [CN-iTunesStore.list](CN-iTunesStore.list) | 46 | 46 | DIRECT | CN128 iTunes Store | v4own, custom |
| 136 | Apple 系统 App 与基础服务（地图/电话/信息/照片/日历/邮件/备忘录/提醒/天气/健康/钱包/文件/设置/App Store/Watch/家庭/Numbers/翻译/语音备忘录/密码/图书/快捷指令/股市/FaceTime/支持/反馈/Apple Store/提示/无边记/手记/预览/相机/计算器/指南针/测距仪/放大器） | [CN-Apple.list](CN-Apple.list) | 19 | 155 | DIRECT | CN050 地图、CN067 电话、CN068 信息、CN069 Safari浏览器、CN070 照片、CN071 相机、CN072 日历、CN073 邮件、CN074 备忘录、CN075 提醒事项、CN076 天气、CN077 健康、CN078 钱包、CN079 计算器、CN080 文件、CN081 设置、CN082 App Store、CN083 Watch、CN089 家庭、CN090 Numbers表格、CN092 翻译、CN112 语音备忘录、CN113 指南针、CN114 测距仪、CN115 放大器、CN116 密码、CN117 图书、CN118 快捷指令、CN119 股市、CN120 FaceTime通话、CN121 支持、CN122 反馈、CN123 Apple Store、CN125 提示、CN126 无边记、CN127 手记、CN129 预览 | v4dep:apple-account, v4dep:apple-apns, v4dep:apple-feedback, v4dep:apple-icloud, v4dep:apple-maps, v4dep:apple-pki, v4dep:apple-search, v4dep:apple-store, v4dep:apple-update, v4own, custom |
| 137 | 腾讯集团共享（QQ/王者/掌盟/ima/Marvis 等共用） | [CN-Tencent.list](CN-Tencent.list) | 2578 | 2498 | DIRECT |  | bm:Tencent, v2:tencent, v4dep:tencent-shared, custom |
| 138 | 字节跳动集团共享（剪映等共用） | [CN-ByteDance.list](CN-ByteDance.list) | 841 | 862 | DIRECT |  | bm:ByteDance, v2:bytedance, v4dep:bytedance-cn-shared, custom |
| 139 | 阿里集团共享（淘宝/淘票票/1688/一淘/千问等共用） | [CN-Alibaba.list](CN-Alibaba.list) | 1338 | 1263 | DIRECT |  | bm:Alibaba, v2:alibaba, v4dep:alibaba-shared, custom |
| 140 | 网易集团共享 | [CN-NetEase.list](CN-NetEase.list) | 132 | 146 | DIRECT |  | bm:NetEase, v2:netease, v4dep:netease-shared, custom |
| 141 | 新浪集团共享 | [CN-Sina.list](CN-Sina.list) | 99 | 108 | DIRECT |  | bm:Sina, v2:sina, v4dep:sina-shared, custom |
| 142 | 华为集团共享 | [CN-Huawei.list](CN-Huawei.list) | 349 | 299 | DIRECT |  | bm:Huawei, v2:huawei, v4dep:huawei-shared, custom |
| 143 | 小米集团共享 | [CN-XiaoMi.list](CN-XiaoMi.list) | 151 | 157 | DIRECT |  | bm:XiaoMi, v2:xiaomi, v4dep:xiaomi-iot-shared, custom |
| 144 | 链家/贝壳集团共享 | [CN-Lianjia.list](CN-Lianjia.list) | 0 | 5 | DIRECT |  | v2:lianjia, v4dep:lianjia-shared, custom |
| 145 | 合合信息集团共享 | [CN-Intsig.list](CN-Intsig.list) | 1 | 5 | DIRECT |  | v2:intsig, v4dep:intsig-shared, custom |
| 146 | 国内通用基础设施（无法归属单一 App：Sukka domestic/direct、企业内网等） | [CN-Common.list](CN-Common.list) | 674 | 803 | DIRECT |  | v4common, custom |
