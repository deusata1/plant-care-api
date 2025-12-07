from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

app = FastAPI(title="Plant Care API")

# ---------- Models ----------

class LocationCreate(BaseModel):
    name: str
    soil_type: Optional[str] = None
    drainage: Optional[str] = None
    default_sun_exposure: Optional[str] = None

class Location(LocationCreate):
    id: int

class PlantCreate(BaseModel):
    name: str
    species: Optional[str] = None
    location_id: int
    sun_exposure: Optional[str] = None  # full_sun, partial_shade, shade
    watering_preference: Optional[str] = None  # low, medium, high
    soil_preference: Optional[str] = None  # for example slightly_acidic
    notes: Optional[str] = None

class Plant(PlantCreate):
    id: int
    planting_date: datetime

class ReadingCreate(BaseModel):
    plant_id: int
    soil_moisture: Optional[float] = None  # 0-100
    soil_ph: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    light_level: Optional[float] = None

class Reading(ReadingCreate):
    id: int
    timestamp: datetime

class Recommendation(BaseModel):
    plant_id: int
    created_at: datetime
    messages: List[str]

# ---------- In-memory "database" ----------

locations: Dict[int, Location] = {}
plants: Dict[int, Plant] = {}
readings: Dict[int, Reading] = {}

location_id_counter = 1
plant_id_counter = 1
reading_id_counter = 1

# ---------- Helper: recommendation engine ----------

def generate_recommendations(plant: Plant, latest_reading: Optional[Reading]) -> List[str]:
    if latest_reading is None:
        return ["No readings yet. Add a soil reading to get recommendations."]

    msgs: List[str] = []

    # 1. Moisture
    if latest_reading.soil_moisture is not None and plant.watering_preference is not None:
        m = latest_reading.soil_moisture
        wp = plant.watering_preference

        if wp == "low":
            low, high = 10, 40
        elif wp == "medium":
            low, high = 30, 60
        elif wp == "high":
            low, high = 50, 80
        else:
            low, high = 30, 60

        if m < low:
            msgs.append(f"Soil moisture is {m:.1f}% which is dry for this plant. Water soon.")
        elif m > high:
            msgs.append(
                f"Soil moisture is {m:.1f}% which is high for this plant. "
                "Risk of overwatering; hold off on watering and check drainage."
            )
        else:
            msgs.append(f"Soil moisture ({m:.1f}%) is within a healthy range for this plant.")

    # 2. pH (simple generic rule)
    if latest_reading.soil_ph is not None:
        ph = latest_reading.soil_ph
        if plant.soil_preference and "acid" in plant.soil_preference.lower():
            ideal_low, ideal_high = 5.5, 6.5
        else:
            ideal_low, ideal_high = 6.0, 7.5

        if ph < ideal_low:
            msgs.append(
                f"Soil pH {ph:.1f} is low (acidic). "
                "Consider adding lime or mixing in less acidic soil."
            )
        elif ph > ideal_high:
            msgs.append(
                f"Soil pH {ph:.1f} is high (alkaline). "
                "Consider adding soil acidifier such as sulfur or organic matter like peat moss."
            )
        else:
            msgs.append(f"Soil pH ({ph:.1f}) is within a reasonable range.")

    if not msgs:
        msgs.append("No specific issues detected with the latest reading.")

    return msgs

# ---------- Routes ----------

@app.get("/")
def root():
    return {"message": "Plant Care API is running."}

# Locations
@app.post("/locations", response_model=Location)
def create_location(loc: LocationCreate):
    global location_id_counter
    location = Location(id=location_id_counter, **loc.dict())
    locations[location_id_counter] = location
    location_id_counter += 1
    return location

@app.get("/locations", response_model=List[Location])
def list_locations():
    return list(locations.values())

@app.get("/locations/{location_id}", response_model=Location)
def get_location(location_id: int):
    if location_id not in locations:
        raise HTTPException(status_code=404, detail="Location not found")
    return locations[location_id]

# Plants
@app.post("/plants", response_model=Plant)
def create_plant(p: PlantCreate):
    global plant_id_counter
    if p.location_id not in locations:
        raise HTTPException(status_code=400, detail="location_id does not exist")

    plant = Plant(
        id=plant_id_counter,
        planting_date=datetime.utcnow(),
        **p.dict()
    )
    plants[plant_id_counter] = plant
    plant_id_counter += 1
    return plant

@app.get("/plants", response_model=List[Plant])
def list_plants():
    return list(plants.values())

@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    if plant_id not in plants:
        raise HTTPException(status_code=404, detail="Plant not found")
    return plants[plant_id]

# Readings
@app.post("/readings", response_model=Reading)
def create_reading(r: ReadingCreate):
    global reading_id_counter
    if r.plant_id not in plants:
        raise HTTPException(status_code=400, detail="plant_id does not exist")

    reading = Reading(
        id=reading_id_counter,
        timestamp=datetime.utcnow(),
        **r.dict()
    )
    readings[reading_id_counter] = reading
    reading_id_counter += 1
    return reading

@app.get("/plants/{plant_id}/readings", response_model=List[Reading])
def list_readings_for_plant(plant_id: int):
    if plant_id not in plants:
        raise HTTPException(status_code=404, detail="Plant not found")
    return [r for r in readings.values() if r.plant_id == plant_id]

# Recommendations
@app.get("/plants/{plant_id}/recommendations", response_model=Recommendation)
def get_recommendations(plant_id: int):
    if plant_id not in plants:
        raise HTTPException(status_code=404, detail="Plant not found")

    plant = plants[plant_id]

    # Find latest reading for this plant
    plant_readings = [r for r in readings.values() if r.plant_id == plant_id]
    latest = max(plant_readings, key=lambda r: r.timestamp) if plant_readings else None

    messages = generate_recommendations(plant, latest)
    return Recommendation(
        plant_id=plant_id,
        created_at=datetime.utcnow(),
        messages=messages
    )
