import React from "react";

const Header = ({ language, toggleLanguage }) => {
  return (
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
          <div>
            <img 
              src="https://customer-assets.emergentagent.com/job_sales-portal-17/artifacts/al407wc2_pymetra_balloon_200x800.png"
              alt="Pymetra"
              style={{ height: '60px', objectFit: 'contain' }}
            />
          </div>
          <div>
            <button
              onClick={toggleLanguage}
              style={{
                background: 'transparent',
                border: '2px solid var(--pymetra-dark-green)',
                borderRadius: '8px',
                padding: '8px 16px',
                fontFamily: 'Montserrat, sans-serif',
                fontWeight: '600',
                color: 'var(--pymetra-dark-green)',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.target.style.background = 'var(--pymetra-dark-green)';
                e.target.style.color = 'var(--white)';
              }}
              onMouseLeave={(e) => {
                e.target.style.background = 'transparent';
                e.target.style.color = 'var(--pymetra-dark-green)';
              }}
            >
              {language === 'es' ? 'EN' : 'ES'}
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;