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

response = requests.get(f'https://api.typeform.com/forms/{FORM_ID}/responses')

print(response.json())