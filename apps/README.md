# 按 App 聚合的规则仓库（apps/ → dist/apps/）

目标：同一个 App 在 GitHub 各家规则仓库里都不完整（例如 blackmatrix7 的 Claude 只有 3 条），这里把所有来源的同一 App 取**并集**，
去重、清洗后，每个 App 输出一个文件 `dist/apps/<App>.list`，主配置直接按 App 引用。

## 文件
| 路径 | 作用 |
|---|---|
| `apps/manifest.json` | App 清单：顺序 = 优先级 = 主配置里的规则顺序；每个 App 的上游来源、可收 IP 的来源、排除项、建议策略 |
| `apps/custom/<App>.list` | 人工补充（抓包、1.3.6/V3.5.x 内联规则、官方文档）。这里的条目不会被“国内重叠”自动剔除 |
| `apps/build_apps.py` | 构建脚本（来源格式见文件头注释） |
| `apps/fetch_upstreams.sh` | 浅克隆全部上游到 `.upstream/`，并写 `dist/apps/sources.lock.json` |
| `apps/coverage_check.py` | 覆盖检查：`dist/v4` 海外条目必须被某个海外 App 表覆盖；`dist/v4/cn.list` 每一条必须落入某个 `CN-*` 表；豁免见 `apps/coverage_exempt.txt` |
| `dist/apps/CN-Guard.list` | 自动生成：被海外 App 关键词误吸的国内域名（如 speedtest.cn 被 Speedtest 的 `speedtest` 关键词吸走），配置中放在海外 App 层之前 DIRECT |
| `dist/apps/CN-Reject.list` | 自动生成：新扩国内表的后缀罩住了广告层原本拦截的域名，配置中放在国内单表之前 REJECT，广告拦截行为不变 |
| `dist/apps/README.md` | 自动生成的总表（每个 App 条目数、最大单一上游条目数、建议策略） |
| `dist/apps/report.json` | 每个来源贡献、丢弃原因、跨 App 冲突、国内重叠剔除明细 |

## 上游
v2fly/domain-list-community · blackmatrix7/ios_rule_script（原仓库，不再用 laobanbiefangcu 镜像）· ACL4SSR · VPSDance/ai-proxy-rules ·
xiaolai/anthropic-claude-surge-rules-set · SukkaW/Surge（ai.conf / global.conf / global.ts / stream.ts / telegram_asn）· Telegram 官方 cidr.txt。

## 清洗规则
1. 只保留 DOMAIN / DOMAIN-SUFFIX / DOMAIN-KEYWORD / DOMAIN-WILDCARD；IP 规则只从 `ip_sources` 指定的来源收取，并合并网段；USER-AGENT / PROCESS-NAME 丢弃。
2. v2fly：递归 include；海外 App 丢弃 `@cn`、国内 App 丢弃 `@!cn`；`@ads` 一律丢弃；regexp 无法表达，跳过并记录。
3. 同一 App 内：被自身后缀覆盖的子域删除。
4. 泛关键词（`keyword_denylist`，如 sentry / datadog / sift）丢弃，避免把所有 App 的遥测拉进 AI 出口。
5. 与国内表重叠（`dist/v4/cn.list`、Sukka domestic/direct、各 `CN-*` 表）的海外条目删除，例如 TikTok 表里的 `snssdk.com`（抖音共用）。
6. 跨 App：完全重复的条目只归排在前面的 App；被前面 App 后缀覆盖的条目删除（死规则）；含前面 App 品牌关键词的条目移入该 App。
7. 被 `dist/v4/protect-cn` 覆盖的条目删除（主配置里 protect-cn 在 App 表之前，属于死规则）。`override_protect_cn` 的 App（Tableau、B 站国际版）例外，须放在 protect-cn 之前。

## 国内 App（V3.5.6 起全量拆分）
国内 App 共 104 个表，覆盖仓库 v4 `rulekit_v4/apps.json` 的全部国内 App（CN001–CN132；CN131 Speedtest 走海外表 Speedtest，INT024 Tableau 走海外表 Tableau）。

- 来源 = 你的抓包与审核结果（`dist/v4/provenance.ndjson.gz` 里 cn / protect-cn 两类，每条带 App 编号）+ blackmatrix7 + v2fly 同名表的并集：
  - `v4own`：本表 `v4_app_ids` 认领的条目（含 protect-cn 业务端点、`rulekit_v4/custom/app-*.list`、`reviewed-*.list`、上游专属表）；
  - `v4dep:<组>`：集团共享依赖组（tencent-shared、alibaba-shared、apple-icloud …）的条目；
  - `v4common`：cn.list 里没有任何 App 归属的通用基础设施（Sukka domestic/direct 等）→ `CN-Common`。
- 归属顺序：**专属 App 在前 → 集团共享表在后 → CN-Common 最后**。一条规则被多个 App 认领时：同一集团（manifest 的 `family`）→ 归集团表；跨集团 → 归排序最前的表。
- 所有国内表策略都是 DIRECT，归属只决定“这条规则写在哪个文件里”，不改变路由；覆盖检查保证 `cn.list` 0 遗漏，所以主配置最终可以删掉 cn.list。
- 有些 App 的表很小或为空（如贝壳的条目都已归 CN-Beike、链家集团表 CN-Lianjia 为空），说明它的域名已被同集团或更前面的表收录，主配置不引用空表。
- `ads_trust`：V3.5.5 起就在国内层的 27 个表，上游条目视同已审核；其余新表的上游条目若本身是广告域名则剔除，若罩住广告域名则把广告域名写进 CN-Reject。

## 本地构建
```bash
bash apps/fetch_upstreams.sh          # 拉上游到 .upstream/
python3 apps/build_apps.py            # 生成 dist/apps/
python3 apps/coverage_check.py        # 覆盖检查
python3 -m unittest discover -s apps -p 'test_*.py'
```
GitHub Actions `.github/workflows/apps.yml`：每周一自动重建；修改 `apps/**`、`dist/v4/cn.list`、`provenance` 推送后，以及 v4 每日更新成功后立即重建。

## 新增 / 修改一个 App
1. 在 `manifest.json` 合适位置加一项（更专属的 App 放在更通用的 App 前面，例如 YouTube 在 Google 前）。
2. 抓包得到的域名写进 `apps/custom/<App>.list`。
3. 推送后 Actions 自动构建；主配置加一行 `RULE-SET,https://raw.githubusercontent.com/dalao-all/Surge-Diversion-Rules/main/dist/apps/<App>.list,<策略>`。
