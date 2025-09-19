import React from "react";
import PymetraSymbol from "./PymetraSymbol";

const HeroSection = ({ language }) => {
  const content = {
    es: {
      title: "Más ventas, menos esfuerzo: conecta con PYMEs europeas.",
      subtitle: "Regístrate gratis y recibe antes que nadie nuevas oportunidades en tu zona y sector.",
      cta: "Pre-regístrate ahora"
    },
    en: {
      title: "More sales, less effort: connect with European SMEs.",
      subtitle: "Register for free and get new opportunities in your sector and region before anyone else.",
      cta: "Pre-register now"
    }
  };

  const scrollToRegistration = () => {
    document.getElementById('registration-section').scrollIntoView({ 
      behavior: 'smooth' 
    });
  };

  return (
    <section style={{ 
      background: 'var(--white)',
      padding: '100px 0',
      textAlign: 'center'
    }}>
      <div className="container">
        <div className="fade-in-up">
          <div style={{ marginBottom: '0px' }}>
            <img 
              src="https://customer-assets.emergentagent.com/job_sales-portal-17/artifacts/3njrdd7w_ChatGPT%20Image%2018%20set%202025%2C%2015_38_20.png"
              alt="Symbol Titol"
              style={{ 
              width: '206px', 
              height: '206px',
              objectFit: 'contain',
              margin: '0 auto'
            }}
          />
        </div>
          <h1 
            className="display-lg"
            style={{ 
              color: 'var(--pymetra-dark-green)',
              marginBottom: '24px',
              maxWidth: '900px',
              margin: '0 auto 24px'
            }}
          >
            {content[language].title}
          </h1>
          <p 
            className="body-lg"
            style={{ 
              marginBottom: '48px',
              maxWidth: '700px',
              margin: '0 auto 48px'
            }}
          >
            {content[language].subtitle}
          </p>
          <button 
            className="btn-primary"
            onClick={scrollToRegistration}
            style={{ fontSize: '1.125rem', padding: '20px 40px' }}
          >
            {content[language].cta}
          </button>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;