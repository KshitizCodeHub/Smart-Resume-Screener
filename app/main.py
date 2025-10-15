"""
FastAPI application entry point for Smart Resume Screener.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database.mongodb import MongoDB
from app.api.routes import router

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print("🚀 Starting Smart Resume Screener...")
    await MongoDB.connect_db()
    print("✅ Application ready!")
    
    yield
    
    # Shutdown
    print("🔌 Shutting down...")
    await MongoDB.close_db()
    print("👋 Goodbye!")

# Create FastAPI app
app = FastAPI(
    title="Smart Resume Screener API",
    description="Intelligent resume parsing and job matching system using LLMs",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

# Root endpoint
@app.get("/api")
async def root():
    """API root endpoint."""
    return {
        "message": "Welcome to Smart Resume Screener API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
