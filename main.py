from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

# ============================================================
# Database Utilities
# ============================================================

DB_PATH = "plantcare.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create plants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            species TEXT NOT NULL,
            location TEXT
        )
    """)

    # Create readings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_id INTEGER NOT NULL,
            moisture INTEGER,
            ph REAL,
            temperature REAL,
            humidity REAL,
            sunlight INTEGER,
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ============================================================
# FastAPI App Configuration
# ============================================================

app = FastAPI(
    title="Plant Care Assistant",
    description="Manage your plants: list all plants, add new ones, and delete plants by ID.",
    version="1.0.0",
    servers=[
        {
            "url": "https://plant-care-api-slmt.onrender.com",
            "description": "Render Deployment"
        }
    ]
)

# Enable CORS for plugin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Mount Static Directories
# ============================================================

# Serve /static for frontend assets
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve .well-known for plugin manifest + logo
if os.path.isdir(".well-known"):
    app.mount("/.well-known", StaticFiles(directory=".well-known"), name="well-known")

# ============================================================
# Data Models
# ============================================================

class PlantBase(BaseModel):
    name: str
    species: str
    location: Optional[str] = None

class Plant(PlantBase):
    id: int

class Reading(BaseModel):
    moisture: Optional[int] = None
    ph: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    sunlight: Optional[int] = None

# ============================================================
# Root Endpoint
# ============================================================

@app.get("/")
def root():
    return {"status": "ok", "message": "Plant Care Assistant API is running."}

# ============================================================
# Plant Endpoints
# ============================================================

@app.get("/plants", response_model=List[Plant])
def list_plants():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, species, location FROM plants")
    rows = cursor.fetchall()
    conn.close()

    return [
        {"id": r[0], "name": r[1], "species": r[2], "location": r[3]}
    for r in rows]

@app.post("/plants", response_model=Plant)
def create_plant(plant: PlantBase):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO plants (name, species, location) VALUES (?, ?, ?)",
        (plant.name, plant.species, plant.location)
    )
    conn.commit()
    plant_id = cursor.lastrowid
    conn.close()

    return {"id": plant_id, **plant.dict()}

@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, species, location FROM plants WHERE id = ?",
        (plant_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    return {"id": row[0], "name": row[1], "species": row[2], "location": row[3]}

@app.delete("/plants/{plant_id}")
def delete_plant(plant_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Plant not found")

    return {"message": "Plant deleted successfully"}

# ============================================================
# Reading Endpoints
# ============================================================

@app.get("/plants/{plant_id}/readings", response_model=List[Reading])
def get_readings(plant_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT moisture, ph, temperature, humidity, sunlight FROM readings WHERE plant_id = ?",
        (plant_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "moisture": r[0],
            "ph": r[1],
            "temperature": r[2],
            "humidity": r[3],
            "sunlight": r[4]
        }
    for r in rows]

@app.post("/plants/{plant_id}/readings")
def add_reading(plant_id: int, reading: Reading):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO readings (plant_id, moisture, ph, temperature, humidity, sunlight)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            plant_id,
            reading.moisture,
            reading.ph,
            reading.temperature,
            reading.humidity,
            reading.sunlight
        )
    )
    conn.commit()
    conn.close()

    return {"message": "Reading added successfully"}

# ============================================================
# Run App (Render Auto-Port)
# ============================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
