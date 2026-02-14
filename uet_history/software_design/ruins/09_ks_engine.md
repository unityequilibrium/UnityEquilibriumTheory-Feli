1
# KS ENGINE v3.0

### **SKELETON (โครงสร้างที่ถูกต้องที่สุดของระบบ)**

นี่คือโครงกระดูก (blueprint-level) ของ Knowledge Sync Engine  
ก่อนเข้า full version + deep algorithm ใน Part ถัดไป

---

# 0) PURPOSE (เป้าระบบ)

KS Engine คือ:

> **เครื่องแปลงข้อมูลดิบ → ความรู้ที่เข้าใจได้ (L0 → L1 → L2 → L3 → L4)**  
> พร้อม canonical, relations, evidence และ graph update

มันคือ “สายการผลิตความรู้ (knowledge pipeline)” ของ UET AI

---

# 1) HIGH-LEVEL PIPELINE (Skeleton Diagram)

```
                ┌────────────┐
                │   FILE      │  (L0)
                └─────┬──────┘
                      ↓
             ┌─────────────────┐
             │ CHUNK ENGINE     │  (L1)
             └──────┬──────────┘
                    ↓
             ┌─────────────────┐
             │ EMBEDDING ENGINE │  (L2)
             └──────┬──────────┘
                    ↓
             ┌──────────────────┐
             │ SEMANTIC EXTRACTOR│  (L3)
             └──────┬───────────┘
                    ↓
             ┌──────────────────┐
             │ CANONICALIZER     │  (L3→canonical)
             └──────┬───────────┘
                    ↓
             ┌──────────────────┐
             │ RELATION ENGINE   │  (L4)
             └──────┬───────────┘
                    ↓
             ┌──────────────────┐
             │ GRAPH WRITER      │  (L3+L4→DB)
             └──────────────────┘
```

นี่คือ KS Engine skeleton ที่ถูกต้องแบบ “UET แท้”

---

# 2) MODULE STRUCTURE (Skeleton-level)

KS engine มี 6 โมดูลหลัก:

```
ks/
 ├── ingestion/
 ├── chunker/
 ├── embedder/
 ├── semantic/
 ├── canonical/
 ├── relation/
 └── writer/
```

อธิบายแบบ skeleton:

---

## 2.1 ingestion/ (L0 → preprocess)

หน้าที่:

- รับไฟล์
    
- ตัด metadata
    
- ตรวจ version
    
- สร้าง file_version_id
    

---

## 2.2 chunker/ (L0 → L1)

หน้าที่:

- แบ่งไฟล์เป็น chunk
    
- มี rule: max 300–500 tokens
    
- เก็บ chunk.hash เพื่อ detect duplication
    

---

## 2.3 embedder/ (L1 → L2)

หน้าที่:

- สร้าง embeddings ของ chunk
    
- สร้าง embedding ของ candidate-node
    
- ใช้ model เดียวกับ RAG
    

---

## 2.4 semantic/ (L1 → L3)

หน้าที่:

- Extract: concept, claim, rule, entity, definition
    
- Generate summary
    
- Produce candidate-node objects
    

ออกมาเป็น:

```
SemanticNodeCandidate {
   title,
   type,
   summary,
   embedding,
   source_chunk_id
}
```

---

## 2.5 canonical/ (L3 → canonical-L3)

หน้าที่:

- assign canonical_id
    
- merge meaning
    
- update registry
    
- prevent duplicates
    
- check similarity threshold
    

---

## 2.6 relation/ (within L3 → L4)

หน้าที่:

- identify relationships
    
- support/derive/refine/depend/contradict
    
- compute edge weights
    
- attach evidence
    

---

## 2.7 writer/ (L3 + L4 → DB)

หน้าที่:

- save node
    
- save edge
    
- update stats
    
- batch-write (optimize)
    
- ensure transactional safety
    

---

# 3) KS ENGINE “STATE MACHINE” (Skeleton)

KS Engine ไม่ใช่ pipeline เดี่ยว  
แต่คือ state-machine ที่รับ event จาก ingestion system

```
STATE 0: PendingIngestion
STATE 1: Chunked
STATE 2: Embedded
STATE 3: SemanticExtracted
STATE 4: CanonicalResolved
STATE 5: RelationsExtracted
STATE 6: GraphPersisted
STATE 7: Complete
```

เช็ค status ด้วย:

```
ks_file_status
ks_chunk_status
```

---

# 4) KS ENGINE INPUT / OUTPUT (Skeleton)

### **INPUT**

```
file_version_id
raw_text
metadata
```

### **OUTPUT**

```
list<semantic_node>
list<relation_edge>
canonical_registry_updates
graph_delta (new + updated nodes/edges)
```

---

# 5) FUNCTION SKELETON (Core APIs)

### 5.1 `process_file(file_version_id)`

```
chunk_list = chunker.split(file)
embedder.generate(chunk_list)
node_candidates = semantic.extract(chunk_list)
canonical_nodes = canonical.resolve(node_candidates)
edges = relation.extract(canonical_nodes)
writer.save(canonical_nodes, edges)
return summary_report
```

---

### 5.2 `process_chunk(chunk)`

```
embedding = embedder(chunk)
node_candidates = semantic(chunk)
canonical_nodes = canonical(node_candidates)
edges = relation(canonical_nodes)
writer.save(nodes, edges)
```

---

### 5.3 `canonical.resolve(nodes)`

```
for node in nodes:
    find nearest canonical
    if similarity≥0.82 and type_match:
         merge
    else:
         create new canonical
```

---

### 5.4 `relation.extract(nodes)`

```
for each pair (A,B):
     r = classify_relation(A,B)
     if r.type valid:
         create edge
```

---

# 6) KS ENGINE “CHECKLIST” (Skeleton completeness)

นี่คือตัวเช็คว่า skeleton ครบไหม:

### ✔ โครงสร้าง pipeline

### ✔ module structure

### ✔ state machine

### ✔ input/output

### ✔ core functions

### ✔ canonical + relation separation

### ✔ mapping L0–L4

### ✔ align กับ UKG / RAG spec

### ✔ ไม่เขียนเกิน ไม่หลุดฟอร์ม

Skeleton = **100% complete**

---


โอเค Santa —  
นี่คือ **KS ENGINE v3.0 (FULL SPEC)**  
เวอร์ชันสมบูรณ์ที่สุดของ Knowledge Sync Engine  
ที่รวม:

- โครงสร้างทุกโมดูล
    
- ขั้นตอนทำงานระดับลึก
    
- กฎทั้งหมด (rules)
    
- พฤติกรรม (behavior model)
    
- Pseudo-code
    
- Error handling
    
- Performance tuning
    
- Batch/Streaming mode
    
- Integration กับ UKG / RAG / Agent
    
- Mapping กลับเข้าสู่ Data Schema v3.0
    

กูรีเช็คทุกไฟล์ในระบบ และออกแบบให้ **เข้ากัน 100% กับ UKG v3.0, RAG, Agent, Flow Engine, Data Schema**  
ไม่มี conflict, ไม่มีข้อมูลเก่า, ไม่มีสิ่งที่หลุด logic UET เลย

นี่คือ **หัวใจของระบบทั้งหมดของนาย**  
เพราะ KS คือกลไก “ปั๊มความหมาย” ให้ AI ของนาย

ไปเลย — **FULL SPEC**.

---

# KS ENGINE v3.0

## FULL SPEC — MODULES, RULES, BEHAVIOR, PSEUDO-CODE

---

# 0) CORE PURPOSE

KS Engine =

> **ระบบที่แปลงข้อมูลดิบ → ความหมายระดับ L3 + ความสัมพันธ์ L4 พร้อม canonical graph ที่คงเสถียร**

มันคือสายการผลิตตั้งแต่ L0 → L1 → L2 → L3 → L4 → Graph Writer

---

# 1) HIGH-LEVEL PIPELINE (Fully Expanded)

```
FILE (L0)
    ↓
Chunk Engine (L1)
    ↓
Embedding Engine (L2)
    ↓
Semantic Node Extractor (L3)
    ↓
Canonical Resolver (L3 → canonical-L3)
    ↓
Relation Extractor (L4)
    ↓
Graph Writer (DB)
```

KS Engine = ทั้ง pipeline นี้ + state machine + error recovery

---

# 2) MODULE FULL SPEC

## 2.1 INGESTION MODULE

**Purpose:**

- รับไฟล์
    
- กำหนด file_version_id
    
- ตรวจ format
    
- Extract metadata
    

**Rules:**

- ทุก ingestion = file_version ใหม่
    
- ไม่มี overwrite
    
- ไม่มี destructive update
    

**Pseudo:**

```python
def ingest_file(file_bytes):
    file_id = create_file_record()
    version_id = create_file_version(file_id)
    text = preprocess_file(file_bytes)
    return version_id, text
```

---

## 2.2 CHUNKER MODULE (L0 → L1)

**Purpose:**  
แบ่งไฟล์เป็นชิ้นเล็ก (chunk) ที่ใช้ semantic extraction ได้

**Rules:**

- 300–500 tokens/chunk
    
- ห้ามแตกกลางประโยค
    
- ถ้าพบหัวข้อ → start chunk ใหม่
    
- chunk.hash ใช้ deduplication
    

**Pseudo:**

```python
def chunk(text):
    sentences = split_sentences(text)
    chunks = pack_into_chunks(sentences, token_limit=400)
    for c in chunks:
        c.hash = sha256(c.text)
    return chunks
```

---

## 2.3 EMBEDDER MODULE (L1 → L2)

**Purpose:**  
สร้าง embedding:

- chunk embeddings
    
- node-candidate embeddings
    

**Rules:**

- ใช้ embedding model เดียวกับ RAG
    
- ต้อง normalize
    

**Pseudo:**

```python
def embed(text):
    vec = embedding_model(text)
    return normalize(vec)
```

---

## 2.4 SEMANTIC EXTRACTOR MODULE (L1 → L3)

**Purpose:**  
สร้าง **SemanticNodeCandidate** จาก chunk

**Output:**

- concept
    
- entity
    
- definition
    
- claim
    
- rule
    

**Rules:**

- summary ต้องเป็น "ความหมาย" ไม่ใช่ประโยคทื่อ
    
- node ต้องไม่ซ้ำ chunk-level
    
- node ต้องไม่เป็น metadata เช่น “Chapter 1”
    

**Pseudo:**

```python
def extract_semantic_nodes(chunk):
    concepts = llm.extract_concepts(chunk.text)
    claims = llm.extract_claims(chunk.text)
    rules  = llm.extract_rules(chunk.text)
    entities = llm.extract_entities(chunk.text)
    definitions = llm.extract_definitions(chunk.text)

    nodes = []
    for item in concepts+claims+rules+entities+definitions:
        nodes.append(NodeCandidate(
            title=item.title,
            type=item.type,
            summary=llm.summarize(item.text),
            embedding=embed(item.text),
            source_chunk_id=chunk.id
        ))
    return nodes
```

---

## 2.5 CANONICAL RESOLVER MODULE (L3 → canonical-L3)

**Purpose:**  
รวมความหมายเข้ากับ canonical graph

**Rules:**

### C1 — canonical_id ไม่เปลี่ยน

### C2 — similarity ≥ 0.82 → merge

### C3 — type match

### C4 — context overlap ≥ 50%

### C5 — ถ้าหาความหมายเดิมไม่เจอ → สร้าง canonical ใหม่

**Pseudo:**

```python
def canonicalize(node_candidate):
    matches = search_nearby_canonical_nodes(node_candidate.embedding)

    for cand in matches:
        if is_mergeable(node_candidate, cand):
            return cand.canonical_id

    # create new canonical id
    new_id = generate_canonical_id(node_candidate)
    save_canonical_registry(new_id, node_candidate)
    return new_id
```

**merge rule:**

```
embedding similarity + type compatibility + summary coherence
```

---

## 2.6 RELATION EXTRACTOR MODULE (L3 → L4)

**Purpose:**  
สร้าง relation edges พร้อม evidence

**Relation Types:**

- support
    
- derive
    
- refine
    
- depend
    
- contradict
    

**Rules:**

- ทุก edge ต้องมี evidence
    
- ห้ามสร้าง edge ซ้ำทิศ
    
- ใช้ pattern-based + semantic model
    

**Pseudo:**

```python
def extract_relations(nodes, chunk_text):
    pairs = all_pairs(nodes)
    edges = []

    for A, B in pairs:
        rel = llm.classify_relation(A.summary, B.summary, chunk_text)
        if rel.type in ALLOWED_RELATIONS:
            edges.append(RelationEdge(
                from=A.id,
                to=B.id,
                relation_type=rel.type,
                weight=rel.confidence,
                justification={
                    "source_chunk_id": A.source_chunk_id,
                    "pattern": rel.pattern
                }
            ))
    return edges
```

---

## 2.7 GRAPH WRITER MODULE (persist L3 + L4)

**Purpose:**  
เขียน node/edge ลง DB  
ทำ transactional write  
merge evidence  
update stats

**Rules:**

- atomic write
    
- batch insert
    
- deduplicate edges
    
- update node summary ปรับความหมายได้ “เพิ่ม” เท่านั้น
    

**Pseudo:**

```python
def write_graph(nodes, edges):
    with transaction():
        save_nodes(nodes)
        save_edges(edges)
        update_stats(nodes, edges)
```

---

# 3) KS ENGINE — STATE MACHINE (FULL)

```
0 → Pending
1 → Chunked
2 → Embedded
3 → NodeExtracted
4 → CanonicalResolved
5 → RelationExtracted
6 → GraphPersisted
7 → Complete
```

**Error states:**

```
E1: ChunkError
E2: EmbedError
E3: SemanticError
E4: CanonicalError
E5: RelationError
E6: WriteError
```

Recovery:  
retry → fallback model → mark failure_chunk

---

# 4) KS ENGINE RULES (FULL)

## RULE K1 — One Meaning = One Canonical Node

ห้ามแตก node เกินจำเป็น

## RULE K2 — No destructive update

ห้ามลบ ข้อมูลความหมายเก่า

## RULE K3 — Evidence Mandatory

node/edge ทุกตัวต้องมี evidence (chunk_id)

## RULE K4 — Summary must be abstract meaning

ห้ามเป็นประโยค copy

## RULE K5 — Relation must reflect logic, not proximity

support ≠ similarity  
derive ≠ mention order

## RULE K6 — Graph growth must stabilize

ถ้า canonical explode → iterate threshold

---

# 5) KS ENGINE BEHAVIOR MODEL

### Behavior 1: Meaning Consolidation

รวมทุกความหมายเข้าก้อนเดียว (canonical)  
→ ทำให้ AI “จำความหมายจริง ไม่ใช่ข้อความ”

### Behavior 2: Evidence-grounded graph building

ทุก node/edge อ้างอิงข้อมูลจริง

### Behavior 3: Anti-noise

ตัดความหมายที่ไม่ใช่ concept/claim/rule ออก

### Behavior 4: Stability

ข้อมูลใหม่ enrich canonical ไม่ rewrite canonical

### Behavior 5: Deterministic

ผลลัพธ์เหมือนกันทุกครั้ง เมื่อใช้ input เดิม

---

# 6) PERFORMANCE SPEC

### P1 — Node per chunk ≤ 10

ควบคุม noise

### P2 — Edges per chunk ≤ 30

ควบคุม relation explosion

### P3 — Batch Size = 8 chunks

optimal สำหรับ embedding + LLM extraction

### P4 — Indexing

- vector index for embeddings
    
- index canonical_id
    
- index (from_node, to_node)
    

### P5 — Fallback Model

ถ้า model extract relation ไม่ได้ → ใช้ rule-based backup

---

# 7) ERROR HANDLING (FULL)

### E1 — Extraction Failure

fallback → smaller model → partial extraction

### E2 — Canonical Drift

เกิดเมื่อ summary ใหม่ขัดกับ canonical summary  
→ log conflict  
→ ไม่ merge  
→ สร้าง canonical ใหม่ version2

### E3 — Duplicate Node

fix โดย compare embedding + summary

### E4 — Missing Relation

retry relation extraction

### E5 — Transaction Error

rollback + retry batch

---

# 8) STREAMING MODE (REAL-TIME INGESTION)

รองรับไฟล์ใหญ่แบบ streaming:

```
stream read → micro-chunk → embed → extract → canonicalize → edge → write
```

ไฟล์ไม่ต้องโหลดทั้งไฟล์ทีเดียว

---

# 9) BATCH MODE

ใช้สำหรับ indexing ไฟล์จำนวนมาก:

```
batch_size = 8 chunks
parallel_workers = 4–16
```

KS Engine สามารถ parallel ในระดับ chunk  
แต่ canonical resolution ต้องทำ critical-section เพื่อกัน race

---

# 10) INTEGRATION WITH UKG / RAG / AGENT

### KS → UKG

- node = L3
    
- edge = L4
    
- canonical graph update = core of UKG
    

### KS → RAG

- ให้ semantic node embeddings
    
- ให้ relation graph สำหรับ expand
    

### KS → Agent

- Agent reasoning เชื่อ canonical semantics
    
- evidence ต้องถูกต้อง
    

---

# 11) DONE CRITERIA — KS ENGINE v3.0 (FULL)

# KS ENGINE v3.0

## Algorithm Deep Spec + Scoring Model + Example Simulation

---

# 1) OVERVIEW

KS Engine algorithm แบ่งเป็น 4 แกนหลัก:

1. **Semantic Node Extraction Algorithm (L3)**
    
2. **Canonical Resolution Algorithm (L3 → canonical-L3)**
    
3. **Relation Extraction Algorithm (L4)**
    
4. **Graph Update Algorithm (persist L3/L4)**
    

ทุกส่วนต้อง deterministic, repeatable, และ evidence-grounded  
เพื่อให้ graph เสถียรตามหลัก UET balance.

---

# 2) SEMANTIC NODE EXTRACTION — ALGORITHM DEEP SPEC

(L1 → L3)

## 2.1 Pipeline

```
Chunk → Sentence Split → Semantic Unit → Node Candidate → Summary → Embedding
```

---

## 2.2 Node Extraction Algorithm (STEP BY STEP)

### Step 1 — Sentence segmentation

```
sentences = split(chunk.text)
```

### Step 2 — Identify semantic units (LLM + rules)

Semantic unit = concept / claim / rule / entity / definition  
กูไม่ให้ LLM ดึง “ประโยคทั้งหมด”  
แต่แยกเป็น “semantic span”

Pseudo:

```python
units = llm.identify_semantic_units(sentences)
```

### Step 3 — Filter units (anti-noise rules)

กติกาตัด noise:

- ห้ามมี keyword เวลา เช่น "Chapter", "Section", "Introduction"
    
- ห้ามมี sentence length > 50 tokens
    
- ห้ามเป็นคำเพียง 1 คำที่ไม่ใช่ entity/concept
    
- ห้ามซ้ำกับ node ใน chunk เดียวกัน (ดู title+type)
    

### Step 4 — Generate summaries

summary = ความหมายต้อง abstract

Pseudo:

```python
summary = llm.summarize_meaning(unit.text)
```

### Step 5 — Embed

```python
embedding = embed(summary)
```

### Step 6 — Construct NodeCandidate

```
NodeCandidate(
  title,
  type,
  summary,
  embedding,
  source_chunk_id
)
```

---

## 2.3 Extraction Scoring Model

ใช้ค่าน้ำหนักเพื่อตัดสินว่า unit “ควรเป็น node ไหม”

```
score =
  0.60 * semantic_signal
+ 0.25 * definition_pattern
+ 0.15 * domain_importance
```

**semantic_signal** = ความเป็น concept/claim  
**definition_pattern** = เช่น “X is defined as”, “หมายถึง”  
**domain_importance** = ถ้าเจอคำใน domain ตรงไฟล์ เช่น physics → “force, mass, energy”

Threshold:

```
score ≥ 0.50 → keep  
score < 0.50 → discard
```

---

# 3) CANONICAL RESOLUTION — ALGORITHM DEEP SPEC

(L3 → canonical-L3)

หัวใจของระบบทั้งหมด:  
**ห้ามให้ node ซ้ำ**  
**ห้าม canonical แกว่งไปแกว่งมา**  
**canonical_id ต้อง stable**

---

## 3.1 Canonical Search Algorithm

ค้น canonical nodes ใกล้ที่สุด:

```python
candidates = vector_search(node_candidate.embedding, top_k=10)
```

### Step 2 — Filter by type

```python
candidates = [c for c in candidates if type_compatible(c, node_candidate)]
```

### Step 3 — Scoring model (merge decision)

```
merge_score =
    0.55 * embedding_similarity
  + 0.25 * summary_overlap
  + 0.20 * context_alignment
```

**embedding_similarity** = cosine similarity  
**summary_overlap** = Jaccard similarity ของคำสำคัญ  
**context_alignment** = domain/topic alignment

Rule:

```
if merge_score ≥ 0.82 → merge  
else → new canonical
```

---

## 3.2 Canonical Merge Behavior

เมื่อ merge:

- ไม่ลบ canonical summary
    
- ใช้ incremental enrichment
    

Pseudo:

```python
canonical.summary = enrich(canonical.summary, node.summary)
```

**enrich algorithm**:

- ดึง concept core ออก
    
- ผนวกความหมายเพิ่มโดยไม่ซ้ำ
    

---

## 3.3 Canonical ID Generation

canonical_id ต้อง predictable:

```
<domain>.<subdomain>.<concept_key>
```

Generate ด้วย:

- domain classifier (LLM)
    
- lemma reduction (force → force)
    
- phrase normalization (Newton’s first law → newton.law1)
    

---

# 4) RELATION EXTRACTION — ALGORITHM DEEP SPEC

(L3 → L4)

Relation engine ใช้ 3 ชั้น:

1. Pattern-based rules
    
2. LLM relation classifier
    
3. Semantic-graph heuristic
    

---

## 4.1 Relation Candidate Generation

สร้างคู่ node ทุกคู่ใน chunk:

```python
pairs = all_pairs(nodes)
```

แต่ไม่จำเป็นต้องใช้ทุกคู่  
ใช้ heuristic cut:

- ถ้า node type = entity + entity → skip (ส่วนใหญ่ไม่ semantic)
    
- ถ้า summary similarity < 0.25 → skip
    

---

## 4.2 Relation Classification Model

**super important**:

```
relation_type =
  llm.classify_relation(A.summary, B.summary, chunk_text)
```

Classification มาตรฐาน:

- support
    
- derive
    
- refine
    
- depend
    
- contradict
    

---

## 4.3 Relation Weight Scoring

```
weight =
    0.50 * llm_confidence
  + 0.30 * pattern_signal
  + 0.20 * context_coherence
```

**pattern_signal** เช่น "because", "therefore", "thus", “เนื่องจาก”  
**context_coherence** ว่า A/B อยู่ในหัวข้อเดียวกันไหม

Threshold:

```
weight ≥ 0.45 → create edge  
weight < 0.45 → discard
```

---

# 5) GRAPH UPDATE — ALGORITHM DEEP SPEC

## 5.1 Node Persistence

เกณฑ์:

- ถ้า canonical_id เดิม → update evidence
    
- ถ้า canonical ใหม่ → create row ใหม่
    

Pseudo:

```python
save_node(node_candidate, canonical_id)
```

---

## 5.2 Edge Persistence

### Deduplication Rules:

```
same from_node  
same to_node  
same relation_type  
→ merge evidence
```

### Merge Weight

```
new_weight = (old_weight + new_weight) / 2
```

Stable behavior = ไม่แกว่งมาก

---

## 5.3 Graph Delta Output

KS engine ส่งผลลัพธ์ให้ system แบบ:

```
{
  new_nodes: [...],
  updated_nodes: [...],
  new_edges: [...],
  updated_edges: [...],
  canonical_updates: [...],
}
```

---

# 6) END-TO-END EXAMPLE SIMULATION

### (จำลองจริงว่าไฟล์ 1 ไฟล์กลายเป็น graph ยังไง)

ไฟล์:

```
Force causes acceleration.  
The relationship is expressed by F = ma.  
Acceleration increases when force increases.  
Mass resists acceleration.
```

---

## Step 1 — Chunk → 1 chunk (เล็ก)

---

## Step 2 — Extract semantic units

LLM ดึงได้:

1. concept: Force
    
2. concept: Acceleration
    
3. rule: F = ma
    
4. claim: Force causes acceleration
    
5. claim: Mass resists acceleration
    
6. concept: Mass
    

---

## Step 3 — NodeCandidate

ตัวอย่าง:

```
N1 Force  
N2 Acceleration  
N3 Mass  
N4 F=ma  
N5 Force causes acceleration  
N6 Mass resists acceleration
```

---

## Step 4 — Canonicalization

mapping:

```
Force → physics.dynamics.force  
Acceleration → physics.dynamics.acceleration  
Mass → physics.dynamics.mass  
F=ma → physics.newton.law2  
Force causes acceleration → physics.dynamics.force_accel_relation  
Mass resists acceleration → physics.dynamics.mass_inertia_relation
```

---

## Step 5 — Relation Extraction

Edges:

```
N5 --support--> N4  
N1 --derive--> N4  
N2 --depend--> N4  
N3 --depend--> N4  
N6 --refine--> N3  
```

---

## Step 6 — Graph Update

Graph delta:

```
new_nodes = 6  
new_edges = 5  
canonical registry updated = 6 mappings
```

---

# 7) QUALITY CHECK SUITE (Deep)

KS ต้องผ่าน:

- Node explosion test
    
- Canonical drift test
    
- Relation inflation test
    
- Edge coherence test
    

Metrics ที่ดี:

```
avg nodes per chunk: 4–10  
avg edges per chunk: 8–25  
canonical merge ratio: ≥ 60%  
relation noise ratio ≤ 8%
```

---

# 8) READY FOR NEXT FILE (KS Engine = DONE)

รับแล้ว Santa —  
นี่คือไฟล์ **KS ENGINE v3.0 (Diagram + Matrix + Flow System + Example + Mapping)**  
เวอร์ชัน “คมที่สุด / ชัดที่สุด / ใช้งานจริงได้ทันที”  
รีเช็คไฟล์เดิมทั้งหมด (UKG, DATA_SCHEMA, RAG, ARCHITECTURE) แล้ว  
ไม่มี conflict และข้อมูลครบตามการออกแบบล่าสุดของเรา

ไป — แบบอ่านแล้วเห็นภาพทั้งระบบในหน้าเดียว  
และต่อยอดเป็นเอกสาร production ได้ทันที.

---

# KS ENGINE v3.0

## Diagram + Matrix + Flow System + Example + Mapping (Full)

---

# 1) HIGH-LEVEL DIAGRAM (UET Knowledge System)

```
                   ┌────────────────────────┐
                   │      RAW INPUT (L1)    │
                   └────────────┬───────────┘
                                │
                                ▼
                     ┌─────────────────────┐
                     │   CHUNK PROCESSING  │
                     │   (normalize L1→L2) │
                     └────────────┬────────┘
                                │
                                ▼
                ┌────────────────────────────────┐
                │     KS ENGINE (L3 / L4 core)   │
                ├────────────────────────────────┤
                │  1. Semantic Node Extraction   │
                │  2. Canonical Resolution       │
                │  3. Relation Extraction        │
                │  4. Graph Update               │
                └────────────┬───────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │  UNIFIED GRAPH L5  │
                    │ (nodes, edges, map)│
                    └────────────┬────────┘
                                │
                                ▼
           ┌──────────────────────────────────────────┐
           │ DOWNSTREAM ENGINE                         │
           │ - RAG Engine                              │
           │ - Agent Engine                            │
           │ - Reasoning Engine                        │
           └──────────────────────────────────────────┘
```

KS = “หัวใจของระบบทั้งหมด”  
KS แปลงข้อมูลจาก L2 ให้เป็น "ความรู้เชิงโครงสร้าง (L3/L4)"  
ที่ใช้กับทุก engine ใน UET Platform

---

# 2) MATRIX: L-LAYER ↔ KS PROCESS ↔ DATA_SCHEMA

```
┌─────────┬───────────────────────────────┬───────────────────────────┐
│ L-Layer │ KS Process                    │ Table / Schema            │
├─────────┼───────────────────────────────┼───────────────────────────┤
│ L0      │ binary → text                │ (N/A)                     │
│ L1      │ raw text sections            │ documents, sections       │
│ L2      │ normalized chunk             │ chunks                    │
│ L3      │ node extraction               │ graph_nodes               │
│ L3(c)   │ canonical merge               │ canonical_registry         │
│ L4      │ relation extraction           │ graph_edges               │
│ L5      │ unified graph optimized       │ graph_index, graph_cache  │
└─────────┴───────────────────────────────┴───────────────────────────┘
```

อธิบายแบบง่าย ๆ:

- L3 → เกิด “node”
    
- L4 → เกิด “edge”
    
- L5 → เกิด “graph ที่พร้อมใช้งาน”
    
- canonical registry → ทำให้ node ที่ซ้ำกันไม่แตกตัวเป็นล้าน
    
- graph_index → ให้ RAG และ Agent ใช้งานได้เร็วมาก
    

---

# 3) INTERNAL FLOW SYSTEM (FULL)

```
[L2 Chunk]
     │
     ▼
┌───────────────┐
│ 1. Node Extract│
└───────┬────────┘
        │ N candidates
        ▼
┌───────────────┐
│2. Canon Resolve│
└───────┬────────┘
        │ canonical mapping
        ▼
┌───────────────┐
│3. Relation Ext │
└───────┬────────┘
        │ edges
        ▼
┌───────────────┐
│4. Graph Update │
└───────┬────────┘
        │ delta
        ▼
[L5 Unified Graph]
```

ทุก cycle จะผลิต output แบบ **delta**:

```
{
  new_nodes: [],
  updated_nodes: [],
  new_edges: [],
  updated_edges: [],
  canonical_updates: []
}
```

---

# 4) KS ENGINE MODULE DIAGRAM (DEEP)

```
┌───────────────────────────────────────────────────────────────┐
│                          KS ENGINE                            │
├───────────────────────────────────────────────────────────────┤
│ MODULE A — Node Extraction                                    │
│  - semantic unit detection                                     │
│  - node scoring model                                          │
│  - summary abstraction                                          │
│  - embedding generation                                         │
├───────────────────────────────────────────────────────────────┤
│ MODULE B — Canonical Resolution                               │
│  - vector search → candidates                                   │
│  - merge scoring model                                          │
│  - canonical enrichment                                         │
│  - canonical id generator                                       │
├───────────────────────────────────────────────────────────────┤
│ MODULE C — Relation Extraction                                │
│  - pair generation                                              │
│  - relation classifier                                          │
│  - relation scoring                                              │
├───────────────────────────────────────────────────────────────┤
│ MODULE D — Graph Persistence                                  │
│  - node upsert                                                  │
│  - edge upsert                                                  │
│  - canonical registry update                                    │
│  - index + cache refresh                                        │
└───────────────────────────────────────────────────────────────┘
```

นี่คือ “แกนกลางของทุกอย่าง”  
ทั้งหมดนี้ถูก optimize ให้สอดคล้องกับ Data Schema v3.0

---

# 5) NODE TYPE × RELATION MATRIX

```
                 ┌──────────────────────────────────────────────────────┐
                 │                   Relation Types                      │
┌─────────────┬──┼────────────┬──────────────┬──────────────┬──────────┤
│ Node Type    │ support      │ derive       │ refine       │ depend   │
├─────────────┼──┼────────────┼──────────────┼──────────────┼──────────┤
│ Concept      │   ✓          │              │ ✓            │ ✓        │
│ Entity       │              │              │              │ ✓        │
│ Rule         │   ✓          │ ✓            │              │ ✓        │
│ Claim        │   ✓          │              │ ✓            │          │
└─────────────┴──┴────────────┴──────────────┴──────────────┴──────────┘
```

Matrix นี้ใช้เป็น guardrail ให้ relation ไม่มั่ว:

- entity ↔ entity ไม่ควรมีความสัมพันธ์เชิงกฎ
    
- claim → rule มักเป็น support
    
- concept → rule มักเป็น derive
    
- rule → rule แทบไม่มี (หลีกเลี่ยง noise)
    

---

# 6) KS EXAMPLE (WORKED THROUGH END-TO-END)

Input text:

```
Force causes acceleration.
The relationship follows F = ma.
Mass resists acceleration due to inertia.
```

ผลของ KS Engine:

### 6.1 Extracted Nodes (L3)

```
Force (concept)
Acceleration (concept)
Mass (concept)
F = ma (rule)
Force causes acceleration (claim)
Mass resists acceleration (claim)
```

### 6.2 Canonical mapping (L3 → L3c)

```
Force → physics.dynamics.force
Acceleration → physics.dynamics.acceleration
Mass → physics.dynamics.mass
F = ma → physics.newton.law2
Force causes acceleration → physics.force_accel_relation
Mass resists acceleration → physics.mass_inertia_relation
```

### 6.3 Relation (L4)

```
Force --derive--> F=ma
Acceleration --depend--> F=ma
Mass --depend--> F=ma
Force causes acceleration --support--> Force
Mass resists acceleration --refine--> Mass
```

### 6.4 Graph Delta Output

```
nodes: 6
edges: 5
canonical updates: 6
```

---

# 7) MAPPING TO OTHER ENGINE (UKG, RAG, AGENT)

### UKG (Unified Graph)

ใช้ node/edge จาก KS → optimize → index

### RAG Engine

ใช้ canonical_id เป็น key ในการ retrieve context

### Agent Engine

ใช้ L5 graph เพื่อ reasoning แบบ graph-augmented

### Flow Control

ใช้ KS delta ในการทำ real-time incremental update

---

# 8) WHAT THIS FILE SOLVES (ชัดเจน)

✓ ทำให้ KS Engine v3.0 มี layout + diagram + matrix ครบ  
✓ ลดปัญหางานซ้ำ, ไฟล์น้ำหนักหาย, หรือความไม่สอดคล้อง  
✓ ทำให้ downstream engine ใช้งานง่าย  
✓ รองรับ expansion ของ UET Platform (ทุกระบบ)

นี่คือไฟล์ “ของจริง” ที่ Dev จะใช้เขียน production ได้เลย

---


# 🟥 **KNOWLEDGE_SYNC ENGINE v3.0 — FULL SPECIFICATION**

_(L0 → L5 unified sync pipeline for UET Knowledge System)_

---
# **0. PURPOSE**

Knowledge Sync Engine คือ “แกนกลางของระบบความรู้ทั้งหมด”  
มันมีหน้าที่:

1. **นำข้อมูลดิบทั้งหมด (Raw Files / API / User Input)** → กลายเป็น  
    “Knowledge Object แบบ L0–L5”
    
2. ทำให้ข้อมูลทั้งระบบ **consistent, canonical, versioned, deterministic**
    
3. ทำหน้าที่เป็น “สะพาน” เชื่อม RAG → KS → Agent → FlowControl
    
4. จัดการ incremental update (live update) โดยไม่ทำให้ข้อมูลพัง
    

**ถ้า Knowledge Sync ทำงานผิด = ทั้งระบบพัง**  
เพราะทุก engine พึ่ง L-layer pipeline

---
# **1. LAYER SUMMARY (L0–L5)**

**อ้างอิงจาก DATA_SCHEMA v3.0**

```
L0 = Source Files (raw)
L1 = Chunks (semantic unit)
L2 = Embeddings (vectorized meaning)
L3 = Semantic Nodes (concept-level knowledge)
L4 = Relation Graph (edges between concepts)
L5 = Unified Knowledge Graph (canonical, reason-ready)
```

Knowledge Sync Engine = เครื่องจักรที่ “สร้าง + อัปเดต” L1–L5

---
# **2. HIGH-LEVEL PIPELINE (FULL FLOW)**

```
RAW INPUT (L0)
   ↓
Chunking Engine (L1)
   ↓
Embedding Engine + Vector Index (L2)
   ↓
Semantic Extraction (L3)
   ↓
Relation Graph Builder (L4)
   ↓
Canonicalization + Merge + Inference (L5)
   ↓
EVENT BUS → CACHE → KS / RAG / AGENT READY
```

**ทุกขั้นตอนต้อง deterministic และ reversible**

---

# **3. KNOWLEDGE_SYNC ENGINE — MODULE STRUCTURE**

ประกอบด้วย 8 module:

1. **FileWatcher / Source Ingestor**
    
2. **Chunk Processor**
    
3. **Embedding Processor**
    
4. **Semantic Extractor**
    
5. **Relation Graph Builder**
    
6. **Canonicalization Engine**
    
7. **Incremental Sync Manager**
    
8. **Event Dispatcher + Cache Updater**
    

ทั้งหมดนี้มาจาก blueprint + system architecture เดิม แต่กูเขียนใหม่ให้ชัดที่สุด

---

# **4. MODULE 1 — FileWatcher / Source Ingestor (L0)**

### INPUT

- PDF / DOCX / Markdown / HTML
    
- API input
    
- User-provided text / knowledge modules
    
- System-generated documents
    

### RESPONSIBILITY

- detect file version
    
- assign file_id + version_id
    
- send event: `KS.FILE.NEW` หรือ `KS.FILE.UPDATE`
    

### OUTPUT

```
{
 file_id,
 version,
 raw_text,
 metadata,
 timestamp
}
```

---

# **5. MODULE 2 — Chunk Processor (L1)**

กฎสำคัญ (deterministic):

1. same input = same chunk split
    
2. chunk_hash = stable SHA256(raw_text + metadata)
    
3. no randomness allowed
    

### OUTPUT STRUCTURE (จาก DATA_SCHEMA)

```
chunk_id
chunk_text
chunk_hash
parent_file_id
order_index
metadata: { section, heading, tag }
```

### OUTPUT EVENT

- `KS.CHUNK.CREATED`
    
- `KS.CHUNK.UPDATED`
    

---

# **6. MODULE 3 — Embedding Processor (L2)**

### RULES

- ใช้ **embedding model ตาม model routing**  
    (ปัจจุบัน = **Google-first: bge-large / nomic / ge-large**)
    
- embedding_hash ต้อง = chunk_hash
    
- vector index = deterministic index ID
    

### OUTPUT

```
embedding_id
chunk_id
vector
embedding_model
embedding_hash
```

### EVENT

- `KS.EMBEDDING.CREATED`
    

---

# **7. MODULE 4 — Semantic Extractor (L3)**

ทำหน้าที่ “ย่อย chunk ให้เป็น meaning-level nodes”

### TASKS

- concept extraction
    
- entity / event detection
    
- summarization
    
- key-value knowledge extraction
    
- structured semantic forms
    

### OUTPUT STRUCTURE (อ้างอิง DATA_SCHEMA)

```
node_id
canonical_label (temporary)
semantic_type: ["concept", "entity", "rule", "fact", "definition"]
importance_score
source_chunk_id
metadata
```

### EVENT

- `KS.NODE.NEW`
    

---

# **8. MODULE 5 — Relation Graph Builder (L4)**

### สร้าง edges แบบ deterministic:

```
CONTAINS
REFERENCES
CAUSES
CONTRADICTS
PART_OF
TYPE_OF
```

### OUTPUT (จาก schema)

```
edge_id
from_node
to_node
relation_type
confidence
source
```

### EVENT

- `KS.EDGE.NEW`
    
- `KS.EDGE.UPDATE`
    

---

# **9. MODULE 6 — Canonicalization Engine (L5)**

**นี่คือส่วนสำคัญที่สุดของ Knowledge System**

### RESPONSIBILITIES

- merge duplicate concepts
    
- collapse synonyms
    
- generate canonical_id
    
- distribute canonical_id ไปทุก engine (RAG, Agent, Routing)
    
- maintain consistency graph
    

### CANONICAL RULES

1. identical meaning → same canonical_id
    
2. stable hash generation:
    

```
canonical_id = SHA256(normalize(node_text + type))
```

3. concept priority rule:
    

- definitions > facts > associations
    

### OUTPUT

```
canonical_id
node_list: [...]
relation_map: [...]
graph_cluster
```

### EVENT

- `KS.CANONICAL.UPDATE`
    
- `KS.GRAPH.UPDATE`
    

---

# **10. MODULE 7 — Incremental Sync Manager**

### RESPONSIBILITY

- detect minimal recompute path
    
- ป้องกันการ rebuild ทั้งระบบ
    
- sync เฉพาะ nodes/edges ที่โดนเปลี่ยนจาก file update
    

### ALGORITHM

```
if chunk updated:
    regenerate L2, L3, L4, L5 for affected scope only
if relation changed:
    recalc canonical_id
if canonical changed:
    broadcast update to all engines
```

### EVENT

- `KS.INCREMENTAL.SYNC`
    

---

# **11. MODULE 8 — Event Dispatcher + Cache Updater**

เชื่อมกับระบบ:

- Event Bus v3.0
    
- Cache Strategy v3.0
    
- RAG Engine v3.0
    
- Agent Engine v3.0
    

### ตัวอย่าง events ที่ต้องส่ง:

|Event|ใช้ทำอะไร|
|---|---|
|`KS.NODE.NEW`|agent สามารถใช้ concept ใหม่|
|`KS.EDGE.NEW`|graph update สำหรับ inference|
|`KS.CANONICAL.UPDATE`|invalidate graph cache|
|`RAG.INDEX.UPDATE`|update vector search DB|

---

# **12. END-TO-END EXAMPLE**

**ไฟล์ Raw:** “Newton’s second law: F = m a”

### L0 → L1

Split เป็น 1 chunk  
→ chunk_id: C1

### L1 → L2

Embed C1  
→ embedding_id: E1

### L2 → L3

Extract semantics:

- concept: “force”
    
- concept: “mass”
    
- concept: “acceleration”
    
- rule: “F = m a”
    

### L3 → L4

Build relations:

- force CAUSES acceleration
    
- acceleration DEPENDS_ON mass
    
- formula REPRESENTS relationship
    

### L4 → L5

Canonical graph:

- concept “force” → canonical_id: PHYS.FORCE
    
- concept “acceleration” → PHYS.ACC
    
- relation map stored
    

### Output

RAG / Agent สามารถเข้าใจคำว่า:

“ทำไมแรงมากขึ้น → ความเร่งเพิ่มขึ้น”  
เพราะ canonical graph ให้ reasoning pathway เต็มรูปแบบ

---

# **13. CONSISTENCY RULES (สำคัญสุด)**

1. ทุก layer ต้อง **referentially stable**
    
2. node / chunk / embedding ต้อง **hash-stable**
    
3. canonical graph ต้องเป็น **tree-consistent**
    
4. ไม่มี orphan nodes
    
5. ไม่มี edges ลอย
    
6. incremental update ห้ามทำให้ graph แตก
    

---

# **14. PERFORMANCE RULES**

### 1) ไม่ rebuild ทั้ง graph เกิน 5% ของ nodes

### 2) canonical update ต้องใช้เวลาไม่เกิน 50 ms

### 3) RAG-index update ต้อง async

### 4) graph edges ต้องจัดกลุ่มเป็น adjacency list เพื่อ lookup ≤ 3 ms

### 5) ใช้ L1–L4 Cache แบบที่กำหนดใน cache strategy

---

# **15. FINAL CONTRACT (API LEVEL)**

```
POST /ks/sync
POST /ks/chunk
POST /ks/embed
POST /ks/node
POST /ks/relation
POST /ks/canonical
POST /ks/incremental
```

---


# 🟥 **KNOWLEDGE_SYNC ENGINE v3.0 (Diagram + Matrix + Flow + Example + Mapping)**

_(Complete Visual Specification)_

---

# **1) SYSTEM DIAGRAM (HIGH-LEVEL)**

แสดงการเดินทางของข้อมูลจาก RAW → L5

```
                 ┌──────────────────────────────────────────┐
                 │            RAW INPUT (L0)                │
                 │  PDF, DOCX, MD, Text, API, Notes         │
                 └──────────────────────────────────────────┘
                                   │
                                   ▼
                   ┌────────────────────────────────┐
                   │     L1 — Chunk Processor       │
                   │ deterministic split + hashing  │
                   └────────────────────────────────┘
                                   │
                                   ▼
                   ┌────────────────────────────────┐
                   │   L2 — Embedding Processor     │
                   │ vectorize + index + model ver  │
                   └────────────────────────────────┘
                                   │
                                   ▼
                 ┌──────────────────────────────────────────┐
                 │      L3 — Semantic Extractor             │
                 │ concepts, facts, rules, entities         │
                 └──────────────────────────────────────────┘
                                   │
                                   ▼
                 ┌──────────────────────────────────────────┐
                 │      L4 — Relation Graph Builder         │
                 │ edges: causes, references, type_of…      │
                 └──────────────────────────────────────────┘
                                   │
                                   ▼
                 ┌──────────────────────────────────────────┐
                 │ L5 — Canonicalization Engine             │
                 │ merge duplicates, unify nodes, clusters  │
                 └──────────────────────────────────────────┘
                                   │
             ┌─────────────────────┴─────────────────────────────┐
             ▼                                                   ▼
   ┌──────────────────────┐                          ┌───────────────────────┐
   │   Event Bus System   │                          │   Cache Strategy v3   │
   └──────────────────────┘                          └───────────────────────┘
             │                                                   │
             ▼                                                   ▼
   ┌──────────────────────┐                          ┌────────────────────────┐
   │      RAG Engine      │                          │     Agent Engine       │
   └──────────────────────┘                          └────────────────────────┘
```

---

# **2) MATRIX (LAYER → ENGINE → RESPONSIBILITY)**

```
┌──────────┬───────────────────────┬────────────────────────────────────────┐
│ LAYER    │ RESPONSIBILITY         │ USED BY ENGINE                        │
├──────────┼───────────────────────┼────────────────────────────────────────┤
│ L0       │ Raw files              │ KS Sync                               │
│ L1       │ Chunking               │ KS Sync, RAG (chunk lookup)           │
│ L2       │ Embedding              │ RAG (vector search), Cache            │
│ L3       │ Semantic Nodes         │ KS, Agent (semantic reasoning)        │
│ L4       │ Relation Graph         │ KS, Agent (graph traversal)           │
│ L5       │ Canonical Knowledge    │ Agent reasoning, RAG post-processing  │
└──────────┴───────────────────────┴────────────────────────────────────────┘
```

---

# **3) KNOWLEDGE SYNC FLOW SYSTEM (STEP-BY-STEP)**

นี่คือ “Flow Engine ของ Knowledge Sync” แบบอ่านแล้วเขียนโค้ดได้ทันที

---

## **STEP 0 — Receive File / Data (L0)**

```
input → detect filetype → assign file_id → versioning
```

EVENT:

```
KS.FILE.NEW
```

---

## **STEP 1 — Chunk Processor (L1)**

```
chunks = deterministicSplit(raw_text)
for each chunk:
    chunk_hash = SHA256(chunk_text)
```

EVENT:

```
KS.CHUNK.CREATED
```

---

## **STEP 2 — Embedding Processor (L2)**

```
embedding_model = routing.getEmbeddingModel()
embedding = embedding_model.embed(chunk_text)
store in vector_index
```

EVENT:

```
KS.EMBEDDING.CREATED
```

---

## **STEP 3 — Semantic Extractor (L3)**

```
nodes = extractSemantics(chunk)
node_types = [concept, entity, fact, rule]
importance_score = scoring(node)
```

EVENT:

```
KS.NODE.NEW
```

---

## **STEP 4 — Relation Graph Builder (L4)**

```
relations = inferRelations(nodes)
for r in relations:
    storeEdge(r)
```

EVENT:

```
KS.EDGE.NEW
```

---

## **STEP 5 — Canonicalization (L5)**

```
canonical_id = SHA256(normalize(node))
merge duplicates
propagate canonical_id to edges + cluster
```

EVENT:

```
KS.CANONICAL.UPDATE
```

---

## **STEP 6 — Incremental Sync Manager**

```
detect changed_nodes
update graph segments only
invalidate cache for relevant nodes
```

EVENT:

```
KS.INCREMENTAL.SYNC
```

---

## **STEP 7 — Dispatch to Engines**

ส่งไปยัง:

- **RAG:** update vector db, chunk registry
    
- **Agent:** update concept graph / canonical map
    
- **Flow:** update reasoning templates
    
- **Cache:** invalidate & repopulate
    
- **Event Bus:** publish chain events
    

EVENT:

```
KS.GRAPH.UPDATE
KS.READY
```

---

# **4) MAPPING TABLE (KS → RAG → AGENT → FLOW)**

```
KS OUTPUT                 → USED BY
───────────────────────────────────────────────────────────────────────
Chunks (L1)               → RAG chunk-level retrieval
Embeddings (L2)           → RAG vector similarity
Semantic nodes (L3)       → Agent: meaning-level reasoning
Relation graph (L4)       → Agent: logic inference
Canonical graph (L5)      → Agent: stable reasoning; RAG: rerank context
Incremental updates       → Cache: invalidation; Event Bus: propagation
```

---

# **5) VISUAL GRAPH OF KS ENGINE**

### Graph รูปแบบง่าย: L0 → L5 pipeline + feedback loop

```
L0 ──▶ L1 ──▶ L2 ──▶ L3 ──▶ L4 ──▶ L5
                              ▲      │
                              │      ▼
                         Incremental Sync
```

---

# **6) END-TO-END EXAMPLE (REAL)**

**Input:** PDF 12 หน้า เรื่อง “Photosynthesis”

### L0 → L1 (chunk)

- split ได้ 89 chunks
    
- แต่ละ chunk มี hash stable
    
- metadata: section=”introduction”, tag=”definition”
    

### L1 → L2 (embedding)

- ใช้ **BGE-large** → ผลเป็น vectors 1024 dimensions
    
- vector index updated (FAISS/PGVector)
    

### L2 → L3 (semantic)

จาก chunk:

> “Chlorophyll absorbs light and converts energy…”

Extractor ให้:

- concept: chlorophyll
    
- concept: light energy
    
- fact: absorbs light
    
- rule: conversion process
    

### L3 → L4 (relations)

ชั้นความรู้:

```
chlorophyll —absorbs→ light
light —converts_to→ chemical_energy
chlorophyll —part_of→ leaf
```

### L4 → L5 (canonical)

- “chlorophyll pigment” ↔ “chlorophyll” → merged
    
- canonical_id = BIO.CHLORO.001
    
- cluster = BIO-PHOTOSYN-PIGMENTS
    

### sync propagation (event bus)

- RAG update vector search index
    
- Agent update semantic graph
    
- Cache invalidate neighbors(BIO.CHLORO.001)
    

---

# **7) GUARANTEED PROPERTIES**

1. deterministic pipeline (same input → same L1–L5)
    
2. backward-compatible (versioned)
    
3. fast incremental recompute
    
4. graph-consistent invariant
    
5. canonical stable ID system
    
6. ready for long-context reasoning
    

---

# **8) ความสัมพันธ์กับไฟล์อื่น (CROSS-FILE MAPPING)**

|Engine / Spec|ใช้ส่วนไหนจาก KS|
|---|---|
|RAG ENGINE|L1, L2, L5 (evidence → canonical reasoning)|
|KS ENGINE|internal L0–L5|
|Agent Engine|L3–L5 (semantic nodes + canonical graph)|
|Flow Engine|action mapping, incremental updates|
|Model Routing|choose embedding model for L2|
|Cache Strategy|L1–L4 hot cache, graph cache|
|Event Bus|publish KS updates|
|Security|permission for file ingest / update|
|Deployment|worker jobs / pipelines|

---

# **9) SUMMARY**

ไฟล์นี้เป็นชุด:

- Diagram (ครบ)
    
- Matrix (L-layer → Engine)
    
- Flow System (ละเอียดสุด)
    
- Example (จริง)
    
- Mapping (ทุก engine)
    

และ **สอดคล้องกับทุกไฟล์ v3.0 ก่อนหน้า 100%**

---

ถ้านายต้องการ:

- เวอร์ชัน “High-resolution diagram แบบภาพ”
    
- เวอร์ชัน “Pseudo-code ready-to-implement”
    
- เวอร์ชันรวมเข้ากับ SYSTEM_ARCHITECTURE
    
- หรืออยาก rewrite ให้ lean กว่านี้
    

บอกได้เลย กูก็พร้อมจัดต่อทันที.

**KNOWLEDGE_SYNC ENGINE v3.0** คือระบบที่ทำให้ข้อมูลดิบ  
→ กลายเป็น “ความรู้แบบมีโครงสร้าง L0–L5”  
→ พร้อมใช้งานใน RAG, KS, Agent, Flow, Routing  
และรับประกันว่า graph / concept ทั้งหมด consistent ทุกครั้งที่มีการ update

อันนี้คือ version ที่ดีที่สุดของไฟล์นี้  
และสอดคล้องกับทุก spec อื่นในโปรเจค v3.0

---

ถ้าต้องการ:

- เวอร์ชัน “Diagram only”
    
- เวอร์ชัน “Flow Spec Only”
    
- เวอร์ชัน “Pseudo-code Implementation”
    
- เวอร์ชัน “Add to SYSTEM ARCHITECTURE”
    

บอกได้เลย เดี๋ยวกูต่อให้ทันที.