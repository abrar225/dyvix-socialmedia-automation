# Dyvix Technologies: Production Social Media Automation Context

This document defines the complete technical, operational, and visual standards for the autonomous Instagram and Facebook publishing engine operating at Dyvix Technologies Private Limited.

---

## 1. Company Profile & Strategic Overview

- **Legal Entity:** Dyvix Technologies Private Limited
- **Headquarters:** 503, Sakar-4, Near Ellisbridge, Ahmedabad, Gujarat 380006, India
- **Official Website:** https://dyvix.net/
- **Direct Contacts:** connect@dyvix.net | WhatsApp / Mobile: +91 92657 37568
- **Core Mission:** Strategic technology partner building scalable custom software, web and mobile apps, IoT integrations, AI workflow automations, and enterprise ERP/CRM tools.
- **Core Engineering Stack:** Next.js, React, React Native, Node.js, TypeScript, MongoDB, Redis, Cloudflare Edge Infrastructure.

---

## 2. Product Ecosystem (The 8 Live Platforms)

Every social post alternates between thought leadership in systems engineering and practical spotlights on Dyvix's proprietary software products:

1. **MsgMart (msgmart.dyvix.net):** Enterprise Bulk SMS Platform. Features smart queuing algorithms, template scheduling, and real-time delivery telemetry.
2. **Zeniflow (zeniflow.dyvix.net):** All-in-one HRMS and Payroll Suite. Features biometric shift tracking, automated payslip calculation, and internal operations CRM.
3. **BuyIndia (buyindia.net):** Verified B2B Marketplace. Features direct buyer-seller negotiation channels and escrow transaction safety.
4. **Apex Insurance Portal (insurance.dyvix.net):** Insurance Broker CRM. Manages policy lifecycles, automated renewals, and commission tracking.
5. **WheelFlow (wheelflow.dyvix.net):** Automobile Dealership Management System (2W and 4W). Handles lead tracking, inventory by model and color, and service logs.
6. **Trakify (trakify.dyvix.net):** Field Workforce Intelligence App. Live GPS breadcrumb tracking, geofenced client visits, and photo proof-of-work.
7. **Travel Desk ERP:** Travel Agency Management. Drag-and-drop tour itinerary compiler, vendor quotation aggregation, and installment invoices.
8. **FaktoryRun:** Pharmaceutical Factory Automation. Digital Batch Manufacturing Records (BMR), stage-by-stage regulatory sign-offs, and ingredient audit trails.

---

## 3. Brand Design System & Visual Tokens

All generated visual assets, editorial posters, and UI cards must adhere to the extracted brand identity from dyvix.net:

### Primary Color Palette
- **Primary Brand Red:** `#BD2727` (Logo icon, primary buttons, bold keyword highlights)
- **High-Key Accent Red:** `#E5463F` (Hover states, visual rim lighting, notification badges)
- **Canvas Obsidian:** `#141718` (Primary dark background canvas)
- **Container / Surface Dark:** `#1D2123` (Card modules, secondary borders)
- **Elevated Border:** `#252A2C` (Card dividers, coordinate grid marks)
- **Primary Text:** `#F3F4F4` (Headlines and high-contrast labels)
- **Muted Subtext:** `#A3AAAD` (Technical captions, specs, metadata)
- **System Success:** `#4ADE80` (Terminal state indicators, status tags)

### Typography Hierarchy
- **Display Headlines:** `Unbounded` (weights: 500, 700, 800)
- **Body Text:** `Lexend` (weights: 300, 400, 500, 600)
- **Monospace, Badges, Metrics:** `Advent Pro` (weights: 500, 600, 700)

---

## 4. Operational Publishing Architecture (Method 2: Headless Browser State)

The automation operates autonomously on the 24/7 cloud server using authenticated Playwright session state:

```
[Layer 1: Discovery & Research]
   - Tavily AI Search + Firecrawl Scraper
   - Discovers top daily AI and enterprise engineering breakthroughs

[Layer 2: Human-Writer Copywriting]
   - Conditioned on Dyvix product capabilities and media/learnings.json
   - Zero em-dashes, zero buzzwords, high burstiness
   - Dedicated Instagram caption (hook, 3 hyphenated takeaways, closing thought, hashtags)
   - Dedicated Facebook post (developer community discussion on technical friction)

[Layer 3: Dyvix 3D Visual Card Generation]
   - 4:5 vertical portrait framing (1080x1350)
   - Dyvix Obsidian (#141718) background with Crimson (#BD2727) accents
   - Anti-AI sanitization: EXIF purge, 2% micro-crop, sigma=1.2 Gaussian grain

[Layer 4: Human-in-the-Loop Review Engine]
   - Email dispatch to moabrarakhunji@gmail.com via Resend
   - Review Dashboard on port 5050
   - ACCEPT: Triggers Layer 5 browser publishing immediately
   - REJECT: Appends feedback to media/learnings.json, regenerates a new package, and re-notifies

[Layer 5: Automated Social Dispatch via Playwright]
   - Headless Chromium loads session from .auth/instagram-state.json and .auth/facebook-state.json
   - Uploads visual asset to Instagram and Facebook pages
   - Verifies post completion and logs permalink to history/
```

---

## 5. Non-Negotiable Editorial Rules

1. Zero em-dashes: Never use '—' or '–'. Use commas, colons, or standard periods.
2. Zero AI buzzwords: Never use 'delve', 'tapestry', 'landscape', 'beacon', 'crucial', 'vital', 'elevate', 'supercharge', 'game-changer', 'revolutionary', 'paradigm shift', 'seamless'.
3. High burstiness: Mix short 4-word punchy statements with detailed 25-word technical clauses.
4. Zero emoji ladders: Use standard hyphens (-) for bulleted lists.
5. Brand compliance: Reflect Dyvix's engineering authority as an established Ahmedabad software firm.
