import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Replace with your Typeform API token and form ID
TYPEFORM_API_TOKEN = os.getenv('TYPEFORM_API_TOKEN')
FORM_ID = os.getenv('TYPEFORM_FORM_ID')

# Typeform Responses API URL
url = f"https://api.typeform.com/forms/{FORM_ID}/responses"
headers = {"Authorization": f"Bearer {TYPEFORM_API_TOKEN}"}
params = {"page_size": 100}  # Augmented for more responses

response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Obtain the data from the responses
    data = response.json()

    # Extract the responses from the data
    responses = data['items']

    # Creating a list to store the responses
    formatted_responses = []

    
