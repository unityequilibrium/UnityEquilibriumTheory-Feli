import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path
from research_uet import ROOT_PATH

root_path = ROOT_PATH


# --- ROBUST PATH FINDER ---


# Engine Import (Crystallized Specialized Engine)
try:
    import importlib.util

    engine_file = (
        root_path
        / "research_uet"
        / "topics"
        / "0.28_Material_Synthesis"
        / "Code"
        / "01_Engine"
        / "Engine_Acoustic_Alignment.py"
    )
    spec = importlib.util.spec_from_file_location("Engine_Acoustic_Alignment", engine_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    AcousticAlignmentEngine = mod.AcousticAlignmentEngine
except Exception as e:
    print(f"Error loading Acoustic Engine: {e}")
    sys.exit(1)


# Standardized UET Root Path


def simulate_acoustic_locking(frequency_mhz):
    """
    Simulates alignment quality using the official Specialized Engine.
    Natural Resonance (432 MHz) is formalized in Pillar 01.
    """
    engine = AcousticAlignmentEngine()
    return engine.calculate_twist_error(frequency_mhz)


def run_alignment_demo():
    frequencies = np.linspace(400, 460, 200)
    errors = [simulate_acoustic_locking(f) for f in frequencies]

    print("\n🔊 ACOUSTIC ALIGNMENT: Searching for Resonant Lock (432 MHz)")
    print("==========================================================")

    test_points = [400, 420, 432, 450]
    for tp in test_points:
        err = simulate_acoustic_locking(tp)
        accuracy = (1.1 / (1.1 + err)) * 100
        status = "🌟 ALIGNMENT LOCKED" if err < 0.01 else "⚪ OSCILLATING"
        print(
            f"Freq: {tp} MHz | Twist Error: {err:.4f}° | Accuracy: {accuracy:.2f}% | Status: {status}"
        )

    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, errors, color="magenta", linewidth=2)
    plt.axvline(x=432, color="green", linestyle="--", label="UET Resonant Lock")
    plt.title("Acoustic Self-Alignment: Frequency vs. Twist Error")
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Twist Error (Degrees)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    # Save to Standardized Results via PathManager
    try:
        from research_uet.core.uet_glass_box import UETPathManager

        output_dir = UETPathManager.get_result_dir(
            topic_id="0.28", experiment_name="Acoustic_Alignment", category="Research"
        )
    except ImportError:
        output_dir = Path("research_uet/topics/0.28_Material_Synthesis/Figures")
        output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "acoustic_alignment_plot.png"
    plt.savefig(output_path)

    print(f"\n✅ Simulation Complete. Plot saved as {output_path}")
    print(
        "💡 CONCLUSION: At 432 MHz resonance, graphene sheets self-align to the 1.1 degree Magic Angle."
    )


if __name__ == "__main__":
    run_alignment_demo()
