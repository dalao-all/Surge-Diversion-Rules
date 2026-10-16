# 164 项应用 → 分类与覆盖矩阵

本表逐行来自 [`rulekit_v4/apps.json`](../rulekit_v4/apps.json)，按稳定 ID 保留 **CN001–CN132（132 项）与 INT001–INT032（32 项）**，不再沿用旧页眉“国内131/总159”。当前登记114个来源和28个共享依赖；来源详情、URL与许可见 [`sources.json`](../rulekit_v4/sources.json)，依赖定义见 apps.json。

**所有行都不是完整覆盖或本次手机业务实测声明。** 源存在、官方网页、集团共享或 Apple 基础网络都不能证明应用所有 API、登录、推送、付款和 CDN 已覆盖。13项未解决和5项本地工具仍保留原行，不编造域名；未匹配流量走主配置兜底。

“直接源数”仅计算该行 `source_ids`；“依赖数”计算 `dependency_ids`；“合并源数”是两者展开后来源ID的去重数量，不是域名条数。多个应用可以共享同一来源。状态是清单 `coverage.status` 的中文说明，可回到 JSON 查看原状态、证据、候选域和备注。

<!-- APP_MATRIX_START -->

| 稳定 ID | 应用名称 | 类别 | 覆盖状态 | 直接源数 | 依赖数 | 合并源数 |
| --- | --- | --- | --- | ---: | ---: | ---: |
| CN001 | 支付宝 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN002 | 云闪付 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN003 | 中国工商银行 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN004 | 中国建设银行 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN005 | 个人手机银行（四川农信） | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN006 | 招商银行 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN007 | 兴业银行 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN008 | 动卡空间 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN009 | 掌上生活 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN010 | 京东金融 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN011 | 微信 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN012 | 钉钉 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN013 | QQ | cn | shared-group-candidate | 0 | 1 | 1 |
| CN014 | 抖音 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN015 | 快手 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN016 | 小红书 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN017 | 哔哩哔哩 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN018 | 微博 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN019 | 快手极速版 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN020 | 网易云音乐 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN021 | 腾讯视频 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN022 | 爱奇艺 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN023 | 音乐 | cn | 独立来源候选 | 1 | 3 | 4 |
| CN024 | 剪映 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN025 | 王者荣耀 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN026 | 掌上英雄联盟 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN027 | 飞智游戏厅 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN028 | 酷安 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN029 | 猫眼 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN030 | 淘票票 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN031 | 播客 | cn | 独立来源候选 | 1 | 3 | 4 |
| CN032 | 视频（Apple TV） | cn | 独立来源候选 | 1 | 3 | 4 |
| CN033 | 淘宝 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN034 | 京东 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN035 | 拼多多 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN036 | 闲鱼 | cn | 独立来源候选 | 2 | 0 | 2 |
| CN037 | 美团 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN038 | 淘宝闪购 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN039 | 大众点评 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN040 | 盒马 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN041 | 山姆会员商店 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN042 | 得物 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN043 | 转转 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN044 | 阿里巴巴（1688） | cn | shared-group-candidate | 0 | 1 | 1 |
| CN045 | 京东AI购 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN046 | 一淘 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN047 | 京粉 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN048 | 省钱快报 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN049 | 高德地图 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN050 | 地图 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN051 | DeepSeek | cn | 独立来源候选 | 1 | 0 | 1 |
| CN052 | 豆包 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN053 | 千问 | cn | shared-group-candidate | 1 | 1 | 2 |
| CN054 | ima | cn | shared-group-candidate | 0 | 1 | 1 |
| CN055 | TRAE | cn | 独立来源候选 | 1 | 0 | 1 |
| CN056 | Marvis | cn | shared-group-candidate | 0 | 1 | 1 |
| CN057 | 铁路12306 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN058 | 携程旅行 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN059 | 航旅纵横 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN060 | 哈啰 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN061 | 天府通 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN062 | 无忧行 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN063 | 懂车帝 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN064 | 汽车之家 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN065 | 吉利汽车 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN066 | 九号出行 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN067 | 电话 | cn | shared-service-candidate | 0 | 2 | 2 |
| CN068 | 信息 | cn | shared-service-candidate | 0 | 4 | 4 |
| CN069 | Safari浏览器 | cn | target-site-routing | 0 | 5 | 5 |
| CN070 | 照片 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN071 | 相机 | cn | 本地功能为主 | 0 | 0 | 0 |
| CN072 | 日历 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN073 | 邮件 | cn | mail-provider-routing | 0 | 3 | 3 |
| CN074 | 备忘录 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN075 | 提醒事项 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN076 | 天气 | cn | shared-service-candidate | 0 | 2 | 2 |
| CN077 | 健康 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN078 | 钱包 | cn | shared-service-candidate | 0 | 2 | 2 |
| CN079 | 计算器 | cn | 本地功能为主 | 0 | 0 | 0 |
| CN080 | 文件 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN081 | 设置 | cn | shared-service-candidate | 0 | 4 | 4 |
| CN082 | App Store | cn | shared-service-candidate | 0 | 3 | 3 |
| CN083 | Watch | cn | shared-service-candidate | 0 | 5 | 5 |
| CN084 | 查找 | cn | shared-service-candidate | 1 | 4 | 5 |
| CN085 | 健身 | cn | shared-service-candidate | 1 | 3 | 4 |
| CN086 | Grow | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN087 | 米家 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN088 | 华为智慧生活 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN089 | 家庭 | cn | shared-service-candidate | 0 | 4 | 4 |
| CN090 | Numbers表格 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN091 | 网易有道词典 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN092 | 翻译 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN093 | BOSS直聘 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN094 | 智联招聘 | cn | existing-config-candidate | 1 | 0 | 1 |
| CN095 | 猎聘 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN096 | 企查查 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN097 | 贝壳找房 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN098 | 国家网络身份认证 | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN099 | 悦通行 | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN100 | 去上网（去哒） | cn | 未解决 | 0 | 0 | 0 |
| CN101 | 中国移动 | cn | 独立来源候选 | 1 | 0 | 1 |
| CN102 | UU远程 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN103 | 交管12123 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN104 | 个人所得税 | cn | 官方服务候选 | 1 | 0 | 1 |
| CN105 | MONO记账 | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN106 | Cookie | cn | 仅官方文档候选 | 1 | 0 | 1 |
| CN107 | 上岛记 | cn | 未解决 | 0 | 0 | 0 |
| CN108 | iCost | cn | 未解决 | 0 | 0 | 0 |
| CN109 | 扫描全能王 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN110 | 黑猫投诉 | cn | shared-group-candidate | 0 | 1 | 1 |
| CN111 | 爱思全能版 | cn | 未解决 | 0 | 0 | 0 |
| CN112 | 语音备忘录 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN113 | 指南针 | cn | 本地功能为主 | 0 | 0 | 0 |
| CN114 | 测距仪 | cn | 本地功能为主 | 0 | 0 | 0 |
| CN115 | 放大器 | cn | 本地功能为主 | 0 | 0 | 0 |
| CN116 | 密码 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN117 | 图书 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN118 | 快捷指令 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN119 | 股市 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN120 | FaceTime通话 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN121 | 支持 | cn | shared-service-candidate | 0 | 2 | 2 |
| CN122 | 反馈 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN123 | Apple Store | cn | shared-service-candidate | 0 | 3 | 3 |
| CN124 | GestaltEdit | cn | 未解决 | 0 | 0 | 0 |
| CN125 | 提示 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN126 | 无边记 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN127 | 手记 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN128 | iTunes Store | cn | shared-service-candidate | 1 | 3 | 4 |
| CN129 | 预览 | cn | shared-service-candidate | 0 | 3 | 3 |
| CN130 | 全球网测 | cn | 未解决 | 0 | 0 | 0 |
| CN131 | Speedtest | cn | 独立来源候选 | 1 | 0 | 1 |
| CN132 | 彩云天气PRO | cn | 独立来源候选 | 1 | 0 | 1 |
| INT001 | ChatGPT | ai | 独立来源候选 | 4 | 2 | 6 |
| INT002 | Claude | ai | 独立来源候选 | 2 | 1 | 3 |
| INT003 | Gemini | ai | 独立来源候选 | 2 | 1 | 3 |
| INT004 | Cursor | ai | 独立来源候选 | 1 | 1 | 2 |
| INT005 | Grok | ai | 独立来源候选 | 1 | 1 | 2 |
| INT006 | Grok Bot | ai | shared-group-candidate | 0 | 2 | 2 |
| INT007 | X | global | 独立来源候选 | 1 | 0 | 1 |
| INT008 | YouTube | stream | 独立来源候选 | 1 | 0 | 1 |
| INT009 | TikTok | tiktok | 独立来源候选 | 1 | 0 | 1 |
| INT010 | Instagram | global | 独立来源候选 | 1 | 0 | 1 |
| INT011 | Facebook | global | 独立来源候选 | 1 | 0 | 1 |
| INT012 | Netflix | stream | 独立来源候选 | 1 | 0 | 1 |
| INT013 | Viki | stream | 独立来源候选 | 1 | 0 | 1 |
| INT014 | WhatsApp | global | 独立来源候选 | 1 | 0 | 1 |
| INT015 | Telegram | global | 独立来源候选 | 1 | 0 | 1 |
| INT016 | Discord | global | 独立来源候选 | 1 | 0 | 1 |
| INT017 | Google | google | shared-group-candidate | 0 | 1 | 1 |
| INT018 | Chrome | google | target-site-routing | 0 | 1 | 1 |
| INT019 | Gmail | google | shared-group-candidate | 0 | 1 | 1 |
| INT020 | 云端硬盘（Google Drive） | google | 独立来源候选 | 1 | 0 | 1 |
| INT021 | Google Maps | google | shared-group-candidate | 0 | 1 | 1 |
| INT022 | Obsidian | global | 官方服务候选 | 1 | 0 | 1 |
| INT023 | DejaVocab | global | 仅官方文档候选 | 1 | 0 | 1 |
| INT024 | Tableau | cn | existing-config-candidate | 1 | 0 | 1 |
| INT025 | Sanas | global | 仅官方文档候选 | 1 | 0 | 1 |
| INT026 | gifgaff | uk | 独立来源候选 | 1 | 0 | 1 |
| INT027 | Shadowrocket | global | 未解决 | 0 | 0 | 0 |
| INT028 | Surge | global | 官方服务候选 | 1 | 0 | 1 |
| INT029 | PayPal | paypal | 独立来源候选 | 1 | 0 | 1 |
| INT030 | Wise | wise | 独立来源候选 | 1 | 0 | 1 |
| INT031 | Binance | binance | 独立来源候选 | 1 | 0 | 1 |
| INT032 | OKX | okx | 独立来源候选 | 1 | 0 | 1 |

<!-- APP_MATRIX_END -->

## 分类与出口

`ai` / `tiktok` → 美国住宅优先 fallback；`stream` → 流媒体 Smart；`google` / `global` → 普通国际 Smart；`uk` → 英国住宅优先、同国机房 fallback；`cn` → DIRECT。必要的精确共享登录端点可能有独立依赖，不能据此把整个 Google 业务归入 AI 住宅。

公开配置 `[Proxy]` 为空，需要用户自行填入节点并核对策略组引用。矩阵中的类别表达规则意图，实际出口与业务可用性需在设备上确认。

## 覆盖状态汇总

- 独立来源候选（`independent-candidate`）：58 项。
- 仅官方文档候选（`official-document-only`）：8 项。
- 官方服务候选（`official-service-candidate`）：3 项。
- 集团共享候选（`shared-group-candidate`）：29 项。
- 原配置候选（`existing-config-candidate`）：8 项。
- 共享服务候选（`shared-service-candidate`）：33 项。
- 未解决（`unresolved`）：13 项。
- 按目标站点分流（`target-site-routing`）：2 项。
- 本地工具/无独立网络规则（`local-only`）：5 项。
- 按邮箱服务商分流（`mail-provider-routing`）：1 项。

当前210个真实域名静态探针仅检查规则命中，不能替代手机启动、登录和主要业务验收。来源、依赖或状态有变化时，应从同一 apps.json 重生成本矩阵，并核对164个稳定ID和行数。
