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

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Initialize services
db_service = DatabaseService()
export_service = ExportService()

@router.get("/", response_class=HTMLResponse)
async def admin_dashboard():
    """Enhanced admin dashboard with Google APIs integration"""
    try:
        count = await db_service.get_registrations_count()
        registrations = await db_service.get_all_registrations(limit=20)
        
        # Check Google APIs authentication status
        from services.google_apis_service import GoogleAPIsService
        google_service = GoogleAPIsService()
        is_google_authenticated = google_service.is_authenticated()
        
        auth_status_html = ""
        if is_google_authenticated:
            auth_status_html = """
            <div style="background: #d4edda; color: #155724; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                ✅ <strong>Google APIs Autenticadas</strong> - Sheets, Drive, Gmail funcionando
            </div>
            """
        else:
            auth_status_html = """
            <div style="background: #f8d7da; color: #721c24; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                ❌ <strong>Google APIs No Autenticadas</strong> 
                <br><a href="/auth/google/login" style="color: #721c24; font-weight: bold;">Hacer clic aquí para autenticar</a>
            </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pymetra Admin - Panel de Control</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; background: #f8f9fa; }}
                .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; }}
                .header {{ background: linear-gradient(135deg, #0C3C32, #1a5d4f); color: white; padding: 40px; border-radius: 12px; margin-bottom: 30px; text-align: center; }}
                .header h1 {{ margin: 0; font-size: 2.5rem; font-weight: 700; }}
                .header p {{ margin: 10px 0 0; opacity: 0.9; font-size: 1.1rem; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .stat-card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); text-align: center; }}
                .stat-number {{ font-size: 3rem; font-weight: 700; color: #F39200; margin-bottom: 10px; }}
                .stat-label {{ color: #666; font-size: 1.1rem; }}
                .actions {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.08); margin-bottom: 30px; }}
                .btn {{ background: #0C3C32; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; margin-right: 15px; margin-bottom: 10px; display: inline-block; font-weight: 600; transition: all 0.3s; }}
                .btn:hover {{ background: #1a5d4f; transform: translateY(-2px); }}
                .btn-orange {{ background: #F39200; }}
                .btn-orange:hover {{ background: #e08600; }}
                .btn-danger {{ background: #dc3545; }}
                .btn-danger:hover {{ background: #c82333; }}
                .table-container {{ background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.08); }}
                table {{ width: 100%; border-collapse: collapse; }}
                th {{ background: #f8f9fa; padding: 20px; text-align: left; font-weight: 600; border-bottom: 2px solid #dee2e6; }}
                td {{ padding: 15px 20px; border-bottom: 1px solid #dee2e6; }}
                tr:hover {{ background: #f8f9fa; }}
                .timestamp {{ font-size: 0.9em; color: #666; }}
                .cv-link {{ color: #F39200; text-decoration: none; font-weight: 500; }}
                .cv-link:hover {{ color: #e08600; }}
                .status {{ padding: 6px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }}
                .status-pending {{ background: #fff3cd; color: #856404; }}
                .status-active {{ background: #d4edda; color: #155724; }}
                @media (max-width: 768px) {{
                    .container {{ padding: 15px; }}
                    .header {{ padding: 20px; }}
                    .header h1 {{ font-size: 2rem; }}
                    .stats-grid {{ grid-template-columns: 1fr; }}
                    .btn {{ display: block; margin-bottom: 10px; text-align: center; }}
                    table, thead, tbody, th, td, tr {{ display: block; }}
                    thead tr {{ position: absolute; top: -9999px; left: -9999px; }}
                    tr {{ border: 1px solid #ccc; margin-bottom: 10px; padding: 10px; }}
                    td {{ border: none; position: relative; padding-left: 30%; }}
                    td:before {{ content: attr(data-label) ": "; position: absolute; left: 6px; width: 25%; text-align: right; font-weight: bold; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Pymetra - Panel de Administración</h1>
                    <p>Control total de registros y datos de agentes</p>
                </div>
                
                {auth_status_html}
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{count}</div>
                        <div class="stat-label">Registros Totales</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{"✅" if is_google_authenticated else "❌"}</div>
                        <div class="stat-label">Google APIs</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">🌐</div>
                        <div class="stat-label">Sistema Activo</div>
                    </div>
                </div>
                
                <div class="actions">
                    <h3 style="margin-top: 0; color: #0C3C32;">📊 Exportar y Gestionar Datos</h3>
                    <a href="/admin/export/csv" class="btn">📥 Descargar CSV Completo</a>
                    <a href="/admin/export/google-sheets-data" class="btn btn-orange">📋 Ver Datos para Google Sheets</a>
                    {"" if is_google_authenticated else '<a href="/auth/google/login" class="btn btn-orange">🔑 Autenticar Google APIs</a>'}
                    <a href="/auth/status" class="btn">🔍 Estado Autenticación</a>
                </div>
                
                <div class="table-container">
                    <h3 style="margin: 20px; color: #0C3C32;">📋 Últimos Registros</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Agente</th>
                                <th>Contacto</th>
                                <th>Ubicación</th>
                                <th>Sector</th>
                                <th>Fecha Registro</th>
                                <th>CV</th>
                                <th>Estado</th>
                            </tr>
                        </thead>
                        <tbody>
        """
        
        for reg in registrations:
            cv_link = f'<a href="/admin/download-cv/{reg.id}" class="cv-link">📄 {reg.cv_filename}</a>' if reg.cv_filename else '<span style="color: #999;">Sin CV</span>'
            status_class = "status-active" if reg.status == "active" else "status-pending"
            
            html_content += f"""
                            <tr>
                                <td data-label="Agente"><strong>{reg.full_name}</strong></td>
                                <td data-label="Contacto">{reg.email}</td>
                                <td data-label="Ubicación">{reg.geographic_area}</td>
                                <td data-label="Sector">{reg.main_sector}</td>
                                <td data-label="Fecha" class="timestamp">{reg.timestamp.strftime('%d/%m/%Y %H:%M')}</td>
                                <td data-label="CV">{cv_link}</td>
                                <td data-label="Estado"><span class="status {status_class}">{reg.status.title()}</span></td>
                            </tr>
            """
        
        html_content += """
                        </tbody>
                    </table>
                </div>
                
                <div style="margin-top: 40px; text-align: center; color: #666;">
                    <p>🔄 <a href="/admin" style="color: #F39200;">Actualizar página</a> para ver nuevos registros</p>
                    <p style="margin-top: 20px; font-size: 0.9rem;">
                        Panel de administración Pymetra • 
                        <a href="https://pymetra.com" style="color: #0C3C32;">Ir a la web</a>
                    </p>
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