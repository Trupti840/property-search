from datetime import datetime
from sqlalchemy import BigInteger, Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Property(Base):
    __tablename__ = "properties"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    locality: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    bhk: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(BigInteger)
    area_sqft: Mapped[int | None] = mapped_column(Integer)
    parking: Mapped[bool] = mapped_column(Boolean)
    possession_status: Mapped[int] = mapped_column(Integer)
    amenities: Mapped[list] = mapped_column(JSONB)
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
