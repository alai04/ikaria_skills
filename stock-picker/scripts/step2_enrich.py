#!/usr/bin/env python3
"""
Step 2: Fetch holdings from MarketXLS, enrich with Yahoo Finance 1-day prices,
score and rank. Reads /tmp/step1_results.json for sector ranking context.
Writes /tmp/step2_results.json and /tmp/step2_pool.json.

Usage: python3 scripts/step2_enrich.py <ETF1> <ETF2> [ETF3...]
  e.g.: python3 scripts/step2_enrich.py XLK XOVR XLI

Fetches holdings for each ETF via MarketXLS, then fetches 1-day prices
concurrently for all unique tickers, enriches with day_change_pct/volume/market_cap,
scores (volume 40% + momentum 40% + mkt_cap 20%), selects top 10 per ETF,
deduplicates, and saves results.
"""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

MARKETXLS_URL = "https://marketxls.com/etfs/{}/top10holdings"
MAX_PER_ETF = {"SCHA": 20}

def fetch_marketxls(ticker):
    """Fetch holdings via MarketXLS. Returns (ticker, [holdings_dicts])."""
    url = MARKETXLS_URL.format(ticker)
    try:
        r = subprocess.run(
            ["curl", "-s", "-L", "-H", "User-Agent: Mozilla/5.0", url],
            capture_output=True, text=True, timeout=30
        )
        html = r.stdout
        m = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
        if not m:
            print(f"  {ticker}: __NEXT_DATA__ not found ({len(html)} bytes)", file=sys.stderr)
            return ticker, []

        data = json.loads(m.group(1))
        holdings = data.get('props', {}).get('pageProps', {}).get('etfData', {}).get('holdings', [])

        valid = []
        for h in holdings:
            t = h.get('ticker', '').strip()
            if not t or t in ('N/A', '—', '-') or '-' in t or t.endswith('.HK'):
                continue
            name = h.get('name', t).strip()
            if name in ('usdx', 'USD', 'CASH', 'Cash', 'NMF', '—') or 'FUTURE' in name.upper() or 'CASH' in name.upper():
                continue
            wt = float(h.get('weight', 0))
            if wt <= 0:
                continue
            valid.append({'ticker': t, 'name': name if name != t else t, 'weight_pct': wt})

        cap = MAX_PER_ETF.get(ticker, 50)
        if len(valid) > cap:
            print(f"  {ticker}: Capping {len(valid)} to top {cap} by weight", file=sys.stderr)
            valid.sort(key=lambda x: x['weight_pct'], reverse=True)
            valid = valid[:cap]

        print(f"  {ticker}: {len(valid)} valid holdings from MarketXLS", file=sys.stderr)
        return ticker, valid
    except Exception as e:
        print(f"  {ticker}: MarketXLS error: {e}", file=sys.stderr)
        return ticker, []

def fetch_price(ticker):
    """Fetch 1-day price from Yahoo Finance. Returns (ticker, price_dict)."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=1d&interval=5m"
    try:
        r = subprocess.run(
            ["curl", "-s", "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", url],
            capture_output=True, text=True, timeout=15
        )
        d = json.loads(r.stdout)
        result = d.get('chart', {}).get('result', [])
        if not result:
            return ticker, {'error': 'no result'}
        meta = result[0]['meta']
        prev = meta.get('chartPreviousClose', 0)
        cur = meta.get('regularMarketPrice', 0)
        vol = meta.get('regularMarketVolume', 0)
        shares = meta.get('sharesOutstanding', 0)

        if prev and prev != 0:
            chg = round((cur - prev) / prev * 100, 2)
        else:
            chg = 0

        mkt_cap = shares * cur if shares and cur else 0

        return ticker, {
            'prev_close': prev, 'current': cur, 'day_change_pct': chg,
            'volume': vol, 'market_cap': mkt_cap, 'error': None
        }
    except Exception as e:
        return ticker, {'error': str(e)}

# --- Main ---
if len(sys.argv) < 2:
    print("Usage: python3 step2_enrich.py <ETF1> [ETF2 ETF3...]", file=sys.stderr)
    sys.exit(1)

SELECTED_ETFS = sys.argv[1:]
print(f"Processing ETFs: {SELECTED_ETFS}", file=sys.stderr)

# Step 2a: Fetch holdings
print("=== Step 2a: Fetching holdings from MarketXLS ===", file=sys.stderr)
all_holdings = {}
with ThreadPoolExecutor(max_workers=3) as ex:
    futures = {ex.submit(fetch_marketxls, t): t for t in SELECTED_ETFS}
    for f in as_completed(futures):
        ticker, data = f.result()
        all_holdings[ticker] = data

# Step 2b: Fetch prices for all unique tickers
all_tickers = set()
for etf, holdings in all_holdings.items():
    for h in holdings:
        all_tickers.add(h['ticker'])

print(f"\n=== Step 2b: Fetching prices for {len(all_tickers)} unique tickers ===", file=sys.stderr)
price_data = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    futures = {ex.submit(fetch_price, t): t for t in all_tickers}
    for f in as_completed(futures):
        ticker, data = f.result()
        price_data[ticker] = data

valid_count = sum(1 for d in price_data.values() if not d.get('error'))
print(f"  Valid prices: {valid_count}/{len(all_tickers)}", file=sys.stderr)

# Step 2c: Enrich + score + rank
print("\n=== Step 2c: Scoring and ranking ===", file=sys.stderr)
results = {}
all_enriched = []

for etf, holdings in all_holdings.items():
    enriched = []
    for h in holdings:
        t = h['ticker']
        pd = price_data.get(t, {})
        if pd.get('error'):
            continue
        h['day_change_pct'] = pd.get('day_change_pct', 0)
        h['volume'] = pd.get('volume', 0)
        h['market_cap'] = pd.get('market_cap', 0)
        h['current'] = pd.get('current', 0)
        enriched.append(h)
        all_enriched.append(h)

    if not enriched:
        print(f"  {etf}: 0 valid enriched holdings", file=sys.stderr)
        results[etf] = {"top10": [], "all_holdings": []}
        continue

    vols = [h['volume'] for h in enriched]
    chgs = [h['day_change_pct'] for h in enriched]
    caps = [h['market_cap'] for h in enriched]

    if max(vols) == 0 and max(chgs) == 0:
        for h in enriched:
            h['composite_score'] = 0
    else:
        sorted_vols = sorted(vols)
        sorted_chgs = sorted(chgs)
        sorted_caps = sorted(caps)
        n = len(enriched)

        for h in enriched:
            v_score = sorted_vols.index(h['volume']) / (n - 1) * 100 if n > 1 and max(vols) != min(vols) else 50
            m_score = sorted_chgs.index(h['day_change_pct']) / (n - 1) * 100 if n > 1 and max(chgs) != min(chgs) else 50
            c_score = sorted_caps.index(h['market_cap']) / (n - 1) * 100 if n > 1 and max(caps) != min(caps) else 50
            h['composite_score'] = round(v_score * 0.4 + m_score * 0.4 + c_score * 0.2, 2)

    enriched.sort(key=lambda x: x['composite_score'], reverse=True)
    top10 = enriched[:10]
    results[etf] = {"top10": top10, "all_holdings": enriched}
    print(f"  {etf}: {len(enriched)} enriched, top10 selected", file=sys.stderr)
    for i, h in enumerate(top10):
        print(f"    {i+1}. {h['ticker']:6s} {h['name'][:25]:25s} wt:{h['weight_pct']:.1f}% chg:{h['day_change_pct']:+.2f}% vol:{h['volume']:,} score:{h['composite_score']:.1f}", file=sys.stderr)

# Deduplicate across ETFs
final_pool_deduped = []
seen = set()
for etf in SELECTED_ETFS:
    for h in results.get(etf, {}).get('top10', []):
        if h['ticker'] not in seen:
            seen.add(h['ticker'])
            final_pool_deduped.append(h)

print(f"\n  Final pool (deduplicated): {len(final_pool_deduped)} stocks", file=sys.stderr)

# Save results (matching gen_report.py expected format)
out = {}
for etf, data in results.items():
    out[etf] = {"top10": data["top10"]}

with open("/tmp/step2_results.json", "w") as f:
    json.dump(out, f, indent=2)

with open("/tmp/step2_pool.json", "w") as f:
    json.dump(final_pool_deduped, f, indent=2)

print(json.dumps({"etfs_processed": len(results), "pool_size": len(final_pool_deduped)}))
