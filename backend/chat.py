from fastapi import APIRouter, HTTPException
from schemas import ChatRequest
from database import connect, stats
from services.rag import answer_question

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    try:
        result = answer_question(req.question)
        con = connect()
        chat_id = con.execute("SELECT id FROM chats ORDER BY id DESC LIMIT 1").fetchone()
        if not chat_id:
            cur = con.execute("INSERT INTO chats(title) VALUES(?)", (req.question[:50],))
            chat_id = (cur.lastrowid,)
        con.execute("INSERT INTO messages(chat_id,role,content) VALUES(?,?,?)",(chat_id[0],"user",req.question))
        con.execute("INSERT INTO messages(chat_id,role,content) VALUES(?,?,?)",(chat_id[0],"assistant",result["answer"]))
        con.commit(); con.close()
        result["stats"] = stats()
        return result
    except Exception as e:
        raise HTTPException(500, str(e))
