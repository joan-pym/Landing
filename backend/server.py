from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from routes.registration import router as registration_router
from routes.admin import router as admin_router
from routes.auth import router as auth_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Pymetra Registration API", version="1.0.0")

# Trust proxy headers (for proper authentication behind proxy/ingress)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(registration_router)
app.include_router(admin_router)
app.include_router(auth_router)

# Health check endpoint
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Pymetra Registration API"}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
