---
name: stock-picker
description: >
  Sector-based stock selection skill. Triggers when user mentions "选股", "推荐股票",
  "有哪些股票需要关注", "stock picking", "stock recommendations", "which stocks to watch",
  or any request to screen and recommend stocks based on sector performance and technical analysis.
  Uses a three-step funnel: sector ETF screening → ETF holdings filtering → technical analysis
  → final recommendations with trading suggestions.
---

# Stock Picker (选股)

A systematic three-step stock selection workflow that identifies the strongest sectors first,
then finds the most representative stocks within those sectors, and finally applies technical
analysis to deliver actionable trading recommendations.

## Disclaimer (MANDATORY — never skip)

Place this disclaimer **at the very top** of every response and **at the bottom** of every response:

**Top disclaimer:**
> ⚠️ **This is AI-generated research for informational purposes only. It is NOT financial advice.**
> I am not a licensed financial advisor, broker, or analyst. This analysis may contain errors,
> outdated information, or misinterpretations of financial data. Always verify critical data points
> independently and consult a qualified financial professional before making investment decisions.
> You are solely responsible for your own investment choices.

**Bottom disclaimer:**
> ⚠️ **Reminder: This analysis is AI-generated and may contain errors.** Do not make investment
> decisions based solely on this output. Verify all data independently. Past performance and
> current metrics do not guarantee future results.

---

## Step 1: Sector ETF Screening

### 1.1 ETF Universe to Check

Check ALL of the following sector ETFs for today's performance:

| Ticker | Sector |
|--------|--------|
| GLD | Gold |
| SLV | Sliver |
| XME | Metals and Mining |
| DIA | Dow Jones Industrial |
| SPY | S&P 500 |
| RSP | S&P 500 Equal Weight |
| VXX | S&P 500 VIX Short-Term Futures |
| IWM | Russell 2000 |
| SCHA | U.S. Small-Cap |
| VB | Small-Cap Index |
| EEM | MSCI Emerging Markets |
| XOVR | Private-Public Crossover |
| IYG | Financial Services |
| IAI | Broker-Dealers & Securities Exchanges |
| KBWB | Bank |
| KIE | Insurance |
| SDY | S&P Dividend |
| ITB | Home Construction |
| NLR | Uranium and Nuclear |
| URAA | Uranium |
| NUKZ | Nuclear Renaissance |
| URA | Uranium |
| XLK | Technology |
| XLE | Energy |
| XLY | Consumer Discretionary |
| XLP | Consumer Staples |
| XLV | Healthcare |
| XLF | Financials |
| XLI | Industrials |
| XLB | Materials |
| XLU | Utilities |
| XLRE | Real Estate |
| XLC | Communication Services |

Also check VOO (S&P 500 ETF) as the benchmark.

### 1.2 Data Collection

For each ETF above, search for and record:
- **Today's price change %** (intraday or close)
- **VOO's today's price change %** (benchmark)
- **Relative performance** = ETF change % minus VOO change %

**Search methods:**
- Use `web_search` for quick queries like "XLK today price change" or "sector ETF performance today"
- Use `browser_navigate` to Yahoo Finance (`https://finance.yahoo.com/`) or MarketWatch
  for a full sector performance table
- Google Finance or Yahoo Finance sector overview pages are ideal for comparing all at once

### 1.3 Selection Criteria

Rank all ETFs by their relative performance vs VOO (excess return).
Select the **top 2-3 sector ETFs** that outperformed VOO by the largest margin.

**Important:** If all sectors are underperforming VOO (rare), pick the ones with the
smallest underperformance (least negative relative return).

### 1.4 Output Format

Present a table:

| ETF | Sector | Today % | VOO % | Relative vs VOO |
|-----|--------|---------|-------|-----------------|
| XLK | Technology | +2.1% | +0.8% | +1.3% |
| XLE | Energy | +1.5% | +0.8% | +0.7% |
| ... | ... | ... | ... | ... |

**Selected sectors:** [List the top 2-3]

---

## Step 2: ETF Holdings Filtering

### 2.1 Get Top Holdings

For each selected sector ETF, retrieve its top holdings.

**Search queries:** "XLK top holdings" (replace XLK with selected ETF ticker)
**Search targets:** ETF issuer websites (State Street, Vanguard), Yahoo Finance ETF page,
ETFdb.com, Morningstar

Record for each holding:
- Ticker symbol
- Company name
- Weight in ETF (%)
- Today's price change %
- Trading volume (today)
- Market cap

### 2.2 Scoring and Ranking

Score each stock using three factors:

1. **Volume score (40% weight):** Higher volume = more liquid, more representative.
   Rank all candidates by volume, assign percentile scores.

2. **Price momentum score (40% weight):** Today's price change %.
   Stocks moving up strongly in an outperforming sector = strong momentum signal.
   Rank by today's % change, assign percentile scores.

3. **Market cap score (20% weight):** Larger cap = more stable, more institutional interest.
   Rank by market cap, assign percentile scores.

**Composite Score** = Volume_score × 0.4 + Momentum_score × 0.4 + MarketCap_score × 0.2

### 2.3 Selection

From each selected ETF, pick the **top 10 stocks** by composite score.
If ETFs overlap (e.g., same stock appears in multiple sector ETFs), deduplicate.

Final pool: up to 30 stocks (10 per sector × 2-3 sectors), typically 20-25 after deduplication.

### 2.4 Output Format

Present a summary table for each selected sector:

**Sector: [Sector Name] ([ETF])**
| # | Ticker | Company | Weight % | Today % | Volume | Mkt Cap | Score |
|---|--------|---------|----------|---------|--------|---------|-------|
| 1 | NVDA | NVIDIA | 8.2% | +3.1% | 52M | $2.1T | 0.92 |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Step 2.5: Fundamental & Trend Filter (MANDATORY)

Before proceeding to Step 3, apply ALL of the following 6 filters to every stock
in the pool from Step 2. Stocks that fail ANY filter are EXCLUDED from Step 3.

### Filter Criteria

| # | Filter | Condition | Rationale |
|---|--------|-----------|-----------|
| 1 | Market Cap | > USD 10 Billion | Ensures sufficient liquidity and institutional interest |
| 2 | 250-day SMA | Current Price > 250-day Simple Moving Average | Long-term uptrend confirmation (above 1-year average) |
| 3 | 20-day EMA | Current Price > 20-day Exponential Moving Average | Short-term momentum confirmation (EMA weights recent prices more) |
| 4 | SMA Cross | 20-day SMA > 50-day SMA | Bullish moving average crossover (short-term above medium-term) |
| 5 | Price Position | Current Price >= 75% of 52-week range | Stock is in the top quartile of its yearly range (strength signal) |
| 6 | 1-Year Beta | Beta > 0.9 | Stock moves at least as much as the market (captures upside) |

### Data Collection

For each stock in the Step 2 pool, gather:
- **Market Cap:** All stocks from major sector ETFs (SPDRs) are S&P 500 constituents,
  so ALL pass the >$10B filter. You can safely set f1=True for all without fetching.
  If you need the actual number, Yahoo Finance chart API does NOT return marketCap in meta.
  Use `sharesOutstanding * regularMarketPrice` from meta as a fallback, or calculate beta
  as a proxy for quality (high-beta stocks are typically large-cap).
- **250-day SMA:** Requires 1-year chart data (`range=1y&interval=1d`), calculate simple average of last 250 closing prices
- **20-day EMA:** Requires 1-year chart data, calculate exponential moving average (smoothing factor = 2/(20+1))
- **20-day SMA & 50-day SMA:** From chart data
- **52-week high & low:** From chart data, calculate position = (price - 52w_low) / (52w_high - 52w_low)
- **1-Year Beta:** Yahoo Finance `quoteSummary` API requires auth crumb and often fails with
  "Unauthorized" or "Too Many Requests". **WORKAROUND:** Calculate beta from 1-year daily
  returns vs the benchmark ETF (VOO/SPY). Fetch 1-year daily closes for both the stock and
  VOO using the chart API, then:
  ```python
  stock_returns = [(closes[i] - closes[i-1]) / closes[i-1] for i in range(1, len(closes))]
  voo_returns = [(voo[i] - voo[i-1]) / voo[i-1] for i in range(1, len(voo))]
  n = min(len(stock_returns), len(voo_returns))
  cov = sum((stock_returns[i]-mean_sr)*(voo_returns[i]-mean_vr) for i in range(n)) / n
  var_vr = sum((v - mean_vr)**2 for v in voo_returns[:n]) / n
  beta = cov / var_vr
  ```

**EMA calculation formula:**
```
multiplier = 2 / (period + 1)  # For 20-day EMA: multiplier = 2/21 ≈ 0.0952
EMA(today) = (price_today - EMA(yesterday)) * multiplier + EMA(yesterday)
Seed: use 20-day SMA of first 20 days as initial EMA value
```

See `references/data-collection.md` for tested API endpoints, beta calculation code, and curl requirements.

### Filter Output

Present a filter results table showing which stocks passed/failed:

| Ticker | Company | Mkt Cap | Price>250SMA | Price>20EMA | 20SMA>50SMA | Pos>=75% | Beta>0.9 | PASS? |
|--------|---------|---------|-------------|------------|------------|---------|---------|------|
| NVDA | NVIDIA | $3.0T | Y | Y | Y | Y | Y | YES |
| AAPL | Apple | $2.9T | Y | N | Y | Y | N | NO |

**After filtering:** [X] of [Y] stocks passed all 6 filters and proceed to Step 3.

**If fewer than 5 stocks pass:** Report the stocks that passed and note that
the pool is smaller than usual. If ZERO stocks pass, report this and suggest
re-running with relaxed criteria or different sector ETFs.

---

## Step 3: Technical Analysis & Final Recommendations

### 3.0 Input Pool

The input to Step 3 is the **filtered pool from Step 2.5** (stocks that passed ALL 6 filters).
This pool will typically be smaller than the Step 2 pool. If the filtered pool has fewer
than 5 stocks, analyze all of them. If it has more than 5, apply the scoring framework
below to select the top 5.

### 3.1 Data Collection for Each Stock

For every stock in the filtered pool (up to ~25-30), gather:

**Today's data:**
- Current price, today's % change, today's volume vs average volume

**1-month data:**
- 1-month price change %
- 1-month high and low
- Current price relative to 1-month range (where in the range?)

**Technical indicators:**
- 20-day SMA (Simple Moving Average)
- 50-day SMA
- 200-day SMA (if available)
- RSI (14-day) — note if overbought (>70) or oversold (<30)
- MACD trend (bullish or bearish crossover)
- Recent volume trend (increasing or decreasing)

**Search queries:** "[TICKER] stock technical analysis", "[TICKER] RSI MACD moving average"
**Search targets:** Yahoo Finance, TradingView, StockCharts, MarketWatch, Finviz

### 3.2 Scoring Framework

Score each stock (0-100) based on:

| Factor | Weight | Criteria |
|--------|--------|----------|
| Trend alignment | 25% | Price above 20/50/200 SMA = bullish. All three = max score. |
| Momentum | 20% | Strong 1-month uptrend with healthy pullbacks, not parabolic. |
| Volume confirmation | 15% | Volume increasing on up days, decreasing on down days. |
| RSI position | 10% | RSI 50-65 is ideal (bullish but not overbought). >70 = overbought penalty. |
| Sector strength | 15% | How much the parent sector ETF outperformed VOO. |
| Relative strength | 15% | Stock's performance vs its sector ETF and vs VOO. |

### 3.3 Final Selection

Rank all stocks by composite score. Select the **top 5** as final recommendations.

### 3.4 Trading Recommendations

For each of the top 5 stocks, provide:

**Format:**
```
📈 [TICKER] - [Company Name]
   Score: XX/100 | Sector: [Sector]
   Current: $XX.XX | Today: +/-X.X%
   1M Change: +/-X.X%

   Technical Summary:
   - Trend: [Bullish/Neutral/Bearish] — Price above/below key MAs
   - RSI(14): XX — [Overbought/Oversold/Neutral]
   - Volume: [Above/Below] average — [Interpretation]
   - MACD: [Bullish/Bearish] crossover

   Recommendation:
   - Action: [Buy / Watch / Buy on Dip]
   - Entry zone: $XX.XX - $XX.XX
   - Stop loss: $XX.XX (below recent support)
   - Target: $XX.XX (near resistance or measured move)
   - Risk/Reward: X:1
   - Timeframe: [Short-term (1-2 weeks) / Medium-term (1-3 months)]

   Rationale: [1-2 sentences explaining why]
```

### 3.5 Summary Table

Present a final overview:

| Rank | Ticker | Company | Sector | Score | Action | Entry | Stop | Target | R:R |
|------|--------|---------|--------|-------|--------|-------|------|--------|-----|
| 1 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

### 3.6 Market Context Note

Include a brief note on overall market conditions:
- VOO trend today and this week
- VIX level (if available) — high = caution
- Any major macro events affecting the market
- General recommendation on position sizing given market conditions

### 3.7 PDF Report Generation

After producing the analysis in chat, generate a downloadable PDF report.

**Pipeline (enscript + ghostscript):**
1. Save the report as a `.txt` file with clean monospace formatting
2. Use `enscript` to convert to PostScript: `enscript -B -f Courier@8 -p report.ps report.txt`
3. Use `gs` (ghostscript) to convert to PDF: `gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=report.pdf report.ps`
4. Clean up: `rm report.ps`

**Environment check:** `enscript` and `gs` are typically available on Amazon Linux.
If missing, install via `sudo apt install enscript ghostscript` (Debian/Ubuntu)
or `sudo yum install enscript ghostscript` (Amazon Linux/RHEL).

**Alternative (if PDF tools unavailable):** Save as `.md` or `.txt` file.

**Output location:** Save to `gen_reports/` directory in the workspace.
**Filename:** `Stock_Picker_Report_YYYY-MM-DD.pdf`

See `references/pdf-generation.md` for tested pipeline commands and enscript flags.

---

## Pitfalls

1. **Step 2.5 filter may eliminate most stocks:** The 6 filters are strict. In practice:
   - Filter 5 (Price >= 75% of 52-week range) is the most aggressive eliminator — in one run,
     16 of 30 stocks failed this filter alone. This is expected: not all outperforming stocks
     are near yearly highs. If fewer than 5 stocks pass, report what passed and note the
     limited pool. If ZERO pass, report this clearly and suggest relaxing criteria (e.g.,
     lower the price position threshold to 60%).
   - In a typical strong market day, expect 5-10 of ~30 stocks to pass all 6 filters.
2. **EMA vs SMA confusion:** The 20-day filter requires EMA (exponential), not SMA.
   EMA weights recent prices more heavily. Use the formula provided in Step 2.5.
3. **Beta availability:** Yahoo Finance quoteSummary API returns "Unauthorized: Invalid Crumb" — 
   beta cannot be fetched directly. Calculate beta from 1-year daily returns vs VOO instead:
   fetch 1-year chart data for both the stock and VOO, compute daily returns, then
   beta = cov(stock_returns, voo_returns) / var(voo_returns). See `references/data-collection.md`.
   Market cap is similarly unavailable via API; for major index ETF constituents (S&P 500),
   all pass the >$10B filter by definition.
4. **52-week range calculation:** Price position = (current_price - 52w_low) / (52w_high - 52w_low).
   Use Yahoo Finance `52WeekRange` field or calculate from 1-year chart data.
5. **Data freshness:** Market data changes rapidly. Always note the timestamp of data used.
   If searching after market close, use closing data. If intraday, note it's real-time.
6. **After-hours trading:** Be aware that after-hours moves may not reflect next day's open.
   Note if data includes after-hours or is regular session only.
7. **ETF overlap:** Large-cap tech stocks (AAPL, MSFT, NVDA) appear in multiple ETFs.
   Deduplicate before scoring to avoid overweighting the same stock.
8. **Low-volume stocks:** Exclude stocks with average daily volume < 1M shares —
   they are too illiquid for reliable technical analysis.
9. **Earnings events:** Check if any selected stock has earnings within the next 5 days.
   If so, flag this as elevated risk and adjust the recommendation accordingly.
10. **Sector concentration:** If top 5 all come from one sector, note the concentration risk
    and consider diversifying by including at least one from a different sector.
11. **Search reliability:** Financial search results may show stale data. Cross-reference
    at least 2 sources for critical numbers (price, volume, RSI).
12. **Weekend/holiday:** On non-trading days, use the most recent trading day's data
    and explicitly state which date the data is from.

---

## Verification

After completing the analysis:
1. Confirm all stocks passed ALL 6 Step 2.5 filters before entering Step 3
2. Verify 250-day SMA, 20-day EMA, and 20/50-day SMA calculations are correct
3. Confirm all recommended stocks have current data (not stale)
4. Verify entry/stop/target levels are logically consistent with technical levels
5. Check that risk/reward ratios are calculated correctly (Target - Entry) / (Entry - Stop)
6. Ensure the summary table matches the detailed recommendations
7. Confirm disclaimers are present at top and bottom
