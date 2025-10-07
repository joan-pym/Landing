#!/usr/bin/env python3
"""
MIGRACIÓN INMEDIATA DE CVs A GOOGLE DRIVE
Script que ejecuta la migración directamente desde el servidor
"""

import asyncio
import sys
from pathlib import Path
import logging

# Add backend to path
backend_path = Path('/app/backend')
sys.path.append(str(backend_path))

from services.database_service import DatabaseService
from services.google_apis_service import GoogleAPIsService
from services.oauth_service import OAuthService

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def migrate_all_cvs():
    """Migrar todos los CVs locales a Google Drive AHORA"""
    logger.info("🚀 === INICIANDO MIGRACIÓN INMEDIATA DE CVs ===")
    
    try:
        # Initialize services
        logger.info("Inicializando servicios...")
        db_service = DatabaseService()
        google_service = GoogleAPIsService()
        
        # Check authentication
        logger.info("Verificando autenticación Google...")
        if not google_service.is_authenticated():
            logger.error("❌ Google APIs no autenticadas")
            logger.error("Solución: Visita https://pymetra.com/api/auth/google/login para autenticar")
            return False
        
        logger.info("✅ Google APIs autenticadas correctamente")
        
        # Get all registrations
        logger.info("Obteniendo todos los registros...")
        registrations = await db_service.get_all_registrations(limit=1000)
        logger.info(f"📊 Encontrados {len(registrations)} registros totales")
        
        # Analyze and migrate
        migrated_count = 0
        already_in_drive = 0
        no_local_file = 0
        errors = 0
        
        logger.info("🔍 === ANÁLISIS Y MIGRACIÓN ===")
        
        for i, registration in enumerate(registrations, 1):
            logger.info(f"[{i}/{len(registrations)}] Procesando: {registration.full_name}")
            
            # Check if already migrated
            if hasattr(registration, 'cv_drive_id') and registration.cv_drive_id:
                logger.info(f"  ✅ Ya en Drive: {registration.cv_drive_id}")
                already_in_drive += 1
                continue
            
            # Check if has local file
            if not (hasattr(registration, 'cv_file_path') and registration.cv_file_path):
                logger.warning(f"  ⚠️  No tiene ruta de archivo local")
                no_local_file += 1
                continue
                
            cv_path = Path(registration.cv_file_path)
            if not cv_path.exists():
                logger.warning(f"  ❌ Archivo local no existe: {cv_path}")
                no_local_file += 1
                continue
            
            # Migrate to Drive
            try:
                logger.info(f"  📤 Subiendo a Google Drive: {cv_path.name}")
                
                # Read file
                with open(cv_path, 'rb') as f:
                    cv_content = f.read()
                
                # Upload to Google Drive
                drive_result = await google_service.upload_to_drive(
                    cv_content,
                    registration.cv_filename or cv_path.name,
                    registration.email
                )
                
                if drive_result:
                    # Update database
                    await db_service.update_registration_drive_info(
                        registration.id,
                        drive_result['file_id'],
                        drive_result['web_link']
                    )
                    
                    logger.info(f"  ✅ MIGRADO: {drive_result['file_id']}")
                    logger.info(f"     Link: {drive_result['web_link']}")
                    migrated_count += 1
                else:
                    logger.error(f"  ❌ Error subiendo a Drive")
                    errors += 1
                    
            except Exception as e:
                logger.error(f"  ❌ Error procesando: {str(e)}")
                errors += 1
        
        # Final report
        logger.info("🎉 === MIGRACIÓN COMPLETADA ===")
        logger.info(f"✅ Migrados a Drive: {migrated_count}")
        logger.info(f"✅ Ya estaban en Drive: {already_in_drive}")
        logger.info(f"⚠️  Sin archivo local: {no_local_file}")
        logger.info(f"❌ Errores: {errors}")
        logger.info(f"📊 Total procesados: {len(registrations)}")
        
        if migrated_count > 0:
            logger.info(f"🎯 ¡{migrated_count} CVs migrados exitosamente a tu Google Drive!")
        
        return True
        
    except Exception as e:
        logger.error(f"💥 Error crítico en migración: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 MIGRACIÓN INMEDIATA DE CVs A GOOGLE DRIVE")
    print("=" * 50)
    
    success = asyncio.run(migrate_all_cvs())
    
    if success:
        print("\n✅ ¡Migración completada exitosamente!")
        print("👉 Verifica tu Google Drive para confirmar que los CVs están allí")
    else:
        print("\n❌ Error durante la migración")
        print("👉 Verifica la autenticación OAuth en https://pymetra.com/api/auth/google/login")