import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "study_assistant.db"

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    con = connect()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS documents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        file_path TEXT,
        status TEXT DEFAULT 'Processed',
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS chats(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        role TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS quiz_results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        total INTEGER,
        percentage REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    con.commit()
    con.close()

def stats():
    con = connect()
    cur = con.cursor()
    docs = cur.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    questions = cur.execute("SELECT COUNT(*) FROM messages WHERE role='user'").fetchone()[0]
    quizzes = cur.execute("SELECT COUNT(*) FROM quiz_results").fetchone()[0]
    avg = cur.execute("SELECT COALESCE(AVG(percentage),0) FROM quiz_results").fetchone()[0]
    con.close()
    return {"documents": docs, "questions": questions, "quizzes": quizzes, "avg_score": round(avg, 2)}
