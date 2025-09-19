import React, { useEffect } from "react";

const HeroSection = ({ language }) => {
  // Precargar la imagen para carga más rápida
  const preloadImage = () => {
    const img = new Image();
    img.src = "https://customer-assets.emergentagent.com/job_sales-portal-17/artifacts/j37inyl3_ChatGPT%20Image%2018%20set%202025%2C%2015_38_20.png";
  };

  // Ejecutar precarga cuando se monta el componente
  useEffect(() => {
    preloadImage();
  }, []);
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
              src="https://customer-assets.emergentagent.com/job_sales-portal-17/artifacts/j37inyl3_ChatGPT%20Image%2018%20set%202025%2C%2015_38_20.png"
              alt="Símbolo Pymetra"
              style={{ 
                width: '200px', 
                height: '200px',
                objectFit: 'contain',
                display: 'block',
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