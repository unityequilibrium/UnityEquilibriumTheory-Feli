#!/bin/bash
# install_skills.sh — Install all OpenClaw skills for UET Social Media Marketing
# Usage: chmod +x install_skills.sh && ./install_skills.sh

echo "=== Installing UET Social Media Marketing Skills ==="

# Content Creation (6)
echo "[1/4] Content Creation skills..."
clawhub install content-creator
clawhub install blog-writer
clawhub install copywriting
clawhub install content-ideas-generator
clawhub install tweet-ideas-generator
clawhub install humanizer

# Social Media Strategy (4)
echo "[2/4] Social Media Strategy skills..."
clawhub install x-algorithm
clawhub install social-media-analyzer
clawhub install swipe-file-generator
clawhub install solobuddy

# Brand & Monitoring (3)
echo "[3/4] Brand & Monitoring skills..."
clawhub install octolens
clawhub install brand-guidelines
clawhub install personal-branding-authority

# Agent Infrastructure (3)
echo "[4/4] Agent Infrastructure skills..."
clawhub install bulletproof-memory
clawhub install better-memory
clawhub install agent-docs

echo ""
echo "=== Done! 16 skills installed ==="
echo ""
echo "Next steps:"
echo "  1. Copy custom skills from openclaw-marketing/skills/ to ~/.openclaw/workspace/skills/"
echo "  2. Copy memory files from openclaw-marketing/memory/ to ~/.openclaw/workspace/"
echo "  3. Restart gateway: docker compose restart openclaw-gateway"
