import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from routes import router as api_router

app = FastAPI(
    title="LinkAI API",
    version="0.1.0",
    description="AI‑powered semantic search and summarisation for research teams",
)

# Include API router under /api
app.include_router(api_router, prefix="/api")

@app.get("/health", response_model=dict)
def health_check():
    """Simple health check endpoint"""
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def root():
    html = """
    <html>
    <head>
        <title>LinkAI – AI‑powered research assistant</title>
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: Arial, Helvetica, sans-serif; padding: 2rem; }
            a { color: #58a6ff; }
            h1 { color: #58a6ff; }
            table { width: 100%%; border-collapse: collapse; margin-top: 1rem; }
            th, td { padding: 0.5rem; border: 1px solid #30363d; text-align: left; }
            th { background-color: #161b22; }
        </style>
    </head>
    <body>
        <h1>LinkAI</h1>
        <p>AI‑powered semantic search for research teams: organise, connect, and collaborate on web knowledge.</p>
        <h2>Available API Endpoints</h2>
        <table>
            <tr><th>Method</th><th>Path</th><th>Purpose</th></tr>
            <tr><td>GET</td><td>/health</td><td>Health check</td></tr>
            <tr><td>POST</td><td>/api/summaries</td><td>Generate academic‑style summary with citations</td></tr>
            <tr><td>POST</td><td>/api/semantic-tags</td><td>Extract domain‑specific tags & relationships</td></tr>
            <tr><td>POST</td><td>/api/search</td><td>Semantic search via natural language query</td></tr>
        </table>
        <p>Tech stack: Next.js 15 • FastAPI 0.115 • PostgreSQL • DigitalOcean Serverless Inference (openai‑gpt‑oss‑120b)</p>
        <p>Docs: <a href="/docs">Swagger UI</a> | <a href="/redoc">ReDoc</a></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html, status_code=200)
