"""
Layer 4: Local Review Landing Page & Feedback Self-Improvement Server
Serves a luxury monochrome dark-mode dashboard at http://localhost:5050 for Human-in-the-Loop approval.

Includes:
1. Approve Action (updates latest_dossier.json with live edits if made).
2. Reject with Feedback Action (persists critiques to media/learnings.json).
"""
import os
import sys
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.config import (
    MEDIA_DIR,
    REVIEW_SERVER_PORT,
    LEARNINGS_FILE
)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dyvix Technologies // Content Review Dashboard</title>
  <style>
    :root {
      --bg: #141718;
      --card-bg: #1D2123;
      --border: #252A2C;
      --text: #F3F4F4;
      --text-muted: #A3AAAD;
      --accent: #BD2727;
      --accent-hi: #E5463F;
      --accent-green: #4ADE80;
      --accent-red: #ef4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    header {
      background: #18181b;
      border-bottom: 1px solid var(--border);
      padding: 16px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .logo-badge {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .badge {
      background: #27272a;
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.05em;
    }
    .status-pill {
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      background: #27272a;
      color: var(--text-muted);
    }
    .status-pill.approved { background: rgba(34, 197, 94, 0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
    .status-pill.rejected { background: rgba(239, 68, 68, 0.15); color: var(--accent-red); border: 1px solid var(--accent-red); }

    .main-container {
      display: grid;
      grid-template-columns: 460px 1fr;
      gap: 28px;
      padding: 28px 32px;
      flex: 1;
      max-width: 1440px;
      margin: 0 auto;
      width: 100%;
    }
    .left-col {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .visual-wrapper {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
      text-align: center;
    }
    .visual-img {
      width: 100%;
      height: auto;
      border-radius: 8px;
      aspect-ratio: 4/5;
      object-fit: cover;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .meta-box {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.6;
    }
    .meta-box strong { color: var(--text); }

    .right-col {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .tabs-nav {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 12px;
    }
    .tab-btn {
      background: transparent;
      border: 1px solid transparent;
      color: var(--text-muted);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      font-size: 14px;
      transition: all 0.2s;
    }
    .tab-btn.active {
      background: var(--card-bg);
      color: var(--text);
      border-color: var(--border);
    }
    .copy-textarea {
      width: 100%;
      height: 380px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px;
      color: var(--text);
      font-size: 14px;
      line-height: 1.6;
      font-family: inherit;
      resize: vertical;
    }
    .copy-textarea:focus {
      outline: none;
      border-color: var(--accent);
    }
    .action-bar {
      display: flex;
      gap: 16px;
      margin-top: auto;
      padding-top: 16px;
    }
    .btn {
      padding: 14px 28px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .btn-approve {
      background: #ffffff;
      color: #000000;
    }
    .btn-approve:hover {
      background: #e4e4e7;
      transform: translateY(-1px);
    }
    .btn-reject {
      background: rgba(239, 68, 68, 0.15);
      color: #fca5a5;
      border: 1px solid #7f1d1d;
    }
    .btn-reject:hover {
      background: rgba(239, 68, 68, 0.25);
    }
    .btn-copy {
      background: #27272a;
      color: var(--text);
      margin-left: auto;
    }

    /* Modal */
    .modal-backdrop {
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      backdrop-filter: blur(4px);
      z-index: 100;
      align-items: center;
      justify-content: center;
    }
    .modal-backdrop.active { display: flex; }
    .modal-box {
      background: #18181b;
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 24px;
      max-width: 500px;
      width: 90%;
    }
    .modal-title { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    .modal-desc { font-size: 13px; color: var(--text-muted); line-height: 1.5; margin-bottom: 16px; }
    .modal-textarea {
      width: 100%;
      height: 120px;
      background: #09090b;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 12px;
      color: var(--text);
      font-size: 13px;
      margin-bottom: 16px;
    }
    .modal-actions { display: flex; justify-content: flex-end; gap: 12px; }
  </style>
</head>
<body>
  <header>
    <div class="logo-badge">
      <span class="badge" style="background:#BD2727; color:#F3F4F4;">DYVIX TECHNOLOGIES // 2026</span>
      <h2 id="top-title" style="font-size: 16px; font-weight: 600;">Dyvix Content Review</h2>
    </div>
    <div id="status-display" class="status-pill">STATUS: DRAFT_READY</div>
  </header>

  <div class="main-container">
    <div class="left-col">
      <div class="visual-wrapper">
        <img id="visual-preview" class="visual-img" src="/media/visual" alt="1080x1350 Visual Card" onerror="this.alt='Visual loading...';">
      </div>
      <div class="meta-box">
        <p><strong>Topic:</strong> <span id="meta-topic">...</span></p>
        <p style="margin-top: 6px;"><strong>Core Insight:</strong> <span id="meta-insight">...</span></p>
        <p style="margin-top: 6px;"><strong>Source URL:</strong> <a id="meta-url" href="#" target="_blank" style="color: var(--accent); text-decoration: none;">View source &rarr;</a></p>
      </div>
    </div>

    <div class="right-col">
      <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('linkedin')">LinkedIn Post</button>
        <button class="tab-btn" onclick="switchTab('instagram')">Instagram Caption</button>
        <button class="tab-btn" onclick="switchTab('facebook')">Facebook Community</button>
        <button class="btn btn-copy" onclick="copyCurrentTab()">📋 Copy Text</button>
      </div>

      <textarea id="copy-editor" class="copy-textarea"></textarea>

      <div class="action-bar">
        <button class="btn btn-approve" onclick="handleApprove()">✅ Approve & Confirm Draft</button>
        <button class="btn btn-reject" onclick="openRejectModal()">❌ Reject with Feedback</button>
      </div>
    </div>
  </div>

  <!-- Rejection Feedback Modal -->
  <div id="reject-modal" class="modal-backdrop">
    <div class="modal-box">
      <div class="modal-title">Reject with Constructive Feedback</div>
      <p class="modal-desc">Explain exactly what was deficient or undesirable. This feedback will be saved into the agent's continuous learning memory so future generations never repeat this mistake.</p>
      <textarea id="reject-reason" class="modal-textarea" placeholder="e.g. Too repetitive in paragraph 2, remove the hashtag #example, tone was too casual for senior engineering audience..."></textarea>
      <div class="modal-actions">
        <button class="btn" style="background:#27272a; color:#f4f4f5;" onclick="closeRejectModal()">Cancel</button>
        <button class="btn" style="background:#ef4444; color:#ffffff;" onclick="submitReject()">Confirm Rejection</button>
      </div>
    </div>
  </div>

  <script>
    let currentDossier = {};
    let activePlatform = 'linkedin';

    async function loadDossier() {
      try {
        const res = await fetch('/api/dossier');
        currentDossier = await res.json();

        document.getElementById('top-title').textContent = currentDossier.topic_title || 'Content Review';
        document.getElementById('meta-topic').textContent = currentDossier.topic_title || '';
        document.getElementById('meta-insight').textContent = currentDossier.core_insight || '';
        document.getElementById('meta-url').href = currentDossier.source_url || '#';

        updateStatusUI(currentDossier.status || 'DRAFT_READY', currentDossier.approved);
        renderCurrentTab();
      } catch (e) {
        console.error('Failed to load dossier', e);
      }
    }

    function updateStatusUI(status, approved) {
      const el = document.getElementById('status-display');
      el.textContent = 'STATUS: ' + status;
      el.className = 'status-pill' + (approved ? ' approved' : (status === 'REJECTED' ? ' rejected' : ''));
    }

    function switchTab(platform) {
      saveCurrentText();
      activePlatform = platform;
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      event.target.classList.add('active');
      renderCurrentTab();
    }

    function saveCurrentText() {
      const text = document.getElementById('copy-editor').value;
      if (activePlatform === 'linkedin') currentDossier.linkedin_copy = text;
      else if (activePlatform === 'instagram') currentDossier.instagram_copy = text;
      else if (activePlatform === 'facebook') currentDossier.facebook_copy = text;
    }

    function renderCurrentTab() {
      const editor = document.getElementById('copy-editor');
      if (activePlatform === 'linkedin') editor.value = currentDossier.linkedin_copy || '';
      else if (activePlatform === 'instagram') editor.value = currentDossier.instagram_copy || '';
      else if (activePlatform === 'facebook') editor.value = currentDossier.facebook_copy || '';
    }

    function copyCurrentTab() {
      const text = document.getElementById('copy-editor').value;
      navigator.clipboard.writeText(text);
      alert('Copied ' + activePlatform.toUpperCase() + ' draft to clipboard!');
    }

    async function handleApprove() {
      saveCurrentText();
      const res = await fetch('/api/approve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentDossier)
      });
      const data = await res.json();
      if (data.status === 'SUCCESS') {
        updateStatusUI('APPROVED', true);
        alert('🎉 Content Dossier marked APPROVED! Engine is ready to publish.');
      }
    }

    function openRejectModal() {
      document.getElementById('reject-modal').classList.add('active');
    }
    function closeRejectModal() {
      document.getElementById('reject-modal').classList.remove('active');
    }

    async function submitReject() {
      const reason = document.getElementById('reject-reason').value.trim();
      if (!reason) {
        alert('Please specify the reason for rejection.');
        return;
      }
      const res = await fetch('/api/reject', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: currentDossier.topic_title,
          critique: reason
        })
      });
      const data = await res.json();
      closeRejectModal();
      updateStatusUI('REJECTED', false);
      alert('Recorded feedback into agent learning memory. Future runs will avoid this mistake.');
    }

    loadDossier();
  </script>
</body>
</html>
"""

class ReviewServerHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._set_headers(200, "text/html")
            self.wfile.write(HTML_PAGE.encode("utf-8"))
            return

        elif self.path == "/media/visual":
            visual_path = MEDIA_DIR / "latest_visual.jpg"
            if visual_path.exists():
                self._set_headers(200, "image/jpeg")
                with open(visual_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404, "text/plain")
                self.wfile.write(b"Visual image not found.")
            return

        elif self.path == "/api/dossier":
            dossier_path = MEDIA_DIR / "latest_dossier.json"
            if dossier_path.exists():
                self._set_headers(200, "application/json")
                with open(dossier_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self._set_headers(404, "application/json")
                self.wfile.write(json.dumps({"error": "No dossier generated yet."}).encode("utf-8"))
            return

        elif self.path == "/api/status":
            dossier_path = MEDIA_DIR / "latest_dossier.json"
            status_data = {"status": "UNKNOWN", "approved": False}
            if dossier_path.exists():
                with open(dossier_path, "r") as f:
                    data = json.load(f)
                    status_data = {
                        "status": data.get("status", "DRAFT_READY"),
                        "approved": data.get("approved", False),
                        "topic": data.get("topic_title")
                    }
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
            return

        self._set_headers(404, "text/plain")
        self.wfile.write(b"Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/api/approve":
            dossier_path = MEDIA_DIR / "latest_dossier.json"
            dossier_data = {}
            if dossier_path.exists():
                with open(dossier_path, "r") as f:
                    dossier_data = json.load(f)

            # Update with live edits if passed
            for key in ["linkedin_copy", "instagram_copy", "facebook_copy"]:
                if key in payload and payload[key]:
                    dossier_data[key] = payload[key]

            dossier_data["approved"] = True
            dossier_data["status"] = "APPROVED"
            dossier_data["approved_at"] = datetime.now(timezone.utc).isoformat()

            with open(dossier_path, "w") as f:
                json.dump(dossier_data, f, indent=2)

            # Trigger auto-publish in background thread
            def _auto_publish():
                try:
                    import subprocess
                    script = str(ROOT_DIR / "run_automation.py")
                    print("📡 [Review Server] Approval confirmed. Dispatching publisher...")
                    subprocess.run([sys.executable, script, "--mode", "publish"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"❌ [Review Server Publish Error] {e}")

            threading.Thread(target=_auto_publish, daemon=True).start()

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"status": "SUCCESS", "message": "Dossier approved and queued for publishing."}).encode("utf-8"))
            return

        elif self.path == "/api/reject":
            critique = payload.get("critique", "No critique provided.")
            topic = payload.get("topic", "General Generation")

            # 1. Update dossier status
            dossier_path = MEDIA_DIR / "latest_dossier.json"
            if dossier_path.exists():
                with open(dossier_path, "r") as f:
                    dossier_data = json.load(f)
                dossier_data["approved"] = False
                dossier_data["status"] = "REJECTED"
                dossier_data["rejected_at"] = datetime.now(timezone.utc).isoformat()
                dossier_data["rejection_reason"] = critique
                with open(dossier_path, "w") as f:
                    json.dump(dossier_data, f, indent=2)

            # 2. Append to persistent learnings ledger
            learnings = []
            if LEARNINGS_FILE.exists():
                try:
                    with open(LEARNINGS_FILE, "r") as f:
                        learnings = json.load(f)
                except Exception:
                    learnings = []

            learnings.append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "topic": topic,
                "critique": critique
            })

            with open(LEARNINGS_FILE, "w") as f:
                json.dump(learnings, f, indent=2)

            print(f"📝 [Learnings Saved] Rejection critique recorded: '{critique}'")

            # Trigger auto-regeneration in background thread
            def _auto_regenerate():
                try:
                    import subprocess
                    script = str(ROOT_DIR / "run_automation.py")
                    print("🔄 [Review Server] Rejection recorded. Regenerating package conditioned on feedback...")
                    subprocess.run([sys.executable, script, "--mode", "generate"], cwd=str(ROOT_DIR))
                except Exception as e:
                    print(f"❌ [Review Server Regeneration Error] {e}")

            threading.Thread(target=_auto_regenerate, daemon=True).start()

            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({"status": "RECORDED", "message": "Feedback stored in learning memory. Generating fresh draft..."}).encode("utf-8"))
            return

        self._set_headers(404, "text/plain")
        self.wfile.write(b"Not Found")

def start_server_background(port: int = REVIEW_SERVER_PORT) -> HTTPServer:
    """Starts the review server in a daemon thread."""
    server = HTTPServer(("0.0.0.0", port), ReviewServerHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"🌐 [Review Server Active] Serving review dashboard at: http://localhost:{port}")
    return server

def run_server_foreground(port: int = REVIEW_SERVER_PORT):
    """Starts the review server synchronously in the foreground."""
    server = HTTPServer(("0.0.0.0", port), ReviewServerHandler)
    print(f"🌐 [Review Server Active] Open dashboard at: http://localhost:{port}")
    print("Press Ctrl+C to terminate.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nReview server stopped.")
        server.server_close()

if __name__ == "__main__":
    run_server_foreground()
