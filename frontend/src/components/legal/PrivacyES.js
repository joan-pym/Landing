import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const PrivacyES = () => {
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
              Política de Privacidad
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Responsable del Tratamiento
                </h2>
                <p className="body-md">
                  <strong>Responsable:</strong> Joan Montserrat<br/>
                  <strong>Contacto:</strong> <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Finalidad del Tratamiento
                </h3>
                <p className="body-md">
                  Los datos personales que nos proporciones serán utilizados para:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md">Gestionar tu pre-registro como agente comercial en la plataforma Pymetra</li>
                  <li className="body-md">Enviarte información sobre oportunidades de colaboración con PYMEs</li>
                  <li className="body-md">Contactarte para procesos de selección y evaluación</li>
                  <li className="body-md">Mantener comunicación contigo durante la fase de prelanzamiento</li>
                </ul>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Legitimación
                </h3>
                <p className="body-md">
                  El tratamiento de tus datos se basa en tu <strong>consentimiento expreso</strong> otorgado al completar el formulario de registro en nuestro sitio web.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Destinatarios
                </h3>
                <p className="body-md">
                  Tus datos serán almacenados en <strong>Google Workspace</strong> (Google Sheets y Gmail) para su gestión y procesamiento. Google actúa como encargado de tratamiento bajo las garantías del Reglamento General de Protección de Datos.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Conservación de los Datos
                </h3>
                <p className="body-md">
                  Conservaremos tus datos personales mientras dure la fase de prelanzamiento de Pymetra o mientras mantengas una relación comercial con nosotros. Una vez finalizada esta relación, los datos serán eliminados conforme a la normativa aplicable.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Derechos del Interesado
                </h3>
                <p className="body-md">
                  Tienes derecho a:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md"><strong>Acceso:</strong> Obtener información sobre qué datos tuyos estamos tratando</li>
                  <li className="body-md"><strong>Rectificación:</strong> Solicitar la corrección de datos inexactos</li>
                  <li className="body-md"><strong>Supresión:</strong> Solicitar la eliminación de tus datos</li>
                  <li className="body-md"><strong>Oposición:</strong> Oponerte al tratamiento de tus datos</li>
                  <li className="body-md"><strong>Limitación:</strong> Solicitar la limitación del tratamiento</li>
                  <li className="body-md"><strong>Portabilidad:</strong> Obtener tus datos en formato estructurado</li>
                </ul>
                <p className="body-md" style={{ marginTop: '16px' }}>
                  Para ejercer estos derechos, puedes escribirnos a <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Reclamaciones
                </h3>
                <p className="body-md">
                  Si consideras que el tratamiento de tus datos no se ajusta a la normativa, puedes presentar una reclamación ante la <strong>Agencia Española de Protección de Datos</strong> (<a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--pymetra-orange)' }}>www.aepd.es</a>).
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

export default PrivacyES;