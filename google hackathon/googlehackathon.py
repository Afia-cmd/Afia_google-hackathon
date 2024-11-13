import openai
from flask import Flask,  render_template, request, jsonify
import geopy
from geopy.geocoders import Nominatim
import requests
import os
print("Current Working Directory:", os.getcwd())

# Initialize Flask App

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reproductive_health')
def reproductive_health():
    print("Navigated to Reproductive Health page") 
    return render_template('reproductive_health.html')

@app.route('/mental_health')
def mental_health():
    return render_template('mental_health.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

@app.route('/self_care_tips')
def self_care_tips():
    return render_template('self_care_tips.html')

@app.route('/doctor_contacts')
def doctor_contacts():
    return render_template('doctor_contacts.html')

if __name__ == '__main__':
    app.run(debug=True)


openai.api_key = "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"

# Define a function to query OpenAI GPT model
def get_health_info(user_query):
    response = openai.Completion.create(
        engine="text-davinci-003",  # or "gpt-4" for more advanced models
        prompt=user_query,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Define function to get nearby clinics using Google Maps API
def get_clinics(location):
    api_key = "AIzaSyAiMhWAmn5SpTTWODneXHf7oJxUxIBckCE       "
    geolocator = Nominatim(user_agent="healthcare-bot")
    location = geolocator.geocode(location)
    if location:
        lat, lon = location.latitude, location.longitude
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=5000&type=hospital&key={api_key}"
        response = requests.get(url)
        return response.json()
    return "Location not found."

# Define function to get helplines (for demo purposes, using a static list)
def get_helplines():
    helplines = {
        "Mental Health": "National Mental Health Helpline: 1-800-123-4567",
        "Reproductive Health": "Women's Health Helpline: 1-800-987-6543"
    }
    return helplines

# Define the route to handle user queries
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_query = data.get("query", "").strip()
    location = data.get("location", "")

    # Get healthcare info from GPT-3 or GPT-4
    health_info = get_health_info(user_query)
    
    # Get nearby clinics if a location is provided
    clinics = get_clinics(location) if location else None

    # Get helplines
    helplines = get_helplines()

    return jsonify({
        "health_info": health_info,
        "clinics": clinics.get("results", []) if clinics else [],
        "helplines": helplines
    })

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
