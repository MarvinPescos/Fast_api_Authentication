import { useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { useAuthStore } from "../store/authStore";
import { authService } from "../services/auth.service";

export function OAuthCallbackPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setUser } = useAuthStore();

  useEffect(() => {
    const handleOAuthCallback = async () => {
      const loginStatus = searchParams.get("login");

      if (loginStatus === "success") {
        try {
          // Fetch user data from JWT cookie
          const userData = await authService.getCurrentUser();
          setUser(userData);
          navigate("/home", { replace: true });
        } catch (error: any) {
          navigate("/login", {
            replace: true,
            state: { error: "Failed to load user data. Please try again." },
          });
        }
      } else {
        // Login failed
        navigate("/login", {
          replace: true,
          state: { error: "OAuth login failed. Please try again." },
        });
      }
    };

    handleOAuthCallback();
  }, [searchParams, navigate, setUser]);

  return (
    <div className="flex items-center justify-center min-h-screen flex-col gap-3">
      <LoadingSpinner />
      <p>Completing sign-in and redirecting to dashboard...</p>
    </div>
  );
}
