from sqlalchemy.orm import Session
from models import SpatialUnit, BAUnit, RRR, Party, Source

# Create a new SpatialUnit
def create_spatial_unit(db: Session, spatial_unit: SpatialUnit):
    db.add(spatial_unit)
    db.commit()
    db.refresh(spatial_unit)
    return spatial_unit

# Read all SpatialUnits
def get_spatial_units(db: Session):
    return db.query(SpatialUnit).all()

# Read a SpatialUnit by UID
def get_spatial_unit(db: Session, uid: str):
    return db.query(SpatialUnit).filter(SpatialUnit.uid == uid).first()

# Update a SpatialUnit
def update_spatial_unit(db: Session, uid: str, updated_data: dict):
    spatial_unit = get_spatial_unit(db, uid)
    if spatial_unit:
        for key, value in updated_data.items():
            setattr(spatial_unit, key, value)
        db.commit()
        db.refresh(spatial_unit)
    return spatial_unit

# Delete a SpatialUnit
def delete_spatial_unit(db: Session, uid: str):
    spatial_unit = get_spatial_unit(db, uid)
    if spatial_unit:
        db.delete(spatial_unit)
        db.commit()
    return spatial_unit

# Similar CRUD functions can be implemented for BAUnit, RRR, Party, and Source models.