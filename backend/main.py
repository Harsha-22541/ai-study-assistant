from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.documents import router as documents_router
from routes.chat import router as chat_router
from routes.generators import router as generators_router
from database import init_db, stats

app = FastAPI(title="AI Study Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this to your frontend origin in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "AI Study Assistant backend is running"}

@app.get("/api/stats")
def get_stats():
    return stats()

app.include_router(documents_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(generators_router, prefix="/api")
