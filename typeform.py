import requests

# Replace with your Typeform API token and form ID
api_token = "API_TOKEN"
form_id   = "FORM_ID"

# Typeform Responses API URL
url = f"https://api.typeform.com/forms/{form_id}/responses"
headers = {"Authorization": f"Bearer {api_token}"}
params = {"page_size": 100}

# Making the request to the Typeform API
response = requests.get(url, headers=headers, params=params)

# Checking if the request was successful
print(response.json())


