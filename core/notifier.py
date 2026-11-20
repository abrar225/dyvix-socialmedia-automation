"""
Resend Email Notification Dispatcher
Sends executive approval alerts with draft summaries and direct review link.
"""
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Any

# Ensure project root is on path when run directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.config import (
    RESEND_API_KEY,
    RESEND_SENDER,
    REVIEWER_EMAIL,
    REVIEW_SERVER_PORT
)

def build_email_html(dossier: Dict[str, Any], review_url: str) -> str:
    """Generates an executive HTML email card matching luxury monochrome aesthetics."""
    topic = dossier.get("topic_title", "Daily Content Dossier")
    insight = dossier.get("core_insight", "Technical synthesis ready for senior review.")
    source = dossier.get("source_url", "")
    linkedin_preview = dossier.get("linkedin_copy", "")[:280] + "..."
    instagram_preview = dossier.get("instagram_copy", "")[:200] + "..."
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #09090b; color: #f4f4f5; margin: 0; padding: 30px; }}
        .container {{ max-width: 600px; margin: 0 auto; background: #121215; border: 1px solid #27272a; border-radius: 14px; overflow: hidden; }}
        .header {{ padding: 24px; border-bottom: 1px solid #27272a; background: #18181b; }}
        .tag {{ display: inline-block; padding: 4px 10px; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; background: #27272a; color: #38bdf8; border-radius: 6px; margin-bottom: 12px; }}
        .title {{ font-size: 20px; font-weight: 700; margin: 0 0 8px 0; color: #ffffff; line-height: 1.3; }}
        .insight {{ font-size: 14px; color: #a1a1aa; line-height: 1.5; margin: 0; }}
        .content {{ padding: 24px; }}
        .section-title {{ font-size: 12px; font-weight: 600; text-transform: uppercase; color: #71717a; margin-bottom: 8px; letter-spacing: 0.05em; }}
        .preview-box {{ background: #09090b; border: 1px solid #27272a; border-radius: 8px; padding: 14px; font-size: 13px; line-height: 1.5; color: #d4d4d8; margin-bottom: 18px; }}
        .cta-container {{ text-align: center; padding: 24px 0 10px 0; }}
        .cta-button {{ display: inline-block; background: #ffffff; color: #000000; font-weight: 600; font-size: 14px; padding: 12px 28px; border-radius: 8px; text-decoration: none; }}
        .footer {{ padding: 16px 24px; border-top: 1px solid #27272a; font-size: 11px; color: #71717a; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <div class="tag">ANTIGRAVITY // DRAFT READY FOR APPROVAL</div>
          <h1 class="title">{topic}</h1>
          <p class="insight">{insight}</p>
        </div>
        <div class="content">
          <div class="section-title">LinkedIn Preview</div>
          <div class="preview-box">{linkedin_preview}</div>

          <div class="section-title">Instagram Preview</div>
          <div class="preview-box">{instagram_preview}</div>

          <div class="cta-container">
            <a href="{review_url}" class="cta-button" target="_blank">Review & Approve in Dashboard &rarr;</a>
          </div>
        </div>
        <div class="footer">
          Source Reference: {source}<br/>
          Engineered for Antigravity Autonomous Social Media Automation.
        </div>
      </div>
    </body>
    </html>
    """
    return html

def send_resend_notification(dossier: Dict[str, Any], review_url: str = None) -> Dict[str, Any]:
    """Sends review notification email via Resend API."""
    target_url = review_url or f"http://localhost:{REVIEW_SERVER_PORT}"
    topic = dossier.get("topic_title", "Daily Content Dossier")

    if not RESEND_API_KEY:
        print("⚠️  [Resend Notice] RESEND_API_KEY is not configured in .env.")
        print(f"👉 Review Dashboard URL available locally: {target_url}")
        return {"status": "SKIPPED", "url": target_url}

    url = "https://api.resend.com/emails"
    payload = {
        "from": RESEND_SENDER,
        "to": [REVIEWER_EMAIL],
        "subject": f"[Action Required] Review Daily Social Media Draft: {topic[:50]}",
        "html": build_email_html(dossier, target_url)
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "AntigravityAutomation/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"📧 [Resend Success] Notification sent to {REVIEWER_EMAIL} (ID: {data.get('id')})")
            return {"status": "SUCCESS", "id": data.get("id"), "url": target_url}
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"⚠️  [Resend HTTP Error] ({e.code}): {err_msg}")
        return {"status": "ERROR", "error": err_msg, "url": target_url}
    except Exception as e:
        print(f"⚠️  [Resend Error] {e}")
        return {"status": "ERROR", "error": str(e), "url": target_url}

if __name__ == "__main__":
    sample_dossier = {
        "topic_title": "AI Engineering Verification & Self-Correction Loops",
        "core_insight": "Autonomous agent reliability scales with deterministic validation rather than model size.",
        "linkedin_copy": "Testing autonomous systems in 2026 demands deterministic verification gates...",
        "instagram_copy": "Autonomous agents need more than just bigger context windows.",
        "source_url": "https://example.com"
    }
    res = send_resend_notification(sample_dossier)
    print("Result:", res)
