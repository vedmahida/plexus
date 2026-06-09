"""
FastAPI orchestration service — main entry point.
Handles research requests, routes to multi-agent graph, returns typed responses.
Production-grade: structured logging, retries, health checks, async throughout.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

##### Configure structured logging #####
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

##### FastAPI lifecycle hooks #####
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle hooks."""
    logger.info("Plexus Orchestrator starting up")
    yield
    logger.info("Plexus Orchestrator shutting down")

##### FastAPI app #####
app = FastAPI(
    title="Plexus Orchestrator",
    description="Multi-agent clinical research assistant 🧪🦠",
    version="1.0.0",
    lifespan=lifespan
)

##### CORS middleware for frontend integration #####
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://medresearch.internal"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def health():
    """Standard health check"""
    return {"service": "orchestrator", "status": "healthy"}


