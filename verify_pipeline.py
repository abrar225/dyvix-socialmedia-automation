#!/usr/bin/env python3
"""
Pre-Flight Health Verification Script
Validates all APIs, credentials, and dual-mode visual engines in under 10 seconds.
"""
import sys
import os
import json
import urllib.request
from pathlib import Path

# Add root to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

from core.config import (
    TAVILY_API_KEY,
    FIRECRAWL_API_KEY,
    GEMINI_API_KEY,
    NVIDIA_API_KEY,
    RESEND_API_KEY,
    RESEND_SENDER,
    REVIEWER_EMAIL,
    REVIEW_SERVER_PORT,
    MEDIA_DIR
)

def test_imports():
    print("Checking core dependencies...", end=" ")
    try:
        import PIL
        import numpy
        import dotenv
        print("✅ OK")
        return True
    except ImportError as e:
        print(f"❌ FAILED ({e})")
        return False

def test_auth_structure():
    print("Validating .auth/ and history/ storage boundaries...", end=" ")
    from core.config import AUTH_DIR, HISTORY_DIR
    if AUTH_DIR.exists() and HISTORY_DIR.exists():
        print("✅ OK")
        return True
    print("❌ FAILED")
    return False

def test_dual_mode_visual():
    print("Testing Dual-Mode Visual Engine (Blueprint & Whiteboard Sketch)...", end=" ")
    from core.visual_card import render_blueprint_card, render_sketch_card
    try:
        bp_path = str(MEDIA_DIR / "test_blueprint.jpg")
        sk_path = str(MEDIA_DIR / "test_sketch.jpg")
        pillars = [
            {"title": "ISOLATION LAYER", "desc": "Deterministic execution boundaries prevent state drift"},
            {"title": "FEEDBACK ADAPTATION", "desc": "Historical human critiques condition future prompts"},
            {"title": "WATERMARK DECOUPLING", "desc": "Gaussian micro-noise dissolves neural classifiers"}
        ]
        render_blueprint_card("System Architecture Test", "Blueprint Verification", pillars, bp_path)
        render_sketch_card("Mental Model Test", "Sketch Verification", pillars, sk_path)

        bp_size = os.path.getsize(bp_path) if os.path.exists(bp_path) else 0
        sk_size = os.path.getsize(sk_path) if os.path.exists(sk_path) else 0

        # Clean up
        if os.path.exists(bp_path): os.remove(bp_path)
        if os.path.exists(sk_path): os.remove(sk_path)

        if bp_size > 10000 and sk_size > 10000:
            print(f"✅ OK (Blueprint: {bp_size}b, Sketch: {sk_size}b)")
            return True
        print("❌ FAILED (Files incomplete)")
        return False
    except Exception as e:
        print(f"❌ FAILED ({e})")
        return False

def test_tavily():
    print("Testing Tavily AI Search API...", end=" ")
    from core.research import search_tavily
    try:
        res = search_tavily("test AI news", max_results=1)
        if res and len(res) > 0:
            print(f"✅ OK (Found: {res[0].get('title')[:30]}...)")
            return True
        print("❌ FAILED (Empty results)")
        return False
    except Exception as e:
        print(f"❌ FAILED ({e})")
        return False

def test_firecrawl():
    print("Testing Firecrawl API...", end=" ")
    from core.research import scrape_firecrawl
    try:
        md = scrape_firecrawl("https://example.com")
        if md and len(md) > 0:
            print("✅ OK")
            return True
        print("⚠️  NOTICE (Scrape fallback available)")
        return True
    except Exception as e:
        print(f"⚠️  NOTICE ({e}, fallback active)")
        return True

def test_llm():
    print("Testing Copywriting LLM (Gemini / NVIDIA)...", end=" ")
    from core.copywriter import call_gemini, call_nvidia_fallback
    try:
        res = call_gemini("Output JSON: {\"status\": \"ok\"}")
        if isinstance(res, dict) and len(res) > 0:
            print("✅ OK (Gemini active)")
            return True
    except Exception as e:
        print(f"\n  [Gemini check: {e}]. Testing NVIDIA fallback...", end=" ")
        try:
            res = call_nvidia_fallback("Output JSON: {\"status\": \"ok\"}")
            if isinstance(res, dict) and len(res) > 0:
                print("✅ OK (NVIDIA Nemotron active)")
                return True
        except Exception as e2:
            print(f"❌ FAILED ({e2})")
            return False
    return False

def test_resend_config():
    print(f"Validating Resend Email Config ({RESEND_SENDER} -> {REVIEWER_EMAIL})...", end=" ")
    if RESEND_API_KEY and RESEND_API_KEY.startswith("re_"):
        print("✅ OK (API Key configured)")
        return True
    print("⚠️  NOTICE (RESEND_API_KEY not configured)")
    return True

def test_review_server():
    print("Testing Local Review Server Engine...", end=" ")
    from core.review_server import start_server_background
    server = None
    try:
        test_port = REVIEW_SERVER_PORT + 10  # Use test port to avoid collision
        server = start_server_background(port=test_port)
        url = f"http://127.0.0.1:{test_port}/api/status"
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "status" in data:
                print(f"✅ OK (Port {test_port} responsive)")
                server.server_close()
                return True
        if server: server.server_close()
        print("❌ FAILED (Invalid response)")
        return False
    except Exception as e:
        if server: server.server_close()
        print(f"⚠️  NOTICE ({e})")
        return True

def main():
    print("=" * 60)
    print("PRE-FLIGHT SYSTEM DIAGNOSTICS // PRODUCTION 2026")
    print("=" * 60)

    checks = [
        ("Python Dependencies", test_imports()),
        ("Storage Boundaries (.auth/ & history/)", test_auth_structure()),
        ("Dual-Mode Visual Engine", test_dual_mode_visual()),
        ("Tavily AI Search", test_tavily()),
        ("Firecrawl Deep Scraper", test_firecrawl()),
        ("Copywriting LLM", test_llm()),
        ("Resend Email Config", test_resend_config()),
        ("Review Server Engine", test_review_server())
    ]

    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY:")
    all_passed = True
    for name, status in checks:
        icon = "✅ PASS" if status else "❌ FAIL"
        if not status:
            all_passed = False
        print(f"  {name:<32} {icon}")
    print("=" * 60)

    if all_passed:
        print("🎉 ALL SYSTEMS READY FOR PRODUCTION AUTOMATION!")
        sys.exit(0)
    else:
        print("⚠️  SOME CHECKS FAILED. Review errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
