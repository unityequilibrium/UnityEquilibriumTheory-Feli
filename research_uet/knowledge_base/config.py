import os
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError("Please install 'tomli' (Python < 3.11) or upgrade to Python 3.11+")

# Path to config.toml
CONFIG_PATH = Path(__file__).parent / "config.toml"

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

with open(CONFIG_PATH, "rb") as f:
    CONFIG = tomllib.load(f)

# Optional: Validate critical keys
if "openrouter" not in CONFIG:
    raise ValueError("Config missing 'openrouter' section")
