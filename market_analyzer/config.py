"""Static config: tickers and feed URLs used by the fetchers."""

# Broad market + sentiment tickers (yfinance symbols)
INDEX_TICKERS = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^IXIC",
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT",
    "VIX": "^VIX",
    "10Y Treasury Yield": "^TNX",
    "US Dollar Index": "DX-Y.NYB",
    "Crude Oil WTI": "CL=F",
    "Gold": "GC=F",
}

SECTOR_ETFS = {
    "Technology": "XLK",
    "Financials": "XLF",
    "Energy": "XLE",
    "Health Care": "XLV",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Industrials": "XLI",
    "Utilities": "XLU",
    "Materials": "XLB",
    "Real Estate": "XLRE",
    "Communication Services": "XLC",
}

# Japan market tickers (yfinance symbols). TOPIX has no working Yahoo index
# ticker, so a TOPIX-tracking ETF (1306.T) is used as a price proxy instead.
JAPAN_INDEX_TICKERS = {
    "Nikkei 225": "^N225",
    "TOPIX (ETF代理)": "1306.T",
    "USD/JPY": "JPY=X",
}

# Corning (GLW) holding + the stocks most likely to move alongside it:
# - Demand drivers: Apple (Gorilla Glass/iPhone demand) and the hyperscalers
#   whose AI data-center capex drives Corning's Optical Communications
#   segment, currently its largest and fastest-growing business line.
# - Peers: direct comps in optical/connectivity components, plus AGC (Tokyo),
#   a specialty/display glass competitor.
HOLDINGS = {
    "Corning (持仓)": "GLW",
}

DEMAND_DRIVER_TICKERS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
}

PEER_TICKERS = {
    "Lumentum": "LITE",
    "Coherent": "COHR",
    "Amphenol": "APH",
    "AGC旭硝子(东京上市)": "5201.T",
}

# Free, no-key economic calendar feed (widely used by retail trading tools).
ECONOMIC_CALENDAR_URL = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
ECONOMIC_CALENDAR_COUNTRIES = ("USD", "JPY")

# NY Fed official reference rates API (free, no key) — gives EFFR/SOFR and
# the current FOMC target range.
NY_FED_RATES_URL = "https://markets.newyorkfed.org/api/rates/all/latest.json"

# Japan Ministry of Finance official JGB yield CSV for the current month
# (free, no key). Shift-JIS encoded, dates use the Japanese era calendar.
JGB_YIELD_CSV_URL = "https://www.mof.go.jp/jgbs/reference/interest_rate/jgbcm.csv"

# Official Federal Reserve RSS feeds (no key required).
FED_FEEDS = {
    "Press Releases": "https://www.federalreserve.gov/feeds/press_all.xml",
    "Speeches": "https://www.federalreserve.gov/feeds/speeches.xml",
    "FOMC Press Releases": "https://www.federalreserve.gov/feeds/press_monetary.xml",
}

# Free financial news RSS feeds (no key required).
NEWS_FEEDS = {
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "MarketWatch Top Stories": "https://feeds.content.dowjones.io/public/rss/mw_topstories",
    "CNBC Top News": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114",
}

REQUEST_TIMEOUT_SECONDS = 10
NEWS_ITEMS_PER_FEED = 8
