# Pymetra Landing Page - Contratos de Integración

## Estado Actual: FRONTEND COMPLETO CON MOCK DATA

### ✅ Funcionalidades Implementadas
- Landing page bilingüe (ES/EN) completamente funcional
- Formulario de registro con validación
- Páginas legales en ambos idiomas
- Diseño responsive siguiendo guidelines de Pymetra
- Navegación fluida entre secciones

### 🔄 Datos Mock Actuales
**Formulario de Registro:** Los datos se almacenan temporalmente en el estado del componente y se muestran en alert. Los siguientes campos se capturan:
- `fullName`: Nombre completo
- `email`: Email del agente
- `geographicArea`: Zona geográfica
- `mainSector`: Sector principal (dropdown con opciones)
- `cv`: Archivo CV (PDF/DOC)

### 🚀 Integraciones Futuras Requeridas

#### 1. Google Sheets Integration
**Endpoint:** `POST /api/register-agent`
**Datos a enviar:**
```json
{
  "fullName": "string",
  "email": "string", 
  "geographicArea": "string",
  "mainSector": "string",
  "timestamp": "ISO datetime",
  "language": "es|en"
}
```
**Destino:** Google Sheets con columnas correspondientes

#### 2. Gmail API Integration  
**Funcionalidad:** Envío automático de CV a info@pymetra.com
**Trigger:** Al completar registro
**Email contenido:**
- Asunto: "Nuevo agente registrado - [Nombre]"
- Cuerpo: Datos del agente + CV adjunto
- Destino: info@pymetra.com

#### 3. Google Drive Storage
**Funcionalidad:** Almacenamiento seguro de CVs
**Estructura de archivos:** `/pymetra-cvs/YYYY/MM/[timestamp]_[nombre]_cv.[ext]`

### 📋 Implementación Backend Requerida

#### Modelos de Datos
```python
class AgentRegistration(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: str
    geographic_area: str
    main_sector: str
    cv_filename: str
    cv_drive_id: str
    language: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "pending"
```

#### Endpoints Requeridos
```python
@api_router.post("/register-agent")
async def register_agent(
    background_tasks: BackgroundTasks,
    full_name: str = Form(...),
    email: str = Form(...),
    geographic_area: str = Form(...),
    main_sector: str = Form(...),
    language: str = Form(...),
    cv: UploadFile = File(...)
):
    # 1. Validar datos
    # 2. Subir CV a Google Drive  
    # 3. Guardar datos en Google Sheets
    # 4. Enviar email con CV a info@pymetra.com
    # 5. Retornar confirmación
```

### 🔐 Credenciales Necesarias (Para Implementación Futura)
- Google Service Account JSON
- Google Sheets ID
- Google Drive Folder ID
- Gmail API credentials

### 📱 Frontend Integración
**Archivo:** `/app/frontend/src/components/RegistrationSection.js`
**Cambio requerido:** Reemplazar mock `handleSubmit` con llamada real a `/api/register-agent`

### 🌐 URLs y Rutas
- Landing page: `/` 
- Legal ES: `/es/aviso-legal`, `/es/privacidad`, `/es/cookies`
- Legal EN: `/en/legal-notice`, `/en/privacy`, `/en/cookies`

### 🎨 Diseño Completado
- Colores Pymetra: Orange #F39200, Dark green #0C3C32, Light gray #F8F8F8
- Tipografía: Montserrat
- Diseño responsive y accesible
- Animaciones y micro-interacciones implementadas

---

**Nota:** La aplicación está lista para producción con funcionalidad mock. Las integraciones reales se pueden implementar cuando las credenciales estén disponibles sin afectar el frontend existente.