from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# -------------------------
# SpatialUnit Schema
# -------------------------
class SpatialUnitBase(BaseModel):
    uid: str
    name: str
    dimension: str
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class SpatialUnitCreate(SpatialUnitBase):
    pass

class SpatialUnit(SpatialUnitBase):
    class Config:
        orm_mode = True

# -------------------------
# BAUnit Schema
# -------------------------
class BAUnitBase(BaseModel):
    baunit_id: str
    name: str
    type: str
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class BAUnitCreate(BAUnitBase):
    pass

class BAUnit(BAUnitBase):
    spatial_units: List[SpatialUnit] = []
    
    class Config:
        orm_mode = True

# -------------------------
# RRR Schema
# -------------------------
class RRRBase(BaseModel):
    rrr_id: str
    type: str
    party_id: Optional[str] = None
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class RRRCreate(RRRBase):
    pass

class RRR(RRRBase):
    party: Optional[str] = None  # Simplified for serialization
    class Config:
        orm_mode = True

# -------------------------
# Party Schema
# -------------------------
class PartyBase(BaseModel):
    party_id: str
    name: str
    party_type: str
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class PartyCreate(PartyBase):
    pass

class Party(PartyBase):
    rrrs: List[RRR] = []
    
    class Config:
        orm_mode = True

# -------------------------
# Source Schema
# -------------------------
class SourceBase(BaseModel):
    source_id: str
    type: str
    description: str
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    rrrs: List[RRR] = []
    spatial_units: List[SpatialUnit] = []
    
    class Config:
        orm_mode = True