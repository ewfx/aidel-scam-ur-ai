import requests
import json

def get_wikidata_qid_from_search(search_term):
    """Searches Wikidata and returns the top QID."""

    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={search_term}&format=json&language=en" #Added language parameter

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["search"]:
            return data["search"][0]["id"]  # Return the top QID
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
def identify_by_qid(qid):

    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        entity = data["entities"][qid]
        if "claims" in entity and "P31" in entity["claims"]:
            instance_of = entity["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]
            print(instance_of)
            if instance_of == "Q5":  # Human
                return "person", qid
            elif "P112" in entity["claims"] or "P3320" in entity["claims"] or "P127" in entity["claims"] or "P159" in entity["claims"] or "P1830" in entity["claims"] or "P355" in entity["claims"]:  # Company
                return "company", qid
            else:
                return "other", qid # Or handle differently.
        else:
            return "unknown", qid # Or handle differently.

    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"
def identify_entity_type(entity_name):
    """Identifies if an entity is a person or company using Wikidata."""

    qid = get_wikidata_qid_from_search(entity_name) #using the function from before.
    if not qid:
        return None, "Entity not found on Wikidata."

    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        entity = data["entities"][qid]
        if "claims" in entity and "P31" in entity["claims"]:
            instance_of = entity["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"]
            print(instance_of)
            if instance_of == "Q5":  # Human
                return "person", qid
            elif "P112" in entity["claims"] or "P3320" in entity["claims"] or "P127" in entity["claims"] or "P159" in entity["claims"] or "P1830" in entity["claims"] or "P355" in entity["claims"]:  # Company
                return "company", qid
            else:
                return "other", qid # Or handle differently.
        else:
            return "unknown", qid # Or handle differently.

    except requests.exceptions.RequestException as e:
        return None, f"Error: {e}"

#example usage
def calculate_pep_score(pep_indicators):
    if "P102" in pep_indicators.keys() and "P3602" in pep_indicators.keys():
        return 1.0
    elif "P102" in pep_indicators.keys() or "P3602" in pep_indicators.keys():
        return 0.5
    else:
        return 0.0
def analyze_person_for_pep(qid):
    """Analyzes a person's Wikidata page for PEP indicators."""

    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        entity = data["entities"][qid]
        pep_indicators = {}
        properties = ["P106", "P101", "P102", "P3602", "P39"] #properties to check.
        for prop in properties:
            if "claims" in entity and prop in entity["claims"]:
                pep_indicators[prop] = [claim["mainsnak"]["datavalue"]["value"]["id"] for claim in entity["claims"][prop]]
        return calculate_pep_score(pep_indicators)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

#example usage, using the QID from the previous function.
def analyze_company_for_connections(qid):
    """Analyzes a company's Wikidata page for connected entities."""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        entity = data["entities"][qid]
        connections = {}
        properties = ["P112", "P169", "P3320", "P127", "P159", "P1830", "P355"]
        for prop in properties:
            if "claims" in entity and prop in entity["claims"]:
                connections[prop] = [claim["mainsnak"]["datavalue"]["value"]["id"] for claim in entity["claims"][prop]]
        return connections
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_wikidata_title(qid, language="en"):
    """Retrieves the title (label) of a Wikidata entity given its QID."""
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json&languages={language}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "entities" in data and qid in data["entities"]:
            entity = data["entities"][qid]
            if "labels" in entity and language in entity["labels"]:
                return entity["labels"][language]["value"]
            else:
                return None  # Label not found for the specified language
        else:
            return None  # Entity not found
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
def process_company_info(data):
    property_map={"P112": "founded by",
    "P169": "ceo" ,
    "P3320": "boardmember",
    "P127": "owned by",
    "P159": "headquarters",
    "P1830": "owner of" ,
    "P355": "has subsidiary"
    }
    entity_list=[]
    for key, value in data.items():
        if key in property_map.keys():
            for entity in value:
                if entity not in entity_list:
                    entity_list.append(entity)
    people_list=[]
    company_list=[]
    other_list=[]
    for entity in entity_list:
        entity_type, qid = identify_by_qid(entity)
        if entity_type == "person":
            people_list.append([get_wikidata_title(entity),analyze_person_for_pep(entity)])
        elif entity_type == "company":
            company_list.append(get_wikidata_title(entity))
        elif entity_type == "other":
            other_list.append(get_wikidata_title(entity))
    return {"people": people_list,"companies":company_list,"other":other_list}



#example usage, using the QID from the first function.
# if entity_type == "company" and qid:
#     company_data = analyze_company_for_connections(qid)
#     print(company_data)
# if entity_type == "person" and qid:
#     pep_data = analyze_person_for_pep(qid)
#     print(pep_data)

# entity_name = "Joe Biden"
# entity_type, qid = identify_entity_type(entity_name)
# print(f"Entity type: {entity_type}, QID: {qid}")
# print(analyze_person_for_pep("Q6279"))

def process_entity(entity_name):
    entity_type, qid = identify_entity_type(entity_name)
    if entity_type == "company" and qid:
        company_data = analyze_company_for_connections(qid)
        return {"type":"company","data":process_company_info(company_data)}
    if entity_type == "person" and qid:
        pep_data = analyze_person_for_pep(qid)
        return {"type":"person","data":pep_data}
    if entity_type == "other" and qid:
        # Gemini call
        return {"type":"other","data":get_wikidata_title(qid)}
    else:
        return None

