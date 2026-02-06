"""
UET Visualization: Black Hole Shadow (Topic 0.2)
================================================
Generates EHT Shadow Simulation (M87*).
Extracted from legacy Research_EHT_Validation.py.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- ROBUST PATH FINDER ---
current_path = Path(__file__).resolve()
root_path = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        root_path = parent
        break

if root_path and str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

# Output Directory
OUTPUT_DIR = (
    root_path / "research_uet" / "topics" / "0.2_Black_Hole_Physics" / "Result" / "01_Showcase"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set Style
plt.style.use("dark_background")


def generate_shadow_plot():
    print("Generating M87* Shadow Simulation...")

    x = np.linspace(-10, 10, 200)
    y = np.linspace(-10, 10, 200)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    # Ring at ~5 Schwarzschild radii (Shadow)
    # Simple Gaussian ring model for visualization
    Z = np.exp(-((R - 5) ** 2) / 2) + np.random.normal(0, 0.05, X.shape)

    plt.figure(figsize=(8, 6))
    plt.imshow(Z, extent=[-10, 10, -10, 10], cmap="magma", origin="lower")
    plt.colorbar(label="Intensity")

    plt.title("Simulated Black Hole Shadow (M87*) - UET Prediction", fontsize=14)
    plt.xlabel("X (Rs)")
    plt.ylabel("Y (Rs)")

    out_path = OUTPUT_DIR / "eht_shadow_simulation_refactored.png"
    plt.savefig(out_path, dpi=150)
    print(f"[SUCCESS] Saved to {out_path}")
    plt.close()


if __name__ == "__main__":
    generate_shadow_plot()
