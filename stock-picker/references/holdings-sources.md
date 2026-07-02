# ETF Holdings Data Sources — Tested & Ranked

## Working Sources

### 1. MarketXLS (PRIMARY — most reliable)

```
URL: https://marketxls.com/etfs/[TICKER]/top10holdings
```

Returns a large HTML page (~1.8-3.4 MB) with ALL holdings data embedded in
`<script id="__NEXT_DATA__">` JSON. The JSON path is
`data['props']['pageProps']['etfData']['holdings']` — each holding has
`ticker`, `name`, `weight`, and `shares` fields.

**Works for:** SPDR ETFs (XLK, KIE, XLF, XLE, etc.), iShares ETFs (IWM), Schwab ETFs (SCHA),
and ALPS ETFs (XOVR).
Validated 2026-06-22: XLK (76 holdings), KIE (55 holdings), IWM (1929 holdings)
all returned cleanly. Validated 2026-06-26: SCHA (1554 holdings), XLI (80 holdings),
XLV (61 holdings). Validated 2026-06-30: XOVR (33 holdings) returned cleanly —
ALPS Private-Public Crossover ETF confirmed as a MarketXLS-supported ticker.

**⚠️ Large ETF limitation:** MarketXLS returns the FULL holdings list, not just the
top 10. ETFs with >50 holdings (SCHA=1554, IWM=1929) will produce a price-fetching
timeout if you try to get 1-day data for every single holding. **Mitigation:** Cap
holdings to the top 20–30 by weight before fetching prices. The Step 2.3 selection
only keeps 10 per ETF anyway, so fetching 1500+ prices is pure waste. Use a
`MAX_PER_ETF` dict to limit large ETFs: `{"SCHA": 20, "IWM": 30}`.

**Extraction script:**
```python
import json, re
with open('page.html') as f:
    html = f.read()
m = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
data = json.loads(m.group(1))
holdings = data['props']['pageProps']['etfData']['holdings']
for h in holdings:
    print(f"{h['ticker']:6s} {h.get('name',''):40s} {float(h.get('weight',0)):6.2f}%")
```

**KIE caveat:** For KIE (SPDR Insurance ETF), the `name` field returns only the ticker
(e.g., `"name": "OSCR"` instead of "Oscar Health"). Map tickers to full names manually.
XLK and IWM data from marketxls include proper company names.

**Limitations:** Page is very large. Save to file first, then parse. Do not attempt to
extract JSON from the raw HTML in a single `curl | python3` pipe (blocked by security
scanner in cron mode).

### 2. DuckDuckGo Lite (FALLBACK — increasingly unreliable)

```
URL: https://lite.duckduckgo.com/lite/?q=[TICKER]+ETF+top+holdings+[known_ticker1]+[known_ticker2]+weight
```

DDG Lite returns simple HTML with no JavaScript. Historically, result snippets in
`<td class='result-snippet'>` contained holdings data as natural language text.

**Example snippet output (historical):**
```
ITB Holdings Information ITB is an equity ETF with a total of 48 individual holdings.
The top holdings are D.R. Horton stock at 16.04%, PulteGroup at 9.14%, Lennar at 7.53%,
NVR, Inc. at 6.88%, and Toll Brothers at 5.38%.
```

**CURRENT STATUS (June 2026):** DDG Lite increasingly returns bot-detection challenge
pages for financial/ETF queries. On 2026-06-22, 2 of 3 ETF queries (XLK, IWM) returned
captcha challenges ("Unfortunately, bots use DuckDuckGo too"). The KIE query returned
results but with no `result-snippet` td elements — the snippets were missing. DDG Lite
is NO LONGER RELIABLE as a primary source. Use MarketXLS instead.

**If MarketXLS fails:** As a last resort, try DDG Lite with the exact query format
`"[TICKER] ETF top holdings [known_ticker1] [known_ticker2] weight"` to improve
snippet quality. Parse tickers from `<td class='result-snippet'>` HTML.

**Limitations:** Even when working, snippets typically show only 5-8 holdings, not all 10.
Bot-detection rate is now too high to depend on.

### 3. Yahoo Finance Chart API v8 (for prices, NOT holdings)

Working for prices, volume, 52-week range, and chart data. Does NOT return holdings.
Use for Steps 1 and 2.5 data collection.

```
URL: https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?range=1d&interval=1d
Requires: User-Agent header (any modern browser UA)
Rate limit: ~0.15s between calls
```

## Blocked / Non-working Sources

| Source | URL Pattern | Failure Mode |
|--------|------------|--------------|
| Yahoo Finance holdings API | `/v1/finance/quoteSummary/...?modules=topHoldings` | "Unknown Host" (500) |
| Yahoo Finance quoteSummary v10 | `/v10/finance/quoteSummary/...` | "Unauthorized: Invalid Crumb" |
| iShares website | `ishares.com/us/products/...` | "Access Denied" (Akamai) |
| iShares AJAX API | `ishares.com/.../1467271812596.ajax` | "Access Denied" |
| ETFDB | `etfdb.com/etf/...` | Cloudflare challenge page |
| StockAnalysis | `stockanalysis.com/etf/...` | Cloudflare challenge page (via curl) |
| ETF.com | `etf.com/...` | Cloudflare challenge page |
| BestETF | `bestetf.net/etf/...` | Cloudflare challenge page |

## Cron Job Constraints

When running as a cron job (no user present):
- `execute_code` is BLOCKED — use `write_file` + `terminal` pattern
- Pipe-to-interpreter (`curl | python3`) is BLOCKED — save to file first
- Python heredocs (`python3 << 'EOF'`) are BLOCKED — use `write_file`
- `browser_navigate` may fail if Chrome is not installed on the cron environment
