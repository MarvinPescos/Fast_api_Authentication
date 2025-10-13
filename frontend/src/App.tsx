import { registerPage as RegisterPage } from "./features/auth/pages/registerPage"
import { emailVerificationPage as EmailVerificationPage } from "./features/auth/pages/emailVerificationPage"
import { loginPage as LoginPage } from "./features/auth/pages/loginPage"

import { LoadingSpinner } from "./shared/components/LoadingSpinner"
import { Navigate, Route, Routes } from "react-router-dom"
import { useAuthStore } from "./features/auth/store/authStore"

function App() {
    const { isLoading } = useAuthStore()

    if (isLoading) {
        return <LoadingSpinner />
    }

    return (
        <Routes>
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/verify-email" element={<EmailVerificationPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<Navigate to="/register" replace />} />
        </Routes>
    )
}

export default App
