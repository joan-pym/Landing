import React, { useState, useEffect } from "react";
import Header from "./Header";
import HeroSection from "./HeroSection";
import BenefitsSection from "./BenefitsSection";
import HowItWorksSection from "./HowItWorksSection";
import RegistrationSection from "./RegistrationSection";
import FinalCTASection from "./FinalCTASection";
import Footer from "./Footer";

const LandingPage = () => {
  const [language, setLanguage] = useState('es');

  // Update page title based on language
  useEffect(() => {
    const titles = {
      es: "Pymetra - Conecta con PYMEs Europeas",
      en: "Pymetra - Connect with European SMEs"
    };
    document.title = titles[language];
  }, [language]);

  const toggleLanguage = () => {
    setLanguage(language === 'es' ? 'en' : 'es');
  };

  return (
    <div className="landing-page">
      <Header language={language} toggleLanguage={toggleLanguage} />
      <HeroSection language={language} />
      <BenefitsSection language={language} />
      <HowItWorksSection language={language} />
      <RegistrationSection language={language} />
      <FinalCTASection language={language} />
      <Footer language={language} />
    </div>
  );
};

export default LandingPage;