# Dyvix Technologies: Autonomous Social Media Automation Engine

A production-grade, 24/7 autonomous social media publishing engine engineered for **Instagram and Facebook** (with LinkedIn integration extensible in Phase 2) for **Dyvix Technologies Private Limited** (https://dyvix.net/).

Designed to operate seamlessly on remote cloud servers inside **Antigravity IDE** using native **Gemini 3.8 Flash (High)** automations.

---

## 🏛️ System Architecture

```
[Layer 1: Discovery & Research]
   ├── Tavily AI Search (Real-time engineering and product trends)
   └── Firecrawl Deep Scraper (Full markdown extraction from source leads)
         │
         ▼
[Layer 2: Strategy & Anti-AI Copywriting]
   ├── Conditioned on Dyvix 8-product ecosystem & media/learnings.json
   ├── Instagram Caption (Hook, 3 hyphenated takeaways, closing thought, hashtags)
   ├── Facebook Community Post (Engineering friction analysis & discussion)
   └── Strict Human-Writer Standard (Zero em-dashes, zero buzzwords, high burstiness)
         │
         ▼
[Layer 3: Visual Generation & Sanitization (Dyvix Design Tokens)]
   ├── 4:5 Vertical Portrait Framing (1080x1350)
   ├── Dyvix Palette: Obsidian (#141718), Crimson Red (#BD2727), Foreground (#F3F4F4)
   ├── Dual-Mode Visual Engine (System Blueprint & Whiteboard Sketch)
   └── Anti-AI Sanitization (EXIF purge, 2% micro-crop, sigma=1.2 film noise)
         │
         ▼
[Layer 4: Human-in-the-Loop Review & Self-Healing Loop]
   ├── Resend Email Notification dispatched to moabrarakhunji@gmail.com
   ├── Local Review Dashboard at http://localhost:5050
   ├── APPROVE -> Automatically triggers Layer 5 browser publishing
   └── REJECT -> Records feedback in media/learnings.json, auto-regenerates, and re-notifies
         │
         ▼
[Layer 5: Automated Social Dispatch via Playwright]
   ├── Headless Chromium loads authenticated sessions from .auth/
   ├── Uploads visual to Instagram and Facebook company pages
   └── Logs audit trail in history/publishing_log.json
```

---

## 📁 Repository Structure

```
dyvix-socialmedia-automation/
├── .auth/                        # Browser session states (ignored by git)
│   ├── .gitkeep
│   ├── instagram-state.json
│   └── facebook-state.json
├── .env.example                  # Secrets template
├── .gitignore                    # Production ignore rules
├── requirements.txt              # Dependencies (Pillow, numpy, python-dotenv, playwright)
├── run_automation.py             # Master CLI runner
├── verify_pipeline.py            # 8-point pre-flight diagnostic self-test
├── DYVIX_AUTOMATION_CONTEXT.md   # Master company and system operational context
├── ANTIGRAVITY_INSTRUCTIONS.md   # Production Antigravity automation prompt
├── README.md                     # Documentation
├── core/
│   ├── __init__.py
│   ├── config.py                 # Paths, environment loader, and defaults
│   ├── research.py               # Tavily + Firecrawl dual-layer discovery
│   ├── copywriter.py             # Anti-AI human-standard copywriting with memory
│   ├── visual_card.py            # Dyvix 1080x1350 visual engine & sanitization
│   ├── notifier.py               # Resend email notification dispatcher
│   ├── review_server.py          # Review dashboard & self-healing feedback server
│   └── publisher.py              # Playwright browser publisher & n8n dispatcher
├── scripts/
│   ├── capture_sessions.py       # Interactive Instagram & Facebook cookie capture utility
│   └── n8n_mcp_client.py         # n8n MCP CLI bridge
├── history/                      # Published logs and audit records
│   └── .gitkeep
└── media/                        # Storage for generated visuals, dossiers, learnings
    ├── .gitkeep
    └── learnings.json            # Continuous human rejection feedback memory
```

---

## 🚀 Setup on Cloud Server (`ubuntu@free-arm-instance`)

### 1. Clone the Repository
```bash
git clone https://github.com/abrar225/dyvix-socialmedia-automation.git
cd dyvix-socialmedia-automation
```

### 2. Install Dependencies & Playwright Browsers
```bash
sudo apt update && sudo apt install -y python3-pip python3-pil python3-numpy
pip install -r requirements.txt
playwright install --with-deps chromium
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
nano .env   # Enter your Tavily, Firecrawl, Gemini, and Resend API keys
```

### 4. Authenticate Browser Sessions
Run the interactive session capture utility to save cookies into `.auth/`:
```bash
# Capture Instagram session
python3 scripts/capture_sessions.py instagram

# Capture Facebook session
python3 scripts/capture_sessions.py facebook

# Verify sessions
python3 scripts/capture_sessions.py check
```

*(If running on a remote headless server without a desktop display, capture the sessions on your local laptop first, then copy `.auth/` to the server via `scp -r .auth/ ubuntu@<server-ip>:~/dyvix-socialmedia-automation/.auth/`)*

### 5. Run Pre-Flight Diagnostics
```bash
python3 verify_pipeline.py
```
*All 8 checks must display `✅ PASS`.*

---

## 🕒 Daily Scheduled Operations

### Option A: Antigravity Scheduled Automation
In Antigravity IDE, open **Automations** -> **+ Create Automation**, paste the prompt from `ANTIGRAVITY_INSTRUCTIONS.md`, and set the schedule to `9:00 AM daily`.

### Option B: 24/7 Cloud Cron (Works when laptop is shut down)
```bash
crontab -e
```
Add:
```bash
0 9 * * * cd /home/ubuntu/dyvix-socialmedia-automation && /usr/bin/python3 run_automation.py --mode generate >> /home/ubuntu/dyvix-socialmedia-automation/cron.log 2>&1
```

---

## 🛠️ CLI Reference

```bash
# Generate fresh daily draft and send review alert
python3 run_automation.py --mode generate

# Run local review dashboard
python3 run_automation.py --mode review-server

# Publish approved content to Instagram and Facebook
python3 run_automation.py --mode publish

# Re-send notification email
python3 run_automation.py --mode notify
```
