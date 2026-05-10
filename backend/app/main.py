"""
Main FastAPI application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.api import api_router

# ============================================
# CREATE FASTAPI APPLICATION
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    description="College ERP System API",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS CONFIGURATION
# ============================================

# Frontend URLs
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
]

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# TRUSTED HOST MIDDLEWARE
# ============================================

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

# ============================================
# ROUTES
# ============================================

# Include API routers
app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "http://localhost:8000/docs",
        "redoc": "http://localhost:8000/redoc"
    }

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "status": "error"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "status": "error"
        }
    )

# ============================================
# STARTUP & SHUTDOWN EVENTS
# ============================================

@app.on_event("startup")
async def startup_event():
    """Run on startup"""
    print(f"[START] {settings.APP_NAME} v{settings.APP_VERSION} started")
    print("[DOCS] http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on shutdown"""
    print(f"[STOP] {settings.APP_NAME} shut down")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )