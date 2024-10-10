import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Replace with your Typeform API token and form ID
api_token = os.getenv('TYPEFORM_API_TOKEN')
form_id   = os.getenv('TYPEFORM_FORM_ID')

# Typeform Responses API URL
url = f"https://api.typeform.com/forms/{form_id}/responses"
headers = {"Authorization": f"Bearer {api_token}"}
params = {"page_size": 100}

# Making the request to the Typeform API
response = requests.get(url, headers=headers, params=params)

# Checking if the request was successful
print(response.json())


