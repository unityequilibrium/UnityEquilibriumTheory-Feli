import os
import sys
import matplotlib.pyplot as plt

# Link to Engine
script_dir = os.path.dirname(os.path.abspath(__file__))
result_dir = os.path.abspath(os.path.join(script_dir, "../../Result/02_Proof"))
engine_dir = os.path.abspath(os.path.join(script_dir, "../01_Engine"))
if engine_dir not in sys.path:
    sys.path.append(engine_dir)

if not os.path.exists(result_dir):
    os.makedirs(result_dir)

from Engine_Slingshot import SingularitySlingEngine


def run_propulsion_proof():
    log_file = os.path.join(result_dir, "Res_LightSpeed_Approach.txt")
    with open(log_file, "w", encoding="utf-8") as f:

        def log_print(msg):
            print(msg)
            f.write(str(msg) + "\n")

        log_print("\n🚀 UET PROOF 05: THE LIGHT-SPEED APPROACH")
        log_print("=========================================")
        log_print("Scenario: Exiting Solar System & Activating Interstellar SGS")

        # 1. Setup
        c = 299792458
        target_v = 0.1 * c
        engine = SingularitySlingEngine(initial_v=11000)

        # A. Departure Phase (Safe Mode)
        log_print(f"Current Position: {engine.dist_from_sun_au} AU (Earth Orbit)")
        is_safe, msg = engine.check_safety()
        log_print(msg)

        # B. Moving to Heliosphere Edge (100 AU)
        log_print("... Moving to Interstellar Vacuum (Heliopause) ...")
        engine.dist_from_sun_au = 120
        is_safe, msg = engine.check_safety()
        log_print(msg)

        # C. Target Parameters
        log_print(f"\nTarget Velocity: {target_v:,.0f} m/s (0.1c)")
        log_print(f"Initial Velocity: {engine.v:,.0f} m/s")
        log_print("-" * 60)

        # 2. Multistage Slingshot Loop
        stage = 1
        current_v = engine.v
        v_history = [current_v / c * 100]

        while current_v < target_v and stage <= 100:
            # Each stage: Fire a 5e12 kg Micro-Singularity
            try:
                # simulate_sling returns a list of dictionaries
                results = engine.simulate_sling(5e12, 1000, 1.0)

                # Check for error dict
                if isinstance(results, list) and len(results) > 0 and "error" in results[0]:
                    log_print(results[0]["error"])
                    break
                elif not results:
                    log_print("⚠️ Error: Simulation returned no data.")
                    break

                # Post-sling velocity (last step)
                new_v = results[-1]["velocity"]
                delta_v = new_v - current_v
                current_v = new_v

                # Update engine for next sling
                engine.v = current_v

                log_print(
                    f"Stage {stage:02d}: V = {current_v:,.0f} m/s (+{delta_v:,.0f} m/s) | {current_v/c*100:.2f}% c"
                )
                v_history.append(current_v / c * 100)
                stage += 1

            except Exception as e:
                log_print(f"⚠️ Simulation Error: {e}")
                break

        # 2.5 Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, len(v_history) + 1), v_history, color="blue", linewidth=2)
        plt.axhline(y=10, color="red", linestyle="--", label="Target (0.1c)")
        plt.title("Relativistic Slingshot: 0.1c Approach")
        plt.xlabel("Slingshot Stages")
        plt.ylabel("Velocity (% of Light Speed)")
        plt.legend()
        plt.grid(True, alpha=0.3)

        # Standard Path: Result/02_Proof
        plot_path = os.path.join(result_dir, "relativistic_acceleration.png")
        plt.savefig(plot_path)
        log_print(f"\n✅ Plot saved to: {plot_path}")

        # 3. Verdict
        log_print("-" * 60)
        if current_v >= target_v:
            log_print(f"✅ SUCCESS: Reached 0.1c in {stage-1} slingshots!")
            log_print("Status: Space-Time Synchronized with Galactic Flow.")
        else:
            log_print(f"⚠️ PARTIAL SUCCESS: Final Velocity {current_v/c*100:.2f}% c reached.")


if __name__ == "__main__":
    run_propulsion_proof()
