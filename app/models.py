from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# -------------------------
# SpatialUnit
# -------------------------
class SpatialUnit(Base):
    __tablename__ = "la_spatialunit"

    uid = Column(String, primary_key=True)
    name = Column(String)
    dimension = Column(String)
    geom = Column(Geometry("POLYGON", srid=4326))
    begin_lifespan_version = Column(TIMESTAMP)
    end_lifespan_version = Column(TIMESTAMP)

    baunits = relationship("BAUnit", secondary="la_baunit_spatialunit", back_populates="spatial_units")
    sources = relationship("Source", secondary="la_source_spatialunit", back_populates="spatial_units")


# -------------------------
# BAUnit
# -------------------------
class BAUnit(Base):
    __tablename__ = "la_baunit"

    baunit_id = Column(String, primary_key=True)
    name = Column(String)
    type = Column(String)
    begin_lifespan_version = Column(TIMESTAMP)
    end_lifespan_version = Column(TIMESTAMP)

    spatial_units = relationship("SpatialUnit", secondary="la_baunit_spatialunit", back_populates="baunits")
    rrrs = relationship("RRR", secondary="la_rrr_baunit", back_populates="baunits")


class BAUnitSpatialUnit(Base):
    __tablename__ = "la_baunit_spatialunit"

    baunit_id = Column(String, ForeignKey("la_baunit.baunit_id"), primary_key=True)
    uid = Column(String, ForeignKey("la_spatialunit.uid"), primary_key=True)


# -------------------------
# RRR
# -------------------------
class RRR(Base):
    __tablename__ = "la_rrr"

    rrr_id = Column(String, primary_key=True)
    type = Column(String)
    party_id = Column(String, ForeignKey("la_party.party_id"))
    begin_lifespan_version = Column(TIMESTAMP)
    end_lifespan_version = Column(TIMESTAMP)

    baunits = relationship("BAUnit", secondary="la_rrr_baunit", back_populates="rrrs")
    party = relationship("Party", back_populates="rrrs")
    sources = relationship("Source", secondary="la_source_rrr", back_populates="rrrs")


class RRRBAUnit(Base):
    __tablename__ = "la_rrr_baunit"

    rrr_id = Column(String, ForeignKey("la_rrr.rrr_id"), primary_key=True)
    baunit_id = Column(String, ForeignKey("la_baunit.baunit_id"), primary_key=True)


# -------------------------
# Party
# -------------------------
class Party(Base):
    __tablename__ = "la_party"

    party_id = Column(String, primary_key=True)
    name = Column(String)
    party_type = Column(String)
    begin_lifespan_version = Column(TIMESTAMP)
    end_lifespan_version = Column(TIMESTAMP)

    rrrs = relationship("RRR", back_populates="party")


# -------------------------
# Source
# -------------------------
class Source(Base):
    __tablename__ = "la_source"

    source_id = Column(String, primary_key=True)
    type = Column(String)
    description = Column(String)
    begin_lifespan_version = Column(TIMESTAMP)
    end_lifespan_version = Column(TIMESTAMP)

    rrrs = relationship("RRR", secondary="la_source_rrr", back_populates="sources")
    spatial_units = relationship("SpatialUnit", secondary="la_source_spatialunit", back_populates="sources")


class SourceRRR(Base):
    __tablename__ = "la_source_rrr"

    source_id = Column(String, ForeignKey("la_source.source_id"), primary_key=True)
    rrr_id = Column(String, ForeignKey("la_rrr.rrr_id"), primary_key=True)


class SourceSpatialUnit(Base):
    __tablename__ = "la_source_spatialunit"

    source_id = Column(String, ForeignKey("la_source.source_id"), primary_key=True)
    uid = Column(String, ForeignKey("la_spatialunit.uid"), primary_key=True)