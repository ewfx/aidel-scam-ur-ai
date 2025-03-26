from wikidataflow1 import process_entity
from news_sentiment import get_sentiment_score
from sanctions_search import process_search,icij_search,search_in_local_data,multi_search,icij_multi_search

def search_entity_in_data_sources(entity_name):
    wikidata_response=process_entity(entity_name)
    entity_list=[]
    wikidata_text=''''''
    if not wikidata_response:
        wikidata_response={}
        wikidata_response['type']='NotFound'
        entity_list.append(entity_name)
        wikidata_text=wikidata_text+'''Wikidata does not have enough information to identify the entity'''+entity_name+'''. '''
    elif wikidata_response["type"]=="company":
        for people in wikidata_response["data"]["people"]:
            entity_list.append(people[0])
        entity_list.append(entity_name)
        entity_list.extend(wikidata_response["data"]["companies"])
        entity_list.extend(wikidata_response["data"]["other"])
        wikidata_text=wikidata_text+'''Wikidata identifies the entity'''+entity_name+''' as a company.'''
        if(len(wikidata_response["data"]["people"])>0):
            wikidata_text=wikidata_text+'''The company has the following people associated with it: '''
            for people in wikidata_response["data"]["people"]:
                wikidata_text=wikidata_text+people[0]
                if(people[1]>0.1):
                    wikidata_text+'''  who is a politically exposed person as per Wikidata, '''
                else:
                    wikidata_text+'''  who is not a politically exposed person as per Wikidata, '''
        if(len(wikidata_response["data"]["companies"])>0):
            wikidata_text=wikidata_text+'''The company has the following companies associated with it: '''
            for company in wikidata_response["data"]["companies"]:
                if(isinstance(company,str)):
                    wikidata_text=wikidata_text+company+''', '''
        if(len(wikidata_response["data"]["other"])>0):
            wikidata_text=wikidata_text+'''The company has the following other entities associated with it: '''
            for other in wikidata_response["data"]["other"]:
                wikidata_text=wikidata_text+other+''', '''
    elif wikidata_response["type"]=="person":
        entity_list.append(entity_name)
        wikidata_text=wikidata_text+'''Wikidata identifies the entity'''+entity_name+''' as a person.'''
        if(wikidata_response["data"]>0.1):
            wikidata_text=wikidata_text+'''The person is a politically exposed person as per Wikidata.'''
        else:
            wikidata_text=wikidata_text+'''The person is not a politically exposed person as per Wikidata.'''
    elif wikidata_response["type"]=="other":
        entity_list.append(entity_name)
        wikidata_text=wikidata_text+'''Wikidata identifies the entity'''+entity_name+''' as an other entity.'''
    else:
        entity_list.append(entity_name)
        wikidata_text=wikidata_text+'''Wikidata does not have enough information to identify the entity'''+entity_name+'''. '''
    #print("Entity List",entity_list)
    #print("Wikidata Response",wikidata_response)

    news_sentiment_text=''''''
    news_sentiment_score=get_sentiment_score(entity_name)
    if(not news_sentiment_score):
        news_sentiment_text='''No news articles were found for the entity'''+entity_name+'''. '''
    elif(news_sentiment_score==-1):
        news_sentiment_text='''No news articles were found for the entity'''+entity_name+'''. '''
    else:
        news_sentiment_text='''The average sentiment score pertaining to potential financial misdoings for the news articles related to the entity'''+entity_name+''' is '''+str(news_sentiment_score[0])+'''. '''
        news_sentiment_text=news_sentiment_text+'''And the combined summary of all parsed news articles is as follows: '''+news_sentiment_score[1]
    #print("News Sentiment Data",news_sentiment_score)

    search_result=multi_search(entity_list)
    #print("Sanction Search",search_result)

    sanction_search_text=''''''
    if(wikidata_response["type"]=="person"):
        if(len(search_result)>0):
            sanction_search_text='''The person'''+entity_name+''' was found in the following search results:'''
            for result in search_result:
                sanction_search_text=sanction_search_text+''' Matched with: '''+result[1]+''' from the source: '''+result[2]+''' with the similarity score: '''+str(result[3])+'''. \n'''
        else:
            sanction_search_text='''The person'''+entity_name+''' was not found in any of the sanction lists or PEP lists '''
    elif(wikidata_response["type"]=="company"):
        if(len(search_result)>0):
            sanction_search_text='''The company, its subsidiaries and the people associated '''+entity_name+''' were found in the following search results:'''
            for result in search_result:
                sanction_search_text=sanction_search_text+'''Searched Term:'''+search_result[0]+''' Matched with: '''+result[1]+''' from the source: '''+result[2]+''' with the similarity score: '''+str(result[3])+'''. \n'''
        else:
            sanction_search_text='''The company , its subsidiaries and the people associated '''+entity_name+''' was not found in any of the sanction lists or PEP lists '''
    else:
        if(len(search_result)>0):
            sanction_search_text='''The entity'''+entity_name+''' was found in the following search results:'''
            for result in search_result:
                sanction_search_text=sanction_search_text+''' Matched with: '''+result[1]+''' from the source: '''+result[2]+''' with the similarity score: '''+str(result[3])+'''. \n'''
        else:
            sanction_search_text='''The entity'''+entity_name+''' was not found in any of the sanction lists or PEP lists '''

    icij_search_result=icij_multi_search(entity_list)
    #print("ICIJ Search",icij_search_result)
    icij_search_text=''''''
    if(wikidata_response["type"]=="person"):
        if(len(icij_search_result)>0):
            icij_search_text='''The person'''+entity_name+''' was found in the following search results from ICIJ Leaks Data:'''
            for result in icij_search_result:
                icij_search_text=icij_search_text+''' Matched with: '''+result[1]+''' with the similarity score: '''+str(result[2])+''' with the reasoning being: '''+result[3]+'''. \n'''
        else:
            icij_search_text='''The person'''+entity_name+''' was not found in any of the ICIJ leaks '''
    elif(wikidata_response["type"]=="company"):
        if(len(icij_search_result)>0):
            icij_search_text='''The company, its subsidiaries and the people associated '''+entity_name+''' were found in the following search results from ICIJ Leaks Data:'''
            for result in icij_search_result:
                icij_search_text=icij_search_text+'''Searched Term: '''+result[0]+''' Matched with: '''+result[1]+''' with the similarity score: '''+str(result[2])+''' with the reasoning being: '''+result[3]+'''. \n'''
        else:
            icij_search_text='''The company , its subsidiaries and the people associated '''+entity_name+''' was not found in any of the ICIJ leaks '''
    else:
        if(len(icij_search_result)>0):
            icij_search_text='''The entity'''+entity_name+''' was found in the following search results from ICIJ Leaks Data:'''
            for result in icij_search_result:
                icij_search_text=icij_search_text+''' Matched with: '''+result[1]+''' with the similarity score: '''+str(result[2])+''' with the reasoning being: '''+result[3]+'''. \n'''
        else:
            icij_search_text='''The entity'''+entity_name+''' was not found in any of the ICIJ leaks '''
    
    full_analysis_text=''' For the entity'''+entity_name+''', the following information was found: \n Wikidata Results Summary:\n'''+wikidata_text+'''\n\n News Articles Summary:\n'''+news_sentiment_text+'''\n\n Sanction Search Summary: \n'''+sanction_search_text+'''\n\n ICIJ Leaks Database Search Summary:\n'''+icij_search_text
    return full_analysis_text

# print(search_entity_in_data_sources("Microsoft"))
