from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete, func
from fastapi import HTTPException, status
import structlog
from typing import Optional

from app.activities.campus_building_rater.models import Building, Rating
from app.activities.campus_building_rater.schemas import (
    BuildingCreate, BuildingResponse, BuildingUpdate,
    RatingCreate, RatingResponse, RatingUpdate, BuildingAverageResponse
)

logger = structlog.get_logger(__name__)


class RatingService:
    """
    Service layer for Rating operations (CRUD + Analytics)
    - Create: create_rating
    - Read: get_rating, list_ratings, list_ratings_by_building
    - Update: update_rating
    - Delete: delete_rating
    - Analytics: get_building_average_ratings
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_rating(self, rating_id: int) -> RatingResponse:
        """Get rating by id"""
        try:
            logger.info("getting_rating", rating_id=rating_id)
            result = await self.db.execute(select(Rating).where(Rating.id == rating_id))
            rating = result.scalar_one_or_none()
            if not rating:
                logger.warning("rating_not_found", rating_id=rating_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rating not found")
            return rating
        except HTTPException:
            raise
        except Exception as e:
            logger.error("get_rating_failed", rating_id=rating_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching rating by id failed"
            )

    async def list_ratings(self, limit: int = 20, offset: int = 0) -> list[Rating]:
        """Get all ratings with pagination"""
        try:
            logger.info("fetching_all_ratings", limit=limit, offset=offset)
            result = await self.db.execute(select(Rating).limit(limit).offset(offset))
            ratings = result.scalars().all()
            return ratings
        except Exception as e:
            logger.error("list_ratings_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching all ratings failed"
            )

    async def list_ratings_by_building(self, building_id: int, limit: int = 20, offset: int = 0) -> list[Rating]:
        """Get all ratings for a specific building with pagination"""
        try:
            logger.info("fetching_ratings_for_building", building_id=building_id, limit=limit, offset=offset)
            result = await self.db.execute(
                select(Rating)
                .where(Rating.building_id == building_id)
                .limit(limit)
                .offset(offset)
            )
            ratings = result.scalars().all()
            return ratings
        except Exception as e:
            logger.error("list_ratings_by_building_failed", building_id=building_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching ratings by building failed"
            )

    async def get_user_rating_for_building(self, building_id: int, user_id: int) -> Optional[RatingResponse]:
        """Get a specific user's rating for a building"""
        try:
            logger.info("fetching_user_rating_for_building", building_id=building_id, user_id=user_id)
            
            result = await self.db.execute(
                select(Rating).where(
                    Rating.building_id == building_id,
                    Rating.user_id == user_id
                )
            )
            rating = result.scalar_one_or_none()
            
            if rating:
                logger.info("user_rating_found", rating_id=rating.id)
            else:
                logger.info("user_rating_not_found")
                
            return rating
            
        except Exception as e:
            logger.error("fetching_user_rating_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching user rating failed"
            )

    async def create_rating(self, rating_data: RatingCreate, user_id: int) -> RatingResponse:
        """Create new Rating or update existing one"""
        try:
            logger.info("creating_rating", building_id=rating_data.building_id, user_id=user_id)

            # Verify building exists
            building_result = await self.db.execute(
                select(Building).where(Building.id == rating_data.building_id)
            )
            building = building_result.scalar_one_or_none()
            
            if not building:
                logger.error("building_not_found_for_rating", building_id=rating_data.building_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Building not found"
                )
            
            # Check if user has already rated this building
            existing_rating_result = await self.db.execute(
                select(Rating).where(
                    Rating.building_id == rating_data.building_id,
                    Rating.user_id == user_id
                )
            )
            existing_rating = existing_rating_result.scalar_one_or_none()
            
            if existing_rating:
                # Update existing rating instead of creating new one
                logger.info("updating_existing_rating", rating_id=existing_rating.id)
                update_data = rating_data.model_dump(exclude={'building_id'})
                
                await self.db.execute(
                    update(Rating)
                    .where(Rating.id == existing_rating.id)
                    .values(**update_data)
                )
                
                await self.db.commit()
                await self.db.refresh(existing_rating)
                
                logger.info("rating_updated_successfully", rating_id=existing_rating.id)
                return existing_rating
            else:
                # Create new rating
                rating_dict = rating_data.model_dump()
                rating_dict['user_id'] = user_id
                new_rating = Rating(**rating_dict)

                self.db.add(new_rating)
                await self.db.commit()
                await self.db.refresh(new_rating)

                logger.info("rating_created_successfully", rating_id=new_rating.id)
                return new_rating

        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("rating_creation_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Creation failed due to data conflict"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("rating_creation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Creation failed"
            )

    async def update_rating(self, rating_id: int, rating_data: RatingUpdate) -> RatingResponse:
        """Update existing rating by id"""
        try:
            logger.info("updating_rating", rating_id=rating_id)
            
            result = await self.db.execute(select(Rating).where(Rating.id == rating_id))
            existing_rating = result.scalar_one_or_none()
            
            if not existing_rating:
                logger.warning("rating_not_found_for_update", rating_id=rating_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rating not found"
                )
            
            update_data = rating_data.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning("no_update_data_provided", rating_id=rating_id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No data provided for update"
                )
            
            await self.db.execute(
                update(Rating)
                .where(Rating.id == rating_id)
                .values(**update_data)
            )
            
            await self.db.commit()
            
            updated_result = await self.db.execute(select(Rating).where(Rating.id == rating_id))
            updated_rating = updated_result.scalar_one()
            
            logger.info("rating_updated_successfully", rating_id=rating_id)
            return updated_rating
            
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("rating_update_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update failed due to data conflict"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("rating_update_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Update failed"
            )
    
    async def delete_rating(self, rating_id: int) -> dict:
        """Delete rating by id"""
        try:
            logger.info("deleting_rating", rating_id=rating_id)
            
            result = await self.db.execute(select(Rating).where(Rating.id == rating_id))
            existing_rating = result.scalar_one_or_none()
            
            if not existing_rating:
                logger.warning("rating_not_found_for_deletion", rating_id=rating_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rating not found"
                )
            
            await self.db.execute(delete(Rating).where(Rating.id == rating_id))
            await self.db.commit()
            
            logger.info("rating_deleted_successfully", rating_id=rating_id)
            return {"message": f"Rating with id {rating_id} has been deleted successfully"}
            
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("rating_deletion_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete rating due to existing references"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("rating_deletion_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Delete failed"
            )

    async def get_building_average_ratings(self, building_id: int) -> BuildingAverageResponse:
        """Get average ratings for a specific building"""
        try:
            logger.info("calculating_building_averages", building_id=building_id)
            
            # Verify building exists
            building_result = await self.db.execute(
                select(Building).where(Building.id == building_id)
            )
            building = building_result.scalar_one_or_none()
            
            if not building:
                logger.warning("building_not_found_for_averages", building_id=building_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Building not found"
                )
            
            result = await self.db.execute(
                select(
                    func.avg(Rating.functionality_rating).label("functionality_avg"),
                    func.avg(Rating.aesthetic_rating).label("aesthetic_avg"),
                    func.avg(Rating.photo_worthiness).label("photo_worthiness_avg"),
                    func.avg(Rating.instagram_potential).label("instagram_potential_avg"),
                    func.avg(Rating.weirdness_factor).label("weirdness_factor_avg"),
                    func.count(Rating.id).label("total_ratings")
                ).where(Rating.building_id == building_id)
            )
            
            averages = result.mappings().first()
            
            logger.info("building_averages_calculated", building_id=building_id, total_ratings=averages["total_ratings"])
            return BuildingAverageResponse(**averages)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error("calculate_averages_failed", building_id=building_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Calculating building averages failed"
            )


class BuildingService:
    """
    Service layer for Building operations (CRUD)
    - Create: create_building
    - Read: get_building, list_buildings  
    - Update: update_building
    - Delete: delete_building
    """

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_building(self, building_id: int) -> BuildingResponse:
        """Get building by id"""
        try:
            logger.info("getting_building", building_id=building_id)
            result = await self.db.execute(select(Building).where(Building.id == building_id))
            building = result.scalar_one_or_none()
            if not building:
                logger.warning("building_not_found", building_id=building_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Building not found")
            return building
        except HTTPException:
            raise
        except Exception as e:
            logger.error("get_building_failed", building_id=building_id, error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching building by id failed"
            ) 

    async def list_buildings(self, limit: int = 20, offset: int = 0) -> list[Building]:
        """Get all buildings with pagination"""
        try:
            logger.info("fetching_all_buildings", limit=limit, offset=offset)
            result = await self.db.execute(select(Building).limit(limit).offset(offset))
            buildings = result.scalars().all()
            return buildings
        except Exception as e:
            logger.error("list_buildings_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Fetching all buildings failed"
            )

    async def create_building(self, building_data: BuildingCreate) -> BuildingResponse:
        """Create new Building"""
        try:
            logger.info("creating_building", building_name=building_data.building_name)

            result = await self.db.execute(
                select(Building).where(Building.building_name == building_data.building_name)
            )

            existing_building = result.scalar_one_or_none()

            if existing_building:
                logger.error("building_already_exists", building_name=building_data.building_name)
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Building already exists"
                )
            
            new_building = Building(**building_data.model_dump())

            self.db.add(new_building)
            await self.db.commit()
            await self.db.refresh(new_building)

            logger.info("building_created_successfully", building_id=new_building.id)
            return new_building

        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("building_creation_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Creation failed due to data conflict"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("building_creation_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Creation failed"
            )

    async def update_building(self, building_id: int, building_data: BuildingUpdate) -> BuildingResponse:
        """Update existing building by id"""
        try:
            logger.info("updating_building", building_id=building_id)
            
            result = await self.db.execute(select(Building).where(Building.id == building_id))
            existing_building = result.scalar_one_or_none()
            
            if not existing_building:
                logger.warning("building_not_found_for_update", building_id=building_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Building not found"
                )
            
            update_data = building_data.model_dump(exclude_unset=True)
            
            if not update_data:
                logger.warning("no_update_data_provided", building_id=building_id)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No data provided for update"
                )
            
            if "building_name" in update_data:
                name_check_result = await self.db.execute(
                    select(Building).where(
                        Building.building_name == update_data["building_name"],
                        Building.id != building_id
                    )
                )
                conflicting_building = name_check_result.scalar_one_or_none()
                
                if conflicting_building:
                    logger.error("building_name_conflict", building_name=update_data['building_name'])
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Building name already exists"
                    )
            
            await self.db.execute(
                update(Building)
                .where(Building.id == building_id)
                .values(**update_data)
            )
            
            await self.db.commit()
            
            updated_result = await self.db.execute(select(Building).where(Building.id == building_id))
            updated_building = updated_result.scalar_one()
            
            logger.info("building_updated_successfully", building_id=building_id)
            return updated_building
            
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("building_update_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Update failed due to data conflict"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("building_update_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Update failed"
            )
    
    async def delete_building(self, building_id: int) -> dict:
        """Delete building by id"""
        try:
            logger.info("deleting_building", building_id=building_id)
            
            result = await self.db.execute(select(Building).where(Building.id == building_id))
            existing_building = result.scalar_one_or_none()
            
            if not existing_building:
                logger.warning("building_not_found_for_deletion", building_id=building_id)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Building not found"
                )
            
            await self.db.execute(delete(Building).where(Building.id == building_id))
            await self.db.commit()
            
            logger.info("building_deleted_successfully", building_id=building_id)
            return {"message": f"Building with id {building_id} has been deleted successfully"}
            
        except HTTPException:
            raise
        except IntegrityError as e:
            await self.db.rollback()
            logger.error("building_deletion_integrity_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot delete building due to existing references (ratings exist)"
            )
        except Exception as e:
            await self.db.rollback()
            logger.error("building_deletion_failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Delete failed"
            )
