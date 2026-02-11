# UET Lab - Page Wiring Diagrams

> **UI-to-Backend Wiring Specification**  
> เอกสารแสดงโครงสร้างการเชื่อมโยงข้อมูลของแต่ละหน้าอย่างละเอียด  
> Reference: `ปัญหาที่ต้องปรับ.md` (Blueprint v0.3)

---

## 1. HOME PAGE (`/`) (Landing)

หน้าแรกสำหรับเลือกเข้า Lab หรือ Gallery

```mermaid
graph TD
    %% UI Layer
    UI_Home[Page: /] --> Hero[Hero Section]
    UI_Home --> Nav[Home Navigation]
    
    %% Components
    Hero -->|Click| Action_Enter[Enter Lab Button]
    Nav -->|Click| Action_Gallery[Gallery Link]
    
    %% Wiring
    Action_Enter -->|Link| Route_Lab[/lab]
    Action_Gallery -->|Link| Route_Gallery[/gallery]
```

---

## 2. GALLERY PAGE (`/gallery`)

หน้ารวม Presets และ Saved Runs สำหรับโหลดเข้า Lab

```mermaid
graph TD
    %% UI Layer
    UI_Gallery[Page: /gallery] --> Grid[Project Grid]
    UI_Gallery --> Filters[Filter Bar]
    
    %% Components
    Grid -->|iterate| Card[Project Card]
    Card -->|Info| Meta[Metadata Display]
    Card -->|Action| Btn_Load[Load Button]
    
    %% Data Wiring
    Filters -->|Query| Store_Gallery[Gallery Store]
    Store_Gallery -->|Fetch| API_Gallery_List[GET /api/projects]
    
    %% Action Wiring
    Btn_Load -->|Select| Action_Nav[Navigate to Lab]
    Action_Nav -->|URL Param| Route_Lab_Param[/lab?room={id}&preset={id}]
    
    %% Database Connection
    API_Gallery_List -.-> DB_Projects[(Table: projects)]
```

---

## 3. LAB PAGE (`/lab`) - THE CORE

หน้าที่ซับซ้อนที่สุด เชื่อมโยงระบบทั้งหมด (Single Shell Architecture)

```mermaid
graph TD
    %% Page Structure
    UI_Lab[Page: /lab] --> Shell[LabShell]
    
    %% --- SHELL LAYER ---
    subgraph Shell_Layer [Shell Components]
        Shell --> TopNav[Top Navigation]
        Shell --> Left[Left Output Panel]
        Shell --> Center[Center Room Router]
        Shell --> Right[Right Studio Panel]
        Shell --> Dock[Graph Dock]
    end
    
    %% --- TOP NAV WIRING ---
    TopNav --> Selector[Room Selector]
    TopNav --> Control_FPS[FPS Meter]
    TopNav --> Control_Settings[Settings Modal]
    
    Selector -->|Select| Router_State[Room State]
    Selector -->|Fetch| Registry_Room[Room Registry]
    
    %% --- CENTER ROUTER WIRING ---
    Center -->|Case: sim3d| Sim_Room[Sim3DRoom]
    Center -->|Case: test_terminal| Test_Room[TestTerminalRoom]
    
    %% --- SIM ROOM WIRING (Complex) ---
    subgraph Sim_Wiring [Simulation Data Flow]
        Sim_Room --> Canvas[WebGL Canvas]
        Sim_Room --> Engine[SimCoreV4]
        
        Engine -->|Telemetry| Service_Tel[Telemetry Service]
        Engine -->|Events| Bus_Events[Event Bus]
        
        Service_Tel -->|Batch| API_Tel[POST /api/telemetry]
        Bus_Events -->|Log| API_Evt[POST /api/events]
    end
    
    %% --- LEFT PANEL WIRING (Output) ---
    subgraph Left_Wiring [Output & Validation]
        Left --> MetricList[Metric Card List]
        Left --> ValStrip[Validation Strip]
        Left --> Inspector[Selection Inspector]
        Left --> Actions[Result Actions]
        
        %% Metric Card 1-1-1 Pattern
        MetricList -->|Map| Card[MetricCard]
        Card -->|Read| Registry_Metric[Metric Registry]
        Card -->|Data| Store_Tel[Telemetry Store]
        
        %% Actions
        Actions -->|Save| Action_Save[Save to DB]
        Actions -->|Export| Action_Export[Export File]
        
        Action_Save -->|POST| API_Save[/api/runs]
        Action_Export -->|Client| File_Gen[File Generator]
    end
    
    %% --- RIGHT PANEL WIRING (Input) ---
    subgraph Right_Wiring [Input & Control]
        Right --> Tab_Eq[Equations Tab]
        Right --> Tab_Par[Params Tab]
        Right --> Tab_Insp[Inspector Tab]
        Right --> Tab_Note[Notes Tab]
        
        %% Param Controls
        Tab_Par -->|Bind| Store_Params[Param Store]
        Store_Params -->|Update| Engine
        
        %% Notes System
        Tab_Note -->|List| List_Note[Note List]
        Tab_Note -->|Create| Btn_NewNote[+ New Note]
        Btn_NewNote -->|POST| API_Note_Create[/api/notes]
    end
    
    %% --- DOCK WIRING ---
    subgraph Dock_Wiring [Visualization]
        Dock -->|Select| Store_Select[Selection Store]
        Dock -->|Data| Store_Tel
        Dock -->|Render| Plotly[Plotly Graph]
        
        %% Auto-grouping logic
        Store_Select -->|Check| Registry_Metric
        Registry_Metric -->|Group| Logic_Group[Auto-Grouping Logic]
    end

    %% --- DATABASE LAYER ---
    API_Tel -.-> DB_Tel[(Table: telemetry_samples)]
    API_Evt -.-> DB_Evt[(Table: event_logs)]
    API_Save -.-> DB_Run[(Table: runs)]
    API_Note_Create -.-> DB_Note[(Table: notes)]
```

---

## 4. KEY DATA CONNECTIONS

สรุปการเชื่อมโยงข้อมูลสำคัญ

### 4.1 Metric System Linkage
1. **Definition**: `Metric Registry` (Source of Truth)
   - Defines: `unit`, `category` (QNT/QLT), `plot_group`
2. **Display**: `MetricCard`
   - Reads: Definition from Registry
   - Reads: Value from Telemetry Store
3. **Visualization**: `GraphDock`
   - Uses: `plot_group` from Registry to decide overlay/stack

### 4.2 Save System Linkage
1. **Trigger**: `Left Panel` > `Save Button`
2. **Collect**:
   - Run Metadata (from Store)
   - Current State (from Engine)
   - Telemetry History (from Service)
3. **Persist**: `POST /api/runs` -> `PostgreSQL`

### 4.3 Note System Linkage
1. **Trigger**: `Right Panel` > `Notes Tab` > `New Note`
2. **Context**: Captures current `t` (time) and `step` from Engine
3. **Persist**: `POST /api/notes` -> `PostgreSQL` (Table: `notes`)

---

** เอกสารนี้ใช้อ้างอิงในการ Wire ระบบจริงทั้งหมด **
