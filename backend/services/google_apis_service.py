import os
from pathlib import Path
from dotenv import load_dotenv
from services.oauth_service import OAuthService
from models import AgentRegistration
from googleapiclient.http import MediaFileUpload
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import base64
import tempfile
from datetime import datetime
import logging

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

class GoogleAPIsService:
    def __init__(self):
        self.oauth_service = OAuthService()
        self.spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
        self.drive_folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', 'joan@pymetra.com')
    
    def is_authenticated(self):
        """Check if Google APIs are authenticated"""
        return self.oauth_service.is_authenticated()
    
    async def save_to_sheets(self, registration: AgentRegistration):
        """Save registration data to Google Sheets"""
        try:
            if not self.is_authenticated():
                raise Exception("Google APIs not authenticated")
            
            sheets_service = self.oauth_service.get_service('sheets', 'v4')
            
            # Prepare data row
            values = [[
                registration.full_name,
                registration.email,
                registration.geographic_area,
                registration.main_sector,
                registration.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                registration.language.upper(),
                registration.status.title()
            ]]
            
            body = {
                'values': values
            }
            
            # Append to sheet
            result = sheets_service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range='A:G',
                valueInputOption='USER_ENTERED',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            updated_cells = result.get('updates', {}).get('updatedCells', 0)
            logger.info(f"Data saved to Google Sheets: {updated_cells} cells updated")
            
            return updated_cells > 0
            
        except Exception as e:
            logger.error(f"Error saving to Google Sheets: {str(e)}")
            return False
    
    async def upload_to_drive(self, file_content: bytes, filename: str, applicant_email: str):
        """Upload CV to Google Drive"""
        try:
            if not self.is_authenticated():
                raise Exception("Google APIs not authenticated")
            
            drive_service = self.oauth_service.get_service('drive', 'v3')
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}") as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
            
            try:
                # Prepare file metadata
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_email = applicant_email.replace("@", "_").replace(".", "_")
                drive_filename = f"{timestamp}_{safe_email}_{filename}"
                
                file_metadata = {
                    'name': drive_filename,
                    'parents': [self.drive_folder_id] if self.drive_folder_id else [],
                    'description': f'CV from {applicant_email} - {datetime.now().strftime("%d/%m/%Y %H:%M")}'
                }
                
                # Upload file
                media = MediaFileUpload(
                    temp_file_path,
                    mimetype='application/octet-stream',
                    resumable=True
                )
                
                file_result = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id,name,webViewLink'
                ).execute()
                
                logger.info(f"File uploaded to Google Drive: {file_result.get('name')}")
                
                return {
                    'file_id': file_result.get('id'),
                    'filename': file_result.get('name'),
                    'web_link': file_result.get('webViewLink')
                }
                
            finally:
                # Clean up temp file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Error uploading to Google Drive: {str(e)}")
            return None
    
    async def send_gmail_notification(self, registration: AgentRegistration, drive_file_info: dict = None):
        """Send email notification via Gmail API"""
        try:
            if not self.is_authenticated():
                raise Exception("Google APIs not authenticated")
            
            gmail_service = self.oauth_service.get_service('gmail', 'v1')
            
            # Create email message
            message = MIMEMultipart()
            message['to'] = self.recipient_email
            message['subject'] = f'Nuevo registro Pymetra - {registration.full_name}'
            
            # Email body
            body_text = f"""
Nuevo agente registrado en Pymetra:

Información del agente:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nombre: {registration.full_name}
• Email: {registration.email}
• Zona geográfica: {registration.geographic_area}
• Sector principal: {registration.main_sector}
• Idioma: {registration.language}
• Fecha de registro: {registration.timestamp.strftime('%d/%m/%Y %H:%M')}

"""
            
            if drive_file_info:
                body_text += f"""• CV en Google Drive: {drive_file_info.get('web_link', 'No disponible')}
• Nombre del archivo: {drive_file_info.get('filename', 'No disponible')}

"""
            
            body_text += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sistema de registro automático Pymetra
            """
            
            message.attach(MIMEText(body_text, 'plain', 'utf-8'))
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(
                message.as_bytes()
            ).decode('utf-8')
            
            # Send email
            send_result = gmail_service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            
            logger.info(f"Email sent via Gmail API: {send_result.get('id')}")
            
            return send_result.get('id') is not None
            
        except Exception as e:
            logger.error(f"Error sending email via Gmail API: {str(e)}")
            return False
    
    async def download_from_drive(self, file_id: str):
        """Download file from Google Drive"""
        try:
            if not self.is_authenticated():
                raise Exception("Google APIs not authenticated")
            
            drive_service = self.oauth_service.get_service('drive', 'v3')
            
            # Download file content
            request = drive_service.files().get_media(fileId=file_id)
            file_content = request.execute()
            
            logger.info(f"File downloaded from Google Drive: {file_id}")
            return file_content
            
        except Exception as e:
            logger.error(f"Error downloading from Google Drive: {str(e)}")
            return None