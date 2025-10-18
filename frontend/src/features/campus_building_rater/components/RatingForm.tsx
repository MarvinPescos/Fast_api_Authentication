import React, { useState, useEffect } from "react";
import { useCampusBuildingRaterStore } from "../store/buildingStore";

export function RatingForm() {
  const {
    selectedBuilding,
    createRating,
    isLoading,
    fetchBuildingAverages,
    getMyRatingForBuilding,
  } = useCampusBuildingRaterStore();
  const [ratings, setRatings] = useState({
    aesthetic_rating: 5,
    functionality_rating: 5,
    photo_worthiness: 5,
    instagram_potential: 5,
    weirdness_factor: 5,
  });
  const [showSuccess, setShowSuccess] = useState(false);
  const [isUpdate, setIsUpdate] = useState(false); // Track if this is an update

  // Reset form when selected building changes
  useEffect(() => {
    const checkExistingRating = async () => {
      if (selectedBuilding) {
        const existingRating = await getMyRatingForBuilding(
          selectedBuilding.id
        );
        if (existingRating) {
          // User has already rated this building, populate form with existing values
          setRatings({
            aesthetic_rating: existingRating.aesthetic_rating,
            functionality_rating: existingRating.functionality_rating,
            photo_worthiness: existingRating.photo_worthiness,
            instagram_potential: existingRating.instagram_potential,
            weirdness_factor: existingRating.weirdness_factor,
          });
          setIsUpdate(true);
        } else {
          // User hasn't rated this building yet, use default values
          setRatings({
            aesthetic_rating: 5,
            functionality_rating: 5,
            photo_worthiness: 5,
            instagram_potential: 5,
            weirdness_factor: 5,
          });
          setIsUpdate(false);
        }
      }
      setShowSuccess(false);
    };

    checkExistingRating();
  }, [selectedBuilding, getMyRatingForBuilding]);

  const handleRatingChange = (field: string, value: number) => {
    setRatings((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBuilding) return;

    try {
      await createRating({
        building_id: selectedBuilding.id,
        ...ratings,
      });

      // Show success message
      setShowSuccess(true);

      // Reset form
      setRatings({
        aesthetic_rating: 5,
        functionality_rating: 5,
        photo_worthiness: 5,
        instagram_potential: 5,
        weirdness_factor: 5,
      });

      // Refresh building averages
      await fetchBuildingAverages(selectedBuilding.id);

      // Hide success message after 3 seconds
      setTimeout(() => setShowSuccess(false), 3000);
    } catch (error) {
      console.error("Failed to submit rating:", error);
    }
  };

  if (!selectedBuilding) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Rate Building
        </h3>
        <p className="text-gray-500">Please select a building to rate</p>
      </div>
    );
  }

  const ratingFields = [
    {
      key: "aesthetic_rating",
      label: "Aesthetic Rating",
      description: "How aesthetically pleasing is the building?",
    },
    {
      key: "functionality_rating",
      label: "Functionality Rating",
      description: "How functional is the building?",
    },
    {
      key: "photo_worthiness",
      label: "Photo Worthiness",
      description: "Is it worth taking photos of?",
    },
    {
      key: "instagram_potential",
      label: "Instagram Potential",
      description: "Would it look good on Instagram?",
    },
    {
      key: "weirdness_factor",
      label: "Weirdness Factor",
      description: "How weird/unique is the architecture?",
    },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        {isUpdate
          ? `Update Rating for ${selectedBuilding.building_name}`
          : `Rate ${selectedBuilding.building_name}`}
      </h3>

      {/* Success Message */}
      {showSuccess && (
        <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <svg
              className="w-5 h-5 text-green-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-green-800 font-medium">
              {isUpdate
                ? "Rating updated successfully! Building averages have been refreshed."
                : "Rating submitted successfully! Building averages have been updated."}
            </span>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        {ratingFields.map((field) => (
          <div key={field.key}>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {field.label} (1-10)
            </label>
            <p className="text-sm text-gray-600 mb-3">{field.description}</p>
            <div className="flex items-center space-x-4">
              <input
                type="range"
                min="1"
                max="10"
                value={ratings[field.key as keyof typeof ratings]}
                onChange={(e) =>
                  handleRatingChange(field.key, parseInt(e.target.value))
                }
                className="flex-1"
              />
              <span className="text-lg font-semibold text-gray-900 w-8 text-center">
                {ratings[field.key as keyof typeof ratings]}
              </span>
            </div>
          </div>
        ))}

        <button
          type="submit"
          disabled={isLoading}
          className="w-full px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {isLoading
            ? isUpdate
              ? "Updating Rating..."
              : "Submitting Rating..."
            : isUpdate
            ? "Update Rating"
            : "Submit Rating"}
        </button>
      </form>
    </div>
  );
}
