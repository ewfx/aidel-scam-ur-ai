from entityextraction import extractNames,data_source_analysis
from entity import search_entity_in_data_sources
import google.generativeai as genai
import json
gemini_api_key=None
with open('creds.json', 'r') as file:
    data = json.load(file)
    gemini_api_key= data['GEMINI_API_KEY']
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

rag_analysis = '''
For the entity: OSNEFT OIL COMPANY, the following information was found: 
 Wikidata Results Summary:
Wikidata does not have enough information to identify the entity: OSNEFT OIL COMPANY. 

 News Articles Summary:
No news articles were found for the entity: OSNEFT OIL COMPANY. 

 Sanction Search Summary: 
The entity: OSNEFT OIL COMPANY was not found in any of the sanction lists or PEP lists 

 ICIJ Leaks Database Search Summary:
No search results were found for the entity: OSNEFT OIL COMPANY in the ICIJ leaks database. 



 For the entity: YAKIMA OIL TRADING, the following information was found: 
 Wikidata Results Summary:
Wikidata does not have enough information to identify the entity: YAKIMA OIL TRADING. 

 News Articles Summary:
No news articles were found for the entity: YAKIMA OIL TRADING. 

 Sanction Search Summary: 
The entity: YAKIMA OIL TRADING was found in the following search results: Matched with: YAKIMA OIL TRADING, LLP from the source: SDN with the similarity score: 0.8780487804878049. 


 ICIJ Leaks Database Search Summary:
The entity: YAKIMA OIL TRADING was found in the following search results from ICIJ Leaks Data: Matched with: YAKIMA TRADING CORP. with the similarity score: 84.21052631578947 with the reasoning being: Entity node extracted from the Paradise Papers - Barbados corporate registry data.. 
 Matched with: YAKIMA TRADING CORP with the similarity score: 84.21052631578947 with the reasoning being: Officer node extracted from the Pandora Papers - Trident Trust data.. 




 For the entity: LLP, the following information was found: 
 Wikidata Results Summary:
Wikidata identifies the entity: LLP as an other entity.

 News Articles Summary:
The average sentiment score pertaining to potential financial misdoings for the news articles related to the entityLLP is 0.19. And the combined summary of all parsed news articles is as follows: The provided excerpt is far too short and lacks any information related to financial matters. It mentions a band forming a limited entity, which is a common and legitimate business practice. There is absolutely no evidence, or even suggestion, of any financial misdoings based on the content given.The news article mentions an arrest warrant being issued for a senior member of Lighthouse, a life-coaching group. While the article excerpt doesn't explicitly detail the reason for the arrest warrant, the context provided (the subject of a BBC podcast series) suggests potential wrongdoing. The lack of specific financial accusations prevents a higher score, but the warrant itself indicates serious concerns, potentially including financial crimes such as fraud or embezzlement, given the nature of such organizations. Further information is needed to confirm specific financial misdeeds.The provided text snippet describes a membership requirement for a website. There is absolutely no indication of any financial misdoings, scandals, fraud, embezzlement, money laundering, or bribery. The snippet simply states that users need to be a member to comment or favorite content, and provides a link to explore membership options.Based solely on the provided excerpt, there is no indication of financial scandals, fraud, embezzlement, money laundering, bribery, or other financial misdoings. The article describes a lawsuit filed by Perkins Coie against the Trump administration, alleging that an executive order is unconstitutional and retaliatory. This legal action focuses on constitutional and potentially political issues, but it does not inherently suggest any financial impropriety by either party.The news article states that Leon Black transferred $170 million to Jeffrey Epstein's accounts. While the article doesn't explicitly accuse Black of a crime, large financial transactions with a known sex offender like Epstein raise serious red flags. These transactions could potentially be related to money laundering, bribery (e.g., paying for silence or influence), or other illicit activities, depending on the specific nature and intent of the transfers. The lack of context necessitates a high but not definitive risk score. Further investigation is required to determine the legality and ethical implications of these financial transactions.The article describes President Trump signing an executive order suspending security clearances of Mark Pomerantz and individuals at Paul, Weiss, Rifkind, Wharton & Garrison. While the suspension of security clearances could be related to an investigation into potential financial misdoings, the article does not provide direct evidence of financial scandals, fraud, embezzlement, money laundering, or bribery. Mark Pomerantz was involved in the investigation of the Trump Organization, so this executive order may be retaliation for this investigation. A potential conflict of interest or obstruction of justice could have a financial element, but without further details, the risk score is relatively low, representing a possible but unconfirmed connection to financial impropriety.The provided article snippet is too brief to definitively identify financial misdoings. However, some phrases raise potential red flags that warrant further investigation, justifying a low but non-zero score. For instance, the rapid growth "from an unknown startup to a pivotal AI force within the legal industry in three years" *could* be indicative of aggressive accounting practices, inflated valuations, or unsustainable business models. The mention of "CEO Winston Weinb" with the text truncated may potentially refer to something negative, or it may have nothing to do with financial misdoings. It's important to note that rapid growth in itself is not illegal or unethical. Further investigation is needed to determine if any actual wrongdoing occurred, but the speed of expansion and the text truncation introduce a hint of risk.The article mentions a lawyer resigning from a law firm (Skadden) due to the firm's inaction regarding Trump. While this suggests potential ethical concerns related to political influence and potentially questionable legal work performed by the firm under pressure from the Trump administration, it doesn't directly indicate financial scandals, fraud, embezzlement, money laundering, or bribery. The connection is indirect and speculative. However, the possibility of the firm prioritizing political considerations over ethical legal practices *could* lead to future financial misdeeds. Therefore, I assign a low score of 0.1 to reflect the indirect nature of the potential risk.The news article describes a legal dispute regarding an onstage kiss at a Malaysian festival. The judge's decision to spare the members of the 1975 from individual liability does not indicate any financial misdoings, fraud, embezzlement, money laundering, or bribery. The article appears to relate to freedom of expression and cultural norms rather than financial malfeasance. Therefore, the risk of financial scandal is assessed as extremely low.The news article discusses a ruling that members of The 1975 are not personally liable for financial losses incurred by a festival. While the festival may have suffered financial losses, the article does not present any evidence of financial scandals, fraud, embezzlement, money laundering, bribery, or other financial misdoings. The lawsuit seems to be about liability for losses, not criminal financial activity.

 Sanction Search Summary: 
The entity: LLP was not found in any of the sanction lists or PEP lists 

 ICIJ Leaks Database Search Summary:
No search results were found for the entity: LLP in the ICIJ leaks database. 



 For the entity: Ali Hussein Falih Al-Mansoori, the following information was found: 
 Wikidata Results Summary:
Wikidata does not have enough information to identify the entity: Ali Hussein Falih Al-Mansoori. 

 News Articles Summary:
No news articles were found for the entity: Ali Hussein Falih Al-Mansoori. 

 Sanction Search Summary: 
The entity: Ali Hussein Falih Al-Mansoori was found in the following search results: Matched with: Ali Hussein Falih Al-Mansoori
 from the source: Consolidated Sanction with the similarity score: 0.9830508474576272. 


 ICIJ Leaks Database Search Summary:
No search results were found for the entity: Ali Hussein Falih Al-Mansoori in the ICIJ leaks database. 



 For the entity: Lasca Holding Ltd, the following information was found: 
 Wikidata Results Summary:
Wikidata does not have enough information to identify the entity: Lasca Holding Ltd. 

 News Articles Summary:
No news articles were found for the entity: Lasca Holding Ltd. 

 Sanction Search Summary: 
The entity: Lasca Holding Ltd was not found in any of the sanction lists or PEP lists 

 ICIJ Leaks Database Search Summary:
The entity: Lasca Holding Ltd was found in the following search results from ICIJ Leaks Data: Matched with: LASCA  HOLDING LTD with the similarity score: 100.0 with the reasoning being: Entity node extracted from the Paradise Papers - Malta corporate registry data.. 
 Matched with: LASCA HOLDING LTD with the similarity score: 100.0 with the reasoning being: Officer node extracted from the Paradise Papers - Malta corporate registry data.. 




 For the entity: NordVP, the following information was found: 
 Wikidata Results Summary:
Wikidata identifies the entity: NordVP as a company.The company has the following companies associated with it: Groupe Nord, 

 News Articles Summary:
No news articles were found for the entity: NordVP. 

 Sanction Search Summary: 
The company , its subsidiaries and the people associated NordVP was not found in any of the sanction lists or PEP lists 

 ICIJ Leaks Database Search Summary:
No search results were found for the entity: NordVP in the ICIJ leaks database.
'''

transaction_data = '''
Transaction ID: TXN-2023-5A9B
Date: 2023-08-15 14:22:00
Sender:
  -Name: 'Rosneft Oil Company'
  -Account: IBAN CH56 0483 5012 3456 7800 9 (Swiss bank)
  -Address: Rue du Marche 17, Geneva, Switzerland
  -Notes: 'Consulting fees for project Aurora'
Receiver:
  -Name: 'YAKIMA OIL TRADING, LLP'
  -Account: 987654321 (Cayman National Bank, KY)
  -Address: P.O. Box 1234, George Town, Cayman Islands
  -Tax ID: KY-45678
Amount: $49,850 (USD)
Currency Exchange: N/A
Transaction Type: Wire Transfer
Reference: 'Charitable Donation - Ref #DR-2023-0815
Additional Notes:
  - Urgent transfer approved by Mr. Ali Hussein Falih Al-Mansoori (Director)
  - Linked invoice missing. Processed via intermediary Lasca Holding Ltd
  - Sender IP: 192.168.89.123 (VPN detected: NordVPN, exit node in Panama)
 '''


def generateFinalOutput(transaction_data, rag_analysis):
    """
    Generates final output for unstructured data
    """
    prompt = f"""
    You are an AI expert tasked with analyzing the risk for a given transaction and entities involved.
    Given a transaction data and risk analysis summary fetched from data sources, generate a final report summarizing the risk assessment for the transaction and entities involved.
    You may flag transactions involving a huge amount, approved by or involving PEPs, or with suspicious entities as high-risk transactions by giving them a high risk score.
    If the transaction involves entities with a history of financial scandals, fraud, embezzlement, money laundering, bribery, or other financial misdoings, assign a high risk score.
    Transaction Data: {transaction_data}
    Risk Analysis Summary: {rag_analysis}
    Provide a final risk assessment for the transaction and entities involved, along with a textual explanation.
    Output format: JSON string with the following fields: Transaction id, Extracted entity, Entity type, Risk score, Supporting evidence, Confidence score, Reason.
    eg:
    {{
        "Transaction ID": "TXN-2023-7C2D",
        "Extracted Entity": ["Quantum Holdings Ltd", "Golden Sands Trading FZE", "Viktor Petrov"],
        "Entity Type": ["Shell Company", "Corporation", "Sanctioned Individual"],
        "Risk Score": 0.98,
        "Supporting Evidence": ["BVI Registry", "OFAC SDN List"],
        "Confidence Score": 0.96,
        "Reason": "Sender is a shell company; Viktor Petrov is a blocked individual under OFAC SDN #9876."
    }}
    """
    retries = 3  # Number of retry attempts
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            text = response.candidates[0].content.parts[0].text.strip()
            start_index = text.find('{')
            end_index = text.rfind('}') + 1 # +1 to include the closing curly brace
            json_string = text[start_index:end_index]
            data = json.loads(json_string)
            return data
        except Exception as e:
            if attempt < retries - 1:
                continue  # Retry on failure
            return f"Error generating output after {retries} attempts: {e}"
        
def process_transaction(transaction_data):
    rag_analysis=data_source_analysis(transaction_data)
    return generateFinalOutput(transaction_data, rag_analysis)
