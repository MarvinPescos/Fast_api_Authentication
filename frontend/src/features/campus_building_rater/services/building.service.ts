import api from "../../../shared/services/api";
import type {
  BuildingType,
  RatingType,
  CreateRatingType,
} from "../schemas/building.schema";

export class CampusBuildingRaterService {
  async getBuildings(): Promise<BuildingType[]> {
    try {
      const response = await api.get(
        "/fullstack_authentication/activities/campus_building_rater/buildings"
      );
      return response as unknown as BuildingType[];
    } catch (error: any) {
      console.error("Failed to fetch buildings:", error);
      throw new Error("Failed to fetch buildings");
    }
  }

  async getBuildingAverages(buildingId: number): Promise<any> {
    try {
      const response = await api.get(
        `/fullstack_authentication/activities/campus_building_rater/buildings/${buildingId}/averages`
      );
      return response;
    } catch (error: any) {
      console.error("Failed to fetch building averages:", error);
      throw new Error("Failed to fetch building averages");
    }
  }

  async createBuilding(buildingData: {
    building_name: string;
    architectural_style?: string;
  }): Promise<BuildingType> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/campus_building_rater/buildings",
        buildingData
      );
      return response as unknown as BuildingType;
    } catch (error: any) {
      console.error("Failed to create building:", error);
      throw new Error("Failed to create building");
    }
  }

  async createRating(ratingData: CreateRatingType): Promise<RatingType> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/campus_building_rater/ratings",
        ratingData
      );
      return response as unknown as RatingType;
    } catch (error: any) {
      console.error("Failed to create rating:", error);
      throw new Error("Failed to create rating");
    }
  }

  async getMyRatingForBuilding(buildingId: number): Promise<RatingType | null> {
    try {
      const response = await api.get(
        `/fullstack_authentication/activities/campus_building_rater/buildings/${buildingId}/my-rating`
      );
      return response as unknown as RatingType;
    } catch (error: any) {
      if (error.response?.status === 404) {
        return null; // User hasn't rated this building yet
      }

      console.warn("Could not fetch user rating for building:", error);
      return null;
    }
  }
}

export const campusBuildingRaterService = new CampusBuildingRaterService();
