# PDF Generation for Stock Picker Reports

## Primary Pipeline: enscript + ghostscript

This is the most reliable method when Python PDF libraries are unavailable.

### Prerequisites

```bash
# Check availability
which enscript  # Typically pre-installed on Amazon Linux
which gs         # Part of ghostscript package
```

### Generate PDF from plain text

```bash
cd /path/to/workspace/gen_reports

# Step 1: Text to PostScript
enscript -B -f Courier@7.5 -p report.ps Stock_Picker_Report_YYYY-MM-DD.txt

# Step 2: PostScript to PDF
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
   -sOutputFile=Stock_Picker_Report_YYYY-MM-DD.pdf report.ps

# Step 3: Clean up
rm report.ps
```

### enscript flags

| Flag | Meaning |
|------|---------|
| `-B` | No page header (cleaner output) |
| `-f Courier@7.5` | Monospace font at 7.5pt (fits ~100 chars/line) |
| `-p report.ps` | Output PostScript file |

Font sizing:
- `Courier@7` — tight fit, ~105 chars/line on letter
- `Courier@7.5` — good balance, ~95 chars/line
- `Courier@8` — readable but may wrap wider tables

### gs flags

| Flag | Meaning |
|------|---------|
| `-dBATCH` | Exit after processing |
| `-dNOPAUSE` | Don't prompt between pages |
| `-q` | Quiet mode |
| `-sDEVICE=pdfwrite` | PDF output |
| `-sOutputFile=...` | Output filename |

## Fallback: Python-only approaches (tested, not working in hermes-agent venv)

| Library | Status |
|---------|--------|
| `fpdf2` | Install fails — no pip in venv, `--system` permission denied |
| `reportlab` | Not pre-installed |
| `weasyprint` | Not pre-installed |
| `yfinance` | Install fails — no pip module |
| `enscript + gs` | ✅ Works reliably |

## Report Formatting Notes

- Use monospace formatting (the PDF is plain text, no rich formatting)
- Keep lines under 95 characters to avoid wrapping with Courier@7.5
- Use `=` for section separators, `-` for sub-separators
- Include the date in the filename: `Stock_Picker_Report_YYYY-MM-DD.pdf`

## Verification

```bash
file Stock_Picker_Report_YYYY-MM-DD.pdf
# Expected: "PDF document, version 1.7, N page(s)"

ls -la Stock_Picker_Report_YYYY-MM-DD.pdf
# Expected: ~12-15KB for a typical 2-page report
```
