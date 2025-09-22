import React, { useState } from "react";
import { Upload } from "lucide-react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const RegistrationSection = ({ language }) => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    geographicArea: '',
    mainSector: '',
    cv: null
  });

  const content = {
    es: {
      title: "Únete a Pymetra",
      subtitle: "Completa tu registro y empieza a recibir oportunidades hoy mismo",
      fields: {
        fullName: "Nombre completo",
        email: "Email",
        geographicArea: "Zona geográfica",
        mainSector: "Sector principal",
        cv: "Adjuntar CV (PDF o DOC)"
      },
      sectors: [
        "Selecciona tu sector",
        "Tecnología",
        "Servicios profesionales",
        "Manufactura",
        "Comercio",
        "Construcción",
        "Alimentación",
        "Textil",
        "Automoción",
        "Energía",
        "Otros"
      ],
      cta: "Unirme gratis",
      successMessage: "¡Registro completado! Te contactaremos pronto con nuevas oportunidades."
    },
    en: {
      title: "Join Pymetra",
      subtitle: "Complete your registration and start receiving opportunities today",
      fields: {
        fullName: "Full name",
        email: "Email",
        geographicArea: "Geographic area",
        mainSector: "Main sector",
        cv: "Upload CV (PDF or DOC)"
      },
      sectors: [
        "Select your sector",
        "Technology",
        "Professional services",
        "Manufacturing",
        "Retail",
        "Construction",
        "Food & Beverage",
        "Textile",
        "Automotive",
        "Energy",
        "Others"
      ],
      cta: "Join for free",
      successMessage: "Registration completed! We'll contact you soon with new opportunities."
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'file' ? files[0] : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Mock form submission - this will be replaced with actual Google Sheets/Gmail integration
    console.log('Form submitted:', formData);
    alert(content[language].successMessage);
    
    // Reset form
    setFormData({
      fullName: '',
      email: '',
      geographicArea: '',
      mainSector: '',
      cv: null
    });
    e.target.reset();
  };

  return (
    <section 
      id="registration-section"
      style={{ 
        background: 'var(--pymetra-light-gray)',
        padding: '100px 0'
      }}
    >
      <div className="container">
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
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
        
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
          <form 
            onSubmit={handleSubmit}
            className="card"
            style={{ background: 'var(--white)' }}
          >
            <div className="form-group">
              <label className="form-label">
                {content[language].fields.fullName}
              </label>
              <input
                type="text"
                name="fullName"
                className="form-input"
                value={formData.fullName}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                {content[language].fields.email}
              </label>
              <input
                type="email"
                name="email"
                className="form-input"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                {content[language].fields.geographicArea}
              </label>
              <input
                type="text"
                name="geographicArea"
                className="form-input"
                value={formData.geographicArea}
                onChange={handleInputChange}
                placeholder={language === 'es' ? 'Ej: Madrid, Barcelona, Valencia...' : 'E.g: Madrid, Barcelona, Valencia...'}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">
                {content[language].fields.mainSector}
              </label>
              <select
                name="mainSector"
                className="form-select"
                value={formData.mainSector}
                onChange={handleInputChange}
                required
              >
                {content[language].sectors.map((sector, index) => (
                  <option key={index} value={index === 0 ? '' : sector}>
                    {sector}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">
                {content[language].fields.cv}
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type="file"
                  name="cv"
                  accept=".pdf,.doc,.docx"
                  onChange={handleInputChange}
                  style={{ display: 'none' }}
                  id="cv-upload"
                  required
                />
                <label 
                  htmlFor="cv-upload"
                  className="file-input"
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '12px',
                    cursor: 'pointer'
                  }}
                >
                  <Upload size={24} color="var(--pymetra-orange)" />
                  <span>
                    {formData.cv 
                      ? formData.cv.name 
                      : (language === 'es' ? 'Seleccionar archivo' : 'Select file')
                    }
                  </span>
                </label>
              </div>
            </div>

            <button type="submit" className="btn-primary" style={{ width: '100%', marginTop: '24px' }}>
              {content[language].cta}
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default RegistrationSection;