from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse
from services.database_service import DatabaseService
from services.export_service import ExportService
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add the backend directory to the path and load env
sys.path.append(str(Path(__file__).parent.parent))
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

# Initialize services
db_service = DatabaseService()
export_service = ExportService()

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """Simple admin dashboard"""
    try:
        count = await db_service.get_registrations_count()
        registrations = await db_service.get_all_registrations(limit=10)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pymetra Admin - Registrations</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #0C3C32; margin-bottom: 30px; }}
                .stats {{ background: #F39200; color: white; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
                .export-buttons {{ margin-bottom: 30px; }}
                .btn {{ background: #0C3C32; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin-right: 10px; display: inline-block; }}
                .btn:hover {{ background: #1a5d4f; }}
                .btn-orange {{ background: #F39200; }}
                .btn-orange:hover {{ background: #e08600; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; font-weight: bold; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .timestamp {{ font-size: 0.9em; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Pymetra Admin - Panel de Registros</h1>
                
                <div class="stats">
                    <h2>📊 Estadísticas</h2>
                    <p><strong>Total de registros:</strong> {count}</p>
                </div>
                
                <div class="export-buttons">
                    <h3>📥 Exportar Datos</h3>
                    <a href="/admin/export/csv" class="btn">Descargar CSV</a>
                    <a href="/admin/export/google-sheets-data" class="btn btn-orange">Ver datos para Google Sheets</a>
                </div>
                
                <h3>📋 Últimos Registros</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Nombre</th>
                            <th>Email</th>
                            <th>Zona</th>
                            <th>Sector</th>
                            <th>Fecha</th>
                            <th>CV</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for reg in registrations:
            cv_link = f'<a href="/admin/download-cv/{reg.id}">📄 {reg.cv_filename}</a>' if reg.cv_filename else 'No CV'
            html_content += f"""
                        <tr>
                            <td><strong>{reg.full_name}</strong></td>
                            <td>{reg.email}</td>
                            <td>{reg.geographic_area}</td>
                            <td>{reg.main_sector}</td>
                            <td class="timestamp">{reg.timestamp.strftime('%d/%m/%Y %H:%M')}</td>
                            <td>{cv_link}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
                
                <div style="margin-top: 40px; text-align: center; color: #666;">
                    <p>🔄 Actualiza la página para ver nuevos registros</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
        
    except Exception as e:
        logger.error(f"Admin dashboard error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error loading dashboard")

@router.get("/export/csv")
async def export_csv():
    """Export all registrations to CSV"""
    try:
        registrations = await db_service.get_all_registrations(limit=1000)
        csv_content = export_service.export_to_csv(registrations)
        
        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=pymetra_registrations.csv"}
        )
        
    except Exception as e:
        logger.error(f"CSV export error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error exporting CSV")

@router.get("/export/google-sheets-data")
async def export_google_sheets_data():
    """Get data in format ready for Google Sheets"""
    try:
        registrations = await db_service.get_all_registrations(limit=1000)
        sheets_data = export_service.export_to_google_sheets_format(registrations)
        
        return {
            "total_records": len(registrations),
            "headers": sheets_data[0],
            "data": sheets_data[1:] if len(sheets_data) > 1 else [],
            "instructions": [
                "1. Copia los datos de la sección 'data'",
                "2. Ve a Google Sheets",
                "3. Crea nueva hoja o selecciona existente", 
                "4. Pega los datos",
                "5. Formato automático se aplicará"
            ]
        }
        
    except Exception as e:
        logger.error(f"Google Sheets export error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error preparing Google Sheets data")