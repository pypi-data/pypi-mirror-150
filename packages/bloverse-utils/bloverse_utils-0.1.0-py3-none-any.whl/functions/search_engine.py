"""
These are all the functions that require us to query a search engine to get information for the purposes of the
extraction service.... we may have something similar for the videoclip service, but no point forcing them into one
"""
import requests
import spacy
nlp = spacy.load('en_core_web_sm')

from Config.settings import value_serp_api_key

def get_search_term_from_noun_chunks(input_text):
    """
    This function takes in an input term or phrase, and then strips it down to the bare minimum
    by focusing on the noun chunks
    """
    chunk_list = []

    doc =nlp(input_text)

    accepted_pos = ['PROPN', 'NOUN']
    for token in doc:
        if token.pos_ in accepted_pos:
            chunk_list.append(token.text)

    for np in doc.noun_chunks:
        if len(np.text) > 0:
            if np.text not in chunk_list:
                chunk_list.append(np.text)

    # Now get the search term by aligning an ordered list of the noun chunks and tokens            
    ordered_chunks = []

    for token in doc:
        if token.text in chunk_list:
            ordered_chunks.append(token.text)

    search_term = ' '.join(ordered_chunks)
    
    return search_term


def get_google_result_links_for_search_term_valueserp(search_term, value_serp_api_key, web_domain = None):
    """
    This function uses valueserp to get the google result news links for an input search_term
    """
    if web_domain is None:
        # set up the request parameters
        params = {
          'api_key': value_serp_api_key,
          'q': search_term,
          'num' : 50
        }
    else:
        search_term = '%s site:%s' %(search_term, web_domain)
        params = {
          'api_key': value_serp_api_key,
          'q': search_term,
          'num' : 50
        }
        
    # make the http GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)
    output = api_result.json()
        
    return output


def get_google_result_news_links_for_search_term_valueserp_by_pagination(search_term, value_serp_api_key, num_results, page):
    """
    This function uses valueserp to get the google result news links for an input search_term
    """

    # set up the request parameters
    params = {
      'api_key': value_serp_api_key,
      'search_type': 'news',
      'q': search_term,
      'num' : num_results,
      'page' : page
    }
        
    # make the http GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)
    output = api_result.json()
        
    return output


def get_google_result_news_links_for_search_term_valueserp(search_term, value_serp_api_key, web_domain = None):
    """
    This function uses valueserp to get the google result news links for an input search_term
    """
    if web_domain is None:
        # set up the request parameters
        params = {
          'api_key': value_serp_api_key,
          'search_type': 'news',
          'q': search_term,
          'num' : 100,
        }
    else:
        search_term = '%s site:%s' %(search_term, web_domain)
        params = {
          'api_key': value_serp_api_key,
          'search_type': 'news',
          'q': search_term,
          'num' : 100,
        }
        
    # make the http GET request to VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params)
    output = api_result.json()
        
    return output


def get_article_url_from_article_tweet_text(tweet_text, value_serp_api_key, brand_domain_url):
    """
    This function takes in the tweet text of a suspected article tweet and then searches twitter to see
    if we are able to find 
    """
    output = get_google_result_news_links_for_search_term_valueserp(tweet_text, value_serp_api_key, brand_domain_url)
    try:
        news_results = output['news_results']
        top_match = news_results[0]
        article_title = top_match['title']

        # Compare the titles for similarity
        doc1 = nlp(tweet_text)
        doc2 = nlp(article_title)
        similar = doc1.similarity(doc2)

        if similar > 0.8:
            article_url = top_match['link']
        else:
            article_url = 'NA'
    except:
        article_url = 'NA'
    
    return article_url


def get_total_google_results_for_search_term(search_term, value_serp_api_key):
    """
    This function takes in a search term, then does a google search and returns the number of hits 
    """
    # set up the request parameters
    params = {
      'api_key': value_serp_api_key,
      'q': search_term,
      'num' : 50
    }

    api_result = requests.get('https://api.valueserp.com/search', params)
    output = api_result.json()

    num_hits = output['search_information']['total_results']
    
    return num_hits