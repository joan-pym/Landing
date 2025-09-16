import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./components/LandingPage";
import LegalNoticeES from "./components/legal/LegalNoticeES";
import LegalNoticeEN from "./components/legal/LegalNoticeEN";
import PrivacyES from "./components/legal/PrivacyES";
import PrivacyEN from "./components/legal/PrivacyEN";
import CookiesES from "./components/legal/CookiesES";
import CookiesEN from "./components/legal/CookiesEN";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/es/aviso-legal" element={<LegalNoticeES />} />
          <Route path="/en/legal-notice" element={<LegalNoticeEN />} />
          <Route path="/es/privacidad" element={<PrivacyES />} />
          <Route path="/en/privacy" element={<PrivacyEN />} />
          <Route path="/es/cookies" element={<CookiesES />} />
          <Route path="/en/cookies" element={<CookiesEN />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;