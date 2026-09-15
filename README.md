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

---

<a id="中文"></a>
## 中文

### 分流规则（简要）

规则按配置**从上到下**匹配，可以概括成：

1. **防护与清理** — 拦 DoH/DoT 旁路、STUN/WebRTC 泄漏；广告/追踪拒绝（保留必要白名单，减少 App 异常）。
2. **金融** — Bybit 欧洲走德国；Bybit 全球 / OKX / Bitget / 钱包 / 币安 / Wise 走台湾池；giffgaff 走英国；PayPal 优先美国家宽（英国备选）。
3. **AI 与身份** — OpenAI / Claude / Grok / Gemini / Cursor / Meta，以及共用验证码与遥测 → **美国家宽**（登录风控同出口）。
4. **TikTok** — 美国机房 Smart（排除家宽 / 0.3X）。
5. **国内与局域网** — 国内 App、Apple 国内/CDN、NTP、国内 IP / GEOIP → **直连**。
6. **流媒体** — YouTube / Netflix / Viki 及分区流媒体集 → **流媒体** Smart（部分走日/台/英池）。
7. **国际网络** — Discord / Telegram / WhatsApp / X / GitHub 及全球规则集 → **国际网络** Smart。
8. **兜底** — 未命中 → 国际网络（含 `dns-failed`）。

策略组：`AI住宅` · `TikTok` · `数字资产` · `Bybit 全球` · `Bybit 欧洲` · `英国专属` · `PayPal` · `流媒体` · `国际网络`（另有隐藏地区节点池）。

### 神经网络分流图

![Surge 规则神经网络预览](assets/rule-map-preview.png)

> GitHub 描述页不能直接运行带脚本的网页，所以上面用预览图展示效果。
>
> **打开内置交互图：** [`index.html`](./index.html)（与 [`rule-map.html`](./rule-map.html) 相同）— 下载后用 Chrome / Safari / Edge 打开。页面支持 **EN / 中文** 切换（默认英文）。

### 文件说明

| 文件 | 说明 |
|------|------|
| `index.html` / `rule-map.html` | 完整可交互规则神经网络图（中英界面） |
| `Surge-Xiaomai.conf` | Surge 主配置 |
| `Surge-Xiaomai-AdBlock.sgmodule` | 去广告模块 |
| `assets/rule-map-preview.png` | 本页嵌入的预览图 |

### 使用步骤

1. 在 `Surge-Xiaomai.conf` 里把 `policy-path` 的 `你的订阅` 换成你的 Surge 订阅链接。
2. 把 `your-subscribe-host.example` 改成你的订阅域名（直连）。
3. 在 Surge 导入 `.conf` 并启用 `.sgmodule`。
4. 本地打开 `index.html` 查看分流拓扑（滚轮缩放、拖拽平移、点击节点）。
