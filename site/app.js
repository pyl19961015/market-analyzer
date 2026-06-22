(function () {
  "use strict";

  const dateSelect = document.getElementById("date-select");
  const generatedAt = document.getElementById("generated-at");
  const emptyState = document.getElementById("empty-state");
  const content = document.getElementById("content");

  function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (c) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    }[c]));
  }

  function formatPct(pct) {
    if (pct === null || pct === undefined) return "--";
    const sign = pct > 0 ? "+" : "";
    return `${sign}${pct}%`;
  }

  function changeClass(pct) {
    if (pct === null || pct === undefined || pct === 0) return "flat";
    return pct > 0 ? "up" : "down";
  }

  function renderQuoteGrid(elementId, quotes) {
    const grid = document.getElementById(elementId);
    grid.innerHTML = Object.entries(quotes).map(([label, info]) => `
      <div class="metric-card">
        <div class="label">${escapeHtml(label)}</div>
        <div class="value">${escapeHtml(info.last ?? "--")}</div>
        <div class="change ${changeClass(info.pct_change)}">${info.error ? escapeHtml(info.error) : formatPct(info.pct_change)}</div>
      </div>
    `).join("");
  }

  function renderRates(rates, usdJpy) {
    const grid = document.getElementById("rates-grid");
    const us = rates.us || {};
    const japan = rates.japan || {};
    const cards = [];

    if (usdJpy) {
      cards.push(`
        <div class="metric-card">
          <div class="label">USD/JPY</div>
          <div class="value">${escapeHtml(usdJpy.last ?? "--")}</div>
          <div class="change ${changeClass(usdJpy.pct_change)}">${formatPct(usdJpy.pct_change)}</div>
        </div>
      `);
    }

    if (us.error) {
      cards.push(`<div class="metric-card"><div class="label">美国联邦基金利率</div><div class="error-text">${escapeHtml(us.error)}</div></div>`);
    } else {
      cards.push(`
        <div class="metric-card">
          <div class="label">美国联邦基金目标区间</div>
          <div class="value">${escapeHtml(us.target_low)}–${escapeHtml(us.target_high)}%</div>
          <div class="change flat">EFFR ${escapeHtml(us.effr)}% · ${escapeHtml(us.as_of)}</div>
        </div>
      `);
    }

    if (japan.error) {
      cards.push(`<div class="metric-card"><div class="label">日本10年期国债收益率</div><div class="error-text">${escapeHtml(japan.error)}</div></div>`);
    } else {
      const deltaBp = japan.prev_yield !== undefined ? (japan.yield - japan.prev_yield) * 100 : null;
      cards.push(`
        <div class="metric-card">
          <div class="label">日本10年期国债收益率</div>
          <div class="value">${escapeHtml(japan.yield)}%</div>
          <div class="change ${changeClass(deltaBp)}">${deltaBp !== null ? `${deltaBp > 0 ? "+" : ""}${deltaBp.toFixed(1)}bp` : ""} · ${escapeHtml(japan.as_of)}</div>
        </div>
      `);
    }

    if (rates.spread_10y !== undefined) {
      cards.push(`
        <div class="metric-card">
          <div class="label">美日10年期利差</div>
          <div class="value">${escapeHtml(rates.spread_10y)}%</div>
          <div class="change flat">美债10Y − 日债10Y</div>
        </div>
      `);
    }

    grid.innerHTML = cards.join("");
  }

  function renderSectors(sectors) {
    const list = document.getElementById("sectors-list");
    const entries = Object.entries(sectors).sort((a, b) => (b[1].pct_change ?? 0) - (a[1].pct_change ?? 0));
    const maxAbs = Math.max(1, ...entries.map(([, v]) => Math.abs(v.pct_change ?? 0)));
    list.innerHTML = entries.map(([label, info]) => {
      const pct = info.pct_change ?? 0;
      const width = (Math.abs(pct) / maxAbs) * 50;
      const cls = changeClass(pct);
      return `
        <div class="bar-row">
          <span>${escapeHtml(label)}</span>
          <div class="bar-track">
            <div class="bar-fill ${cls}" style="width:${width}%"></div>
          </div>
          <span class="price">${escapeHtml(info.last ?? "--")} <span class="change ${cls}">${formatPct(pct)}</span></span>
        </div>
      `;
    }).join("");
  }

  function formatEventDate(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return iso;
    const weekday = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"][d.getDay()];
    return `${d.getMonth() + 1}月${d.getDate()}日 ${weekday}`;
  }

  function formatEventTime(iso) {
    const d = new Date(iso);
    if (isNaN(d)) return "";
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function renderCalendar(events) {
    const list = document.getElementById("calendar-list");
    if (!events || events.length === 0) {
      list.innerHTML = `<p class="error-text">暂无经济日历数据</p>`;
      return;
    }
    if (events[0].error) {
      list.innerHTML = `<p class="error-text">经济日历获取失败: ${escapeHtml(events[0].error)}</p>`;
      return;
    }
    const groups = new Map();
    for (const ev of events) {
      const dayKey = formatEventDate(ev.date);
      if (!groups.has(dayKey)) groups.set(dayKey, []);
      groups.get(dayKey).push(ev);
    }
    list.innerHTML = Array.from(groups.entries()).map(([day, evs]) => `
      <div class="event-day">
        <div class="event-day-header">${escapeHtml(day)}</div>
        ${evs.map((ev) => `
          <div class="event-row">
            <span class="event-time">${escapeHtml(formatEventTime(ev.date))}</span>
            <span class="event-title">
              <span class="impact-badge ${(ev.impact || "low").toLowerCase()}">${escapeHtml(ev.impact || "Low")}</span>
              <span class="country-tag">${escapeHtml(ev.country || "")}</span>
              ${escapeHtml(ev.title)}
            </span>
            <span class="event-figures">${escapeHtml(ev.forecast) || "&nbsp;"}${ev.previous ? ` / 前值 ${escapeHtml(ev.previous)}` : ""}</span>
          </div>
        `).join("")}
      </div>
    `).join("");
  }

  function formatPublished(value) {
    const d = new Date(value);
    if (isNaN(d)) return escapeHtml(value || "");
    return d.toLocaleString([], { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
  }

  function renderFeedGroups(containerId, groups) {
    const el = document.getElementById(containerId);
    el.innerHTML = Object.entries(groups).map(([label, items]) => `
      <div class="feed-group">
        <div class="feed-group-header">${escapeHtml(label)}</div>
        ${items.map((item) => item.error
          ? `<p class="error-text">${escapeHtml(item.error)}</p>`
          : `
            <a class="feed-item" href="${escapeHtml(item.link)}" target="_blank" rel="noopener noreferrer">
              <span class="feed-title">${escapeHtml(item.title)}</span>
              <span class="feed-time">${formatPublished(item.published)}</span>
            </a>
          `).join("")}
      </div>
    `).join("");
  }

  function renderReport(report) {
    generatedAt.textContent = `报告日期: ${report.date} · 生成时间: ${report.generated_at}`;
    renderQuoteGrid("indices-grid", report.market_sentiment.indices);
    renderSectors(report.market_sentiment.sectors);
    renderQuoteGrid("japan-grid", report.japan_market.indices);
    renderQuoteGrid("holdings-grid", report.watchlist.holdings);
    renderQuoteGrid("demand-drivers-grid", report.watchlist.demand_drivers);
    renderQuoteGrid("peers-grid", report.watchlist.peers);
    renderRates(report.rates, report.japan_market.indices["USD/JPY"]);
    renderCalendar(report.economic_calendar);
    renderFeedGroups("fed-list", report.fed_policy);
    renderFeedGroups("news-list", report.news);
  }

  async function loadReport(date) {
    const res = await fetch(`data/${date}.json`);
    const report = await res.json();
    renderReport(report);
  }

  function setupTabs() {
    const tabs = document.querySelectorAll(".tab");
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        tabs.forEach((t) => t.classList.remove("active"));
        document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
        tab.classList.add("active");
        document.getElementById(tab.dataset.target).classList.add("active");
      });
    });
  }

  async function init() {
    setupTabs();
    let dates = [];
    try {
      const res = await fetch("data/index.json");
      if (res.ok) dates = await res.json();
    } catch (e) {
      dates = [];
    }

    if (!dates || dates.length === 0) {
      emptyState.hidden = false;
      content.hidden = true;
      dateSelect.hidden = true;
      return;
    }

    dateSelect.innerHTML = dates.map((d) => `<option value="${escapeHtml(d)}">${escapeHtml(d)}</option>`).join("");
    dateSelect.addEventListener("change", () => loadReport(dateSelect.value));
    await loadReport(dates[0]);
  }

  init();
})();
