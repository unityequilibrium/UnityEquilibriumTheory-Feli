# สถาปัตยกรรม Retrieval-Augmented Generation (RAG) จากหลายแหล่งข้อมูล: เอกสารสรุปสำหรับผู้เชี่ยวชาญ

## 1. บทสรุปสำหรับผู้บริหาร (Executive Summary)

สถาปัตยกรรม Retrieval-Augmented Generation (RAG) ได้พัฒนาไปไกลกว่าแนวทางพื้นฐาน (naive approach) โดยมุ่งเน้นการแก้ไขข้อจำกัดด้านความแม่นยำในการดึงข้อมูล (retrieval) และการขาดบริบทที่สมบูรณ์ RAG ขั้นสูงจากหลายแหล่งข้อมูล (Multi-source RAG) ได้กลายเป็นมาตรฐานใหม่ โดยผสานรวมเทคนิคที่ซับซ้อนเพื่อเพิ่มประสิทธิภาพการทำงานของ Large Language Models (LLMs) อย่างมีนัยสำคัญ หัวใจสำคัญของสถาปัตยกรรมสมัยใหม่นี้คือการผสมผสานระหว่าง **การค้นหาแบบไฮบริด (Hybrid Search)** ซึ่งรวมการค้นหาตามความหมาย (semantic search) ผ่านเวกเตอร์ เข้ากับการค้นหาตามคำสำคัญ (keyword search) ด้วยอัลกอริทึมอย่าง BM25 เพื่อให้ได้ผลลัพธ์ที่ครอบคลุมทั้งความหมายและคำศัพท์เฉพาะทาง

นอกจากนี้ ไปป์ไลน์ RAG สมัยใหม่ยังประกอบด้วยขั้นตอนหลายชั้นที่สามารถปรับแต่งได้ (composable pipelines) โดยมี **Reranker** เป็นองค์ประกอบสำคัญในการจัดลำดับเอกสารที่ดึงมาใหม่ตามความเกี่ยวข้องกับคำค้นหาอย่างละเอียด ซึ่งช่วยลดภาระของ LLM และเพิ่มความแม่นยำของคำตอบ กลยุทธ์ **การแบ่งส่วนข้อมูล (Chunking)** ก็มีความซับซ้อนมากขึ้น โดยมีการใช้เทคนิคเช่น **การติดแท็กข้อมูลเมตา (Metadata Tagging)** ตามโครงสร้างของเอกสาร (เช่น หัวข้อ H1, H2) และ **Parent Document Retriever (PDR)** ที่ดึงข้อมูลส่วนย่อย (child chunk) ที่ตรงเป้า แต่ส่งมอบข้อมูลส่วนใหญ่ (parent chunk) เพื่อให้บริบทที่สมบูรณ์แก่ LLM เฟรมเวิร์กโอเพนซอร์สอย่าง LangChain และ LlamaIndex เป็นเครื่องมือหลักที่ช่วยให้นักพัฒนาสามารถสร้างและผสานรวมส่วนประกอบเหล่านี้เข้าด้วยกันได้อย่างมีประสิทธิภาพ ก่อให้เกิดระบบ RAG ที่แข็งแกร่ง แม่นยำ และตอบสนองต่อโจทย์ทางธุรกิจที่ซับซ้อนได้ดียิ่งขึ้น

--------------------------------------------------------------------------------

## 2. สถาปัตยกรรมและพิมพ์เขียวสำคัญ (Key Architectures or Blueprints)

สถาปัตยกรรม RAG สมัยใหม่ได้แตกแขนงออกเป็นหลายรูปแบบ โดยแต่ละรูปแบบถูกออกแบบมาเพื่อแก้ไขปัญหาเฉพาะด้านของการดึงข้อมูลและสร้างบริบท

### สถาปัตยกรรม RAG พื้นฐาน (Naive RAG) และข้อจำกัด

เวิร์กโฟลว์ของ RAG แบบพื้นฐานประกอบด้วยการแบ่งเอกสารขนาดใหญ่ออกเป็นส่วนย่อย (chunks) ที่แยกจากกันโดยสิ้นเชิง ซึ่งมักทำให้ข้อมูลสูญเสียบริบทและความเชื่อมโยงกับเนื้อหาโดยรวมของเอกสาร การค้นหาโดยใช้ความคล้ายคลึงทางความหมาย (semantic similarity) เพียงอย่างเดียวอาจไม่เพียงพอ ทำให้ประสิทธิภาพและคุณภาพการดึงข้อมูลลดลง

### สถาปัตยกรรม RAG แบบไฮบริด (Hybrid RAG)

นี่คือแนวทางที่ได้รับการยอมรับอย่างกว้างขวางเพื่อปรับปรุงประสิทธิภาพของ RAG พื้นฐาน โดยเป็นการผสานพลังของการค้นหาสองรูปแบบ:

1. **Dense Retrieval (Semantic Search)**: แปลงข้อความใน chunk ให้เป็นเวกเตอร์ (embeddings) และจัดเก็บใน Vector Database เพื่อค้นหาเอกสารที่มีความหมายใกล้เคียงกับคำค้นหา
2. **Sparse Retrieval (Keyword Search)**: ใช้อัลกอริทึมเช่น **BM25** หรือ **TF-IDF** เพื่อสร้างดัชนีคำสำคัญและค้นหาเอกสารที่มีคำศัพท์ตรงกับคำค้นหาอย่างแม่นยำ เหมาะสำหรับคำค้นหาที่มีคำเฉพาะทาง รหัสผลิตภัณฑ์ หรือชื่อเฉพาะ

ผลลัพธ์จากทั้งสองระบบจะถูกนำมารวมกัน โดยมักใช้เทคนิค **Reciprocal Rank Fusion (RRF)** เพื่อจัดลำดับและคัดเลือกเอกสารที่ดีที่สุดจากทั้งสองวิธี

### ไปป์ไลน์ RAG ขั้นสูงพร้อม Reranker (Advanced RAG with Reranker)

สถาปัตยกรรมนี้เป็นส่วนขยายของ Hybrid RAG โดยเพิ่มขั้นตอนการจัดลำดับใหม่ (Reranking) เข้ามาเพื่อเพิ่มความแม่นยำสูงสุด

1. **Initial Retrieval (การดึงข้อมูลขั้นต้น)**: ใช้ Hybrid Retriever (เช่น `EnsembleRetriever` ใน LangChain) เพื่อดึงเอกสารที่เกี่ยวข้องจำนวนหนึ่ง (Top-K) ซึ่งขั้นตอนนี้เน้นความเร็วและความครอบคลุม
2. **Reranking (การจัดลำดับใหม่)**: นำเอกสารที่ได้จากขั้นตอนแรกมาผ่านโมเดล **Cross-Encoder** (เช่น `BAAI/bge-reranker-v2-m3`) ซึ่งเป็นโมเดลที่มีประสิทธิภาพสูงแต่ใช้ทรัพยากรมากกว่า โมเดลนี้จะคำนวณคะแนนความเกี่ยวข้องระหว่าง "คำค้นหา" และ "เนื้อหาเอกสาร" แต่ละฉบับอย่างละเอียด แล้วจัดลำดับใหม่เพื่อให้เอกสารที่เกี่ยวข้องที่สุดอยู่ด้านบนสุดก่อนส่งให้ LLM

### RAG เชิงบริบท (Contextual RAG)

แนวทางนี้มุ่งเน้นการเพิ่มคุณภาพของข้อมูลในแต่ละ chunk ตั้งแต่ขั้นตอนการประมวลผลล่วงหน้า โดยการ **เติมข้อมูลบริบทเฉพาะของ chunk นั้นๆ** เข้าไปในทุก chunk ก่อนที่จะนำไปสร้าง embeddings เทคนิคนี้ได้รับแรงบันดาลใจจากแนวทางของ Anthropic ซึ่งจะมีการสร้างบทสรุปสั้นๆ ที่อธิบายว่า chunk ดังกล่าวเกี่ยวข้องกับเอกสารโดยรวมอย่างไร แล้วผนวกเข้าไปที่ส่วนต้นของ chunk นั้นๆ

### กลยุทธ์การแบ่งส่วนเอกสารขั้นสูง (Advanced Chunking Strategies)

|   |   |   |
|---|---|---|
|กลยุทธ์|คำอธิบาย|จุดเด่น|
|**การแบ่งส่วนตามโครงสร้างและ Metadata**|แบ่งเอกสารตามโครงสร้างทางตรรกะ เช่น หัวข้อ H1, H2, H3 และติดแท็ก Metadata เหล่านี้ไปกับแต่ละ chunk|- ช่วยให้สามารถกรองการค้นหาตามโครงสร้างเอกสารได้<br>- รักษาลำดับชั้นและความสัมพันธ์ของข้อมูล<br>- ลดปัญหาการตัดประโยคหรือย่อหน้ากลางคัน|
|**Parent Document Retriever (PDR)**|สร้าง chunk ย่อย (child chunks) ที่มีความเฉพาะเจาะจงสูงเพื่อใช้ในการค้นหา แต่เมื่อพบ chunk ที่เกี่ยวข้อง จะทำการดึง chunk ใหญ่ (parent chunk) ที่ครอบคลุมเนื้อหานั้นๆ มาใช้งาน|- LLM ได้รับบริบทที่สมบูรณ์และกว้างขึ้น<br>- ลดปัญหาสูญเสียข้อมูลสำคัญที่อาจอยู่รอบๆ chunk ที่ถูกค้นเจอ<br>- เพิ่มความแม่นยำในการตอบคำถามที่ต้องการความเข้าใจในภาพรวม|
|**Meta Chunking**|จัดกลุ่มประโยคหรือย่อหน้าที่มีความหมายใกล้เคียงกันเข้าไว้ด้วยกันเป็น chunk โดยใช้หลักการว่าประโยคที่อยู่ติดกันมักมีความเชื่อมโยงทางตรรกะ|- สร้าง chunk ที่มีความสอดคล้องทางความหมาย (semantic coherence)<br>- เหมาะสำหรับเอกสารทั้งขนาดสั้นและยาว|

### RAG แบบปรับตัวได้และแบบหลายขั้นตอน (Adaptive & Composable RAG)

- **Adaptive RAG**: เป็นสถาปัตยกรรมที่เพิ่มขั้นตอนการ "ประเมินผล" เข้าไปในไปป์ไลน์ เช่น ใช้ **Retrieval Grader** (ซึ่งเป็น LLM อีกตัว) เพื่อตรวจสอบว่าเอกสารที่ดึงมานั้นเกี่ยวข้องกับคำถามจริงหรือไม่ ก่อนที่จะส่งไปให้ LLM ตัวหลักสร้างคำตอบ หากไม่เกี่ยวข้อง ระบบอาจทำการค้นหาใหม่หรือแจ้งผู้ใช้
- **ComposeRAG**: เป็นเฟรมเวิร์กที่แบ่งกระบวนการตอบคำถามซับซ้อน (multi-hop) ออกเป็นโมดูลย่อยๆ ที่ทำงานต่อกันได้ เช่น การแยกคำถาม (question decomposition), การเขียนคำค้นหาใหม่ (query rewriting), การจัดลำดับเอกสาร (passage reranking) และการตรวจสอบคำตอบ (answer verification)

--------------------------------------------------------------------------------

## 3. ตัวอย่างการใช้งาน (Implementation Snippets)

ตัวอย่างโค้ดต่อไปนี้แสดงการใช้งานองค์ประกอบหลักในสถาปัตยกรรม RAG ขั้นสูง โดยใช้เฟรมเวิร์ก LangChain

### การค้นหาแบบไฮบริดด้วย EnsembleRetriever

การผสมผสานระหว่าง BM25 (keyword) และ Vector Search (semantic) เพื่อดึงข้อมูลจากหลายมุมมอง

```python
# สมมติว่า docs คือรายการเอกสารที่ผ่านการประมวลผลแล้ว
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 1. ตั้งค่า Keyword Retriever (BM25)
bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 5

# 2. ตั้งค่า Semantic Retriever (Vector Store)
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)
similarity_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 3. รวม Retriever ทั้งสองเข้าด้วยกัน
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, similarity_retriever],
    weights=[0.5, 0.5] # กำหนดน้ำหนักความสำคัญ
)
```

### การเพิ่ม Reranker เข้าไปในไปป์ไลน์

หลังจากได้ผลลัพธ์จาก `EnsembleRetriever` แล้ว จะใช้ `ContextualCompressionRetriever` ร่วมกับ Cross-Encoder เพื่อจัดลำดับผลลัพธ์ใหม่

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# 1. โหลดโมเดล Reranker จาก Hugging Face
reranker_model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")

# 2. สร้าง Compressor สำหรับการจัดลำดับใหม่
compressor = CrossEncoderReranker(model=reranker_model, top_n=5)

# 3. สร้าง Retriever สุดท้ายที่รวม Reranker เข้าไปด้วย
# base_retriever ในที่นี้คือ ensemble_retriever จากตัวอย่างก่อนหน้า
final_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=ensemble_retriever
)

# เมื่อเรียกใช้ final_retriever จะได้เอกสารที่ผ่านการจัดลำดับใหม่และมีความเกี่ยวข้องสูงสุด
# relevant_docs = final_retriever.invoke("your_query")
```

### การติดแท็ก Metadata ระหว่างการแบ่งส่วนข้อมูล

ตัวอย่างนี้แสดงการสร้าง `index_schema` สำหรับ Redis vector store โดยดึงค่าจาก metadata ของเอกสาร เพื่อให้สามารถกรองการค้นหาได้

```python
# docs คือ List[Document] ที่แต่ละ Document มี metadata เช่น {'article_h1_main': '...'}
def build_index_schema(documents):
    schema = {"text": []}
    for doc in documents:
        for key in doc.metadata:
            name_dict = {"name": f"{key}"}
            if name_dict not in schema["text"]:
                schema["text"].append(name_dict)
    return schema

index_schema = build_index_schema(docs)
# {'text': [{'name': 'article_h1_main'}, {'name': 'article_h2_subsection'}, ...]}

# สร้าง Vector Store พร้อม schema ที่กำหนด
# vectorstore = Redis.from_documents(
#     docs,
#     embeddings,
#     redis_url='redis://localhost:6379',
#     index_schema=index_schema
# )
```

--------------------------------------------------------------------------------

## 4. ข้อดี ข้อเสีย และข้อจำกัด (Pros, Cons, Limitations)

|   |   |
|---|---|
|ด้าน|รายละเอียด|
|**ข้อดี (Pros)**|**- ความแม่นยำสูงขึ้น:** การค้นหาแบบไฮบริดและ Reranker ช่วยให้ได้เอกสารที่ตรงกับเจตนาของผู้ใช้มากที่สุด ทั้งในเชิงความหมายและคำสำคัญ<br>**- บริบทที่ดีกว่า:** เทคนิคอย่าง Parent Document Retriever และ Contextual RAG ช่วยลดปัญหาสูญเสียบริบท ทำให้ LLM สร้างคำตอบที่สมบูรณ์และลดการสร้างข้อมูลเท็จ (hallucination)<br>**- การค้นหาที่ยืดหยุ่น:** การใช้ Metadata ทำให้สามารถสร้างระบบค้นหาที่กรองข้อมูลตามเงื่อนไขเฉพาะได้ ซึ่งสำคัญมากในระดับองค์กร<br>**- ลดการพึ่งพา LLM:** Reranker ช่วยกรองและจัดลำดับเอกสารก่อนถึง LLM ทำให้ลดจำนวนโทเค็นที่ไม่จำเป็นและลดภาระการประมวลผลของโมเดลหลัก|
|**ข้อเสีย (Cons)**|**- ความซับซ้อนที่เพิ่มขึ้น:** สถาปัตยกรรมมีความซับซ้อนในการออกแบบ, พัฒนา, และบำรุงรักษาสูงกว่า RAG พื้นฐาน<br>**- ค่าใช้จ่ายและ Latency สูงขึ้น:** การเรียกใช้ Retriever หลายตัวและโมเดล Cross-Encoder สำหรับ Reranking ใช้เวลาและพลังการประมวลผลสูงกว่า ทำให้ต้นทุนต่อคำค้นหาและเวลาในการตอบสนอง (latency) เพิ่มขึ้น<br>**- ต้องการการปรับจูน:** การกำหนดน้ำหนักใน `EnsembleRetriever` หรือการเลือกเกณฑ์คะแนน (threshold) ใน Reranker อาจต้องมีการทดลองและปรับจูนเพื่อให้ได้ประสิทธิภาพสูงสุดสำหรับชุดข้อมูลนั้นๆ|
|**ข้อจำกัด (Limitations)**|**- ปัญหา "Lost in the Middle":** แม้จะได้บริบทที่ดี แต่ LLM ยังมีแนวโน้มที่จะให้ความสำคัญกับข้อมูลที่อยู่ตอนต้นและตอนท้ายของ Prompt มากกว่าข้อมูลที่อยู่ตรงกลาง<br>**- คุณภาพขึ้นอยู่กับการแบ่งส่วนข้อมูล:** ประสิทธิภาพของระบบโดยรวมยังคงขึ้นอยู่กับคุณภาพของการแบ่งส่วนข้อมูล (chunking) ซึ่งยังคงเป็นความท้าทายและไม่มีวิธีใดที่ดีที่สุดสำหรับทุกกรณี<br>**- การจัดการข้อมูลหลายรูปแบบ (Multi-modal):** แม้สถาปัตยกรรมจะรองรับได้ แต่การจัดการกับข้อมูลที่ไม่ใช่ข้อความ เช่น รูปภาพ ตาราง หรือเสียง ยังคงมีความซับซ้อนและต้องใช้เครื่องมือเฉพาะทางเพิ่มเติม|

--------------------------------------------------------------------------------

## 5. แหล่งข้อมูล / การอ้างอิง (Sources / References)

เอกสารนี้รวบรวมข้อมูลจากเฟรมเวิร์กและโครงการโอเพนซอร์สต่างๆ ที่เป็นแกนหลักในการพัฒนาระบบ RAG สมัยใหม่

### เฟรมเวิร์กและไลบรารีหลัก

- **LangChain**: เฟรมเวิร์กสำหรับสร้างแอปพลิเคชันที่ขับเคลื่อนด้วย LLM มีเครื่องมือสำเร็จรูปสำหรับสร้างไปป์ไลน์ RAG ที่ซับซ้อน ([https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain))
- **LlamaIndex**: เฟรมเวิร์กที่เน้นด้านการเชื่อมต่อข้อมูล (data connectivity) และการดึงข้อมูล (retrieval) สำหรับ RAG โดยเฉพาะ มีความสามารถในการจัดการดัชนีและตัวดึงข้อมูลที่หลากหลาย
- **RAGatouille**: ไลบรารีที่เน้นทำให้การใช้งานโมเดล ColBERT (late-interaction retrieval) เป็นเรื่องง่าย ซึ่งมีประสิทธิภาพสูงในการดึงข้อมูลสำหรับโดเมนที่ซับซ้อน ([https://github.com/AnswerDotAI/RAGatouille](https://github.com/AnswerDotAI/RAGatouille))

### โครงการ RAG โอเพนซอร์สตัวอย่าง

- **R2R (RAG to Riches)**: RAG engine แบบ end-to-end ที่สามารถติดตั้งใช้งานได้ทันที ([https://github.com/SciPhi-AI/R2R](https://github.com/SciPhi-AI/R2R))
- **rag_blueprint**: กรอบการทำงานแบบโมดูลาร์สำหรับสร้างและปรับใช้ระบบ RAG พร้อมการประเมินผลและติดตามในตัว ([https://github.com/feld-m/rag_blueprint](https://github.com/feld-m/rag_blueprint))
- **rag-with-reranker**: ตัวอย่างการใช้งาน RAG ที่เน้นการใช้ Reranker เพื่อเพิ่มความแม่นยำ ([https://github.com/nikhilraj-1/rag-with-reranker](https://github.com/nikhilraj-1/rag-with-reranker))
- **Multi-Tenant RAG System**: ระบบ RAG สำหรับการใช้งานแบบหลายผู้เช่า (Multi-Tenant) สร้างด้วย FastAPI, Qdrant และ Streamlit ([https://github.com/mominalix/Multi-Tenant-Retrieval-Augmented-Generation-RAG-System](https://github.com/mominalix/Multi-Tenant-Retrieval-Augmented-Generation-RAG-System))
- **fastapi-langgraph-agent-production-ready-template**: Template สำหรับสร้าง AI Agent ที่พร้อมใช้งานจริงด้วย FastAPI และ LangGraph ([https://github.com/wassim249/fastapi-langgraph-agent-production-ready-template](https://github.com/wassim249/fastapi-langgraph-agent-production-ready-template))
- **Building-advanced-hybrid-RAG-application**: ตัวอย่างการสร้าง RAG ขั้นสูงที่ใช้ pgvectorscale ([https://github.com/Jaimboh/Building-advanced-hybrid-RAG-application](https://github.com/Jaimboh/Building-advanced-hybrid-RAG-application))