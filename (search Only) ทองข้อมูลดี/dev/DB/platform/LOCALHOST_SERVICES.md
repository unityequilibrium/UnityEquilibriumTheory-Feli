# 🌐 Localhost Services Reference

> **ใช้เพื่อ**: Quick reference สำหรับ dev servers และ services ที่ใช้ในโปรเจค
> **Updated**: 2025-12-23

---

## 📦 Active Services

| Port | Service | Start Command | Description |
|------|---------|---------------|-------------|
| **3000** | Next.js Frontend | `cd frontend && npm run dev` | UET Lab UI (Gallery, Lab, etc.) |
| **5432** | PostgreSQL | Auto-start (system service) | Database |
| **5555** | Prisma Studio | `cd database && npx prisma studio` | Database GUI |

---

## 🔗 Quick URLs

### Frontend (Port 3000)
- **Home**: http://localhost:3000/
- **Gallery**: http://localhost:3000/gallery
- **Lab**: http://localhost:3000/lab
- **API - Runs**: http://localhost:3000/api/runs
- **API - Projects**: http://localhost:3000/api/projects

### Database Tools (Port 5555)
- **Prisma Studio**: http://localhost:5555

---

## ⚡ Start All Services

```powershell
# Terminal 1: Frontend
cd frontend
bun run dev

# Terminal 2: Prisma Studio (optional)
cd database
bun prisma studio
```

---

## 🔧 Common Issues

### "localhost:5555 refused to connect"
**สาเหตุ**: Prisma Studio ไม่ได้รัน
**Fix**: `cd database && bun prisma studio`

### "localhost:3000 refused to connect"
**สาเหตุ**: Next.js dev server ไม่ได้รัน
**Fix**: `cd frontend && bun run dev`

### "Database connection error"
**สาเหตุ**: PostgreSQL ไม่ได้รัน
**Fix**: Start PostgreSQL service (Windows Services or Docker)

---

## 📊 Check Port Status

```powershell
netstat -ano | findstr "LISTENING" | findstr ":3000 :5432 :5555"
```

Expected output:
```
TCP    0.0.0.0:3000    LISTENING    (Next.js)
TCP    0.0.0.0:5432    LISTENING    (PostgreSQL)
TCP    0.0.0.0:5555    LISTENING    (Prisma Studio)
```
