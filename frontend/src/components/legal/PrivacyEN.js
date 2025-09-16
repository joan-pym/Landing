import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const PrivacyEN = () => {
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
              Back to home
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
              Privacy Policy
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Data Controller
                </h2>
                <p className="body-md">
                  <strong>Data controller:</strong> Joan Montserrat<br/>
                  <strong>Contact:</strong> <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Purpose of Processing
                </h3>
                <p className="body-md">
                  The personal data you provide will be used to:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md">Manage your pre-registration as a sales agent on the Pymetra platform</li>
                  <li className="body-md">Send you information about collaboration opportunities with SMEs</li>
                  <li className="body-md">Contact you for selection and evaluation processes</li>
                  <li className="body-md">Maintain communication with you during the pre-launch phase</li>
                </ul>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Legal Basis
                </h3>
                <p className="body-md">
                  The processing of your data is based on your <strong>explicit consent</strong> given when completing the registration form on our website.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Recipients
                </h3>
                <p className="body-md">
                  Your data will be stored in <strong>Google Workspace</strong> (Google Sheets and Gmail) for management and processing. Google acts as a data processor under the guarantees of the General Data Protection Regulation.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Data Retention
                </h3>
                <p className="body-md">
                  We will retain your personal data during the pre-launch phase of Pymetra or as long as you maintain a business relationship with us. Once this relationship ends, the data will be deleted in accordance with applicable regulations.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Data Subject Rights
                </h3>
                <p className="body-md">
                  You have the right to:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md"><strong>Access:</strong> Obtain information about what data of yours we are processing</li>
                  <li className="body-md"><strong>Rectification:</strong> Request correction of inaccurate data</li>
                  <li className="body-md"><strong>Erasure:</strong> Request deletion of your data</li>
                  <li className="body-md"><strong>Objection:</strong> Object to the processing of your data</li>
                  <li className="body-md"><strong>Restriction:</strong> Request limitation of processing</li>
                  <li className="body-md"><strong>Data portability:</strong> Obtain your data in structured format</li>
                </ul>
                <p className="body-md" style={{ marginTop: '16px' }}>
                  To exercise these rights, you can write to us at <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Supervisory Authority
                </h3>
                <p className="body-md">
                  If you believe that the processing of your data does not comply with regulations, you can file a complaint with the <strong>Spanish Data Protection Agency</strong> (<a href="https://www.aepd.es" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--pymetra-orange)' }}>www.aepd.es</a>).
                </p>
              </div>

              <div style={{ textAlign: 'center', paddingTop: '32px', borderTop: '1px solid var(--border-light)' }}>
                <p className="body-md" style={{ color: 'var(--text-light)' }}>
                  Last updated: January 2025
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PrivacyEN;