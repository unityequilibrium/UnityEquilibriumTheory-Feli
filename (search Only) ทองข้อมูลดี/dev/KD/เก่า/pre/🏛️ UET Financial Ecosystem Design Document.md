# 🏛️ UET Financial Ecosystem Design Document

**(ระบบนิเวศการเงินและตัวชี้วัดแบบ Fractal)**

## 1. ปรัชญาการออกแบบ (Design Philosophy)

ระบบการเงินของ UET ไม่ใช่แค่ "ระบบชำระเงิน (Payment Gateway)" แต่เป็น **"ระบบบริหารจัดการพลังงาน (Energy Management System)"** ของทั้งแพลตฟอร์ม โดยมีแนวคิดหลักคือ:

1. **Database as a Scorecard:** ทุกธุรกรรมที่เกิดขึ้นใน Database (Back-end) จะถูกนำมาประมวลผลเป็นกราฟและตัวชี้วัด (Front-end) ทันทีแบบ Real-time ไม่มีการทำรายงานมือ
    
2. **Fractal Economy:** โครงสร้างการบริหารจัดการเงินและ KPI จะเหมือนกันในทุกระดับชั้น (Platform $\to$ Project $\to$ User)
    
3. **Transparency:** ความโปร่งใสของข้อมูลการเงินคือหัวใจสำคัญที่ทำให้เกิดความเชื่อมั่น (Trust)
    

## 2. โครงสร้างสกุลเงิน (Dual-Currency Architecture)

เราแยกระบบเงิน "คงที่" กับเงิน "ผันแปร" ออกจากกันเพื่อเสถียรภาพ:


| **ประเภท** | **ชื่อเรียก**       | **หน้าที่หลัก**             | **ลักษณะทางเทคนิค**                                                              |
| ---------- | ------------------- | --------------------------- | -------------------------------------------------------------------------------- |
| **Stable** | **UET Credit (UC)** | ใช้แทนเงินสด (1 UC ≈ 1 THB) | เก็บใน Digital Wallet, ใช้ Donate, ซื้อ Service, ไม่มีวันหมดอายุ                 |
| **Energy** | **AI Token (AT)**   | ใช้เป็น "เชื้อเพลิง" รัน AI | ผันแปรตามโมเดล AI ที่เลือกใช้, ถูก "เผา (Burn)" ทิ้งเมื่อใช้งาน, มีเรทแลกเปลี่ยน |

Flow การเงิน:

เงินบาท (QR Payment) $\xrightarrow{\text{Top Up}}$ UET Credit (UC) $\xrightarrow{\text{Exchange}}$ AI Token (AT) $\xrightarrow{\text{Usage}}$ Burn

## 3. The Balanced Scorecard Logic (จาก Database สู่ KPI)

เนื่องจาก Database เราเก็บ Log ละเอียดอยู่แล้ว เราจะ Map ข้อมูลดิบเข้าสู่มุมมอง Balanced Scorecard (BSC) 4 ด้าน ดังนี้:

### 🌐 ระดับที่ 1: Platform Level (ภาพรวมทั้งระบบ)

_เป้าหมาย: ความยั่งยืนของระบบนิเวศ (Ecosystem Sustainability)_


| **มุมมอง (Perspective)**    | **KPI / ตัวชี้วัด**                                                                                                                                                                              | **ดึงจาก Database Table ไหน?**                                                                                |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| **Financial** (การเงิน)     | - **Total Revenue:** รายได้รวมจากการเติมเงิน<br><br>  <br><br>- **Burn Rate:** อัตราการเผา Token (แสดงถึงการใช้งานจริง)<br><br>  <br><br>- **Exchange Spread Profit:** กำไรจากส่วนต่างแลกเปลี่ยน | `transactions` (type='topup')<br><br>  <br><br>`usage_logs`<br><br>  <br><br>`transactions` (type='exchange') |
| **Customer** (ผู้ใช้)       | - **Active Donors:** จำนวนคนที่บริจาคซ้ำ<br><br>  <br><br>- **User Retention:** ผู้ใช้ที่กลับมา Top-up ต่อเนื่อง                                                                                 | `users` JOIN `transactions`<br><br>  <br><br>`login_logs`                                                     |
| **Internal Process** (ระบบ) | - **Server Cost Efficiency:** ต้นทุน Server ต่อ 1 ล้าน Token<br><br>  <br><br>- **System Uptime:** ความเสถียรของระบบ                                                                             | `server_logs` vs `usage_logs`<br><br>  <br><br>`system_health`                                                |
| **Learning** (การเติบโต)    | - **Total Knowledge Created:** จำนวน Note/Theory ใหม่<br><br>  <br><br>- **New Project Growth:** อัตราการเกิดโปรเจกต์ใหม่                                                                        | `notebooks`<br><br>  <br><br>`projects`                                                                       |

### 🚀 ระดับที่ 2: Project Level (Mini-App / Lab)

_เป้าหมาย: ความสำเร็จของโครงการและการระดมทุน (Project Viability)_


| **มุมมอง (Perspective)**     | **KPI / ตัวชี้วัด**                                                                                                                        | **ดึงจาก Database Table ไหน?**                                      |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| **Financial** (การเงิน)      | - **Funding Progress:** ยอดบริจาค vs เป้าหมาย (UC)<br><br>  <br><br>- **Runway:** Token ที่เหลือพอให้ AI รันงานได้กี่วัน                   | `wallets` (project_id)<br><br>  <br><br>`usage_logs` (avg usage)    |
| **Customer** (ผู้สนับสนุน)   | - **Supporter Count:** จำนวนคนที่มา Donate<br><br>  <br><br>- **Community Engagement:** ยอด Comment/Share ในโปรเจกต์                       | `transactions` (type='donate')<br><br>  <br><br>`posts`, `comments` |
| **Internal Process** (ผลงาน) | - **AI Output Rate:** ปริมาณงานที่ AI ผลิตได้ (บทความ/โค้ด)<br><br>  <br><br>- **Task Completion:** งานที่ทำเสร็จใน Kanban                 | `usage_logs`<br><br>  <br><br>`tasks`                               |
| **Learning** (องค์ความรู้)   | - **Theory Contribution:** จำนวน Theory ที่ Publish ออกสู่ส่วนกลาง<br><br>  <br><br>- **Citation Count:** จำนวนครั้งที่ Project ถูกอ้างอิง | `theories`<br><br>  <br><br>`citations`                             |

### 👤 ระดับที่ 3: Personal Level (Me Inc.)

_เป้าหมาย: การเติบโตและการมีส่วนร่วมส่วนบุคคล (Self-Growth)_


| **มุมมอง (Perspective)**     | **KPI / ตัวชี้วัด**                                                                                                               | **ดึงจาก Database Table ไหน?**                                      |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Financial** (กระเป๋าตังค์) | - **Total Contribution:** ยอดเงินที่บริจาคไปทั้งหมด<br><br>  <br><br>- **Spending History:** กราฟวงกลมแยกประเภทรายจ่าย            | `transactions` (user_id)<br><br>  <br><br>`transactions` (category) |
| **Customer** (สังคม)         | - **Reputation Score:** คะแนนชื่อเสียงจากการช่วยตอบคำถาม<br><br>  <br><br>- **Network:** จำนวนเพื่อนหรือ Project ที่เข้าร่วม      | `user_reputation`<br><br>  <br><br>`project_members`                |
| **Internal Process** (วินัย) | - **Learning Streak:** จำนวนวันที่เข้าใช้งานต่อเนื่อง<br><br>  <br><br>- **Goal Achievement:** เปอร์เซ็นต์ KPI ส่วนตัวที่ทำสำเร็จ | `daily_logins`<br><br>  <br><br>`user_goals`                        |
| **Learning** (ความรู้)       | - **Research Volume:** ปริมาณ Token ที่ใช้เพื่อการศึกษา<br><br>  <br><br>- **Skill Badges:** เหรียญตราที่ได้รับ                   | `usage_logs`<br><br>  <br><br>`user_badges`                         |

## 4. Technical Implementation (โครงสร้าง Database)

เพื่อให้ระบบข้างต้นทำงานได้ เราต้องมี Table หลักที่ออกแบบมาเพื่อรองรับ Query แบบ Scorecard โดยเฉพาะ:

```
-- 1. Wallets (กระเป๋าเงินรวมศูนย์: เป็นของ User หรือ Project ก็ได้)
CREATE TABLE wallets (
    id UUID PRIMARY KEY,
    owner_id UUID NOT NULL, -- User ID หรือ Project ID
    owner_type VARCHAR(20), -- 'USER', 'PROJECT', 'PLATFORM'
    credit_balance DECIMAL(18, 2) DEFAULT 0, -- เงินบาท (UC)
    token_balance DECIMAL(18, 2) DEFAULT 0,  -- Token (AT)
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. Transactions (สมุดบัญชีแยกประเภท: บันทึกทุกอย่างที่เปลี่ยนมือ)
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    from_wallet_id UUID,   -- ต้นทาง (NULL ถ้าเป็นการเติมเงินเข้าระบบ)
    to_wallet_id UUID,     -- ปลายทาง (NULL ถ้าเป็นการจ่ายออกนอกระบบ)
    amount DECIMAL(18, 2),
    currency VARCHAR(10),  -- 'UC', 'AT'
    type VARCHAR(30),      -- 'TOPUP', 'DONATE', 'EXCHANGE', 'USAGE_BURN'
    category VARCHAR(50),  -- 'Education', 'Infrastructure', 'Charity' (ใช้ทำกราฟวงกลม)
    metadata JSONB,        -- เก็บรายละเอียดเพิ่ม เช่น { "project_kpi_ref": "KPI-001" }
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Goals & Metrics (ตารางเก็บเป้าหมายเพื่อทำ Scorecard)
CREATE TABLE goals (
    id UUID PRIMARY KEY,
    owner_id UUID,
    type VARCHAR(20),      -- 'FINANCIAL', 'LEARNING', 'SOCIAL'
    target_value DECIMAL,  -- ค่าเป้าหมาย (เช่น 50,000 UC)
    current_value DECIMAL, -- ค่าปัจจุบัน (Update อัตโนมัติจาก Transaction Trigger)
    status VARCHAR(20),    -- 'ON_TRACK', 'WARNING', 'CRITICAL'
    deadline TIMESTAMP
);
```

## 5. บทสรุปการใช้งานจริง

เมื่อ User เข้ามาที่หน้า **"Financial Console"**:

1. **System Query:** ระบบจะดึงข้อมูลจาก `Transactions` และ `Goals` ตาม `owner_id` ของ User นั้นๆ
    
2. **Processing:** คำนวณผลต่าง (Variance) ระหว่างเป้าหมาย vs ความจริง
    
3. **Visualization:** แสดงผลเป็น Dashboard (เขียว/เหลือง/แดง) ทันที
    

นี่คือระบบที่ **"Data-Driven"** อย่างแท้จริง ไม่ต้องมีการกรอกข้อมูลหลอก ทุกอย่างสะท้อนจากการกระทำจริงในระบบครับ

# 🏛️ UET Financial Ecosystem Design Document (Global Premium Edition)

**(พิมพ์เขียวระบบการเงินสำหรับแพลตฟอร์มวิจัยระดับโลก)**

## 1. ปรัชญาการออกแบบ (Design Philosophy)

- **Premium & Clean:** ใช้หน่วยเงินที่มีมูลค่าสูง (High Value Currency) เพื่อภาพลักษณ์ที่น่าเชื่อถือ ไม่เฟ้อ และหน้าจอสะอาดตา
- **Pay-as-you-Scale:** จ่ายจริงตามที่ใช้ (Fair Usage) ไม่บังคับ Subscription ผูกมัด แต่รองรับการใช้งานต่อเนื่อง
- **Curated Workspace:** การจ่ายเงินคือการเข้าถึงเครื่องมือ (Tools) และสังคมคุณภาพ (Quality Network) ที่คัดกรองแล้ว ต่างจาก Social Platform ทั่วไป
- **Database as a Scorecard:** ใช้ Data ธุรกรรมจริงในการวัดผล KPI (Real-time Transparency)

## 2. โครงสร้างสกุลเงิน (High Value Architecture)

เราใช้โมเดล **"Gold Standard"** โดยอิงค่าเงินกับ USD เป็นหลักเพื่อให้ง่ายต่อการจัดการต้นทุน Global Server/AI


| **หน่วยเงิน**       | **มูลค่าอ้างอิง (Pegging)** | **เหตุผลทางจิตวิทยา**                                                                                  |
| ------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------ |
| **UET Credit (UC)** | **1 UC ≈ $10.00 USD**       | ทำให้หน่วยเงินดูมีมูลค่าสูง (Premium), ตัวเลขในหน้าจอดูไม่เยอะ (Minimalist), เหมาะกับการถือครองระยะยาว |
| **AI Token (AT)**   | **1,000 AT ≈ 0.001 UC**     | หน่วยย่อยสำหรับ "เผา" รันงาน AI (ละเอียดถึงทศนิยม)                                                     |

**ตัวอย่างการแสดงผลราคา (Pricing Example):**

- เติมเงิน $100 $\rightarrow$ ได้รับ **10.00 UC**
- ค่า AI Model (GPT-4o) ต่อ 1M Token ($5) $\rightarrow$ หัก **0.50 UC**
- ค่า AI Model (Flash/Mini) ต่อ 1M Token ($0.15) $\rightarrow$ หัก **0.015 UC**
- บริจาคให้โปรเจกต์ (Micro-donation) $\rightarrow$ **0.10 UC** ($1)
## 3. Global Payment & Compliance (Stripe Integration)

ใช้ **Stripe** เป็น Gateway หลักเจ้าเดียวเพื่อจบทุกปัญหา:

1. **Multi-Currency In:**
    - 🇺🇸 User จ่าย USD
    - 🇹🇭 User จ่าย THB (ตัดบัตร หรือ PromptPay via Stripe)
    - 🇪🇺 User จ่าย EUR
    - $\rightarrow$ **ระบบแปลงเข้าบัญชีเราเป็น USD** $\rightarrow$ **Convert เป็น UC ให้ User**
        
2. **Tax Invoice / Receipt:**
    - ระบบ Generate ใบเสร็จรับเงินอัตโนมัติ (PDF) ระบุชื่อองค์กร/ที่อยู่ได้ (สำคัญมากสำหรับการเบิกงบวิจัย)
        
3. **Minimum Load:**
    - เพื่อป้องกันค่าธรรมเนียมกินหมด ควรกำหนดเติมขั้นต่ำที่ **1 UC ($10)**

## 4. The Balanced Scorecard Logic (Updated for High Value)

### 🚀 ระดับ Project Level (Mini-App / Lab)

_เพิ่มฟีเจอร์การเงินสำหรับทีมวิจัย_


| **มุมมอง**    | **KPI / ฟีเจอร์ใหม่**                                                                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Financial** | - **Project Wallet:** กระเป๋ากลางของโปรเจกต์<br>- **Allowance System:** หัวหน้าทีม (Admin) จำกัดงบลูกทีมได้ (เช่น Max 0.05 UC/day)<br>- **Burn Rate Analysis:** กราฟแสดงการใช้เงินเทียบกับความคืบหน้างาน |
| **Customer**  | - **Supporter Tier:** แบ่งระดับคนบริจาค (e.g., Gold Donor > 5 UC)                                                                                                                                        |

### 👤 ระดับ Personal Level (Me Inc.)

_เพิ่มฟีเจอร์ติดตามค่าใช้จ่ายละเอียด_


| **มุมมอง**    | **KPI / ฟีเจอร์ใหม่**                                                                                                                                                                |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Financial** | - **Expense Categorization:** แยกหมวดหมู่: ค่า AI (RAG), ค่า Storage, ค่า Donate<br>- **Decimal View:** UI แสดงทศนิยม 4 ตำแหน่ง (เช่น 10.0045 UC) เมื่อเอาเมาส์ไปชี้ เพื่อความแม่นยำ |

## 5. UI/UX Strategy for "High Value Currency"

### 5.1 การแสดงผลตัวเลข (Decimal Handling)

เนื่องจาก 1 UC มีค่ามาก ($10) การแสดงผลทศนิยมจึงสำคัญ:

- **Dashboard View:** แสดง 2 ตำแหน่งเน้นความสวยงาม (e.g., **12.50 UC**)
- **Transaction/Micro View:** แสดง 4 ตำแหน่งเมื่อจำเป็น (e.g., Cost: **-0.0015 UC**)
- **Visual Cue:** ใช้สีที่ดู "แพง" (เช่น สีทอง, Emerald Green, หรือ Platinum) สำหรับหน่วย UC

### 5.2 Flow การเติมเงิน

1. User กด **"Top Up"**
2. เลือก Package (เน้นความคุ้มค่า):
    
    - 🥈 **Starter:** 1 UC ($10)
    - 🥇 **Pro:** 5 UC ($50) + แถม Token ฟรีนิดหน่อย
    - 💎 **Lab:** 20 UC ($200) + ออกใบกำกับภาษีเต็มรูปแบบ
        
3. Stripe Popup ขึ้นมา $\rightarrow$ จ่ายเงิน $\rightarrow$ UC เข้าทันที

## 6. Technical Schema Update (Database)

เพิ่ม Field เพื่อรองรับระบบ Invoice และ Allowance

```
-- อัปเดตตาราง Wallets
ALTER TABLE wallets 
ADD COLUMN currency_code VARCHAR(3) DEFAULT 'USD', -- Base Currency
ADD COLUMN settings JSONB; -- เก็บ config เช่น { "allowance_per_member": 0.05 }

-- เพิ่มตาราง Invoices (สำหรับการเบิกงบ)
CREATE TABLE invoices (
    id UUID PRIMARY KEY,
    user_id UUID,
    transaction_id UUID,
    amount_fiat DECIMAL, -- ยอดเงินจริง (USD/THB)
    currency_fiat VARCHAR(3),
    tax_info JSONB, -- ชื่อที่อยู่บริษัท/มหาลัย
    stripe_receipt_url VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 🛡️ Why This Works? (บทวิเคราะห์)

1. **Psychological Anchor:** การตั้ง 1 UC = $10 ทำให้ User คิดก่อนใช้ (Mindful Spending) ซึ่งตรงกับจริตนักวิจัยที่ต้องการความคุ้มค่า
2. **Global Ready:** ฐาน $10 เป็นตัวเลขที่ Universal มาก (ประมาณข้าว 1 มื้อใน US/Europe หรือหนังสือ 1 เล่มในไทย)
3. **Low Friction:** การใช้ Stripe เจ้าเดียว ลดความปวดหัวเรื่องการเชื่อมต่อธนาคารแต่ละประเทศ และได้ฟีเจอร์ออกบิลฟรี
 

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UET Finance Console (Global Premium)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Chart.js for beautiful charts -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Prompt', sans-serif; }
        .glass-panel {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(229, 231, 235, 0.5);
        }
        .burn-warning { animation: pulse-red 2s infinite; }
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .tab-active {
            border-bottom: 3px solid #10b981;
            color: #10b981;
            font-weight: 600;
        }
        .tab-inactive {
            border-bottom: 3px solid transparent;
            color: #64748b;
        }
        .tab-inactive:hover { color: #334155; }
        
        /* Premium Gradients */
        .bg-gradient-premium { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }
        .text-gradient-gold {
            background: linear-gradient(to right, #fbbf24, #d97706);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="bg-slate-50 text-slate-800">

    <!-- Navbar -->
    <nav class="bg-slate-900 text-white px-6 py-3 flex justify-between items-center sticky top-0 z-50 shadow-lg">
        <div class="flex items-center space-x-6">
            <div class="font-bold text-xl tracking-wider text-emerald-400 flex items-center">
                <i class="fa-solid fa-layer-group mr-2"></i>
                <span>UET <span class="text-white font-light">Finance</span></span>
            </div>
            <div class="hidden md:flex space-x-1 text-sm text-slate-400">
                <a href="#" class="px-3 py-2 hover:text-white transition">Home</a>
                <a href="#" class="px-3 py-2 hover:text-white transition">Theory</a>
                <a href="#" class="px-3 py-2 hover:text-white transition">Projects</a>
                <a href="#" class="px-3 py-2 text-white bg-slate-800 rounded-md">Donate & Assets</a>
                <a href="#" class="px-3 py-2 hover:text-white transition">Community</a>
            </div>
        </div>
        <div class="flex items-center space-x-4">
            <span class="bg-indigo-600 text-[10px] px-2 py-1 rounded-full uppercase tracking-wide font-bold shadow-glow border border-indigo-400">
                Research Lab
            </span>
            <div class="flex items-center space-x-2 cursor-pointer hover:bg-slate-800 px-2 py-1 rounded transition">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Santa" class="w-8 h-8 rounded-full border-2 border-slate-700 bg-slate-800">
                <div class="text-xs text-right hidden sm:block">
                    <p class="font-bold text-white">Dr. Santa</p>
                    <p class="text-slate-400">Me Inc.</p>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">

        <!-- Header -->
        <div class="flex justify-between items-end mb-2">
            <div>
                <h1 class="text-2xl font-bold text-slate-800">Financial Console</h1>
                <p class="text-slate-500 text-sm">Energy Management System (High Value Currency Standard)</p>
            </div>
            <div class="text-right hidden md:block">
                <p class="text-xs text-emerald-600 font-semibold mb-1"><i class="fa-solid fa-circle-check mr-1"></i>System Operational</p>
                <p class="text-[10px] text-slate-400">Rate: 1 UC ≈ $10.00 USD</p>
            </div>
        </div>

        <!-- ZONE 1: Personal Wallet (Premium View) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <!-- 1.1 UET Credits (The Gold Standard) -->
            <div class="bg-white rounded-xl p-5 shadow-sm border-l-4 border-emerald-600 relative overflow-hidden group hover:shadow-md transition">
                <div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition">
                    <i class="fa-solid fa-vault text-8xl text-emerald-800"></i>
                </div>
                <div>
                    <p class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest mb-1">My UET Credits (UC)</p>
                    <div class="flex items-baseline space-x-2">
                        <h2 class="text-4xl font-bold text-slate-800 tracking-tight" id="creditBalance">12.50</h2>
                        <span class="text-sm font-medium text-slate-400">UC</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-1">≈ $125.00 USD (High Value)</p>
                </div>
                <div class="mt-5">
                    <button onclick="openModal('topupModal')" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-2 px-4 rounded-lg text-sm font-medium shadow-sm transition flex items-center justify-center">
                        <i class="fa-solid fa-plus-circle mr-2"></i> Top Up Package
                    </button>
                </div>
            </div>

            <!-- 1.2 AI Tokens (Energy Source) -->
            <div class="bg-white rounded-xl p-5 shadow-sm border-l-4 border-amber-500 relative overflow-hidden group hover:shadow-md transition">
                <div class="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition">
                    <i class="fa-solid fa-bolt text-8xl text-amber-600"></i>
                </div>
                <div>
                    <p class="text-[10px] font-bold text-amber-600 uppercase tracking-widest mb-1">AI Tokens (Energy)</p>
                    <div class="flex items-baseline space-x-2">
                        <h2 class="text-4xl font-bold text-slate-800 tracking-tight" id="tokenBalance">2.4M</h2>
                        <span class="text-sm font-medium text-slate-400">AT</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-1">Enough for ~240 Research Queries</p>
                </div>
                <div class="mt-5 flex space-x-2">
                     <button onclick="document.getElementById('exchangeInput').focus()" class="flex-1 bg-slate-50 hover:bg-slate-100 text-slate-700 py-2 px-4 rounded-lg text-sm font-medium border border-slate-200 transition">
                        Manage Energy
                    </button>
                </div>
            </div>

            <!-- 1.3 Exchange Center -->
            <div class="bg-gradient-premium rounded-xl p-5 shadow-lg text-white relative flex flex-col justify-between border border-slate-700">
                 <div>
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-sm font-bold text-slate-200"><i class="fa-solid fa-right-left mr-2"></i>Quick Exchange</h3>
                        <span class="text-[10px] bg-slate-800/80 px-2 py-0.5 rounded text-emerald-400 border border-slate-700">1 UC = 1M AT</span>
                    </div>
                    
                    <div class="space-y-3">
                        <div class="relative">
                            <label class="text-[10px] text-slate-400 absolute -top-2 left-2 bg-slate-800 px-1">From (UC)</label>
                            <input type="number" id="exchangeInput" value="1.00" step="0.01" class="w-full bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-emerald-500" oninput="calculateExchange()">
                        </div>
                        <div class="flex justify-center text-slate-500 text-xs"><i class="fa-solid fa-arrow-down"></i></div>
                        <div class="flex justify-between items-center bg-slate-800/50 p-2 rounded-lg border border-slate-700 border-dashed">
                            <span class="text-xs text-slate-400">Receive:</span>
                            <span class="font-mono text-emerald-400 font-bold" id="exchangeOutput">1,000,000 <span class="text-[10px] text-slate-500">AT</span></span>
                        </div>
                    </div>
                 </div>
                 <button class="w-full mt-3 bg-emerald-600 hover:bg-emerald-500 text-white py-2 rounded-lg text-sm font-medium transition shadow-lg shadow-emerald-900/50" onclick="executeExchange()">
                    Confirm Conversion
                </button>
            </div>
        </div>

        <!-- ZONE 2: Tab Switcher (Fractal Levels) -->
        <div class="flex border-b border-slate-200 mb-4 overflow-x-auto">
            <button onclick="changeView('projects')" id="tabProjects" class="tab-active py-2 px-4 text-sm focus:outline-none transition whitespace-nowrap">
                <i class="fa-solid fa-flask mr-2"></i>Project Scorecards
            </button>
            <button onclick="changeView('personal')" id="tabPersonal" class="tab-inactive py-2 px-4 text-sm focus:outline-none transition whitespace-nowrap">
                <i class="fa-solid fa-user-astronaut mr-2"></i>Me Inc. (Personal KPI)
            </button>
            <button onclick="changeView('platform')" id="tabPlatform" class="tab-inactive py-2 px-4 text-sm focus:outline-none transition whitespace-nowrap">
                <i class="fa-solid fa-globe mr-2"></i>Platform Health
            </button>
        </div>

        <!-- ZONE 3: Dynamic Views -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
            
            <!-- VIEW A: PROJECTS (Lab/Team View) -->
            <div id="viewProjects" class="lg:col-span-3 space-y-6">
                 <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                    <div class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
                        <h3 class="font-bold text-slate-800">Active Research Funding</h3>
                        <div class="flex space-x-2">
                            <button class="text-xs text-slate-500 hover:text-indigo-600 flex items-center bg-white border border-slate-200 px-2 py-1 rounded shadow-sm">
                                <i class="fa-solid fa-file-invoice-dollar mr-1"></i> Export Tax Invoice
                            </button>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left">
                            <thead class="text-xs text-slate-500 uppercase bg-slate-50 border-b border-slate-100">
                                <tr>
                                    <th class="px-6 py-3">Project / Lab</th>
                                    <th class="px-6 py-3 text-center">Target (UC)</th>
                                    <th class="px-6 py-3 text-center">Funded</th>
                                    <th class="px-6 py-3 text-center">Daily Allowance</th>
                                    <th class="px-6 py-3 text-center">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-100">
                                <tr class="hover:bg-slate-50 transition">
                                    <td class="px-6 py-4">
                                        <div class="flex items-center space-x-3">
                                            <div class="w-10 h-10 rounded-lg bg-indigo-100 text-indigo-600 flex items-center justify-center text-lg"><i class="fa-solid fa-brain"></i></div>
                                            <div>
                                                <div class="font-bold text-slate-800">Cognitive RAG</div>
                                                <div class="text-[10px] text-emerald-600 bg-emerald-50 px-1 rounded inline-block">Active Research</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 text-center font-mono text-slate-600">5,000 UC</td>
                                    <td class="px-6 py-4">
                                        <div class="flex justify-between text-[10px] mb-1"><span>4,250 UC</span><span class="text-emerald-600">85%</span></div>
                                        <div class="w-full bg-slate-100 rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 85%"></div></div>
                                    </td>
                                    <td class="px-6 py-4 text-center">
                                        <div class="text-xs text-slate-500"><i class="fa-solid fa-lock mr-1"></i>0.50 UC/Member</div>
                                    </td>
                                    <td class="px-6 py-4 text-center"><button class="bg-slate-900 text-white px-3 py-1.5 rounded text-xs hover:bg-indigo-600 shadow-sm transition" onclick="donateToProject('Cognitive RAG')">Donate</button></td>
                                </tr>
                                <!-- More rows... -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- VIEW B: ME INC. (New Personal Scorecard) -->
            <div id="viewPersonal" class="hidden lg:col-span-3 space-y-6">
                <!-- KPI Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex justify-between items-start mb-2">
                            <div class="bg-blue-100 text-blue-600 w-8 h-8 rounded flex items-center justify-center"><i class="fa-solid fa-book"></i></div>
                            <span class="text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full">On Track</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-500 uppercase">Learning Goal</h4>
                        <p class="text-sm font-bold mt-1">Finish 5 Theory Modules</p>
                        <div class="mt-3 text-xs text-slate-400">Progress: 3/5</div>
                        <div class="w-full bg-slate-100 rounded-full h-1 mt-1"><div class="bg-blue-500 h-1 rounded-full" style="width: 60%"></div></div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex justify-between items-start mb-2">
                            <div class="bg-purple-100 text-purple-600 w-8 h-8 rounded flex items-center justify-center"><i class="fa-solid fa-microscope"></i></div>
                            <span class="text-[10px] bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">Ongoing</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-500 uppercase">Research Volume</h4>
                        <p class="text-sm font-bold mt-1">Use 500k AI Tokens</p>
                        <div class="mt-3 text-xs text-slate-400">Progress: 120k/500k</div>
                        <div class="w-full bg-slate-100 rounded-full h-1 mt-1"><div class="bg-purple-500 h-1 rounded-full" style="width: 24%"></div></div>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                        <div class="flex justify-between items-start mb-2">
                            <div class="bg-pink-100 text-pink-600 w-8 h-8 rounded flex items-center justify-center"><i class="fa-solid fa-heart"></i></div>
                            <span class="text-[10px] bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">Need Action</span>
                        </div>
                        <h4 class="text-xs font-bold text-slate-500 uppercase">Contribution</h4>
                        <p class="text-sm font-bold mt-1">Donate 50 UC</p>
                        <div class="mt-3 text-xs text-slate-400">Progress: 12.5/50</div>
                        <div class="w-full bg-slate-100 rounded-full h-1 mt-1"><div class="bg-pink-500 h-1 rounded-full" style="width: 25%"></div></div>
                    </div>
                </div>

                <!-- Personal Expense Chart -->
                <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
                    <h3 class="font-bold text-slate-800 mb-4">My Resource Allocation</h3>
                    <div class="h-64">
                         <canvas id="personalExpenseChart"></canvas>
                    </div>
                </div>
            </div>

            <!-- VIEW C: PLATFORM (Treasury View) -->
            <div id="viewPlatform" class="hidden lg:col-span-3 space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="bg-slate-900 rounded-xl p-6 text-white relative overflow-hidden">
                        <div class="absolute right-0 top-0 p-6 opacity-10"><i class="fa-solid fa-building-columns text-9xl"></i></div>
                        <h3 class="text-sm font-bold text-slate-400 uppercase">Platform Treasury Fund</h3>
                        <p class="text-4xl font-bold mt-2">854,120 <span class="text-lg font-normal text-slate-400">UC</span></p>
                        <p class="text-xs text-emerald-400 mt-2"><i class="fa-solid fa-arrow-trend-up"></i> +5.4% Growth (MoM)</p>
                        <div class="mt-6 flex space-x-2">
                            <span class="text-xs bg-slate-800 px-2 py-1 rounded border border-slate-700">Reserve: 60%</span>
                            <span class="text-xs bg-slate-800 px-2 py-1 rounded border border-slate-700">Dev Grant: 30%</span>
                            <span class="text-xs bg-slate-800 px-2 py-1 rounded border border-slate-700">Ops: 10%</span>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl p-6 border border-slate-200">
                        <h3 class="text-sm font-bold text-slate-500 uppercase mb-4">System Burn Rate (24h)</h3>
                        <div class="flex items-end space-x-2 h-32">
                             <div class="w-1/6 bg-rose-200 rounded-t h-[40%]"></div>
                             <div class="w-1/6 bg-rose-300 rounded-t h-[60%]"></div>
                             <div class="w-1/6 bg-rose-400 rounded-t h-[30%]"></div>
                             <div class="w-1/6 bg-rose-500 rounded-t h-[80%] relative group">
                                <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-800 text-white text-[10px] px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition whitespace-nowrap">Peak: 12M AT</div>
                             </div>
                             <div class="w-1/6 bg-rose-400 rounded-t h-[50%]"></div>
                             <div class="w-1/6 bg-rose-300 rounded-t h-[45%]"></div>
                        </div>
                        <p class="text-xs text-center text-slate-400 mt-2">00:00 - 24:00 (UTC)</p>
                    </div>
                </div>
            </div>

            <!-- RIGHT SIDEBAR (Live Log) -->
            <div class="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col h-full lg:col-span-1">
                <h3 class="text-xs font-bold text-slate-500 uppercase mb-3 flex justify-between items-center">
                    <span>Live Ledger</span>
                    <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
                </h3>
                <div class="flex-1 overflow-y-auto space-y-3 pr-2 max-h-[600px]" id="transactionLog">
                    <div class="bg-white p-3 rounded border border-slate-100 shadow-sm text-xs">
                        <div class="flex justify-between mb-1"><span class="font-bold text-indigo-600">@Dr.Santa</span><span class="text-slate-400">Now</span></div>
                        <p class="text-slate-600">Burned <span class="font-bold text-rose-500">1,200 AT</span> (Notebook #42)</p>
                    </div>
                     <div class="bg-white p-3 rounded border border-slate-100 shadow-sm text-xs">
                        <div class="flex justify-between mb-1"><span class="font-bold text-slate-600">@User_99</span><span class="text-slate-400">2m ago</span></div>
                        <p class="text-slate-600">Top-up <span class="font-bold text-emerald-600">5.00 UC</span> (Pro Pack)</p>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Modal: Top Up Packages -->
    <div id="topupModal" class="fixed inset-0 bg-black/60 z-[100] hidden flex items-center justify-center backdrop-blur-sm">
        <div class="bg-white rounded-xl shadow-2xl p-6 w-[600px] relative transform transition-all scale-100">
            <button onclick="closeModal('topupModal')" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
            
            <div class="text-center mb-6">
                <h3 class="text-xl font-bold text-slate-800">Add Funds</h3>
                <p class="text-sm text-slate-500">Secure Global Payment via Stripe (USD Base)</p>
            </div>

            <div class="grid grid-cols-3 gap-4">
                <!-- Starter -->
                <div class="border border-slate-200 rounded-xl p-4 hover:border-emerald-500 cursor-pointer transition text-center group">
                    <div class="text-2xl mb-2">🥈</div>
                    <h4 class="font-bold text-slate-700">Starter</h4>
                    <p class="text-2xl font-bold text-emerald-600 my-2">1.00 <span class="text-xs text-slate-400">UC</span></p>
                    <p class="text-xs text-slate-400 mb-3">≈ $10 USD</p>
                    <button class="w-full bg-slate-100 group-hover:bg-emerald-600 group-hover:text-white text-slate-600 text-xs font-bold py-2 rounded transition">Select</button>
                </div>
                <!-- Pro (Recommended) -->
                <div class="border-2 border-emerald-500 rounded-xl p-4 bg-emerald-50 cursor-pointer transition text-center relative shadow-md">
                    <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Popular</div>
                    <div class="text-2xl mb-2">🥇</div>
                    <h4 class="font-bold text-slate-700">Pro Researcher</h4>
                    <p class="text-2xl font-bold text-emerald-600 my-2">5.00 <span class="text-xs text-slate-400">UC</span></p>
                    <p class="text-xs text-slate-400 mb-3">≈ $50 USD</p>
                    <button class="w-full bg-emerald-600 text-white text-xs font-bold py-2 rounded shadow transition">Select</button>
                </div>
                <!-- Lab -->
                <div class="border border-slate-200 rounded-xl p-4 hover:border-indigo-500 cursor-pointer transition text-center group">
                    <div class="text-2xl mb-2">💎</div>
                    <h4 class="font-bold text-slate-700">Lab Fund</h4>
                    <p class="text-2xl font-bold text-indigo-600 my-2">20.00 <span class="text-xs text-slate-400">UC</span></p>
                    <p class="text-xs text-slate-400 mb-3">≈ $200 USD</p>
                    <button class="w-full bg-slate-100 group-hover:bg-indigo-600 group-hover:text-white text-slate-600 text-xs font-bold py-2 rounded transition">Select</button>
                </div>
            </div>
            
            <p class="text-[10px] text-center text-slate-400 mt-6 flex justify-center items-center">
                <i class="fa-brands fa-stripe text-2xl mr-2 text-slate-400 opacity-50"></i> Encrypted Payment Processing
            </p>
        </div>
    </div>

    <script>
        // --- View Switcher ---
        function changeView(viewName) {
            const views = ['viewProjects', 'viewPersonal', 'viewPlatform'];
            const tabs = ['tabProjects', 'tabPersonal', 'tabPlatform'];
            
            views.forEach(v => document.getElementById(v).classList.add('hidden'));
            tabs.forEach(t => document.getElementById(t).className = "tab-inactive py-2 px-4 text-sm focus:outline-none transition whitespace-nowrap");

            document.getElementById('view' + viewName.charAt(0).toUpperCase() + viewName.slice(1)).classList.remove('hidden');
            document.getElementById('tab' + viewName.charAt(0).toUpperCase() + viewName.slice(1)).className = "tab-active py-2 px-4 text-sm focus:outline-none transition whitespace-nowrap";
            
            // Re-render chart if switching to personal view
            if(viewName === 'personal') renderChart();
        }

        // --- Exchange Logic (1 UC = 1M AT) ---
        function calculateExchange() {
            const input = document.getElementById('exchangeInput').value;
            // 1 UC = 1,000,000 AT
            const result = input * 1000000;
            document.getElementById('exchangeOutput').innerHTML = result.toLocaleString() + ' <span class="text-[10px] text-slate-500">AT</span>';
        }

        function executeExchange() {
             const btn = document.querySelector('button[onclick="executeExchange()"]');
             const originalText = btn.innerText;
             btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
             setTimeout(() => {
                btn.innerHTML = '<i class="fa-solid fa-check"></i> Converted!';
                btn.classList.add('bg-emerald-700');
                
                // Update balances mock
                let currentUC = parseFloat(document.getElementById('creditBalance').innerText);
                let inputVal = parseFloat(document.getElementById('exchangeInput').value);
                
                if (currentUC >= inputVal) {
                     document.getElementById('creditBalance').innerText = (currentUC - inputVal).toFixed(2);
                     let currentAT = 2400000; // Mock current
                     let addedAT = inputVal * 1000000;
                     document.getElementById('tokenBalance').innerText = ((currentAT + addedAT) / 1000000).toFixed(1) + 'M';
                     
                     // Add log
                     const log = document.getElementById('transactionLog');
                     log.innerHTML = `<div class="bg-indigo-50 p-3 rounded border border-indigo-100 shadow-sm text-xs animate-pulse"><div class="flex justify-between mb-1"><span class="font-bold text-slate-600">@Dr.Santa</span><span class="text-slate-400">Just now</span></div><p class="text-slate-600">Converted <span class="font-bold text-indigo-600">${inputVal} UC</span> → Energy</p></div>` + log.innerHTML;
                }

                setTimeout(() => { 
                    btn.innerText = originalText; 
                    btn.classList.remove('bg-emerald-700');
                }, 2000);
             }, 1000);
        }

        // --- Modal ---
        function openModal(id) { document.getElementById(id).classList.remove('hidden'); }
        function closeModal(id) { document.getElementById(id).classList.add('hidden'); }

        function donateToProject(name) {
             const amount = prompt(`Donate to ${name} (UC):`, "1.00");
             if (amount) alert(`Thank you! ${amount} UC donated.`);
        }

        // --- Chart.js ---
        let chartInstance = null;
        function renderChart() {
            const ctx = document.getElementById('personalExpenseChart').getContext('2d');
            if (chartInstance) chartInstance.destroy();
            
            chartInstance = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['AI Energy (Research)', 'Donations', 'Storage Fees'],
                    datasets: [{
                        data: [65, 20, 15],
                        backgroundColor: ['#f59e0b', '#ec4899', '#6366f1'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right' }
                    }
                }
            });
        }
    </script>
</body>
</html>
```










## UET Project Workspace

![[Pasted image 20251203153203.png]]


```
```