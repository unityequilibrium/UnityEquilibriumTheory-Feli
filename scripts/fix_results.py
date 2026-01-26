import os
import shutil
import glob

# Map Solver Name (in folder) to Topic Result Path
TOPIC_MAP = {
    "Phase_Solver": "research_uet/topics/0.11_Phase_Transitions/Result",
    "Casimir_Solver": "research_uet/topics/0.12_Vacuum_Energy_Casimir/Result",
    "Econ_Solver": "research_uet/topics/0.14_Complex_Systems/Result",
    "Cluster_Solver": "research_uet/topics/0.15_Cluster_Dynamics/Result",
    "Nuclear_Solver": "research_uet/topics/0.16_Heavy_Nuclei/Result",
    "Higgs_Solver": "research_uet/topics/0.17_Mass_Generation/Result",
    "Mixing_Solver": "research_uet/topics/0.18_Neutrino_Mixing/Result",
    "Gravity_Solver": "research_uet/topics/0.19_Gravity_GR/Result",
    "Atomic_Solver": "research_uet/topics/0.20_Atomic_Physics/Result",
    "MassGap_Solver": "research_uet/topics/0.21_Yang_Mills_Mass_Gap/Result",
    "Neural_Solver": "research_uet/topics/0.22_Neural_Dynamics/Result",
}

ROOT_RESULT = "Result"


def migrate_results():
    print("Migrating Results...")

    for solver_key, target_path in TOPIC_MAP.items():
        # Find all folders matching *SolverKey
        folders = glob.glob(os.path.join(ROOT_RESULT, f"*{solver_key}"))

        if not folders:
            # Silent if not found (already moved)
            continue

        # Sort by timestamp (Folder name starts with timestamp)
        # 1768..._Name
        folders.sort(reverse=True)
        latest_folder = folders[0]

        print(f"Latest {solver_key}: {latest_folder} -> {target_path}")

        # Ensure target dir exists
        os.makedirs(target_path, exist_ok=True)

        # Copy files
        for item in os.listdir(latest_folder):
            s = os.path.join(latest_folder, item)
            d = os.path.join(target_path, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

        # Create Summary File
        with open(os.path.join(target_path, "README_RESULTS.md"), "w") as f:
            f.write(f"# Results for {solver_key}\n\n")
            f.write(f"Source: `{latest_folder}`\n")
            f.write(f"Migrated on: 2026-01-15\n\n")
            f.write("## Contents\n")
            f.write("- `metrics.csv`: Time-series data of the simulation.\n")
            f.write("- `params.json`: Configuration used.\n")
            f.write("- `final_state.npy`: Final field configuration (if enabled).\n")


if __name__ == "__main__":
    migrate_results()
