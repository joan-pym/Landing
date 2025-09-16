import React from "react";

const FinalCTASection = ({ language }) => {
  const content = {
    es: {
      title: "Empieza hoy a recibir oportunidades",
      subtitle: "No pierdas más tiempo buscando clientes. Deja que ellos te encuentren.",
      cta: "Quiero registrarme gratis"
    },
    en: {
      title: "Start receiving opportunities today",
      subtitle: "Stop wasting time looking for clients. Let them find you.",
      cta: "Register for free"
    }
  };

  const scrollToRegistration = () => {
    document.getElementById('registration-section').scrollIntoView({ 
      behavior: 'smooth' 
    });
  };

  return (
    <section style={{ 
      background: 'var(--pymetra-dark-green)',
      padding: '100px 0',
      textAlign: 'center'
    }}>
      <div className="container">
        <div className="fade-in-up">
          <h2 
            className="display-md"
            style={{ 
              color: 'var(--white)',
              marginBottom: '24px',
              maxWidth: '800px',
              margin: '0 auto 24px'
            }}
          >
            {content[language].title}
          </h2>
          <p 
            className="body-lg"
            style={{ 
              color: 'rgba(255, 255, 255, 0.9)',
              marginBottom: '48px',
              maxWidth: '600px',
              margin: '0 auto 48px'
            }}
          >
            {content[language].subtitle}
          </p>
          <button 
            className="btn-primary"
            onClick={scrollToRegistration}
            style={{ 
              fontSize: '1.125rem', 
              padding: '20px 40px',
              background: 'var(--pymetra-orange)',
              boxShadow: '0 8px 32px rgba(243, 146, 0, 0.3)'
            }}
          >
            {content[language].cta}
          </button>
        </div>
      </div>
    </section>
  );
};

export default FinalCTASection;