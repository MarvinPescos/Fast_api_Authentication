import { create } from "zustand";
import type { SubscriptionStatus, CatFact } from "../types/catFacts.types";
import { catFactsService } from "../services/catFacts.service";

interface CatFactsState {
  status: SubscriptionStatus | null;
  currentFact: CatFact | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  fetchStatus: () => Promise<void>;
  subscribe: (preferredTime?: string, timezone?: string) => Promise<void>;
  unsubscribe: () => Promise<void>;
  fetchRandomFact: () => Promise<void>;
  clearError: () => void;
}

export const useCatFactsStore = create<CatFactsState>((set) => ({
  status: null,
  currentFact: null,
  isLoading: false,
  error: null,

  fetchStatus: async () => {
    set({ isLoading: true, error: null });
    try {
      const status = await catFactsService.getSubscriptionStatus();
      set({ status, isLoading: false });
    } catch (error: any) {
      // Don't show error for authentication issues - let ProtectedRoute handle it
      if (error.response?.status === 401) {
        set({ isLoading: false });
        return;
      }
      set({
        error:
          error instanceof Error ? error.message : "Failed to fetch status",
        isLoading: false,
      });
    }
  },

  subscribe: async (preferredTime?: string, timezone?: string) => {
    set({ isLoading: true, error: null });
    try {
      await catFactsService.subscribe({
        preferred_time: preferredTime,
        timezone: timezone || "UTC",
      });

      // Refresh status after subscribing
      const status = await catFactsService.getSubscriptionStatus();
      set({ status, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to subscribe",
        isLoading: false,
      });
      throw error;
    }
  },

  unsubscribe: async () => {
    set({ isLoading: true, error: null });
    try {
      await catFactsService.unsubscribe();

      // Refresh status after unsubscribing
      const status = await catFactsService.getSubscriptionStatus();
      set({ status, isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to unsubscribe",
        isLoading: false,
      });
      throw error;
    }
  },

  fetchRandomFact: async () => {
    set({ isLoading: true, error: null });
    try {
      const fact = await catFactsService.getRandomCatFact();
      set({ currentFact: fact, isLoading: false });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to fetch cat fact",
        isLoading: false,
      });
    }
  },

  clearError: () => set({ error: null }),
}));
