#!/usr/bin/env python3
"""
Fetch today's price change for all 34 sector ETFs + VOO via Yahoo Finance chart API.
Uses concurrent ThreadPoolExecutor (Pitfall #31). Saves clean JSON to /tmp/step1_results.json.
Output stdout: one-line JSON summary. stderr: per-ticker progress.
Run: python3 scripts/fetch_etf_prices.py
"""
import json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

ETFS = [
    "GLD", "SLV", "XME", "DIA", "SPY", "RSP", "VXX", "IWM", "SCHA", "VB",
    "EEM", "XOVR", "IYG", "IAI", "KBWB", "KIE", "SDY", "ITB",
    "NLR", "URAA", "NUKZ", "URA",
    "XLK", "XLE", "XLY", "XLP", "XLV", "XLF", "XLI", "XLB", "XLU", "XLRE", "XLC",
    "VOO"
]

def fetch_one(ticker):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=5m"
        r = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", url],
            capture_output=True, text=True, timeout=15
        )
        d = json.loads(r.stdout)
        meta = d["chart"]["result"][0]["meta"]
        prev_close = meta.get("chartPreviousClose", 0)
        current = meta.get("regularMarketPrice", 0)
        volume = meta.get("regularMarketVolume", 0)

        if prev_close and prev_close != 0:
            chg_pct = round((current - prev_close) / prev_close * 100, 2)
        else:
            chg_pct = 0

        return ticker, {
            "prev_close": prev_close,
            "current": current,
            "day_change_pct": chg_pct,
            "volume": volume,
            "error": None
        }
    except Exception as e:
        return ticker, {"error": str(e)}

results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = {ex.submit(fetch_one, t): t for t in ETFS}
    for f in as_completed(futures):
        ticker, data = f.result()
        results[ticker] = data
        if data.get("error"):
            print(f"  ERROR {ticker}: {data['error']}", file=sys.stderr)
        else:
            print(f"  {ticker}: ${data['current']:.2f} ({data['day_change_pct']:+.2f}%)", file=sys.stderr)

# VOO benchmark — extract from results dict AFTER all futures complete
voo_data = results.get("VOO", {})
voo_chg = voo_data.get("day_change_pct", 0) if not voo_data.get("error") else 0
print(f"\nVOO benchmark: {voo_chg:+.2f}%", file=sys.stderr)

# Rank by excess vs VOO
ranked = []
for ticker, data in results.items():
    if data.get("error") or ticker == "VOO":
        continue
    excess = data["day_change_pct"] - voo_chg
    ranked.append((ticker, data["day_change_pct"], excess))

ranked.sort(key=lambda x: x[2], reverse=True)

print("\n## TOP 5 SECTORS vs VOO", file=sys.stderr)
for ticker, chg, excess in ranked[:5]:
    print(f"  {ticker}: {chg:+.2f}% (excess: {excess:+.2f}%)", file=sys.stderr)

# Save clean JSON to file (CRITICAL for cron: avoid stdout/stderr interleave, Pitfall #26)
with open("/tmp/step1_results.json", "w") as f:
    json.dump({"voo_change": voo_chg, "etfs": results}, f, indent=2)

print(json.dumps({"voo_change": voo_chg, "etf_count": len(results)}))
