import { useAuthStore } from "../store/authStore";
import { authService } from "../services/auth.service";
import type { loginRequest } from "../schemas/login.schema";
import type { registerRequest } from "../schemas/register.schema";

export function useAuth() {
    const {user, isAuthenticated, isLoading, error, setUser, setLoading, setError, logout, clearError} = useAuthStore();

    const login = async(credentials: loginRequest) => {
        try{
            setLoading(true);
            setError(null);
            const response = await authService.login(credentials);
            setUser(response.user)
            return response
        } catch (error) {
            const message = error instanceof Error ? error.message: "Login Failed";
            setError(message)
            throw error
        } finally {
            setLoading(false)
        }
    };

    const register = async(data: registerRequest) => {
        try{
            setLoading(true);
            setError(null)
            const response = await authService.register(data);
            setUser(response.user)
            return response
        } catch (error){
            const message = error instanceof Error ? error.message : "Registration Failed"
            setError(message)
            throw error
        } finally {
            setLoading(false)
        }
    };

    const handleLogout= async() => {
        try{
        await authService.logout()
        logout();
        } catch (error) {
            console.log("Logout error:", error);
            logout()
        }
    };


    return {
        // State
        user,
        isAuthenticated,
        isLoading,
        error,

        //Actions
        login, 
        register,
        logout: handleLogout,
        clearError

    };
}