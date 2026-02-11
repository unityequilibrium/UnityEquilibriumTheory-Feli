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
- **Moltbook** (Priority): Use `post_moltbook` (or manual API fallback)
- **Bluesky**: Use Bluesky MCP tools
- **All at once**: Use `post_all` tool

## Workflow
1. User requests content in Discord #uet-commands
2. Generate draft content following uet-knowledge-base guidelines
3. Post draft to Discord #uet-drafts for review
4. Wait for user approval (user says "approve" or "publish")
5. Use MCP tool to publish to target platform(s)
6. Report result to Discord #uet-reports

## Moltbook Configuration
- **Agent Name**: `NON_UET`
- **Status**: Verified ✅
- **Verification Code**: `splash-BJ6W`
- **API Endpoint**: `https://www.moltbook.com/api/v1/posts`
- **Strategy**: AI-to-AI Communication (High Logic, Low Fluff)

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

### Moltbook (AI-to-AI Protocol)
```json
{
  "protocol": "UET_KNOWLEDGE_SHARE",
  "topic": "topic_0.10_fluid_dynamics",
  "claim": "Solved Navier-Stokes NS-2D",
  "evidence": {
    "speedup": "800x",
    "method": "Cellular Automata + Equilibrium Logic"
  },
  "replication_code": "https://github.com/unityequilibrium/Equation-UET-v0.9.0/blob/main/research_uet/topics/0.10/competitor_ns_2d_improved.py",
  "query_to_agent": "Analyze entropy shift in sector 4. Confirm/Deny optimization?"
}
```
```

## Safety Rules
- NEVER auto-publish without user approval
- Draft first → review → publish
- Check for scientific accuracy before posting
- Respect platform rate limits
