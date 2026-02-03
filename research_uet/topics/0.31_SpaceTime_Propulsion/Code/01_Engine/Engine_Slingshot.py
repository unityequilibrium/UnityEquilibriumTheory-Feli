import math
import time


class SingularitySlingEngine:
    """
    UET Space-Time Engine: Singularity Gravitational Slingshot (SGS)
    Objective: Achieve Relativistic Velocity (0.1c+) using transient micro-singularities.
    """

    def __init__(self, ship_mass=500000, initial_v=11000, omega_coupling=1e9):
        self.G = 6.67430e-11
        self.c = 299792458
        self.hbar = 1.0545718e-34
        self.ship_mass = ship_mass
        self.v = initial_v
        self.omega_coupling = omega_coupling  # UET Hyper-Gravity Factor
        self.dist_from_sun_au = 1.0  # Current distance from sun (default 1 AU)

    def check_safety(self):
        """Standard UET Safety Protocol: No Singularities inside Solar System."""
        # 100 AU is approx the heliopause
        if self.dist_from_sun_au < 100:
            return (
                False,
                "🛑 SAFETY BREACH: Too close to Solar System ( < 100 AU). Use Planetary Slingshot instead.",
            )
        return True, "✅ CLEAR: Interstellar Space. SGS Authorized."

    def calculate_evap_time(self, mass_kg):
        """Hawking Radiation Decay Time"""
        # Formula: t = (5120 * pi * G^2 * M^3) / (hbar * c^4)
        return (5120 * math.pi * (self.G**2) * (mass_kg**3)) / (self.hbar * (self.c**4))

    def simulate_sling(self, singularity_mass_kg, distance_m, duration_s):
        """
        Simulate a single 'Sling' pass using UET Omega Coupling.
        """
        is_safe, msg = self.check_safety()
        if not is_safe:
            return [{"error": msg}]

        dt = 0.001
        steps = int(duration_s / dt)

        results = []
        current_mass = singularity_mass_kg
        current_v = self.v
        current_dist = distance_m

        # Calculate evaporation rate
        evap_time = self.calculate_evap_time(singularity_mass_kg)
        mass_decay_rate = singularity_mass_kg / evap_time if evap_time > 0 else 0

        for s in range(steps):
            if current_mass <= 1e-10 or current_dist <= 1.0:
                break

            # UET Hyper-Gravity: Force is amplified by Omega Field
            force = (self.G * current_mass * self.ship_mass * self.omega_coupling) / (
                current_dist**2
            )
            accel = force / self.ship_mass

            # Simple 1D vector: pulling forward
            current_v += accel * dt

            # Decay the singularity
            current_mass -= mass_decay_rate * dt

            if s % 100 == 0:
                results.append(
                    {
                        "time": s * dt,
                        "velocity": current_v,
                        "dist": current_dist,
                        "mass": current_mass,
                    }
                )

        # Ensure we always return at least the final state
        if not results:
            results.append(
                {
                    "time": duration_s,
                    "velocity": current_v,
                    "dist": current_dist,
                    "mass": current_mass,
                }
            )

        return results


if __name__ == "__main__":
    # Test case: Interstellar Space (150 AU)
    engine = SingularitySlingEngine(initial_v=11000)
    engine.dist_from_sun_au = 150

    sling_results = engine.simulate_sling(1e5, 10.0, 1.0)

    print(f"{'Time (s)':<10} | {'Velocity (m/s)':<20} | {'Dist (m)':<15} | {'Mass (kg)':<20}")
    print("-" * 75)
    for r in sling_results:
        if "error" in r:
            print(r["error"])
            break
        print(
            f"{r['time']:<10.2f} | {r['velocity']:<20,.2f} | {r['dist']:<15.2f} | {r['mass']:<20.2e}"
        )
