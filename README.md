# Surge-Diversion-Rules

<p align="center">
  <strong>Surge policy / rule design notes</strong><br/>
  <a href="./index.html">Open description page (EN / 中文 switch)</a>
</p>

> **Disclaimer / 声明**
>
> Rule-setting discussion and technical exchange only.
> Not sharing proxy access, not promoting any VPN/airport/service, not offering connectivity.
> Placeholders only (`你的订阅`). Not legal advice.
>
> 仅用于**规则设定交流与技术讨论**。不是分享接入、不是推广服务、不提供连接。占位符需自备有权使用的资源。

![Rule map preview](assets/rule-map-preview.png)

## Quick routing idea

DNS/leak controls & ads → finance / AI identity policies → domestic DIRECT → streaming & social groups → FINAL fallback.

## Files

| File | Role |
|------|------|
| [`index.html`](./index.html) | Description page: centered title + Surge icon + **one language at a time** (default English) |
| [`rule-map.html`](./rule-map.html) | Interactive neural rule map |
| `Surge-Xiaomai.conf` | Sample Surge profile (placeholders) |
| `Surge-Xiaomai-AdBlock.sgmodule` | Sample ad-related module |
| `assets/rule-map-preview.png` | Preview image on this page |

---

## English summary

### Routing logic
1. Protect and clean (DoH/DoT/STUN, ads)
2. Finance-related policy labels (EU / TW / UK / PayPal)
3. AI and identity-related policies
4. TikTok-related Smart policy example
5. Domestic and LAN → DIRECT
6. Streaming-related policies
7. General international policies
8. FINAL fallback

### How to view the single-language UI
Download/open [`index.html`](./index.html) in a browser. Switch **English / 中文** under the title — only one language is shown.

### Personalize (your own resources)
1. Replace `你的订阅` on `policy-path` with your own lawful subscription.
2. Replace `your-subscribe-host.example` if needed.
3. Optional Agent: rewrite placeholders only; do not invent nodes or provide access.

### Other clients (e.g. Shadowrocket)
Format study only — map DOMAIN/IP/GEOIP/FINAL syntax; Smart/MITM/Script may not translate 1:1.

---

## 中文摘要

### 分流逻辑
1. 防护与清理（DoH/DoT/STUN、广告）
2. 金融相关策略标签（欧/台/英/PayPal）
3. AI 与身份相关策略
4. TikTok 相关 Smart 样例
5. 国内与局域网 → 直连
6. 流媒体相关策略
7. 一般国际策略
8. FINAL 兜底

### 单语言描述页怎么看
用浏览器打开 [`index.html`](./index.html)。标题下方切换 **English / 中文**，同一时间只显示一种语言。

### 自行替换占位符
1. 把 `policy-path` 的 `你的订阅` 换成你有权使用的订阅。
2. 按需改 `your-subscribe-host.example`。
3. 可用 Agent 只改占位符，不要编造节点或提供接入。

### 其他客户端（如 Shadowrocket）
仅作规则写法/格式对照；Smart/MITM/脚本可能无法一一对应。

