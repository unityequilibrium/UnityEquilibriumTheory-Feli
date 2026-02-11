# UET UI Design System

## 🎯 Core Principles

| Concept | Definition |
|---------|------------|
| **Padding** | ระยะห่างระหว่าง "เนื้อหาข้างใน" กับ "ขอบของตัวมันเอง" |
| **Margin** | ระยะห่างระหว่าง "ขอบของวัตถุหนึ่ง" กับ "วัตถุอื่นๆ" |
| **Whitespace** | พื้นที่ว่างเพื่อให้งานดูสะอาดตา |
| **Safe Zone** | ขอบเขตที่ไม่ควรวางเนื้อหาสำคัญ |
| **Leading** | ระยะห่างระหว่างบรรทัด (1.5x มาตรฐาน) |
| **Tracking** | ปรับช่องไฟของกลุ่มข้อความ |
| **Measure** | ความยาวบรรทัด (45-90 ตัวอักษร) |

---

## 📏 8px Grid System

```
Base Scale:
0 → 0px
1 → 4px   (xs)
2 → 8px   (sm)
3 → 12px  (md)
4 → 16px  (lg)
6 → 24px  (xl)
8 → 32px  (xxl)
```

---

## 🧱 Token Reference

### Padding (Internal)
```ts
AppTokens.padding.button     // '8px 16px'
AppTokens.padding.input      // '8px 12px'
AppTokens.padding.card       // '16px'
AppTokens.padding.panel      // '12px'
AppTokens.padding.modal      // '24px'
```

### Margin (External)
```ts
AppTokens.margin.element     // '8px'  ระหว่าง elements
AppTokens.margin.section     // '16px' ระหว่าง sections
AppTokens.margin.group       // '24px' ระหว่าง groups
```

### Whitespace
```ts
AppTokens.whitespace.line       // '4px'  ระหว่างบรรทัด
AppTokens.whitespace.paragraph  // '16px' ระหว่างย่อหน้า
AppTokens.whitespace.visual     // '24px' breathing room
AppTokens.whitespace.emphasis   // '32px' เน้นจุดสำคัญ
```

### Safe Zone
```ts
AppTokens.safeZone.edge   // '8px'  จากขอบจอ
AppTokens.safeZone.panel  // '4px'  จากขอบ panel
AppTokens.safeZone.modal  // '16px' จากขอบ modal
```

---

## 📐 Usage Examples

```tsx
// Button
<button style={{ padding: AppTokens.padding.button }}>
  Click Me
</button>

// Section with margin
<section style={{ marginBottom: AppTokens.margin.section }}>
  Content
</section>

// Card with safe zone
<div style={{ 
  padding: AppTokens.padding.card,
  margin: AppTokens.safeZone.edge 
}}>
  Card Content
</div>
```

---

## ✅ Best Practices

1. **ใช้ 8px Grid** - ใช้ค่าที่หารด้วย 4 หรือ 8 ลงตัว
2. **Consistency** - ใช้ tokens แทน hardcode
3. **Semantic** - ใช้ชื่อที่สื่อความหมาย เช่น `padding.button`
4. **Hierarchy** - ใช้ whitespace แยก visual groups
