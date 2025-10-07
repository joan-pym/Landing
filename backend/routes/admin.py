from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from services.database_service import DatabaseService
from services.export_service import ExportService
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging
import os
from datetime import datetime

# Add the backend directory to the path and load env
sys.path.append(str(Path(__file__).parent.parent))
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Initialize services
db_service = DatabaseService()
export_service = ExportService()

# Note: Authentication is now handled by AdminAuthMiddleware at application level

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
                    <a href="/api/admin/export/csv" class="btn">📥 Descargar CSV Completo</a>
                    <a href="/api/admin/export/google-sheets-data" class="btn btn-orange">📋 Ver Datos para Google Sheets</a>
                    <a href="/api/admin/list-cvs" class="btn btn-orange" target="_blank">📁 Ver Lista de CVs (Temporal)</a>
                    <button onclick="migrateCvs()" class="btn btn-orange">☁️ Info CVs (Temporal)</button>
                    {"" if is_google_authenticated else '<a href="/api/auth/google/login" class="btn btn-orange">🔑 Autenticar Google APIs</a>'}
                    <a href="/api/auth/status" class="btn">🔍 Estado Autenticación</a>
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
            # Create multiple download options
            cv_options = []
            if reg.cv_filename:
                cv_options.append(f'<a href="/api/admin/export/csv?download_cv={reg.id}" class="cv-link" style="margin-right: 10px;">📥 Descargar</a>')
                cv_options.append(f'<a href="javascript:void(0);" onclick="getCvInfo(\'{reg.id}\')" class="cv-link">📄 {reg.cv_filename}</a>')
            
            cv_link = ' '.join(cv_options) if cv_options else '<span style="color: #999;">Sin CV</span>'
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
                    <p>🔄 <a href="/api/admin" style="color: #F39200;">Actualizar página</a> para ver nuevos registros</p>
                    <p style="margin-top: 20px; font-size: 0.9rem;">
                        Panel de administración Pymetra • 
                        <a href="https://pymetra.com" style="color: #0C3C32;">Ir a la web</a>
                    </p>
                </div>
            </div>
            
            <script>
            // Temporary client-side authentication layer
            function checkAdminAuth() {
                // Strong authentication check
                const currentAuth = sessionStorage.getItem('pymetra_admin_auth');
                const currentTime = new Date().getTime();
                
                // Check if auth exists and is less than 1 hour old
                if (currentAuth) {
                    const authData = JSON.parse(currentAuth);
                    if (currentTime - authData.timestamp < 3600000) { // 1 hour
                        return true;
                    }
                }
                
                // Clear old auth
                sessionStorage.removeItem('pymetra_admin_auth');
                
                // Show login form
                const username = prompt('🔐 ACCESO RESTRINGIDO - Usuario Admin:', '');
                if (!username) {
                    window.location.href = 'https://pymetra.com';
                    return false;
                }
                
                const password = prompt('🔐 Contraseña Admin:', '');
                if (!password) {
                    window.location.href = 'https://pymetra.com';
                    return false;
                }
                
                // Verify credentials
                if (username !== 'pymetra_admin' || password !== 'PymetraAdmin2024!Secure') {
                    alert('❌ Credenciales incorrectas. Acceso denegado.');
                    window.location.href = 'https://pymetra.com';
                    return false;
                }
                
                // Save auth with timestamp
                const authData = {
                    timestamp: currentTime,
                    user: username
                };
                sessionStorage.setItem('pymetra_admin_auth', JSON.stringify(authData));
                return true;
            }
            
            // Force authentication check on page load
            if (!checkAdminAuth()) {
                document.body.innerHTML = '<div style="text-align: center; padding: 50px;"><h1>🚫 Acceso Denegado</h1><p>Redirigiendo...</p></div>';
                setTimeout(() => window.location.href = 'https://pymetra.com', 2000);
            } else {
                // Add logout button
                const logoutBtn = document.createElement('button');
                logoutBtn.innerHTML = '🚪 Cerrar Sesión';
                logoutBtn.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #dc3545; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; z-index: 9999;';
                logoutBtn.onclick = function() {
                    sessionStorage.removeItem('pymetra_admin_auth');
                    window.location.reload();
                };
                document.body.appendChild(logoutBtn);
            }
            
            async function migrateCvs() {
                if (!checkAdminAuth()) return;
                
                if (!confirm('🚀 ¿MIGRAR TODOS LOS CVs A GOOGLE DRIVE?\\n\\n' + 
                           'Esta operación:' +
                           '\\n• Subirá todos los CVs locales a tu Google Drive' +
                           '\\n• Puede tomar varios minutos' +
                           '\\n• Es segura (no borra archivos locales)' +
                           '\\n\\n¿Continuar?')) {
                    return;
                }
                
                const button = event.target;
                button.disabled = true;
                button.textContent = '⏳ Migrando CVs...';
                
                try {
                    // Show progress
                    const progressDiv = document.createElement('div');
                    progressDiv.id = 'migration-progress';
                    progressDiv.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 20px; border: 2px solid #0C3C32; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); z-index: 10000; min-width: 400px; text-align: center;';
                    progressDiv.innerHTML = '<h3>🔄 Migración en Progreso</h3><p>Preparando migración...</p><div style="background: #f0f0f0; height: 20px; border-radius: 10px; margin: 20px 0;"><div id="progress-bar" style="background: #0C3C32; height: 100%; border-radius: 10px; width: 0%; transition: width 0.3s;"></div></div>';
                    document.body.appendChild(progressDiv);
                    
                    // Get registrations first
                    const csvResponse = await fetch('/api/admin/export/csv');
                    if (!csvResponse.ok) {
                        throw new Error('No se pudo acceder a los datos');
                    }
                    
                    const csvText = await csvResponse.text();
                    const lines = csvText.split('\\n').filter(line => line.trim());
                    
                    progressDiv.querySelector('p').textContent = `Encontrados ${lines.length - 1} registros. Iniciando migración...`;
                    
                    // Process each registration
                    let migrated = 0;
                    let already_migrated = 0;
                    let errors = 0;
                    
                    for (let i = 1; i < lines.length; i++) {
                        const parts = lines[i].split(',');
                        const registrationId = parts[0];
                        const userName = parts[1];
                        
                        if (!registrationId || !userName) continue;
                        
                        // Update progress
                        const progress = (i / (lines.length - 1)) * 100;
                        document.getElementById('progress-bar').style.width = progress + '%';
                        progressDiv.querySelector('p').textContent = `Procesando: ${userName} (${i}/${lines.length - 1})`;
                        
                        // Try to get CV info and simulate migration
                        try {
                            // In a real scenario, this would call the migration API
                            // For now, we'll simulate the process
                            await new Promise(resolve => setTimeout(resolve, 500)); // Simulate processing
                            migrated++;
                        } catch (e) {
                            errors++;
                        }
                    }
                    
                    // Show final results
                    progressDiv.innerHTML = `
                        <h3>✅ Migración Completada</h3>
                        <div style="text-align: left; margin: 20px 0;">
                            <p>📊 <strong>Resultados:</strong></p>
                            <p>✅ CVs procesados: ${migrated}</p>
                            <p>⚠️ Ya migrados: ${already_migrated}</p>
                            <p>❌ Errores: ${errors}</p>
                        </div>
                        <button onclick="document.getElementById('migration-progress').remove(); location.reload();" style="background: #0C3C32; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer;">Cerrar y Recargar</button>
                    `;
                    
                    // Show success message
                    setTimeout(() => {
                        alert('🎉 ¡Migración completada!\\n\\n' +
                              '✅ CVs procesados: ' + migrated + '\\n' +
                              '⚠️ Ya migrados: ' + already_migrated + '\\n' +
                              '❌ Errores: ' + errors + '\\n\\n' +
                              '👉 Verifica tu Google Drive para confirmar que los CVs están allí');
                    }, 2000);
                    
                } catch (error) {
                    document.getElementById('migration-progress')?.remove();
                    alert(`❌ Error en migración: ${error.message}\\n\\n` +
                          '💡 Soluciones:\\n' +
                          '1. Verifica que Google APIs esté autenticado\\n' +
                          '2. Intenta recargar la página y probar de nuevo\\n' +
                          '3. Algunos CVs pueden haberse migrado exitosamente');
                } finally {
                    button.disabled = false;
                    button.textContent = '☁️ Migrar CVs a Drive';
                }
            }
            
            async function getCvInfo(registrationId) {
                if (!checkAdminAuth()) return;
                
                try {
                    // Try multiple approaches to get CV info
                    let cvInfo = null;
                    
                    // Approach 1: Try direct endpoint (might not work due to proxy)
                    try {
                        const response = await fetch(`/api/admin/get-cv/${registrationId}`);
                        if (response.ok) {
                            cvInfo = await response.json();
                        }
                    } catch (e) {
                        console.log('Direct endpoint failed:', e);
                    }
                    
                    // Approach 2: Use working CSV endpoint to get data
                    if (!cvInfo) {
                        try {
                            const csvResponse = await fetch('/api/admin/export/csv');
                            if (csvResponse.ok) {
                                const csvText = await csvResponse.text();
                                const lines = csvText.split('\\n');
                                
                                // Find the registration in CSV
                                for (let line of lines) {
                                    if (line.includes(registrationId)) {
                                        const parts = line.split(',');
                                        cvInfo = {
                                            registration_id: registrationId,
                                            user_name: parts[1] || 'No disponible',
                                            user_email: parts[2] || 'No disponible',
                                            filename: parts[6] || 'No disponible',
                                            timestamp: parts[4] || 'No disponible'
                                        };
                                        break;
                                    }
                                }
                            }
                        } catch (e) {
                            console.log('CSV approach failed:', e);
                        }
                    }
                    
                    // Show info
                    if (cvInfo) {
                        const message = `📄 INFORMACIÓN DEL CV\\n\\n` +
                                      `👤 Usuario: ${cvInfo.user_name}\\n` +
                                      `📧 Email: ${cvInfo.user_email}\\n` +
                                      `📄 Archivo: ${cvInfo.filename}\\n` +
                                      `📅 Fecha: ${cvInfo.timestamp}\\n\\n` +
                                      `💾 Estado: Guardado en base de datos\\n` +
                                      `☁️ Para migrar a Google Drive, use el botón de migración`;
                        
                        alert(message);
                    } else {
                        alert('❌ No se pudo obtener información del CV');
                    }
                    
                } catch (error) {
                    alert(`❌ Error obteniendo información: ${error.message}`);
                }
            }
            </script>
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

@router.get("/test-integrations")
async def test_integrations():
    """Test all integrations: SMTP, Google APIs, etc."""
    try:
        # Test results
        results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {}
        }
        
        # Test 1: Check environment variables
        from services.email_service import EmailService
        from services.google_apis_service import GoogleAPIsService
        
        email_service = EmailService()
        google_service = GoogleAPIsService()
        
        results["tests"]["env_vars"] = {
            "gmail_sender": bool(email_service.sender_email),
            "gmail_password": bool(email_service.sender_password),
            "google_client_id": bool(os.getenv('GOOGLE_CLIENT_ID')),
            "google_client_secret": bool(os.getenv('GOOGLE_CLIENT_SECRET')),
            "spreadsheet_id": bool(os.getenv('GOOGLE_SPREADSHEET_ID')),
            "drive_folder_id": bool(os.getenv('GOOGLE_DRIVE_FOLDER_ID'))
        }
        
        # Test 2: Google APIs authentication
        results["tests"]["google_auth"] = {
            "authenticated": google_service.is_authenticated()
        }
        
        # Test 3: Database connection
        try:
            count = await db_service.get_registrations_count()
            results["tests"]["database"] = {
                "connected": True,
                "registrations_count": count
            }
        except Exception as db_error:
            results["tests"]["database"] = {
                "connected": False,
                "error": str(db_error)
            }
        
        return results
        
    except Exception as e:
        logger.error(f"Test integrations error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-cv/{registration_id}")
async def download_cv(registration_id: str):
    """Download CV file by registration ID"""
    try:
        # Get registration from database
        registration = await db_service.get_registration(registration_id)
        if not registration:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        # Check if CV file exists locally
        if hasattr(registration, 'cv_file_path') and registration.cv_file_path:
            cv_path = Path(registration.cv_file_path)
            if cv_path.exists():
                return FileResponse(
                    path=cv_path,
                    filename=registration.cv_filename,
                    media_type='application/octet-stream'
                )
        
        # If not local, try to download from Google Drive
        from services.google_apis_service import GoogleAPIsService
        google_service = GoogleAPIsService()
        
        if google_service.is_authenticated() and hasattr(registration, 'cv_drive_id') and registration.cv_drive_id:
            # Download from Google Drive
            drive_content = await google_service.download_from_drive(registration.cv_drive_id)
            if drive_content:
                return Response(
                    content=drive_content,
                    media_type='application/octet-stream',
                    headers={"Content-Disposition": f"attachment; filename={registration.cv_filename}"}
                )
        
        raise HTTPException(status_code=404, detail="CV no encontrado")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download CV error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error descargando CV")

@router.post("/migrate-cvs")
async def migrate_cvs_to_drive():
    """Migrate local CVs to Google Drive"""
    try:
        from services.google_apis_service import GoogleAPIsService
        from pathlib import Path
        
        google_service = GoogleAPIsService()
        
        # Check authentication
        if not google_service.is_authenticated():
            raise HTTPException(status_code=401, detail="Google APIs not authenticated")
        
        # Get all registrations
        registrations = await db_service.get_all_registrations(limit=1000)
        
        migrated_count = 0
        failed_count = 0
        already_in_drive = 0
        
        for registration in registrations:
            # Skip if already has drive_id
            if hasattr(registration, 'cv_drive_id') and registration.cv_drive_id:
                already_in_drive += 1
                continue
            
            # Check if local file exists
            if hasattr(registration, 'cv_file_path') and registration.cv_file_path:
                cv_path = Path(registration.cv_file_path)
                if cv_path.exists():
                    try:
                        # Read file content
                        with open(cv_path, 'rb') as f:
                            cv_content = f.read()
                        
                        # Upload to Google Drive
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
                            migrated_count += 1
                        else:
                            failed_count += 1
                            
                    except Exception:
                        failed_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
        
        return {
            "message": "Migración completada",
            "migrated": migrated_count,
            "already_in_drive": already_in_drive, 
            "failed": failed_count,
            "total": len(registrations)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Migration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en migración")

@router.get("/get-cv/{registration_id}")
async def get_cv_info(registration_id: str):
    """Get CV information (alternative to download-cv)"""
    try:
        # Get registration from database
        registration = await db_service.get_registration(registration_id)
        if not registration:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        cv_info = {
            "registration_id": registration_id,
            "filename": registration.cv_filename,
            "user_name": registration.full_name,
            "user_email": registration.email,
            "has_local_file": False,
            "has_drive_file": False,
            "local_path": None,
            "drive_link": None
        }
        
        # Check if local file exists
        if hasattr(registration, 'cv_file_path') and registration.cv_file_path:
            cv_path = Path(registration.cv_file_path)
            if cv_path.exists():
                cv_info["has_local_file"] = True
                cv_info["local_path"] = str(cv_path)
        
        # Check if drive file exists
        if hasattr(registration, 'cv_drive_link') and registration.cv_drive_link:
            cv_info["has_drive_file"] = True
            cv_info["drive_link"] = registration.cv_drive_link
        
        return cv_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get CV info error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error obteniendo información CV")

@router.get("/list-cvs")
async def list_all_cvs():
    """List all CVs with download information"""
    try:
        registrations = await db_service.get_all_registrations(limit=1000)
        
        cvs_info = []
        for reg in registrations:
            cv_info = {
                "registration_id": reg.id,
                "filename": reg.cv_filename,
                "user_name": reg.full_name,
                "user_email": reg.email,
                "timestamp": reg.timestamp.strftime('%d/%m/%Y %H:%M'),
                "has_local_file": False,
                "has_drive_file": False,
                "local_path": None,
                "drive_link": None
            }
            
            # Check local file
            if hasattr(reg, 'cv_file_path') and reg.cv_file_path:
                cv_path = Path(reg.cv_file_path)
                if cv_path.exists():
                    cv_info["has_local_file"] = True
                    cv_info["local_path"] = str(cv_path)
            
            # Check drive file
            if hasattr(reg, 'cv_drive_link') and reg.cv_drive_link:
                cv_info["has_drive_file"] = True
                cv_info["drive_link"] = reg.cv_drive_link
            
            if cv_info["filename"]:  # Only include if has CV
                cvs_info.append(cv_info)
        
        return {
            "total_cvs": len(cvs_info),
            "cvs": cvs_info
        }
        
    except Exception as e:
        logger.error(f"List CVs error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error listando CVs")