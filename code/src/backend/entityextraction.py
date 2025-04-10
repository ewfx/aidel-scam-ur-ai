# Description: Extracts entities from transaction text.



import google.generativeai as genai
import json
from entity import search_entity_in_data_sources
gemini_api_key=None
with open('creds.json', 'r') as file:
    data = json.load(file)
    gemini_api_key= data['GEMINI_API_KEY']
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def extractNames(transaction_data):
    """
    Extracts names from the text.
    """
    prompt = f"""Extract all named entities (e.g., names of individuals, organizations and parties involved) from the following transaction data. You must definitely include all the names of the entities involved in the transaction which might be further needed for risk analysis.
    Transaction data: {transaction_data}
    Provide the entities as a comma-separated list: [entity1, entity2, entity3, ...]"""
    retries = 3  # Number of retry attempts
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.candidates[0].content.parts[0].text.strip()
            return list(map(str.strip, text[1:-1].split(',')))
        except Exception as e:
            if attempt < retries - 1:
                continue  # Retry on failure
            return f"Error extracting entities after {retries} attempts: {e}"


def data_source_analysis(transaction_data):
    entities = extractNames(transaction_data)
    print(entities)
    if(len(entities)==0):
        return "No entities found in the transaction data."
    optext = ""
    for entity in entities:
        if(entity and (len(entity)>0)):
            optext += search_entity_in_data_sources(entity) + "\n\n"
    return optext


