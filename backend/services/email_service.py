import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('GMAIL_SENDER_EMAIL')
        self.sender_password = os.getenv('GMAIL_APP_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'joan@pymetra.com')
        
    async def send_registration_notification(self, registration_data, cv_file_path: Optional[str] = None):
        try:
            # Create message
            message = MIMEMultipart()
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = f'Nuevo registro - {registration_data.full_name}'
            
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
            
            # Attach CV if exists
            if cv_file_path and os.path.exists(cv_file_path):
                with open(cv_file_path, 'rb') as f:
                    attachment = MIMEApplication(f.read())
                    attachment.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(cv_file_path)}"'
                    )
                    message.attach(attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            logger.info(f"Email sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False