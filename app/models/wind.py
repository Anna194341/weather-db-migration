import enum

from sqlalchemy import Column, Float, Integer, Enum, Boolean
from sqlalchemy.orm import relationship
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


class Wind(Base):
    __tablename__ = "wind"

    id = Column(Integer, primary_key=True, index=True)

    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_direction = Column(Enum(WindDirection))

    gust_mph = Column(Float)
    gust_kph = Column(Float)

    is_good_to_go_out = Column(Boolean)

    weather = relationship("Weather", back_populates="wind")