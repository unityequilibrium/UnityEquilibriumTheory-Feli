# 🧠 UET Knowledge Base Client (`research_uet.knowledge_base`)

![Status](https://img.shields.io/badge/Status-ACTIVE-brightgreen)
![Client](https://img.shields.io/badge/Client-Python-blue)
![Integration](https://img.shields.io/badge/Integration-MCP_Bridge-orange)

> **"The Connector"** - ชุดเครื่องมือ (Python SDK) สำหรับเชื่อมต่อกับ `uet_kb` (Rust) และจัดการระบบ RAG ทั้งหมด.

---

## 🏛️ Components

| File | Purpose |
| :--- | :--- |
| **`config.toml`** | **Single Source of Truth** สำหรับ API Keys, Models, และ Budgets ทั้งหมด. |
| **`api_client.py`** | Client สำหรับคุยกับ OpenRouter พร้อมระบบ **Cost Tracking**. |
| **`vector_store.py`** | สะพานเชื่อม (Bridge) ไปยัง LanceDB/Postgres ผ่าน MCP. |
| **`ingest.py`** | Pipeline สำหรับอ่านไฟล์ `.md/.py` ทั้งหมด -> แปลงเป็น Vector -> ส่งเข้า Database. |
| **`tensorizer.py`** | แปลงเนื้อหาเอกสารเป็นค่า UET Vector ($\Omega, \kappa, \beta$). |

---

## 🔗 How it works

```mermaid
graph LR
    User["👤 Ingest Command"] --> Ingest["📥 ingest.py"]
    Ingest -->|Tensorize| Tensor["🧮 tensorizer.py"]
    Tensor -->|Upload| KB["🗄️ uet_kb (Rust)"]
    
    Agent["🤖 Agent"] -->|Query| Search["🔍 omega_search.py"]
    Search -->|Fetch| KB
    
    style Ingest fill:#e1bee7,stroke:#8e24aa
    style Search fill:#bbdefb,stroke:#1e88e5
```

---

## 🚀 Key Commands

**1. เริ่มกระบวนการนำเข้าข้อมูล (Ingestion):**
```bash
python -m research_uet.knowledge_base.ingest
```

**2. ดูรายงานค่าใช้จ่าย (Cost Dashboard):**
```bash
python -m research_uet.knowledge_base.cost_dashboard
```
