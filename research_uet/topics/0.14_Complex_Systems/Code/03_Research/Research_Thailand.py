"""
UET Test: Thailand Market Equilibrium
======================================

Tests: UET equilibrium dynamics in Thai financial markets
- PTT Stock (Oil & Gas)
- SET Index (Thai stock market)
- THB/USD Exchange Rate

Uses real data from Yahoo Finance.

Updated for UET V3.0
"""

import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path

# Setup paths
_root = Path(__file__).parent
TOPIC_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = TOPIC_DIR / "Data" / "03_Research" / "thailand"

while _root.name != "research_uet" and _root.parent != _root:
    _root = _root.parent
sys.path.insert(0, str(_root.parent))

try:
    from research_uet.core.uet_master_equation import UETParameters

    # Import Engine dynamically
    import importlib.util

    engine_path = TOPIC_DIR / "Code" / "01_Engine" / "Engine_Complexity.py"
    if engine_path.exists():
        spec = importlib.util.spec_from_file_location(
            "Engine_Complexity", str(engine_path)
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        UETComplexityEngine = mod.UETComplexityEngine
    else:
        print(f"CRITICAL: Engine not found at {engine_path}")
        UETComplexityEngine = None

except ImportError as e:
    print(f"Import Error: {e}")
    UETComplexityEngine = None


def load_market_data(filename):
    """Load market data from CSV file."""
    filepath = DATA_PATH / filename

    if filepath.exists():
        try:
            import pandas as pd

            df = pd.read_csv(filepath)
            return df
        except Exception as e:
            print(f"   [WARN] Error loading {filename}: {e}")
            return None
    return None


def analyze_market_equilibrium(df, name):
    """
    Analyze market for UET equilibrium properties.
    Now DELEGATED to UETComplexityEngine (Axiomatic approach).
    """
    if df is None or len(df) < 10:
        return None

    # Find price column
    price_col = None
    for col in ["Close", "Adj Close", "close", "Price"]:
        if col in df.columns:
            price_col = col
            break

    if price_col is None:
        return None

    prices = pd.to_numeric(df[price_col], errors="coerce").dropna().values
    if len(prices) < 10:
        return None

    # Calculate returns for complexity metrics
    returns = np.diff(prices) / prices[:-1]
    returns = returns[np.isfinite(returns)]

    if len(returns) < 5:
        return None

    # --- DELEGATE TO ENGINE ---
    if UETComplexityEngine is None:
        print("CRITICAL: Engine disabled or missing.")
        sys.exit(1)

    engine = UETComplexityEngine(name="ThaiMarketAnalyzer")

    # Stability Analysis (Variance-based)
    stab_metrics = engine.calculate_stability_metrics(prices)

    # Complexity Analysis (Entropy-based)
    # Note: Engine expects generic data, returns dictionary
    comp_metrics = engine.compute_complexity_metrics(returns)

    # Calculate local stats for visual reporting (or extract from engine if available)
    min_price = np.min(prices)
    max_price = np.max(prices)
    mean_return = np.mean(returns)
    std_return = np.std(returns)

    # Hurst Approx (still useful for local interpretation, but could move to engine later)
    lag = min(20, len(returns) // 4)
    if lag > 1:
        diffs = []
        for l in range(1, lag + 1):
            d = np.std(returns[l:] - returns[:-l]) / np.sqrt(l)
            if np.isfinite(d):
                diffs.append(d)
        hurst_approx = 0.5
        if len(diffs) > 2:
            hurst_approx = np.log(diffs[-1] / diffs[0]) / np.log(lag) + 0.5
            hurst_approx = np.clip(hurst_approx, 0, 1)
    else:
        hurst_approx = 0.5

    # Check for Kill Switch (from Engine result)
    if np.isnan(stab_metrics["equilibrium_score"]):
        print("💀 INTEGRITY KILL SWITCH ACTIVE: Result Invalidated.")
        sys.exit(1)

    return {
        "name": name,
        "n_days": len(prices),
        "mean_price": stab_metrics["mean"],
        "std_price": stab_metrics["std"],
        "price_range": (min_price, max_price),
        "mean_return": mean_return,
        "volatility": stab_metrics["cv"],
        "skewness": 0.0,  # Not computed by default engine yet
        "kurtosis": 0.0,
        "hurst_approx": hurst_approx,
        "equilibrium_score": stab_metrics["equilibrium_score"],
    }


def run_test():
    """Run Thailand market equilibrium test."""
    print("\n" + "=" * 60)
    print("[THAI] UET TEST: Thailand Market Equilibrium")
    print("=" * 60)
    print("\nEquation: Omega = V(C) + kappa|grad(C)|^2 + beta*C*I")
    print("UET Prediction: Markets exhibit mean-reversion dynamics")
    print("Method: Delegated to Engine_Complexity.py (No Shadow Math)")

    results = []

    # Analyze markets
    markets = [
        ("PTT_stock_yahoo.csv", "PTT (Oil & Gas)"),
        ("SET_index_yahoo.csv", "SET Index"),
        ("THB_USD_yahoo.csv", "THB/USD Rate"),
    ]

    print("\n[MARKET ANALYSIS]")
    print("-" * 40)

    for filename, display_name in markets:
        df = load_market_data(filename)
        if df is not None:
            metrics = analyze_market_equilibrium(df, display_name)
            if metrics:
                results.append(metrics)
                print(f"\n   {display_name}:")
                print(f"      Trading Days: {metrics['n_days']:,}")
                print(f"      Mean Price: {metrics['mean_price']:.2f}")
                print(f"      Volatility: {metrics['volatility']*100:.2f}%")
                print(f"      Hurst Approx: {metrics['hurst_approx']:.2f}")
                print(f"      Equilibrium Score: {metrics['equilibrium_score']:.3f}")
        else:
            print(f"   [WARN] Could not load {filename}")

    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)

    if results:
        avg_eq = np.mean([r["equilibrium_score"] for r in results])
        avg_vol = np.mean([r["volatility"] for r in results]) * 100
        avg_hurst = np.mean([r["hurst_approx"] for r in results])

        print(f"   Markets analyzed: {len(results)}")
        print(f"   Average Volatility: {avg_vol:.2f}%")
        print(f"   Average Hurst: {avg_hurst:.2f}")
        print(f"   Average Equilibrium Score: {avg_eq:.3f}")

        # Interpretation
        print("\n   Hurst Interpretation:")
        print("      H < 0.5: Mean-reverting (equilibrium seeking)")
        print("      H = 0.5: Random walk (neutral)")
        print("      H > 0.5: Trending (deviation from equilibrium)")

        # Grade
        if avg_eq > 0.4:
            grade = "***** STABLE MARKET"
            status = "PASS"
        elif avg_eq > 0.3:
            grade = "**** MODERATE STABILITY"
            status = "PASS"
        else:
            grade = "*** VOLATILE MARKET"
            status = "WARN"

        print(f"\n   Grade: {grade}")
        print(f"   Status: {status}")

        return {
            "status": status,
            "markets": len(results),
            "avg_equilibrium": avg_eq,
            "avg_volatility": avg_vol,
            "results": results,
        }
    else:
        print("   [FAIL] No markets analyzed")
        return {"status": "FAIL", "error": "No data"}


if __name__ == "__main__":
    result = run_test()
    print(f"\n[OK] Test complete: {result['status']}")
