from sqlalchemy import Column, DateTime, Float, Integer, String, Time, ForeignKey
from app.database.db import Base


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)

    country = Column(String, nullable=False)
    location_name = Column(String, nullable=False)

    last_updated = Column(DateTime, nullable=False)
    temperature_celsius = Column(Float)

    sunrise = Column(Time)

    wind_id = Column(Integer, ForeignKey("wind.id"))