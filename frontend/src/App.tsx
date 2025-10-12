import { registerPage } from "./features/auth/pages/registerPage"
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
            <Route path="/register" element={registerPage()} />
            <Route path="/" element={<Navigate to="/register" replace />} />
        </Routes>
    )
}

export default App
