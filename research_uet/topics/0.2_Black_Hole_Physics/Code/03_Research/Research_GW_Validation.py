"""
UET Gravitational Wave Test - Entropy Unification
=================================================
Verifies that Gravitational Waves (GW) are Information Entropy waves.

Hypothesis:
Energy radiated (E_gw) corresponds to the Information (S) lost
during the merger event, mediated by the Universal Memory Field.

Event: GW150914
Data: LIGO Open Science Center
"""

import sys
import math
import json
from pathlib import Path

# --- PATH SETUP (Must be FIRST) ---
current_path = Path(__file__).resolve()
ROOT = None
for parent in [current_path] + list(current_path.parents):
    if (parent / "research_uet").exists():
        ROOT = parent
        break

if ROOT:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    print("CRITICAL: research_uet root not found!")
    sys.exit(1)

# Core Imports
try:
    from research_uet.core.uet_glass_box import UETPathManager
    from research_uet.core.uet_parameters import G, C, M_SUN, K_B, HBAR

    c = C
    M_sun = M_SUN
    k_B = K_B
    h_bar = HBAR

    # Helper: Dynamic Import of Engine
    import importlib.util

    eng_path = (
        ROOT
        / "research_uet/topics/0.2_Black_Hole_Physics/Code/01_Engine/Engine_BlackHole.py"
    )
    if eng_path.exists():
        spec = importlib.util.spec_from_file_location("Engine_BlackHole", eng_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        UETBlackHoleEngine = mod.UETBlackHoleEngine
    else:
        print("CRITICAL: Engine not found.")
        sys.exit(1)

except ImportError as e:
    print(f"CRITICAL: Core UET imports failed: {e}")
    sys.exit(1)


def bekenstein_entropy(M):
    """
    S = 4 * PI * G * M^2 * k_B / (h_bar * c)
    """
    return 4 * math.pi * G * M**2 * k_B / (h_bar * c)


def run_test():
    print("=" * 60)
    print("UET GRAVITATIONAL WAVE ENTROPY TEST")
    print("Event: GW150914")
    print("=" * 60)

    # Path to Data
    TOPIC_DIR = ROOT / "research_uet" / "topics" / "0.2_Black_Hole_Physics"
    data_path = TOPIC_DIR / "Data" / "03_Research" / "black_hole_data.json"

    try:
        with open(data_path, "r") as f:
            bh_data = json.load(f)
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

    gw_event = next(
        item for item in bh_data["gravitational_wave"] if item["event"] == "GW150914"
    )

    # Initialize Engine
    engine = UETBlackHoleEngine()

    M1 = gw_event["m1"]
    M2 = gw_event["m2"]
    M_final = gw_event["final_mass"]

    # Radiated Energy (Observed)
    E_rad_obs = ((M1 + M2) - M_final) * M_sun * c**2

    # Calculate Entropies using Engine
    S1 = engine.compute_entropy(M1)
    S2 = engine.compute_entropy(M2)
    S_final = engine.compute_entropy(M_final)

    S_init = S1 + S2
    Delta_S = S_final - S_init

    print(f"Initial Entropy: {S_init:.2e} J/K")
    print(f"Final Entropy:   {S_final:.2e} J/K")
    print(f"Entropy Change:  {Delta_S:.2e} J/K (Increased)")

    # Temperature Scale (Hawking Temp of Final BH)
    T_H_final = engine.compute_temperature(M_final)
    Thermodynamic_Available_Work = Delta_S * T_H_final

    print(f"T_Hawking (Final): {T_H_final:.2e} K")
    print(f"T * Delta_S:       {Thermodynamic_Available_Work:.2e} J")
    print(f"Observed E_rad:    {E_rad_obs:.2e} J")

    # Guard against zero division if kill switch active (T=nan)
    if math.isnan(T_H_final):
        print("KILL SWITCH DETECTED: Engine returned NaN.")
        return False

    Ratio = E_rad_obs / Thermodynamic_Available_Work
    print(f"Amplification Ratio: {Ratio:.4f}")

    UET_CONSTANT = math.log(2) / math.pi
    print(f"Theoretical UET Constant (ln(2)/pi): {UET_CONSTANT:.4f}")

    error_margin = abs(Ratio - UET_CONSTANT) / UET_CONSTANT
    print(f"Deviation: {error_margin*100:.2f}%")

    if error_margin < 0.05:
        print("\nSUCCESS! Universal Gravitational Entropy Relation Confirmed.")
        print(f"Formula: E_rad = (ln 2 / pi) * T_H * Delta_S")
        return True
    else:
        print("\nFAIL: Ratio does not match ln(2)/pi.")
        return False


if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
