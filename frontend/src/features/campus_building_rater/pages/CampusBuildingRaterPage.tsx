import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useCampusBuildingRaterStore } from "../store/buildingStore";
import { BuildingSelector } from "../components/BuildingSelector";
import { RatingForm } from "../components/RatingForm";
import { BuildingAverages } from "../components/BuildingAverages";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";

export function CampusBuildingRaterPage() {
  const navigate = useNavigate();
  const { error, createBuilding, isLoading } = useCampusBuildingRaterStore();
  const [showAddForm, setShowAddForm] = useState(false);
  const [buildingName, setBuildingName] = useState("");
  const [architecturalStyle, setArchitecturalStyle] = useState("");

  const handleAddBuilding = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!buildingName.trim()) return;

    await createBuilding({
      building_name: buildingName.trim(),
      architectural_style: architecturalStyle.trim() || undefined,
    });

    // Reset form
    setBuildingName("");
    setArchitecturalStyle("");
    setShowAddForm(false);
  };

  const handleBackToDashboard = () => {
    navigate("/home");
  };

  return (
    <ActivityLayout
      title="Campus Building Rater"
      description="Rate and review campus buildings based on various criteria"
      currentPath="/activities/campus-building-rater"
    >
      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="text-red-500">⚠️</div>
            <div>
              <p className="font-medium text-red-800">Error</p>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Add Building Section */}
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Add New Building
          </h3>
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="px-4 py-2 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors"
          >
            {showAddForm ? "Cancel" : "Add Building"}
          </button>
        </div>

        {showAddForm && (
          <form onSubmit={handleAddBuilding} className="space-y-4">
            <div>
              <label
                htmlFor="building-name"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Building Name *
              </label>
              <input
                type="text"
                id="building-name"
                value={buildingName}
                onChange={(e) => setBuildingName(e.target.value)}
                placeholder="e.g., Main Library, Science Building"
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
                required
              />
            </div>
            <div>
              <label
                htmlFor="architectural-style"
                className="block text-sm font-medium text-gray-700 mb-2"
              >
                Architectural Style (Optional)
              </label>
              <input
                type="text"
                id="architectural-style"
                value={architecturalStyle}
                onChange={(e) => setArchitecturalStyle(e.target.value)}
                placeholder="e.g., Modern, Gothic, Brutalist"
                className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={isLoading || !buildingName.trim()}
              className="w-full px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed h-12 flex items-center justify-center"
            >
              {isLoading ? (
                <div className="flex items-center space-x-2 h-6">
                  <LoadingSpinner size="sm" />
                  <span>Adding...</span>
                </div>
              ) : (
                <div className="h-6 flex items-center">Add Building</div>
              )}
            </button>
          </form>
        )}
      </div>

      <BuildingSelector />
      <BuildingAverages />
      <RatingForm />
    </ActivityLayout>
  );
}
