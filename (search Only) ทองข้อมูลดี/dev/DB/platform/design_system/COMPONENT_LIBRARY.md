# UET Lab - Component Library Standards

> **มาตรฐานการเขียน UI Components**  
> Reference: `src/shell/AppTokens.ts`  
> Theme: Glassmorphism

---

## 1. PRIMITIVES

### 1.1 Buttons

**Primary Button (Action)**
```tsx
// Purpose: Create Run, Save, Submit
<button className="
  h-8 px-4 
  bg-[rgba(78,205,196,0.1)] 
  border border-[rgba(78,205,196,0.5)] 
  text-[#4ecdc4] 
  hover:bg-[rgba(78,205,196,0.2)] 
  rounded flex items-center justify-center gap-2
  transition-all duration-200
">
  <Icon /> Label
</button>
```

**Secondary Button (Ghost)**
```tsx
// Purpose: Cancel, Back, Additional Options
<button className="
  h-8 px-3 
  text-gray-400 hover:text-white 
  hover:bg-white/5 
  rounded flex items-center justify-center
">
  Label
</button>
```

### 1.2 Inputs

**Number Input (Parameter)**
```tsx
// Purpose: Parameter adjustment
<div className="flex items-center gap-2">
  <label className="text-xs text-gray-400">Mass (kg)</label>
  <input type="number" className="
    h-7 bg-black/20 border border-white/10 rounded px-2 
    text-sm text-right font-mono
    focus:border-[#4ecdc4] focus:outline-none
  " />
</div>
```

### 1.3 Badges

**Category Badge (Unit Type)**
```tsx
// Variants: QNT (Gray), QLT (Blue), COUNT (Purple)
<span className="text-[10px] px-1 rounded bg-white/10 text-gray-300 font-mono">
  QNT
</span>
```

**Mode Badge (Source)**
```tsx
// Variants: PHY (Green), UET (Yellow), IND (Orange)
<span className="text-[10px] px-1 rounded bg-[#4ade80]/10 text-[#4ade80] font-mono border border-[#4ade80]/20">
  PHY
</span>
```

---

## 2. CONTAINERS

### 2.1 Glass Panel (Base)

พื้นฐานของทุก Panel ในระบบ
```tsx
<div className="
  bg-[#1c1c22]/70 
  backdrop-blur-md 
  border-r border-white/5 
  h-full flex flex-col
">
  {/* Content */}
</div>
```

### 2.2 Metric Card (Unique)

Pattern: `1-1-1` (Checkbox - Value - Graph)
```tsx
<div className="
  flex items-center justify-between 
  p-2 mb-1 rounded 
  hover:bg-white/5 transition-colors group
">
  <div className="flex items-center gap-2">
    <input type="checkbox" className="accent-[#4ecdc4]" />
    <span className="text-sm">Total Energy</span>
  </div>
  
  <div className="flex items-center gap-2">
    <span className="font-mono text-[#4ecdc4]">-2534.11 J</span>
    <Badge>QNT</Badge>
  </div>
</div>
```

---

## 3. ICONS & ASSETS

- **Library**: `lucide-react` (Standard)
- **Size**: 
  - `w-3 h-3`: Tiny indicators
  - `w-4 h-4`: Button icons (Default)
  - `w-5 h-5`: Navigation icons

---

## 4. LAYOUT PATTERNS

### 4.1 Sidebar Layout
```tsx
<div className="w-[320px] max-w-[320px] flex-shrink-0 flex flex-col">
  {/* Header */}
  <div className="h-12 border-b border-white/5 px-4 flex items-center">...</div>
  
  {/* Scrollable Content */}
  <div className="flex-1 overflow-y-auto px-2 py-2 scrollbar-thin">...</div>
  
  {/* Footer Actions */}
  <div className="p-4 border-t border-white/5">...</div>
</div>
```

### 4.2 Graph Dock
```tsx
<div className="
  fixed bottom-0 left-[320px] right-[320px] 
  bg-[#1c1c22]/90 backdrop-blur-lg 
  border-t border-white/10 
  transition-all duration-300
">
  {/* Height controlled by state: h-0 or h-[300px] */}
</div>
```
