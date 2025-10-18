from pydantic import BaseModel, Field, validator
from typing import List, Optional
import re

class BuildingBase(BaseModel):
    building_name: str = Field(..., min_length=3, max_length=50, description="building name")
    architectural_style: str | None = None

    @validator('building_name')
    def validate_name(cls, v: str) -> str:
        if not re.match(r'^[A-Za-z0-9\s\-]+$', v):
            raise ValueError("Building name must contain only letters, numbers, spaces, or dashes")
        return v


class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BuildingBase):
    building_name: str | None = None
    architectural_style: str | None = None

class BuildingResponse(BuildingBase):
    id: int = Field(..., description="Building Response id")
    
    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    aesthetic_rating: int = Field(..., ge=1, le=10, description="Aesthetic rating (1-10)")
    functionality_rating: int = Field(..., ge=1, le=10, description="Functionality rating (1-10)")
    photo_worthiness: int = Field(..., ge=1, le=10, description="Photo worthiness rating (1-10)")
    instagram_potential: int = Field(..., ge=1, le=10, description="Instagram potential rating (1-10)")
    weirdness_factor: int = Field(..., ge=1, le=10, description="Weirdness factor rating (1-10)")

    @validator('aesthetic_rating', 'functionality_rating', 'photo_worthiness', 
              'instagram_potential', 'weirdness_factor')
    def validate_rating_range(cls, v: int) -> int:
        if not 1 <= v <= 10:
            raise ValueError("Rating must be between 1 and 10")
        return v

class RatingCreate(RatingBase):
    building_id: int = Field(..., description="ID of the building being rated")

class RatingUpdate(BaseModel):
    aesthetic_rating: Optional[int] = Field(None, ge=1, le=10, description="Aesthetic rating (1-10)")
    functionality_rating: Optional[int] = Field(None, ge=1, le=10, description="Functionality rating (1-10)")
    photo_worthiness: Optional[int] = Field(None, ge=1, le=10, description="Photo worthiness rating (1-10)")
    instagram_potential: Optional[int] = Field(None, ge=1, le=10, description="Instagram potential rating (1-10)")
    weirdness_factor: Optional[int] = Field(None, ge=1, le=10, description="Weirdness factor rating (1-10)")

    @validator('aesthetic_rating', 'functionality_rating', 'photo_worthiness', 
              'instagram_potential', 'weirdness_factor', pre=True)
    def validate_rating_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not 1 <= v <= 10:
            raise ValueError("Rating must be between 1 and 10")
        return v

class RatingResponse(RatingBase):
    id: int = Field(..., description="Rating ID")
    building_id: int = Field(..., description="Building ID")
    user_id: int = Field(..., description="User ID")

    class Config: 
        from_attributes = True

class BuildingAverageResponse(BaseModel):
    functionality_avg: Optional[float] = Field(None, description="Average functionality rating")
    aesthetic_avg: Optional[float] = Field(None, description="Average aesthetic rating")
    photo_worthiness_avg: Optional[float] = Field(None, description="Average photo worthiness rating")
    instagram_potential_avg: Optional[float] = Field(None, description="Average Instagram potential rating")
    weirdness_factor_avg: Optional[float] = Field(None, description="Average weirdness factor rating")
    total_ratings: int = Field(..., description="Total number of ratings")