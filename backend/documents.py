from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil, json
from database import connect, stats
from services.document_processor import extract_text, chunk_text
from services.vector_store import add_documents

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/documents/upload")
async def upload(files: list[UploadFile] = File(...)):
    processed = []
    for f in files:
        ext = Path(f.filename or "").suffix.lower()
        if ext not in {".pdf",".docx",".txt"}:
            raise HTTPException(400, f"Unsupported file: {f.filename}")
        path = UPLOAD_DIR / Path(f.filename).name
        with path.open("wb") as out:
            shutil.copyfileobj(f.file, out)
        try:
            pages = extract_text(str(path))
            chunks = []
            for text, page in pages:
                for chunk in chunk_text(text):
                    chunks.append({"text": chunk, "filename": f.filename, "page": page})
            if not chunks:
                raise ValueError("Document contains no extractable text")
            add_documents(chunks)
        except Exception as e:
            raise HTTPException(500, f"Could not process {f.filename}: {e}")
        con = connect()
        con.execute("INSERT INTO documents(filename,file_path,status) VALUES(?,?,?)",(f.filename,str(path),"Processed"))
        con.commit(); con.close()
        processed.append(f.filename)
    return {"message": f"Processed {len(processed)} document(s).", "files": processed, "stats": stats()}

@router.get("/documents")
def list_documents():
    con = connect()
    rows = con.execute("SELECT id,filename,status,uploaded_at FROM documents ORDER BY id DESC").fetchall()
    con.close()
    return {"documents":[{"id":r[0],"filename":r[1],"status":r[2],"uploaded_at":r[3]} for r in rows], "stats":stats()}
