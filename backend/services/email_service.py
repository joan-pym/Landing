import smtplib
import os
from pathlib import Path
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional
import logging

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('GMAIL_SENDER_EMAIL')
        self.sender_password = os.getenv('GMAIL_APP_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'joan@pymetra.com')
        
    async def send_registration_notification(self, registration_data, cv_file_path: Optional[str] = None):
        logger.info(f"=== SMTP EMAIL SERVICE START ===")
        logger.info(f"Sender: {self.sender_email}")
        logger.info(f"Recipient: {self.recipient_email}")
        logger.info(f"CV file: {cv_file_path}")
        logger.info(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
        
        try:
            # Verify credentials
            if not self.sender_email or not self.sender_password:
                logger.error("SMTP credentials missing")
                logger.error(f"Sender email: {self.sender_email}")
                logger.error(f"Password exists: {bool(self.sender_password)}")
                return False
            
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = f'Nuevo registro Pymetra - {registration_data.full_name}'
            
            # Email body in Spanish
            body = f"""
Nuevo agente registrado en Pymetra:

Información del agente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nombre: {registration_data.full_name}
• Email: {registration_data.email}
• Zona geográfica: {registration_data.geographic_area}
• Sector principal: {registration_data.main_sector}
• Idioma: {registration_data.language}
• Fecha de registro: {registration_data.timestamp.strftime('%d/%m/%Y %H:%M')}

El CV se encuentra adjunto a este correo.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sistema de registro automático Pymetra
            """
            
            message.attach(MIMEText(body, 'plain', 'utf-8'))
            logger.info("Email body attached")
            
            # Attach CV if exists
            if cv_file_path and os.path.exists(cv_file_path):
                logger.info(f"Attaching CV: {cv_file_path}")
                with open(cv_file_path, 'rb') as f:
                    attachment = MIMEApplication(f.read())
                    attachment.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(cv_file_path)}"'
                    )
                    message.attach(attachment)
                logger.info("CV attachment added")
            else:
                logger.warning(f"CV file not found: {cv_file_path}")
            
            # Send email
            logger.info("Connecting to SMTP server...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                logger.info("Starting TLS...")
                server.starttls()
                
                logger.info("Logging in to SMTP...")
                server.login(self.sender_email, self.sender_password)
                
                logger.info("Sending message...")
                server.send_message(message)
                
            logger.info(f"✅ Email sent successfully to {self.recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError as auth_error:
            logger.error(f"❌ SMTP Authentication failed: {str(auth_error)}")
            logger.error("Check Gmail App Password configuration")
            return False
        except smtplib.SMTPException as smtp_error:
            logger.error(f"❌ SMTP Error: {str(smtp_error)}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected email error: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            return False