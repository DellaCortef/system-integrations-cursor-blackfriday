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
params = {"page_size": 100}  # Aumentado para obter mais respostas

# Making the Typeform API request
response = requests.get(url, headers=headers, params=params)

# Verifying the response status
if response.status_code == 200:
    # Obtaining request data
    data = response.json()

    # Extracting the answers
    responses = data['items']

    # Creates a list to store formatted data
    formatted_responses = []

    for resp in responses:
        formatted_resp = {
            'submitted_at': resp['submitted_at'],
            'response_id': resp['response_id']
        }

        # Add answers to each question
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

    # Creates a DataFrame with formatted responses
    df = pd.DataFrame(formatted_responses)

    # Configuring the connection to the PostgreSQL Database
    db_url = os.getenv('DATABASE_URL')
    engine = create_engine(db_url)

    # Stores the DataFrame in the Database 'typeform_responses' table
    df.to_sql(name='typeform_responses', con=engine, if_exists='append', index=False)

    print('Data saved successfully in PostgreSQL!')
else:
    print(f"Error: {response.status_code}")