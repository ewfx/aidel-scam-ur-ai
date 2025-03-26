import requests
import json
from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def search_in_consolidated_sanctions(word):
    with open(r'consolidated_sanctions.txt', 'r') as fp:
        # read all lines using readline()
        found_lines=[]
        lines = fp.readlines()
        for row in lines:
            # check if string present on a current line
            #print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            if row.find(word) != -1:
                print('string exists in file')
                print('line Number:', lines.index(row))
                print(row)
                found_lines.append(row)
        return found_lines

def search_in_sanctions(word):
    with open(r'sanctions.txt', 'r') as fp:
        # read all lines using readline()
        lines = fp.readlines()
        found_lines=[]
        for row in lines:
            # check if string present on a current line
            #print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            if row.find(word) != -1:
                print('string exists in file')
                print('line Number:', lines.index(row))
                print(row)
                found_lines.append(row)
        return found_lines

def search_in_pep(word):
    with open(r'pep.txt', 'r') as fp:
        # read all lines using readline()
        found_lines=[]
        lines = fp.readlines()
        for row in lines:
            # check if string present on a current line
            #print(row.find(word))
            # find() method returns -1 if the value is not found,
            # if found it returns index of the first occurrence of the substring
            if row.find(word) != -1:
                print('string exists in file')
                print('line Number:', lines.index(row))
                print(row)
                found_lines.append(row)
        return found_lines

ofac_api_key=None
with open('creds.json', 'r') as file:
    data = json.load(file)
    ofac_api_key = data['OFAC_API_KEY']
def multi_search_in_api(words):
    url = "https://api.ofac-api.com/v4/search"
    headers = {"Content-Type": "application/json"}
    case_list=[]
    id_count=0
    for word in words:
        if isinstance(word, str):
            case_list.append({"name": word})
    print("Case List",case_list)
    data = {
        "apiKey": ofac_api_key,  # Replace with your actual API key
        "source": ["SDN", "EU","NONSDN","DPL","UN","OFSI","FSF","PEP","DFAT","FHFA","SAM","HUD","SEMA","BFS","SECO","MXSAT","LEIE","LFIU","FINCEN","INTERPOL","REPET","IL"],
        "cases": case_list  # Use the passed 'word' here
    }
    id_count+=1
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        response_dict=response.json()
        results=response_dict["results"]
        match_list=[]
        for result in results:
            if result["matchCount"]>0:
                matches=result["matches"]
                searched_term=result["name"]
                for match in matches:
                    source=match["source"]
                    match_name=match["name"]
                    similarity_score=similar(match_name,searched_term)
                    if (similarity_score>0.8):
                        match_list.append([searched_term,match_name,source,similarity_score])
        return match_list  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None  # Indicate API call failure
    except json.JSONDecodeError:
        print("API Response is not valid JSON")
        return None
def search_in_api(word):
    url = "https://api.ofac-api.com/v4/search"
    headers = {"Content-Type": "application/json"}
    data = {
        "apiKey": ofac_api_key,  # Replace with your actual API key
        "source": ["SDN", "EU","NONSDN","DPL","UN","OFSI","FSF","PEP","DFAT","FHFA","SAM","HUD","SEMA","BFS","SECO","MXSAT","LEIE","LFIU","FINCEN","INTERPOL","REPET","IL"],
        "cases": [{"name": word},{'name': 'Microsoft Online'}, {'name': 'Microsoft Operations'}, {'name': 'Microsoft Regional Sales'}, {'name': 'LinkedIn Ireland'}, {'name': 'Microsoft Japan'}, {'name': 'ZeniMax Media'}, {'name': 'Microsoft Switzerland'}, {'name': 'Microsoft Canada'}, {'name': 'Clipchamp Pty Ltd'}, {'name': 'Microsoft Morocco'}, {'name': 'Nuance Communications'}, {'name': 'Activision Blizzard'}, {'name': 'Redmond'}, {'name': 'Microsoft India R & D'}, {'name': 'Microsoft Production Studios'}, {'name': 'ProClarity'}, {'name': 'Microsoft Kids'}, {'name': 'Microsoft Egypt'}, {'name': 'Microsoft (Ukraine)'}, {'name': 'Microsoft Saudi'}, {'name': 'Softomotive'}, {'name': 'DreamWorks Interactive'}]  # Use the passed 'word' here
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return None  # Indicate API call failure
    except json.JSONDecodeError:
        print("API Response is not valid JSON")
        return None

def search_in_local_data(word):
    # Your alternative function logic here
    print(f"Local Data Search with: {word}")
    # Example: return some alternative data
    match_list=[]
    consolidated_sanction_result = search_in_consolidated_sanctions(word)
    sanction_result=search_in_sanctions(word)
    pep_result=search_in_pep(word)
    for result in consolidated_sanction_result:
        source="Consolidated Sanction"
        match_name=result
        similarity_score=similar(match_name,word)
        if (similarity_score>0.78):
            match_list.append([word,match_name,source,similarity_score])
    for result in sanction_result:
        source="Sanction"
        match_name=result
        similarity_score=similar(match_name,word)
        if (similarity_score>0.78):
            match_list.append([word,match_name,source,similarity_score])
    for result in pep_result:
        source="PEP"
        match_name=result
        similarity_score=similar(match_name,word)
        if (similarity_score>0.78):
            match_list.append([word,match_name,source,similarity_score])
    return match_list  # Return the JSON response

def process_search(word):
    api_result = search_in_api(word)

    if api_result:
        print("API call successful, using API results:")
        print(api_result)
        return api_result #return the result, so you can use it later.
    else:
        print("API call failed, using local data:")
        func1_result = search_in_local_data(word)
        print(func1_result)
        return func1_result #return the result, so you can use it later.

def multi_search(words):
    api_result = multi_search_in_api(words)

    if api_result:
        print("API call successful, using API results:")
        print(api_result)
        return api_result #return the result, so you can use it later.
    else:
        print("API call failed, using local data:")
        match_list=[]
        for word in words:
            if isinstance(word, str):
                match_list.extend(search_in_local_data(word))
        return match_list #return the result, so you can use it later.
def icij_search(word):
 
    url = "https://offshoreleaks.icij.org/api/v1/reconcile"
    headers = {"Content-Type": "application/json"}
    data = {
        "query": word,
        "type": "Node"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_dict=response.json()
        matches=response_dict["result"]
        match_list=[]
        for match in matches:
            match_name=match["name"]
            similarity_score=match["score"]
            description=match["description"]
            if (similarity_score>80):
                match_list.append([word,match_name,similarity_score,description])
        return match_list
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError:
        print("Response is not valid JSON")
        return None

def icij_multi_search(words):
    url = "https://offshoreleaks.icij.org/api/v1/reconcile"
    headers = {"Content-Type": "application/json"}
    queries_object={}
    id=0
    for word in words:
        if isinstance(word, str):
            queries_object["q"+str(id)]={"query":word}
            id+=1

    data = {
        "queries": queries_object,
        "type": "Node"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_dict=response.json()
        print(response_dict)
        query_keys=response_dict.keys()
        match_list=[]
        for key in query_keys:
            search_word=queries_object[key]["query"]
            matches=response_dict[key]["result"]
            for match in matches:
                match_name=match["name"]
                similarity_score=match["score"]
                description=match["description"]
                if (similarity_score>80):
                    match_list.append([search_word,match_name,similarity_score,description])
        return match_list
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError:
        print("Response is not valid JSON")
        return None
#print(icij_search("Mossack Fonseca Limited"))
# process_search("Adel Batterjee")
# process_search("Microsoft")
#multi_search(["Microsoft","Apple"])
#print(icij_multi_search(['Bill Gates', 'Paul Allen', 'Steve Ballmer', 'Satya Nadella', 'Reid Hoffman', 'Hugh Francis Johnston', 'Teri List', 'Penny Pritzker', 'Charlie Scharf', 'Arne Sorenson', 'John W. Stanton', 'John W. Thompson', 'Emma Walmsley', 'Padmasree Warrior', 'Charles Noski', 'Helmut Panke', 'Sandi Peterson', 'Carlos Rodriguez', 'Catherine MacGregor', 'Mark Mason', 'Microsoft', 'BlackRock', 'The Vanguard Group', 'Capital Group Companies', 'State Street Corporation', 'Microsoft TechNet', 'BigPark', 'Games for Windows', 'Microsoft Academic Search', 'Mojang Studios', 'Live Search', 'Windows Live Home', 'Microsoft Media Player', 'so.cl', 'MSN Groups', 'Cambria', 'Office Online', 'Windows Live Call', 'Windows Live Web Messenger', 'Havok', 'Bing News', 'Bing Webmaster Center', 'Ms. Dewey', 'MSN Games', 'Xamarin', 'Live Search Academic', 'Live Search Books', 'Microsoft Pinpoint', 'Hotmail', 'Microsoft Popfly', 'Revolution Analytics', 'Aces Studio', 'Bing Health', 'MSN Travel', 'Bing Videos', 'The Coalition', 'Channel 9', 'docs.com', 'Good Science Studio', 'MGS Mobile Gaming', 'MSN China', 'MSN Music', 'Massive Incorporated', 'Microsoft Update Catalog', 'System Center Advisor', 'Launchworks', 'Microsoft Vine', 'Xbox', 'Cortana', 'Press Play', 'Sway', '.bing', 'Microsoft Garage', 'Microsoft Translator', 'Xbox Entertainment Studios', '.NET My Services', 'Microsoft Academic', 'Microsoft s.r.o.', 'Columbia Data Center', 'Microsoft Casual Games', 'GitHub', 'Xbox Game Studios', 'Turn 10 Studios', 'Yammer', 'Microsoft Bing', 'Windows Media Player', 'MSN', 'LinkedIn', 'Outlook.com', 'Powerset', 'CodePlex', 'Skype Technologies', 'Corbel', 'Ensemble Studios', 'Ciao', 'Windows Live Admin Center', 'Hotmail Calendar', 'Digital Anvil', 'Windows Live', 'Microsoft Developer Network', 'Bing Maps', 'OneDrive', 'Windows Live Spaces', 'Microsoft PowerToys', 'OpenAI Global', 'Microsoft', 'Avanade', 'Microsoft Algeria', 'Lionhead Studios', 'Microsoft Mobile', 'Rare Ltd.', 'Microsoft Store', 'Danger, Inc.', 'Perceptive Pixel', 'GreenButton', 'Microsoft Research Asia', 'Sysinternals', 'Tellme Networks', 'Visio Corporation', 'aQuantive', 'Fast Search & Transfer', 'Razorfish', 'Microsoft Israel', 'Microsoft (United Kingdom)', 'Microsoft (Netherlands)', 'LinkedIn Corporation', 'Microsoft (France)', 'Microsoft Ireland Research', 'Microsoft Global Finance', 'Microsoft Ireland Operations', 'Microsoft Online', 'Microsoft Operations', 'Microsoft Regional Sales', 'LinkedIn Ireland', 'Microsoft Japan', 'ZeniMax Media', 'Microsoft Switzerland', 'Microsoft Canada', 'Clipchamp Pty Ltd', 'Microsoft Morocco', 'Nuance Communications', 'Activision Blizzard', None, 'Redmond', 'Microsoft India R & D', 'Microsoft Production Studios', 'ProClarity', 'Microsoft Kids', 'Microsoft Egypt', 'Microsoft (Ukraine)', 'Microsoft Saudi', 'Softomotive', 'DreamWorks Interactive']))
#search_in_api("Microsoft")
