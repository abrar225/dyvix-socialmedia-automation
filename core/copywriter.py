"""
Layer 2: Senior Strategic Analysis & Anti-AI Copywriting Engine
Strictly complies with the Human-Writer Standard, Wikipedia Manual of Style, and continuous learning feedback:
- ZERO em-dashes (—) or en-dashes (–)
- ZERO AI slop buzzwords (delve, tapestry, landscape, game-changer, etc.)
- ZERO repetitive emoji ladders
- ZERO fake engagement begging
- High burstiness and technical cadence
- Dynamic prompt conditioning based on previous human rejection feedback
"""
import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any
from core.config import (
    GEMINI_API_KEY,
    DEFAULT_GEMINI_MODEL,
    NVIDIA_API_KEY,
    NVIDIA_BASE_URL,
    FALLBACK_NVIDIA_MODEL,
    LEARNINGS_FILE
)

BANNED_WORDS = [
    "delve", "tapestry", "beacon", "testament", "foster", "pivotal",
    "crucial", "vital", "harness", "unleash", "elevate", "supercharge",
    "demystify", "seamless", "game-changer", "revolutionary",
    "paradigm shift", "fast-paced world", "in today's digital age",
    "transformative", "realm", "ever-evolving"
]

BASE_SYSTEM_PROMPT = """You are the Principal Systems Engineering Writer for Dyvix Technologies Private Limited (https://dyvix.net/), an enterprise software development firm based in Ahmedabad. You produce authoritative, zero-slop technical social content for Instagram, Facebook, and LinkedIn.

NON-NEGOTIABLE WRITING CONSTRAINTS:
1. BAN EM-DASHES AND EN-DASHES: Never write '—' or '–'. Use commas, colons, or standard periods.
2. BAN AI SLOP WORDS: Never use words like 'delve', 'tapestry', 'landscape', 'beacon', 'crucial', 'vital', 'elevate', 'supercharge', 'game-changer', 'revolutionary', 'paradigm shift', 'seamless'.
3. BAN EMOJI LADDERS: Never build bullet points with emojis (no ⚡, 🚀, 🎯, 🔥). Use simple hyphens (-) or natural prose.
4. BAN FAKE ENGAGEMENT BEGGING: Never end with 'What do you think? Let me know below!' or 'Save this post'. End with a blunt architectural trade-off or technical dilemma.
5. HIGH BURSTINESS: Vary sentence lengths aggressively. Mix 4-word punchy sentences with 25-word technical sentences packed with concrete numbers.
6. DYVIX CONTEXT: Connect engineering breakthroughs to scalable software architectures, high-reliability microservices, distributed data, or practical enterprise operations (such as bulk messaging, ERP/CRM workflows, field intelligence, or automated manufacturing).

VISUAL PILLARS & VISUAL MODE:
- Provide 3 technical pillars for an editorial card (Title: max 25 chars, Description: max 100 chars).
- Recommend visual_mode: 'blueprint' (if structural framework/infrastructure) OR 'whiteboard_sketch' (if mental model/developer friction/heuristics).
- Provide a clean 4:5 vertical editorial 3D illustration prompt (Dyvix Obsidian #141718 background, Crimson #BD2727 accents, zero text/letters).
"""

USER_PROMPT_TEMPLATE = """Research Dossier:
Headline: {title}
Primary URL: {url}
Date: {published_date}
Synthesized Insights:
{deep_content}

{learnings_section}
Synthesize this into a structured JSON object with EXACTLY these keys:
- topic_title: string (clean, technical headline, max 60 chars)
- subtitle: string (specific architectural context, max 70 chars)
- core_insight: string (the contrarian or technical realization)
- visual_mode: string ('blueprint' or 'whiteboard_sketch')
- pillars: list of 3 items, each an object with:
    - title: string (short capitalized heading, e.g. "EPISODIC PRUNING")
    - desc: string (1 concise sentence explaining the engineering mechanism)
- linkedin_copy: string (150-180 words. High burstiness. Zero em dashes. Technical depth. No body links. 3 niche hashtags)
- instagram_copy: string (Hook line, 3 hyphenated takeaways, closing technical thought, 5 hashtags)
- facebook_copy: string (Conversational breakdown of the engineering friction for dev communities)
- image_prompt: string (4:5 vertical editorial visual prompt, Bauhaus/Swiss technical minimalism, no text)
"""

def get_historical_learnings_section() -> str:
    """Reads historical rejection feedback to condition prompts against past mistakes."""
    if not LEARNINGS_FILE.exists():
        return ""
    try:
        with open(LEARNINGS_FILE, "r") as f:
            learnings = json.load(f)
        if not learnings:
            return ""
        
        lines = [
            "CRITICAL HISTORICAL FEEDBACK (DO NOT REPEAT PREVIOUS MISTAKES):",
            "The human reviewer previously rejected drafts with the following critiques. Strictly adhere to avoiding them:"
        ]
        for item in learnings[-5:]:
            critique = item.get("critique", "").strip()
            topic = item.get("topic", "")
            if critique:
                lines.append(f"- [Context: {topic}] Critique: {critique}")
        return "\n".join(lines) + "\n\n"
    except Exception:
        return ""

def clean_anti_slop(text: str) -> str:
    """Post-processing sanitizer ensuring zero em-dashes and minimal AI quirks."""
    cleaned = text.replace("—", ", ").replace("–", "-")
    for word in BANNED_WORDS:
        # Case insensitive replacement of banned buzzwords
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        if word in ["game-changer", "revolutionary", "transformative"]:
            cleaned = pattern.sub("significant development", cleaned)
        elif word in ["delve", "tapestry", "landscape"]:
            cleaned = pattern.sub("analysis", cleaned)
    return cleaned

def call_gemini(prompt: str, system_prompt: str = BASE_SYSTEM_PROMPT) -> Dict[str, Any]:
    """Call Google AI Studio / Gemini API."""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY / GOOGLE_AI_STUDIO_API_KEY not found in .env")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{DEFAULT_GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.4
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        candidate = res["candidates"][0]
        text = candidate["content"]["parts"][0]["text"]
        return json.loads(text)

def call_nvidia_fallback(prompt: str, system_prompt: str = BASE_SYSTEM_PROMPT) -> Dict[str, Any]:
    """Fallback call to NVIDIA NIM (Nemotron Bolt)."""
    if not NVIDIA_API_KEY:
        raise ValueError("NVIDIA_API_KEY not configured for fallback")

    url = f"{NVIDIA_BASE_URL}/chat/completions"
    payload = {
        "model": FALLBACK_NVIDIA_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt + "\nYou MUST reply with strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4,
        "max_tokens": 1800
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"].get("content", "").strip()
        if "```" in content:
            matches = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if matches:
                content = matches[0]
        return json.loads(content)

def generate_copywriting_package(research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generates the full multi-platform copywriting package conditioned with historical feedback."""
    learnings_section = get_historical_learnings_section()
    prompt = USER_PROMPT_TEMPLATE.format(
        title=research_data.get("title", ""),
        url=research_data.get("url", ""),
        published_date=research_data.get("published_date", ""),
        deep_content=research_data.get("deep_content", "")[:3500],
        learnings_section=learnings_section
    )
    
    package = None
    try:
        print("✍️  Step 3: Generating Copywriting with Gemini 2.5 Flash...")
        package = call_gemini(prompt)
    except Exception as e:
        print(f"  [Gemini Warning] {e}. Switching to NVIDIA Nemotron fallback...")
        try:
            package = call_nvidia_fallback(prompt)
        except Exception as e2:
            raise RuntimeError(f"Both primary and fallback LLMs failed: {e2}")

    # Sanitize outputs against em-dashes and AI slop
    for key in ["linkedin_copy", "instagram_copy", "facebook_copy", "core_insight"]:
        if key in package and isinstance(package[key], str):
            package[key] = clean_anti_slop(package[key])

    return package
