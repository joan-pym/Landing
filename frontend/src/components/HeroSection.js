import React from "react";

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
            <PymetraSymbol size={120} />
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