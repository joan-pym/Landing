import csv
import io
from typing import List
from models import AgentRegistration
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ExportService:
    def __init__(self):
        pass
    
    def export_to_csv(self, registrations: List[AgentRegistration]) -> str:
        """Export registrations to CSV format"""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            # CSV Headers
            headers = [
                'ID',
                'Nombre Completo',
                'Email', 
                'Zona Geográfica',
                'Sector Principal',
                'Nombre CV',
                'Ruta CV',
                'Idioma',
                'Fecha Registro',
                'Estado'
            ]
            writer.writerow(headers)
            
            # Data rows
            for reg in registrations:
                writer.writerow([
                    reg.id,
                    reg.full_name,
                    reg.email,
                    reg.geographic_area,
                    reg.main_sector,
                    reg.cv_filename or '',
                    reg.cv_file_path or '',
                    reg.language,
                    reg.timestamp.strftime('%d/%m/%Y %H:%M:%S'),
                    reg.status
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            logger.info(f"Exported {len(registrations)} registrations to CSV")
            return csv_content
            
        except Exception as e:
            logger.error(f"Failed to export to CSV: {str(e)}")
            raise
    
    def export_to_google_sheets_format(self, registrations: List[AgentRegistration]) -> List[List]:
        """Export registrations in format ready for Google Sheets"""
        try:
            # Headers
            data = [[
                'Nombre Completo',
                'Email', 
                'Zona Geográfica',
                'Sector Principal',
                'Fecha Registro',
                'Idioma',
                'Estado'
            ]]
            
            # Data rows
            for reg in registrations:
                data.append([
                    reg.full_name,
                    reg.email,
                    reg.geographic_area,
                    reg.main_sector,
                    reg.timestamp.strftime('%d/%m/%Y %H:%M'),
                    reg.language.upper(),
                    reg.status.title()
                ])
            
            logger.info(f"Prepared {len(registrations)} registrations for Google Sheets")
            return data
            
        except Exception as e:
            logger.error(f"Failed to prepare Google Sheets data: {str(e)}")
            raise