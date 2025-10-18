import React, { useEffect } from "react";
import { useCampusBuildingRaterStore } from "../store/buildingStore";

export function BuildingAverages() {
  const {
    selectedBuilding,
    buildingAverages,
    fetchBuildingAverages,
    isLoading,
  } = useCampusBuildingRaterStore();

  useEffect(() => {
    if (selectedBuilding) {
      fetchBuildingAverages(selectedBuilding.id);
    }
  }, [selectedBuilding, fetchBuildingAverages]);

  if (!selectedBuilding) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Building Averages
        </h3>
        <div className="animate-pulse space-y-3">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-4 bg-gray-200 rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!buildingAverages || buildingAverages.total_ratings === 0) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Building Averages
        </h3>
        <p className="text-gray-500">
          No ratings available for this building yet
        </p>
      </div>
    );
  }

  const averages = [
    { label: "Aesthetic", value: buildingAverages.aesthetic_avg },
    { label: "Functionality", value: buildingAverages.functionality_avg },
    { label: "Photo Worthiness", value: buildingAverages.photo_worthiness_avg },
    {
      label: "Instagram Potential",
      value: buildingAverages.instagram_potential_avg,
    },
    { label: "Weirdness Factor", value: buildingAverages.weirdness_factor_avg },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        {selectedBuilding.building_name} Averages
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        {averages.map((avg) => (
          <div
            key={avg.label}
            className="text-center p-3 bg-gray-50 rounded-lg"
          >
            <div className="text-sm text-gray-600">{avg.label}</div>
            <div className="text-2xl font-bold text-gray-900">
              {avg.value ? avg.value.toFixed(1) : "N/A"}
            </div>
          </div>
        ))}
      </div>
      <div className="text-sm text-gray-600 text-center">
        Based on {buildingAverages.total_ratings} rating
        {buildingAverages.total_ratings !== 1 ? "s" : ""}
      </div>
    </div>
  );
}
