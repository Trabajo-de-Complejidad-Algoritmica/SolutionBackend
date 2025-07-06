from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, Mapped
from app.core.database import Base

class CPIData(Base):
    __tablename__ = 'gpi_data'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    country: Mapped[String] = mapped_column(String(100), nullable=False)
    country_code: Mapped[String] = mapped_column(String(3), nullable=False, unique=True)
    region: Mapped[String] = mapped_column(String(50))
    cpi_score: Mapped[int] = mapped_column(Integer)
    standard_error: Mapped[Float] = mapped_column(Float)
    lower_ci: Mapped[int] = mapped_column(Integer)
    upper_ci: Mapped[int] = mapped_column(Integer)