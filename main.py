import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import random

# Configure Gemini API
# IMPORTANT: Set GEMINI_API_KEY in your environment variables
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

app = FastAPI(title="EcoTransit AI API")

# Serve the static HTML/JS/CSS files from the "static" folder
app.mount("/ui", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_root():
    # Redirect root URL to the frontend UI
    return FileResponse("static/index.html")

@app.get("/api/data")
async def get_live_data():
    # Simulate live IoT data for Metropolis
    return {
        "traffic_congestion_percent": random.randint(65, 85),
        "transit_passengers": random.randint(40000, 50000),
        "aqi": random.randint(40, 70),
        "micro_mobility_active": random.randint(3000, 4000)
    }

@app.post("/api/chat")
async def chat_with_data(request: ChatRequest):
    # 1. Fetch the current simulated state
    live_state = {
        "traffic": "78%",
        "aqi": "49",
        "active_buses": "120"
    }

    # 2. Inject context into the Gemini prompt
    prompt = f"""
    You are EcoTransit AI, a city planning assistant for Metropolis.
    Current Live System State:
    - Traffic Congestion: {live_state['traffic']}
    - Air Quality Index: {live_state['aqi']}
    - Active Public Transit: {live_state['active_buses']}

    User Query: {request.message}

    Provide a short, actionable response based strictly on these metrics.
    """

    # 3. Call the Gemini 3.5 Flash Model (using 1.5 mapping for SDK compatibility)
    response = model.generate_content(prompt)
    return {"reply": response.text}