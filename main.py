from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List, Optional

# ============================================================
# Config
# ============================================================

# ⬅️ UPDATE THIS whenever ngrok gives you a new URL
NGROK_URL = "https://aerobiologic-denae-unbroken.ngrok-free.dev"

app = FastAPI(
    title="Plant Care Assistant",
    description=(
        "Manage your plants in a simple tracker: list all plants, "
        "add new ones, and delete plants by ID."
    ),
    version="1.0.0",
    # This fixes the “Could not find a valid URL in `servers`” error
    servers=[
        {
            "url": NGROK_URL,
            "description": "Ngrok tunnel for local development",
        }
    ],
)

# Allow ChatGPT (and browsers) to call your API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # for dev; you can lock this down later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Models
# ============================================================

class PlantBase(BaseModel):
    name: str
    species: str
    location: Optional[str] = None


class Plant(PlantBase):
    id: int


# ============================================================
# Simple in-memory "database"
# ============================================================

plants_db: List[Plant] = []
_next_id: int = 1


def get_next_id() -> int:
    global _next_id
    curr = _next_id
    _next_id += 1
    return curr


# ============================================================
# Helper / plugin metadata endpoints
# ============================================================

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "message": "Plant Care Assistant API is running."}


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
def get_manifest():
    """
    Serves the plugin manifest for ChatGPT / Actions.
    Make sure the file .well-known/ai-plugin.json exists next to main.py.
    """
    return FileResponse(
        ".well-known/ai-plugin.json",
        media_type="application/json",
    )


@app.get("/.well-known/logo.png", include_in_schema=False)
def get_logo():
    """
    Serves the logo file referenced in logo_url in ai-plugin.json.
    Place logo.png inside the .well-known folder.
    """
    return FileResponse(
        ".well-known/logo.png",
        media_type="image/png",
    )


@app.get("/legal", response_class=PlainTextResponse, include_in_schema=False)
def legal():
    """
    Simple legal / terms endpoint referenced in the manifest.
    """
    return (
        "Plant Care Assistant\n"
        "This tool is for demonstration and educational purposes only. "
        "It does not replace professional horticultural advice."
    )


# ============================================================
# Plant CRUD endpoints (used by the plugin)
# ============================================================

@app.get("/plants", response_model=List[Plant])
def list_plants():
    """
    List all stored plants.
    """
    return plants_db


@app.post("/plants", response_model=Plant)
def create_plant(plant: PlantBase):
    """
    Create a new plant with name, species, and optional location.
    """
    new_plant = Plant(id=get_next_id(), **plant.dict())
    plants_db.append(new_plant)
    return new_plant


@app.get("/plants/{plant_id}", response_model=Plant)
def get_plant(plant_id: int):
    """
    Get a plant by its ID.
    """
    for p in plants_db:
        if p.id == plant_id:
            return p
    raise HTTPException(status_code=404, detail="Plant not found")


@app.delete("/plants/{plant_id}", response_model=dict)
def delete_plant(plant_id: int):
    """
    Delete a plant by its ID.
    """
    global plants_db
    for index, p in enumerate(plants_db):
        if p.id == plant_id:
            plants_db.pop(index)
            return {"message": f"Plant {plant_id} deleted."}
    raise HTTPException(status_code=404, detail="Plant not found")