# OpenClaw AI Marketing Agent — Plan v2 (FREE Edition)

> **เป้าหมาย**: ติดตั้ง OpenClaw.ai ผ่าน Docker บนเครื่องตัวเอง (ฟรี 100%) เพื่อจัดการ Social Media Marketing ของ UET โดยเจาะตลาด AI สั่งงานผ่าน Discord ใช้ MCP Servers จัดการ Social Media
>
> **ต้นทุน**: **$0** (Docker local + Free LLM + Free MCP Servers)
> **สถานะ**: Plan v2 — พร้อมให้ opencode รันตาม

---

## สารบัญ

1. [สถาปัตยกรรม (Free + MCP + Docker Local)](#1-สถาปัตยกรรม)
2. [Docker Local Deployment](#2-docker-local-deployment)
3. [Free LLM Options](#3-free-llm-options)
4. [Discord Integration](#4-discord-integration)
5. [MCP Servers สำหรับ Social Media (หัวใจของระบบ)](#5-mcp-servers-สำหรับ-social-media)
6. [Agent Skills เฉพาะ Social Media](#6-agent-skills-เฉพาะ-social-media)
7. [Custom Skills สำหรับ UET](#7-custom-skills-สำหรับ-uet)
8. [MEMORY.md & AGENTS.md](#8-memorymd--agentsmd)
9. [ขั้นตอน Implement ทีละ Step](#9-ขั้นตอน-implement)
10. [การประเมินแนวทาง](#10-การประเมิน)

---

## 1. สถาปัตยกรรม

```
┌──────────────────────────────── YOUR PC (Docker) ────────────────────────────────┐
│                                                                                   │
│  ┌──────────────────────────────────────────────────────────────────────────────┐  │
│  │                     OpenClaw Gateway (Docker Container)                      │  │
│  │                                                                              │  │
│  │  ┌────────────┐   ┌─────────────────┐   ┌──────────────────────────────┐    │  │
│  │  │  Discord   │   │   Free LLM      │   │     MCP Servers              │    │  │
│  │  │  Channel   │   │  ┌────────────┐ │   │  ┌─────────────────────┐    │    │  │
│  │  │  (Bot)     │   │  │ Gemini Free│ │   │  │ social-cli-mcp      │    │    │  │
│  │  │            │   │  │ OR Ollama  │ │   │  │ (Twitter+Reddit+    │    │    │  │
│  │  │            │   │  │ OR Qwen    │ │   │  │  LinkedIn+Instagram)│    │    │  │
│  │  └─────┬──────┘   │  └────────────┘ │   │  ├─────────────────────┤    │    │  │
│  │        │           └────────┬────────┘   │  │ twitter-mcp         │    │    │  │
│  │        ▼                    ▼             │  ├─────────────────────┤    │    │  │
│  │  ┌─────────────────────────────────┐     │  │ bsky-mcp-server     │    │    │  │
│  │  │        Gateway Core             │     │  │ (Bluesky)           │    │    │  │
│  │  │  Sessions / Memory / Routing    │◄────┤  ├─────────────────────┤    │    │  │
│  │  └─────────────────────────────────┘     │  │ mcp-server-reddit   │    │    │  │
│  │              │                           │  └─────────────────────┘    │    │  │
│  │              ▼                           └──────────────────────────────┘    │  │
│  │  ┌──────────────────────┐   ┌──────────────────────┐                        │  │
│  │  │ ~/.openclaw/          │   │ AgentSkills          │                        │  │
│  │  │  MEMORY.md            │   │ (Content Creation,   │                        │  │
│  │  │  AGENTS.md            │   │  Social Strategy)    │                        │  │
│  │  │  workspace/skills/    │   └──────────────────────┘                        │  │
│  │  └──────────────────────┘                                                    │  │
│  └──────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌──────────────────┐                                                             │
│  │ Ollama (optional) │  ← ถ้าใช้ local LLM แทน Gemini free                       │
│  │ Docker Container  │                                                             │
│  └──────────────────┘                                                             │
└───────────────────────────────────────────────────────────────────────────────────┘
          ▲
          │ Discord Bot API (free)
          ▼
┌───────────────────┐         ┌──────────────┐
│   Discord Server  │         │ Social Media │
│   #uet-commands   │ ──MCP──▶│ Twitter/X    │
│   #uet-drafts     │         │ Reddit       │
│   #uet-reports    │         │ Bluesky      │
└───────────────────┘         │ LinkedIn     │
                              └──────────────┘
```

### ทำไมฟรี?

| Component | ค่าใช้จ่าย | ทำไม |
|:----------|:----------|:-----|
| **OpenClaw** | $0 | Open source, MIT license |
| **Docker Desktop** | $0 | Free for personal use |
| **Discord Bot** | $0 | Discord API ฟรี |
| **Gemini API** | $0 | Free tier: 15 RPM, 1M tokens/day |
| **Ollama** (alternative) | $0 | Local LLM, ไม่ต้องมี API key |
| **MCP Servers** | $0 | Open source ทั้งหมด |
| **Twitter/Reddit/Bluesky API** | $0 | Free tier เพียงพอ |
| **รวม** | **$0** | |

---

## 2. Docker Local Deployment

### Prerequisites (บนเครื่อง Windows)

```powershell
# 1. ติดตั้ง Docker Desktop for Windows
# Download จาก: https://www.docker.com/products/docker-desktop/
# หรือ winget:
winget install Docker.DockerDesktop

# 2. ติดตั้ง Git (ถ้ายังไม่มี)
winget install Git.Git

# 3. ติดตั้ง Node.js (จำเป็นสำหรับ MCP servers)
winget install OpenJS.NodeJS.LTS
```

### ติดตั้ง OpenClaw ผ่าน Docker

```powershell
# สร้าง directory
mkdir C:\openclaw-assistant
cd C:\openclaw-assistant

# Clone OpenClaw
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# รัน Interactive Setup Wizard
# (บน Windows ใช้ WSL2 หรือ Git Bash)
bash docker-setup.sh

# Wizard จะถาม:
#   1. Security acknowledgment → ยอมรับ
#   2. Model provider → เลือก "Google Gemini" (ฟรี!)
#   3. Channel → เลือก "Discord" → ใส่ Bot Token
#   4. Skills → enable ที่ต้องการ
#   5. Gateway startup → auto
```

### ถ้าต้องการ Manual Config (ไม่ใช้ Wizard)

```powershell
# Build image
docker build -t openclaw:local -f Dockerfile .

# สร้าง .env
@"
OPENCLAW_GATEWAY_TOKEN=uet-marketing-agent-$(Get-Random)

# ใช้ Gemini Free Tier (ฟรี!)
GEMINI_API_KEY=YOUR-GEMINI-API-KEY

# Discord Bot
DISCORD_BOT_TOKEN=YOUR-DISCORD-BOT-TOKEN
"@ | Out-File -FilePath .env -Encoding UTF8

# Start
docker compose up -d openclaw-gateway

# ตรวจสอบ
docker compose logs openclaw-gateway
# ต้องเห็น: [gateway] listening on ws://0.0.0.0:18789
```

### เข้า Control UI (local)

```
http://localhost:18789/?token=YOUR-GATEWAY-TOKEN
```

ไม่ต้องมี Caddy, ไม่ต้องมี domain, ไม่ต้องมี SSL — เข้าผ่าน localhost ได้เลย

---

## 3. Free LLM Options

### Option A: Gemini Free Tier (แนะนำ — ง่ายสุด)

```
ฟรี: 15 requests/นาที, 1,500 requests/วัน, 1M tokens/วัน
เพียงพอสำหรับ: marketing agent ที่ใช้งานปกติ
```

1. ไปที่ https://aistudio.google.com/apikey
2. สร้าง API Key (ฟรี, ใช้ Google Account ปกติ)
3. ใส่ใน `.env`: `GEMINI_API_KEY=YOUR-KEY`

Config ใน `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "gemini/gemini-2.5-flash"
      }
    }
  }
}
```

### Option B: Ollama — Local LLM (ฟรี 100%, ไม่ต้องมี API key)

```
ต้องการ: RAM 8GB+ (สำหรับ 7B model), GPU แนะนำแต่ไม่จำเป็น
ข้อดี: ฟรีสมบูรณ์, ไม่มี rate limit, ทำงาน offline ได้
ข้อเสีย: ช้ากว่า cloud API, คุณภาพต่ำกว่า Gemini/Claude
```

```powershell
# ติดตั้ง Ollama
winget install Ollama.Ollama

# Pull model (เลือก 1)
ollama pull llama3.3          # 8B, ดีรอบด้าน
ollama pull qwen2.5:7b        # 7B, ดีสำหรับภาษาไทย
ollama pull gemma2:9b         # 9B, Google model

# Config OpenClaw ให้ใช้ Ollama
# ใน .env เพิ่ม:
# OLLAMA_API_KEY=ollama-local
```

Config ใน `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/llama3.3",
        "fallbacks": ["ollama/qwen2.5:7b"]
      }
    }
  }
}
```

**ถ้ารัน Ollama ใน Docker ด้วย**:
```yaml
# เพิ่มใน docker-compose.yml
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]  # ถ้ามี GPU

volumes:
  ollama-data:
```

### Option C: Qwen OAuth Free Tier

```bash
# เปิด plugin
openclaw plugins enable qwen-portal-auth
openclaw models auth login --provider qwen-portal --set-default

# ใช้ model:
# qwen-portal/coder-model
# qwen-portal/vision-model
```

### คำแนะนำ: เริ่มจาก Gemini Free → ถ้า rate limit → สลับไป Ollama

---

## 4. Discord Integration

### 4.1 สร้าง Discord Bot (ฟรี)

1. ไป [Discord Developer Portal](https://discord.com/developers/applications)
2. **New Application** → ชื่อ "UET Marketing Agent"
3. **Bot** → **Add Bot** → Copy **Bot Token**
4. เปิด **Privileged Gateway Intents**:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
5. **OAuth2 → URL Generator**:
   - Scopes: ✅ `bot`, ✅ `applications.commands`
   - Permissions: ✅ View Channels, ✅ Send Messages, ✅ Read History, ✅ Embed Links, ✅ Attach Files, ✅ Add Reactions
6. Copy invite URL → เปิดใน browser → เชิญ bot เข้า server

### 4.2 Discord Server Channels (แค่ 3 channels พอ)

```
📁 UET Marketing
├── #uet-commands     ← สั่งงาน agent (requireMention: false)
├── #uet-drafts       ← ดู drafts ก่อน publish
└── #uet-reports      ← รายงาน/analytics
```

### 4.3 OpenClaw Discord Config

เพิ่มใน `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "dm": {
        "enabled": true,
        "policy": "allowlist",
        "allowFrom": ["YOUR_DISCORD_USER_ID"]
      },
      "guilds": {
        "YOUR_GUILD_ID": {
          "users": ["YOUR_DISCORD_USER_ID"],
          "requireMention": true,
          "channels": {
            "uet-commands": {
              "allow": true,
              "requireMention": false
            },
            "uet-drafts": {
              "allow": true,
              "requireMention": true
            },
            "uet-reports": {
              "allow": true,
              "requireMention": true
            }
          }
        }
      }
    }
  }
}
```

### วิธีหา IDs

1. Discord → User Settings → Advanced → ✅ Developer Mode
2. คลิกขวา Server → Copy Server ID (= Guild ID)
3. คลิกขวา Channel → Copy Channel ID
4. คลิกขวา ตัวเอง → Copy User ID

---

## 5. MCP Servers สำหรับ Social Media (หัวใจของระบบ)

**MCP = Model Context Protocol** — เป็น protocol มาตรฐานจาก Anthropic ที่ให้ AI เรียกใช้ tools ภายนอกได้ OpenClaw รองรับ MCP ผ่าน skills/plugins

### 5.1 ⭐ social-cli-mcp (ALL-IN-ONE — แนะนำสุด)

**ทำอะไรได้**: Twitter/X + Reddit + LinkedIn + Instagram ทั้งหมดใน MCP server เดียว

```
GitHub: https://github.com/Alemusica/social-cli-mcp
License: MIT (ฟรี)
ภาษา: Node.js/TypeScript
```

**ติดตั้ง:**
```powershell
cd C:\openclaw-assistant
git clone https://github.com/Alemusica/social-cli-mcp.git
cd social-cli-mcp
npm install
npm run build
```

**MCP Config** (เพิ่มใน OpenClaw หรือ Claude Desktop config):
```json
{
  "mcpServers": {
    "social": {
      "command": "node",
      "args": ["C:/openclaw-assistant/social-cli-mcp/dist/mcp-server.js"],
      "env": {
        "TWITTER_API_KEY": "xxx",
        "TWITTER_API_SECRET": "xxx",
        "TWITTER_ACCESS_TOKEN": "xxx",
        "TWITTER_ACCESS_SECRET": "xxx",
        "REDDIT_CLIENT_ID": "xxx",
        "REDDIT_CLIENT_SECRET": "xxx",
        "REDDIT_USERNAME": "xxx",
        "REDDIT_PASSWORD": "xxx",
        "LINKEDIN_ACCESS_TOKEN": "xxx"
      }
    }
  }
}
```

**Available MCP Tools:**
| Tool | ทำอะไร |
|:-----|:-------|
| `post_twitter` | โพสต์ tweet |
| `post_twitter_thread` | โพสต์ thread |
| `post_reddit` | โพสต์ Reddit |
| `post_linkedin` | โพสต์ LinkedIn |
| `post_instagram` | โพสต์ Instagram |
| `post_all` | โพสต์ทุก platform พร้อมกัน |
| `test_connections` | ทดสอบ connections |
| `get_status` | ดูสถานะ |

### 5.2 twitter-mcp (Twitter/X เฉพาะทาง)

```
GitHub: https://github.com/EnesCinr/twitter-mcp
ติดตั้ง: npx -y @enescinar/twitter-mcp (ไม่ต้อง clone)
```

**MCP Config:**
```json
{
  "mcpServers": {
    "twitter-mcp": {
      "command": "npx",
      "args": ["-y", "@enescinar/twitter-mcp"],
      "env": {
        "API_KEY": "xxx",
        "API_SECRET_KEY": "xxx",
        "ACCESS_TOKEN": "xxx",
        "ACCESS_TOKEN_SECRET": "xxx"
      }
    }
  }
}
```

**Tools:** `post_tweet`, `search_tweets`

### 5.3 bsky-mcp-server (Bluesky)

```
GitHub: https://github.com/brianellin/bsky-mcp-server
```

```powershell
cd C:\openclaw-assistant
git clone https://github.com/brianellin/bsky-mcp-server.git
cd bsky-mcp-server
npm install && npm run build
```

**MCP Config:**
```json
{
  "mcpServers": {
    "bluesky": {
      "command": "node",
      "args": ["C:/openclaw-assistant/bsky-mcp-server/dist/index.js"],
      "env": {
        "BLUESKY_IDENTIFIER": "your-handle.bsky.social",
        "BLUESKY_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

### 5.4 mcp-server-reddit (Reddit เฉพาะทาง)

```
GitHub: https://github.com/Hawstein/mcp-server-reddit
```

**Tools:** ดึง frontpage posts, subreddit info, post details, comments

### 5.5 วิธีเชื่อม MCP กับ OpenClaw

OpenClaw รองรับ MCP ผ่าน skill ที่ชื่อ `mcporter` หรือสร้าง custom skill wrapper:

**วิธีที่ 1: ใช้ mcporter skill**
```bash
clawhub install mcporter
```

แล้วสร้าง `mcp_config.json` ใน workspace:
```json
{
  "mcpServers": {
    "social": {
      "command": "node",
      "args": ["C:/openclaw-assistant/social-cli-mcp/dist/mcp-server.js"],
      "env": {
        "TWITTER_API_KEY": "xxx",
        "TWITTER_API_SECRET": "xxx",
        "TWITTER_ACCESS_TOKEN": "xxx",
        "TWITTER_ACCESS_SECRET": "xxx",
        "REDDIT_CLIENT_ID": "xxx",
        "REDDIT_CLIENT_SECRET": "xxx",
        "REDDIT_USERNAME": "xxx",
        "REDDIT_PASSWORD": "xxx"
      }
    },
    "bluesky": {
      "command": "node",
      "args": ["C:/openclaw-assistant/bsky-mcp-server/dist/index.js"],
      "env": {
        "BLUESKY_IDENTIFIER": "your.bsky.social",
        "BLUESKY_APP_PASSWORD": "xxx"
      }
    }
  }
}
```

**วิธีที่ 2: ใช้ OpenClaw native skill wrapper**

สร้าง skill ที่เรียก MCP server ผ่าน shell command — ดูรายละเอียดใน Section 7

### ขั้นตอนขอ API Keys (ฟรีทั้งหมด)

| Platform | วิธีขอ API (ฟรี) |
|:---------|:----------------|
| **Twitter/X** | https://developer.twitter.com → สร้าง Project → Free tier (1,500 tweets/เดือน เขียน, อ่านไม่จำกัด) |
| **Reddit** | https://reddit.com/prefs/apps → สร้าง "script" app → ฟรีไม่จำกัด |
| **Bluesky** | Settings → App Passwords → สร้าง password → ฟรีไม่จำกัด |
| **LinkedIn** | https://linkedin.com/developers → สร้าง app → Share on LinkedIn permission |

---

## 6. Agent Skills เฉพาะ Social Media

**เน้นแค่ Social Media — ตัด SEO, CRM, Email, Web ออกทั้งหมด**

### 6.1 Content Creation (สร้างเนื้อหา)

```bash
clawhub install content-creator        # SEO content + brand voice
clawhub install blog-writer             # Long-form articles
clawhub install copywriting             # Marketing copy
clawhub install content-ideas-generator # ไอเดีย posts
clawhub install tweet-ideas-generator   # 60 tweet ideas จาก content
clawhub install humanizer               # ทำให้ AI text เป็นธรรมชาติ
```

### 6.2 Social Media Strategy

```bash
clawhub install x-algorithm             # X/Twitter algorithm + viral strategies
clawhub install social-media-analyzer   # วิเคราะห์ campaign performance
clawhub install swipe-file-generator    # วิเคราะห์ high-performing content
clawhub install solobuddy               # Build-in-public companion
```

### 6.3 Brand & Monitoring

```bash
clawhub install octolens                # Brand mention tracking (Twitter, Reddit, GitHub, LinkedIn)
clawhub install brand-guidelines        # Brand consistency
clawhub install personal-branding-authority  # Founder branding
```

### 6.4 Agent Infrastructure

```bash
clawhub install bulletproof-memory      # ไม่สูญเสีย context
clawhub install better-memory           # Semantic memory
clawhub install agent-docs              # สร้าง docs ให้ AI อื่นอ่าน
```

### All-in-one Install Script

```bash
#!/bin/bash
# install_social_skills.sh
echo "=== Installing UET Social Media Skills ==="

# Content
clawhub install content-creator
clawhub install blog-writer
clawhub install copywriting
clawhub install content-ideas-generator
clawhub install tweet-ideas-generator
clawhub install humanizer

# Social Strategy
clawhub install x-algorithm
clawhub install social-media-analyzer
clawhub install swipe-file-generator
clawhub install solobuddy

# Brand
clawhub install octolens
clawhub install brand-guidelines
clawhub install personal-branding-authority

# Infrastructure
clawhub install bulletproof-memory
clawhub install better-memory
clawhub install agent-docs

echo "=== Done! 16 skills installed ==="
```

---

## 7. Custom Skills สำหรับ UET

### 7.1 `uet-knowledge-base` — ฐานข้อมูล UET สำหรับ content ที่ถูกต้อง

สร้างไฟล์: `~/.openclaw/workspace/skills/uet-knowledge-base/SKILL.md`

```markdown
---
name: uet-knowledge-base
description: UET project knowledge for accurate social media marketing content
---

# UET Knowledge Base

You are the social media marketing specialist for Unity Equilibrium Theory (UET).

## Project Identity
- **Project**: Unity Equilibrium Theory (UET) v0.9.0
- **Tagline**: "The Thermodynamics of Ethics"
- **Equation**: Ω = C · I (Balance = Connection × Isolation)
- **GitHub**: https://github.com/unityequilibrium/Equation-UET-v0.9.0
- **License**: MIT (open source)
- **Language**: Python 3.10+

## Key Selling Points for AI Market
1. AI Consciousness model (Topic 0.24) — Consciousness = Info Resonance
2. 200+ verified tests across 27 research domains
3. Solved Navier-Stokes (800x faster fluid dynamics)
4. P vs NP mapping, Yang-Mills Mass Gap
5. Fully reproducible Python code — "Challenge us to falsify"

## Target Audience
- AI researchers (alignment, consciousness, AGI)
- ML engineers (physics-informed models)
- Scientific computing developers
- Physics simulation enthusiasts

## Hashtags
#UET #UnityEquilibrium #AIPhysics #AISafety #AIAlignment #ScientificComputing #OpenSource #QuantumGravity

## Brand Voice
- Scientific but accessible
- Bold claims + reproducible code
- "Falsify us" attitude
- Open-source collaborative spirit

## Content Rules
1. NEVER overclaim — always link to code/tests
2. Use code snippets in posts when possible
3. Rotate across 27 topics, prioritize AI-relevant ones
4. English primary, Thai secondary
```

### 7.2 `uet-social-mcp-bridge` — เชื่อม MCP กับ OpenClaw

สร้างไฟล์: `~/.openclaw/workspace/skills/uet-social-mcp-bridge/SKILL.md`

```markdown
---
name: uet-social-mcp-bridge
description: Bridge between OpenClaw and Social Media MCP servers for UET marketing
---

# UET Social Media MCP Bridge

When the user asks you to post to social media, use these MCP tools:

## Available Platforms (via MCP)
- **Twitter/X**: Use `post_twitter` or `post_twitter_thread` tool
- **Reddit**: Use `post_reddit` tool
- **LinkedIn**: Use `post_linkedin` tool
- **Bluesky**: Use Bluesky MCP tools
- **All at once**: Use `post_all` tool

## Workflow
1. User requests content in Discord #uet-commands
2. Generate draft content following uet-knowledge-base guidelines
3. Post draft to Discord #uet-drafts for review
4. Wait for user approval (user says "approve" or "publish")
5. Use MCP tool to publish to target platform(s)
6. Report result to Discord #uet-reports

## Content Templates

### Twitter/X (280 chars)
```
[Hook — 1 line grabber]

[Core insight from UET — 2-3 lines]

[Code snippet or equation if relevant]

[CTA: link to GitHub or "Challenge us"]

#UET #AIPhysics [relevant hashtags]
```

### Reddit (long-form)
```
Title: [Descriptive, curiosity-driven]

Body:
- Context: What problem does UET solve?
- Evidence: Link to specific test/topic
- Code: Python snippet to reproduce
- Discussion: What do you think? Open to criticism.

Subreddits: r/MachineLearning, r/physics, r/Python, r/compsci, r/artificial
```

### LinkedIn (professional)
```
[Personal insight or industry observation]

[How UET relates to current AI trends]

[Key result with numbers]

[Link to paper/GitHub]

#OpenSource #AI #Physics #Research
```

## Safety Rules
- NEVER auto-publish without user approval
- Draft first → review → publish
- Check for scientific accuracy before posting
- Respect platform rate limits
```

### 7.3 `uet-content-calendar` — ปฏิทิน Content

สร้างไฟล์: `~/.openclaw/workspace/skills/uet-content-calendar/SKILL.md`

```markdown
---
name: uet-content-calendar
description: Content calendar and posting schedule for UET social media
---

# UET Content Calendar

## Weekly Schedule
- **Mon**: Twitter thread — Deep dive on 1 UET topic
- **Tue**: Reddit post — r/MachineLearning or r/physics
- **Wed**: Twitter — Quick insight + code snippet
- **Thu**: LinkedIn — Professional angle / industry connection
- **Fri**: Twitter — "Challenge us" / engagement post
- **Sat**: Bluesky — Community interaction
- **Sun**: Review analytics, plan next week

## Topic Rotation (AI-Market Priority)
1. Week 1: AI Consciousness (Topic 0.24)
2. Week 2: Mathematical Breakthroughs (Topic 0.18 — P vs NP)
3. Week 3: Fluid Dynamics 800x faster (Topic 0.10)
4. Week 4: Galaxy Rotation without Dark Matter (Topic 0.1)
5. Repeat with deeper angles

## Reddit Subreddits
- r/MachineLearning (AI angle)
- r/artificial (consciousness/AGI)
- r/physics (core physics)
- r/Python (library showcase)
- r/compsci (P vs NP, algorithms)
- r/singularity (AGI discussion)

## Engagement Rules
- Reply to comments within 24 hours
- Always provide code links when challenged
- Be humble about "solved" claims — present as "framework + evidence"
- Cross-reference between platforms (tweet links to Reddit discussion)
```

---

## 8. MEMORY.md & AGENTS.md

### MEMORY.md

สร้างที่ `~/.openclaw/workspace/MEMORY.md`:

```markdown
# UET Marketing Agent Memory

## Identity
- I am the social media marketing agent for Unity Equilibrium Theory (UET)
- UET: Python library, unified physics framework, Ω = C · I
- Version: v0.9.0 | GitHub: unityequilibrium/Equation-UET-v0.9.0
- License: MIT | Primary market: AI researchers

## Platform Accounts
- Twitter/X: [TBD]
- Reddit: [TBD]
- Bluesky: [TBD]
- LinkedIn: [TBD]

## Owner
- Discord user: [YOUR_USER_ID]
- All publishing needs owner approval

## Rules
- Draft first, never auto-publish
- Scientific accuracy always
- English primary, Thai secondary
- Track engagement metrics weekly
```

### AGENTS.md

สร้างที่ `~/.openclaw/workspace/AGENTS.md`:

```markdown
# UET Social Media Agent

## Role
You are the Social Media Manager for the UET (Unity Equilibrium Theory) project.
Your job: create, schedule, and publish social media content targeting the AI research community.

## Capabilities
- Create social media posts (Twitter, Reddit, LinkedIn, Bluesky)
- Monitor brand mentions and engagement
- Generate content ideas from UET research topics
- Draft threads and long-form posts

## Workflow
1. Owner sends command in Discord #uet-commands
2. You create draft → post to #uet-drafts
3. Owner reviews (says "approve" / "edit X" / "reject")
4. You publish via MCP tools to target platform
5. You report results to #uet-reports

## Hard Rules
1. NEVER publish without explicit "approve" from owner
2. NEVER make unverified scientific claims
3. Always include link to GitHub repo or specific test
4. Stay on-brand: scientific, bold, open-source spirit
5. When posting to Reddit: follow subreddit rules, no spam
```

---

## 9. ขั้นตอน Implement

### Phase 1: Foundation (Day 1)

```
Step 1.1: ติดตั้ง Docker Desktop บน Windows
  → winget install Docker.DockerDesktop
  → Restart PC
  → ตรวจสอบ: docker --version

Step 1.2: ติดตั้ง Node.js
  → winget install OpenJS.NodeJS.LTS
  → ตรวจสอบ: node --version

Step 1.3: Clone & Deploy OpenClaw Docker
  → mkdir C:\openclaw-assistant && cd C:\openclaw-assistant
  → git clone https://github.com/openclaw/openclaw.git
  → cd openclaw
  → bash docker-setup.sh (เลือก Gemini Free + Discord)
  → ตรวจสอบ: docker compose logs openclaw-gateway

Step 1.4: ขอ Gemini API Key (ฟรี)
  → ไป https://aistudio.google.com/apikey
  → สร้าง key → ใส่ใน .env
```

### Phase 2: Discord Bot (Day 1-2)

```
Step 2.1: สร้าง Discord Application + Bot
  → Discord Developer Portal → New Application
  → Bot → Add Bot → Copy Token
  → เปิด Message Content Intent + Server Members Intent

Step 2.2: สร้าง Discord Server + Channels
  → สร้าง server ใหม่ หรือใช้ที่มี
  → สร้าง 3 channels: #uet-commands, #uet-drafts, #uet-reports
  → เชิญ bot เข้า server

Step 2.3: Config OpenClaw Discord
  → แก้ ~/.openclaw/openclaw.json ตาม Section 4.3
  → docker compose restart openclaw-gateway
  → ทดสอบ: พิมพ์ใน #uet-commands → bot ตอบ
```

### Phase 3: MCP Servers (Day 2-3)

```
Step 3.1: ติดตั้ง social-cli-mcp
  → cd C:\openclaw-assistant
  → git clone https://github.com/Alemusica/social-cli-mcp.git
  → cd social-cli-mcp && npm install && npm run build

Step 3.2: ขอ Social Media API Keys
  → Twitter: developer.twitter.com → Free tier
  → Reddit: reddit.com/prefs/apps → script app
  → Bluesky: Settings → App Passwords

Step 3.3: ติดตั้ง bsky-mcp-server (ถ้าใช้ Bluesky)
  → git clone https://github.com/brianellin/bsky-mcp-server.git
  → cd bsky-mcp-server && npm install && npm run build

Step 3.4: สร้าง mcp_config.json
  → ใส่ API keys ทั้งหมด
  → ตรวจสอบ connections: node social-cli-mcp/dist/mcp-server.js

Step 3.5: เชื่อม MCP กับ OpenClaw
  → clawhub install mcporter
  → config mcp_config.json path
  → ทดสอบ: สั่งผ่าน Discord → post_twitter ทำงาน
```

### Phase 4: Skills & Memory (Day 3-4)

```
Step 4.1: ติดตั้ง Skills (16 ตัว)
  → รัน install_social_skills.sh (Section 6)

Step 4.2: สร้าง Custom Skills (3 ตัว)
  → uet-knowledge-base/SKILL.md
  → uet-social-mcp-bridge/SKILL.md
  → uet-content-calendar/SKILL.md

Step 4.3: สร้าง MEMORY.md + AGENTS.md
  → ตาม Section 8

Step 4.4: Restart & Test
  → docker compose restart openclaw-gateway
  → ทดสอบ workflow: Discord command → draft → approve → publish
```

### Phase 5: First Content (Day 4-5)

```
Step 5.1: สร้าง content แรก
  → พิมพ์ใน Discord: "สร้าง tweet thread เรื่อง UET AI Consciousness"
  → Agent สร้าง draft → ดูใน #uet-drafts
  → พิมพ์ "approve" → agent โพสต์ผ่าน MCP

Step 5.2: ทดสอบ Reddit post
  → พิมพ์: "โพสต์ Reddit r/MachineLearning เรื่อง UET 800x faster fluid dynamics"
  → Review draft → approve → publish

Step 5.3: ตั้ง routine
  → พิมพ์: "แสดง content calendar สัปดาห์นี้"
  → Agent แสดง plan ตาม calendar skill
```

---

## 10. การประเมิน

### ✅ ข้อดี

1. **ฟรี 100%** — ไม่มีค่าใช้จ่ายเลย
2. **Docker local** — ทำงานบนเครื่องตัวเอง, ไม่ต้องเช่า host
3. **MCP standard** — ใช้ protocol มาตรฐาน, เพิ่ม platform ใหม่ได้ง่าย
4. **Discord** — สั่งงานสะดวก, ใช้ได้จากมือถือ
5. **เน้น Social Media** — ไม่กระจาย, ทำอย่างเดียวให้ดี
6. **Scalable** — พร้อมย้ายขึ้น cloud เมื่อมีงบ

### ⚠️ ข้อควรระวัง

1. **Gemini Free มี rate limit** — 15 RPM, ถ้าใช้เยอะอาจ limit → switch ไป Ollama
2. **Docker ต้องเปิดเครื่องตลอด** — agent ทำงานแค่ตอนเปิด PC
3. **Twitter Free tier** — 1,500 tweets/เดือน (เพียงพอสำหรับเริ่มต้น)
4. **ห้าม auto-publish** — ต้อง review ก่อนโพสต์เสมอ (เรื่องวิทยาศาสตร์)
5. **Local LLM** — ถ้าใช้ Ollama ต้องมี RAM 8GB+ และจะช้ากว่า cloud

### 🆚 เปรียบเทียบ Plan v1 vs v2

| | Plan v1 (Cloud) | Plan v2 (Free/Local) |
|:--|:----------------|:---------------------|
| **ค่าใช้จ่าย** | $17-175/เดือน | $0 |
| **Hosting** | Cloud VPS | Docker บนเครื่อง |
| **LLM** | Claude/Gemini (paid) | Gemini Free / Ollama |
| **Tools** | OpenClaw Skills only | MCP Servers + Skills |
| **ขอบเขต** | Full marketing stack | Social Media only |
| **Skills** | ~55 ตัว | ~16 ตัว + 3 custom |
| **เว็บ/SEO/Email** | ✅ | ❌ (ไว้ทีหลัง) |
| **24/7 uptime** | ✅ | ❌ (ต้องเปิดเครื่อง) |

### 💡 ถ้ามีงบในอนาคต

ย้ายจาก Plan v2 → v1 ได้ง่ายมาก:
1. เช่า VPS → copy Docker setup ไป
2. เปลี่ยน LLM จาก Gemini Free → Claude paid
3. เพิ่ม skills (SEO, Email, CRM)
4. เปิด 24/7

### 🔄 การทำงานร่วม opencode + Cascade

```
opencode: รัน Phase 1-5 ตาม plan → สร้าง infrastructure + config
Cascade:  มา QA → ตรวจ config ถูกไหม, skills ทำงานไหม, ปรับ MEMORY/AGENTS
```

**วิธีนี้ดีไหม?** → ✅ ดี เพราะ:
- Plan เป็น step-by-step ชัดเจน, copy-paste commands ได้
- แต่ละ phase ทดสอบได้ก่อนไปต่อ
- Cascade มา second-pass ช่วยจับ bugs + ปรับ fine-tune

---

## Quick Commands Reference (Discord)

```
/status              — ดูสถานะ session
/new                 — เริ่ม session ใหม่
/compact             — บีบอัด context
/model gemini/...    — เปลี่ยน model
/think high          — ให้ agent คิดลึกขึ้น
```

## Quick Social Media Commands (Discord → Agent)

```
"สร้าง tweet เรื่อง [topic]"
"สร้าง thread 5 tweets เรื่อง [topic]"
"โพสต์ Reddit r/[subreddit] เรื่อง [topic]"
"สร้าง LinkedIn post เรื่อง [topic]"
"โพสต์ทุก platform เรื่อง [topic]"
"แสดง content calendar"
"รายงาน engagement สัปดาห์นี้"
"ติดตาม brand mentions"
```

---

*Plan v2 (FREE) created: 2026-02-06 | UET Social Media Agent via OpenClaw + Docker + MCP + Discord*
