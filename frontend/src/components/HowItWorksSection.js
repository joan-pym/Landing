import React from "react";
import { UserPlus, Mail, Handshake } from "lucide-react";

const HowItWorksSection = ({ language }) => {
  const content = {
    es: {
      title: "¿Cómo funciona?",
      subtitle: "Tres pasos simples para empezar a recibir oportunidades",
      steps: [
        {
          icon: UserPlus,
          title: "Te registras gratis",
          description: "Completa tu perfil y sube tu CV en menos de 5 minutos."
        },
        {
          icon: Mail,
          title: "Recibes ofertas relevantes",
          description: "Te enviamos solo las oportunidades que encajan contigo."
        },
        {
          icon: Handshake,
          title: "Contactas con la empresa interesada",
          description: "Conecta directamente y cierra el acuerdo."
        }
      ]
    },
    en: {
      title: "How it works?",
      subtitle: "Three simple steps to start receiving opportunities",
      steps: [
        {
          icon: UserPlus,
          title: "Register for free",
          description: "Complete your profile and upload your CV in less than 5 minutes."
        },
        {
          icon: Mail,
          title: "Receive relevant offers",
          description: "We send you only opportunities that match your profile."
        },
        {
          icon: Handshake,
          title: "Connect directly with the company",
          description: "Connect directly with interested companies and close deals."
        }
      ]
    }
  };

  return (
    <section style={{ 
      background: 'var(--white)',
      padding: '100px 0'
    }}>
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '80px' }}>
          <h2 
            className="display-md"
            style={{ 
              color: 'var(--pymetra-dark-green)',
              marginBottom: '24px'
            }}
          >
            {content[language].title}
          </h2>
          <p className="body-lg" style={{ maxWidth: '600px', margin: '0 auto' }}>
            {content[language].subtitle}
          </p>
        </div>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '40px',
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          {content[language].steps.map((step, index) => {
            const IconComponent = step.icon;
            return (
              <div 
                key={index}
                className="card hover-lift"
                style={{ textAlign: 'center', position: 'relative' }}
              >
                <div style={{
                  position: 'absolute',
                  top: '-20px',
                  left: '50%',
                  transform: 'translateX(-50%)',
                  width: '40px',
                  height: '40px',
                  background: 'var(--pymetra-orange)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  color: 'var(--white)',
                  fontSize: '1.25rem'
                }}>
                  {index + 1}
                </div>
                
                <div style={{
                  width: '80px',
                  height: '80px',
                  background: 'rgba(243, 146, 0, 0.1)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '32px auto'
                }}>
                  <IconComponent 
                    size={40} 
                    color="var(--pymetra-orange)"
                  />
                </div>
                
                <h3 
                  className="h2"
                  style={{ 
                    color: 'var(--pymetra-dark-green)',
                    marginBottom: '16px'
                  }}
                >
                  {step.title}
                </h3>
                <p className="body-md">
                  {step.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;