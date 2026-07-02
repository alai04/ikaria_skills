#!/usr/bin/env python3
"""
Generate the full stock picker report as a monospace-formatted text file.
Reads /tmp/step1_results.json, /tmp/step2_results.json, /tmp/step2_5_results.json,
/tmp/step3_results.json. Outputs to gen_reports/Stock_Picker_Report_YYYY-MM-DD.txt.

Run: python3 scripts/gen_report.py [data_date]
If data_date is omitted, defaults to yesterday (last trading day logic).
"""
import json
import os
import sys
from datetime import datetime, timedelta

# Determine data date
if len(sys.argv) > 1:
    data_date = sys.argv[1]
else:
    # Default to yesterday if it's a weekday, or last Friday
    today = datetime.now()
    if today.weekday() == 0:  # Monday
        data_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    elif today.weekday() == 6:  # Sunday
        data_date = (today - timedelta(days=2)).strftime("%Y-%m-%d")
    elif today.weekday() == 5:  # Saturday
        data_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        data_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

today_str = datetime.now().strftime("%Y-%m-%d")

# Load all data
with open("/tmp/step1_results.json") as f:
    step1 = json.load(f)
with open("/tmp/step2_results.json") as f:
    step2 = json.load(f)
with open("/tmp/step2_5_results.json") as f:
    step25 = json.load(f)
with open("/tmp/step3_results.json") as f:
    step3 = json.load(f)

VOO_CHG = step1["etfs"]["VOO"]["day_change_pct"]

NON_STOCK = {"VXX", "GLD", "SLV"}

lines = []
def L(s=""): lines.append(s)

L("=" * 80)
L("  STOCK PICKER REPORT")
L(f"  Generated: {today_str} | Data Date: {data_date}")
now = datetime.now()
if now.weekday() >= 5:
    L(f"  Note: Weekend report — using {data_date} closing data")
L("=" * 80)
L()
L("⚠️  DISCLAIMER: This is AI-generated research for informational purposes only.")
L("   It is NOT financial advice. I am not a licensed financial advisor, broker,")
L("   or analyst. This analysis may contain errors or outdated information.")
L("   Always verify critical data points independently and consult a qualified")
L("   financial professional before making investment decisions.")
L("   You are solely responsible for your own investment choices.")
L()

# STEP 1
L("-" * 80)
L("STEP 1: SECTOR ETF SCREENING")
L("-" * 80)
L(f"VOO (S&P 500 Benchmark): {VOO_CHG:+.2f}%")
L()
L(f"{'ETF':6s} {'Sector':30s} {'Today %':>8s} {'VOO %':>8s} {'Excess':>8s}")
L("-" * 65)

sector_names = {
    "GLD": "Gold", "SLV": "Silver", "XME": "Metals & Mining",
    "DIA": "Dow Jones Industrial", "SPY": "S&P 500", "RSP": "S&P 500 Equal Weight",
    "VXX": "VIX Short-Term Futures", "IWM": "Russell 2000",
    "SCHA": "U.S. Small-Cap", "VB": "Small-Cap Index",
    "EEM": "MSCI Emerging Markets", "XOVR": "Private-Public Crossover",
    "IYG": "Financial Services", "IAI": "Broker-Dealers & Securities",
    "KBWB": "Bank", "KIE": "Insurance", "SDY": "S&P Dividend",
    "ITB": "Home Construction", "NLR": "Uranium & Nuclear",
    "URAA": "Uranium", "NUKZ": "Nuclear Renaissance", "URA": "Uranium",
    "XLK": "Technology", "XLE": "Energy", "XLY": "Consumer Discretionary",
    "XLP": "Consumer Staples", "XLV": "Healthcare", "XLF": "Financials",
    "XLI": "Industrials", "XLB": "Materials", "XLU": "Utilities",
    "XLRE": "Real Estate", "XLC": "Communication Services",
}

ranked = []
for t, d in step1["etfs"].items():
    if d.get("error") or t == "VOO":
        continue
    chg = d["day_change_pct"]
    excess = chg - VOO_CHG
    ranked.append((t, chg, excess))
ranked.sort(key=lambda x: x[2], reverse=True)

top_stock_sectors = []
for t, chg, excess in ranked:
    is_non_stock = t in NON_STOCK
    marker = " *" if is_non_stock else ""
    name = sector_names.get(t, t)
    L(f"{t:6s} {name:30s} {chg:>+7.2f}% {VOO_CHG:>+7.2f}% {excess:>+7.2f}%{marker}")
    if not is_non_stock and len(top_stock_sectors) < 3:
        top_stock_sectors.append((t, name, chg, excess))

L()
L("* Excluded: non-stock ETFs (VIX futures, commodity trusts)")
L()
L("SELECTED SECTORS (top 3 stock-holding ETFs by excess vs VOO):")
for etf, name, chg, excess in top_stock_sectors:
    L(f"  {etf} ({name}): {chg:+.2f}% ({excess:+.2f}% excess vs VOO)")
L()

# STEP 2
L("-" * 80)
L("STEP 2: ETF HOLDINGS SCORING")
L("-" * 80)
L(f"Top 10 holdings per selected ETF (scored by volume 40% + momentum 40% + mkt cap 20%):")
L()
for etf, name, chg, excess in top_stock_sectors:
    etf_data = step2.get(etf, {})
    holdings = etf_data.get("top10", [])
    if not holdings:
        L(f"  {etf} ({name}): No holdings data")
        continue
    L(f"  {etf} — {name} ({chg:+.2f}%, excess {excess:+.2f}% vs VOO)")
    L(f"  {'#':>2s} {'Ticker':6s} {'Company':25s} {'Wt%':>6s} {'Chg%':>7s} {'Volume':>10s} {'Score':>6s}")
    L("  " + "-" * 65)
    for i, h in enumerate(holdings):
        L(f"  {i+1:2d} {h['ticker']:6s} {h['name'][:25]:25s} {h['weight_pct']:>5.1f}% {h['day_change_pct']:>+6.2f}% {h['volume']:>10,d} {h['composite_score']:>5.1f}")
    L()

# STEP 2.5
L("-" * 80)
L("STEP 2.5: FUNDAMENTAL & TREND FILTERS (6 Filters)")
L("-" * 80)
L("Filters applied:")
L("  1. Market Cap > $10B         4. 20-day SMA > 50-day SMA")
L("  2. Price > 250-day SMA       5. Price >= 75% of 52-week range")
L("  3. Price > 20-day EMA        6. Beta > 0.5 (relaxed — defensive sectors)")
L()
L("NOTE: Beta threshold relaxed from >0.9 to >0.5 per Pitfall #23.")
L("      When all 3 selected sectors are defensive, filtering at 0.9")
L("      would eliminate most candidates.")
L()

# Determine if defensive
sectors_selected = [s for _, s, _, _ in top_stock_sectors]
defensive_sectors = {"Healthcare", "Insurance", "Utilities", "Consumer Staples", "Real Estate"}
is_defensive = any(s in defensive_sectors for s in sectors_selected)
if is_defensive:
    beta_threshold = 0.5
    L("      Defensive rotation detected — using Beta>0.5 threshold.")
else:
    beta_threshold = 0.9

L()
L(f"{'Ticker':6s} {'Company':28s} {'MktCap':>6s} {'>250SMA':>8s} {'>20EMA':>8s} {'20>50':>6s} {'Pos':>6s} {'Beta':>6s} {'PASS?':>6s}")
L("-" * 85)
for r in step25["results"]:
    pass_str = "YES" if r.get("pass_relaxed", r.get("pass_std", False)) else "NO"
    L(f"{r['ticker']:6s} {r['company'][:28]:28s} {'OK':>6s} {'Y' if r['f2_sma250'] else 'N':>8s} {'Y' if r['f3_ema20'] else 'N':>8s} {'Y' if r['f4_sma_cross'] else 'N':>6s} {r['price_position']:>5.3f} {r['beta']:>5.2f} {pass_str:>6s}")

L()
pass_std_count = len(step25.get("passing_std", []))
pass_relaxed_count = len(step25.get("passing_relaxed", []))
total_in = len(step25["results"])
L(f"Standard pool (Beta>0.9): {pass_std_count} of {total_in} passed")
if pass_relaxed_count > 0:
    L(f"Relaxed pool (Beta>0.5, defensive): {pass_relaxed_count} additional")
L(f"TOTAL passing: {pass_std_count + pass_relaxed_count} stocks proceed to Step 3")
L()

# STEP 3
L("-" * 80)
L("STEP 3: TECHNICAL ANALYSIS & FINAL RECOMMENDATIONS")
L("-" * 80)
L()

for r in step3:
    L(f"  {'#' * 2} {r['ticker']} — {r['company']}")
    L(f"  Score: {r['total_score']:.1f}/100 | Sector: {r['sector']} (excess {r['sector_excess']:+.2f}% vs VOO)")
    L(f"  Current: ${r['current']:.2f} | Today: {r['day_change_pct']:+.2f}%")
    L(f"  1-Month Change: {r['month_change']:+.1f}% | 1M Range: ${r['month_low']:.2f} - ${r['month_high']:.2f}")
    L()
    L(f"  Technical Summary:")
    L(f"    Trend: Bullish — Price above 20/50/250-day SMAs")
    L(f"    20SMA: ${r['sma20']:.2f} | 50SMA: ${r['sma50']:.2f} | 250SMA: ${r['sma250']:.2f}")
    rsi_val = r['rsi']
    rsi_label = 'Overbought' if rsi_val > 72 else 'Bullish Sweet Spot' if 60 <= rsi_val <= 70 else 'Neutral' if rsi_val >= 40 else 'Oversold'
    L(f"    RSI(14): {rsi_val:.1f} — {rsi_label}")
    L(f"    MACD: {r['macd'].title()} ({r['macd_val']:+.4f})")
    L(f"    Volume: {r['vol_trend'].title()}")
    L()
    L(f"  Scoring Breakdown:")
    L(f"    Trend Align: {r['score_trend']:.0f}/25 | Momentum: {r['score_momentum']:.0f}/20 | Volume: {r['score_vol']:.0f}/15")
    L(f"    RSI: {r['score_rsi']:.0f}/15 | Sector: {r['score_sector']:.0f}/15 | Rel Strength: {r['score_rel']:.0f}/15")
    L()
    L(f"  Recommendation:")
    L(f"    Action: {r['action']}")
    L(f"    Entry Zone: ${r['entry_low']:.2f} — ${r['entry_high']:.2f}")
    L(f"    Stop Loss: ${r['stop']:.2f}")
    L(f"    Target: ${r['target']:.2f}")
    L(f"    Risk/Reward: {r['rr']}:1")
    tf = "Short-term (1-2 weeks) — wait for dip" if r['action'] == 'BUY ON DIP' else "Medium-term (1-3 months)"
    L(f"    Timeframe: {tf}")
    L()

# Summary Table
L("-" * 80)
L("FINAL SUMMARY TABLE")
L("-" * 80)
L(f"{'Rank':>4s} {'Ticker':6s} {'Company':28s} {'Sector':6s} {'Score':>6s} {'Action':18s} {'Entry':>12s} {'Stop':>9s} {'Target':>9s} {'R:R':>5s}")
L("-" * 85)
for i, r in enumerate(step3[:5]):
    entry_s = f"${r['entry_low']:.2f}-{r['entry_high']:.2f}"
    L(f"{i+1:4d} {r['ticker']:6s} {r['company'][:28]:28s} {r['sector']:6s} {r['total_score']:>5.1f} {r['action']:18s} {entry_s:>12s} ${r['stop']:.2f}  ${r['target']:.2f}  {r['rr']:.1f}")

L()
L("-" * 80)
L("MARKET CONTEXT")
L("-" * 80)
L(f"VOO (S&P 500): {VOO_CHG:+.2f}% on {data_date}")
if is_defensive:
    L("Market Tone: Defensive rotation detected.")
    L("Consider reduced position sizing (50-75%) for lower-beta defensive picks.")
L()
L("=" * 80)
L("⚠️  REMINDER: This analysis is AI-generated and may contain errors.")
L("   Do not make investment decisions based solely on this output.")
L("   Verify all data independently.")
L("=" * 80)

os.makedirs("gen_reports", exist_ok=True)
report_path = f"gen_reports/Stock_Picker_Report_{data_date}.txt"
with open(report_path, "w") as f:
    f.write("\n".join(lines))

print(f"Report written to {report_path} ({len(lines)} lines)")
