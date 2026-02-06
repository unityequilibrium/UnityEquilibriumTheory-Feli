# 🎬 UET Cinematic Viz Standard (Manim)

This document defines the standard for creating high-end, cinematic mathematical animations for UET research, suitable for social media showcase and high-impact presentations.

---

### 🏛️ 1. The Cinematic Philosophy
**"Make the Invisible, Visible."**
UET Cinematic Viz should not just show data; it should show the **underlying geometry and information gradients** of the universe.

- **Contrast:** High contrast between the dark vacuum (background) and bright information fields.
- **Motion:** Smooth, physics-based transitions. Avoid jerky movements.
- **Clarity:** Use LaTeX for all mathematical notation to ensure professional quality.

---

### 🎨 2. Aesthetic Design System
To maintain a unified brand across all UET showcases, use the following color palette and styles:

| Element | Color Code | Usage |
| :--- | :--- | :--- |
| **UET_CYAN** | `#00e5ff` | Primary Field (C), Information Gradients, Main Logic |
| **UET_MAGENTA**| `#ff00ff` | Hidden State (I), Entropy, Energy Decay |
| **UET_GOLD** | `#ffd700` | Constants, Proof Points, High-Value Highlights |
| **Background** | `#000000` | Pure Black (The Vacuum) |

**Typography:**
- Use **LaTeX** for all formulas.
- For titles, use `Tex` or `MathTex` with `golden_ratio` or `UET_CYAN` coloring.

---

### 🛠️ 3. Technical Stack
- **Engine:** [Manim](https://www.manim.community/) (Community Edition).
- **Physics Backend:** Use `research_uet/core/uet_base_solver.py` to generate the raw data points if necessary, then pass them to Manim.
- **Rendering:** 1440p (2K) or 1080p, 60fps for final export. 

---

### 📝 4. Workflow Standard (Concept to Render)

#### **Step 1: The Concept (The LNS Logic)**
- **L (Limitation):** What is hard to see in the current static plot?
- **N (Necessity):** What motion/dimension is needed to explain it?
- **S (Solution):** Define the Manim camera path or object evolution.

#### **Step 2: The Math Engine**
Write the Python logic to calculate the fields.
> [!TIP]
> Do not calculate complex physics *inside* the Manim `construct` method. Pre-calculate to a `numpy` array or JSON for faster rendering iterations.

#### **Step 3: Manim Scripting**
Create a class inheriting from `Scene` or `ThreeDScene`.
```python
from manim import *

class UETShowcase(ThreeDScene):
    def construct(self):
        # 1. Setup
        title = Tex("UET: Spacetime Fluid", color=CYAN).to_edge(UP)
        
        # 2. Logic (Fields)
        axes = ThreeDAxes()
        field_plot = self.create_uet_field() # Custom method
        
        # 3. Animation
        self.play(Write(title))
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.1)
        self.play(Create(field_plot), run_time=3)
        self.wait(2)
```

---

### 🚀 5. Standards for Social Media (Cinematic Hacks)
1. **Glow Effects:** Use `Create` with `rate_func=smooth` and slight bloom if possible.
2. **Dynamic Camera:** Never let the camera stay still. Use `self.begin_ambient_camera_rotation` or subtle zooms.
3. **The "Pulse":** For UET fields, use a repeating pulse animation to represent the "breathing" of the information vacuum.
4. **Music Sync:** If adding audio (not in Manim), ensure transitions happen on beats.

---

### 📂 Directory Standard
Cinematic scripts should be named with prefix `Cine_` and placed in `05_Visualization`:
- `Code/05_Visualization/Cine_Riemann_UET.py`
- `Result/01_Showcase/Cine_Riemann_UET.mp4`
