<p align="right">
  <a href="#english"><b>English</b></a> · <a href="#中文">中文</a>
</p>

# Surge-Diversion-Rules

Interactive Surge diversion / routing map + shareable profile by **Xiaomai**.

**Quick idea:** DNS/leak protection & ads first → high-risk finance & AI identity traffic on dedicated exits → China apps DIRECT → streaming / social on smart groups → everything else to International.

---

<a id="english"></a>
## English *(default)*

### Routing rules (short)

Traffic is matched **top to bottom**. In plain terms:

1. **Protect & clean** — block DoH/DoT bypass, STUN/WebRTC leaks; reject ads/trackers (with careful allowlists so apps don’t break).
2. **Finance** — Bybit EU → Germany; Bybit Global / OKX / Bitget / wallets / Binance / Wise → Taiwan pools; giffgaff → UK; PayPal → US residential (UK backup).
3. **AI & identity** — OpenAI / Claude / Grok / Gemini / Cursor / Meta / shared captcha & telemetry → **US residential** (same exit for login risk).
4. **TikTok** — US datacenter Smart group (no residential / 0.3X).
5. **China & LAN** — domestic apps, Apple CN/CDN, NTP, China IP / GEOIP → **DIRECT**.
6. **Streaming** — YouTube / Netflix / Viki + region stream sets → **Streaming** Smart (or JP/TW/UK pools where needed).
7. **International** — Discord / Telegram / WhatsApp / X / GitHub / global sets → **International** Smart.
8. **Final** — unmatched → International (`dns-failed` aware).

Policy groups: `AI住宅` · `TikTok` · `数字资产` · `Bybit 全球` · `Bybit 欧洲` · `英国专属` · `PayPal` · `流媒体` · `国际网络` (+ hidden regional pools).

### Neural rule map

![Surge rule neural map preview](assets/rule-map-preview.png)

> GitHub’s README cannot run JavaScript, so the live canvas is shown above as a preview image.
>
> **Open the built-in interactive map:** [`index.html`](./index.html) (same as [`rule-map.html`](./rule-map.html)) — download/open in Chrome, Safari, or Edge. Use the **EN / 中文** switch in the page header (defaults to English).

### Files

| File | Description |
|------|-------------|
| `index.html` / `rule-map.html` | Full interactive neural rule map (EN/中文 UI) |
| `Surge-Xiaomai.conf` | Main Surge profile |
| `Surge-Xiaomai-AdBlock.sgmodule` | Ad-blocking module |
| `assets/rule-map-preview.png` | Preview image embedded on this page |

### Setup

1. In `Surge-Xiaomai.conf`, replace `你的订阅` on `policy-path` with your Surge subscription URL.
2. Replace `your-subscribe-host.example` with your subscription host (DIRECT).
3. Import the `.conf` and enable the `.sgmodule` in Surge.
4. Open `index.html` locally to explore the graph (scroll to zoom, drag to pan, click nodes).

### Let an Agent do it for you

#### A) Manual Agent (you drive the chat)

Paste this prompt to Cursor / ChatGPT / Claude / Grok Bot (attach this repo or the three files):

```text
You are helping me customize Surge-Diversion-Rules for my own setup.
Repo files: Surge-Xiaomai.conf, Surge-Xiaomai-AdBlock.sgmodule, index.html.
Tasks:
1) Replace every placeholder 你的订阅 with MY_SURGE_SUBSCRIPTION_URL.
2) Replace your-subscribe-host.example with MY_SUBSCRIBE_HOST.
3) Keep policy logic unchanged unless I ask.
4) Return the full modified .conf (and .sgmodule if touched). Do not invent nodes.
My subscription URL: <PASTE_URL>
My subscribe host: <PASTE_HOST>
```

#### B) Agent → finished config file (hands-off)

Give the Agent write access to a working folder and paste:

```text
Clone or open https://github.com/dalao-all/Surge-Diversion-Rules
Read Surge-Xiaomai.conf.
Replace policy-path=你的订阅 with policy-path=<MY_SURGE_SUBSCRIPTION_URL>.
Replace your-subscribe-host.example with <MY_SUBSCRIBE_HOST>.
Write output to ./dist/Surge-Xiaomai.personalized.conf
Also copy Surge-Xiaomai-AdBlock.sgmodule to ./dist/
Print a short diff summary of placeholder replacements only.
Do not commit or push unless I say so.
```

### Convert to Shadowrocket (小火箭)

Shadowrocket cannot import Surge `.conf` / `.sgmodule` 1:1 (no Smart groups / MITM module parity). Practical paths:

1. **Subscription only (simplest)**  
   In Shadowrocket → Add Node → Type: Subscribe → paste the **same airport subscription URL** your provider gives. This gets nodes, not this repo’s full rule brain.

2. **Rules via converters**  
   Export/copy DOMAIN / DOMAIN-SUFFIX / RULE-SET lines from `Surge-Xiaomai.conf`, convert with a trusted Surge→Quantumult X / Clash tool, then import into Shadowrocket. Map groups roughly: DIRECT; REJECT*; AI/TikTok/finance/streaming/international → select groups with filtered nodes.

3. **Agent-assisted Shadowrocket draft**

```text
Convert Surge-Xiaomai.conf into a Shadowrocket-friendly rule list.
Constraints:
- No MITM / Script / Map Local / Body Rewrite (drop AdBlock module features).
- Approximate Smart/fallback groups as select groups with comments.
- Keep DOMAIN / DOMAIN-SUFFIX / IP-CIDR / GEOIP / FINAL.
- Replace 你的订阅 with <MY_URL>.
Output: paste-ready text plus a short “what was dropped” list.
```

4. **Expectation** — TikTok/AI/finance exit discipline will be weaker than Surge unless you recreate node filters carefully.

---

<a id="中文"></a>
## 中文

### 分流规则（简要）

规则按配置**从上到下**匹配，可以概括成：

1. **防护与清理** — 拦 DoH/DoT 旁路、STUN/WebRTC 泄漏；广告/追踪拒绝（保留必要白名单）。
2. **金融** — Bybit 欧洲走德国；Bybit 全球 / OKX / Bitget / 钱包 / 币安 / Wise 走台湾池；giffgaff 走英国；PayPal 优先美国家宽（英国备选）。
3. **AI 与身份** — OpenAI / Claude / Grok / Gemini / Cursor / Meta，以及共用验证码与遥测 → **美国家宽**。
4. **TikTok** — 美国机房 Smart（排除家宽 / 0.3X）。
5. **国内与局域网** — 国内 App、Apple 国内/CDN、NTP、国内 IP / GEOIP → **直连**。
6. **流媒体** — YouTube / Netflix / Viki 及分区流媒体集 → **流媒体** Smart（部分走日/台/英池）。
7. **国际网络** — Discord / Telegram / WhatsApp / X / GitHub 及全球规则集 → **国际网络** Smart。
8. **兜底** — 未命中 → 国际网络（含 `dns-failed`）。

### 神经网络分流图

![Surge 规则神经网络预览](assets/rule-map-preview.png)

> GitHub 描述页不能直接运行脚本，所以上面用预览图展示。
>
> **打开内置交互图：** [`index.html`](./index.html) — 用浏览器打开；支持 **EN / 中文**（默认英文）。

### 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` / `rule-map.html` | 可交互规则神经网络图 |
| `Surge-Xiaomai.conf` | Surge 主配置 |
| `Surge-Xiaomai-AdBlock.sgmodule` | 去广告模块 |
| `assets/rule-map-preview.png` | 本页预览图 |

### 使用步骤

1. 把 `policy-path` 的 `你的订阅` 换成你的 Surge 订阅链接。
2. 把 `your-subscribe-host.example` 改成你的订阅域名。
3. Surge 导入 `.conf` 并启用 `.sgmodule`。
4. 本地打开 `index.html` 查看拓扑。

### 让 Agent 代劳

#### A) 手动对话式 Agent

把仓库或三个文件丢给 Agent，粘贴：

```text
请根据 Surge-Diversion-Rules 帮我个性化配置。
文件：Surge-Xiaomai.conf、Surge-Xiaomai-AdBlock.sgmodule、index.html。
任务：
1) 把所有「你的订阅」替换为 MY_SURGE_SUBSCRIPTION_URL；
2) 把 your-subscribe-host.example 替换为 MY_SUBSCRIBE_HOST；
3) 不改分流逻辑，除非我另说；
4) 输出完整修改后的 .conf（如有改动也给出 .sgmodule）。不要编造节点。
我的订阅 URL：<粘贴>
我的订阅域名：<粘贴>
```

#### B) Agent 直接产出结果文件

```text
打开仓库 Surge-Diversion-Rules。
读取 Surge-Xiaomai.conf。
将 policy-path=你的订阅 替换为 policy-path=<我的订阅URL>。
将 your-subscribe-host.example 替换为 <我的订阅域名>。
写出 ./dist/Surge-Xiaomai.personalized.conf
并把 Surge-Xiaomai-AdBlock.sgmodule 复制到 ./dist/
只汇报占位符替换摘要。未经允许不要 commit/push。
```

### 转为 Shadowrocket（小火箭）

小火箭无法 1:1 吃 Surge 的 Smart / MITM / 脚本模块。可用路径：

1. **只导订阅** — 小火箭添加「订阅」节点，填机场订阅链接（只有节点，没有本仓库完整策略脑）。
2. **规则转换** — 提取 DOMAIN / DOMAIN-SUFFIX / RULE-SET，用可信 Surge→QX/Clash 转换后再导入小火箭；策略组按美国家宽 / 美国机房 / 台湾等自行对应。
3. **让 Agent 起草小火箭规则**

```text
把 Surge-Xiaomai.conf 转成 Shadowrocket 可用规则。
约束：去掉 MITM/Script/Map Local/Body Rewrite；Smart/fallback 改成 select 并注释；保留 DOMAIN/IP/GEOIP/FINAL；「你的订阅」换成 <我的URL>。
输出可粘贴文本 +「删减项」清单。
```

4. **预期** — 金融/AI/TikTok 出口纪律通常弱于 Surge，需自己维护节点过滤。
