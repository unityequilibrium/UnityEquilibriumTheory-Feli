# 🔧 NiceHash Setup Guide

สำหรับใช้กับ UET Rust Bitcoin Miner

```
wsl -d Ubuntu -- bash -c "cd /mnt/c/Users/santa/Desktop/lad/Lab_uet_harness_v0.9.0/research_uet/topics/0.18_Mathnicry/rust_miner && ./target/release/uet_miner"
```

---

## 📝 ขั้นตอนการ Setup NiceHash

### 1. สร้าง/Login NiceHash Account

1. ไปที่ https://www.nicehash.com/
2. คลิก **Register** หรือ **Login**
3. ทำ **KYC/KYB Verification** (ต้องทำก่อนถึงจะ mine ได้!)
   - ใช้ Passport หรือบัตรประชาชน
   - อาจใช้เวลา 1-3 วัน

### 2. ใช้ Stratum Generator (สำหรับ Custom Miner)

จากหน้าที่เห็น ให้เลือก **"Stratum generator"** (ล่างซ้าย)

![NiceHash Options](uploaded_media_1769947280829.png)

**Stratum Generator** จะให้:
- Pool URL: `sha256.auto.nicehash.com`
- Port: `3334` (หรือ 443 ถ้าใช้ SSL)
- Username format: `YOUR_WALLET.WORKER_NAME`

### 3. หา Wallet Address

1. ไปที่ https://www.nicehash.com/my/wallet
2. คลิก **Deposit**
3. Copy **BTC Wallet Address** ของคุณ
4. ใส่ใน config:

```rust
// src/main.rs - แก้ไขตรงนี้
wallet: "YOUR_BTC_WALLET_HERE".to_string(),
worker: "RX6600XT".to_string(),  // ชื่อ worker
```

### 4. Verify Mining

1. Run miner
2. ไปที่ https://www.nicehash.com/my/rig-manager
3. ควรเห็น worker ของคุณ online

---

## ⚠️ Important Notes

| เรื่อง | รายละเอียด |
|--------|------------|
| **KYC Required** | NiceHash ต้อง verify ตัวตนก่อน mine ได้ |
| **Minimum Payout** | 0.001 BTC (~$50-100) |
| **SHA256 GPU** | ไม่ profitable (ASIC ชนะ) แต่เรียนรู้ได้! |
| **Alternative** | ใช้ Testnet pool สำหรับ test ฟรี |

---

## 🧪 ทดสอบกับ Testnet Pool (ฟรี)

ถ้าไม่อยากทำ KYC สามารถใช้ Testnet:

```rust
pool_url: "solo.ckpool.org".to_string(),
pool_port: 3333,
wallet: "YOUR_TESTNET_ADDRESS".to_string(),
```

---

## 🔗 Quick Links

- [NiceHash Dashboard](https://www.nicehash.com/my/dashboard)
- [Rig Manager](https://www.nicehash.com/my/rig-manager)
- [Mining Calculator](https://www.nicehash.com/profitability-calculator)
- [Stratum Protocol Docs](https://www.nicehash.com/blog/post/blockchain-basics-mining-job)

---

*📅 สร้างเมื่อ: 2026-02-01 | สำหรับ: UET Rust Bitcoin Miner*
