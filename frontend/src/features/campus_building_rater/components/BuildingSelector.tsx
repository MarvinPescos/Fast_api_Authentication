import React from "react";
import { useCampusBuildingRaterStore } from "../store/buildingStore";
import type { Building } from "../types/building.types";

export function BuildingSelector() {
  const { buildings, selectedBuilding, setSelectedBuilding, fetchBuildings } =
    useCampusBuildingRaterStore();

  React.useEffect(() => {
    fetchBuildings();
  }, [fetchBuildings]);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Select Building
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {buildings.map((building) => (
          <button
            key={building.id}
            onClick={() => setSelectedBuilding(building)}
            className={`p-4 border rounded-lg text-left transition-colors ${
              selectedBuilding?.id === building.id
                ? "border-amber-500 bg-amber-50"
                : "border-gray-200 hover:border-gray-300"
            }`}
          >
            <div className="font-medium text-gray-900">
              {building.building_name}
            </div>
            {building.architectural_style && (
              <div className="text-sm text-gray-600 mt-1">
                {building.architectural_style}
              </div>
            )}
          </button>
        ))}
      </div>
    </div>
  );
}
