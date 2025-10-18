import { useEffect } from "react";
import { useAuthStore } from "../../features/auth/store/authStore";
import { authService } from "../../features/auth/services/auth.service";

export function useAuthInitialization() {
  const { user, setUser, setLoading } = useAuthStore();

  useEffect(() => {
    const initializeAuth = async () => {
      // If user is stored in localStorage, verify they're still authenticated
      if (user) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
        } catch (error) {
          setUser(null);
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []); // Empty dependency array - only run on mount
}
