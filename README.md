Plant Care Assistant API

The Plant Care Assistant API is a FastAPI-based backend designed to manage plants, track soil and environmental readings, and support a natural-language interface through a ChatGPT plugin. It includes a SQLite database, static web interface, and fully documented REST endpoints.

Features

Plant creation, retrieval, and deletion

Soil and environmental metric tracking (moisture, pH, temperature, humidity, sunlight)

REST API with automatically generated documentation (/docs)

ChatGPT plugin support via .well-known/ai-plugin.json

SQLite database included for local persistence

Static frontend served from the /static directory

CORS enabled for browser and plugin compatibility

Project Structure
plant-care-api/
│── main.py                # FastAPI application
│── plantcare.db           # SQLite database
│── seed_plants.py         # Database seeding script
│── requirements.txt       # Python dependencies
│── .gitignore
│── index.html             # Example HTML interface
│── static/                # Static assets (CSS/JS)
│── .well-known/
│     └── ai-plugin.json   # ChatGPT plugin manifest

Installation and Setup
1. Clone the Repository
git clone https://github.com/deusata1/plant-care-api.git
cd plant-care-api

2. Install Dependencies
pip install -r requirements.txt

3. Run the FastAPI Server
uvicorn main:app --reload


The API will be available at:

API Root: http://localhost:8000

Swagger Documentation: http://localhost:8000/docs

Redoc Documentation: http://localhost:8000/redoc

Static Site: http://localhost:8000/

API Endpoints
Plant Endpoints
Method	Endpoint	Description
GET	/plants	List all plants
POST	/plants	Add a new plant
GET	/plants/{id}	Get a plant’s details
DELETE	/plants/{id}	Delete a plant
Soil Reading Endpoints
Method	Endpoint	Description
GET	/plants/{id}/readings	List readings for a plant
POST	/plants/{id}/readings	Add new soil/environment reading
ChatGPT Plugin Integration

This repository includes a fully functional ChatGPT plugin implementation.

The manifest file is located at:

/.well-known/ai-plugin.json


FastAPI automatically exposes the OpenAPI specification, enabling ChatGPT to:

Add and manage plants

Query plant health

Retrieve readings

Provide automated care recommendations

Database Seeding (Optional)

Run the seeding script to populate initial sample data:

python seed_plants.py

Technologies Used

FastAPI

Uvicorn

Pydantic

SQLite

HTML, CSS, JavaScript

License

A license may be added to this project (MIT recommended).
If you would like a license file generated, ask: “Create an MIT license for my repo.”

Credits

Developed by Thomas A. Deusa as part of a full-stack learning project integrating Python, FastAPI, and ChatGPT plugin development.
