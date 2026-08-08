from services.vector_store import search
from services.llm_service import ask

def context():
    hits = search("main concepts definitions important topics formulas examples", 8)
    return "\n\n".join(f"[{h['filename']} p.{h.get('page','?')}]\n{h['text']}" for h in hits)

def generate(prompt, fallback):
    result = ask(prompt)
    return result if result else fallback

def summary(kind):
    c = context()
    return generate(f"""Create a {kind} study summary from this material.
Use headings and bullet points. Do not add facts not supported by the material.
Material:
{c}""", "Add documents and configure OPENAI_API_KEY to generate an AI summary.")

def important_questions():
    c = context()
    return generate(f"""Generate exam-oriented questions from this material.
Separate into 2-mark, 5-mark and 10-mark sections.
Material:
{c}""", "Add documents and configure OPENAI_API_KEY to generate questions.")

def notes():
    c = context()
    return generate(f"""Create structured B.Tech revision notes from this material.
Include definitions, key concepts, formulas if present, examples, advantages, disadvantages and applications.
Material:
{c}""", "Add documents and configure OPENAI_API_KEY to generate notes.")

def explain(text, level):
    return generate(f"""Explain the following text at {level} level.
Keep the meaning accurate and use a simple example if helpful.
Text:
{text}""", "Configure OPENAI_API_KEY to enable AI explanations.")

def plan(subject, units, days, hours, exam_date):
    return generate(f"""Create a practical {days}-day study plan for B.Tech subject {subject}.
There are {units} units, {hours} hours per day, and exam date is {exam_date or 'not specified'}.
Include daily theory, practice and revision.""", "Configure OPENAI_API_KEY to generate an AI study plan.")

def mcqs(count, difficulty):
    c = context()
    result = ask(f"""Generate exactly {count} {difficulty}-difficulty MCQs from this study material.
Return valid JSON only in this format:
{{"questions":[{{"question":"...","options":["A","B","C","D"],"answer":"exact correct option","explanation":"..."}}]}}
Material:
{c}""")
    return result
