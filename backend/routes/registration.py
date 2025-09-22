from fastapi import APIRouter, File, UploadFile, Form, HTTPException, BackgroundTasks
from pydantic import EmailStr
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import logging

# Add the backend directory to the path and load env
sys.path.append(str(Path(__file__).parent.parent))
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

from models import AgentRegistration, AgentRegistrationResponse
from services.database_service import DatabaseService
from services.file_service import FileService
from services.email_service import EmailService
from services.google_apis_service import GoogleAPIsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["registration"])

# Initialize services
db_service = DatabaseService()
file_service = FileService()
email_service = EmailService()

@router.post("/register-agent", response_model=AgentRegistrationResponse)
async def register_agent(
    background_tasks: BackgroundTasks,
    fullName: str = Form(...),
    email: EmailStr = Form(...),
    geographicArea: str = Form(...),
    mainSector: str = Form(...),
    language: str = Form(default="es"),
    cv: UploadFile = File(...)
):
    try:
        # Validate file type
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if cv.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail="Tipo de archivo no válido. Solo se permiten PDF, DOC, DOCX"
            )
            
        # Validate file size (5MB limit)
        cv_content = await cv.read()
        if len(cv_content) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="El archivo es demasiado grande. Máximo 5MB"
            )
        
        # Create registration object
        registration = AgentRegistration(
            full_name=fullName,
            email=email,
            geographic_area=geographicArea,
            main_sector=mainSector,
            language=language,
            cv_filename=cv.filename
        )
        
        # Save CV file
        cv_file_path = await file_service.save_cv_file(cv_content, cv.filename, email)
        if cv_file_path:
            registration.cv_file_path = cv_file_path
        
        # Save to database
        registration_id = await db_service.save_registration(registration)
        
        # Send email notification in background
        background_tasks.add_task(
            email_service.send_registration_notification,
            registration,
            cv_file_path
        )
        
        return AgentRegistrationResponse(
            message="Registro completado exitosamente",
            registration_id=registration_id,
            email_sent=True,
            cv_saved=cv_file_path is not None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/registrations/count")
async def get_registrations_count():
    count = await db_service.get_registrations_count()
    return {"total_registrations": count}

@router.get("/registrations")
async def get_registrations(limit: int = 50):
    registrations = await db_service.get_all_registrations(limit)
    return {"registrations": registrations}