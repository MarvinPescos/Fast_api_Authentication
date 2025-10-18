from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core import get_db
from app.users import User
from app.auth.dependencies import get_current_user
from app.activities.campus_building_rater.service import BuildingService, RatingService
from app.activities.campus_building_rater.schemas import (
    BuildingCreate, BuildingResponse, BuildingUpdate,
    RatingCreate, RatingResponse, RatingUpdate, BuildingAverageResponse
)

router = APIRouter()


# ========== BUILDING ENDPOINTS ==========

@router.post(
    "/buildings",
    response_model=BuildingResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new building"
)
async def create_building(
    building_data: BuildingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new campus building.
    
    Requires authentication.
    """
    service = BuildingService(db)
    return await service.create_building(building_data)


@router.get(
    "/buildings",
    response_model=List[BuildingResponse],
    status_code=status.HTTP_200_OK,
    description="Get all buildings with pagination"
)
async def list_buildings(
    limit: int = Query(20, ge=1, le=100, description="Number of buildings to return"),
    offset: int = Query(0, ge=0, description="Number of buildings to skip"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all buildings with pagination.
    
    Requires authentication.
    """
    service = BuildingService(db)
    return await service.list_buildings(limit=limit, offset=offset)


@router.get(
    "/buildings/{building_id}",
    response_model=BuildingResponse,
    status_code=status.HTTP_200_OK,
    description="Get building by ID"
)
async def get_building(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a specific building by its ID.
    
    Requires authentication.
    """
    service = BuildingService(db)
    return await service.get_building(building_id)


@router.put(
    "/buildings/{building_id}",
    response_model=BuildingResponse,
    status_code=status.HTTP_200_OK,
    description="Update building by ID"
)
async def update_building(
    building_id: int,
    building_data: BuildingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing building's information.
    
    Requires authentication.
    """
    service = BuildingService(db)
    return await service.update_building(building_id, building_data)


@router.delete(
    "/buildings/{building_id}",
    status_code=status.HTTP_200_OK,
    description="Delete building by ID"
)
async def delete_building(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a building. 
    
    Note: Cannot delete if building has ratings.
    
    Requires authentication.
    """
    service = BuildingService(db)
    return await service.delete_building(building_id)


# ========== RATING ENDPOINTS ==========

@router.post(
    "/ratings",
    response_model=RatingResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create a new rating for a building"
)
async def create_rating(
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Rate a campus building.
    
    All ratings are on a scale of 1-10:
    - aesthetic_rating: How aesthetically pleasing is the building?
    - functionality_rating: How functional is the building?
    - photo_worthiness: Is it worth taking photos of?
    - instagram_potential: Would it look good on Instagram?
    - weirdness_factor: How weird/unique is the architecture?
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.create_rating(rating_data, current_user.id)


@router.get(
    "/ratings",
    response_model=List[RatingResponse],
    status_code=status.HTTP_200_OK,
    description="Get all ratings with pagination"
)
async def list_ratings(
    limit: int = Query(20, ge=1, le=100, description="Number of ratings to return"),
    offset: int = Query(0, ge=0, description="Number of ratings to skip"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all ratings with pagination.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.list_ratings(limit=limit, offset=offset)


@router.get(
    "/ratings/{rating_id}",
    response_model=RatingResponse,
    status_code=status.HTTP_200_OK,
    description="Get rating by ID"
)
async def get_rating(
    rating_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a specific rating by its ID.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.get_rating(rating_id)


@router.get(
    "/buildings/{building_id}/ratings",
    response_model=List[RatingResponse],
    status_code=status.HTTP_200_OK,
    description="Get all ratings for a specific building"
)
async def list_ratings_by_building(
    building_id: int,
    limit: int = Query(20, ge=1, le=100, description="Number of ratings to return"),
    offset: int = Query(0, ge=0, description="Number of ratings to skip"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all ratings for a specific building with pagination.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.list_ratings_by_building(building_id, limit=limit, offset=offset)


@router.get(
    "/buildings/{building_id}/averages",
    response_model=BuildingAverageResponse,
    status_code=status.HTTP_200_OK,
    description="Get average ratings for a building"
)
async def get_building_averages(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate and retrieve average ratings for a specific building.
    
    Returns averages for all rating categories plus total rating count.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.get_building_average_ratings(building_id)


@router.get(
    "/buildings/{building_id}/my-rating",
    response_model=RatingResponse,
    status_code=status.HTTP_200_OK,
    description="Get current user's rating for a specific building"
)
async def get_my_rating_for_building(
    building_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user's rating for a specific building.
    
    Returns the user's rating if they have rated the building, otherwise returns null.
    Requires authentication.
    """
    service = RatingService(db)
    rating = await service.get_user_rating_for_building(building_id, current_user.id)
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You haven't rated this building yet"
        )
    return rating


@router.put(
    "/ratings/{rating_id}",
    response_model=RatingResponse,
    status_code=status.HTTP_200_OK,
    description="Update rating by ID"
)
async def update_rating(
    rating_id: int,
    rating_data: RatingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing rating.
    
    All fields are optional - only provide the ones you want to update.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.update_rating(rating_id, rating_data)


@router.delete(
    "/ratings/{rating_id}",
    status_code=status.HTTP_200_OK,
    description="Delete rating by ID"
)
async def delete_rating(
    rating_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a rating.
    
    Requires authentication.
    """
    service = RatingService(db)
    return await service.delete_rating(rating_id)

