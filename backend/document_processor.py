from pathlib import Path
import re

def clean_text(text: str) -> str:
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def chunk_text(text: str, chunk_size=800, overlap=100):
    text = clean_text(text)
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks

def extract_text(path: str):
    ext = Path(path).suffix.lower()
    if ext == ".txt":
        return [(clean_text(Path(path).read_text(encoding="utf-8", errors="ignore")), 1)]
    if ext == ".pdf":
        from pypdf import PdfReader
        reader = PdfReader(path)
        return [(clean_text(page.extract_text() or ""), i + 1) for i, page in enumerate(reader.pages)]
    if ext == ".docx":
        from docx import Document
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return [(clean_text(text), 1)]
    raise ValueError("Unsupported file type")
