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
params = {"page_size": 1000}  # Aumentado para obter mais respostas

try:
    # Making the request to the Typeform API
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raises an HTTPError for bad responses

    # Gets the response data
    data = response.json()
    
    # Extract the answers
    responses = data['items']
    
    # Creates a list to store formatted data
    formatted_responses = []
    
    for resp in responses:
        if resp is not None and 'answers' in resp and resp['answers'] is not None:
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
        else:
            print("No answers found in the response")
    
    # Creates a DataFrame with formatted responses
    df = pd.DataFrame(formatted_responses)
    
    # Saves the DataFrame to a CSV file
    csv_filename = 'typeform_responses.csv'
    df.to_csv(csv_filename, index=False)
    
    print(f"As respostas foram salvas em '{csv_filename}'")
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
except KeyError as e:
    print(f"Erro ao acessar dados da resposta: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")