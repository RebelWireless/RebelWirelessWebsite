from sqlalchemy.orm import Session
from app.models.location import Location

def get_all_locations(db: Session):
    return db.query(Location).all()

def add_location(db: Session, loc_data: dict):
    loc = Location(**loc_data)
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc

def get_location_by_name(db: Session, name: str):
    return db.query(Location).filter(Location.name == name).first()
