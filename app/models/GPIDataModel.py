from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped
from app.core.database import Base

class GPIData(Base):
    __tablename__ = 'gpi_data'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country: Mapped[String] = mapped_column(String(100), nullable=False)
    iso3c: Mapped[String] = mapped_column(String(3), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(Integer)
    overall_score: Mapped[Float] = mapped_column(Float)
    safety_security: Mapped[Float] = mapped_column(Float)
    ongoing_conflicts: Mapped[Float] = mapped_column(Float)
    militarization: Mapped[Float] = mapped_column(Float)
