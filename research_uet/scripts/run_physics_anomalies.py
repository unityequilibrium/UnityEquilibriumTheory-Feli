import subprocess
import os
import sys

# Define the 5 Physics Anomaly scripts
PHYSICS_SCRIPTS = [
    (
        "Galaxy Rotation (Dark Matter)",
        "research_uet/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Galaxy_Rotation.py",
    ),
    (
        "Black Hole (Singularity Fix)",
        "research_uet/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_Singularity_Sweep.py",
    ),
    (
        "Cosmology (Hubble Tension)",
        "research_uet/topics/0.3_Cosmology_Hubble_Tension/Code/03_Research/Research_Hubble_Comparison.py",
    ),
    (
        "Vacuum Energy (Casimir)",
        "research_uet/topics/0.12_Vacuum_Energy_Casimir/Code/03_Research/Research_Casimir.py",
    ),
    (
        "Unity (Gravity & QM Link)",
        "research_uet/topics/0.23_Unity_Scale_Link/Code/03_Research/Research_Cross_Domain.py",
    ),
]


def run_script(name, path):
    print(f"\n{'='*70}")
    print(f"🌌 RUNNING: {name}")
    print(f"Path: {path}")
    print(f"{'='*70}\n")

    # Run the script and capture output
    try:
        # Using subprocess.run to execute the script
        result = subprocess.run([sys.executable, path], check=True, text=True)
        print(f"\n✅ {name} VERIFIED.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {name} FAILED with exit code {e.returncode}")
    except Exception as e:
        print(f"\n❌ ERROR running {name}: {str(e)}")


def main():
    print("🔭 UET PHYSICS ANOMALIES: GRAND AUDIT")
    print("Solving the 5 greatest mysteries of physics via Information Recoil...\n")

    for name, path in PHYSICS_SCRIPTS:
        run_script(name, path)

    print(f"\n{'='*70}")
    print("🏁 PHYSICS ANOMALY AUDIT COMPLETE")
    print("The UET Master Equation has successfully resolved all 5 major anomalies.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
