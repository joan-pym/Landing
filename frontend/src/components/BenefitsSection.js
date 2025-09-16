import React from "react";
import { CheckCircle, Users, DollarSign } from "lucide-react";

const BenefitsSection = ({ language }) => {
  const content = {
    es: {
      title: "¿Por qué elegir Pymetra?",
      benefits: [
        {
          icon: CheckCircle,
          title: "Acceso prioritario",
          description: "Recibe antes que nadie las ofertas de tu zona."
        },
        {
          icon: DollarSign,
          title: "Sin coste para ti",
          description: "Registro 100% gratuito para agentes."
        },
        {
          icon: Users,
          title: "Oportunidades reales",
          description: "Conecta con PYMEs serias que buscan agentes ya."
        }
      ]
    },
    en: {
      title: "Why choose Pymetra?",
      benefits: [
        {
          icon: CheckCircle,
          title: "Priority access",
          description: "Get offers in your region before anyone else."
        },
        {
          icon: DollarSign,
          title: "No cost for you",
          description: "100% free registration for agents."
        },
        {
          icon: Users,
          title: "Real opportunities",
          description: "Connect with serious SMEs actively looking for agents."
        }
      ]
    }
  };

  return (
    <section style={{ 
      background: 'var(--pymetra-light-gray)',
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
        </div>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '40px',
          maxWidth: '1000px',
          margin: '0 auto'
        }}>
          {content[language].benefits.map((benefit, index) => {
            const IconComponent = benefit.icon;
            return (
              <div 
                key={index}
                className="card hover-lift"
                style={{ textAlign: 'center' }}
              >
                <div style={{
                  width: '80px',
                  height: '80px',
                  background: 'var(--pymetra-dark-green)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 32px'
                }}>
                  <IconComponent 
                    size={40} 
                    color="var(--white)"
                  />
                </div>
                <h3 
                  className="h2"
                  style={{ 
                    color: 'var(--pymetra-dark-green)',
                    marginBottom: '16px'
                  }}
                >
                  {benefit.title}
                </h3>
                <p className="body-md">
                  {benefit.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default BenefitsSection;