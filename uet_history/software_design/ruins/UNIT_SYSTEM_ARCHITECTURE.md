# Full Stack Unit System Mapping

> **Related Documents:**
> - [SMART_SYSTEM_DESIGN](design_system/SMART_SYSTEM_DESIGN.md) ← Smart Parameter System
> - [SMART_UNIT_COMPONENT](design_system/SMART_UNIT_COMPONENT.md) ← Unit Converter UI
> - [DATA_DICTIONARY](standards/DATA_DICTIONARY.md) ← All Unit Definitions
> - [DATABASE_SCHEMA](DATABASE_SCHEMA.md) ← Table Structures

> **Architecture Blueprint**
> Trace of the "Smart Unit" system from Database Storage $\to$ User Interface.

---

## 🏗️ 1. Architecture Overview (The Pipeline)

| Layer | Responsibility | Data State |
|:---|:---|:---|
| **Database (PostgreSQL)** | Storage of Definitions & Raw History | **Raw SI** (Immutable) |
| **Backend (API)** | Streaming & Aggregation | **Raw SI** (JSON) |
| **Frontend (Logic)** | Real-time Conversion & State | **Calculated** (Transient) |
| **UX / UI (React)** | Interaction & Visualization | **Formatted** (String) |

---

## 🗄️ 2. Database Layer (`schema.prisma`)

### 2.1 Metric Definitions (The "Truth")
The `MetricRegistry` table defines *what* can be measured.
- **Table**: `MetricRegistry`
- **Fields**:
  - `id`: `total_energy`, `mass` (The Code Key)
  - `unitCategory`: `QNT` (Enforces quantitative handling)
  - `unit`: `J`, `kg` (The **Storage Base Unit**)

### 2.2 Telemetry Storage (The "Data")
We **NEVER** store converted values (e.g., "Earths"). We only store immutable SI.
- **Table**: `TelemetrySample`
- **Fields**:
  - `value`: `Decimal` (e.g., `5.97e24`)
  - `metricId`: `mass`
- **Why?**: Allows us to change conversion formulas later without breaking old data.

---

## 🔌 3. Backend Layer (NestJS API)

### 3.1 Registry Endpoint
Delivers the Dictionary to the frontend at startup.
- **GET** `/api/registry`
- **Response**: Returns content matching `metrics.json`.

### 3.2 Telemetry Stream
Delivers raw numbers.
- **GET** `/api/runs/:id/telemetry`
- **Payload**: `{ t: 10.5, mass: 5.97e24, energy: 4.18e9 }`
- **Role**: Dumb pipe. Does NOT perform conversion (to save CPU).

---

## ⚛️ 4. Frontend Layer (React/TypeScript)

### 4.1 The Converter Engine (`UnitConverter.ts`)
A dedicated utility class that holds the "Lens" logic.
```typescript
const CONVERSION_TABLE = {
  mass: {
    base: 'kg',
    units: {
      earths: { label: 'Earths', factor: 1 / 5.97e24 },
      suns:   { label: 'Suns',   factor: 1 / 1.99e30 }
    }
  }
};
// Function: convert(value, 'kg', 'earths') -> value * factor
```

### 4.2 State Management (Zustand)
Stores the user's *current view preference*.
- **Store**: `useUnitStore`
- **State**: `preferences: { mass: 'earths', energy: 'tnt' }`
- **Effect**: If user changes `mass` to `Earths` on one screen, it applies globally (optional).

---

## 🖥️ 5. UX/UI Layer (Components)

### 5.1 The Smart Button Component (`SmartMetric.tsx`)
Connects the full stack into the single control.

1.  **Receive**: Props `{ metricId: 'mass', rawValue: 5.97e24 }`.
2.  **Lookup**: Check `useUnitStore` $\to$ User wants `'earths'`.
3.  **Convert**: Call `UnitConverter` $\to$ `1.0`.
4.  **Render**:
    - **Display**: `1.00`
    - **Button Label**: `Earths ▾`
    - **Checkbox**: `[✓]` (Toggled ON)

### 5.2 The Graph Component (`TelemetryGraph.tsx`)
- **Input**: Receives the *Unit Preference* from the Button.
- **Axis**: Updates Y-Axis Label to `Mass (Earths)`.
- **Data**: Scales the plotted line by the conversion factor visually.

---

## 🔄 Summary of Flow
1.  **DB** reads `5.97e24`.
2.  **API** sends `5.97e24`.
3.  **Frontend** receives `5.97e24`.
4.  **User** selects "Earths".
5.  **UI** calculates $5.97e24 \times (1/5.97e24) = 1.00$.
6.  **Screen** shows **`1.00 Earths`**.
