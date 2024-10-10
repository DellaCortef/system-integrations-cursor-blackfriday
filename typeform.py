import requests

# Replace with your Typeform API token and form ID
api_token = "API_TOKEN"

# Typeform Responses API URL
url = f"https://api.typeform.com/forms/{form_id}/responses"
headers = {"Authorization": f"Bearer {api_token}"}
params = {"page_size": 100}

# Making the request to the Typeform API
response = requests.get(url, headers=headers, params=params)