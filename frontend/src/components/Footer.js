import React from "react";
import { Link } from "react-router-dom";

const Footer = ({ language }) => {
  const content = {
    es: {
      links: {
        legal: "Aviso legal",
        privacy: "Política de privacidad",
        cookies: "Política de cookies"
      },
      copyright: "© 2025 Pymetra. Todos los derechos reservados."
    },
    en: {
      links: {
        legal: "Legal Notice",
        privacy: "Privacy Policy",
        cookies: "Cookies Policy"
      },
      copyright: "© 2025 Pymetra. All rights reserved."
    }
  };

  const getLinkPath = (type) => {
    const paths = {
      legal: language === 'es' ? '/es/aviso-legal' : '/en/legal-notice',
      privacy: language === 'es' ? '/es/privacidad' : '/en/privacy',
      cookies: language === 'es' ? '/es/cookies' : '/en/cookies'
    };
    return paths[type];
  };

  return (
    <footer style={{ 
      background: 'var(--pymetra-light-gray)',
      padding: '60px 0 30px',
      borderTop: '1px solid var(--border-light)'
    }}>
      <div className="container">
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '40px',
          marginBottom: '40px'
        }}>
          {/* Logo and Contact */}
          <div>
            <img 
              src="https://customer-assets.emergentagent.com/job_cd4bdb57-a937-4f3c-8471-d99cd1e3f0ea/artifacts/2qfih5n9_Pymetra_logo_sinfondo_2.PNG"
              alt="Pymetra"
              style={{ height: '45px', marginBottom: '20px' }}
            />
            <p className="body-md" style={{ marginBottom: '16px' }}>
              {language === 'es' 
                ? 'Conectando PYMEs con agentes comerciales en toda Europa.'
                : 'Connecting SMEs with sales agents across Europe.'
              }
            </p>
            <p className="body-md" style={{ fontWeight: '500' }}>
              <a 
                href="mailto:info@pymetra.com"
                style={{ 
                  color: 'var(--pymetra-dark-green)',
                  textDecoration: 'none'
                }}
              >
                info@pymetra.com
              </a>
            </p>
          </div>

          {/* Legal Links */}
          <div>
            <h4 
              className="h3" 
              style={{ 
                color: 'var(--pymetra-dark-green)',
                marginBottom: '20px'
              }}
            >
              {language === 'es' ? 'Legal' : 'Legal'}
            </h4>
            <nav style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <Link 
                to={getLinkPath('legal')}
                style={{ 
                  color: 'var(--text-light)',
                  textDecoration: 'none',
                  transition: 'color 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.color = 'var(--pymetra-orange)'}
                onMouseLeave={(e) => e.target.style.color = 'var(--text-light)'}
              >
                {content[language].links.legal}
              </Link>
              <Link 
                to={getLinkPath('privacy')}
                style={{ 
                  color: 'var(--text-light)',
                  textDecoration: 'none',
                  transition: 'color 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.color = 'var(--pymetra-orange)'}
                onMouseLeave={(e) => e.target.style.color = 'var(--text-light)'}
              >
                {content[language].links.privacy}
              </Link>
              <Link 
                to={getLinkPath('cookies')}
                style={{ 
                  color: 'var(--text-light)',
                  textDecoration: 'none',
                  transition: 'color 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.color = 'var(--pymetra-orange)'}
                onMouseLeave={(e) => e.target.style.color = 'var(--text-light)'}
              >
                {content[language].links.cookies}
              </Link>
            </nav>
          </div>
        </div>

        {/* Copyright */}
        <div style={{
          borderTop: '1px solid var(--border-light)',
          paddingTop: '30px',
          textAlign: 'center'
        }}>
          <p className="body-md" style={{ color: 'var(--text-light)' }}>
            {content[language].copyright}
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;