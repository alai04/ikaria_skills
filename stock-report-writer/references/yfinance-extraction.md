# yfinance Data Extraction Script

The Chief Strategist runs this after collecting subagent outputs to get verified real-time data.

## Installation

```bash
pip3 install yfinance --break-system-packages --quiet
```

## Core Extraction Script

```python
import yfinance as yf
import numpy as np

ticker = "NVDA"  # replace with target ticker
t = yf.Ticker(ticker)
info = t.info
hist = t.history(period="1y")

# Price and market data
cp = info.get("currentPrice") or info.get("regularMarketPrice") or hist["Close"].iloc[-1]
print(f"Current Price: ${cp:.2f}")
print(f"Market Cap: ${info.get('marketCap',0)/1e12:.2f}T")

# Valuation
print(f"P/E TTM: {info.get('trailingPE','N/A')}")
print(f"Forward P/E: {info.get('forwardPE','N/A')}")
print(f"Forward EPS: {info.get('forwardEps','N/A')}")
print(f"P/S (TTM): {info.get('priceToSalesTrailing12Months','N/A')}")

# 52-week range
h52 = hist["High"].max()
l52 = hist["Low"].min()
print(f"52W High: ${h52:.2f} | 52W Low: ${l52:.2f}")
print(f"Position in Range: {((cp - l52) / (h52 - l52)) * 100:.1f}%")

# Moving averages
sma50 = hist["Close"].rolling(50).mean().iloc[-1]
sma200 = hist["Close"].rolling(200).mean().iloc[-1]
print(f"SMA50: ${sma50:.2f}")
print(f"SMA200: ${sma200:.2f}")

# RSI
delta = hist["Close"].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs.iloc[-1]))
print(f"RSI(14): {rsi:.1f}")

# MACD
exp1 = hist["Close"].ewm(span=12, adjust=False).mean()
exp2 = hist["Close"].ewm(span=26, adjust=False).mean()
macd = exp1 - exp2
signal = macd.ewm(span=9, adjust=False).mean()
print(f"MACD: {macd.iloc[-1]:.2f} | Signal: {signal.iloc[-1]:.2f}")

# Volume and short interest
print(f"Beta: {info.get('beta','N/A')}")
print(f"Volume: {info.get('volume','N/A')}")
print(f"Avg Volume: {info.get('averageVolume','N/A')}")
print(f"Shares Outstanding: {info.get('sharesOutstanding',0)/1e9:.2f}B")
print(f"Short % of Float: {info.get('shortPercentOfFloat','N/A')}")
print(f"Short Ratio: {info.get('shortRatio','N/A')}")

# Analyst targets
print(f"Target Mean: ${info.get('targetMeanPrice','N/A')}")
print(f"Target High: ${info.get('targetHighPrice','N/A')}")
print(f"Target Low: ${info.get('targetLowPrice','N/A')}")
print(f"Recommendation: {info.get('recommendationKey','N/A')}")
print(f"Num Analysts: {info.get('numberOfAnalystOpinions','N/A')}")

# Growth and margins
print(f"Revenue Growth: {info.get('revenueGrowth','N/A')}")
print(f"Earnings Growth: {info.get('earningsGrowth','N/A')}")
print(f"Profit Margins: {info.get('profitMargins','N/A')}")
print(f"Operating Margins: {info.get('operatingMargins','N/A')}")
print(f"Dividend Yield: {info.get('dividendYield','N/A')}")
```

## Notes

- yfinance may return `None` for some fields (e.g., heldPercentInstitutional, impliedVolatility)
- Always have fallback: `info.get("field") or hist["Close"].iloc[-1]`
- The `info` dict is cached — calling `t.info` once is enough
- For A-shares, use ticker format: "600519.SS" (Shanghai), "000858.SZ" (Shenzhen)
- For HK stocks, use ticker format: "0700.HK"
