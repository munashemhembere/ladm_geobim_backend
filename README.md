# LADM Backend API

## Description
This project is a FastAPI application that provides endpoints for managing spatial units and their traceability.

## Installation
1. Clone the repository.
2. Create a virtual environment and activate it.
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
Run the application using Uvicorn:
```
uvicorn app.main:app --reload
```

## API Endpoints
- `GET /spatialunits`: Retrieve all spatial units.
- `GET /traceability/{uid}`: Retrieve traceability information for a specific spatial unit.

## Environment Variables
Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```