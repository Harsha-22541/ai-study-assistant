from pathlib import Path
import json
import faiss
import numpy as np
from services.embeddings import embed

STORE = Path(__file__).resolve().parents[1] / "data" / "vectorstore"
STORE.mkdir(parents=True, exist_ok=True)
INDEX_FILE = STORE / "index.faiss"
META_FILE = STORE / "metadata.json"

def add_documents(chunks):
    # chunks: [{"text":..., "filename":..., "page":...}]
    if not chunks:
        return
    vectors = np.asarray(embed([x["text"] for x in chunks]), dtype="float32")
    if INDEX_FILE.exists():
        index = faiss.read_index(str(INDEX_FILE))
        metadata = json.loads(META_FILE.read_text(encoding="utf-8"))
    else:
        index = faiss.IndexFlatIP(vectors.shape[1])
        metadata = []
    index.add(vectors)
    metadata.extend(chunks)
    faiss.write_index(index, str(INDEX_FILE))
    META_FILE.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")

def search(query, k=5):
    if not INDEX_FILE.exists():
        return []
    index = faiss.read_index(str(INDEX_FILE))
    metadata = json.loads(META_FILE.read_text(encoding="utf-8"))
    q = np.asarray(embed([query]), dtype="float32")
    scores, ids = index.search(q, min(k, index.ntotal))
    return [{**metadata[i], "score": float(score)} for score, i in zip(scores[0], ids[0]) if i >= 0]
