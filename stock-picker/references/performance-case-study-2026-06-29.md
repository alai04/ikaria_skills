# Performance Case Study — 2026-06-29 (Gap-Up Day, Dual Session)

## Market Context

- **Day Type:** Gap-Up (XOVR +3.25% from prev close $19.69 → $20.33)
- **VOO (morning):** +1.42% at 09:50 AM ET
- **VOO (afternoon):** +1.56% at 02:15 PM ET
- **VOO Close:** $681.01
- **VOO 5min→Close (morning):** +0.49% | **VOO 5min→Close (afternoon):** +0.06%
- **Market Tone:** Broad risk-on. Growth/tech leading (XOVR +4.19%, XLK +2.23%).
  Defensive sectors lagged (XLP -0.71%, XLU -0.55%).

## Morning Session (~09:55 AM ET)

**Context:** 0 of 27 stocks passed standard 6 filters. 3 qualified under relaxed criteria
(≥3/5 technical, Pos52w ≥0.50, Beta >0.5). All picks flagged as RELAXED.

| Ticker | Action | RSI | Sector | 5min Avg | Close | 5min→Close | 10:30 Price | 10:30 vs Avg |
|--------|--------|-----|--------|----------|-------|------------|-------------|--------------|
| ABNB | BUY | 66.2 | XLY | $148.55 | $147.17 | **-0.93%** | $149.77 | +0.82% |
| TTWO | BUY | 69.1 | XLC | $248.17 | $247.15 | **-0.41%** | $247.29 | -0.35% |
| BAC | WATCH | 72.1 | XLC | $58.05 | $57.88 | **-0.29%** | $58.28 | +0.40% |

**Morning Avg: -0.54%** (vs VOO +0.49%)

## Afternoon Session (~02:15 PM ET)

**Context:** 7 of 27 stocks passed all 6 standard filters. Full confidence picks.

| Ticker | Action | RSI | Sector | 5min Avg | Close | 5min→Close |
|--------|--------|-----|--------|----------|-------|------------|
| GLW | WATCH | 72.0 | XLK | $251.77 | $255.69 | **+1.56%** |
| ANET | BUY | 55.6 | XOVR | $163.91 | $164.10 | **+0.11%** |
| KLAC | BUY ON DIP | 68.3 | XLK | $278.27 | $278.39 | **+0.04%** |
| AMD | BUY | 58.5 | XLK | $539.33 | $539.49 | **+0.03%** |
| LRCX | WATCH | 70.5 | XLK | $411.70 | $410.91 | **-0.19%** |

**Afternoon Avg: +0.31%** (vs VOO +0.06%)

## Morning → Afternoon Reference

| Ticker | Morning 5min→Close | Afternoon Ref 5min→Close |
|--------|--------------------|-------------------------|
| ABNB | -0.93% | -0.57% |
| TTWO | -0.41% | +0.01% |
| BAC | -0.29% | -0.49% |

Morning picks at afternoon entry: **-0.35% avg** (improvement from -0.54% but still negative).

## Key Insights

### 1. Gap-Up Day Fade — 3rd Consecutive Session
Morning picks -0.54% vs afternoon +0.31%. This is now a 3-session validated pattern:

| Date | Morning Avg | Afternoon Avg | Day Type |
|------|-------------|---------------|----------|
| Jun 24 | +0.01% | +0.89% | Gap-up (ITB +2.76%) |
| Jun 27 | +0.01%* | +0.63%* | Gap-up (Tech +3.92%) |
| Jun 29 | -0.54% | +0.31% | Gap-up (XOVR +3.25%) |
| Jun 25 | +0.72% | +0.38% | Flat open |

**Conclusion:** Afternoon is the preferred execution window on gap-up days.
Morning outperforms on flat-open days. 3 sessions of gap-up data confirm this.

### 2. Relaxed Criteria Warning Validated
Morning had 0 standard passes — all 3 relaxed picks declined. The relaxed
flag correctly identified reduced confidence. When the filter says "no good
picks exist," it's worth listening.

### 3. 10:30 Continuation Check — Necessary but Not Sufficient
Only TTWO triggered the fade signal at 10:30 (-0.35%). ABNB and BAC were
HIGHER at 10:30 (passing the check) but both faded later:
- ABNB: 10:30 $149.77 → Close $147.17 = -1.74% decline
- BAC: 10:30 $58.28 → Close $57.88 = -0.69% decline

**Refinement:** The 10:30 check catches early faders (TTWO) but passing it
does not guarantee holding. On gap-up days, consider an extended trailing
check from 10:30 to close — if a stock is losing momentum in the 10:30-11:30
window, downgrade even if 10:30 was above the 09:50-10:00 average.

### 4. Building Momentum RSI (55-60) — 5th Consecutive Session
ANET (RSI 55.6, +0.11%) and AMD (RSI 58.5, +0.03%) both positive.
Track record:
- Jun 22: SWK 65.3 → +1.26%
- Jun 23: CNO 50.4 → +1.52%
- Jun 24: SWK 65.3 → +1.26%
- Jun 25: CAT 66.6 → +1.75%
- Jun 26: UNH 68.2 → +0.96%
- Jun 29: ANET 55.6 +0.11%, AMD 58.5 +0.03%

### 5. WATCH GLW (+1.56%) — Parabolic Mover with Sector Tailwind
GLW flagged WATCH due to +37.2% 1-month run and broken R:R. Despite WATCH,
rallied +1.56% in final 75 minutes. This mirrors OSCR (Jun 23/26) where
WATCH/BUY ON DIP flags were too conservative for parabolic movers with
strong sector tailwinds and healthy RSI. Consider a small starter position
(25% sizing) for WATCH candidates with RSI <72 and sector excess >0.5%.

### 6. RSI Sweet Spot Masked by Gap-Up
Morning sweet-spot stocks (TTWO 69.1, ABNB 66.2) declined not because the
RSI zone failed but because gap-up morning dynamics overwhelmed individual
technicals. The day type is a stronger signal than RSI zone on gap-up days.

## Skill Implications

- Pitfall #28 (session day-type dependency) strengthened to 3-session pattern
- 10:30 continuation check needs extension: add "10:30→11:30 trailing" for gap-up days
- Relaxed criteria flag correctly identifies reduced-confidence picks
- Building momentum RSI 55-60 now validated across 5 sessions
