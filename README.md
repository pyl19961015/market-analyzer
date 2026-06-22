# 每日市场因素分析

每日抓取可能影响美股/日股走势的因素，汇总为一份报告并通过静态看板展示：

- **美股**：标普/纳指/道指/罗素2000、VIX、10年期美债收益率、美元指数、原油、黄金，以及11个板块ETF表现（yfinance，免费）
- **日股**：日经225、TOPIX（ETF代理）、USD/JPY（yfinance，免费）
- **美日利率**：美联储联邦基金目标区间+EFFR（NY Fed官方API）、日本10年期国债收益率（日本财务省官方CSV）、美日10年期利差
- **个股**：当前持仓康宁(GLW) + 下游需求驱动（苹果、四大云厂商）+ 同业对标（Lumentum、Coherent、Amphenol、AGC）
- **宏观经济日历**：本周美国/日本高/中/低重要性经济数据发布（CPI、非农、PMI、FOMC、BOJ等，免费日历feed）
- **美联储动态**：美联储官方新闻稿、官员讲话、FOMC声明（联储官方RSS）
- **新闻头条**：Yahoo Finance / MarketWatch / CNBC 财经新闻RSS

所有数据源均为免费/公开接口，无需API key。

看板是纯静态网页（HTML/CSS/JS，无服务端依赖），支持手机浏览，可直接部署到任意静态托管。

## 使用方法

```bash
# 生成今日报告（保存到 reports/YYYY-MM-DD.json，并同步到 docs/data/）
uv run python -m market_analyzer.report

# 本地预览看板
cd docs && python3 -m http.server 8765
# 浏览器打开 http://localhost:8765/
```

每次生成新报告后，`docs/data/` 会自动同步最新的 JSON 数据和日期索引，看板里的日期选择器会显示所有历史报告。

## 部署：GitHub Pages + Actions 自动刷新

`.github/workflows/refresh-data.yml` 在工作日每15分钟（00:00-21:00 UTC，覆盖日股+美股交易时段）自动跑一次 `uv run python -m market_analyzer.report`，把新数据 commit & push 回仓库；GitHub Pages 配置为从 `main` 分支的 `/docs` 目录发布，每次 push 会自动重新发布，看板就能看到最新数据。也可以在 Actions 页面手动触发（workflow_dispatch）。

仓库是 **public**，所以 Actions 分钟数不限量；如果改成 private，免费额度每月只有2000分钟，按当前频率大概率会超额。

## 项目结构

```
.github/workflows/
  refresh-data.yml       # 定时抓取数据 + commit + push
market_analyzer/
  config.py              # 股票代码、RSS地址等配置
  report.py               # 聚合所有数据，生成/保存每日报告
  build_site.py           # 把 reports/ 同步到 docs/data/（含日期索引）
  fetchers/
    market_data.py        # 美股/日股指数、板块、个股报价 (yfinance)
    rates.py               # 美联储EFFR/目标区间、日本JGB收益率
    watchlist.py            # 持仓 + 下游需求驱动 + 同业对标
    economic_calendar.py  # 宏观经济日历（美国+日本）
    fed_policy.py         # 美联储RSS
    news.py                # 财经新闻RSS
reports/                  # 每日生成的JSON报告（按日期命名）
docs/                     # 静态看板（GitHub Pages 发布目录）
  index.html
  style.css
  app.js
  data/                   # 报告数据副本 + index.json（由 build_site.py 生成）
```
