import google.generativeai as genai
import json
gemini_api_key=None
with open('creds.json', 'r') as file:
    data = json.load(file)
    gemini_api_key= data['GEMINI_API_KEY']
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def analyze_financial_risk(article_text):
    """Analyzes a news article for financial scandals and assigns a risk score."""

    prompt = f"""
    Analyze the following news article for signs of financial scandals, fraud, embezzlement, money laundering, bribery, or other financial misdoings. Do not include financial losses or poor financial performance.

    Article: {article_text}

    Provide a financial risk score from 0 to 1, where 0 means no evidence of financial misdoings and 1 means strong evidence of financial scandals.

    Also provide a textual explanation for the score.

    Output the result as a json object with the following fields:
    "score" : numerical value between 0 and 1,
    "explanation" : textual explanation of the score.
    """

    try:
        response = model.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text
        start_index = text.find('{')
        end_index = text.rfind('}') + 1 # +1 to include the closing curly brace
        json_string = text[start_index:end_index]
        data = json.loads(json_string)
        # Assuming the LLM returns json in the response.
        return data
    except Exception as e:
        return {"score": -1, "explanation": f"Error analyzing article: {e}"}

