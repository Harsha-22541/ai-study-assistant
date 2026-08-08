from services.vector_store import search
from services.llm_service import ask

SYSTEM = """You are an academic study assistant.
Answer primarily from the supplied study context.
If the context does not contain the answer, say:
"I could not find this information in your uploaded study material."
Do not invent document-specific facts."""

def answer_question(question):
    hits = search(question, 5)
    if not hits:
        return {"answer": "No processed study material is available yet. Upload and process a document first.", "sources": []}
    context = "\n\n".join(
        f"[Source: {h['filename']}, page {h.get('page','?')}]\n{h['text']}" for h in hits
    )
    prompt = f"Study context:\n{context}\n\nStudent question:\n{question}\n\nGive a clear B.Tech-level explanation."
    result = ask(prompt, SYSTEM)
    if result is None:
        result = "LLM API key is not configured. The RAG retrieval found relevant material, but an AI answer cannot be generated until OPENAI_API_KEY is configured."
    sources = [{"filename": h["filename"], "page": h.get("page")} for h in hits]
    return {"answer": result, "sources": sources}
