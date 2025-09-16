import React from "react";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const CookiesEN = () => {
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
              Cookies Policy
            </h1>

            <div className="card" style={{ lineHeight: '1.8' }}>
              <div style={{ marginBottom: '32px' }}>
                <h2 className="h2" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  What are cookies?
                </h2>
                <p className="body-md">
                  Cookies are small text files that are stored on your device when you visit a website. They allow us to recognize your browser and capture certain information.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Cookies we use
                </h3>
                <p className="body-md">
                  Currently, this website only uses <strong>essential technical cookies</strong> that are necessary for the basic functioning of the website, including:
                </p>
                <ul style={{ marginLeft: '24px', marginTop: '12px' }}>
                  <li className="body-md">Session cookies to maintain your navigation</li>
                  <li className="body-md">Language preference cookies</li>
                  <li className="body-md">Basic site functionality cookies</li>
                </ul>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Third-party cookies
                </h3>
                <p className="body-md">
                  Currently, we <strong>do not use analytics or third-party cookies</strong> on this website.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Future implementations
                </h3>
                <p className="body-md">
                  If in the future we decide to incorporate analytics, marketing, or other non-essential cookies, we will implement a consent banner compliant with the <strong>General Data Protection Regulation (GDPR)</strong> and the <strong>ePrivacy Directive</strong>.
                </p>
                <p className="body-md">
                  We will properly inform you about the use of these cookies and request your explicit consent before their installation.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Cookie management
                </h3>
                <p className="body-md">
                  You can manage cookies from your browser settings. Please note that disabling essential technical cookies may affect the website's functionality.
                </p>
              </div>

              <div style={{ marginBottom: '32px' }}>
                <h3 className="h3" style={{ color: 'var(--pymetra-dark-green)', marginBottom: '16px' }}>
                  Contact
                </h3>
                <p className="body-md">
                  If you have any questions about our cookies policy, you can contact us at <a href="mailto:info@pymetra.com" style={{ color: 'var(--pymetra-orange)' }}>info@pymetra.com</a>
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

export default CookiesEN;