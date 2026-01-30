from sqlalchemy import Column, Integer, String, Float, JSON
from app.database import Base

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    service_types = Column(JSON, nullable=True)  # store list
    max_speed = Column(String, nullable=True)
