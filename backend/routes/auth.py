from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from services.oauth_service import OAuthService
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add the backend directory to the path and load env
sys.path.append(str(Path(__file__).parent.parent))
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

oauth_service = OAuthService()

@router.get("/google/login")
async def google_login():
    """Initiate Google OAuth flow with automatic redirect"""
    try:
        authorization_url, state = oauth_service.get_authorization_url()
        
        # Return HTML page that redirects automatically
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pymetra - Redirigiendo a Google...</title>
            <meta charset="utf-8">
            <meta http-equiv="refresh" content="0; url={authorization_url}">
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; background: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 50px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .loading {{ color: #0C3C32; font-size: 18px; margin-bottom: 20px; }}
                .spinner {{ border: 4px solid #f3f3f3; border-top: 4px solid #F39200; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }}
                @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
                .manual-link {{ color: #F39200; text-decoration: none; font-weight: bold; }}
                .manual-link:hover {{ color: #e08600; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="loading">🔐 Conectando con Google...</h1>
                <div class="spinner"></div>
                <p>Serás redirigido automáticamente a Google para autenticarte.</p>
                <p>Si no te redirige automáticamente, <a href="{authorization_url}" class="manual-link">haz clic aquí</a></p>
            </div>
            
            <script>
                // Fallback JavaScript redirect
                setTimeout(function() {{
                    window.location.href = "{authorization_url}";
                }}, 2000);
            </script>
        </body>
        </html>
        """)
        
    except Exception as e:
        logger.error(f"Error initiating OAuth: {str(e)}")
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Pymetra OAuth</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1 class="error">❌ Error de Configuración OAuth</h1>
            <p>Error: {str(e)}</p>
            <p><a href="/admin">Volver al Panel Admin</a></p>
        </body>
        </html>
        """, status_code=500)

@router.get("/google/callback")
async def google_callback(
    code: str = Query(...),
    state: str = Query(...),
    error: str = Query(None)
):
    """Handle Google OAuth callback"""
    try:
        if error:
            raise HTTPException(status_code=400, detail=f"OAuth error: {error}")
        
        # Exchange code for credentials
        credentials = oauth_service.exchange_code_for_credentials(code, state)
        
        # Return success page
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pymetra - Autenticación Exitosa</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin: 50px; background: #f5f5f5; }
                .container { max-width: 600px; margin: 0 auto; background: white; padding: 50px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                .success { color: #0C3C32; font-size: 24px; margin-bottom: 20px; }
                .btn { background: #F39200; color: white; padding: 15px 30px; text-decoration: none; border-radius: 6px; font-weight: bold; }
                .btn:hover { background: #e08600; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">✅ Autenticación Exitosa</h1>
                <p>Google APIs configuradas correctamente para Pymetra.</p>
                <p>Ahora puedes usar:</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>Google Sheets - Guardar registros automáticamente</li>
                    <li>Google Drive - Almacenar CVs</li>
                    <li>Gmail API - Enviar notificaciones</li>
                </ul>
                <br><br>
                <a href="/api/admin" class="btn">Ir al Panel Admin</a>
                <a href="http://localhost:3000" class="btn" style="margin-left: 10px;">Ir a la Web</a>
            </div>
        </body>
        </html>
        """)
        
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error de Autenticación</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin: 50px; }}
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1 class="error">❌ Error de Autenticación</h1>
            <p>Error: {str(e)}</p>
            <a href="/auth/google/login">Intentar de nuevo</a>
        </body>
        </html>
        """, status_code=500)

@router.get("/status")
async def auth_status():
    """Check authentication status"""
    try:
        is_authenticated = oauth_service.is_authenticated()
        
        return {
            "authenticated": is_authenticated,
            "message": "Google APIs authenticated" if is_authenticated else "Not authenticated",
            "login_url": "/auth/google/login" if not is_authenticated else None
        }
        
    except Exception as e:
        logger.error(f"Error checking auth status: {str(e)}")
        return {
            "authenticated": False,
            "error": str(e),
            "login_url": "/auth/google/login"
        }