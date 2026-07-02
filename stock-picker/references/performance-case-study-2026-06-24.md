# Performance Case Study — June 24, 2026

## Market Context

- VOO: $676.34 prev_close → $675.69 close (-0.10%)
- VXX: -1.38% (low volatility, risk-on)
- Strong sector rotation: ITB +5.64% excess vs VOO in morning, +5.99% in afternoon
- Homebuilders surging on rate-cut expectations / housing data catalyst

## Morning Session (~09:55 AM ET)

Top sectors: ITB (+5.64% excess), XLY (+1.25%), XLV (+0.89%)
4 of 27 stocks passed all 6 filters (all homebuilders).

| Ticker | Action | 09:30 | 09:50 | 09:55 | 10:00 | 5min Avg | Close | 5min→Close | Session |
|--------|--------|-------|-------|-------|-------|----------|-------|------------|---------|
| TOL | BUY | 159.21 | 162.19 | 160.85 | 160.10 | 161.05 | 161.03 | -0.01% | +4.95% |
| MTH | BUY ON DIP | 79.69 | 81.89 | 81.56 | 80.66 | 81.37 | 82.39 | +1.25% | +6.50% |
| PHM | WATCH | 133.59 | 136.62 | 136.48 | 135.60 | 136.23 | 135.71 | -0.38% | +4.64% |
| LGIH | BUY ON DIP | 60.19 | 62.19 | 62.19 | 61.43 | 61.94 | 61.44 | -0.80% | +8.13% |

**Morning Avg 5min→Close: +0.01%** (flat)
**Morning Avg Session (open→close): +6.06%**

## Afternoon Session (~02:15 PM ET)

Top sectors: ITB (+5.99% excess), XLY (+1.69%), XLI (+1.10%)
7 of 25 stocks passed all 6 filters. Industrials surged into afternoon leadership.

| Ticker | Action | 09:30 | 14:10 | 14:15 | 14:20 | 5min Avg | Close | 5min→Close | Session |
|--------|--------|-------|-------|-------|-------|----------|-------|------------|---------|
| DAL | BUY | 89.14 | 89.68 | 89.83 | 89.92 | 89.81 | 90.65 | +0.93% | +2.51% |
| SWK | BUY | 86.23 | 88.50 | 88.56 | 88.59 | 88.55 | 89.66 | +1.26% | +5.33% |
| PHM | BUY ON DIP | 133.59 | 136.01 | 136.03 | 136.10 | 136.05 | 135.71 | -0.25% | +4.64% |
| MAS | BUY | 75.73 | 77.14 | 77.21 | 77.31 | 77.22 | 78.05 | +1.07% | +5.30% |
| UAL | BUY ON DIP | 126.64 | 128.40 | 128.72 | 128.92 | 128.68 | 130.54 | +1.44% | +5.27% |

**Afternoon Avg 5min→Close: +0.89%**
**Afternoon Avg Session (open→close): +4.61%**

## Combined Performance

| Metric | Value |
|--------|-------|
| Overall 5min→Close (8 pick-events) | +0.61% |
| VOO benchmark | -0.10% |
| BUY avg (n=4) | +0.81% |
| BUY ON DIP avg (n=3) | +0.63% |
| WATCH avg (n=1) | -0.38% |

## Key Takeaway: Morning Peak Fade Pattern

All 4 morning picks peaked at 09:50-09:55 AM then faded:

```
TOL:  09:30=$159  →  09:50=$162 ↑  →  10:00=$160 ↓  →  16:00=$161
MTH:  09:30=$80   →  09:50=$82  ↑  →  10:00=$81  ↓  →  16:00=$82
PHM:  09:30=$134  →  09:50=$137 ↑  →  10:00=$136 ↓  →  16:00=$136
LGIH: 09:30=$60   →  09:55=$62  ↑  →  10:00=$61  ↓  →  14:10=$60  →  16:00=$61
```

The pattern is: open strong → peak at 09:50-09:55 → fade through 10:00 → mixed afternoon recovery.
This validates Pitfall #27 (morning execution delay) and Pitfall #28 (afternoon outperformance).

## Key Takeaway: RSI Sweet Spot Confirmed

SWK (RSI 65.3) delivered +1.26%, the best afternoon performer. This is in the optimal
RSI 60-70 "strong but not overbought" zone (Pitfall #15). Stocks with RSI >72
(MTH 78.3, LGIH 77.7, PHM 74.1) were more volatile and had wider 5min→Close variance.

## Key Takeaway: PHM Double-Pick Degradation

PHM was picked in both sessions — WATCH in morning, BUY ON DIP in afternoon.
Underperformed both times (-0.38% morning, -0.25% afternoon). Pattern: strong open,
steady degradation, never recovered. This validates the WATCH designation and suggests
a "fading leader" detection rule would be valuable.

## Key Takeaway: BUY ON DIP Zones Too Wide

LGIH's entry zone ($55-60) was well below the actual dip ($60.14). MTH's zone ($78-82)
was also below the dip ($80.66). On gap-up days, the recommended zones are too low.
Suggestion: tighten to 1-2% below recommendation price on gap-up days, or use 20-day
SMA as the zone floor.

## VOO Intraday Reference

| Time (ET) | VOO Price |
|-----------|-----------|
| 09:30 | 679.22 |
| 09:50 | 679.59 |
| 10:00 | 678.01 |
| 12:00 | 680.39 |
| 14:00 | 675.27 |
| 16:00 | 675.69 |

VOO peaked at noon and faded in the afternoon, finishing -0.10%. All 8 picked stocks
outperformed VOO on a session basis (open→close), confirming the sector-first approach.
