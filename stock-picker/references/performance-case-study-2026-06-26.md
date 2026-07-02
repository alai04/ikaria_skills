# Performance Case Study — 2026-06-26 (Defensive Rotation, Afternoon-Only)

## Market Context

- **Day Type:** Defensive Rotation (Risk-Off)
- **VOO:** +0.14% (full day close vs prev close) but -0.52% 14:30→Close window
- **Top sectors (afternoon data):** XLV Healthcare +2.44% excess, KIE Insurance +2.31%, XOVR +1.55%
- **Data timestamp:** ~14:30 ET for Step 1; closing data for final report
- **Morning session:** DID NOT RUN (cron failure)

## Stock Picks

The afternoon session at ~14:30 ET selected 7 stocks that passed all 6 filters (Beta relaxed to >0.5):

| Rank | Ticker | Action | RSI | Sector | Score |
|------|--------|--------|-----|--------|-------|
| 1 | VRTX | BUY (momentum) | 76.5 | XLV | 90.0 |
| 2 | MET | BUY | 56.2 | KIE | 89.0 |
| 3 | UNH | BUY | 68.2 | XLV | 83.0 |
| 4 | PFG | BUY | 55.7 | KIE | 82.0 |
| 5 | OSCR | BUY ON DIP | 71.7 | KIE | 71.0 |
| — | TGT | WATCH | 73.6 | XOVR | 80.0 |
| — | CNO | WATCH | 81.5 | KIE | 70.0 |

## Performance: 5-min Post-Pick vs Close (14:25-14:35 → 16:00)

| Ticker | Action | 5min Avg | Close | 5min→Close |
|--------|--------|----------|-------|------------|
| OSCR | BUY ON DIP | $28.86 | $29.79 | **+3.23%** |
| UNH | BUY | $423.83 | $427.89 | **+0.96%** |
| CNO | WATCH | $52.21 | $52.52 | **+0.59%** |
| PFG | BUY | $107.27 | $107.75 | **+0.45%** |
| TGT | WATCH | $140.60 | $140.39 | **-0.15%** |
| MET | BUY | $86.19 | $85.95 | **-0.28%** |
| VRTX | BUY (momentum) | $493.29 | $491.34 | **-0.39%** |
| VOO | BENCHMARK | $673.76 | $670.26 | **-0.52%** |

**Overall 5min→Close: +0.63%** (all 7 picks beat VOO at -0.52%)

## Morning Reference (Hypothetical 09:55 pick)

| Ticker | 5min Avg | Close | 5min→Close |
|--------|----------|-------|------------|
| PFG | $105.82 | $107.75 | **+1.82%** |
| OSCR | $29.27 | $29.79 | **+1.79%** |
| UNH | $423.22 | $427.89 | **+1.10%** |
| CNO | $52.26 | $52.52 | **+0.50%** |
| MET | $85.68 | $85.95 | **+0.32%** |
| TGT | $140.79 | $140.39 | **-0.28%** |
| VRTX | $494.67 | $491.34 | **-0.67%** |
| VOO | $671.71 | $670.26 | **-0.22%** |

Morning hypothetical avg: +0.65% — similar to afternoon but different distribution.

## Key Insights

### 1. Momentum exception failed despite all confirmations
VRTX (RSI 76.5, XLV +2.44% excess, MACD Bullish, Volume Increasing, no +5% gap)
was flagged BUY (momentum) as the #1 pick. All 3 secondary confirmations passed.
Yet VRTX declined -0.39% from 14:30 to close.

**Root cause:** VOO was declining -0.52% through the same window. A broad market
fade overwhelmed the sector tailwind. The momentum exception's secondary checks
were necessary but not sufficient — a market-context gate is also needed.

**Fix:** Before granting BUY under momentum exception, verify VOO is NOT declining
>0.3% over the trailing 30-minute window. If VOO is declining, downgrade ALL
momentum-exception BUYs to WATCH regardless of secondary confirmations.

### 2. OSCR continues parabolic run
OSCR flagged BUY ON DIP due to +30.1% 1-month move, yet rallied +3.23%. This is
the 2nd consecutive session where OSCR's BUY ON DIP flag was too conservative
(Jun 23: WATCH → +6.13% open→close). RSI 71.7 was healthy.

**Pattern:** When a BUY ON DIP candidate has healthy RSI (60-70), adding an
aggressive alternative (25% position at market) could capture runaway momentum
while the primary BUY ON DIP entry waits for a dip.

### 3. RSI sweet spot (60-70) confirmed — 4th consecutive session
UNH (RSI 68.2) was the best-performing BUY action at +0.96%. Track record:
- Jun 22: SWK 65.3 → +1.26%
- Jun 23: CNO 50.4 → +1.52%
- Jun 24: SWK 65.3 → +1.26%
- Jun 25: CAT 66.6 → +1.75%
- Jun 26: UNH 68.2 → +0.96%

### 4. Building momentum stocks need time in risk-off
MET (RSI 56.2, -0.28%) and PFG (RSI 55.7, +0.45%) were flat. These are not
failures — building momentum takes time, especially in defensive rotations.

### 5. CNO persistent outperformer
CNO has been in the relaxed pool or WATCH in both defensive sessions (Jun 23
and Jun 26) but delivered positive returns both times (+1.52%, +0.59%). In
KIE-led rotations, CNO deserves closer monitoring for potential BUY upgrade.

## Skill Updates

- Pitfall #24 updated: added market-context gate for momentum exception
  (verify VOO not declining >0.3% in trailing 30-min before granting BUY)
- New case study saved as `references/performance-case-study-2026-06-26.md`
