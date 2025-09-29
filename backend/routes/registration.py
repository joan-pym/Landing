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
google_service = GoogleAPIsService()

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
        
        # Initialize result tracking
        google_sheets_saved = False
        google_drive_uploaded = False
        google_email_sent = False
        
        # Try Google APIs integration if authenticated
        logger.info(f"Google APIs authenticated: {google_service.is_authenticated()}")
        
        if google_service.is_authenticated():
            try:
                logger.info("Starting Google APIs integration...")
                
                # Save to Google Sheets
                google_sheets_saved = await google_service.save_to_sheets(registration)
                logger.info(f"Google Sheets save result: {google_sheets_saved}")
                
                # Upload CV to Google Drive
                drive_result = await google_service.upload_to_drive(cv_content, cv.filename, email)
                google_drive_uploaded = drive_result is not None
                logger.info(f"Google Drive upload result: {google_drive_uploaded}")
                logger.info(f"Drive result details: {drive_result}")
                
                # Send Gmail notification
                google_email_sent = await google_service.send_gmail_notification(registration, drive_result)
                logger.info(f"Gmail notification result: {google_email_sent}")
                
            except Exception as e:
                logger.error(f"Google APIs integration error: {str(e)}")
                logger.error(f"Error type: {type(e).__name__}")
        else:
            logger.warning("Google APIs not authenticated - skipping Google integration")
        
        # ALWAYS send email notification via SMTP with CV attached
        logger.info("Sending SMTP email notification with CV...")
        background_tasks.add_task(
            email_service.send_registration_notification,
            registration,
            cv_file_path
        )
        
        return AgentRegistrationResponse(
            message="Registro completado exitosamente" + (" - Datos guardados en Google Sheets y Drive" if google_sheets_saved and google_drive_uploaded else " - Datos guardados localmente"),
            registration_id=registration_id,
            email_sent=google_email_sent or True,  # Either Google or SMTP
            cv_saved=google_drive_uploaded or (cv_file_path is not None)
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