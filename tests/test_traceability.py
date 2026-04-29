from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import SessionLocal
from app.models import Base, SpatialUnit, BAUnit, RRR, Party, Source

# Setup the test database
DATABASE_URL = "postgresql://postgres:fall20back01@localhost:5432/test_ladm_uz"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[SessionLocal] = override_get_db

def test_get_traceability():
    # Assuming a SpatialUnit with uid 'test_uid' exists in the test database
    response = client.get("/traceability/test_uid")
    assert response.status_code == 200
    assert "spatial_unit" in response.json()
    assert response.json()["spatial_unit"]["uid"] == "test_uid"

def test_get_traceability_not_found():
    response = client.get("/traceability/non_existent_uid")
    assert response.status_code == 404
    assert response.json() == {"error": "SpatialUnit non_existent_uid not found"}