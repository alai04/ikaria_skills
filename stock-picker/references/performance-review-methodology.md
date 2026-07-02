# Performance Review Methodology

How to review stock-picker performance by comparing 5-minute post-pick average
prices against closing prices. Validated on 2026-06-24 (8 pick-events, gap-up day),
2026-06-25 (9 picks, flat-open day), 2026-06-26 (7 picks, defensive rotation),
2026-06-29 (8 picks, gap-up day, dual session), 2026-06-30 (10 picks,
Momentum Gap-Up day, dual session — first morning-beats-afternoon gap-up),
and 2026-07-01 (7 picks, bearish correction, universal SMA crossover failure,
commodity sector trap).

## When to Use

Run as a next-day cron job to evaluate the previous trading day's picks from both
the morning (开盘后) and afternoon (午后) sessions.

## Step 1: Extract Picks from Past Sessions

Use `session_search` with query like `"stock-picker 选股 YYYY-MM-DD"` to find both
sessions from the target date. Scroll into each session to extract:
- Ticker, company name, recommended action (BUY/BUY ON DIP/WATCH)
- Approximate pick time (morning ~09:55 AM ET, afternoon ~02:15 PM ET)
- Entry zone, stop, target (for context)
- RSI, sector, score (from step3 results JSON)

**If only one session is found (e.g., the afternoon cron didn't fire), run the**
**review with available data and note the missing session in the report.**

## Step 2: Fetch Intraday 5-Minute Data

Use the Yahoo Finance chart API with period1/period2 Unix timestamps covering
the full trading day (09:30 AM – 04:00 PM ET = 13:30 – 20:00 UTC).

```bash
# For each ticker:
curl -s -H "User-Agent: Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?period1=START_UNIX&period2=END_UNIX&interval=5m"
```

Parse `chart.result[0].timestamp` and `indicators.quote[0].close` for 5-min candles.
Include VOO as the benchmark.

**⚠️ Yahoo Finance rate-limits aggressively.** Always:
- Use `-H "User-Agent: Mozilla/5.0"` header
- Add `time.sleep(0.3)` between requests
- Save each ticker's response to a separate file with `curl -o`, then read+parse
- Do NOT pipe `curl | python3` — blocked by the security scanner in cron

**Python template** (write to file, then `terminal()` to run — `execute_code` blocked in cron):

```python
from datetime import datetime, timezone, timedelta

start = datetime(YYYY, M, D, 13, 0, 0, tzinfo=timezone.utc)  # 9:00 AM ET
end   = datetime(YYYY, M, D, 20, 30, 0, tzinfo=timezone.utc) # 4:30 PM ET
period1 = int(start.timestamp())
period2 = int(end.timestamp())

for ticker in STOCKS:
    outfile = f"/tmp/intra_{ticker}.json"
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={period1}&period2={period2}&interval=5m"
    subprocess.run(["curl", "-s", "-H", "User-Agent: Mozilla/5.0", "-o", outfile, url])
    with open(outfile) as f:
        data = json.load(f)
    # parse timestamps + closes, convert to ET
    time.sleep(0.3)
```

## Step 3: Compute 5-Minute Post-Pick Average

**Morning session** (pick time ~09:55 AM ET): average close prices at 09:50, 09:55, 10:00 ET.
**Afternoon session** (pick time ~02:15 PM ET): average close prices at 14:10, 14:15, 14:20 ET.

The closing price is the 16:00 ET candle close.

Compute: `pct_5min_to_close = (close_price - avg_5min) / avg_5min * 100`

## Step 4: Analyze by Category

Group results by:
- **Session**: Morning vs Afternoon
- **Action type**: BUY vs BUY ON DIP vs WATCH
- **RSI zone**: sweet spot (60-70) vs overbought (>72) vs weak (<60)
- **Sector**: which sectors delivered returns
- **Day type**: gap-up (>2% sector gap from prev close) vs flat open
- **Repeated picks**: stocks that appeared in both sessions

Also compute the afternoon reference (what the morning picks would have returned
if entered at 02:15 PM) for session comparison.

## Step 5: Generate Report + Send Email

1. Write report as `.txt` with clear tables and analysis
2. Convert to PDF: `enscript -B -f Courier@7.5 -p report.ps report.txt` then `gs ...`
3. Send via SMTP (resend.com) with PDF attached — see `send-email` skill
4. Save PDF to `gen_reports/Stock_Picker_Performance_YYYY-MM-DD.pdf`
5. Send email via `terminal()` running a Python script (write script first, then run it)

## Key Metrics to Report

| Metric | Description |
|--------|-------------|
| 5min→Close % per stock | Core performance metric |
| Session avg (morning/afternoon) | Compare timing windows |
| Action-type avg | BUY vs BUY ON DIP vs WATCH reliability |
| RSI zone avg | Sweet spot (60-70) vs overbought (>72) |
| Sector avg | Which sectors delivered |
| Overall avg vs VOO | Strategy vs benchmark |
| VOO 5min→Close | Benchmark return over same window |
| Intraday trajectory | Price at key times (open, 09:50, 10:00, 10:30, 12:00, 14:00, close) |
| Morning vs afternoon ref | What if morning picks were entered at 02:15 PM? |

## Optimization Signals to Watch For

- **Morning peak-timing:** if 09:50-09:55 shows local tops → Pitfall #27 (delay on gap-up days)
- **Session day-type context (Pitfall #28):** Gap-up days split into two types:
  - **"Momentum Gap-Up"** (tech/semiconductor leadership, XLK/XOVR excess >1.5%):
    morning entry is preferred — momentum sustains through close (Jun 30).
  - **"Fragile Gap-Up"** (non-tech or mixed leadership): afternoon entry is preferred
    — morning peaks fade (Jun 24/27/29).
  Always classify the gap-up type in the report. On flat-open days, morning picks
  can be acted on directly.
- **RSI sweet spot confirmation:** if RSI 60-70 stocks outperform >72 stocks
- **Momentum exception validation:** check if RSI 72-78 stocks with sector excess >2%
  actually delivered (Pitfall #24). Track MACD expansion + volume trend as confirming signals.
- **10:30 continuation check:** if a stock is LOWER at 10:30 ET than the 09:50-10:00 avg,
  it's a strong fade signal — flag for potential WATCH downgrade. **Caveat (Jun 29):**
  passing the 10:30 check does NOT guarantee holding. On gap-up days, ABNB and BAC
  were higher at 10:30 but still faded 0.7-1.7% to close. Consider a trailing
  10:30→11:30 check for gap-up days — if the stock is fading through mid-morning,
  downgrade even if the 10:30 candle passed.
- **BUY ON DIP over-conservatism:** if a stock flagged BUY ON DIP with healthy RSI never
  dips to entry zone and rallies further, note the missed opportunity
- **Sector intraday trajectory:** sector ETFs that peaked early and faded (like ITB on
  2026-06-25) may not sustain picks even if the day's excess looks strong
- **Repeated-pick degradation:** if stocks picked in both sessions fade (PHM pattern)
- **Sector concentration:** if picks are all one sector, check diversification
- **Sector quality gate (Pitfall #40):** if a sector's excess vs VOO is <0.5%,
  stocks in that sector rarely deliver positive 5min→Close. Flag thin-leadership
  sectors and expect their picks to lag.
- **Afternoon dilution (Pitfall #41):** if morning stalwarts are performing well,
  afternoon should re-evaluate them rather than replace with weaker-sector names.
  New afternoon-only picks from sub-threshold sectors are a negative signal.
- **Building-momentum penalty (Pitfall #42):** on strong trend days (VOO >+0.5%,
  top sector excess >1.5%), RSI <60 stocks lag. Reduce building-momentum weight
  in Step 3 scoring.
- **Commodity-driven excess trap (Pitfall #47 — NEW):** when uranium/mining ETFs
  (URAA, URA, URNM, NLR, NUKZ, XME) rank in the top 3 by excess, the sector
  outperformance may reflect commodity futures spikes rather than sustainable
  equity momentum. Individual stock returns may NOT follow sector-level gains.
  Flag and consider reducing excess weighting to 50% in Step 3 scoring.

## Case Studies

- `references/performance-case-study-2026-06-17.md` — Pre-market reversal, early RSI validation
- `references/performance-case-study-2026-06-22.md` — Gap-up day, BUY ON DIP validation
- `references/performance-case-study-2026-06-23.md` — Defensive rotation, Beta relaxation
- `references/performance-case-study-2026-06-24.md` — Gap-up day, afternoon outperformance
- `references/performance-case-study-2026-06-25.md` — Flat-open day, morning outperformance, momentum exception counter-example
- `references/performance-case-study-2026-06-26.md` — Defensive rotation, afternoon-only, momentum exception market-context gate
- `references/performance-case-study-2026-06-29.md` — Gap-up day, dual session, 3-session gap-up pattern confirmed, 10:30 check limitation
- `references/performance-case-study-2026-06-30.md` — Momentum Gap-Up day, dual session, gap-up type classification, sector quality gate, afternoon dilution
- `references/performance-review-case-study-2026-07-01.md` — Bearish correction, universal SMA crossover failure, uranium sector trap, WATCH accuracy, cross-session sector rotation, commodity-driven excess deception (Pitfall #47)
