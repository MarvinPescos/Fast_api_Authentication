import { create } from "zustand";
import type {
  CampusBuildingRaterState,
  Building,
  BuildingAverage,
} from "../types/building.types";
import { campusBuildingRaterService } from "../services/building.service";
import { CreateRatingSchema } from "../schemas/building.schema";
import { ZodError } from "zod";

interface CampusBuildingRaterStore extends CampusBuildingRaterState {
  setSelectedBuilding: (building: Building | null) => void;
  fetchBuildings: () => Promise<void>;
  fetchBuildingAverages: (buildingId: number) => Promise<void>;
  createBuilding: (buildingData: {
    building_name: string;
    architectural_style?: string;
  }) => Promise<void>;
  createRating: (ratingData: any) => Promise<void>;
  getMyRatingForBuilding: (buildingId: number) => Promise<any | null>;
  reset: () => void;
}

const initialState: CampusBuildingRaterState = {
  buildings: [],
  selectedBuilding: null,
  buildingAverages: null,
  ratings: [],
  isLoading: false,
  error: null,
};

export const useCampusBuildingRaterStore = create<CampusBuildingRaterStore>(
  (set, get) => ({
    ...initialState,

    setSelectedBuilding: (building) => set({ selectedBuilding: building }),

    fetchBuildings: async () => {
      set({ isLoading: true, error: null });
      try {
        const buildings = await campusBuildingRaterService.getBuildings();
        set({ buildings, isLoading: false });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Failed to fetch buildings";
        set({ error: errorMessage, isLoading: false });
      }
    },

    fetchBuildingAverages: async (buildingId) => {
      set({ isLoading: true, error: null });
      try {
        const averages = await campusBuildingRaterService.getBuildingAverages(
          buildingId
        );
        set({ buildingAverages: averages, isLoading: false });
      } catch (error) {
        const errorMessage =
          error instanceof Error
            ? error.message
            : "Failed to fetch building averages";
        set({ error: errorMessage, isLoading: false });
      }
    },

    createBuilding: async (buildingData) => {
      set({ isLoading: true, error: null });
      try {
        await campusBuildingRaterService.createBuilding(buildingData);
        // Refresh buildings list after creating
        await get().fetchBuildings();
        set({ isLoading: false });
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Failed to create building";
        set({ error: errorMessage, isLoading: false });
      }
    },

    createRating: async (ratingData) => {
      set({ isLoading: true, error: null });
      try {
        const validatedData = CreateRatingSchema.parse(ratingData);
        await campusBuildingRaterService.createRating(validatedData);
        set({ isLoading: false });
      } catch (error) {
        let errorMessage = "Failed to create rating.";
        if (error instanceof ZodError) {
          errorMessage = error.issues.map((issue) => issue.message).join(", ");
        } else if (error instanceof Error) {
          errorMessage = error.message;
        }
        set({ error: errorMessage, isLoading: false });
      }
    },

    getMyRatingForBuilding: async (buildingId) => {
      try {
        const rating = await campusBuildingRaterService.getMyRatingForBuilding(
          buildingId
        );
        return rating;
      } catch (error) {
        // Don't set error for this function - it's expected to fail when user hasn't rated
        // The service already handles 404 cases properly
        console.warn("Could not fetch user rating for building:", error);
        return null;
      }
    },

    reset: () => set(initialState),
  })
);
