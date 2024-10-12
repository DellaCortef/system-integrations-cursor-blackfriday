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

    for resp in responses:
        formatted_resp = {
            'response_id': resp['response_id'],
            'submitted_at': resp['submitted_at']
        }

        # Adding the answers to the response
        for answer in resp['answers']:
            question_id = answer['field']['id']
            question_type = answer['type']

            if question_type in ['text', 'number', 'date']:
                formatted_resp[question_id] = answer[question_type]
            elif question_type == 'choice':
                formatted_resp[question_id] = answer['choice']['label']
            elif question_type == 'choices':
                formatted_resp[question_id] = ', '.join([choice['label'] for choice in answer['choices']['labels']])
        
        formatted_responses.append(formatted_resp)

    # Create a DataFrame from the formatted responses
    df = pd.DataFrame(formatted_responses)

    # Save the DataFrame to a CSV file
    csv_filename = 'typeform_responses.csv'
    df.to_csv(csv_filename, index=False)

    print(f"CSV file '{csv_filename}' has been created successfully.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
    print(response.json())  # Print the error details   
