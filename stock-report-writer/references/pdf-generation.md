# PDF Generation Script

Converts markdown report to professional PDF using weasyprint.

## Installation

```bash
pip3 install markdown weasyprint --break-system-packages --quiet
```

## Usage

Write this script to a file (NOT inline heredoc — bash escaping breaks triple-quoted strings):

```python
import markdown
from weasyprint import HTML

# Read the markdown report
with open("NVDA_Stock_Analysis_2026-04-15.md", "r") as f:
    md_content = f.read()

# Convert markdown to HTML body
html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code"])

# Create full HTML with professional A4 styling
html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4;
    margin: 2cm 2.5cm;
    @bottom-right {{ content: "Page " counter(page) " of " counter(pages); font-size: 9px; color: #666; }}
    @top-right {{ content: "NVDA Equity Research Report"; font-size: 8px; color: #999; }}
}}
body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11px;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
}}
h1 {{
    font-size: 24px;
    color: #1a1a2e;
    border-bottom: 3px solid #e94560;
    padding-bottom: 8px;
    margin-top: 0;
    page-break-before: avoid;
}}
h2 {{
    font-size: 16px;
    color: #16213e;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
    margin-top: 24px;
    page-break-after: avoid;
}}
h3 {{
    font-size: 13px;
    color: #0f3460;
    margin-top: 16px;
    page-break-after: avoid;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 10px;
}}
th {{
    background-color: #1a1a2e;
    color: white;
    padding: 6px 8px;
    text-align: left;
    font-weight: bold;
}}
td {{
    padding: 5px 8px;
    border-bottom: 1px solid #eee;
}}
tr:nth-child(even) {{ background-color: #f8f9fa; }}
blockquote {{
    border-left: 4px solid #e94560;
    margin: 12px 0;
    padding: 8px 16px;
    background-color: #fff5f5;
    font-size: 10px;
    color: #333;
}}
p {{ margin: 8px 0; }}
ul, ol {{ margin: 6px 0; padding-left: 24px; }}
li {{ margin: 3px 0; }}
strong {{ color: #1a1a2e; }}
em {{ color: #555; }}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

# Write HTML intermediate (optional, for debugging)
with open("report.html", "w") as f:
    f.write(html_template)

# Convert to PDF
HTML(string=html_template).write_pdf("report.pdf")
print("PDF generated successfully!")
```

## Critical Notes

1. **NEVER use inline heredoc** (`python3 << 'EOF'`) for this script — bash escapes `{{` `}}` and triple-quoted strings break.
2. **Always write to a .py file first**, then execute: `python3 gen_pdf.py`
3. **Clean up** after generation: `rm gen_pdf.py report.html`
4. The `@page` CSS rules handle headers, footers, and page numbers automatically.
5. File naming: `[TICKER]_Stock_Analysis_[YYYY-MM-DD].pdf`
