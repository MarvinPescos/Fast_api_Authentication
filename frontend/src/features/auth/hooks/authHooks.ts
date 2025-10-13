import { useAuthStore } from "../store/authStore";
import { authService } from "../services/auth.service";
import type { loginRequest } from "../schemas/login.schema";
import type { registerRequest } from "../schemas/register.schema";
import type { emailVerificationRequest } from "../schemas/emailVerification.schema";

export function authHooks() {
    const {user, isAuthenticated, isLoading, error, setUser, setLoading, setError, logout, clearError} = useAuthStore();


    const register = async(data: registerRequest) => {
        try{
            setLoading(true);
            setError(null);
            const response = await authService.register(data);
            // Don't set user here - user is not logged in until email is verified
            // setUser(response.user)
            return response
        } catch (error){
            const message = error instanceof Error ? error.message : "Registration Failed"
            setError(message)
            throw error
        } finally {
            setLoading(false)
        }
    };

    const verifyEmail = async(verificationData: emailVerificationRequest) => {
        try{
            setLoading(true);
            setError(null);
            const response = await authService.verifyEmail(verificationData);
            // Don't set user here - user needs to login after verification
            // setUser(response.user)
            return response
        } catch (error) {
            const message = error instanceof Error ? error.message : "Email verification failed"
            setError(message)
            throw error
        } finally {
            setLoading(false)
        }
    };

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
        register,
        verifyEmail,
        login, 
        logout: handleLogout,
        clearError

    };
}