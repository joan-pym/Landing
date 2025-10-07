#!/usr/bin/env python3
"""
Script para migrar CVs antiguos a Google Drive
Pymetra - Migración de archivos locales
"""

import asyncio
import sys
from pathlib import Path
import logging

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from services.database_service import DatabaseService
from services.google_apis_service import GoogleAPIsService
from services.file_service import FileService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def migrate_cvs_to_drive():
    """Migrate local CVs to Google Drive and update database"""
    logger.info("=== INICIANDO MIGRACIÓN DE CVs A GOOGLE DRIVE ===")
    
    # Initialize services
    db_service = DatabaseService()
    google_service = GoogleAPIsService()
    file_service = FileService()
    
    # Check Google authentication
    if not google_service.is_authenticated():
        logger.error("❌ Google APIs not authenticated. Cannot migrate.")
        return False
    
    logger.info("✅ Google APIs authenticated")
    
    try:
        # Get all registrations
        registrations = await db_service.get_all_registrations(limit=1000)
        logger.info(f"📋 Found {len(registrations)} registrations")
        
        migrated_count = 0
        failed_count = 0
        already_in_drive = 0
        
        for registration in registrations:
            logger.info(f"🔍 Processing: {registration.full_name} ({registration.email})")
            
            # Skip if already has drive_id
            if hasattr(registration, 'cv_drive_id') and registration.cv_drive_id:
                logger.info(f"  ✅ Already in Drive: {registration.cv_drive_id}")
                already_in_drive += 1
                continue
            
            # Check if local file exists
            if hasattr(registration, 'cv_file_path') and registration.cv_file_path:
                cv_path = Path(registration.cv_file_path)
                if cv_path.exists():
                    logger.info(f"  📄 Found local CV: {cv_path}")
                    
                    try:
                        # Read file content
                        with open(cv_path, 'rb') as f:
                            cv_content = f.read()
                        
                        # Upload to Google Drive
                        logger.info(f"  ☁️  Uploading to Google Drive...")
                        drive_result = await google_service.upload_to_drive(
                            cv_content, 
                            registration.cv_filename, 
                            registration.email
                        )
                        
                        if drive_result:
                            # Update registration with drive info
                            await db_service.update_registration_drive_info(
                                registration.id,
                                drive_result['file_id'],
                                drive_result['web_link']
                            )
                            
                            logger.info(f"  ✅ Migrated successfully: {drive_result['file_id']}")
                            migrated_count += 1
                        else:
                            logger.error(f"  ❌ Failed to upload to Drive")
                            failed_count += 1
                            
                    except Exception as e:
                        logger.error(f"  ❌ Error processing CV: {str(e)}")
                        failed_count += 1
                else:
                    logger.warning(f"  ⚠️  Local CV not found: {cv_path}")
                    failed_count += 1
            else:
                logger.warning(f"  ⚠️  No CV file path for registration")
                failed_count += 1
        
        # Summary
        logger.info("=== MIGRACIÓN COMPLETADA ===")
        logger.info(f"✅ Migrated successfully: {migrated_count}")
        logger.info(f"✅ Already in Drive: {already_in_drive}")
        logger.info(f"❌ Failed migrations: {failed_count}")
        logger.info(f"📊 Total processed: {len(registrations)}")
        
        return migrated_count > 0
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        return False

async def main():
    """Main migration function"""
    logger.info("🚀 Starting CV migration to Google Drive...")
    success = await migrate_cvs_to_drive()
    
    if success:
        logger.info("🎉 Migration completed successfully!")
    else:
        logger.error("💥 Migration failed!")
    
    return success

if __name__ == "__main__":
    asyncio.run(main())