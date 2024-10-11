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
params = {"page_size": 1000}  # Aumentado para obter mais respostas

# Configuração do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

def get_typeform_responses():
    url = f"https://api.typeform.com/forms/{FORM_ID}/responses"
    headers = {
        "Authorization": f"Bearer {TYPEFORM_API_TOKEN}"
    }
    params = {
        "page_size": 1000,
        "completed": "true"
    }

    responses = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        responses.extend(data['items'])
        
        if data['page_count'] == data['total_items']:
            break
        
        params['before'] = data['items'][-1]['submitted_at']

    return responses

def process_responses(responses):
    processed_data = []
    for resp in responses:
        if resp is not None and 'answers' in resp and resp['answers'] is not None:
            row = {
                'response_id': resp['response_id'],
                'submitted_at': resp['submitted_at']
            }
            for answer in resp['answers']:
                question_id = answer['field']['id']
                question_type = answer['type']
                
                if question_type in ['text', 'number', 'date']:
                    row[question_id] = answer[question_type]
                elif question_type == 'choice':
                    row[question_id] = answer['choice']['label']
                elif question_type == 'choices':
                    row[question_id] = ', '.join([choice['label'] for choice in answer['choices']['labels']])
            
            processed_data.append(row)
    
    return pd.DataFrame(processed_data)

try:
    # Obtém as respostas do Typeform
    responses = get_typeform_responses()

    # Processa as respostas em um DataFrame
    df = process_responses(responses)

    # Salva o DataFrame no banco de dados
    df.to_sql('typeform', engine, if_exists='replace', index=False)

    print("As respostas foram salvas no banco de dados.")

except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
except KeyError as e:
    print(f"Erro ao acessar dados da resposta: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
