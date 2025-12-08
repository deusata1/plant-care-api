<p align="center">
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  </a>
  <a href="https://fastapi.tiangolo.com/">
    <img src="https://img.shields.io/badge/FastAPI-0.110+-009688.svg" alt="FastAPI">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
  <a href="http://localhost:8000/docs">
    <img src="https://img.shields.io/badge/OpenAPI-Auto--Generated-lightgrey.svg" alt="OpenAPI Docs">
  </a>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Project Status">
</p>

<br>

Plant Care Assistant API

The Plant Care Assistant API is a FastAPI-based backend designed to manage plants, track soil and environmental readings, and support a natural-language interface through a ChatGPT plugin. It includes a SQLite database, static web interface, and fully documented REST endpoints.

---

Features

- Plant creation, retrieval, and deletion  
- Soil and environmental metric tracking (moisture, pH, temperature, humidity, sunlight)  
- REST API with automatically generated documentation (`/docs`)  
- ChatGPT plugin support via `.well-known/ai-plugin.json`  
- SQLite database for local persistence  
- Static frontend served from the `/static` directory  
- CORS enabled for browser and plugin compatibility

## Screenshots

API Root Status Page

<p align="center">
  <img src="https://raw.githubusercontent.com/deusata1/plant-care-api/main/static.png" width="700">
</p>

ChatGPT Plugin Manifest Page

<p align="center">
  <img src="https://raw.githubusercontent.com/deusata1/plant-care-api/main/plugin.png" width="700">
</p>

FastAPI Documentation (Swagger UI)

<p align="center">
  <img src="https://raw.githubusercontent.com/deusata1/plant-care-api/main/fast%20api.png" width="700">
</p>

Technologies Used

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Framework-009688.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Uvicorn-ASGI%20Server-orange.svg" alt="Uvicorn">
  <img src="https://img.shields.io/badge/Pydantic-Data%20Validation-green.svg" alt="Pydantic">
  <img src="https://img.shields.io/badge/SQLite-Database-lightgrey.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/HTML-Frontend-red.svg" alt="HTML">
  <img src="https://img.shields.io/badge/CSS-Styling-blueviolet.svg" alt="CSS">
  <img src="https://img.shields.io/badge/JavaScript-Scripting-yellow.svg" alt="JavaScript">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI%20Docs-Swagger%20UI-green.svg" alt="Swagger UI">
  <img src="https://img.shields.io/badge/OpenAPI-Automatic%20Documentation-lightgrey.svg" alt="OpenAPI">
  <img src="https://img.shields.io/badge/ChatGPT%20Plugin-Enabled-blue.svg" alt="ChatGPT Plugin">
</p>

Project Structure

    main.py                            # FastAPI application
    plantcare.db                       # SQLite database
    seed_plants.py                     # Database seeding script
    requirements.txt                   # Python dependencies
    .gitignore
    index.html                         # Example HTML interface
    static/ # Static assets (CSS/JS)
    .well-known/
        ai-plugin.json                 # ChatGPT plugin manifest

Installation and Setup

1. Clone the Repository

    git clone https://github.com/deusata1/plant-care-api.git
    cd plant-care-api

2. Install Dependencies

   pip install -r requirements.txt

3. Run the FastAPI Server

  uvicorn main:app --reload

  API Available At:

      http://localhost:8000
      http://localhost:8000/docs
      http://localhost:8000/redoc
      http://localhost:8000/

API Endpoints

Plant Endpoints

| Method | Endpoint       | Description           |
| ------ | -------------- | --------------------- |
| GET    | `/plants`      | List all plants       |
| POST   | `/plants`      | Add a new plant       |
| GET    | `/plants/{id}` | Get plant details     |
| DELETE | `/plants/{id}` | Delete a plant        |

Soil Rendering Endpoints

| Method | Endpoint                | Description                      |
| ------ | ----------------------- | -------------------------------- |
| GET    | `/plants/{id}/readings` | List readings for a plant        |
| POST   | `/plants/{id}/readings` | Add new soil/environment reading |

ChatGPT Plugin Integration

This repository includes a fully functional ChatGPT plugin located at:

      /.well-known/ai-plugin.json

FastAPI automatically exposes the OpenAI specification, enabling ChatGPT to:

      Add and Manage Plants
      Query Plant Health
      Retrieve Readings
      Provided Automated Care Recommendations

Database Seeding (Optional)

    python seed_plants.py

License

This project is licensed under the MIT License.
See the LICENSE file for details.

Credits

Developed by Thomas A. Deusa as part of a full-stack project integrating Python, FastAPI, and ChatGPT Plugins.




---
