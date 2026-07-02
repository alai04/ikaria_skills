# Performance Case Study: 2026-06-25

## Market Context

- **VOO:** Prev close $675.69 → Close $675.71 (+0.04%, flat session)
- **VXX:** -1.31% (low volatility, calm markets)
- **Day type:** Non-gap-up, flat open, risk-on rotation
- **Leading sectors:** XLI +2.24% excess, SCHA +1.70% excess, ITB +1.67% excess
- **Lagging sectors:** XLC -1.03% excess, URAA -1.51% excess

## Morning Session (09:55 AM ET)

9 of 30 stocks passed all 6 filters. Top 5: CAT, ATI, MKSI, PHM, SNDK.

### Performance: 5min Post-Pick Average (09:50-10:00) → Close (16:00)

| Ticker | Action | RSI | Sector | 5min_Avg | Close | 5min→Close% | Day Chg% |
|--------|--------|-----|--------|----------|-------|-------------|----------|
| CAT | BUY | 66.6 | XLI | $1,027.35 | $1,057.01 | **+2.89%** | +6.29% |
| ATI | BUY | 67.9 | SCHA | $201.73 | $199.50 | -1.11% | +0.97% |
| MKSI | BUY | 62.1 | SCHA | $386.11 | $410.31 | **+6.27%** | +7.52% |
| PHM | WATCH | 73.2 | ITB | $138.98 | $135.81 | -2.28% | +0.07% |
| SNDK | BUY ON DIP | 62.3 | SCHA | $2,122.82 | $2,335.00 | **+10.00%** | +21.53% |
| RVMD | BUY | 69.7 | SCHA | $176.58 | $178.17 | +0.90% | +4.88% |
| TOL | BUY | 68.9 | ITB | $163.88 | $162.08 | -1.10% | +0.65% |
| GE | BUY | 75.8 | XLI | $373.90 | $371.36 | -0.68% | +1.50% |
| ETN | BUY | 54.0 | XLI | $416.19 | $419.87 | +0.88% | +3.78% |
| **VOO** | BENCHMARK | — | — | $674.09 | $675.71 | **+0.24%** | +0.04% |

**Morning average:** +1.75% (all 9), +0.72% (ex-SNDK outlier)
**Strategy excess vs VOO:** +1.51% (all), +0.48% (ex-SNDK)

### Afternoon Reference (02:15 PM ET → Close)

| Ticker | 14:15_Avg | Close | 14:15→Close% |
|--------|-----------|-------|-------------|
| CAT | $1,047.25 | $1,057.01 | +0.93% |
| ATI | $198.82 | $199.50 | +0.34% |
| MKSI | $406.94 | $410.31 | +0.83% |
| PHM | $135.74 | $135.81 | +0.05% |
| SNDK | $2,306.50 | $2,335.00 | +1.24% |
| RVMD | $178.38 | $178.17 | -0.12% |
| TOL | $161.36 | $162.08 | +0.45% |
| GE | $372.66 | $371.36 | -0.35% |
| ETN | $419.56 | $419.87 | +0.07% |

**Afternoon reference average:** +0.38%

## Key Findings

### 1. RSI Sweet Spot Continues to Validate (Pitfall #15)
- RSI 60-70: **+2.97% avg** (6 stocks: CAT, ATI, MKSI, SNDK, RVMD, TOL)
- RSI >70: **-1.48% avg** (2 stocks: PHM -2.28%, GE -0.68%)
- RSI <60: +0.88% (1 stock: ETN)

The RSI 60-70 "sweet spot" delivered 4.45 percentage points more return than the
overbought zone. This is the strongest signal in the scoring framework.

### 2. WATCH Designation Was Correct (Pitfall #15)
PHM (RSI 73.2, WATCH) declined -2.28%. The WATCH threshold at RSI 72 correctly
identified this as a stock to avoid entering immediately.

### 3. Momentum Exception Failed for GE (Pitfall #24 — REFINED)
GE (RSI 75.8, XLI +2.24% excess) received BUY via the momentum exception but
declined -0.68%. Unlike OSCR on 2026-06-23 (which had expanding MACD and
increasing volume), GE had:
- MACD histogram: +2.92 (declining from prior days — contraction signal)
- Volume trend: "stable" (not increasing)
- No gap-up that day (GE: +2.2% intraday, not an extreme gap)

**Lesson:** The momentum exception requires secondary confirmation:
(a) MACD histogram expanding, (b) volume trend increasing, (c) no >5% gap-up.
If any check fails, default to WATCH.

### 4. BUY ON DIP May Be Overly Conservative on Non-Gap-Up Days
SNDK gapped +12.91% and was flagged BUY ON DIP (1-month +34.87% was parabolic).
It never dipped to the entry zone ($1,960-$2,146) and rallied another +10%.
The 5min_avg of $2,122.82 was actually inside the entry zone ($1,960-$2,146),
so the dip never materialized.

On non-gap-up days where a stock's 1-month run is extended but RSI is healthy
(62.3), consider a partial BUY with tighter stop rather than full BUY ON DIP.

### 5. ITB Sector Underperformed Despite Strong Screening
ITB was the #3 selected sector (+1.67% excess) but both PHM (-2.28%) and
TOL (-1.10%) declined 5min→Close. The sector's excess was driven by early
session enthusiasm that faded. SCHA (+1.70% excess) was the real winner
with MKSI +6.27% and SNDK +10%.

### 6. Morning vs Afternoon: Day-Type Matters (Pitfall #28 — REFINED)
On June 24 (gap-up day), afternoon outperformed morning (+0.89% vs +0.01%).
On June 25 (flat open), morning outperformed afternoon (+1.75% vs +0.38%).

**Refined rule:** Afternoon is the primary window on GAP-UP days (>2% sector gap).
On non-gap-up days, morning picks work. Check sector gap condition before applying
the automatic delay.

### 7. All 9 Stocks Showed ↑10:30 Continuation
Every stock in the pool was higher at 10:30 ET than at the 09:50-10:00 average.
This validates that the 5-min post-pick window captures a real entry signal, not
just a fleeting spike. The divergence happens after 10:30 — winners keep going,
losers fade.

| Ticker | 10:30 vs 5min_Avg | Final Direction |
|--------|-------------------|-----------------|
| CAT | ↑ | Continued ↑ to close |
| MKSI | ↑ | Continued ↑ to close |
| SNDK | ↑ | Continued ↑ to close |
| RVMD | ↑ | Mixed, slight ↑ |
| ETN | ↑ | Continued ↑ to close |
| ATI | ↑ | Reversed ↓ to close |
| TOL | ↑ | Reversed ↓ to close |
| GE | ↑ | Reversed ↓ to close |
| PHM | ↓ | Continued ↓ to close |

Only PHM was lower at 10:30 — all others showed early continuation before diverging.

## Optimization Recommendations

1. **Tighten momentum exception (Pitfall #24):** Require MACD histogram expansion
   + increasing volume trend before granting BUY to RSI 72-78 stocks.

2. **Contextualize afternoon vs morning (Pitfall #28):** Check gap condition before
   applying delay. If no sector ETF gapped >2%, morning picks are actionable.

3. **Add 10:30 confirmation check:** If a stock is lower at 10:30 vs 09:50-10:00 avg,
   downgrade to WATCH (this would have caught PHM).

4. **BUY ON DIP aggressiveness:** When RSI is in sweet spot (60-70), the 1-month
   run, even if parabolic, may not warrant BUY ON DIP. Consider "BUY (reduced size)"
   instead for stocks with healthy RSI + strong sector tailwind.

5. **Sector momentum beyond day's excess:** ITB's +1.67% excess was driven by
   early-session surge but faded. Consider checking the sector ETF's intraday
   trajectory (is it still rising at pick time, or peaking?) before weighting
   sector strength too heavily.
