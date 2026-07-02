# KIE (SPDR Insurance ETF) — Ticker-to-Company-Name Mapping

MarketXLS returns only the ticker in the `name` field for KIE holdings
(e.g., `"name": "OSCR"` instead of "Oscar Health Inc"). Use this mapping
to resolve full company names when parsing KIE holdings data.

Last updated: 2026-06-23 | 48 tickers mapped

## Full Mapping

```
OSCR → Oscar Health Inc
KMPR → Kemper Corp
MET  → MetLife Inc
PFG  → Principal Financial Group
LNC  → Lincoln National Corp
PRI  → Primerica Inc
CNO  → CNO Financial Group
FNF  → Fidelity National Financial
UNM  → Unum Group
FAF  → First American Financial Corp
MCY  → Mercury General Corp
GL   → Globe Life Inc
SIGI → Selective Insurance Group
AIZ  → Assurant Inc
THG  → Hanover Insurance Group
GNW  → Genworth Financial Inc
ALL  → Allstate Corp
RNR  → RenaissanceRe Holdings Ltd
AFG  → American Financial Group
LMND → Lemonade Inc
AFL  → Aflac Inc
BHF  → Brighthouse Financial Inc
L    → Loews Corp
PRU  → Prudential Financial Inc
RGA  → Reinsurance Group of America
HIG  → Hartford Financial Services
TRV  → Travelers Companies Inc
GSHD → Goosehead Insurance Inc
WTM  → White Mountains Insurance Group
CB   → Chubb Ltd
PLMR → Palomar Holdings Inc
AXS  → AXIS Capital Holdings Ltd
CINF → Cincinnati Financial Corp
ORI  → Old Republic International
PGR  → Progressive Corp
SKWD → Skyward Specialty Insurance
ACGL → Arch Capital Group Ltd
WRB  → W.R. Berkley Corp
AJG  → Arthur J. Gallagher & Co
AON  → Aon plc
AGO  → Assured Guaranty Ltd
MMC  → Marsh & McLennan Companies
AIG  → American International Group
RYAN → Ryan Specialty Holdings
ERIE → Erie Indemnity Co
MKL  → Markel Group Inc
KNSL → Kinsale Capital Group Inc
WTW  → Willis Towers Watson
BRO  → Brown & Brown Inc
```

## Usage

```python
KIE_NAMES = {
    "OSCR": "Oscar Health Inc", "KMPR": "Kemper Corp",
    "MET": "MetLife Inc", "PFG": "Principal Financial Group",
    "LNC": "Lincoln National Corp", "PRI": "Primerica Inc",
    # ... (full mapping above)
}

for holding in kie_holdings:
    name = holding.get("name", "")
    ticker = holding.get("ticker", "")
    if not name or name == ticker:  # MarketXLS KIE quirk
        name = KIE_NAMES.get(ticker, ticker)
```

## Notes

- This mapping covers all 48 non-futures/non-cash KIE holdings as of June 2026.
- The ETF rebalances periodically — verify against marketxls.com if holdings change.
- Non-stock holdings (NMF money market, futures contracts) are excluded from this list.
- XLK and IWM holdings from MarketXLS include proper company names and do not need this mapping.
