import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const LegalNoticeES = () => {
  return (
    <div style={{ background: 'var(--white)', minHeight: '100vh' }}>
      {/* Header */}
      <header style={{ 
        background: 'var(--white)', 
        padding: '20px 0',
        borderBottom: '1px solid var(--border-light)'
      }}>
        <div className="container">
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center' 
          }}>
            <Link to="/">
              <img 
                src="https://customer-assets.emergentagent.com/job_cd4bdb57-a937-4f3c-8471-d99cd1e3f0ea/artifacts/2qfih5n9_Pymetra_logo_sinfondo_2.PNG"
                alt="Pymetra"
                style={{ height: '50px' }}
              />
            </Link>
            <Link 
              to="/"
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                color: 'var(--pymetra-dark-green)',
                textDecoration: 'none',
                fontWeight: '500'
              }}
            >
              <ArrowLeft size={20} />
              Volver al inicio
            </Link>
          </div>
        </div>
      </header>

      {/* Content */}
      <main style={{ padding: '80px 0' }}>
        <div className="container">
          <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <h1 
              className="display-md"
              style={{ 
                color: 'var(--pymetra-dark-green)',
                marginBottom: '40px',
                textAlign: 'center'
              }}
            >
              Aviso Legal
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Información General
                </h2>
                <p className="body-md">
                  El presente sitio web es propiedad de <strong>Joan Montserrat</strong>, en adelante <strong>Pymetra</strong>.
                </p>
                <p className="body-md">
                  <strong>Correo electrónico:</strong> <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Objeto del Sitio Web
                </h3>
                <p className="body-md">
                  El sitio tiene como finalidad facilitar un canal de contacto y registro de agentes comerciales interesados en colaborar con PYMEs europeas a través de la plataforma Pymetra.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Propiedad Intelectual
                </h3>
                <p className="body-md">
                  Todos los elementos contenidos en este sitio web, incluyendo pero no limitándose a textos, imágenes, logotipos, iconos, software, y cualquier otro material, son propiedad de Pymetra o de sus autores legítimos y están protegidos por las leyes de propiedad intelectual e industrial aplicables.
                </p>
                <p className="body-md">
                  Queda prohibida la reproducción, distribución, comunicación pública o transformación de dichos contenidos sin la autorización expresa de sus titulares.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Limitación de Responsabilidad
                </h3>
                <p className="body-md">
                  Pymetra no garantiza la disponibilidad continua del sitio web, aunque trabajará para asegurar su correcto funcionamiento. No se hace responsable de los daños que puedan derivarse del uso o la imposibilidad de uso del sitio web.
                </p>
                <p className="body-md">
                  Pymetra se reserva el derecho de modificar, suspender o dar de baja el sitio web sin previo aviso.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Ley Aplicable y Jurisdicción
                </h3>
                <p className="body-md">
                  Estas condiciones se rigen por la legislación española. Para la resolución de cualquier conflicto derivado del uso de este sitio web, las partes se someten a la jurisdicción de los tribunales españoles.
                </p>
              </div>

              <div style={{ textAlign: 'center', paddingTop: '32px', borderTop: '1px solid var(--border-light)' }}>
                <p className="body-md" style={{ color: 'var(--text-light)' }}>
                  Última actualización: Enero 2025
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LegalNoticeES;