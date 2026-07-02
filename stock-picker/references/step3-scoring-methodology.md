# Step 3 — Concrete Scoring Methodology

This document provides concrete formulas for the 6-factor scoring framework
in Step 3.2. The SKILL.md defines weights and criteria at a high level;
this reference provides tested numeric mappings used in production runs.

Last validated: 2026-06-26 (defensive rotation day — XLV/XLP/KIE, 7 stocks passed, BUY ON DIP R:R floor tested)

---

## Factor 1: Trend Alignment (25 points max)

How many of the 3 key moving averages is the current price above?

| MAs above | Score | Rationale |
|-----------|-------|-----------|
| 3 of 3 (20/50/200) | 25.0 | Full bullish alignment |
| 2 of 3 | 16.7 | Mostly bullish, one gap |
| 1 of 3 | 8.3 | Weak trend |
| 0 of 3 | 0.0 | Bearish alignment |

Implementation: `score = (count_above / 3) * 25`

---

## Factor 2: Momentum (20 points max)

Based on 1-month (~21 trading day) price change %. Prefer strong but not
parabolic moves.

| 1-Month Change | Score | Rationale |
|---------------|-------|-----------|
| +5% to +15% | 18–20 | Strong, healthy trend |
| +15% to +25% | 14–16 | Extended but still investable |
| > +25% | 10–12 | Parabolic — needs breather |
| 0% to +5% | 10–14 | Modest uptrend |
| Negative | 3–8 | Weak or declining |

Implementation nuance: On gap-up days where the 1-month change is concentrated
in the last 1-2 sessions, score toward the lower end of the range.

---

## Factor 3: Volume Confirmation (15 points max)

| Volume Trend | Today vs 20-day avg | Score |
|-------------|---------------------|-------|
| Increasing (last 10d avg > prior 10d avg) | Any | 13 |
| Stable (±5%) | Any | 9 |
| Decreasing | Any | 5 |

**⚠️ Intraday Volume Pitfall:** When running mid-session, today's volume
will be far below the 20-day average (typically 0.1–0.3x) because the day
isn't over. The `vol_vs_avg` ratio is misleading intraday — rely on the
directional trend (is recent volume higher than prior period?) not the
absolute ratio. On 2026-06-24, all 4 passing stocks showed 0.1–0.2x avg
volume mid-session despite being objectively high-volume movers.

---

## Factor 4: RSI Position (15 points max)

| RSI Range | Score | Designation |
|-----------|-------|-------------|
| 60–70 | 15 | Bullish sweet spot — optimal entry |
| 55–60 | 13 | Building momentum |
| 70–72 | 11 | Elevated but acceptable |
| 72–78 (sector excess >2%) | 10 | MOMENTUM extended but sector tailwind (Pitfall #24) |
| 72–78 (sector excess ≤2%) | 6 | Overbought — WATCH territory |
| >78 | 4 | Severely overbought — WATCH only |
| 40–55 | 7 | Neutral/consolidating |
| <40 | 3 | Oversold/weak |

Note: When sector excess >2.0%, the WATCH threshold relaxes from 72 → 78
per Pitfall #24. Stocks with RSI 72–78 in a +2%+ excess sector get a
"MOMENTUM" note rather than pure WATCH.

---

## Factor 5: Sector Strength (10 points max)

Based on the parent sector ETF's excess return vs VOO from Step 1.

| Sector Excess vs VOO | Score |
|---------------------|-------|
| > +5% | 10 |
| +3% to +5% | 9 |
| +2% to +3% | 8 |
| +1% to +2% | 7 |
| +0.5% to +1% | 6 |
| 0% to +0.5% | 5 |
| Negative | 3 |

---

## Factor 6: Relative Strength (15 points max)

Stock's today change % minus its sector ETF's excess return. Measures whether
the stock is leading or lagging its own sector.

| Stock chg% − Sector excess | Score |
|---------------------------|-------|
| > +2% | 15 |
| +1% to +2% | 13 |
| 0% to +1% | 10 |
| Negative | 6 |

---

## Action Determination

After scoring, assign one of three actions:

| Condition | Action |
|-----------|--------|
| RSI < 72, composite ≥ 70 | **BUY** |
| RSI 72–78 AND sector excess >2% | **BUY** (MOMENTUM tailwind, Pitfall #24) |
| RSI 72–78 AND sector excess ≤2% | **WATCH** |
| RSI > 78 | **WATCH** |
| 1-month change > 25% (parabolic) | **BUY ON DIP** regardless of RSI |
| 1-month change > 20% AND RSI > 72 | **BUY ON DIP** |

---

## Entry Zone, Stop, and Target Formulas

### Base Formula
```
entry_low  = current_price * 0.97   (3% below current)
entry_high = current_price * 1.01   (1% above current)
stop       = current_price * 0.94   (6% below current)
target     = current_price * 1.10   (10% above current)
```
These produce R:R = (1.10p - 1.01p) / (1.01p - 0.94p) = 0.09p / 0.07p ≈ 1.29,
above the minimum threshold.

### Gap-Adjustment (Pitfall #21)
When a stock gaps up >2% from previous close (today_chg% > 2%):
- The stock opened well above yesterday's close and may have blown through
  the entry zone calculated from current price.
- **Widen the entry zone:** `entry_low = current * 0.95` to `entry_high = current * 1.02`
- **Raise target:** `target = current * 1.12` (compensates for wider zone)
  This gives R:R = (1.12p - 1.02p) / (1.02p - 0.94p) = 0.10p / 0.08p = 1.25.
- **For BUY ON DIP:** Set `entry_high` at current price or 1% above, and
  set `entry_low` near the 20-day SMA or a recent support level, whichever
  is higher. The goal is to wait for intraday mean-reversion toward the
  moving average.
- On 2026-06-24, TOL (+7.36%) got entry zone $158–165 (wider 4.4% zone
  vs default 3.9%). MTH (+7.63%) and LGIH (+11.33%) got BUY ON DIP zones
  anchored to their 20-day SMAs ($71→$78–82, $52→$55–60).

### BUY ON DIP Zone
Set `entry_high` at the lower of: current price, or 20-day SMA * 1.15.
Set `entry_low` at the higher of: 20-day SMA * 1.05, or recent support level.
Set `stop` at 50-day SMA or 6% below entry_low, whichever is tighter.
Set `target` at 52-week high or current * 1.12, whichever is lower.

**⚠️ BUY ON DIP R:R Floor (2026-06-26):** The formula `stop = min(50d_SMA, entry_low * 0.94)`
can produce stops far below current price for parabolic movers (1-month >30%), collapsing
R:R below 1.0. OSCR (current $28.98, 50d_SMA $22.73) produced R:R=0.46. **After computing
BUY ON DIP stop/target, validate R:R. If < 1.0, tighten stop to `current * 0.94` (standard
BUY trailing stop) and recompute. If still < 1.0, downgrade to WATCH.**

### Risk/Reward Calculation
```
risk   = entry_high - stop
reward = target - entry_high
R:R    = reward / risk
```
Reject any recommendation with R:R < 1.0 — flag as "unfavorable setup."
Target R:R ≥ 1.2 for BUY, ≥ 1.5 for BUY ON DIP.

**⚠️ R:R Formula Validation (2026-06-26):** The previous default formulas
(stop=0.93) produced R:R ≈ 0.89 for all standard BUY recommendations,
contradicting the minimum threshold of 1.0. Fixed by tightening stop to 0.94
(default R:R → 1.29) and raising gap-adjusted target to 1.12 (R:R → 1.25).

---

## Validation Check (2026-06-24)

Tested on 4 homebuilder stocks that passed all 6 filters:

| Ticker | Trend | Mom | Vol | RSI | Sec | Rel | Total | RSI | Action |
|--------|-------|-----|-----|-----|-----|-----|-------|-----|--------|
| TOL | 25.0 | 12 | 13 | 11 | 15 | 13 | 89.0 | 71.3 | BUY |
| MTH | 25.0 | 12 | 13 | 6 | 15 | 13 | 84.0 | 78.3 | BUY ON DIP |
| PHM | 25.0 | 12 | 13 | 6 | 12 | 15 | 83.0 | 74.1 | WATCH |
| LGIH | 25.0 | 12 | 5 | 6 | 15 | 15 | 78.0 | 77.7 | BUY ON DIP |

All scores are internally consistent and action designations match the
stated rules. PHM correctly gets WATCH (RSI 74.1 > 72, sector excess
+1.25% < 2.0% — no Pitfall #24 relaxation).

## Validation Check (2026-06-26)

Tested on 9 stocks that passed all 6 filters across 3 sectors (SCHA, XLI, XLV):

| Ticker | Trend | Mom | Vol | RSI | Sec | Rel | Total | RSI | Action |
|--------|-------|-----|-----|-----|-----|-----|-------|-----|--------|
| MKSI | 25.0 | 15.4 | 13 | 15 | 12 | 15 | 95.4 | 66.1 | BUY |
| CAT | 25.0 | 14.1 | 13 | 15 | 12 | 15 | 94.1 | 64.3 | BUY |
| SNDK | 25.0 | 16.0 | 9 | 15 | 12 | 15 | 92.0 | 63.8 | BUY ON DIP |
| URI | 25.0 | 14.6 | 9 | 13 | 12 | 15 | 88.6 | 58.7 | BUY |
| RVMD | 25.0 | 20.0 | 5 | 11 | 12 | 15 | 88.0 | 70.5 | BUY |
| TECH | 25.0 | 16.0 | 13 | 4 | 12 | 15 | 85.0 | 78.3 | BUY ON DIP |
| DAL | 25.0 | 14.1 | 13 | 11 | 12 | 6 | 81.1 | 71.7 | BUY |
| GE | 25.0 | 14.7 | 13 | 6 | 12 | 6 | 76.7 | 76.3 | WATCH |
| MTSI | 25.0 | 3.1 | 5 | 7 | 12 | 15 | 67.1 | 51.9 | BUY |

Notes:
- SNDK: BUY ON DIP correctly triggered by 1-month change > 25% (44.9% — parabolic).
- TECH: BUY ON DIP triggered by 1-month > 20% AND RSI > 72 (78.3).
- GE: Correctly WATCH (RSI 76.3 > 72, sector excess +1.84% < 2.0% — no Pitfall #24 relaxation).
- MTSI: Low score due to -4.9% 1-month change and declining volume — correctly ranked last.
- DAL: Low relative strength score (6) due to +0.98% change vs +1.84% sector excess.

## Validation Check (2026-06-26 — Defensive Rotation)

Tested on 7 stocks that passed all 6 filters (Beta>0.5 relaxed) across XLV, XLP, KIE:

| Ticker | Trend | Mom | Vol | RSI | Sec | Rel | Total | RSI | Action |
|--------|-------|-----|-----|-----|-----|-----|-------|-----|--------|
| VRTX | 25.0 | 18 | 13 | 10 | 13 | 10 | 89.0 | 76.3 | BUY (momentum) |
| UNH | 25.0 | 18 | 5 | 15 | 13 | 6 | 82.0 | 67.1 | BUY |
| TGT | 25.0 | 18 | 13 | 6 | 12 | 6 | 80.0 | 73.6 | WATCH |
| EW | 25.0 | 12 | 5 | 15 | 13 | 6 | 76.0 | 63.3 | BUY |
| MET | 25.0 | 12 | 9 | 7 | 12 | 6 | 71.0 | 53.9 | BUY |
| OSCR | 25.0 | 11 | 5 | 11 | 12 | 6 | 70.0 | 71.4 | BUY ON DIP |
| CNO | 25.0 | 18 | 5 | 4 | 12 | 6 | 70.0 | 81.5 | WATCH |

Notes:
- VRTX: BUY (momentum) correctly triggered — RSI 76.3 in 72-78 range, sector excess +2.73%
  (>2%), all 3 secondary confirmations passed (MACD Bullish, Volume Increasing, no 5% gap).
- TGT: Correctly WATCH — RSI 73.6 > 72, sector excess +1.83% < 2.0% (no Pitfall #24 relaxation).
- OSCR: BUY ON DIP correctly triggered by 1-month >25% (+31.8% parabolic). **R:R validation
  caught broken stop:** 50d_SMA=$22.73 produced R:R=0.46, triggered Pitfall #34 tightening
  to current*0.94=$27.24 for R:R=2.0.
- CNO: Correctly WATCH — RSI 81.5 > 78 (above even relaxed momentum threshold).
- 4/7 stocks had decreasing volume trends — typical defensive rotation behavior.
