import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import router  # our routes

# -------------------------
# Logging config
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# Lifespan handler
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Application startup complete.")
    yield
    # Shutdown logic
    logger.info("Application shutdown complete.")

# -------------------------
# FastAPI app setup
# -------------------------
app = FastAPI(title="Rebel Wireless", lifespan=lifespan)

# -------------------------
# CORS Middleware
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Static files
# -------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# -------------------------
# Include API routes
# -------------------------
app.include_router(router)

# -------------------------
# Healthcheck endpoint
# -------------------------
@app.get("/health")
async def healthcheck():
    return {"status": "ok"}

# -------------------------
# Run with uvicorn
# -------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
    )
