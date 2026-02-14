# 📊 Visualization Capabilities Report

> **Library:** Plotly (Open Source)
> **Reference:** https://plotly.com/python/
> **License:** MIT (Free & Open Source)
> **Last Updated:** 2025-12-23

---

## 📋 Overview

Plotly เป็น library สร้างกราฟ interactive ที่ใช้ได้ทั้ง Python และ JavaScript (plotly.js)
UET Lab สามารถใช้ Plotly แสดงผลได้หลากหลายรูปแบบดังนี้:

---

## 🎯 Chart Types Available

### 1️⃣ Basic Charts (พื้นฐาน)

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Scatter Plot** | Plot จุด particles | แสดงตำแหน่ง x, y ของ bodies |
| **Line Chart** | Time series data | Energy vs Time |
| **Bar Chart** | Compare values | เปรียบเทียบ params หลาย runs |
| **Pie Chart** | Distribution | สัดส่วน Kinetic/Potential |
| **Bubble Chart** | 3 dimensions | Position + Mass + Velocity |

### 2️⃣ Statistical Charts (สถิติ)

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Error Bars** | Uncertainty | แสดง error ในการวัด |
| **Box Plot** | Distribution | กระจายตัวของ Energy หลาย runs |
| **Histogram** | Frequency | ความถี่ของค่า field |
| **Dist Plot** | Probability | PDF ของ convergence |
| **2D Histogram** | Density | ความหนาแน่นของ particles |

### 3️⃣ Scientific Charts (วิทยาศาสตร์) ⭐ สำคัญสำหรับ UET

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Contour Plot** | Field visualization | แสดง potential field φ(x,y) |
| **Heatmap** | 2D data | Evolution ของ field ตลอด grid |
| **Imshow** | Image data | Field state เป็น image |
| **Ternary Plot** | 3 components | สมดุลของ 3 equations |
| **Log Plot** | Exponential data | Energy decay (log scale) |

### 4️⃣ 3D Charts ⭐ สำคัญมาก

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **3D Scatter** | Particle positions | แสดง bodies ใน 3D space |
| **3D Surface** | Field surface | Potential surface φ(x,y,z) |
| **3D Line** | Trajectories | วิถีโคจรของ particles |
| **3D Mesh** | Complex shapes | Visualization surfaces |
| **Isosurface** | Volumetric | Density isosurfaces |

### 5️⃣ Financial Charts (Time Series)

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Time Series** | Temporal data | ทุก metric vs time |
| **Candlestick** | OHLC data | สำหรับ stock toy model |
| **Waterfall** | Change analysis | Energy change breakdown |
| **Range Slider** | Time navigation | เลือกช่วงเวลาที่ต้องการดู |

### 6️⃣ Maps (ถ้าต้องการ Geo)

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Choropleth** | Geographic data | Traffic toy model |
| **Scatter Map** | Points on map | Location-based simulations |
| **Line on Map** | Paths | Traffic flow visualization |

### 7️⃣ AI/ML Charts

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **ROC Curve** | Model evaluation | Neural prediction accuracy |
| **PCA Viz** | Dimensionality | Parameter space exploration |
| **Cluster** | Grouping | Classify simulation outcomes |

### 8️⃣ Specialized Bio/Science

| Chart Type | Use Case in UET | ตัวอย่างการใช้งาน |
|------------|-----------------|-------------------|
| **Volcano Plot** | Differential analysis | Compare parameter effects |
| **Clustergram** | Hierarchical | Group similar runs |
| **Alignment** | Sequence data | สำหรับ LLM toy model |

---

## 🎬 Animations

Plotly รองรับ **animations** ได้ โดยสามารถ:
- Animate over time
- Play/Pause control
- Slider for time navigation
- Smooth transitions

```python
fig = px.scatter(df, x="x", y="y", animation_frame="time")
```

---

## 🎛️ Custom Controls

Plotly มี built-in controls:

| Control | Description |
|---------|-------------|
| **Buttons** | Toggle traces, change data |
| **Sliders** | Scrub through time |
| **Dropdowns** | Select variables |
| **Range Slider** | Zoom time range |

---

## 🔗 Integration with UET Lab

### Python Backend (scripts/)
```python
import plotly.express as px
import plotly.graph_objects as go

# Line chart for energy
fig = px.line(df, x='time', y='energy', title='Total Energy')
fig.write_html('reports/energy.html')
```

### Frontend (plotly.js)
```javascript
// Already installed via plotly.js in node_modules
Plotly.newPlot('graph', [{
    x: telemetry.time,
    y: telemetry.energy,
    type: 'scatter',
    mode: 'lines'
}]);
```

---

## 📈 Recommended Charts for UET Use Cases

### Simulation Monitoring
| Use Case | Recommended Chart |
|----------|-------------------|
| Energy vs Time | Line Chart |
| Energy Conservation | Filled Area |
| Particle Positions | 3D Scatter |
| Field Evolution | Heatmap Animation |
| Parameter Sweep | Scatter Matrix |

### Analysis & Comparison
| Use Case | Recommended Chart |
|----------|-------------------|
| Compare Runs | Grouped Bar |
| Convergence | Log Scale Line |
| Distribution | Box Plot / Violin |
| Correlation | Scatter + Trendline |
| Stability Grade | Pie Chart (PASS/FAIL/WARN) |

### Presentation
| Use Case | Recommended Chart |
|----------|-------------------|
| Trajectories | 3D Line + Animation |
| Field Surface | 3D Surface |
| Phase Space | 2D Scatter (x vs dx/dt) |
| Gallery Thumbnails | Static PNG export |

---

## ✅ Summary

| Category | Charts Available | Recommended for UET |
|----------|-----------------|---------------------|
| Basic | 5 | ✅ Line, Scatter |
| Statistical | 5 | ✅ Box, Histogram |
| Scientific | 5 | ✅ Heatmap, Contour |
| 3D | 5+ | ⭐ All (core feature) |
| Financial | 5 | ✅ Time Series |
| Maps | 5 | ⬜ Optional |
| AI/ML | 5 | ⬜ Optional |
| Animation | Yes | ⭐ Critical |

**Total: 40+ chart types, 15+ ที่เหมาะกับ UET Lab**

---

## 📚 Resources

- [Plotly Python Docs](https://plotly.com/python/)
- [Plotly.js Docs](https://plotly.com/javascript/)
- [Dash (Python App Framework)](https://dash.plotly.com/)
- [GitHub Source](https://github.com/plotly/plotly.py)
