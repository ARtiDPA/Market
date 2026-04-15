"""Main FastAPI application."""
from fastapi import FastAPI

app = FastAPI(
    title="Market API",
    description="Modular marketplace application",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Market API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
