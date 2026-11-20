#!/usr/bin/env python3
"""
Interactive Session State Capture Utility for Instagram & Facebook
Launches browser to log into accounts, then exports cookies/storage state to .auth/
"""
import os
import sys
import argparse
from pathlib import Path

# Add root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.config import AUTH_DIR

INSTAGRAM_STATE = AUTH_DIR / "instagram-state.json"
FACEBOOK_STATE = AUTH_DIR / "facebook-state.json"

def capture_instagram():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright is not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("📸 INSTAGRAM SESSION CAPTURE // DYVIX AUTOMATION")
    print("=" * 60)
    print("Opening Chromium browser for Instagram login...")
    print("Please log in to your Instagram account in the browser window.")
    print("Once logged in and seeing your feed, return to this terminal and press ENTER.")
    print("=" * 60)

    try:
        with sync_playwright() as p:
            # Check if display is available
            is_headless = not bool(os.environ.get("DISPLAY") or sys.platform == "darwin")
            if is_headless:
                print("⚠️  Notice: Running in headless mode because no visual display was detected.")
                print("If you are on a remote server, run this on your local laptop first, then scp .auth/ to the server.")

            browser = p.chromium.launch(
                headless=is_headless,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto("https://www.instagram.com/accounts/login/")

            input("\n👉 Press [ENTER] after you have completed logging into Instagram... ")

            AUTH_DIR.mkdir(parents=True, exist_ok=True)
            context.storage_state(path=str(INSTAGRAM_STATE))
            browser.close()

            print(f"✅ Success: Instagram session saved to {INSTAGRAM_STATE}")
    except Exception as e:
        print(f"❌ Error capturing Instagram session: {e}")

def capture_facebook():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright is not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("👥 FACEBOOK SESSION CAPTURE // DYVIX AUTOMATION")
    print("=" * 60)
    print("Opening Chromium browser for Facebook login...")
    print("Please log in to your Facebook account and switch to your company page if applicable.")
    print("Once logged in, return to this terminal and press ENTER.")
    print("=" * 60)

    try:
        with sync_playwright() as p:
            is_headless = not bool(os.environ.get("DISPLAY") or sys.platform == "darwin")
            if is_headless:
                print("⚠️  Notice: Running in headless mode because no visual display was detected.")

            browser = p.chromium.launch(
                headless=is_headless,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.goto("https://www.facebook.com/login")

            input("\n👉 Press [ENTER] after you have completed logging into Facebook... ")

            AUTH_DIR.mkdir(parents=True, exist_ok=True)
            context.storage_state(path=str(FACEBOOK_STATE))
            browser.close()

            print(f"✅ Success: Facebook session saved to {FACEBOOK_STATE}")
    except Exception as e:
        print(f"❌ Error capturing Facebook session: {e}")

def check_status():
    print("\n" + "=" * 60)
    print("🔍 AUTHENTICATION SESSION STATUS")
    print("=" * 60)
    ig_ok = INSTAGRAM_STATE.exists() and os.path.getsize(INSTAGRAM_STATE) > 50
    fb_ok = FACEBOOK_STATE.exists() and os.path.getsize(FACEBOOK_STATE) > 50

    print(f"  Instagram Session (.auth/instagram-state.json): {'✅ ACTIVE' if ig_ok else '❌ MISSING'}")
    print(f"  Facebook Session  (.auth/facebook-state.json):  {'✅ ACTIVE' if fb_ok else '❌ MISSING'}")
    print("=" * 60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Capture browser sessions for Instagram and Facebook")
    parser.add_argument("platform", choices=["instagram", "facebook", "all", "check"], default="all", nargs="?",
                        help="Platform to capture: 'instagram', 'facebook', 'all', or 'check'")
    args = parser.parse_args()

    if args.platform == "check":
        check_status()
    elif args.platform == "instagram":
        capture_instagram()
    elif args.platform == "facebook":
        capture_facebook()
    elif args.platform == "all":
        capture_instagram()
        capture_facebook()
        check_status()

if __name__ == "__main__":
    main()
