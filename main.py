import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from src.config import Settings
from src.handlers.pr_handler import PRAnalyzerHandler
from src.models.webhook_models import ADOWebhookPayload
from src.services.cosmos_service import CosmosService

app = FastAPI(title="Azure DevOps PR Analyzer Agent")

# Initialize settings and services
# Note: In a production app, you might use dependency injection
settings = Settings()
cosmos_service = CosmosService()
handler = PRAnalyzerHandler(settings, cosmos_service)

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/api/status")
async def get_status():
    return {
        "status": "online",
        "activity": [
            {"timestamp": "Just now", "type": "SYSTEM", "message": "Listening for Azure webhooks...", "status": "success"},
        ]
    }

@app.post("/webhook/pr")
async def handle_pr_webhook(payload: ADOWebhookPayload, background_tasks: BackgroundTasks):
    """
    Endpoint for Azure DevOps Webhooks (git.pullrequest.created, git.pullrequest.updated)
    """
    try:
        # Run the analysis in the background to avoid webhook timeouts
        background_tasks.add_task(handler.handle, payload)
        return {"status": "accepted", "message": "PR analysis started in background"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run server locally
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
