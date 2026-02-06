"""
UET Cosmic Flow Research
========================
Topic: 0.26 - Cosmic Dynamic Frame
Data: Laniakea Supercluster (Tully et al. 2014)
Goal: Visualize the Flow Field from Dipole Repeller to Shapley Attractor.
"""

import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path

# --- PATH SETUP ---
current_path = Path(__file__).resolve()
ROOT = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        ROOT = parent
        break

if ROOT and str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from research_uet.core.uet_glass_box import UETPathManager, UETMetricLogger
except Exception as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)


def load_flows():
    path = (
        ROOT
        / "research_uet"
        / "topics"
        / "0.26_Cosmic_Dynamic_Frame"
        / "Data"
        / "03_Research"
        / "Laniakea_Flows.json"
    )
    if not path.exists():
        raise FileNotFoundError(f"Missing Data: {path}")

    with open(path, "r") as f:
        return json.load(f)


def run_viz():
    print("=" * 60)
    print("UET COSMIC FLOW VISUALIZATION")
    print("Data: Laniakea (Tully 2014)")
    print("=" * 60)

    # 1. Setup Showcase Output
    output_dir = UETPathManager.get_result_dir(
        topic_id="0.26", experiment_name="Laniakea_Flow", category="showcase"
    )
    logger = UETMetricLogger("Laniakea_Flow", output_dir=output_dir)

    # 2. Load Data
    data = load_flows()
    landmarks = data["landmarks"]

    # Extract Coordinates
    names = []
    coords = []
    types = []

    for l in landmarks:
        names.append(l["name"])
        coords.append(l["coords"])
        types.append(l["type"])

    coords = np.array(coords)  # Shape (N, 3)

    # 3. Visualization
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Plot Points
    colors = {
        "Observer": "blue",
        "Attractor": "red",
        "Major Attractor": "darkred",
        "Repeller (Void)": "cyan",
        "Filament": "green",
        "Local Hub": "orange",
    }

    for i in range(len(names)):
        c = colors.get(types[i], "gray")
        s = 200 if "Attractor" in types[i] else 100
        ax.scatter(
            coords[i, 0],
            coords[i, 1],
            coords[i, 2],
            c=c,
            s=s,
            label=types[i] if types[i] not in plt.gca().get_legend_handles_labels()[1] else "",
        )
        ax.text(coords[i, 0], coords[i, 1], coords[i, 2] + 5, names[i], fontsize=9)

    # Plot Streamlines (Schematic)
    # Flow from Repeller -> Milky Way -> Great Attractor -> Shapley
    # We construct a Bezier-like path or simple lines

    # Find Indices
    try:
        idx_repeller = names.index("Dipole Repeller")
        idx_mw = names.index("Milky Way (Local Group)")
        idx_ga = names.index("Great Attractor (Norma)")
        idx_shapley = names.index("Shapley Concentration")

        path_indices = [idx_repeller, idx_mw, idx_ga, idx_shapley]
        path_coords = coords[path_indices]

        ax.plot(
            path_coords[:, 0], path_coords[:, 1], path_coords[:, 2], "k--", linewidth=1, alpha=0.5
        )

        # Add Arrows
        for j in range(len(path_coords) - 1):
            start = path_coords[j]
            end = path_coords[j + 1]
            # Quiver takes (x,y,z, u,v,w)
            # ax.quiver(start[0], start[1], start[2], end[0]-start[0], end[1]-start[1], end[2]-start[2], length=0.2, color='gray')
            # Actually simple plot is cleaner for schematic
            pass

    except ValueError:
        pass

    ax.set_xlabel("SGX (Mpc)")
    ax.set_ylabel("SGY (Mpc)")
    ax.set_zlabel("SGZ (Mpc)")
    ax.set_title("Laniakea Supercluster: Cosmic Flow Field (UET Dynamic Frame)")

    # Legend deduplication
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    save_path = output_dir / "Laniakea_Flow_Map.png"
    plt.savefig(save_path, dpi=300)
    print(f"📸 Showcase Image Saved: {save_path}")

    print("✅ Result: SUCCESS (Flow Field Mapped)")
    return True


if __name__ == "__main__":
    run_viz()
