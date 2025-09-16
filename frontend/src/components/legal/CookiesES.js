import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const CookiesES = () => {
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
              Política de Cookies
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  ¿Qué son las cookies?
                </h2>
                <p className="body-md">
                  Las cookies son pequeños archivos de texto que se almacenan en tu dispositivo cuando visitas un sitio web. Nos permiten reconocer tu navegador y capturar cierta información.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Cookies que utilizamos
                </h3>
                <p className="body-md">
                  Actualmente, este sitio web utiliza únicamente <strong>cookies técnicas esenciales</strong> que son necesarias para el funcionamiento básico del sitio web, incluyendo:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md">Cookies de sesión para mantener tu navegación</li>
                  <li className="body-md">Cookies de preferencias de idioma</li>
                  <li className="body-md">Cookies de funcionalidad básica del sitio</li>
                </ul>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Cookies de terceros
                </h3>
                <p className="body-md">
                  En la actualidad, <strong>no utilizamos cookies de analítica ni de terceros</strong> en este sitio web.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Futuras implementaciones
                </h3>
                <p className="body-md">
                  En caso de que en el futuro decidamos incorporar cookies de análisis, marketing u otras cookies no esenciales, implementaremos un banner de consentimiento conforme al <strong>Reglamento General de Protección de Datos (RGPD)</strong> y la <strong>Directiva ePrivacy</strong>.
                </p>
                <p className="body-md">
                  Te informaremos debidamente sobre el uso de estas cookies y solicitaremos tu consentimiento expreso antes de su instalación.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Gestión de cookies
                </h3>
                <p className="body-md">
                  Puedes gestionar las cookies desde la configuración de tu navegador. Ten en cuenta que deshabilitar las cookies técnicas esenciales puede afectar al funcionamiento del sitio web.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Contacto
                </h3>
                <p className="body-md">
                  Si tienes alguna pregunta sobre nuestra política de cookies, puedes contactarnos en <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
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

export default CookiesES;