#!/usr/bin/env python3
"""
Master Social Media Automation CLI Runner
Designed specifically for Antigravity Scheduled Automations and Autonomous Runs.
"""
import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Ensure root directory is on Python path
CURRENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CURRENT_DIR))

from core.config import (
    MEDIA_DIR,
    REVIEW_SERVER_PORT,
    REVIEWER_EMAIL
)
from core.research import execute_research
from core.copywriter import generate_copywriting_package
from core.visual_card import create_visual
from core.notifier import send_resend_notification
from core.publisher import execute_multiplatform_publish, mark_dossier_approved
from core.review_server import start_server_background, run_server_foreground

DEFAULT_QUERIES = [
    "enterprise software architecture scalable microservices cloudflare 2026",
    "artificial intelligence engineering breakthroughs developer tools 2026",
    "open source AI agent memory architectures long running systems",
    "real time distributed messaging high throughput queueing architectures",
    "enterprise ERP CRM automation field sales workforce tracking technology"
]

def run_generate(query: str = None, visual_mode: str = "auto", use_diffusion: bool = False, skip_notify: bool = False) -> dict:
    timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    target_query = query or DEFAULT_QUERIES[0]
    
    print("=" * 70)
    print("🚀 STARTING AUTONOMOUS SOCIAL MEDIA GENERATION PIPELINE")
    print("=" * 70)
    print(f"Timestamp: {timestamp_str}")
    print(f"Target Query: {target_query}\n")

    # Step 1: Research
    research_data = execute_research(target_query)
    print(f"✅ Research Completed. Lead Source: {research_data['url']}\n")

    # Step 2: Copywriting (with Historical Feedback Conditioning)
    copy_package = generate_copywriting_package(research_data)
    print("✅ Copywriting Package Generated (Anti-AI Slop Compliant).\n")

    # Determine visual mode
    selected_mode = visual_mode
    if selected_mode == "auto":
        selected_mode = copy_package.get("visual_mode", "auto")

    # Step 3: Visual Generation
    latest_visual_path = str(MEDIA_DIR / "latest_visual.jpg")
    archive_visual_path = str(MEDIA_DIR / f"visual_{timestamp_str}.jpg")
    
    create_visual(
        title=copy_package.get("topic_title", "System Architecture"),
        subtitle=copy_package.get("subtitle", "Engineering Breakdown"),
        pillars=copy_package.get("pillars", []),
        prompt=copy_package.get("image_prompt", ""),
        output_path=latest_visual_path,
        visual_mode=selected_mode,
        use_diffusion=use_diffusion
    )
    # Save archive copy
    with open(latest_visual_path, "rb") as src, open(archive_visual_path, "wb") as dst:
        dst.write(src.read())
    print(f"✅ 1080x1350 Visual Saved: {latest_visual_path}\n")

    # Step 4: Save Dossier
    dossier = {
        "status": "DRAFT_READY",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "topic_title": copy_package.get("topic_title"),
        "subtitle": copy_package.get("subtitle"),
        "core_insight": copy_package.get("core_insight"),
        "visual_mode": selected_mode,
        "pillars": copy_package.get("pillars"),
        "source_url": research_data.get("url"),
        "linkedin_copy": copy_package.get("linkedin_copy"),
        "instagram_copy": copy_package.get("instagram_copy"),
        "facebook_copy": copy_package.get("facebook_copy"),
        "image_prompt": copy_package.get("image_prompt"),
        "visual_card_path": latest_visual_path,
        "archive_visual_path": archive_visual_path,
        "approved": False,
        "published": False
    }

    latest_dossier_path = str(MEDIA_DIR / "latest_dossier.json")
    archive_dossier_path = str(MEDIA_DIR / f"dossier_{timestamp_str}.json")

    with open(latest_dossier_path, "w") as f:
        json.dump(dossier, f, indent=2)
    with open(archive_dossier_path, "w") as f:
        json.dump(dossier, f, indent=2)

    # Step 5: Send Resend Notification
    review_url = f"http://localhost:{REVIEW_SERVER_PORT}"
    if not skip_notify:
        send_resend_notification(dossier, review_url=review_url)

    print("=" * 70)
    print("✨ DAILY CONTENT DOSSIER GENERATION COMPLETE")
    print("=" * 70)
    print(f"\n📌 TITLE: {dossier['topic_title']}")
    print(f"💡 INSIGHT: {dossier['core_insight']}")
    print(f"🎨 VISUAL MODE: {dossier['visual_mode'].upper()}")
    print("\n--- LINKEDIN PREVIEW ---")
    print(dossier['linkedin_copy'][:280] + "...")
    print("\n--- INSTAGRAM PREVIEW ---")
    print(dossier['instagram_copy'][:280] + "...")
    print("\n--- FACEBOOK PREVIEW ---")
    print(dossier['facebook_copy'][:280] + "...")
    print(f"\n🖼️  VISUAL ASSET: file://{latest_visual_path}")
    print(f"📁 DOSSIER FILE: file://{latest_dossier_path}")
    print(f"🌐 REVIEW DASHBOARD: {review_url}")
    print("=" * 70)

    return dossier

def run_publish():
    latest_dossier_path = str(MEDIA_DIR / "latest_dossier.json")
    if not os.path.exists(latest_dossier_path):
        print(f"❌ Error: No dossier found at {latest_dossier_path}. Run --mode generate first.")
        sys.exit(1)

    with open(latest_dossier_path, "r") as f:
        dossier = json.load(f)

    print(f"📡 Publishing content dossier: '{dossier.get('topic_title')}'...")
    mark_dossier_approved(latest_dossier_path)
    result = execute_multiplatform_publish(dossier)
    return result

def main():
    parser = argparse.ArgumentParser(description="Autonomous Social Media Engine for Antigravity")
    parser.add_argument("--mode", choices=["generate", "publish", "review-server", "notify", "full"], default="generate",
                        help="Operation mode: 'generate' drafts, 'publish' approved draft, 'review-server' UI, 'notify' resend email")
    parser.add_argument("--query", type=str, default=None, help="Custom research topic query")
    parser.add_argument("--visual-mode", choices=["auto", "blueprint", "whiteboard_sketch"], default="auto",
                        help="Visual card aesthetic mode")
    parser.add_argument("--diffusion", action="store_true", help="Use AI diffusion generation instead of editorial card")
    parser.add_argument("--skip-notify", action="store_true", help="Skip sending Resend email notification")
    parser.add_argument("--auto-publish", action="store_true", help="Automatically publish immediately after generating")

    args = parser.parse_args()

    if args.mode in ["generate", "full"]:
        dossier = run_generate(query=args.query, visual_mode=args.visual_mode, use_diffusion=args.diffusion, skip_notify=args.skip_notify)
        if args.mode == "full" or args.auto_publish:
            print("\n🚀 Executing automatic publication...")
            run_publish()
    elif args.mode == "publish":
        run_publish()
    elif args.mode == "notify":
        latest_dossier_path = str(MEDIA_DIR / "latest_dossier.json")
        if os.path.exists(latest_dossier_path):
            with open(latest_dossier_path, "r") as f:
                dossier = json.load(f)
            send_resend_notification(dossier)
        else:
            print("❌ No dossier found to notify.")
    elif args.mode == "review-server":
        run_server_foreground()

if __name__ == "__main__":
    main()
