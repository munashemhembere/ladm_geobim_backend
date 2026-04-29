from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
import json
from database import SessionLocal
from models import SpatialUnit, BAUnit, RRR, Party, Source

app = FastAPI()

# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def root():
    return RedirectResponse (url="/docs")
# -------------------------
# DB Session Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# SpatialUnits Endpoint
# -------------------------
@app.get("/spatialunits")
def get_spatialunits(db: Session = Depends(get_db)):
    results = db.execute(select(SpatialUnit)).scalars().all()
    features = []
    for su in results:
        geojson_str = db.scalar(su.geom.ST_AsGeoJSON())
        geometry = json.loads(geojson_str) if geojson_str else None
        features.append({
            "type": "Feature",
            "geometry": geometry,
            "properties": {
                "uid": su.uid,
                "name": su.name,
                "dimension": su.dimension,
                "valid_from": su.begin_lifespan_version,
                "valid_to": su.end_lifespan_version
            }
        })
    return {"type": "FeatureCollection", "features": features}

# -------------------------
# Traceability Endpoint
# -------------------------
@app.get("/traceability/{uid}")
def get_traceability(uid: str, db: Session = Depends(get_db)):
    # Step 1: Find the SpatialUnit
    su = db.query(SpatialUnit).filter(SpatialUnit.uid == uid).first()
    if not su:
        return {"error": f"SpatialUnit {uid} not found"}

    trace = {
        "spatial_unit": {
            "uid": su.uid,
            "name": su.name,
            "dimension": su.dimension
        },
        "baunits": []
    }

    # Step 2: For each BAUnit linked to this SpatialUnit
    for ba in su.baunits:
        baunit_info = {
            "baunit_id": ba.baunit_id,
            "name": ba.name,
            "type": ba.type,
            "rrrs": []
        }

        # Step 3: For each RRR linked to this BAUnit
        for r in ba.rrrs:
            rrr_info = {
                "rrr_id": r.rrr_id,
                "type": r.type,
                "party": {
                    "party_id": r.party.party_id,
                    "name": r.party.name,
                    "party_type": r.party.party_type
                } if r.party else None,
                "sources": [
                    {
                        "source_id": s.source_id,
                        "type": s.type,
                        "description": s.description
                    }
                    for s in r.sources
                ]
            }
            baunit_info["rrrs"].append(rrr_info)

        trace["baunits"].append(baunit_info)

    return trace