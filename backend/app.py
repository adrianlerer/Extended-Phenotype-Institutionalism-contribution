"""
FastAPI Backend for Legal Evolution Research Suite
Provides API endpoints for paper building, CLI calculations, and AI assistance
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from pathlib import Path

from routes import paper_builder, cli_calculator, figure_generator, ai_assistant
from services.monitoring import IntelligentMonitor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Legal Evolution Research API",
    description="AI-powered research infrastructure for constitutional law analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize monitoring
monitor = IntelligentMonitor()

# Include routers
app.include_router(paper_builder.router, prefix="/api/papers", tags=["Papers"])
app.include_router(cli_calculator.router, prefix="/api/cli", tags=["CLI Calculator"])
app.include_router(figure_generator.router, prefix="/api/figures", tags=["Figures"])
app.include_router(ai_assistant.router, prefix="/api/chat", tags=["AI Assistant"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Legal Evolution Research API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": monitor.get_timestamp(),
        "uptime": monitor.get_uptime()
    }


@app.get("/api/status")
async def system_status():
    """Get system status and metrics"""
    return {
        "status": "operational",
        "metrics": monitor.get_metrics(),
        "recent_builds": monitor.get_recent_builds(),
        "recent_errors": monitor.get_recent_errors()
    }


@app.post("/api/webhook/genspark")
async def genspark_webhook(request: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Webhook endpoint for Genspark integration
    Allows Genspark to receive analysis requests and send back responses
    """
    action = request.get("action")
    
    if action == "review_code":
        # Queue code review task
        background_tasks.add_task(
            monitor.queue_code_review,
            file_path=request.get("file"),
            content=request.get("content")
        )
        return {"status": "queued", "action": "review_code"}
    
    elif action == "analyze_error":
        # Queue error analysis task
        background_tasks.add_task(
            monitor.queue_error_analysis,
            error_log=request.get("log")
        )
        return {"status": "queued", "action": "analyze_error"}
    
    elif action == "query_docs":
        # Queue documentation query
        background_tasks.add_task(
            monitor.queue_doc_query,
            question=request.get("question")
        )
        return {"status": "queued", "action": "query_docs"}
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action: {action}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler with AI analysis"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Queue error for AI analysis
    monitor.queue_error_analysis(str(exc))
    
    return {
        "error": str(exc),
        "message": "An error occurred. AI analysis has been queued.",
        "request_path": str(request.url)
    }


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
