import sys
from pathlib import Path

# --- ROBUST PATH FINDER ---


from research_uet.core.uet_parameters import get_params, G, C


class GravityWellEngine:
    """
    UET Space-Time Engine v2: Gradient Surfer
    Logic: Universe is a slope. Singularities are traction.
    """

    def __init__(self, ship_mass=500000, initial_v=11000, omega_coupling=1e9, params=None):
        self.params = params if params else get_params("0.31")
        self.G = G
        self.c = C
        self.ship_mass = ship_mass
        self.v = initial_v
        self.omega_coupling = omega_coupling

        # New: Universal Gradient Factors
        self.universal_fall_v = 600000  # 600 km/s relative to CMB
        self.ship_height_potential = 1.0  # Normalized height in the "Well"

    def simulate_gradient_sling(self, singularity_mass, target_well_depth):
        """
        Simulate matching a target well by 'falling' down the gradient.
        """
        log = []
        # Calculate Delta-V needed to match target flow
        required_v = target_well_depth
        c_v = self.v

        log.append(f"Starting V: {c_v:,.0f} m/s | Target Flow: {required_v:,.0f} m/s")

        # Simulation of the "Falling" phase
        # The user says: "Create a hole to move forward with the universe's fall"
        steps = 50
        for i in range(steps):
            # Each 'pulse' of the SGS pulls us 100km/s (Simplified for demo)
            boost = (self.omega_coupling * self.G * singularity_mass) / (1000**2)
            # We cap boost for realism in this demo
            boost_v = min(boost * 0.01, 500000)

            c_v += boost_v
            # The "Height" in the gradient decreases as we fall faster
            self.ship_height_potential -= 0.01

            if i % 10 == 0:
                log.append(f"Step {i}: V={c_v:,.0f} | Potential={self.ship_height_potential:.2f}")

            if c_v >= required_v:
                log.append(
                    f"✅ SYNC REACHED: Ship is 'falling' at the same speed as the target world."
                )
                break

        return log


if __name__ == "__main__":
    engine = GravityWellEngine()
    # Scenario: Moving from Solar System (600 km/s flow) to a Deep-Void Well (2,000 km/s flow)
    results = engine.simulate_gradient_sling(singularity_mass=1e12, target_well_depth=2000000)
    for line in results:
        print(line)
