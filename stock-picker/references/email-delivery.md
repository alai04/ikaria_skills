# Cron Job Email Delivery Pipeline

When running stock-picker as a scheduled cron job, the final step sends
the PDF report via email. This is separate from the `send-email` skill —
the stock-picker cron workflow embeds email delivery as its output step.

## SMTP Configuration

Uses Resend.com SMTP relay:

| Setting | Value |
|---------|-------|
| Server | `smtp.resend.com` |
| Port | `465` (SSL) |
| Username | `resend` |
| From | `noreply@alai04.net` |

## Delivery Script Template

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

msg = MIMEMultipart()
msg["From"] = "Hermes Agent <noreply@alai04.net>"
msg["To"] = "recipient@example.com"
msg["Subject"] = f"Stock Picker Report — {data_date}"

# Plain-text body with top-level summary
msg.attach(MIMEText(body_text, "plain", "utf-8"))

# Attach PDF
with open(pdf_path, "rb") as f:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(f.read())
encoders.encode_base64(part)
part.add_header("Content-Disposition", f"attachment; filename=Stock_Picker_Report_{data_date}.pdf")
msg.attach(part)

with smtplib.SMTP_SSL("smtp.resend.com", 465) as server:
    server.login("resend", SMTP_PASSWORD)
    server.send_message(msg)
```

## Recipient

Default delivery: `lai@ikariagroup.com`
Change by editing the cron job command or delivery script.

## Pitfalls

- Port 465 uses implicit SSL — always use `SMTP_SSL`, not `SMTP` + `starttls()`.
- From address must be a verified domain in Resend (`alai04.net`).
- Resend free tier limit: 100 emails/day.
- PDF must exist before sending — verify path.
