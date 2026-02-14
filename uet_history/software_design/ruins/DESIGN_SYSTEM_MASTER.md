# UET Lab - Design System Master

> **เอกสารมาตรฐานการออกแบบ UI/UX และ Architecture**  
> Linked to: `BLUEPRINT_MASTER.md`  
> Created: 2024-12-23

---

## 1. HIGH-LEVEL ARCHITECTURE DIAGRAM

แผนภาพแสดงความเชื่อมโยงของการออกแบบ Front-end ไปจนถึง Database ตามมาตรฐาน Single Shell Architecture

```mermaid
graph TD
    %% User Access Points
    User[User / Browser] -->|Visit /| Landing[Home Page]
    User -->|Visit /gallery| Gallery[Gallery Page]
    User -->|Visit /lab| LabShell[LabShell (Main App)]

    %% Generic Shell Structure
    subgraph Shell [Single Shell Architecture]
        style Shell fill:#1c1c22,stroke:#4ecdc4,stroke-width:2px
        
        LabShell --> TopNav
        LabShell --> LeftPanel[Left Output Panel]
        LabShell --> RightPanel[Right Studio Panel]
        LabShell --> Dock[Graph Dock]
        LabShell --> Router[Room Router]
        
        %% State & Context
        Context[AuthContext / AppState] -.-> LabShell
    end

    %% Room Content
    subgraph Rooms [Room Content (Variable)]
        Router -->|room=solarSystem| Sim3D[Sim3DRoom (Canvas)]
        Router -->|room=testGates| Terminal[TestTerminalRoom]
        
        Sim3D --> SimCore[SimCoreV4 (Engine)]
        Terminal --> TestRunner[Test Registry Runner]
    end

    %% Features & Components
    subgraph Features [Feature Sets]
        LeftPanel --> MetricList[MetricCardList]
        Dock --> GraphView[Recharts / GraphDock]
        RightPanel --> Controls[Param Controls]
        RightPanel --> Editor[Equation Editor]
    end

    %% Data Flow
    subgraph Backend [Backend Services]
        SimCore -->|Events| EventBus
        SimCore -->|Telemetry| TelService[Telemetry Service]
        
        TelService -->|Batch| API_Tel[/api/telemetry]
        EventBus -->|Logs| API_Events[/api/events]
        Controls -->|Save| API_Runs[/api/runs]
    end

    %% Database
    API_Tel --> DB[(PostgreSQL)]
    API_Events --> DB
    API_Runs --> DB
```

---

## 2. AESTHETIC & THEME STANDARDS (AppTokens)

เราใช้ **Premium Glassmorphism Dark Theme** เพื่อให้ความรู้สึก Modern & Scientific

### 2.1 Color Palette
- **Background**: `#0f0f14` (Deep Space Black)
- **Surface**: `#1c1c22` (Glassy Dark) with `backdrop-filter: blur(12px)`
- **Primary (C-Field)**: `#4ecdc4` (Cyan Teal) - ใช้สำหรับค่าที่ควบคุมได้ / Action หลัก
- **Secondary (I-Field)**: `#ff6b6b` (Soft Red) - ใช้สำหรับค่าผลลัพธ์ / Action รอง

### 2.2 Glassmorphism Rules
ทุก Panel ต้องใช้สูตรนี้:
```css
background: rgba(28, 28, 34, 0.7);
backdrop-filter: blur(12px);
border: 1px solid rgba(255, 255, 255, 0.08);
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
```

### 2.3 Typography
- **Font**: Inter (UI) + JetBrains Mono (Numbers/Code)
- **Scale**:
  - `text-xs` (12px): Labels, meta info
  - `text-sm` (14px): Body, values
  - `text-base` (16px): Headings, important data

  - `text-base` (16px): Headings, important data

### 2.4 Unit Display Standards (Smart Lens)
We use a **Contextual Lens System** to handle complex units.
- **Reference**: [`DATA_DICTIONARY.md`](../standards/DATA_DICTIONARY.md) (Master Registry)
- **UI Spec**: [`SMART_UNIT_COMPONENT.md`](SMART_UNIT_COMPONENT.md) (Smart Button Logic)

---

## 3. COMPONENT ARCHITECTURE & GAPS

วิเคราะห์ความเชื่อมโยงกับ `BLUEPRINT_MASTER.md`

### 3.1 LabShell (✅ Implemented)
- **Status**: สร้างแล้วใน `src/shell/LabShell.tsx`
- **Standard**: เป็น Container หลักที่หุ้มทุกอย่าง มี TopNav, Left/Right Panel placeholders
- **Connections**:
  - รับ `roomId` จาก URL/Props
  - เรียก `RoomRouter` เพื่อ render เนื้อหาตรงกลาง

### 3.2 Registries (✅ Implemented)
- **Status**: สร้างแล้วใน `src/registries/`
- **Standard**: `roomRegistry`, `testRegistry` ถูกต้อง
- **Gap**: ยังต้องย้าย `metricRegistry` จาก `lib/registry/` มาที่นี่

### 3.3 Feature Components (⚠️ Partial)
- **Status**: Components เก่ายังกระจัดกระจายอยู่ใน `components/lab/`
- **Standard**: ต้องย้ายเข้า `features/`
  - `MetricCard` -> `features/metrics/`
  - `GraphDock` -> `features/metrics/`
  - `LeftOutputPanel` -> `features/panels/`
- **Gap**: ต้องทำการ Migrate code เก่าให้เข้าโครงสร้างใหม่

### 3.4 Room Router (✅ Implemented)
- **Status**: สร้างแล้วใน `src/features/rooms/RoomRouter.tsx`
- **Standard**: Switch case ตาม `room.type` ถูกต้อง
- **Gap**: ยังต้อง wire เข้ากับ `/app/lab/page.tsx`

---

## 4. UI/UX STANDARD CHECKLIST

| Standard | Current Status | Action Item |
|----------|----------------|-------------|
| **Single Shell** | ✅ Created | Wire to `/lab` page |
| **Room Selector** | ⚠️ Partial | Add Dropdown in TopNav |
| **Glass Theme** | ✅ Defined | Apply `AppTokens` globally |
| **Metric Card** | ✅ 1-1-1 Pattern | Move to `features/metrics` |
| **Graph Dock** | ✅ Auto-grouping | Move to `features/metrics` |
| **Save/Export** | ⚠️ Logic exists | Ensure UI is ONLY in Left Panel |
| **Test Lab** | ❌ Route `/test-lab` | Merge into `/lab?room=testGates` |

---

## 5. REFACTORING ROADMAP (Next Steps)

เพื่อให้ UI/UX สมบูรณ์ตาม Blueprint:

1. **Wiring**: แก้ไข `/app/lab/page.tsx` ให้เรียกใช้ `<LabShell>`
2. **Migration**: ย้าย Components จาก `components/lab` -> `features/`
3. **Cleanup**: ลบโฟลเดอร์เก่า (`components/lab`, `/test-lab`)
4. **Verification**: ตรวจสอบ UI ว่าตรงตามกฎ Glassmorphism

---

** เอกสารนี้ใช้เป็น Reference ในการตรวจสอบ Standards ทั้งหมด **
