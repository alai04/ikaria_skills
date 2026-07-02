# Performance Case Study: 2026-07-01 — Universal SMA Crossover Failure

## Market Context
- **Date:** 2026-07-01 (Tuesday)
- **VOO:** -0.41%
- **Market Tone:** Broad correction — 20SMA < 50SMA for ALL 17 screened stocks
- **VIX:** Not captured (API limitation)

## Step 1: Sector Leaders (Excess vs VOO)
| ETF | Sector | Change | Excess |
|-----|--------|--------|--------|
| URAA | Uranium | +2.79% | +3.20% |
| XLC | Communication Svcs | +1.78% | +2.19% |
| URA | Uranium | +1.60% | +2.01% |

Top non-stock exclusions: SLV (+2.26%), GLD (+2.25%).

URAA flagged as fund-of-funds — holdings were ETF wrappers (URA, URNM, NLR, FGTXX).

## Step 2 Pool: 17 Stocks
XLC (10): META, TTD, NFLX, FOXA, T, SATS, TMUS, GOOGL, OMC, WBD
URA (7): SMR, URG, UEC, CCJ, NNE, PR, LEU

## Step 2.5: Filter Results

### Standard Pool (all 6 filters): 0/17 passed
**Universal failure:** f4 (20SMA > 50SMA) — ALL 17 stocks failed.

This is the first documented session where the SMA crossover filter eliminated
EVERY stock in the pool. Even stocks with strong day performance (META +6.90%,
XLC +2.19% excess) were below their 20SMA vs 50SMA.

### Breakdown of individual filter failures:
- f2 (Price > 250SMA): Only SATS, GOOGL, WBD, CCJ, PR passed (5/17)
- f3 (Price > 20EMA): Only META, OMC, WBD passed (3/17)
- f4 (20SMA > 50SMA): 0/17
- f5 (Price ≥75% range): Only GOOGL, WBD passed (2/17)
- f6 (Beta > 0.9): META, GOOGL, SMR, URG, UEC, CCJ, NNE, LEU passed (8/17)

### Relaxed Pool (drop f4, f5≥50%, beta>0.5): 1/17 passed
- WBD: pos=84%, sma250=Y, ema20=Y, beta=0.73 → PASS

### Second Relaxation (drop f4 + f2, f5≥50%, beta>0.5): Still only 1 passed
- WBD only

## Step 3: Mixed Pool Analysis
Used the 1 relaxed-passer (WBD) + 3 near-misses from XLC/URA:

| Rank | Ticker | Score | RSI | 1M Chg | Action |
|------|--------|-------|-----|--------|--------|
| 1 | META | 72.3 | 60.4 | +1.11% | BUY |
| 2 | GOOGL | 53.0 | 49.7 | -1.27% | WATCH |
| 3 | WBD | 51.3 | 49.6 | -1.27% | WATCH |
| 4 | CCJ | 44.0 | 58.5 | -14.42% | WATCH |

META was the only BUY — RSI 60.4 sweet spot, MACD bullish expanding, +6.90% day,
+1.11% 1-month. But below 250SMA (long-term trend damage).

## Key Takeaways

1. **Universal f4 failure is a genuine market signal, not a bug.** When all 17
   stocks show 20SMA < 50SMA, it means the entire market is in a correction.
   The filter is doing its job — flagging bearish alignment.

2. **Fund-of-funds pitfall:** URAA (#1 by excess) provided 0 individual stocks.
   The ETF_TICKERS exclusion set must include all 34 screening tickers.

3. **Fallback sequence needed:** The skill now has explicit fallback steps
   (Pitfall #44) for the 0-pass scenario: relax f4 → relax f2 → mixed pool.

4. **Position sizing:** On days like this, the standard report should include
   a 25-50% position size recommendation with prominent risk warnings.

5. **Custom report generator:** The session used a custom gen_report.py because
   step3 field names didn't match the skill's gen_report.py expectations.
   Future sessions should standardize on one format.
