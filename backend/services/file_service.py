import os
import aiofiles
from pathlib import Path
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.upload_dir = Path("uploads/cvs")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
    async def save_cv_file(self, file_content: bytes, filename: str, applicant_email: str) -> Optional[str]:
        try:
            # Create safe filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_email = applicant_email.replace("@", "_").replace(".", "_")
            file_extension = Path(filename).suffix
            safe_filename = f"{timestamp}_{safe_email}_cv{file_extension}"
            
            file_path = self.upload_dir / safe_filename
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_content)
                
            logger.info(f"CV file saved: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Failed to save CV file: {str(e)}")
            return None
            
    def get_cv_file_info(self, file_path: str) -> dict:
        try:
            path = Path(file_path)
            if path.exists():
                return {
                    "filename": path.name,
                    "size": path.stat().st_size,
                    "created": datetime.fromtimestamp(path.stat().st_ctime)
                }
        except Exception as e:
            logger.error(f"Failed to get file info: {str(e)}")
        return {}