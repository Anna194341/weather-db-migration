import enum

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, Time
from app.database.db import Base


class WindDirection(enum.Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)

    country = Column(String, nullable=False)
    location_name = Column(String, nullable=False)

    last_updated = Column(DateTime, nullable=False)
    temperature_celsius = Column(Float)

    sunrise = Column(Time)

    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(Enum(WindDirection))

    gust_mph = Column(Float)
    gust_kph = Column(Float)