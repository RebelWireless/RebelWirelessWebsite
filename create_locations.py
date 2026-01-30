#!/usr/bin/env python3
import os
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.crud.location import add_location
from app.routes import LocationCreate

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

locations_to_add = [
    {
        "name": "Downtown Store",
        "address": "123 Main St",
        "city": "Metropolis",
        "postal_code": "12345",
        "lat": 40.7128,
        "lng": -74.0060,
        "service_types": ["4G", "5G"],
        "max_speed": "500Mbps",
    },
    {
        "name": "Uptown Store",
        "address": "456 Elm St",
        "city": "Metropolis",
        "postal_code": "12346",
        "lat": 40.7306,
        "lng": -73.9352,
        "service_types": ["4G"],
        "max_speed": "200Mbps",
    },
]

def main():
    db: Session = SessionLocal()
    try:
        for loc_data in locations_to_add:
            loc = LocationCreate(**loc_data)
            added_loc = add_location(db, loc.dict())
            print(f"Added location: {added_loc.name} (ID: {added_loc.id})")
    finally:
        db.close()


if __name__ == "__main__":
    main()
