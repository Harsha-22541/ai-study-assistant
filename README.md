# AI Study Assistant – HTML/CSS/JavaScript + FastAPI

A medium-level B.Tech CSE AI project using a normal web frontend instead of Streamlit.

## Stack

Frontend:
- HTML5
- CSS3
- Vanilla JavaScript
- Fetch API

Backend:
- FastAPI
- Sentence Transformers
- FAISS
- PyPDF
- python-docx
- OpenAI API
- SQLite

## Features

- PDF/DOCX/TXT upload
- Text extraction
- Chunking
- Embeddings
- FAISS vector search
- RAG document Q&A
- Source/page references
- Summarization
- MCQ generation
- Important questions
- Flashcards
- Study notes
- Explain Simply
- Study planner
- SQLite statistics

## Setup

### 1. Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Never put this key in frontend JavaScript.

### 4. Start backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Backend:
http://127.0.0.1:8000

API docs:
http://127.0.0.1:8000/docs

### 5. Start frontend

Open a second terminal:

```bash
cd frontend
python -m http.server 5500
```

Open:
http://127.0.0.1:5500

You can also use VS Code Live Server.

## RAG pipeline

Document → text extraction → cleaning → chunks → Sentence Transformer embeddings → FAISS → similarity search → relevant context → LLM → answer + sources.

## Important MVP note

Quiz submission in this starter is intentionally not falsely graded against hidden answers. A production version should return a `quiz_id` with generated questions, store the answer key server-side, and submit `{quiz_id, answers}` for secure grading.

## Future enhancements

- Authentication
- Multiple users
- Persistent per-user vector stores
- Streaming AI responses
- Better document deletion/re-indexing
- Secure quiz IDs
- Charts and analytics
- OCR for scanned PDFs
- Cloud deployment
