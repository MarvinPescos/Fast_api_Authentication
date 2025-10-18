import { useAuthStore } from "../store/authStore";
import { authService } from "../services/auth.service";
import type { loginRequest } from "../schemas/login.schema";
import type { registerRequest } from "../schemas/register.schema";
import type { emailVerificationRequest } from "../schemas/emailVerification.schema";

export function authHooks() {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    setUser,
    setLoading,
    setError,
    logout,
    clearError,
  } = useAuthStore();

  const register = async (data: registerRequest) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authService.register(data);
      // Don't set user here - user is not logged in until email is verified
      // setUser(response.user)
      return response;
    } catch (error: any) {
      let message = "Registration failed. Please try again.";

      // Handle different types of errors
      if (error?.response?.status === 400) {
        if (error?.response?.data?.detail?.includes("email")) {
          message =
            "This email is already registered. Please use a different email or try logging in.";
        } else if (error?.response?.data?.detail?.includes("username")) {
          message =
            "This username is already taken. Please choose a different username.";
        } else {
          message =
            error?.response?.data?.detail ||
            "Please check your information and try again.";
        }
      } else if (error?.response?.status === 422) {
        message = "Please check that all fields are filled correctly.";
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const verifyEmail = async (verificationData: emailVerificationRequest) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authService.verifyEmail(verificationData);
      // Don't set user here - user needs to login after verification
      // setUser(response.user)
      return response;
    } catch (error: any) {
      let message = "Email verification failed. Please try again.";

      // Handle different types of errors
      if (error?.response?.status === 400) {
        message =
          "Invalid verification code. Please check your email and try again.";
      } else if (error?.response?.status === 404) {
        message =
          "Verification code not found. Please request a new verification email.";
      } else if (error?.response?.status === 410) {
        message =
          "Verification code has expired. Please request a new verification email.";
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const login = async (credentials: loginRequest) => {
    try {
      setLoading(true);
      setError(null);
      const response = await authService.login(credentials);
      setUser(response.user);
      return response;
    } catch (error: any) {
      let message = "Login failed. Please try again.";

      // Handle different types of errors
      if (error?.response?.status === 401) {
        message =
          "Invalid email or password. Please check your credentials and try again.";
      } else if (error?.response?.status === 403) {
        if (error?.response?.data?.detail === "2FA_REQUIRED") {
          message =
            "Two-factor authentication required. Please enter your 6-digit code.";
        } else {
          message =
            "Account is not verified. Please check your email for verification instructions.";
        }
      } else if (error?.response?.status === 422) {
        message = "Please check your email and password format.";
      } else if (error?.response?.status === 429) {
        message =
          "Too many login attempts. Please wait a moment before trying again.";
      } else if (error?.response?.data?.detail) {
        // Use backend error message if available
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const loginWithFacebook = async () => {
    try {
      setLoading(true);
      setError(null);

      const { authorization_url } = await authService.getFacebookLoginUrl();

      window.location.href = authorization_url;
    } catch (error: any) {
      let message = "Facebook login failed. Please try again.";

      if (error?.response?.status === 500) {
        message =
          "Facebook login is temporarily unavailable. Please try again later.";
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const loginWithGoogle = async () => {
    try {
      setLoading(true);
      setError(null);

      const { authorization_url } = await authService.getGoogleLoginUrl();

      window.location.href = authorization_url;
    } catch (error: any) {
      let message = "Google login failed. Please try again.";

      if (error?.response?.status === 500) {
        message =
          "Google login is temporarily unavailable. Please try again later.";
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const resendVerification = async (user_id: number | undefined) => {
    try {
      if (!user_id || typeof user_id !== "number") {
        throw new Error("Invalid user ID");
      }

      setLoading(true);
      setError(null);
      const response = await authService.resendVerification(user_id);
      return response;
    } catch (error: any) {
      let message = "Failed to resend verification email. Please try again.";

      // Handle different types of errors
      if (error?.response?.status === 400) {
        message =
          "Unable to resend verification email. Please try again later.";
      } else if (error?.response?.status === 404) {
        message = "User not found. Please try registering again.";
      } else if (error?.response?.status === 429) {
        message =
          "Too many requests. Please wait before requesting another verification email.";
      } else if (error?.response?.data?.detail) {
        message = error.response.data.detail;
      } else if (error instanceof Error) {
        message = error.message;
      }

      setError(message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      logout();
    } catch (error) {
      logout();
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
    resendVerification,
    login,
    loginWithFacebook,
    loginWithGoogle,
    logout: handleLogout,
    clearError,
  };
}
