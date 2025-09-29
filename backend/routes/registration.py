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
    logger.info(f"=== REGISTRATION START ===")
    logger.info(f"User: {fullName} ({email})")
    logger.info(f"File: {cv.filename} ({cv.content_type})")
    
    try:
        # Validate file type
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]
        
        if cv.content_type not in allowed_types:
            logger.error(f"Invalid file type: {cv.content_type}")
            raise HTTPException(
                status_code=400, 
                detail="Tipo de archivo no válido. Solo se permiten PDF, DOC, DOCX"
            )
            
        # Validate file size (5MB limit)
        cv_content = await cv.read()
        logger.info(f"CV size: {len(cv_content)} bytes")
        
        if len(cv_content) > 5 * 1024 * 1024:
            logger.error(f"File too large: {len(cv_content)} bytes")
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
        logger.info(f"Registration object created: {registration.id}")
        
        # Save CV file locally
        cv_file_path = await file_service.save_cv_file(cv_content, cv.filename, email)
        logger.info(f"CV saved locally: {cv_file_path}")
        
        if cv_file_path:
            registration.cv_file_path = cv_file_path
        
        # Save to database
        registration_id = await db_service.save_registration(registration)
        logger.info(f"Saved to MongoDB: {registration_id}")
        
        # Initialize result tracking
        google_sheets_saved = False
        google_drive_uploaded = False
        google_email_sent = False
        smtp_email_sent = False
        
        # Check Google APIs authentication
        is_google_authenticated = google_service.is_authenticated()
        logger.info(f"Google APIs authenticated: {is_google_authenticated}")
        
        if is_google_authenticated:
            logger.info("=== STARTING GOOGLE APIS INTEGRATION ===")
            
            try:
                # Test 1: Save to Google Sheets
                logger.info("Attempting Google Sheets save...")
                google_sheets_saved = await google_service.save_to_sheets(registration)
                logger.info(f"Google Sheets result: {google_sheets_saved}")
                
                # Test 2: Upload CV to Google Drive
                logger.info("Attempting Google Drive upload...")
                drive_result = await google_service.upload_to_drive(cv_content, cv.filename, email)
                google_drive_uploaded = drive_result is not None
                logger.info(f"Google Drive result: {drive_result}")
                
                # Test 3: Send Gmail notification
                logger.info("Attempting Gmail API notification...")
                google_email_sent = await google_service.send_gmail_notification(registration, drive_result)
                logger.info(f"Gmail API result: {google_email_sent}")
                
                logger.info("=== GOOGLE APIS INTEGRATION COMPLETE ===")
                
            except Exception as google_error:
                logger.error(f"=== GOOGLE APIs ERROR ===")
                logger.error(f"Error type: {type(google_error).__name__}")
                logger.error(f"Error message: {str(google_error)}")
                logger.error(f"Error details: {repr(google_error)}")
        else:
            logger.warning("Google APIs not authenticated - skipping Google integration")
        
        # ALWAYS attempt SMTP email as backup
        logger.info("=== STARTING SMTP EMAIL BACKUP ===")
        try:
            # Send email synchronously for debugging
            smtp_result = await email_service.send_registration_notification(registration, cv_file_path)
            smtp_email_sent = smtp_result
            logger.info(f"SMTP email result: {smtp_email_sent}")
        except Exception as smtp_error:
            logger.error(f"=== SMTP EMAIL ERROR ===")
            logger.error(f"SMTP Error type: {type(smtp_error).__name__}")
            logger.error(f"SMTP Error message: {str(smtp_error)}")
            logger.error(f"SMTP Error details: {repr(smtp_error)}")
        
        # Final status
        logger.info("=== REGISTRATION COMPLETE ===")
        logger.info(f"Google Sheets: {google_sheets_saved}")
        logger.info(f"Google Drive: {google_drive_uploaded}")
        logger.info(f"Gmail API: {google_email_sent}")
        logger.info(f"SMTP Email: {smtp_email_sent}")
        
        # Determine message
        if google_sheets_saved and google_drive_uploaded:
            message = "Registro completado - Datos en Google Sheets y Drive"
        elif smtp_email_sent:
            message = "Registro completado - Revisa tu email para los datos"
        else:
            message = "Registro completado - Datos guardados localmente"
        
        return AgentRegistrationResponse(
            message=message,
            registration_id=registration_id,
            email_sent=google_email_sent or smtp_email_sent,
            cv_saved=google_drive_uploaded or (cv_file_path is not None)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"=== CRITICAL REGISTRATION ERROR ===")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Type: {type(e).__name__}")
        logger.error(f"Details: {repr(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/registrations/count")
async def get_registrations_count():
    count = await db_service.get_registrations_count()
    return {"total_registrations": count}

@router.get("/registrations")
async def get_registrations(limit: int = 50):
    registrations = await db_service.get_all_registrations(limit)
    return {"registrations": registrations}