import os
from pathlib import Path

TOPICS_TO_CHECK = [
    "0.2_Black_Hole_Physics",
    "0.3_Cosmology_Hubble_Tension",
    "0.4_Superconductivity_Superfluids",
    "0.6_Electroweak_Physics",
    "0.7_Neutrino_Physics",
    "0.8_Muon_g2_Anomaly",
    "0.9_Quantum_Nonlocality",
    "0.14_Complex_Systems",
]

ROOT = Path("research_uet/topics")


def check_topic(topic_name):
    topic_path = ROOT / topic_name
    print(f"Checking {topic_name}...")

    # 1. Engine Check
    engine_dir = topic_path / "Code/01_Engine"
    engines = list(engine_dir.glob("*.py"))
    engines = [e for e in engines if e.name != "__init__.py"]

    if not engines:
        print(f"  ❌ No Engine found in {engine_dir}")
        return False

    engine_compliant = False
    for eng in engines:
        content = eng.read_text(encoding="utf-8")
        if "INTEGRITY_KILL_SWITCH" in content:
            engine_compliant = True
            print(f"  ✅ Engine {eng.name}: Kill Switch present")
        else:
            print(f"  ❌ Engine {eng.name}: No Kill Switch!")

    if not engine_compliant:
        return False

    # 2. Research Check
    research_dir = topic_path / "Code/03_Research"
    scripts = list(research_dir.glob("*.py"))
    scripts = [s for s in scripts if s.name != "__init__.py"]

    if not scripts:
        print(f"  ⚠️ No Research scripts found")
        return True  # Technically pass if no scripts

    all_scripts_pass = True
    for sc in scripts:
        content = sc.read_text(encoding="utf-8")
        if "Engine" in content:
            print(f"  ✅ Research {sc.name}: Referenced Engine")
        else:
            print(
                f"  ❌ Research {sc.name}: No 'Engine' string found (Shadow Math risk)"
            )
            all_scripts_pass = False

    return all_scripts_pass


def main():
    print("=== CUSTOM AUDIT FOR ASSIGNED TOPICS ===")
    all_pass = True
    for topic in TOPICS_TO_CHECK:
        if not check_topic(topic):
            all_pass = False
            print(f"❌ TOPIC FAILED: {topic}\n")
        else:
            print(f"✅ TOPIC PASSED: {topic}\n")

    if all_pass:
        print("🎉 ALL ASSIGNED TOPICS VERIFIED!")
    else:
        print("💀 SOME TOPICS FAILED.")


if __name__ == "__main__":
    main()
