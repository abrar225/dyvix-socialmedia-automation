"""
Centralized Configuration & Environment Loader
Loads environment variables and sets system defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Base paths
ROOT_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = ROOT_DIR / "media"
AUTH_DIR = ROOT_DIR / ".auth"
HISTORY_DIR = ROOT_DIR / "history"

MEDIA_DIR.mkdir(parents=True, exist_ok=True)
AUTH_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# Load .env
ENV_FILE = ROOT_DIR / ".env"
load_dotenv(ENV_FILE)

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
GEMINI_API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY") or os.getenv("GEMINI_API_KEY", "")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# n8n Configuration
N8N_BASE_URL = os.getenv("N8N_BASE_URL", "https://flow.dyvix.net")
N8N_MCP_URL = os.getenv("N8N_MCP_URL", "https://flow.dyvix.net/mcp-server/http")
N8N_API_KEY = os.getenv("N8N_API_KEY", "")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")

# Resend & Review Server Configuration
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RESEND_SENDER = os.getenv("RESEND_SENDER", "automation@opsmentum.online")
REVIEWER_EMAIL = os.getenv("REVIEWER_EMAIL", "moabrarakhunji@gmail.com")
REVIEW_SERVER_PORT = int(os.getenv("REVIEW_SERVER_PORT", "5050"))
LEARNINGS_FILE = MEDIA_DIR / "learnings.json"

# Image Specifications (4:5 Portrait for Instagram & LinkedIn)
IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "1080"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "1350"))
POLLINATIONS_BASE_URL = os.getenv("POLLINATIONS_BASE_URL", "https://image.pollinations.ai/prompt")

# LLM Preferences
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
FALLBACK_NVIDIA_MODEL = "nvidia/nemotron-3.5-bolt-e4b"
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
