# Public Deployment Guide

## 1. GitHub
Create a repository and upload this entire project. Do not upload `.env`.

## 2. Render backend
Create a new Web Service from the GitHub repository.
- Root Directory: `backend`
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/api/health`
- Environment variable: `OPENAI_API_KEY` = your secret key
- Environment variable: `OPENAI_MODEL` = `gpt-4o-mini`

The included `render.yaml` can also be used as a Blueprint.

## 3. Connect frontend
After Render deploys, copy its URL, for example `https://ai-study-assistant-api.onrender.com`.
Edit `frontend/config.js`:
`window.API_BASE = "https://YOUR-RENDER-SERVICE.onrender.com/api";`
Commit and push.

## 4. GitHub Pages
GitHub repository -> Settings -> Pages -> Source: GitHub Actions.
The included workflow publishes only the `frontend` folder.

Your URL will look like:
`https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`

## 5. Test
Open the Pages URL, upload a PDF, ask a question, then test summary and MCQs.

## Storage note
Render services normally have an ephemeral filesystem. Uploaded files, SQLite and FAISS data can disappear on restart/redeploy unless persistent storage is configured. Render documents persistent disks as a paid feature. For a college demo this is acceptable, but production should use persistent/cloud storage and a managed database/vector store.

Never put `OPENAI_API_KEY` in frontend code.
