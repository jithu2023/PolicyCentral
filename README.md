# 🛡️ AarogyaAid - AI-Powered Insurance Recommendation Platform

An empathetic, RAG-based health insurance advisor that helps users find the right policy based on their health profile, lifestyle, and financial situation.

> **Built for:** AarogyaAid AI Engineering Assignment  
> **Timeline:** 2 Days | **Status:** ✅ Production Ready

---

## 📋 Quick Navigation

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [AI Framework Justification](#-ai-framework-justification-required-by-spec)
- [Recommendation Logic](#-recommendation-logic)
- [Document Parsing & Chunking](#-document-parsing--chunking)
- [Setup Instructions](#-setup-instructions)
- [Running the Application](#-running-the-application)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Demo Credentials](#-demo-credentials)
- [Compliance Checklist](#-compliance-checklist)

---

## ✨ Features

### User Portal

| Feature | Implementation |
|---------|----------------|
| **6-field profile form** | Name, Age, Lifestyle, Pre-existing Conditions, Income, City Tier |
| **AI recommendations with RAG** | Retrieved from uploaded policy docs - no hallucination |
| **Peer Comparison Table** | 3 policies with Premium, Cover Amount, Waiting Period, Score |
| **Coverage Details Table** | Inclusions, Exclusions, Sub-limits, Co-pay %, Claim type |
| **Why This Policy** | 150-250 words referencing 3+ profile fields |
| **Chat Explainer** | Term definitions, personalized examples, session memory |
| **Medical Guardrail** | Declines medical advice ("Please consult a doctor") |

### Admin Panel

| Feature | Implementation |
|---------|----------------|
| **Secure authentication** | HTTP Basic Auth (env variables) |
| **Multi-format upload** | PDF (pdfplumber), TXT (UTF-8), JSON (recursive extraction) |
| **Document management** | View, Edit, Delete from vector store |
| **Vector store sync** | Immediate removal from RAG pipeline |

---

## 🛠️ Tech Stack

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Frontend** | React 18 + Vite | Fast HMR, component reusability, excellent DX |
| **Backend** | FastAPI | Async support, automatic OpenAPI docs, Python type hints |
| **AI Framework** | LangChain + Groq | See detailed justification below |
| **Vector Store** | ChromaDB | Lightweight, persistent, perfect for local RAG |
| **Database** | SQLite | Zero-config, ACID compliant for session storage |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | 80MB, good semantic search, 384-dim vectors |
| **PDF Parsing** | pdfplumber | Handles complex PDFs, table extraction |
| **LLM** | Groq (Llama 3.3 70B) | 1200+ tokens/sec, free tier, excellent reasoning |

---

## 🤖 AI Framework Justification (Required by Spec)

**Why LangChain + Groq instead of Google ADK?**

I evaluated both frameworks against the assignment requirements:

| Criteria | Google ADK | LangChain + Groq | Winner |
|----------|------------|------------------|--------|
| RAG simplicity | Custom implementation needed | `similarity_search()` in 3 lines | LangChain |
| Response speed | 50-100 t/s (standard GPU) | 1200+ t/s (Groq LPU) | Groq |
| Structured output | Requires tool-calling | Native prompt templating | LangChain |
| 48-hour velocity | Steeper learning curve | Abstractions ready | LangChain |
| Cost | Requires GCP account | Free tier (30 req/min) | Groq |

**Decision: LangChain + Groq**

1. **RAG Simplicity**: ChromaDB integration provides production-ready retrieval without building from scratch
2. **Performance**: Groq's LPU delivers sub-3 second responses even with 70B models - critical for real-time recommendations
3. **Structured Output**: The three-section requirement (tables + prose) is reliably handled by LangChain's prompt templating
4. **Development Velocity**: With 48-hour deadline, LangChain's abstractions for embeddings, vector stores, and chat memory accelerated development significantly
5. **Accessibility**: Groq's free tier means reviewers can test without provisioning API keys

**Trade-off**: ADK offers better Google Cloud integration and production-grade orchestration, but for this RAG-heavy, low-latency, empathy-focused use case, LangChain + Groq is the pragmatic choice.

---

## 🧠 Recommendation Logic

### Matching Algorithm: Semantic RAG (No Hardcoded Rules)

```
User Profile → Query Construction → Vector Similarity Search → Retrieved Chunks → LLM Reasoning → Structured Output
```

### How Each Field Influences the Recommendation

| Field | Input Options | Influence Logic |
|-------|---------------|-----------------|
| **Name** | Free text | Personalizes greetings and policy summaries |
| **Age** | 1-99 | Premium bracket, waiting period sensitivity, peer comparison group |
| **Lifestyle** | Sedentary/Moderate/Active/Athlete | Risk weighting; active users prioritized for OPD cover |
| **Pre-existing Conditions** | Diabetes, Hypertension, Asthma, Cardiac, None, Other | Primary driver for exclusion matching and waiting period flagging |
| **Income** | under 3L/3-8L/8-15L/15L+ | Coverage amount target and premium affordability threshold |
| **City/Tier** | Metro/Tier-2/Tier-3 | Network hospital availability and claim settlement estimates |

### Retrieval Strategy

1. **Query Construction**: Converts profile to natural language
   - Example: *"Health insurance for 45-year-old with diabetes, living in Metro"*
2. **Semantic Search**: Cosine similarity retrieves top 5 policy chunks
3. **Context Assembly**: Retrieved chunks + profile data
4. **LLM Reasoning**: Groq generates structured output with source attribution

### Example Flow

```
Input: 52yo, sedentary, diabetes+hypertension, 8-15L income, Tier-2
  ↓
Query: "Insurance for 52yo sedentary diabetic hypertensive from Tier-2"
  ↓
Retrieved: Policy chunks mentioning waiting periods, diabetes coverage, co-pay
  ↓
Output: HDFC ERGO (higher cover, restoration benefit despite longer waiting period)
```

### Empathy & Tone Implementation

The prompt explicitly requires:
- Acknowledge health situation before presenting numbers
- Define insurance terms on first use
- Provide alternative paths for high-cost scenarios
- Never use clinical detachment

**Example output:**
> *"I understand you're managing diabetes and hypertension. Let me help you find a policy that covers your needs..."*

---

## 📄 Document Parsing & Chunking

### Parsing Strategy by Format

| Format | Parser | Fallback |
|--------|--------|----------|
| **PDF** | pdfplumber (extracts text + tables) | PyPDF2 |
| **TXT** | Native UTF-8 text extraction | Latin-1 decoding |
| **JSON** | Recursive field extraction | Stringify entire object |

### Chunking Strategy

```python
chunk_size = 500 words
overlap = 50 words (10%)
```

**Why these values:**
- **500 words**: Optimal for sentence-transformers/all-MiniLM-L6-v2 (512 token limit)
- **10% overlap**: Prevents context loss at chunk boundaries
- **Semantic boundaries**: Prefer paragraph breaks when available

### Metadata Stored Per Chunk

```json
{
  "source": "policy1.pdf",
  "type": "policy",
  "chunk_id": 0,
  "policy_name": "Star Health Plus",
  "total_chunks": 12,
  "file_type": "PDF"
}
```

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.11+ (3.14 works, 3.11 recommended)
- Node.js 18+
- Groq API key ([free at console.groq.com](https://console.groq.com))

### Step 1: Clone & Backend Setup

```bash
git clone <your-repo-url>
cd PolicyCentral/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
cp .env.example .env
```

**.env.example** (copy this to .env):

```env
GROQ_API_KEY=your_groq_api_key_here
ADMIN_USER=admin
ADMIN_PASS=admin123
```

> **⚠️ Important:** Never commit your `.env` file. The `.env.example` is provided as a template.

### Step 3: Frontend Setup

```bash
cd ../frontend
npm install
```

---

## ▶️ Running the Application

### Terminal 1 - Backend

```bash
cd backend
venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

### Access Points

| URL | Purpose |
|-----|---------|
| http://localhost:5173 | User Portal |
| http://localhost:8000/docs | Backend API Docs |
| http://localhost:8000/admin/policies | Admin API |

---

## 🧪 Testing

### Upload Sample Policies

```bash
cd backend
python test_upload.py
```

### Test Recommendation Engine

```bash
python test_recommendation_real.py
```

### Test Chat & Session Memory

```bash
python test_chat.py
```

### Verify Vector Store Contents

```bash
python debug_policies.py
```

**Expected Output:**
```
Total chunks found: 15
Sources: policy1.txt (5 chunks), policy2.json (5 chunks), policy3.pdf (5 chunks)
```

---

## 📁 Project Structure

```
PolicyCentral/
├── backend/
│   ├── core/
│   │   └── llm.py              # Groq LLM configuration
│   ├── rag/
│   │   └── vectorstore.py      # ChromaDB + embeddings
│   ├── routes/
│   │   ├── admin.py            # Upload/Edit/Delete with auth
│   │   ├── chat.py             # Chat + session memory
│   │   └── recommendation.py   # RAG recommendation
│   ├── services/
│   │   ├── policy_service.py   # PDF/TXT/JSON parsing
│   │   └── recommendation_service.py  # Prompt engineering
│   ├── database.py             # SQLite session storage
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt
│   ├── .env.example
│   ├── sample_policies/        # 3+ demo policy files
│   ├── test_upload.py
│   ├── test_chat.py
│   └── test_recommendation_real.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProfileForm.jsx     # Exactly 6 fields
│   │   │   ├── Recommendation.jsx  # 3-section output
│   │   │   ├── ChatBox.jsx         # Interactive chat
│   │   │   └── AdminPanel.jsx      # Policy management
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── README.md
└── PRD.md
```

---

## 🔑 Demo Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

---

## 📝 Sample Policy Documents

Three sample policies are included in `backend/sample_policies/`:

| File | Format | Content |
|------|--------|---------|
| policy1.txt | TXT | Aarogya Plus - Star Health |
| policy2.json | JSON | Family First Complete - HDFC ERGO |
| policy3.pdf | PDF | Care Basic Health Insurance |

Reviewers can upload these or their own PDF/TXT/JSON files.

---

## ✅ Compliance Checklist

| Requirement | Spec Section | Status | Evidence |
|-------------|--------------|--------|----------|
| Exactly 6 fields | 3.1 | ✅ | ProfileForm.jsx has 6 inputs |
| RAG grounding (no hallucination) | 4.2 | ✅ | vectorstore.similarity_search() |
| Peer comparison table | 3.2.2 | ✅ | Recommendation.jsx parses markdown table |
| Coverage details table | 3.2.2 | ✅ | Extracted from LLM output |
| Why this policy (150-250 words) | 3.2.2 | ✅ | Prompt enforces length, 3+ fields referenced |
| Term definitions in chat | 3.3 | ✅ | ChatBox.jsx + test_chat.py passes |
| Personalized examples | 3.3 | ✅ | Uses user's conditions from database |
| Session memory | 3.3 | ✅ | SQLite + database.py persists profiles |
| Admin upload/edit/delete | 3.4 | ✅ | AdminPanel.jsx + admin.py |
| Multi-format (PDF/TXT/JSON) | 3.4 | ✅ | policy_service.py handles all three |
| Medical advice guardrail | 4.2 | ✅ | Prompt instruction + test_chat.py |
| No hardcoded secrets | 4.3 | ✅ | .env.example provided |
| Unit test | 4.3 | ✅ | test_recommendation_real.py |

---

## 🙏 Acknowledgments

- **Groq** for free high-speed LLM inference (1200+ tokens/sec)
- **LangChain** for RAG abstractions
- **Sentence-transformers** for quality embeddings
- **AarogyaAid** for the thoughtful assignment

