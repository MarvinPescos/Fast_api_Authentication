export interface Building {
  id: number;
  building_name: string;
  architectural_style?: string;
}

export interface Rating {
  id: number;
  building_id: number;
  aesthetic_rating: number;
  functionality_rating: number;
  photo_worthiness: number;
  instagram_potential: number;
  weirdness_factor: number;
}

export interface BuildingAverage {
  functionality_avg?: number;
  aesthetic_avg?: number;
  photo_worthiness_avg?: number;
  instagram_potential_avg?: number;
  weirdness_factor_avg?: number;
  total_ratings: number;
}

export interface CampusBuildingRaterState {
  buildings: Building[];
  selectedBuilding: Building | null;
  buildingAverages: BuildingAverage | null;
  ratings: Rating[];
  isLoading: boolean;
  error: string | null;
}
