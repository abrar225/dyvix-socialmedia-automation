"""
Layer 3: Dual-Mode Visual Generation & Anti-AI Sanitization Engine
Creates 1080x1350 (4:5 portrait) high-aesthetic visuals for Instagram & LinkedIn.

Two Core Operational Modes:
1. Architecture Blueprint: Precision systems schematics, obsidian canvas, data-flow vectors.
2. Whiteboard Sketch (Excalidraw Style): Hand-drawn sketch aesthetic, organic stroke notes, mental model diagrams.

All modes strictly enforce anti-AI sanitization:
- Complete stripping of EXIF and C2PA metadata
- 2% subtle center micro-crop to dissolve neural grid markers
- Micro-film Gaussian noise injection (sigma ~ 1.4)
"""
import io
import math
import random
import urllib.parse
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from core.config import (
    IMAGE_WIDTH,
    IMAGE_HEIGHT,
    POLLINATIONS_BASE_URL
)

def apply_anti_ai_noise(img: Image.Image, sigma: float = 1.4) -> Image.Image:
    """Injects micro-film Gaussian noise to break neural watermarks and AI classifiers."""
    arr = np.array(img, dtype=np.float32)
    noise = np.random.normal(0, sigma, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)

def render_blueprint_card(
    title: str,
    subtitle: str,
    pillars: list,
    output_path: str
) -> str:
    """
    Mode A: Dyvix System Architecture Blueprint
    Obsidian canvas (#141718), Dyvix Crimson (#BD2727) accents, precision Cartesian grid, dataflow schema boxes.
    """
    W, H = IMAGE_WIDTH, IMAGE_HEIGHT
    img = Image.new('RGB', (W, H), color=(20, 23, 24))  # Dyvix Canvas Obsidian (#141718)
    draw = ImageDraw.Draw(img)

    # 1. Coordinate Grid
    for x in range(0, W, 45):
        draw.line([(x, 0), (x, H)], fill=(29, 33, 35), width=1)
    for y in range(0, H, 45):
        draw.line([(0, y), (W, y)], fill=(29, 33, 35), width=1)

    # 2. Outer Technical Border with Corner Crosshairs
    draw.rounded_rectangle([45, 45, W - 45, H - 45], radius=20, outline=(37, 42, 44), width=2)
    # Corner markers in Dyvix Crimson
    for cx, cy in [(45, 45), (W - 45, 45), (45, H - 45), (W - 45, H - 45)]:
        draw.line([(cx - 8, cy), (cx + 8, cy)], fill=(189, 39, 39), width=2)
        draw.line([(cx, cy - 8), (cx, cy + 8)], fill=(189, 39, 39), width=2)

    # 3. Dyvix Header Tag
    draw.rounded_rectangle([90, 95, 460, 145], radius=10, fill=(29, 33, 35), outline=(189, 39, 39), width=1)
    draw.text((115, 112), "[DYVIX TECHNOLOGIES // SPEC 2026]", fill=(229, 70, 63))

    # 4. Main Titles
    draw.text((90, 180), title[:40], fill=(243, 244, 244))
    draw.text((90, 230), subtitle[:55], fill=(163, 170, 173))

    # 5. Data Flow Connection Track
    track_x = 135
    draw.line([(track_x, 340), (track_x, 340 + 3 * 220)], fill=(37, 42, 44), width=3)

    # 6. Structured Architecture Nodes (3 Pillars)
    y_pos = 330
    for i, item in enumerate(pillars[:3]):
        p_title = item.get("title", "") if isinstance(item, dict) else str(item[0])
        p_desc = item.get("desc", "") if isinstance(item, dict) else str(item[1])
        
        # Node Connection Indicator
        draw.ellipse([track_x - 8, y_pos + 40, track_x + 8, y_pos + 56], fill=(189, 39, 39), outline=(20, 23, 24), width=2)

        # Node Card
        draw.rounded_rectangle([175, y_pos, W - 90, y_pos + 185], radius=14, fill=(29, 33, 35), outline=(37, 42, 44), width=1)
        
        # Micro Stage Tag
        stage_text = f"NODE 0{i+1} // {p_title[:28]}"
        draw.text((205, y_pos + 26), stage_text, fill=(229, 70, 63))
        draw.text((205, y_pos + 72), p_desc[:110], fill=(243, 244, 244))
        
        # Micro Technical Specs
        draw.text((W - 270, y_pos + 26), "STATE: BOUNDED", fill=(74, 222, 128))
        
        y_pos += 225

    # 7. Bottom Blueprint Verification Footer
    draw.line([(90, H - 130), (W - 90, H - 130)], fill=(37, 42, 44), width=1)
    draw.text((90, H - 100), "VERIFIED PRODUCTION BLUEPRINT // LATENCY CRITICAL", fill=(163, 170, 173))
    draw.text((W - 370, H - 100), "DYVIX TECHNOLOGIES // dyvix.net", fill=(229, 70, 63))

    # Anti-AI micro-film noise injection
    clean_img = apply_anti_ai_noise(img, sigma=1.2)
    clean_img.save(output_path, format="JPEG", quality=95, optimize=True)
    return output_path

def render_sketch_card(
    title: str,
    subtitle: str,
    pillars: list,
    output_path: str
) -> str:
    """
    Mode B: Handwritten Whiteboard Sketch (Excalidraw Style)
    Dark chalk slate canvas, multi-stroke jittered boxes, hand-annotated sketch notes.
    """
    W, H = IMAGE_WIDTH, IMAGE_HEIGHT
    img = Image.new('RGB', (W, H), color=(20, 23, 24))  # Dyvix Dark Slate Board
    draw = ImageDraw.Draw(img)

    # 1. Subtle Whiteboard Stipple Texture
    for _ in range(120):
        rx, ry = random.randint(30, W - 30), random.randint(30, H - 30)
        draw.point((rx, ry), fill=(29, 33, 35))

    # 2. Organic Hand-Drawn Outer Frame (Double Jittered Stroke)
    box = [50, 50, W - 50, H - 50]
    draw.rounded_rectangle([box[0] - 1, box[1] + 1, box[2] + 1, box[3] - 1], radius=24, outline=(37, 42, 44), width=2)
    draw.rounded_rectangle([box[0] + 1, box[1] - 1, box[2] - 1, box[3] + 1], radius=24, outline=(29, 33, 35), width=1)

    # 3. Hand-Annotated Header Badge
    draw.rounded_rectangle([90, 95, 460, 145], radius=16, fill=(29, 33, 35), outline=(189, 39, 39), width=1)
    draw.text((115, 112), "// DYVIX SYSTEMS // MENTAL MODEL", fill=(229, 70, 63))

    # 4. Whiteboard Headings
    draw.text((90, 180), title[:40], fill=(243, 244, 244))
    draw.text((90, 230), subtitle[:55], fill=(163, 170, 173))

    # 5. Hand-Drawn Arrow Connectors
    y_pos = 330
    for i, item in enumerate(pillars[:3]):
        p_title = item.get("title", "") if isinstance(item, dict) else str(item[0])
        p_desc = item.get("desc", "") if isinstance(item, dict) else str(item[1])

        # Dual jittered stroke for organic sketch feel
        card_box = [90, y_pos, W - 90, y_pos + 185]
        draw.rounded_rectangle([card_box[0], card_box[1], card_box[2], card_box[3]], radius=18, fill=(29, 33, 35), outline=(37, 42, 44), width=2)
        draw.rounded_rectangle([card_box[0] + 1, card_box[1] - 1, card_box[2] - 1, card_box[3] + 1], radius=18, outline=(29, 33, 35), width=1)

        # Hand-annotated callout badge
        badge_text = f"STEP {i+1} -> {p_title[:30]}"
        draw.text((120, y_pos + 26), badge_text, fill=(74, 222, 128))
        draw.text((120, y_pos + 72), p_desc[:115], fill=(243, 244, 244))

        # Sketch hand-drawn arrow between cards
        if i < 2:
            arrow_y = y_pos + 195
            draw.line([(W // 2, arrow_y), (W // 2, arrow_y + 20)], fill=(189, 39, 39), width=2)
            draw.line([(W // 2 - 6, arrow_y + 14), (W // 2, arrow_y + 20)], fill=(189, 39, 39), width=2)
            draw.line([(W // 2 + 6, arrow_y + 14), (W // 2, arrow_y + 20)], fill=(189, 39, 39), width=2)

        y_pos += 230

    # 6. Sketch Footer
    draw.line([(90, H - 130), (W - 90, H - 130)], fill=(37, 42, 44), width=1)
    draw.text((90, H - 100), "// SKETCHED FOR DYVIX SYSTEMS REVIEW", fill=(163, 170, 173))
    draw.text((W - 350, H - 100), "DYVIX TECHNOLOGIES // dyvix.net", fill=(229, 70, 63))

    # Anti-AI micro-film noise injection
    clean_img = apply_anti_ai_noise(img, sigma=1.2)
    clean_img.save(output_path, format="JPEG", quality=95, optimize=True)
    return output_path

def sanitize_external_image(raw_bytes: bytes) -> bytes:
    """Strips EXIF, enforces 1080x1350 bounds, applies 2% micro-crop, and adds micro-film grain."""
    with Image.open(io.BytesIO(raw_bytes)) as img:
        img = ImageOps.exif_transpose(img)
        img = img.convert("RGB")
        img = ImageOps.fit(img, (IMAGE_WIDTH, IMAGE_HEIGHT), method=Image.Resampling.LANCZOS)
        
        # 2% subtle center crop
        crop_x = int(IMAGE_WIDTH * 0.01)
        crop_y = int(IMAGE_HEIGHT * 0.01)
        cropped = img.crop((crop_x, crop_y, IMAGE_WIDTH - crop_x, IMAGE_HEIGHT - crop_y))
        resized = cropped.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.Resampling.LANCZOS)
        
        clean_img = apply_anti_ai_noise(resized, sigma=1.5)
        out_buf = io.BytesIO()
        clean_img.save(out_buf, format="JPEG", quality=92, optimize=True)
        return out_buf.getvalue()

def fetch_pollinations_visual(prompt: str, output_path: str) -> str:
    """Fetches image from Pollinations.ai and sanitizes it."""
    encoded_prompt = urllib.parse.quote(prompt[:250])
    url = f"{POLLINATIONS_BASE_URL}/{encoded_prompt}?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&model=flux&nologo=true"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; SocialMediaEngine/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        clean_bytes = sanitize_external_image(resp.read())
        
    with open(output_path, "wb") as f:
        f.write(clean_bytes)
    return output_path

def build_nano_banana_prompt(title: str, subtitle: str, core_insight: str, pillars: list) -> str:
    """
    Constructs a world-class 3D Octane/Cinema 4D prompt based on CreativeClout & Peakpath reference aesthetics.
    Features: First-person POV, human and cyborg cybernetic hands, glowing retro CRT/arcade screen,
    floating glossy badges, neon lime green / electric ultraviolet rim lighting on obsidian canvas.
    """
    topic_clean = title.replace('"', '').strip()
    return f'''Create an award-winning, state-of-the-art 3D commercial tech poster in 4:5 vertical portrait orientation (1080x1350).

VISUAL CONCEPT & ART DIRECTION:
- Subject: A cinematic, high-end 3D composition representing the Dyvix engineering breakthrough: "{topic_clean}".
- Center 3D Hero: A sleek, retro-futuristic computing workstation or server console. In first-person perspective, two highly detailed hands are interacting with the controls: on the left, an authentic human hand, on the right, a precision-machined glossy black and chrome robotic cyborg hand with glowing Dyvix Crimson (#BD2727) joint indicators.
- Display & Screen: The monitor emits a vivid Dyvix crimson and subtle cyan glow, displaying modular nodes, real-time data flows, and telemetry.
- Environment & Lighting: Deep obsidian dark background (#141718) with subtle Cartesian floor wireframe lines. Atmospheric volumetric haze, sharp rim light reflecting off the chrome robotic knuckles, glass, and brushed aluminum.
- Accents & Tactile Details: Floating glossy 3D badge pins reading "DYVIX // 2026", tactile switches, and realistic cast shadows.
- Render Caliber: Photorealistic 3D Octane Render / Redshift / Cinema 4D quality, physically based materials, raytraced reflections, authentic depth of field (f/2.8).
- Composition: 4:5 vertical framing. Clean, high-impact commercial studio finish that instantly commands attention on Instagram and Facebook. No blurry low-res artifacts or distorted anatomy.'''

def determine_visual_mode(title: str, subtitle: str, pillars: list) -> str:
    """
    Intelligently determines whether topic fits Blueprint or Whiteboard Sketch:
    - Structural frameworks, hardware, infrastructure, data-flow -> Blueprint
    - Mental models, productivity, heuristics, developer friction -> Whiteboard Sketch
    """
    text_corpus = f"{title} {subtitle} {' '.join([p.get('desc', '') if isinstance(p, dict) else str(p) for p in pillars])}".lower()
    sketch_signals = [
        "productivity", "mental model", "developer", "friction", "perception",
        "heuristic", "workflow", "team", "bias", "speed", "sentiment", "experience"
    ]
    blueprint_signals = [
        "architecture", "infrastructure", "pipeline", "cluster", "gpu",
        "inference", "model", "latency", "schema", "node", "storage", "spec"
    ]

    sketch_score = sum(1 for w in sketch_signals if w in text_corpus)
    blueprint_score = sum(1 for w in blueprint_signals if w in text_corpus)

    if sketch_score > blueprint_score:
        return "whiteboard_sketch"
    return "blueprint"

def create_visual(
    title: str,
    subtitle: str,
    pillars: list,
    prompt: str,
    output_path: str,
    visual_mode: str = "auto",
    use_diffusion: bool = False
) -> str:
    """Master visual entrypoint supporting Dual-Mode (Blueprint vs Whiteboard Sketch)."""
    if use_diffusion:
        try:
            print("🎨 Generating diffusion visual via Pollinations.ai...")
            return fetch_pollinations_visual(prompt, output_path)
        except Exception as e:
            print(f"  [Diffusion Notice] {e}. Falling back to high-aesthetic dual-mode card.")

    selected_mode = visual_mode
    if selected_mode == "auto":
        selected_mode = determine_visual_mode(title, subtitle, pillars)

    if selected_mode == "whiteboard_sketch":
        print("🎨 Rendering 1080x1350 Handwritten Whiteboard Sketch Card (Excalidraw Style)...")
        return render_sketch_card(title, subtitle, pillars, output_path)
    else:
        print("🎨 Rendering 1080x1350 System Architecture Blueprint Card...")
        return render_blueprint_card(title, subtitle, pillars, output_path)
