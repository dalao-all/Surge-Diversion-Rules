# 按 App 规则集（dist/apps）

构建日期：2026-10-17。每个 App 一个文件，内容为多个上游同名规则的并集（去重、剔除国内共用域名、跨 App 冲突按优先级归属）。

引用格式：`RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/dist/apps/<App>.list,<策略>`

表格顺序即推荐的规则顺序（共享域名只归属排在前面的 App）。详细来源统计见 report.json，上游提交见 sources.lock.json。

| # | App | 文件 | 条目 | 最大单一上游 | 建议策略 | 上游 |
|---|---|---|---|---|---|---|
| 1 | OKX | [OKX.list](OKX.list) | 21 | 9 | 🪙 OKX 台湾 | v2:okx, bm:OKX, custom |
| 2 | Binance | [Binance.list](Binance.list) | 48 | 45 | 🪙 Binance 台湾 | v2:binance, bm:Binance, acl:Binance.list, custom |
| 3 | Bybit | [Bybit.list](Bybit.list) | 35 | 16 | 💳 Bybit 全球 | v2:bybit, repo-patch:finance-bybit-global, custom |
| 4 | Bybit EU | [BybitEU.list](BybitEU.list) | 7 | 1 | 🇩🇪 Bybit 欧洲 | repo-patch:finance-bybit-eu, custom |
| 5 | Bitget Wallet | [BitgetWallet.list](BitgetWallet.list) | 8 | 0 | 🪙 数字资产 | custom |
| 6 | UU Wallet | [UUWallet.list](UUWallet.list) | 1 | 0 | 🪙 数字资产 | custom |
| 7 | Plasma One | [PlasmaOne.list](PlasmaOne.list) | 3 | 0 | 🪙 数字资产 | custom |
| 8 | 其他交易所/钱包/链上工具 + WalletConnect/Reown | [Crypto-Common.list](Crypto-Common.list) | 197 | 197 | 🪙 数字资产 | bm:Crypto, bm:Cryptocurrency, custom |
| 9 | PayPal | [PayPal.list](PayPal.list) | 241 | 247 | 💳 PayPal 美国 | v2:paypal, bm:PayPal, custom |
| 10 | Wise | [Wise.list](Wise.list) | 2 | 2 | 💸 Wise 台湾 | v2:wise, custom |
| 11 | AI 通用依赖（验证码/风控/特性开关/登录） | [AI-Common.list](AI-Common.list) | 28 | 7 | 🤖 AI住宅 | repo-custom:reviewed-ai-auth, repo-custom:ai-login-endpoints, repo-custom:ai-challenge, repo-custom:ai-featureflags, custom |
| 12 | Claude | [Claude.list](Claude.list) | 39 | 34 | 🤖 AI住宅 | v2:anthropic, bm:Claude, acl:Claude.list, acl:ClaudeAI.list, vpsd:anthropic, xiaolai:anthropic, sukka-ai:Anthropic / Claude, bm:Anthropic, custom |
| 13 | ChatGPT / OpenAI | [ChatGPT.list](ChatGPT.list) | 31 | 30 | 🤖 AI住宅 | v2:openai, bm:OpenAI, acl:OpenAi.list, vpsd:openai, sukka-ai:OpenAI / ChatGPT, custom |
| 14 | Gemini / Google AI | [Gemini.list](Gemini.list) | 50 | 47 | 🤖 AI住宅 | v2:google-gemini, v2:google-deepmind, bm:Gemini, acl:Gemini.list, vpsd:google-ai, sukka-ai:Google, bm:BardAI, custom |
| 15 | Grok / xAI | [Grok.list](Grok.list) | 6 | 4 | 🤖 AI住宅 | v2:xai, vpsd:x-ai, sukka-ai:Grok, custom |
| 16 | Cursor | [Cursor.list](Cursor.list) | 8 | 5 | 🤖 AI住宅 | v2:cursor, vpsd:cursor, sukka-ai:Cursor, custom |
| 17 | 其他 AI（Perplexity/Copilot/HuggingFace/Mistral/OpenRouter/Windsurf/Poe/Groq/…） | [AI-Other.list](AI-Other.list) | 76 | 40 | 🤖 AI住宅 | vpsd:perplexity, vpsd:copilot, vpsd:huggingface, vpsd:mistral-ai, vpsd:openrouter, vpsd:windsurf, vpsd:poe, vpsd:groq, vpsd:cohere, vpsd:midjourney, vpsd:replit, vpsd:sourcegraph, vpsd:zed, vpsd:augment-code, vpsd:meta-ai, v2:perplexity, v2:github-copilot, v2:huggingface, v2:poe, v2:windsurf, v2:groq, sukka-ai:Perplexity, sukka-ai:POE, sukka-ai:GitHub Copilot, sukka-ai:groq, sukka-ai:OpenRouter AI - Unified Relay, sukka-ai:Windsurf (formerly Codeium), sukka-ai:Meta AI, bm:Copilot, sukka-ai:Cloudflare AI Gateway, sukka-ai:Dify.AI, sukka-ai:Jasper, sukka-ai:OpenArt, sukka-ai:JetBrains AI, custom |
| 18 | Notion | [Notion.list](Notion.list) | 9 | 7 | 🤖 AI住宅 | v2:notion, bm:Notion, custom |
| 19 | IP 检测站点 | [IPCheck.list](IPCheck.list) | 9 | 0 | 🤖 AI住宅 | custom |
| 20 | YouTube | [YouTube.list](YouTube.list) | 179 | 178 | 📺 YouTube | v2:youtube, bm:YouTube, bm:YouTubeMusic, acl:YouTube.list, acl:YouTubeMusic.list, sukka-stream:YouTube, sukka-stream:YouTube Music, custom |
| 21 | Google（搜索/Chrome/Gmail/地图/云端硬盘/Play/FCM/Authenticator） | [Google.list](Google.list) | 735 | 942 | 🤖 AI住宅 | v2:google, bm:Google, bm:GoogleDrive, bm:GoogleEarth, bm:GoogleFCM, acl:Google.list, acl:GoogleFCM.list, acl:GoogleEarth.list, sukka-global:GOOGLE, sukka-gl:Google, bm:GoogleSearch, bm:GoogleVoice, custom |
| 22 | TikTok（国际版） | [TikTok.list](TikTok.list) | 67 | 36 | 🎵 TikTok | v2:tiktok, bm:TikTok, acl:TikTok.list, sukka-stream:TikTok, custom |
| 23 | WhatsApp | [WhatsApp.list](WhatsApp.list) | 13 | 11 | 💬 WhatsApp | v2:whatsapp, bm:Whatsapp, acl:Whatsapp.list, custom |
| 24 | Instagram | [Instagram.list](Instagram.list) | 74 | 72 | 📘 Meta | v2:instagram, bm:Instagram, acl:Instagram.list, custom |
| 25 | Threads | [Threads.list](Threads.list) | 2 | 2 | 📘 Meta | v2:threads, bm:Threads, custom |
| 26 | Facebook / Messenger | [Facebook.list](Facebook.list) | 491 | 570 | 📘 Meta | v2:facebook, v2:messenger, v2:facebook-dev, bm:Facebook, acl:Facebook.list, sukka-gl:Facebook, custom |
| 27 | Reddit | [Reddit.list](Reddit.list) | 13 | 12 | 👽 Reddit | v2:reddit, bm:Reddit, acl:Reddit.list, sukka-gl:Reddit, custom |
| 28 | Netflix | [Netflix.list](Netflix.list) | 1154 | 1156 | 🎬 Netflix | v2:netflix, bm:Netflix, acl:Netflix.list, acl:NetflixIP.list, sukka-stream:Netflix, custom |
| 29 | Telegram | [Telegram.list](Telegram.list) | 47 | 40 | ✈️ Telegram | v2:telegram, bm:Telegram, acl:Telegram.list, bm:TelegramNL, bm:TelegramSG, bm:TelegramUS, custom |
| 30 | X / Twitter | [X.list](X.list) | 39 | 33 | 🐦 X | v2:twitter, bm:Twitter, acl:Twitter.list, sukka-gl:Twitter, custom |
| 31 | Discord | [Discord.list](Discord.list) | 29 | 29 | 🎮 Discord | v2:discord, bm:Discord, acl:Discord.list, sukka-gl:Discord, custom |
| 32 | Viki | [Viki.list](Viki.list) | 7 | 7 | 🎬 流媒体 | bm:Viki, custom |
| 33 | Bilibili 国际版 | [BilibiliIntl.list](BilibiliIntl.list) | 7 | 4 | 🎬 流媒体 | sukka-stream:Bilibili International, bm:BiliBiliIntl, custom |
| 34 | GitHub | [GitHub.list](GitHub.list) | 61 | 65 | 🌍 国际网络 | v2:github, bm:GitHub, acl:Github.list, sukka-gl:GitHub, custom |
| 35 | Obsidian | [Obsidian.list](Obsidian.list) | 1 | 1 | 🌍 国际网络 | repo-custom:app-INT022, custom |
| 36 | DejaVocab | [DejaVocab.list](DejaVocab.list) | 1 | 1 | 🌍 国际网络 | repo-custom:app-INT023, custom |
| 37 | Sanas | [Sanas.list](Sanas.list) | 1 | 2 | 🌍 国际网络 | repo-custom:app-INT025, custom |
| 38 | Tableau | [Tableau.list](Tableau.list) | 5 | 4 | 🌍 国际网络 | repo-custom:app-INT024, custom |
| 39 | Surge / Shadowrocket（代理工具自身） | [Surge.list](Surge.list) | 5 | 1 | 🌍 国际网络 | repo-custom:app-INT028, custom |
| 40 | Speedtest | [Speedtest.list](Speedtest.list) | 10 | 13 | 🌍 国际网络 | v2:ookla-speedtest, bm:Speedtest, sukka-gl:Speedtest, custom |
| 41 | giffgaff | [giffgaff.list](giffgaff.list) | 4 | 2 | 🇬🇧 英国专属 | v2:giffgaff, custom |
| 42 | 通用海外服务（非单一 App） | [Global-Misc.list](Global-Misc.list) | 16 | 0 | 🌍 国际网络 | custom |
| 43 | AliPay（国内） | [CN-AliPay.list](CN-AliPay.list) | 21 | 21 | DIRECT | bm:AliPay, custom |
| 44 | UnionPay（国内） | [CN-UnionPay.list](CN-UnionPay.list) | 17 | 16 | DIRECT | bm:UnionPay, v2:unionpay, custom |
| 45 | ICBC（国内） | [CN-ICBC.list](CN-ICBC.list) | 58 | 58 | DIRECT | bm:ICBC, v2:icbc, custom |
| 46 | CCB（国内） | [CN-CCB.list](CN-CCB.list) | 18 | 18 | DIRECT | bm:CCB, v2:ccb, custom |
| 47 | CMB（国内） | [CN-CMB.list](CN-CMB.list) | 39 | 38 | DIRECT | bm:CMB, v2:cmb, custom |
| 48 | JingDong（国内） | [CN-JingDong.list](CN-JingDong.list) | 269 | 249 | DIRECT | bm:JingDong, v2:jd, custom |
| 49 | WeChat（国内） | [CN-WeChat.list](CN-WeChat.list) | 330 | 330 | DIRECT | bm:WeChat, custom |
| 50 | DingTalk（国内） | [CN-DingTalk.list](CN-DingTalk.list) | 14 | 11 | DIRECT | bm:DingTalk, v2:dingtalk, custom |
| 51 | TencentVideo（国内） | [CN-TencentVideo.list](CN-TencentVideo.list) | 50 | 51 | DIRECT | bm:TencentVideo, custom |
| 52 | Tencent（国内） | [CN-Tencent.list](CN-Tencent.list) | 554 | 560 | DIRECT | bm:Tencent, v2:tencent, custom |
| 53 | DouYin（国内） | [CN-DouYin.list](CN-DouYin.list) | 78 | 71 | DIRECT | bm:DouYin, v2:douyin, custom |
| 54 | KuaiShou（国内） | [CN-KuaiShou.list](CN-KuaiShou.list) | 688 | 678 | DIRECT | bm:KuaiShou, v2:kuaishou, custom |
| 55 | XiaoHongShu（国内） | [CN-XiaoHongShu.list](CN-XiaoHongShu.list) | 10 | 9 | DIRECT | bm:XiaoHongShu, v2:xiaohongshu, custom |
| 56 | BiliBili（国内） | [CN-BiliBili.list](CN-BiliBili.list) | 120 | 123 | DIRECT | bm:BiliBili, v2:bilibili, custom |
| 57 | Weibo（国内） | [CN-Weibo.list](CN-Weibo.list) | 4 | 4 | DIRECT | bm:Weibo, custom |
| 58 | NetEaseMusic（国内） | [CN-NetEaseMusic.list](CN-NetEaseMusic.list) | 28 | 28 | DIRECT | bm:NetEaseMusic, custom |
| 59 | iQIYI（国内） | [CN-iQIYI.list](CN-iQIYI.list) | 56 | 56 | DIRECT | bm:iQIYI, v2:iqiyi, custom |
| 60 | ByteDance（国内） | [CN-ByteDance.list](CN-ByteDance.list) | 904 | 862 | DIRECT | bm:ByteDance, v2:bytedance, custom |
| 61 | Coolapk（国内） | [CN-Coolapk.list](CN-Coolapk.list) | 3 | 3 | DIRECT | bm:Coolapk, v2:coolapk, custom |
| 62 | GaoDe（国内） | [CN-GaoDe.list](CN-GaoDe.list) | 9 | 9 | DIRECT | bm:GaoDe, custom |
| 63 | Alibaba（国内） | [CN-Alibaba.list](CN-Alibaba.list) | 362 | 339 | DIRECT | bm:Alibaba, v2:alibaba, custom |
| 64 | Pinduoduo（国内） | [CN-Pinduoduo.list](CN-Pinduoduo.list) | 7 | 7 | DIRECT | bm:Pinduoduo, v2:pinduoduo, custom |
| 65 | MeiTuan（国内） | [CN-MeiTuan.list](CN-MeiTuan.list) | 19 | 19 | DIRECT | bm:MeiTuan, v2:meituan, custom |
| 66 | ZhuanZhuan（国内） | [CN-ZhuanZhuan.list](CN-ZhuanZhuan.list) | 4 | 4 | DIRECT | bm:ZhuanZhuan, custom |
| 67 | 12306（国内） | [CN-12306.list](CN-12306.list) | 15 | 15 | DIRECT | bm:12306, custom |
| 68 | XieCheng（国内） | [CN-XieCheng.list](CN-XieCheng.list) | 37 | 29 | DIRECT | bm:XieCheng, v2:ctrip, custom |
| 69 | ChinaMobile（国内） | [CN-ChinaMobile.list](CN-ChinaMobile.list) | 50 | 38 | DIRECT | bm:ChinaMobile, v2:chinamobile, custom |
