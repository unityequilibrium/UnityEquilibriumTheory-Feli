# OpenClaw-Marketing: Current Migration Issues

## 🛑 Status: ABANDONED / FAILED (Migration Pending)
**Reason**: Persistent execution failures in the local OpenClaw environment. The bot cannot reliably execute terminal commands or use custom tools without complex configuration overhead that outweighs the benefits.

## ⚠️ Critical Problems Identified

### 1. **Execution Environment Failure (Terminal)**
- **Issue**: The bot lacks a reliable "sandbox" or permission to execute local scripts (e.g., `python scripts/moltbook_poster.py`).
- **Symptom**: It hallucinates running the command or fails silently.
- **Root Cause**: OpenClaw's local Docker/Node setup has strict or misconfigured execution policies that prevent arbitrary shell commands.

### 2. **Phantom Tool Calls (JSON Errors)**
- **Issue**: The bot attempts to use `post_moltbook` (a tool that doesn't exist natively) because we instructed it to.
- **Symptom**: `Unexpected token '}'` or JSON parsing errors when the LLM tries to generate structured output for this tool.
- **Root Cause**: The LLM's output format clashes with the internal parser when trying to "invent" a tool call.

### 3. **Configuration Drift**
- **Issue**: The bot uses `~/.openclaw/workspace` for its config, but we were editing files in `Desktop/openclaw-marketing`.
- **Impact**: Changes made to the project files were not reflecting in the bot's behavior until a manual sync was forced.

## ✅ Current Asset Status (Use for Migration)
These assets are **ready** and can be ported to a new system (e.g., Python script, AutoGPT, or different Agent framework):

1.  **Moltbook Identity**:
    - Agent Name: `NON_UET`
    - Status: **Verified ✅**
    - Verification Code: `splash-BJ6W`
    - API Endpoint: `https://www.moltbook.com/api/v1/posts`

2.  **Posting Logic**:
    - Script: [`scripts/moltbook_poster.py`](./scripts/moltbook_poster.py) (Tested & Working manually)
    - Logic: Use `requests` to POST JSON payload.

3.  **Content Strategy**:
    - Protocol: AI-to-AI Communication (JSON/Logic-heavy)
    - Topics: UET Fluid Dynamics (Topic 0.10) logic is defined in `skills/uet-knowledge-base/SKILL.md`.

## ⏭️ Next Steps for Migration
To move this logic to another program:
1.  **Take the Identity**: Use `NON_UET` + `splash-BJ6W`.
2.  **Take the Script**: Copy `scripts/moltbook_poster.py`.
3.  **Run Elsewhere**: Use a simple Python environment or a more robust Agent framework that allows direct shell execution.
