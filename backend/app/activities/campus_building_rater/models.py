from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core import Base

class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    building_name: Mapped[str] = mapped_column(String(255), nullable=False)
    architectural_style: Mapped[str] = mapped_column(String(255), nullable=True)

    ratings = relationship("Rating", back_populates="building")

class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True )
    aesthetic_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    functionality_rating: Mapped[int] = mapped_column(Integer, nullable=False)
    photo_worthiness: Mapped[int] = mapped_column(Integer, nullable=False)
    instagram_potential: Mapped[int] = mapped_column(Integer, nullable=False)
    weirdness_factor: Mapped[int] = mapped_column(Integer, nullable=False)

    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    building = relationship("Building", back_populates="ratings")