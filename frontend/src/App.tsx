import { registerPage as RegisterPage } from "./features/auth/pages/registerPage";
import { emailVerificationPage as EmailVerificationPage } from "./features/auth/pages/emailVerificationPage";
import { loginPage as LoginPage } from "./features/auth/pages/loginPage";
import { ForgotPasswordPage } from "./features/auth/pages/ForgotPasswordPage";
import { ResetPasswordPage } from "./features/auth/pages/ResetPasswordPage";
import { OAuthCallbackPage } from "./features/auth/pages/OAuthCallbackPage";
import { DashboardPage } from "./features/auth/pages/DashboardPage";
import { ProfilePage } from "./features/auth/pages/ProfilePage";
import { TriviaPage } from "./features/trivia/pages/TriviaPage";
import { CiphersPage } from "./features/ciphers/pages/CiphersPage";
import { QRGeneratorPage } from "./features/qr_generator/pages/QRGeneratorPage";
import { CampusBuildingRaterPage } from "./features/campus_building_rater/pages/CampusBuildingRaterPage";
import { JokeCipherQRPage } from "./features/joke_cipher_qr/pages/JokeCipherQRPage";
import { CatFactsPage } from "./features/cat_facts/pages/CatFactsPage";
import { TwoFactorSettingsPage } from "./features/auth/pages/TwoFactorSettingsPage";

import { LoadingSpinner } from "./shared/components/LoadingSpinner";
import { ProtectedRoute } from "./shared/components/ProtectedRoute";
import { Navigate, Route, Routes } from "react-router-dom";
import { useAuthStore } from "./features/auth/store/authStore";
import { useAuthInitialization } from "./shared/hooks/useAuthInitialization";

function App() {
  const { isLoading } = useAuthStore();

  // Initialize authentication on app startup
  useAuthInitialization();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <Routes>
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/verify-email" element={<EmailVerificationPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />
      <Route path="/dashboard" element={<OAuthCallbackPage />} />
      <Route
        path="/home"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/trivia"
        element={
          <ProtectedRoute>
            <TriviaPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/ciphers"
        element={
          <ProtectedRoute>
            <CiphersPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/qr-generator"
        element={
          <ProtectedRoute>
            <QRGeneratorPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/campus-building-rater"
        element={
          <ProtectedRoute>
            <CampusBuildingRaterPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/joke-cipher-qr"
        element={
          <ProtectedRoute>
            <JokeCipherQRPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/activities/cat-facts"
        element={
          <ProtectedRoute>
            <CatFactsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/settings/2fa"
        element={
          <ProtectedRoute>
            <TwoFactorSettingsPage />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/register" replace />} />
    </Routes>
  );
}

export default App;
