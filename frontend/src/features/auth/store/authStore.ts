import { create } from "zustand";
import { persist } from "zustand/middleware";
import {type AuthStore } from "../types/auth.types";
import {type User } from "../../users/schemas/users.schema";

export const useAuthStore = create<AuthStore>()(
    persist(
        (set) => ({
            // Initial state
            user: null,
            isAuthenticated: false,
            isLoading: true,
            error: null,

            // Actions
            setUser: (user: User | null) =>
                set({
                    user,
                    isAuthenticated: !!user,
                    error: null,
                }),

            setLoading: (loading: boolean) => set({ isLoading: loading }),

            setError: (error: string | null) => set({ error }),

            logout: () =>
                set({
                    user: null,
                    isAuthenticated: false,
                    error: null,
                }),

            clearError: () => set({ error: null }),
        }),
        {
            name: "auth-storage",
            partialize: (state) => ({ user: state.user }),
            onRehydrateStorage: () => (state) => {
                state?.setLoading(false)
            },
        }
    )
);