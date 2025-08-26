"""FastAPI application entrypoint for Eisenhower Matrix Todo API with SQLite backend."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from contextlib import asynccontextmanager

from .routers import tasks
from .database import engine
from .models.task import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup if needed


ENV = os.getenv("ENVIRONMENT", "development")
allowed_origins = ["http://localhost:3000"] if ENV == "production" else ["http://localhost:3000", "*"]

app = FastAPI(
    title="Eisenhower Matrix Todo API",
    version="1.0.0",
    description="SQLite-backed Eisenhower matrix for task prioritization and management.",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router, prefix="/api")

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Eisenhower Matrix Todo API", "version": "1.0.0", "storage": "sqlite"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"message": "Eisenhower Matrix Todo API", "version": "1.0.0", "storage": "sqlite", "status": "healthy"}
