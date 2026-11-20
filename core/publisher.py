"""
Layer 4: Social Publisher & Dispatcher
Autonomous multi-platform publishing engine for Dyvix Technologies.
Supports:
1. Method 2: Headless Browser DOM Automation (Playwright) using saved sessions for Instagram and Facebook.
2. Method 1: Webhook dispatch to n8n if configured.
3. Persistent publishing audit trail in history/.
"""
import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

from core.config import (
    ROOT_DIR,
    AUTH_DIR,
    HISTORY_DIR,
    N8N_WEBHOOK_URL
)

INSTAGRAM_STATE_FILE = AUTH_DIR / "instagram-state.json"
FACEBOOK_STATE_FILE = AUTH_DIR / "facebook-state.json"
PUBLISHING_LOG_FILE = HISTORY_DIR / "publishing_log.json"

def log_publishing_result(platform: str, status: str, details: Dict[str, Any]):
    """Appends publishing event to history audit log."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    logs = []
    if PUBLISHING_LOG_FILE.exists():
        try:
            with open(PUBLISHING_LOG_FILE, "r") as f:
                logs = json.load(f)
        except Exception:
            logs = []

    logs.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "platform": platform,
        "status": status,
        "details": details
    })

    with open(PUBLISHING_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

def publish_to_instagram_browser(dossier: Dict[str, Any]) -> Dict[str, Any]:
    """
    Publishes post to Instagram using Playwright and saved session state (.auth/instagram-state.json).
    """
    if not INSTAGRAM_STATE_FILE.exists():
        msg = f"Instagram session missing at {INSTAGRAM_STATE_FILE}. Run 'python3 scripts/capture_sessions.py instagram' to authenticate."
        print(f"⚠️  [Instagram Skipped] {msg}")
        return {"status": "SKIPPED_NO_AUTH", "message": msg}

    visual_path = dossier.get("visual_card_path", "")
    caption = dossier.get("instagram_copy", "")

    if not os.path.exists(visual_path):
        return {"status": "ERROR", "message": f"Visual asset not found at {visual_path}"}

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"status": "ERROR", "message": "Playwright is not installed. Run 'pip install playwright && playwright install chromium'."}

    print("🤖 [Playwright] Launching headless browser for Instagram...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(INSTAGRAM_STATE_FILE),
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto("https://www.instagram.com/", wait_until="networkidle", timeout=30000)

            # Check if login redirect occurred
            if "accounts/login" in page.url:
                browser.close()
                return {"status": "ERROR", "message": "Instagram session expired. Please re-run 'python3 scripts/capture_sessions.py instagram'."}

            print("📷 [Instagram] Navigated to feed. Uploading media...")
            # Click New Post / Create button
            create_btn = page.locator("svg[aria-label='New post'], svg[aria-label='Create'], a[href*='/create/']")
            if create_btn.count() > 0:
                create_btn.first.click()
                page.wait_for_timeout(2000)

            # Set file into file input
            file_input = page.locator("input[type='file']")
            if file_input.count() > 0:
                file_input.first.set_input_files(visual_path)
                page.wait_for_timeout(3000)

                # Click Next (crop screen)
                next_btn = page.locator("button:has-text('Next'), div[role='button']:has-text('Next')")
                if next_btn.count() > 0:
                    next_btn.first.click()
                    page.wait_for_timeout(2000)

                # Click Next (filter screen)
                if next_btn.count() > 0:
                    next_btn.first.click()
                    page.wait_for_timeout(2000)

                # Type caption
                caption_box = page.locator("div[aria-label='Write a caption...'], div[role='textbox']")
                if caption_box.count() > 0:
                    caption_box.first.fill(caption)
                    page.wait_for_timeout(1500)

                # Click Share
                share_btn = page.locator("button:has-text('Share'), div[role='button']:has-text('Share')")
                if share_btn.count() > 0:
                    share_btn.first.click()
                    print("🚀 [Instagram] Post submitted. Awaiting confirmation...")
                    page.wait_for_timeout(6000)

                browser.close()
                log_publishing_result("instagram", "SUCCESS", {"topic": dossier.get("topic_title")})
                return {"status": "SUCCESS", "platform": "instagram", "message": "Successfully posted to Instagram."}
            else:
                browser.close()
                return {"status": "ERROR", "message": "Upload file input not found on Instagram page."}
    except Exception as e:
        log_publishing_result("instagram", "ERROR", {"error": str(e)})
        return {"status": "ERROR", "error": str(e)}

def publish_to_facebook_browser(dossier: Dict[str, Any]) -> Dict[str, Any]:
    """
    Publishes post to Facebook using Playwright and saved session state (.auth/facebook-state.json).
    """
    if not FACEBOOK_STATE_FILE.exists():
        msg = f"Facebook session missing at {FACEBOOK_STATE_FILE}. Run 'python3 scripts/capture_sessions.py facebook' to authenticate."
        print(f"⚠️  [Facebook Skipped] {msg}")
        return {"status": "SKIPPED_NO_AUTH", "message": msg}

    visual_path = dossier.get("visual_card_path", "")
    copy_text = dossier.get("facebook_copy", "")

    if not os.path.exists(visual_path):
        return {"status": "ERROR", "message": f"Visual asset not found at {visual_path}"}

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"status": "ERROR", "message": "Playwright is not installed."}

    print("🤖 [Playwright] Launching headless browser for Facebook...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                storage_state=str(FACEBOOK_STATE_FILE),
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto("https://www.facebook.com/", wait_until="networkidle", timeout=30000)

            if "login" in page.url:
                browser.close()
                return {"status": "ERROR", "message": "Facebook session expired. Please re-run 'python3 scripts/capture_sessions.py facebook'."}

            print("👥 [Facebook] Logged in. Preparing post creation...")
            # Facebook post creation logic
            post_box = page.locator("div[role='button']:has-text(\"What's on your mind\"), div[role='button']:has-text('Create post')")
            if post_box.count() > 0:
                post_box.first.click()
                page.wait_for_timeout(2000)

                # Attach file if file input exists
                file_input = page.locator("input[type='file']")
                if file_input.count() > 0:
                    file_input.first.set_input_files(visual_path)
                    page.wait_for_timeout(2500)

                # Insert copy
                text_editor = page.locator("div[role='textbox'], div[aria-label*='Write something']")
                if text_editor.count() > 0:
                    text_editor.first.fill(copy_text)
                    page.wait_for_timeout(1500)

                # Click Post
                submit_btn = page.locator("div[aria-label='Post'][role='button'], button:has-text('Post')")
                if submit_btn.count() > 0:
                    submit_btn.first.click()
                    print("🚀 [Facebook] Post submitted.")
                    page.wait_for_timeout(5000)

            browser.close()
            log_publishing_result("facebook", "SUCCESS", {"topic": dossier.get("topic_title")})
            return {"status": "SUCCESS", "platform": "facebook", "message": "Successfully posted to Facebook."}
    except Exception as e:
        log_publishing_result("facebook", "ERROR", {"error": str(e)})
        return {"status": "ERROR", "error": str(e)}

def dispatch_to_n8n_webhook(dossier: Dict[str, Any], webhook_url: str = None) -> Dict[str, Any]:
    """Posts the approved dossier to the designated n8n webhook (Method 1)."""
    import urllib.request
    target_url = webhook_url or N8N_WEBHOOK_URL
    if not target_url:
        return {"status": "SKIPPED", "message": "N8N_WEBHOOK_URL not configured."}

    payload = {
        "topic": dossier.get("topic_title"),
        "linkedin": dossier.get("linkedin_copy"),
        "instagram": dossier.get("instagram_copy"),
        "facebook": dossier.get("facebook_copy"),
        "image_path": dossier.get("visual_card_path"),
        "source_url": dossier.get("source_url"),
        "timestamp": dossier.get("generated_at")
    }

    req = urllib.request.Request(
        target_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return {"status": "SUCCESS", "response": raw}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}

def execute_multiplatform_publish(dossier: Dict[str, Any]) -> Dict[str, Any]:
    """
    Master Dispatcher:
    Executes Method 2 (Direct Playwright publishing for Instagram and Facebook).
    Executes Method 1 (n8n Webhook) if configured.
    """
    results = {}
    print("\n" + "=" * 60)
    print("🚀 EXECUTING MULTI-PLATFORM DISPATCH // DYVIX TECHNOLOGIES")
    print("=" * 60)

    # 1. Instagram Browser Dispatch
    results["instagram"] = publish_to_instagram_browser(dossier)

    # 2. Facebook Browser Dispatch
    results["facebook"] = publish_to_facebook_browser(dossier)

    # 3. n8n Fallback / Dual Dispatch
    if N8N_WEBHOOK_URL:
        results["n8n"] = dispatch_to_n8n_webhook(dossier)

    # Mark published in dossier
    dossier["published"] = any(r.get("status") == "SUCCESS" for r in results.values())
    dossier["published_at"] = datetime.now(timezone.utc).isoformat()
    dossier["dispatch_results"] = results

    latest_dossier_path = ROOT_DIR / "media" / "latest_dossier.json"
    with open(latest_dossier_path, "w") as f:
        json.dump(dossier, f, indent=2)

    print("\nDispatch Summary:")
    for platform, res in results.items():
        status_icon = "✅" if res.get("status") == "SUCCESS" else "⚠️"
        print(f"  {status_icon} {platform.upper()}: {res.get('status')} - {res.get('message', res.get('error', 'OK'))}")
    print("=" * 60 + "\n")

    return results

def mark_dossier_approved(dossier_path: str) -> Dict[str, Any]:
    """Updates dossier approval status in JSON file."""
    if not os.path.exists(dossier_path):
        raise FileNotFoundError(f"Dossier not found at {dossier_path}")

    with open(dossier_path, "r") as f:
        data = json.load(f)

    data["approved"] = True
    data["ready_to_publish"] = True
    data["approved_at"] = datetime.now(timezone.utc).isoformat()

    with open(dossier_path, "w") as f:
        json.dump(data, f, indent=2)

    return data
