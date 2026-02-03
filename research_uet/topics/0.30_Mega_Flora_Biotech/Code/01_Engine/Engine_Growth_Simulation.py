import math
import random
import sys
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

from research_uet.core.uet_parameters import get_params


class YggdrasilEngine:
    def __init__(self, species_name="Yggdrasil-X1", growth_rate=1.2, params=None):
        self.params = params if params else get_params("0.30")
        self.species = species_name
        self.growth_rate = growth_rate

        # Allometric Scaling Constants (for Giant Sequoias/Banyan hybrid)
        self.root_to_shoot_ratio = 0.8  # Massive root system for anchoring
        self.wood_density_start = 600.0  # kg/m3 (Young wood)
        self.wood_density_max = 1200.0  # kg/m3 (Ironwood-like core)

    def grow_tree(self, years=100):
        """
        Simulate the lifecycle of the Mega-Flora.
        Returns a timeline of stats.
        """
        timeline = []

        # Initial State (Seedling)
        height_m = 0.5
        diameter_cm = 1.0
        biomass_kg = 0.1
        current_density = self.wood_density_start
        root_depth_m = 0.3  # Initial root depth

        for year in range(1, years + 1):
            # 1. Calculate Structural Stress (Thigmomorphogenesis)
            # Higher height/thin trunk = High Stress.
            # Stress Ratio > 100 means "Wobbly". Ideal is < 80.
            stress_ratio = (height_m * 100) / diameter_cm

            # 2. Smart Energy Allocation (The "Balance" Logic)
            # If stressed -> Prioritize Girth/Density (Fortress Mode)
            # If stable -> Prioritize Height (Sprint Mode)
            if stress_ratio > 90:
                allocation_height = 0.2
                allocation_girth = 0.8
            else:
                allocation_height = 0.7  # Sprint!
                allocation_girth = 0.3

            # 3. Growth Phase (Age Factor)
            # Young trees grow faster (Exponential), Old trees slow down
            age_factor = 1.0
            if year < 15:
                age_factor = 1.6  # Genetic Sprint Boost (+60%)
            elif year > 50:
                age_factor = 0.5  # Senior slowdown

            # 4. Execute Growth
            # Base growth unit (depends on leaves/biomass)
            # Tapering Logic: Height growth slows down as it gets taller (Hydraulic tension)
            h_tension_drag = max(0.1, 1.0 - (height_m / 250.0))

            # --- UET BALANCING: Bioluminescent Energy Drain ---
            # Using bioluminescence as a 'Safety Valve' to prevent over-growth.
            # Lighting up the city at night drains ATP/Sugars.
            biolum_intensity = 0.0
            if year > 5:
                # Intensity increases with size (more 'lamps' for the city)
                biolum_intensity = min(1.0, height_m / 100.0)

            # Energy drain factor (0.0 to 0.4 reduction in growth power)
            energy_drain = biolum_intensity * 0.4

            growth_power = (
                (biomass_kg**0.6)
                * self.growth_rate
                * age_factor
                * h_tension_drag
                * (1.0 - energy_drain)
            )

            # Apply Allocation
            # As height increases, allocation_height naturally decreases to favor stability
            if height_m > 30.0:
                allocation_height *= 0.7  # Organic slowdown
                allocation_girth *= 1.3  # Focus on foundation

            delta_h = (growth_power * allocation_height) * 0.5  # Height is hard
            delta_d = (growth_power * allocation_girth) * 0.2  # Girth is slow

            height_m += delta_h
            diameter_cm += delta_d

            # 5. Lignification (Density)
            # Density acts as a multiplier for strength
            if current_density < self.wood_density_max:
                # Add density based on Girth allocation (Thickening implies hardening)
                current_density += allocation_girth * 10.0

            # 6. Biomass Update (Square-Cube Law approx)
            # Biomass ~ Volume * Density
            volume_m3 = (math.pi * ((diameter_cm / 200) ** 2) * height_m) / 3  # Cone approx
            biomass_kg = volume_m3 * current_density

            # 7. Root System (Adaptive Anchoring)
            # Roots must counterbalance Height
            target_root_depth = height_m * 0.7
            if root_depth_m < target_root_depth:
                root_depth_m += 0.5  # Roots dig deep

            # 8. Structural Integrity Score
            # Force ~ Mass * Gravity * Height (Moment arm)
            # Resistance ~ Diameter^3 * Density (Section Modulus)
            load = biomass_kg * height_m
            resistance = (diameter_cm**3) * (current_density / 100.0)
            safety_factor = resistance / (load + 1.0)  # Avoid div/0

            # Metric for the User: "Strength" relative to Concrete Pile
            # We scale this to N for the Proof script
            integrity_newtons = resistance * 50.0

            stats = {
                "year": year,
                "height_m": round(height_m, 2),
                "diameter_cm": round(diameter_cm, 2),
                "root_depth_m": round(root_depth_m, 2),
                "integrity_score": round(integrity_newtons, 0),
                "fruit_yield_kg": round((diameter_cm * 2) * 5 if year > 5 else 0, 1),
                "stress_ratio": round(stress_ratio, 1),
                "safety_factor": round(safety_factor, 1),
            }
            timeline.append(stats)

        return timeline


if __name__ == "__main__":
    # Test Run
    engine = YggdrasilEngine()
    history = engine.grow_tree(50)
    print(f"Year 50 Stats: {history[-1]}")
