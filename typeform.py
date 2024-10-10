import requests

# forms_id from our Typeform account
forms_id = "qHJL1W2j"

# API request
response = requests.get(f"https://api.typeform.com/forms/{forms_id}/responses")

# print API response
print(response.json())