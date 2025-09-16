import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const LegalNoticeEN = () => {
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
              Legal Notice
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  General Information
                </h2>
                <p className="body-md">
                  This website is owned by <strong>Joan Montserrat</strong>, hereinafter <strong>Pymetra</strong>.
                </p>
                <p className="body-md">
                  <strong>Contact email:</strong> <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Purpose of the Website
                </h3>
                <p className="body-md">
                  The purpose of the site is to provide a channel for sales agents to register and express interest in future collaboration opportunities with European SMEs through the Pymetra platform.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Intellectual Property
                </h3>
                <p className="body-md">
                  All elements contained on this website, including but not limited to texts, images, logos, icons, software, and any other material, belong to Pymetra or their legitimate authors and are protected by applicable intellectual and industrial property laws.
                </p>
                <p className="body-md">
                  Reproduction, distribution, public communication, or transformation of such content is prohibited without the express authorization of their owners.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Disclaimer
                </h3>
                <p className="body-md">
                  Pymetra does not guarantee the continuous availability of the website, though best efforts will be made to ensure proper functioning. We are not responsible for damages that may arise from the use or inability to use the website.
                </p>
                <p className="body-md">
                  Pymetra reserves the right to modify, suspend, or discontinue the website without prior notice.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Applicable Law and Jurisdiction
                </h3>
                <p className="body-md">
                  These conditions are governed by Spanish legislation. For the resolution of any conflict arising from the use of this website, the parties submit to the jurisdiction of Spanish courts.
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

export default LegalNoticeEN;