# Performance Case Study: 2026-06-17 Reversal Day

## Market Conditions

- **Date:** 2026-06-17 (Wednesday)
- **Snapshot time:** 09:51 AM ET (pre-market/early session)
- **VOO:** +0.16% pre-market → -1.21% close (-1.35% intraday reversal)
- **VIX:** Not checked (improvement opportunity)
- **Leading sectors pre-market:** XLK +1.36%, XLI +0.87%, XLF +0.72%
- **Leading sectors close:** All reversed: XLK -0.34%, XLI -0.14%, XLF -0.55%

## Strategy Output

7 of 30 stocks passed all 6 Step 2.5 filters. Top 5 recommended:

| Rank | Ticker | RSI | Score | Pre-Mkt | Recommendation | Close | Open→Close | Result |
|------|--------|-----|-------|---------|---------------|-------|------------|--------|
| 1 | AMAT | 77.6 | 16.6 | +8.87% | WATCH | +4.35% | -0.15% | ✅ CORRECT |
| 2 | GE | 69.6 | 16.3 | +1.26% | BUY | +1.51% | +1.40% | 👍 GOOD |
| 3 | MS | 69.3 | 16.3 | +1.89% | BUY | +1.87% | +1.28% | 👍 GOOD |
| 4 | CAT | 62.4 | 16.2 | +2.12% | BUY | +1.11% | -0.11% | ⚠️ MIXED |
| 5 | GS | 64.3 | 16.1 | +1.51% | BUY | +0.78% | +0.06% | ⚠️ MIXED |

## Key Learnings

### 1. WATCH for RSI > 75 saved the day
AMAT was the top-scored stock (16.6/100) but had RSI 77.6. The WATCH recommendation
prevented buying into a stock that opened at $592, spiked to $623, then collapsed to $593.
Without the RSI gate, the best-scored pick would have been the worst performer.

### 2. RSI 65-70 is the sweet spot
GE (RSI 69.6, +1.40% intraday) and MS (RSI 69.3, +1.28%) were the best BUY performers.
Both were in the "strong but not overbought" zone. This validates the current RSI scoring
and suggests increasing its weight.

### 3. Pre-market optimism fades on reversal days
All 5 stocks had positive pre-market changes (+1.26% to +8.87%) but 4 of 5 closed lower
than their pre-market levels. The pre-market snapshot at 9:51 AM captured peak optimism
before a broad market sell-off.

### 4. Market regime matters more than stock selection
When VOO reverses -1.35% intraday, even stocks that passed 6 rigorous filters struggle.
A market-override rule (if VOO/SPY down >1%, downgrade BUY to WATCH) would have
improved results.

### 5. Beta amplifies both directions
AMAT (beta 2.38) had the largest swing: +8.87% pre-market to +4.35% close. High-beta
stocks are double-edged — they amplify upside in rallies and downside in sell-offs.

## Optimization Actions Taken

- Added Pitfall #13: Pre-market data may capture peak optimism
- Added Pitfall #14: Market-wide reversal protection
- Added Pitfall #15: RSI sweet spot validated, consider tightening WATCH to RSI 72
- Created `references/data-collection.md` with tested API endpoints
- Created `references/pdf-generation.md` with enscript+gs pipeline
