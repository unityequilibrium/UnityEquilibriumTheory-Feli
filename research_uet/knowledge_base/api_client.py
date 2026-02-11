"""
OpenRouter API Client with Per-Agent Cost Tracking
===================================================
Unified client for all OpenRouter API calls (embeddings + chat).
Each call is logged with agent_id, model, token counts, and cost.

Usage:
    from research_uet.knowledge_base.api_client import OpenRouterClient

    client = OpenRouterClient.from_config("path/to/config.toml")

    # Embeddings
    vectors = client.embed(["Hello world", "UET physics"])

    # Chat (agent-routed)
    response = client.chat("orchestrator", [
        {"role": "user", "content": "Find research on κ > 0.5"}
    ])

    # Check costs
    client.cost_tracker.print_summary()

Rust Compatibility:
    - CostEntry is a simple dataclass → maps to Rust struct
    - cost_log.jsonl is line-delimited JSON → serde-compatible
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, date
from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

try:
    import httpx
except ImportError:
    httpx = None


# =============================================================================
# COST TRACKING
# =============================================================================

# OpenRouter pricing per 1M tokens (as of 2026-02)
# Source: https://openrouter.ai/models
_MODEL_PRICING = {
    # Embedding models
    "qwen/qwen3-embedding-8b": {"input": 0.01, "output": 0.0},
    "baai/bge-m3": {"input": 0.01, "output": 0.0},
    "google/gemini-embedding-001": {"input": 0.15, "output": 0.0},
    "openai/text-embedding-3-small": {"input": 0.02, "output": 0.0},
    "openai/text-embedding-3-large": {"input": 0.13, "output": 0.0},
    # Chat models
    "qwen/qwen3-coder-next": {"input": 0.07, "output": 0.30},
    "zhipu/glm-4.7-flash": {"input": 0.06, "output": 0.40},
    "deepseek/deepseek-v3.2": {"input": 0.25, "output": 0.38},
    "qwen/qwen3-30b-a3b:free": {"input": 0.0, "output": 0.0},
    "mistral/devstral-2": {"input": 0.05, "output": 0.22},
}


@dataclass
class CostEntry:
    """Single API call cost record. Rust-compatible (serde JSON)."""

    timestamp: str
    agent_id: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    cumulative_daily_usd: float
    endpoint: str  # "chat" or "embeddings"
    success: bool = True
    error: Optional[str] = None


class CostTracker:
    """
    Track API costs per agent, per model, per day.

    Logs every call to a JSONL file for transparency.
    Enforces daily budget limits per agent.
    """

    def __init__(self, log_file: Path, alert_threshold: float = 1.0):
        self.log_file = Path(log_file)
        self.alert_threshold = alert_threshold
        self._daily_totals: dict[str, float] = {}  # agent_id -> daily USD
        self._today: str = ""
        self._reset_if_new_day()

    def _reset_if_new_day(self):
        """Reset daily totals at midnight."""
        today = date.today().isoformat()
        if today != self._today:
            self._daily_totals = {}
            self._today = today

    def get_daily_total(self, agent_id: str) -> float:
        """Get today's total cost for an agent."""
        self._reset_if_new_day()
        return self._daily_totals.get(agent_id, 0.0)

    def get_total_daily_cost(self) -> float:
        """Get today's total cost across all agents."""
        self._reset_if_new_day()
        return sum(self._daily_totals.values())

    def check_budget(self, agent_id: str, budget_limit: float) -> bool:
        """Check if agent is within daily budget. Raises if over."""
        current = self.get_daily_total(agent_id)
        if current >= budget_limit > 0:
            raise BudgetExceeded(
                f"Agent '{agent_id}' exceeded daily budget: "
                f"${current:.4f} >= ${budget_limit:.2f}"
            )
        return True

    def log_call(
        self,
        agent_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        endpoint: str = "chat",
        success: bool = True,
        error: Optional[str] = None,
    ) -> CostEntry:
        """Log an API call and update daily totals."""
        self._reset_if_new_day()

        # Calculate cost
        pricing = _MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
        cost = (
            input_tokens * pricing["input"] / 1_000_000
            + output_tokens * pricing["output"] / 1_000_000
        )

        # Update daily total
        self._daily_totals[agent_id] = self._daily_totals.get(agent_id, 0.0) + cost
        cumulative = self._daily_totals[agent_id]

        # Create entry
        entry = CostEntry(
            timestamp=datetime.now().isoformat(),
            agent_id=agent_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=round(cost, 8),
            cumulative_daily_usd=round(cumulative, 6),
            endpoint=endpoint,
            success=success,
            error=error,
        )

        # Write to log file
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

        # Alert check
        total = self.get_total_daily_cost()
        if total > self.alert_threshold:
            print(
                f"⚠️  COST ALERT: Daily total ${total:.4f} "
                f"exceeds threshold ${self.alert_threshold:.2f}"
            )

        return entry

    def print_summary(self):
        """Print today's cost summary."""
        self._reset_if_new_day()
        print(f"\n{'='*60}")
        print(f"  API Cost Summary — {self._today}")
        print(f"{'='*60}")
        print(f"  {'Agent':<20} {'Cost USD':>10}")
        print(f"  {'-'*20} {'-'*10}")
        for agent, cost in sorted(self._daily_totals.items()):
            print(f"  {agent:<20} ${cost:>9.6f}")
        print(f"  {'-'*20} {'-'*10}")
        total = self.get_total_daily_cost()
        print(f"  {'TOTAL':<20} ${total:>9.6f}")
        print(f"{'='*60}\n")


class BudgetExceeded(Exception):
    """Raised when an agent exceeds its daily budget."""

    pass


# =============================================================================
# OPENROUTER CLIENT
# =============================================================================


class OpenRouterClient:
    """
    Unified OpenRouter API client with agent-aware routing.

    Each agent uses its own model and has independent cost tracking.
    All calls are logged to cost_log.jsonl for full transparency.
    """

    def __init__(
        self,
        base_url: str,
        keys: dict[str, str],
        agents: dict[str, dict],
        cost_tracker: CostTracker,
    ):
        if httpx is None:
            raise ImportError("httpx is required: pip install httpx")

        self.base_url = base_url.rstrip("/")
        self.keys = keys
        self.agents = agents
        self.cost_tracker = cost_tracker
        self._client = httpx.Client(timeout=120.0)

    @classmethod
    def from_config(cls, config_path: str | Path) -> "OpenRouterClient":
        """Create client from config.toml file."""
        if tomllib is None:
            raise ImportError("tomllib (Python 3.11+) or tomli is required: pip install tomli")

        config_path = Path(config_path)
        with open(config_path, "rb") as f:
            config = tomllib.load(f)

        cost_log_path = config_path.parent / config["cost_tracking"]["log_file"]
        tracker = CostTracker(
            log_file=cost_log_path,
            alert_threshold=config["cost_tracking"]["alert_threshold_usd"],
        )

        return cls(
            base_url=config["openrouter"]["base_url"],
            keys=config["openrouter"]["keys"],
            agents=config["agents"],
            cost_tracker=tracker,
        )

    def _get_key(self, agent_id: str) -> str:
        """Get API key for an agent."""
        agent_cfg = self.agents.get(agent_id, {})
        key_name = agent_cfg.get("key_name", "default")
        key = self.keys.get(key_name)
        if not key or key == "sk-or-v1-CHANGEME":
            raise ValueError(
                f"API key '{key_name}' not configured. "
                f"Edit config.toml [openrouter.keys].{key_name}"
            )
        return key

    def _get_model(self, agent_id: str) -> str:
        """Get model for an agent."""
        agent_cfg = self.agents.get(agent_id)
        if not agent_cfg:
            raise ValueError(
                f"Unknown agent '{agent_id}'. " f"Available: {list(self.agents.keys())}"
            )
        return agent_cfg["model"]

    def _check_budget(self, agent_id: str):
        """Check if agent is within budget."""
        agent_cfg = self.agents.get(agent_id, {})
        budget = agent_cfg.get("daily_budget_usd", 0.0)
        if budget > 0:
            self.cost_tracker.check_budget(agent_id, budget)

    def embed(
        self,
        texts: list[str],
        agent_id: str = "embedding",
    ) -> list[list[float]]:
        """
        Generate embeddings via OpenRouter.

        Args:
            texts: List of strings to embed
            agent_id: Agent for cost tracking (default: "embedding")

        Returns:
            List of embedding vectors
        """
        self._check_budget(agent_id)
        model = self._get_model(agent_id)
        key = self._get_key(agent_id)

        response = self._client.post(
            f"{self.base_url}/embeddings",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "input": texts,
            },
        )
        response.raise_for_status()
        data = response.json()

        # Extract token usage
        usage = data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)

        # Log cost
        self.cost_tracker.log_call(
            agent_id=agent_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=0,
            endpoint="embeddings",
        )

        # Extract vectors
        embeddings = [item["embedding"] for item in data["data"]]
        return embeddings

    def chat(
        self,
        agent_id: str,
        messages: list[dict],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Chat completion via OpenRouter with agent-specific routing.

        Args:
            agent_id: Which agent is making this call
            messages: Chat messages [{"role": "user", "content": "..."}]
            max_tokens: Override max tokens (default: from config)
            temperature: Sampling temperature

        Returns:
            Assistant response text
        """
        self._check_budget(agent_id)
        model = self._get_model(agent_id)
        key = self._get_key(agent_id)
        agent_cfg = self.agents.get(agent_id, {})

        if max_tokens is None:
            max_tokens = agent_cfg.get("max_tokens_per_call", 4096)

        response = self._client.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://uet-research.local",
                "X-Title": f"UET-Agent-{agent_id}",
            },
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
        )
        response.raise_for_status()
        data = response.json()

        # Extract usage
        usage = data.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)

        # Log cost
        self.cost_tracker.log_call(
            agent_id=agent_id,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            endpoint="chat",
        )

        # Extract response
        return data["choices"][0]["message"]["content"]

    def close(self):
        """Close HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    # Quick self-test without API (tests CostTracker only)
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, mode="w") as tmp:
        tmp_path = Path(tmp.name)

    tracker = CostTracker(log_file=tmp_path)

    # Simulate some calls
    tracker.log_call("orchestrator", "qwen/qwen3-coder-next", 1000, 500, "chat")
    tracker.log_call("embedding", "qwen/qwen3-embedding-8b", 5000, 0, "embeddings")
    tracker.log_call("local_data", "zhipu/glm-4.7-flash", 800, 200, "chat")
    tracker.log_call("web_research", "deepseek/deepseek-v3.2", 2000, 1000, "chat")

    # Print summary
    tracker.print_summary()

    # Verify log file
    with open(tmp_path) as f:
        lines = f.readlines()
    print(f"✅ Logged {len(lines)} entries to {tmp_path}")

    for line in lines:
        entry = json.loads(line)
        print(f"  {entry['agent_id']:<16} {entry['model']:<30} ${entry['cost_usd']:.8f}")

    # Cleanup
    tmp_path.unlink()
    print("\n✅ CostTracker self-test PASSED")
