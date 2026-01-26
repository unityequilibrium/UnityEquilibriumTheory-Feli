# How to Write Code/README.md

This guide defines the standard template for writing `Code/README.md` files in UET topics.

## Required Sections

Every `Code/README.md` MUST contain the following sections in order:

---

### 1. Header & Description

```markdown
# Topic X.XX: [Topic Name] - Code

[Brief 2-3 line description of what this topic validates/tests]
- **Key Concept 1** -> UET parameter/term it relates to
- **Key Concept 2** -> UET parameter/term it relates to
```

---

### 2. 5x4 Structure

```markdown
## 5x4 Structure

\```
Code/
  01_Engine/       # (if exists) Core calculation engines
  02_Proof/        # (if exists) Mathematical proofs
  03_Research/     # Research scripts against real data
    Research_*.py  # All research scripts
  04_Competitor/   # (if exists) Baseline/comparison scripts
\```
```

**Naming Convention:**
- `01_Engine/`: `Engine_*.py`
- `02_Proof/`: `Proof_*.py`
- `03_Research/`: `Research_*.py`
- `04_Competitor/`: `Competitor_*.py`, `Baseline_*.py`

---

### 3. Run Commands

```markdown
## Run Commands

\```powershell
# Navigate to project root
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7

# Run individual scripts
python research_uet/topics/X.XX_Topic_Name/Code/03_Research/Research_Script1.py
python research_uet/topics/X.XX_Topic_Name/Code/03_Research/Research_Script2.py
\```
```

**Rules:**
- Use PowerShell syntax
- Include full relative paths from project root
- List ALL runnable scripts

---

### 4. Test Results Table

```markdown
## Test Results

| Script | Tests | Status |
|--------|-------|--------|
| Research_Script1.py | 3/3 | PASS |
| Research_Script2.py | 4/4 | PASS |

**Total: X/Y PASS**
```

**Rules:**
- Update after running tests
- Include total count

---

### 5. Data Sources

```markdown
## Data Sources (with DOIs)

- **Author et al. (Year)** Journal - DOI: XX.XXXX/XXXXXX
- **Collaboration Name** - Dataset description
```

**Rules:**
- MUST include DOIs for all published sources
- List all external data used

---

### 6. Engine/Proof Analysis

```markdown
## Engine/Proof Analysis

### Current Status
[What does this topic currently use from core?]

### Recommendation
- **Engine needed?** [Yes/No + reason]
- **Proof needed?** [Yes/No + reason]
```

---

### 7. Key Physics (Optional but Recommended)

```markdown
## Key Physics

\```
[Core equation or formula in ASCII]

Where:
  parameter1 = [description]
  parameter2 = [description]
\```
```

---

### 8. Notes Section (Optional)

```markdown
## ASCII Note

All Unicode characters have been replaced with ASCII for Windows PowerShell compatibility.
```

---

## Complete Template

```markdown
# Topic X.XX: [Topic Name] - Code

[Brief description connecting physics to UET]
- **Concept 1** -> beta term
- **Concept 2** -> kappa term

## 5x4 Structure

\```
Code/
  03_Research/
    Research_Script1.py   # Description
    Research_Script2.py   # Description
\```

## Run Commands

\```powershell
cd c:\Users\santa\Desktop\lad\Lab_uet_harness_v0.8.7
python research_uet/topics/X.XX_Topic_Name/Code/03_Research/Research_Script1.py
\```

## Test Results

| Script | Tests | Status |
|--------|-------|--------|
| Research_Script1.py | 3/3 | PASS |

**Total: 3/3 PASS**

## Data Sources (with DOIs)

- **Author (Year)** Journal - DOI: 10.XXXX/XXXXX

## Engine/Proof Analysis

### Current Status
Uses existing `UETParameters` from core.

### Recommendation
- **No new Engine needed** - [reason]
- **No Proof needed** - [reason]

## Key Physics

\```
Omega = V(C) + kappa|grad(C)|^2 + beta*C*I
\```

## ASCII Note

All Unicode replaced with ASCII for Windows compatibility.
```

---

## Checklist Before Commit

- [ ] Header with topic name and brief description
- [ ] 5x4 structure documented
- [ ] Run commands with full paths
- [ ] Test results table with PASS counts
- [ ] Data sources with DOIs
- [ ] Engine/Proof analysis with recommendation
- [ ] All scripts tested and passing
- [ ] No Unicode characters (use ASCII only)
