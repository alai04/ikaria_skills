---
name: stock-report-writer
description: >
  Multi-agent collaborative stock research report generation. Uses parallel subagents
  simulating an institutional equity research team: Market Researcher, Fundamental Analyst,
  Technical Analyst, Risk Analyst, and Chief Strategist. Produces institutional-quality
  investment research reports in structured markdown or PDF format. Supports A-shares,
  US stocks, and HK stocks. Trigger when the user asks for a comprehensive stock report,
  multi-agent analysis, collaborative equity research, or institutional-grade stock report.
  Different from stock-analyzer (single-agent deep dive) — this skill orchestrates multiple
  specialized agents working in parallel, then synthesizes their outputs into a unified report.
---

# Stock Report Writer

Multi-agent collaborative equity research system. Simulates an institutional research
team where each agent plays a specialized role, works independently, and then their
outputs are synthesized into a comprehensive investment research report.

## Architecture

```
User Request (ticker)
        │
        ▼
   ┌─────────┐
   │Chief    │  (orchestrator: distributes work, synthesizes results)
   │Strategist│
   └────┬────┘
        │ (parallel dispatch)
   ┌────┼────┬──────────┬──────────┐
   ▼    ▼    ▼          ▼          ▼
 ┌───┐┌───┐┌────┐    ┌────┐    ┌────┐
 │MR ││FA ││TA  │    │RA  │    │SA  │
 │arket││und││ech │    │isk │    │ent │
 │Rsch ││amnt││ncl │    │Anl │    │imnt│
 │er  ││als││yst │    │yst │    │    │
 └───┘└───┘└────┘    └────┘    └────┘
   │    │    │         │         │
   └────┴────┴─────────┴─────────┘
        │ (consolidation)
        ▼
   ┌─────────┐
   │Chief    │  (final synthesis → structured report)
   │Strategist│
   └─────────┘
```

## Agent Roster

| Agent | Role | Key Deliverables |
|-------|------|-----------------|
| Market Researcher (MR) | 收集市场动态、新闻、行业信息 | 新闻摘要、行业趋势、催化剂清单 |
| Fundamental Analyst (FA) | 分析财报、估值指标、财务健康 | 财务指标表、同业对比、DCF估算 |
| Technical Analyst (TA) | 分析价格形态、技术指标、量价关系 | 关键价位、均线系统、RSI/MACD分析 |
| Risk Analyst (RA) | 识别风险因素、压力测试、情景分析 | 风险清单、空头论点、压力情景 |
| Sentiment Agent (SA) | 分析市场情绪、资金流向、机构持仓 | 情绪指标、机构动向、散户情绪 |
| Chief Strategist | 统筹分发、综合研判、撰写最终报告 | 完整研报、投资建议、目标价 |

## Execution Flow

### Step 1: Chief Strategist distributes work (batch dispatch)

delegate_task supports max 3 parallel subagents per call. Dispatch in two batches:

**Batch 1 (3 agents):** Market Researcher + Fundamental Analyst + Technical Analyst
**Batch 2 (2 agents):** Risk Analyst + Sentiment Agent

Each subagent runs independently with its own terminal session and specific research instructions.

### Step 2: Parallel subagent execution

Each agent performs its specialized research using web search and produces a structured output.
All agents MUST search for real data — never fabricate numbers.

### Step 3: Chief Strategist supplements with yfinance

After collecting subagent outputs, the Chief Strategist MUST run yfinance directly to get
verified real-time data that subagents may miss or fail to retrieve:

```python
import yfinance as yf
nvda = yf.Ticker("TICKER")
info = nvda.info
hist = nvda.history(period="1y")
```

Key metrics to extract: currentPrice, marketCap, trailingPE, forwardPE, targetMeanPrice,
targetHighPrice, targetLowPrice, recommendationKey, numberOfAnalystOpinions, shortPercentOfFloat,
heldPercentInstitutional, heldPercentInsider, beta, volume, averageVolume, revenueGrowth,
earningsGrowth, profitMargins, operatingMargins, forwardEps, sharesOutstanding, shortRatio.

Use hist to calculate: SMA20, SMA50, SMA200, RSI(14), MACD, Stochastic, volume ratios.

This supplements and verifies subagent data — especially for Technical Analyst and Sentiment Agent
outputs which are prone to incomplete web search results.

### Step 4: Chief Strategist synthesizes

The Chief Strategist collects all 5 agent outputs + yfinance data, resolves conflicts between agents
(e.g., FA says "cheap" but TA says "overbought"), and writes the final report.

### Step 5: Output and PDF generation

Produce a structured markdown report. For PDF:

1. Install dependencies if needed:
   ```bash
   pip3 install markdown weasyprint --break-system-packages --quiet
   ```

2. Write a Python script (not inline heredoc — bash escaping issues):
   ```python
   import markdown
   from weasyprint import HTML
   with open("report.md") as f: md = f.read()
   html_body = markdown.markdown(md, extensions=["tables", "fenced_code"])
   # Wrap in styled HTML template with @page rules for A4
   HTML(string=full_html).write_pdf("report.pdf")
   ```

3. Clean up intermediate .html and .py files after PDF generation.

File naming: `[TICKER]_Collaborative_Report_[YYYY-MM-DD].pdf`

## Mandatory Disclaimer

Place at the top and bottom of every report:

> This is AI-generated research for informational purposes only. It is NOT financial advice.
> I am not a licensed financial advisor. This analysis may contain errors or outdated information.
> Always verify critical data independently and consult a qualified financial professional
> before making investment decisions.

## Research Quality Rules

1. **Never fabricate financial numbers.** If a search does not return a specific metric,
   say "data not available" rather than guessing.
2. **Cite sources.** For every key data point, note the source (Yahoo Finance, SEC filing, etc.)
3. **Primary sources preferred.** SEC filings > company IR > Reuters/Bloomberg > Seeking Alpha > social media.
4. **Check dates.** Financial data older than 1 quarter should be flagged as potentially stale.
5. **Search queries should be short and specific** — 2-5 words for best results.

## Output Report Structure

The final report follows the structure defined in `references/report-template.md`.
Each agent's contribution feeds into specific sections:

- Market Researcher → Section 1: Market Overview & Catalysts
- Fundamental Analyst → Section 2: Financial Analysis & Valuation
- Technical Analyst → Section 3: Technical Analysis
- Risk Analyst → Section 4: Risk Assessment
- Sentiment Agent → Section 5: Market Sentiment & Capital Flows
- Chief Strategist → Section 6: Investment Thesis & Recommendation

## Sector-Specific Overlays

After identifying the sector in Step 1, load `references/agent-roles.md` and apply
sector-specific metrics for:
- **Tech/SaaS:** ARR, NRR, CAC/LTV, Rule of 40
- **Biotech:** Pipeline stages, FDA calendar, cash runway
- **Financials:** NIM, CET1 ratio, loan loss provisions
- **Manufacturing:** Capacity utilization, order backlog, margins
- **Consumer/retail:** Same-store sales, inventory turnover, unit economics

## Market Coverage

- **A-shares (沪深):** Use akshare, eastmoney, xueqiu for data sources
- **US stocks (美股):** Use Yahoo Finance, SEC EDGAR, Finviz
- **HK stocks (港股):** Use AAStocks, HKEX, eastmoney
- **Crypto:** NOT supported — use other tools for crypto analysis

## Pitfalls

1. **Subagents may return conflicting data.** The Chief Strategist must explicitly flag
   and resolve conflicts, not silently ignore them.
2. **Technical Analyst subagent may fail to execute Python code.** Subagents sometimes write\n   Python code but don't successfully execute it. The Chief Strategist MUST run yfinance\n   directly (Step 3) to get reliable technical data — do not rely solely on the TA subagent output.\n\n   **Critical: subagent web search prices can be stale by months.** In a SPY report, subagents\n   returned ~$582 while yfinance showed $711.90 (22% gap). VIX was also off (14.8 vs 19.0).\n   Web search returns cached/indexed data — it is NOT real-time. ALWAYS treat subagent price\n   numbers, VIX levels, and technical indicator values as potentially stale. yfinance is the\n   ground truth for all quantitative market data. Explicitly flag and override stale subagent\n   numbers in the conflict resolution section.
3. **Sentiment Agent may return incomplete results.** The SA subagent often completes quickly
   without sufficient searches. Supplement with yfinance institutional ownership, short interest,
   and analyst consensus data directly.
4. **delegate_task max 3 per call.** Dispatch in two batches: 3 + 2 agents.
5. **PDF generation requires separate script file.** Do not use inline heredoc for Python
   scripts with HTML templates — bash escaping breaks triple-quoted strings. Write to a .py file
   first, then execute.
6. **weasyprint and markdown packages not pre-installed.** Run pip3 install before PDF generation.
7. **Chinese A-shares use different terminology.** Ensure correct mapping
   (e.g., 市盈率 = P/E, 市净率 = P/B, 净资产收益率 = ROE).
8. **Market data timing.** A-shares close at 15:00 CST, US at 16:00 ET, HK at 16:00 HKT.
   Note whether data is real-time or delayed.
9. **Currency conversion.** When comparing across markets, note the exchange rate used.
10. **Avoid duplicate searches.** Each agent has a specific domain — do not have the
    Technical Analyst search for P/E ratios, etc.

## Verification

After generating the report:
1. Check that all sections are populated (no empty sections)
2. Verify that the Chief Strategist's verdict is supported by the underlying agent data
3. Ensure the disclaimer is present at top and bottom
4. Confirm source citations are included for key data points
5. Cross-check key numbers against yfinance output (price, P/E, targets, RSI, MACD)
6. File naming: `[TICKER]_Collaborative_Report_[YYYY-MM-DD].pdf` (or .md)
7. Clean up intermediate files (.html, .py) after PDF generation
