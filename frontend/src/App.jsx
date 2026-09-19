import { Navigate, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage.jsx";
import CalculatorPage from "./pages/CalculatorPage.jsx";
import ContactsPage from "./pages/ContactsPage.jsx";
import Layout from "./components/Layout.jsx";
import LegalPage from "./pages/LegalPage.jsx";
import LoginPage from "./pages/LoginPage.jsx";
import ActiveSOSPage from "./pages/ActiveSOSPage.jsx";
import ProfilePage from "./pages/ProfilePage.jsx";
import SignupPage from "./pages/SignupPage.jsx";
import TherapyPage from "./pages/TherapyPage.jsx";
import TrackPage from "./pages/TrackPage.jsx";

export default function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      {/* Public SOS tracking link (no login required - the link is the key) */}
      <Route path="/track/:sosId" element={<TrackPage />} />

      {/* Authenticated app */}
      <Route element={<Layout />}>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/therapy" element={<TherapyPage />} />
        <Route path="/legal" element={<LegalPage />} />
        <Route path="/contacts" element={<ContactsPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/sos/:sosId" element={<ActiveSOSPage />} />
        <Route path="/calculator" element={<CalculatorPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}