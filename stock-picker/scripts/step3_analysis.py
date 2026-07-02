#!/usr/bin/env python3
"""
Step 3: Technical Analysis & Final Recommendations.
Reads /tmp/step2_5_results.json and /tmp/step1_results.json.
Fetches 3-month chart data, computes RSI/MACD/SMA/EMA, scores, and produces
recommendations with entry/stop/target levels.
Saves /tmp/step3_results.json in gen_report.py-compatible format.

Usage: python3 scripts/step3_analysis.py
"""
import json, subprocess, sys, math
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = ["-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"]
YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{}?range=3mo&interval=1d"

# Load input data
with open("/tmp/step2_5_results.json") as f:
    step25 = json.load(f)

with open("/tmp/step1_results.json") as f:
    step1 = json.load(f)

# Build effective pool: standard + relaxed
effective_pool = step25.get("effective_pool_data", [])
if len(effective_pool) <= 2:
    relaxed_tickers = step25.get("passing_relaxed", [])
    std_tickers = step25.get("passing_std", [])
    for r in step25.get("results", []):
        if r["ticker"] in relaxed_tickers and r["ticker"] not in std_tickers:
            if not any(e["ticker"] == r["ticker"] for e in effective_pool):
                s = {"ticker": r["ticker"], "company": r["company"],
                     "current": r["current"], "sector": r["sector"],
                     "day_change_pct": r["day_change_pct"], "is_relaxed": True}
                effective_pool.append(s)
    for e in effective_pool:
        e.setdefault("is_relaxed", False)

print(f"Step 3 pool: {len(effective_pool)} stocks", file=sys.stderr)
for e in effective_pool:
    flag = "(relaxed)" if e.get("is_relaxed") else "(std)"
    print(f"  {e['ticker']:6s} {e.get('company','')[:40]} {flag}", file=sys.stderr)

# --- Fetch 3-month chart data ---
def fetch_chart(ticker):
    url = YAHOO_CHART.format(ticker)
    try:
        r = subprocess.run(
            ["curl", "-s", "-H", HEADERS[1], url],
            capture_output=True, text=True, timeout=30
        )
        d = json.loads(r.stdout)
        chart = d["chart"]["result"][0]
        closes = chart["indicators"]["quote"][0]["close"]
        volumes = chart["indicators"]["quote"][0]["volume"]
        closes = [c for c in closes if c is not None]  # Pitfall #29
        volumes = [v for v in volumes if v is not None]
        return ticker, {"closes": closes, "volumes": volumes}
    except Exception as e:
        return ticker, {"error": str(e)}

print("Fetching 3-month charts...", file=sys.stderr)
tickers = [s["ticker"] for s in effective_pool]
charts = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    futures = [ex.submit(fetch_chart, t) for t in tickers]
    for f in as_completed(futures):
        t, data = f.result()
        charts[t] = data

# Also fetch VOO 3mo for relative context
_, voo_chart = fetch_chart("VOO")
voo_closes = voo_chart.get("closes", [])

# --- Technical Indicators ---
def compute_rsi(closes, period=14):
    if len(closes) < period + 1:
        return 50
    gains, losses = [], []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i-1]
        gains.append(delta if delta >= 0 else 0)
        losses.append(-delta if delta < 0 else 0)
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period-1) + gains[i]) / period
        avg_loss = (avg_loss * (period-1) + losses[i]) / period
    if avg_loss == 0:
        return 100
    return 100 - (100 / (1 + avg_gain / avg_loss))

def compute_macd(closes):
    """
    Return (macd_line, signal_line, histogram, trend_str).
    PITFALL: Do NOT use a loop condition that depends on list length
    when the only code that appends to the list is inside the branch
    gated by that condition (e.g., `if len(macd_vals) >= X: macd_vals.append(...)`).
    The condition starts false and stays false forever.
    Instead: warm up both EMAs in a single pass from index 26 onward,
    appending unconditionally once warmup completes.
    Fixed 2026-07-01.
    """
    if len(closes) < 26:
        return None, None, None, "N/A"
    ema12 = sum(closes[:12]) / 12
    ema26 = sum(closes[:26]) / 26
    m12, m26, m9 = 2/13, 2/27, 2/10
    macd_vals = []
    for i in range(26, len(closes)):
        ema12 = (closes[i] - ema12) * m12 + ema12
        ema26 = (closes[i] - ema26) * m26 + ema26
        macd_vals.append(ema12 - ema26)
    if len(macd_vals) < 9:
        return None, None, None, "N/A"
    signal = sum(macd_vals[:9]) / 9
    signal_vals = [signal]
    for val in macd_vals[9:]:
        signal = (val - signal) * m9 + signal
        signal_vals.append(signal)
    macd_line = macd_vals[-1]
    signal_line = signal_vals[-1]
    histogram = macd_line - signal_line
    if len(macd_vals) >= 2 and len(signal_vals) >= 2:
        prev_hist = macd_vals[-2] - signal_vals[-2]
        if histogram > 0 and prev_hist <= 0:
            trend = "Bullish crossover"
        elif histogram < 0 and prev_hist >= 0:
            trend = "Bearish crossover"
        elif histogram > prev_hist:
            trend = "Bullish (expanding)"
        elif histogram < prev_hist:
            trend = "Bearish (contracting)"
        else:
            trend = "Flat"
    else:
        trend = "Starting"
    return round(macd_line, 4), round(signal_line, 4), round(histogram, 4), trend

def compute_sma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period

def compute_ema(closes, period):
    if len(closes) < period * 2:
        return None
    multiplier = 2 / (period + 1)
    ema = sum(closes[:period]) / period
    for price in closes[period:]:
        ema = (price - ema) * multiplier + ema
    return ema

def compute_beta(stock_closes, voo_closes):
    """1-year beta from daily returns. Requires pre-fetched 1y data."""
    n = min(len(stock_closes), len(voo_closes))
    if n < 50:
        return 0
    sr = [(stock_closes[i] - stock_closes[i-1]) / stock_closes[i-1]
          for i in range(max(1, len(stock_closes) - n), len(stock_closes))]
    vr = [(voo_closes[i] - voo_closes[i-1]) / voo_closes[i-1]
          for i in range(max(1, len(voo_closes) - n), len(voo_closes))]
    n2 = min(len(sr), len(vr))
    if n2 < 20:
        return 0
    mean_sr = sum(sr[:n2]) / n2
    mean_vr = sum(vr[:n2]) / n2
    cov = sum((sr[i]-mean_sr)*(vr[i]-mean_vr) for i in range(n2)) / n2
    var_vr = sum((v-mean_vr)**2 for v in vr[:n2]) / n2
    return cov / var_vr if var_vr > 0 else 0

# --- Score each stock ---
results = []
for stock in effective_pool:
    ticker = stock["ticker"]
    company = stock.get("company", ticker)
    current = stock["current"]
    day_chg = stock["day_change_pct"]
    sector = stock["sector"]
    is_relaxed = stock.get("is_relaxed", False)

    chart = charts.get(ticker, {})
    closes = chart.get("closes", [])
    volumes = chart.get("volumes", [])

    # Technical indicators
    rsi = compute_rsi(closes, 14)
    macd_line, signal_line, hist, macd_trend = compute_macd(closes)
    sma20 = compute_sma(closes, 20)
    sma50 = compute_sma(closes, 50)
    sma200 = compute_sma(closes, 200)
    ema20 = compute_ema(closes, 20)

    # 1-month change
    if len(closes) >= 22:
        month_ago = closes[-22]
        month_chg = ((closes[-1] - month_ago) / month_ago) * 100 if month_ago > 0 else 0
    else:
        month_chg = day_chg

    # Volume trend
    if len(volumes) >= 20:
        recent_10 = sum(volumes[-10:]) / 10
        prior_10 = sum(volumes[-20:-10]) / 10
        if prior_10 > 0:
            vol_ratio = recent_10 / prior_10
            vol_trend = "increasing" if vol_ratio > 1.05 else ("decreasing" if vol_ratio < 0.95 else "stable")
        else:
            vol_trend = "stable"
    else:
        vol_trend = "unknown"

    # Sector excess
    etf_data = step1.get("etfs", {}).get(sector, {})
    sector_chg = etf_data.get("day_change_pct", 0)
    sector_excess = sector_chg - step1.get("voo_change", 0)

    # === 6-Factor Scoring (see references/step3-scoring-methodology.md) ===
    ma_above = sum([sma20 and current > sma20, sma50 and current > sma50, sma200 and current > sma200])
    trend_score = (ma_above / 3) * 25

    if month_chg > 25: mom_score = 11  # Parabolic
    elif month_chg > 15: mom_score = 15
    elif month_chg > 5: mom_score = 19
    elif month_chg > 0: mom_score = 12
    else: mom_score = 5

    vol_score = 13 if vol_trend == "increasing" else (9 if vol_trend == "stable" else 5)

    if 60 <= rsi <= 70: rsi_score = 15
    elif 55 <= rsi < 60: rsi_score = 13
    elif 70 < rsi <= 72: rsi_score = 11
    elif 72 < rsi <= 78 and sector_excess > 2.0: rsi_score = 10
    elif 72 < rsi <= 78: rsi_score = 6
    elif rsi > 78: rsi_score = 4
    elif 40 <= rsi < 55: rsi_score = 7
    else: rsi_score = 3

    if sector_excess > 5: sec_score = 15
    elif sector_excess > 3: sec_score = 14
    elif sector_excess > 2: sec_score = 13
    elif sector_excess > 1: sec_score = 12
    elif sector_excess > 0.5: sec_score = 9
    elif sector_excess > 0: sec_score = 7
    else: sec_score = 5

    rel = day_chg - sector_excess
    rel_score = 15 if rel > 2 else (13 if rel > 1 else (10 if rel > 0 else 6))

    composite = trend_score + mom_score + vol_score + rsi_score + sec_score + rel_score

    # --- Action Determination ---
    action = "BUY"
    action_note = ""
    if month_chg > 25:
        action = "BUY ON DIP"; action_note = "Parabolic 1-month run"
    elif month_chg > 20 and rsi > 72:
        action = "BUY ON DIP"; action_note = "Extended + overbought"
    elif rsi > 78:
        action = "WATCH"; action_note = "Severely overbought"
    elif 72 < rsi <= 78:
        if sector_excess > 2.0:
            macd_expanding = hist is not None and hist > 0
            vol_ok = vol_trend == "increasing"
            no_gap = day_chg < 5.0
            if macd_expanding and vol_ok and no_gap:
                action = "BUY"; action_note = "MOMENTUM — sector tailwind"
            else:
                action = "WATCH"; action_note = "Overbought (no momentum exception)"
        else:
            action = "WATCH"; action_note = "Overbought"
    elif rsi <= 72 and composite >= 70:
        action = "BUY"
    else:
        action = "WATCH"; action_note = "Below score threshold"

    # --- Entry/Stop/Target ---
    if day_chg > 2.0:
        entry_low = round(current * 0.95, 2)
        entry_high = round(current * 1.02, 2)
        target = round(current * 1.12, 2)
    else:
        entry_low = round(current * 0.97, 2)
        entry_high = round(current * 1.01, 2)
        target = round(current * 1.10, 2)

    if action == "BUY ON DIP":
        if sma20 and sma20 < current:
            entry_high = round(min(current, sma20 * 1.15), 2)
            entry_low = round(max(sma20 * 1.05, sma20), 2)
        stop = round(min(sma50, entry_low * 0.94), 2) if sma50 else round(entry_low * 0.94, 2)
        high_52w = max(closes) if closes else current * 1.12
        target = round(min(high_52w, current * 1.12), 2)
    else:
        stop = round(current * 0.94, 2)

    # Risk/Reward with Pitfall #34 validation
    risk = entry_high - stop
    reward = target - entry_high
    rr = round(reward / risk, 2) if risk > 0 else 0

    if action == "BUY ON DIP" and rr < 1.0:
        stop2 = round(current * 0.94, 2)
        risk2 = entry_high - stop2
        rr2 = round(reward / risk2, 2) if risk2 > 0 else 0
        if rr2 >= 1.0:
            stop = stop2; rr = rr2; action_note += "; stop tightened for R:R"
        else:
            action = "WATCH"; action_note = "BUY ON DIP rejected — no acceptable R:R"; rr = rr2

    if action == "BUY" and rr < 1.0:
        stop = round(current * 0.94, 2)
        risk = entry_high - stop
        rr = round(reward / risk, 2) if risk > 0 else 0
        if rr < 1.0:
            action = "WATCH"; action_note = "Unfavorable R:R"

    # RSI designation
    if rsi > 78: rsi_label = "Severely Overbought"
    elif rsi > 72: rsi_label = "Overbought"
    elif rsi > 70: rsi_label = "Elevated"
    elif rsi >= 60: rsi_label = "Bullish (sweet spot)"
    elif rsi >= 55: rsi_label = "Building momentum"
    elif rsi >= 40: rsi_label = "Neutral"
    elif rsi >= 30: rsi_label = "Weak"
    else: rsi_label = "Oversold"

    # Trend designation
    trend_labels = ["Bearish", "Neutral", "Mostly Bullish", "Bullish"]
    trend_label = trend_labels[ma_above] if ma_above < len(trend_labels) else "Bullish"

    result = {
        "ticker": ticker, "company": company, "sector": sector,
        "current": round(current, 2),
        "day_change_pct": round(day_chg, 2),
        "month_change_pct": round(month_chg, 2),
        "rsi": round(rsi, 1), "rsi_designation": rsi_label,
        "macd_trend": macd_trend, "macd_histogram": round(hist, 4) if hist else None,
        "volume_trend": vol_trend, "trend_designation": trend_label,
        "sma20": round(sma20, 2) if sma20 else None,
        "sma50": round(sma50, 2) if sma50 else None,
        "sma200": round(sma200, 2) if sma200 else None,
        "ema20": round(ema20, 2) if ema20 else None,
        "ma_above": ma_above,
        "composite_score": round(composite, 1),
        "score_breakdown": {
            "trend": round(trend_score, 1), "momentum": round(mom_score, 1),
            "volume": round(vol_score, 1), "rsi_pos": round(rsi_score, 1),
            "sector": round(sec_score, 1), "relative": round(rel_score, 1),
        },
        "action": action, "action_note": action_note,
        "entry_low": entry_low, "entry_high": entry_high,
        "stop": stop, "target": target, "risk_reward": rr,
        "sector_excess": round(sector_excess, 2), "is_relaxed": is_relaxed,
    }
    results.append(result)

# Sort by composite score
results.sort(key=lambda x: x["composite_score"], reverse=True)

# Print summary to stderr
for i, r in enumerate(results[:5], 1):
    print(f"\n#{i} {r['ticker']} - {r['company'][:45]}", file=sys.stderr)
    print(f"   Score: {r['composite_score']}/100 | Action: {r['action']} | RSI: {r['rsi']} ({r['rsi_designation']})", file=sys.stderr)
    print(f"   Entry: ${r['entry_low']}-${r['entry_high']} | Stop: ${r['stop']} | Target: ${r['target']} | R:R: {r['risk_reward']}", file=sys.stderr)

# Transform to gen_report.py-compatible format (Pitfall #38)
transformed = []
for r in results:
    sb = r.get("score_breakdown", {})
    t = {
        "ticker": r["ticker"], "company": r["company"],
        "total_score": r["composite_score"], "sector": r["sector"],
        "sector_excess": r.get("sector_excess", 0),
        "current": r["current"], "day_change_pct": r["day_change_pct"],
        "month_change": r["month_change_pct"],
        "month_low": r.get("current", 0) * 0.90,
        "month_high": r.get("current", 0) * 1.10,
        "sma20": r.get("sma20", 0), "sma50": r.get("sma50", 0), "sma250": 0,
        "rsi": r["rsi"],
        "macd": r["macd_trend"].split()[0].lower() if r.get("macd_trend") else "neutral",
        "macd_val": r.get("macd_histogram", 0) or 0,
        "vol_trend": r["volume_trend"],
        "score_trend": sb.get("trend", 0), "score_momentum": sb.get("momentum", 0),
        "score_vol": sb.get("volume", 0), "score_rsi": sb.get("rsi_pos", 0),
        "score_sector": sb.get("sector", 0), "score_rel": sb.get("relative", 0),
        "action": r["action"],
        "entry_low": r["entry_low"], "entry_high": r["entry_high"],
        "stop": r["stop"], "target": r["target"], "rr": r["risk_reward"],
    }
    transformed.append(t)

with open("/tmp/step3_results.json", "w") as f:
    json.dump(transformed, f, indent=2)

print(f"\nSaved {len(transformed)} recommendations to /tmp/step3_results.json", file=sys.stderr)
print(json.dumps({"count": len(transformed), "best": transformed[0]["total_score"] if transformed else 0}))
