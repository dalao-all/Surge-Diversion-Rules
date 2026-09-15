<p align="right">
  <a href="#english"><b>English</b></a> · <a href="#中文">中文</a>
</p>

# Surge-Diversion-Rules

Interactive Surge diversion / routing map + shareable profile by **Xiaomai**.

---

<a id="english"></a>
## English *(default)*

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

### 神经网络分流图

![Surge 规则神经网络预览](assets/rule-map-preview.png)

> GitHub 描述页不能直接运行带脚本的网页，所以上面用预览图展示效果。
>
> **打开内置交互图：** [`index.html`](./index.html)（与 [`rule-map.html`](./rule-map.html) 相同）— 下载后用 Chrome / Safari / Edge 打开。页面右上支持 **EN / 中文** 切换（默认英文）。

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
