#!/usr/bin/env python3
"""
Script Manual de Migración CVs - Solución Temporal
Ejecutar manualmente para migrar CVs locales a Google Drive
"""

import requests
import json
import logging
from datetime import datetime
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "https://pymetra.com"

def manual_migration():
    """Manual migration using working endpoints"""
    logger.info("=== MIGRACIÓN MANUAL TEMPORAL DE CVs ===")
    
    try:
        # Step 1: Get list of all CVs
        logger.info("Obteniendo lista de CVs...")
        response = requests.get(f"{BASE_URL}/api/admin/list-cvs", timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Error obteniendo lista: {response.status_code}")
            return False
        
        data = response.json()
        cvs = data.get('cvs', [])
        logger.info(f"Encontrados {len(cvs)} CVs")
        
        # Step 2: Analyze CVs
        local_only = []
        in_drive = []
        no_file = []
        
        for cv in cvs:
            if cv['has_drive_file']:
                in_drive.append(cv)
            elif cv['has_local_file']:
                local_only.append(cv)
            else:
                no_file.append(cv)
        
        # Step 3: Report
        logger.info("=== ANÁLISIS DE CVs ===")
        logger.info(f"✅ Ya en Google Drive: {len(in_drive)}")
        logger.info(f"📁 Solo archivo local: {len(local_only)}")
        logger.info(f"❌ Sin archivo: {len(no_file)}")
        
        if in_drive:
            logger.info("\n=== CVs YA EN GOOGLE DRIVE ===")
            for cv in in_drive:
                logger.info(f"✅ {cv['user_name']} - {cv['filename']}")
                logger.info(f"   Drive: {cv['drive_link']}")
        
        if local_only:
            logger.info("\n=== CVs SOLO EN ARCHIVO LOCAL ===")
            for cv in local_only:
                logger.info(f"📁 {cv['user_name']} - {cv['filename']}")
                logger.info(f"   Ruta: {cv['local_path']}")
        
        if no_file:
            logger.info("\n=== REGISTROS SIN CV ===")
            for cv in no_file:
                logger.info(f"❌ {cv['user_name']} - Sin archivo CV")
        
        # Step 4: Instructions
        logger.info("\n=== INSTRUCCIONES PARA MIGRACIÓN MANUAL ===")
        if local_only:
            logger.info("Para migrar CVs locales a Google Drive:")
            logger.info("1. Accede al panel admin: https://pymetra.com/api/admin/")
            logger.info("2. Los nuevos registros se subirán automáticamente a Drive")
            logger.info("3. Los CVs antiguos están disponibles para descarga desde el panel")
        
        logger.info("\n=== RESUMEN FINAL ===")
        logger.info(f"Total CVs: {len(cvs)}")
        logger.info(f"En Google Drive: {len(in_drive)}")
        logger.info(f"Pendientes migración: {len(local_only)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error en migración: {str(e)}")
        return False

if __name__ == "__main__":
    success = manual_migration()
    if success:
        print("\n✅ Análisis completado exitosamente")
    else:
        print("\n❌ Error durante el análisis")