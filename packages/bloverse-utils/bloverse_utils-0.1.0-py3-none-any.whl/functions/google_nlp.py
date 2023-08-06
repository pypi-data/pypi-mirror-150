"""
These are functions that have to do with leveraging google services to carry out entity analysis
"""
## Add the root path so modules can be easily imported
import os
import sys
temp = os.path.dirname(os.path.abspath(__file__))
vals = temp.split('/')
BASE_DIR = '/'.join(vals[:-2])
BASE_DIR = '%s/' % BASE_DIR

# Add the root path to our python paths
sys.path.insert(0, BASE_DIR)

import os
from Config.settings import BASE_DIR
from blov_utils.functions import general as gen

from google.cloud import language_v1
import numpy as np
from nltk.tokenize import sent_tokenize

## You now need to work on the functionality to get the content text metadata
## Set google application credentials
google_service_key_path = os.path.join(BASE_DIR, 'general_input', 'service_keys', 'bloverse-image-staging-c4559b844a06.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=google_service_key_path

# This should go into the google nlp function
entity_type_list = ['Unknown', 'Person', 'Location', 'Organization', 'Event', 'Artwork', 'Consumer Product', 'Other', 'Phone Number', 'Address', 'Date', 'Number', 'Price']
accepted_entity_types = ['Person', 'Location', 'Organization', 'Event', 'Consumer Product', 'Artwork', 'Other']
relevant_entity_types = ['Person', 'Organization', 'Event', 'Consumer Product']

# get_google_text_entities_and_keywords(text, entity_type_list, accepted_entity_types, process_wiki)
def get_google_text_entities_and_keywords(text, entity_type_list, accepted_entity_types):
    """
    This function takes an input text and then passes it to the google to get relevant terms and information
    around them like their wikipedia links
    
    * We added a key name without '.' to make it easy to save to mongo, but the raw name is also captured
    """
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text,
        type_ = language_v1.Document.Type.PLAIN_TEXT)

    response = client.analyze_entities(document=document)

    # Process the term dict
    key_entity_dict = {}
    other_entity_dict = {}
    keyword_dict = {}
    top_entity_tags = []
    processed_wiki_urls = []
    
    for term in response.entities:
        try:
            # Get the term metadata
            name=term.name,
            name = name[0]
            
            # Clean up the term name
            name_words = name.split()
            words = [word.replace(".", "").strip() for word in name_words]
            key_name = ' '.join(words)
            
            # Get the term type
            term_type = entity_type_list[term.type_]

            salience=f"{term.salience:.1%}",
            salience = salience[0]
            relevance_score = float(salience.strip('%'))/100

            if relevance_score > 0:
                wikipedia_url=term.metadata.get("wikipedia_url", "-"),
                wikipedia_url = wikipedia_url[0]
                
                sentiment = term.sentiment
                sentiment_score = sentiment.score
                
                mentions_list = []
                for mention in term.mentions:
                    mention_text = mention.text.content
                    mentions_list.append(mention_text)
                new_relevance_score = round(relevance_score*len(mentions_list), 3)

                term_dict = {
                    'name' : key_name,
                    'type' : term_type,
                    'relevance_score' : relevance_score,
                    'new_relevance_score' : new_relevance_score,
                    'wiki_url' : wikipedia_url,
                    'sentiment_score' : sentiment_score,
                    'mentions' : mentions_list
                }
                
                temp_type = entity_type_list[term.type_]
                if temp_type == 'Other':
                    if len(wikipedia_url) > 1:
                        text_type = 'Entity'
                        if term_type in accepted_entity_types:
                            if len(wikipedia_url) > 1:
                                key_entity_dict.update({key_name:term_dict})
                            else:
                                other_entity_dict.update({key_name:term_dict})
                        else:
                            other_entity_dict.update({key_name:term_dict})
                    else:
                        text_type = 'Keyword'
                        keyword_dict.update({key_name:term_dict})
                else:
                    text_type = 'Entity'
                    if term_type in accepted_entity_types:
                        if len(wikipedia_url) > 1:
                            key_entity_dict.update({key_name:term_dict})
                        else:
                            other_entity_dict.update({key_name:term_dict})
                    else:
                        other_entity_dict.update({key_name:term_dict})
        except Exception as e:
            pass
    
    return key_entity_dict, other_entity_dict, keyword_dict


def get_google_text_categories(text):
    """Classify the input text into categories. """

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    results = response.categories
    
    category_dict = {}
    for category in results:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
#         category_dict[category.name] = category.confidence
        category_dict.update({category.name:category.confidence})

    return category_dict


def get_google_text_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    content_sentiment = float(response.document_sentiment.score)

    sentence_sentiment_dict = {}
    # Get sentiment for all sentences in the document
    sentence_list = []
    sentence_sentiment_list = []
    count = 1
    for sentence in response.sentences:
        sentence_name = 'sentence_%s' % count
        sentence_text = str(sentence.text.content)
        sentence_sentiment = float(sentence.sentiment.score)
        sentence_sentiment_dict.update({sentence_name:{'sentence_text':sentence_text, 'sentence_sentiment':sentence_sentiment}})
        count += 1
        
    return content_sentiment, sentence_sentiment_dict

"""
Processing text metadata
"""
def order_text_metadata_terms_by_relevance(text_metadata_dict):
    """
    This function takes text metadata terms and then sorts in order
    of the relevance and then returns the new dict
    """
    relevance_score_list = []
    dict_list = []
    for term in text_metadata_dict:
        term_dict = text_metadata_dict[term]
        rel_score = term_dict['new_relevance_score']
        relevance_score_list.append(rel_score)
        dict_list.append(term_dict)

    sorted_rel_score_indices, sorted_rel_score_list = gen.sort_list_and_return_sorted_indices(relevance_score_list)
    
    new_dict = {}
    for ind in sorted_rel_score_indices:
        term_dict = dict_list[ind]
        term = term_dict['name']
        new_dict.update({term:term_dict})
    
    return new_dict


def order_text_metadata_terms_by_num_mentions(text_metadata_dict):
    """
    This function takes text metadata terms and then sorts in order
    of the relevance and then returns the new dict
    """
    relevance_score_list = []
    dict_list = []
    for term in text_metadata_dict:
        term_dict = text_metadata_dict[term]
        rel_score = term_dict['new_relevance_score']
        relevance_score_list.append(rel_score)
        dict_list.append(term_dict)

    sorted_rel_score_indices, sorted_rel_score_list = gen.sort_list_and_return_sorted_indices(relevance_score_list)
    
    new_dict = {}
    for ind in sorted_rel_score_indices:
        term_dict = dict_list[ind]
        term = term_dict['name']
        new_dict.update({term:term_dict})
    
    return new_dict

def generate_content_signficant_and_top_terms(key_entity_dict, other_entity_dict, keyword_dict):
    """
    This function scours through the key, other and keyword dicts and then returns the significant terms as well as 
    """
    ## Now get the top 10 terms across the article... this is what we will use for filling out the headline sequence... more importantly it will also help with filtering out
    ## which articles to generate or not based on what the article is talking about
    relevant_key_term_count = 0
    relevance_score_list = []
    term_name_list = []
    term_type_list = []
    dict_name_list = []

    # key_entity_dict
    for term in key_entity_dict:
        term_dict = key_entity_dict[term]
        term_name = term_dict['name']
        term_type = term_dict['type']
        rel_score = term_dict['new_relevance_score']
        term_name_list.append(term_name)
        term_type_list.append(term_type)
        dict_name_list.append('Key')
        relevance_score_list.append(rel_score)
        relevant_key_term_count += 1

    # other_entity_dict
    for term in other_entity_dict:
        term_dict = other_entity_dict[term]
        term_name = term_dict['name']
        term_type = term_dict['type']
        rel_score = term_dict['new_relevance_score']
        term_name_list.append(term_name)
        term_type_list.append(term_type)
        dict_name_list.append('Other')
        relevance_score_list.append(rel_score)

    # keyword_dict
    for term in keyword_dict:
        term_dict = keyword_dict[term]
        term_name = term_dict['name']
        term_type = term_dict['type']
        rel_score = term_dict['new_relevance_score']
        term_name_list.append(term_name)
        term_type_list.append(term_type)
        dict_name_list.append('Keyword')
        relevance_score_list.append(rel_score)

    # Sort out the terms by the relevance score
    sorted_rel_score_indices, sorted_rel_score_list = gen.sort_list_and_return_sorted_indices(relevance_score_list)  

    ranked_term_dict = {}
    for ind in sorted_rel_score_indices:
        term_name = term_name_list[ind]
        term_type = term_type_list[ind]
        dict_type = dict_name_list[ind]

        if dict_type == 'Key':
            term_dict = key_entity_dict[term_name]
            term_mentions = term_dict['mentions']
            num_mentions = len(term_mentions)
            rel_score = term_dict['new_relevance_score']
            if rel_score > 0.001:
                term_dict['dict_type'] = dict_type
                term_dict['num_mentions'] = num_mentions
                ranked_term_dict.update({term_name:term_dict})
        elif dict_type == 'Other':
            term_dict = other_entity_dict[term_name]
            term_dict['dict_type'] = dict_type
            term_mentions = term_dict['mentions']
            num_mentions = len(term_mentions)
            rel_score = term_dict['new_relevance_score']
            if rel_score > 0.001:
                term_dict['dict_type'] = dict_type
                term_dict['num_mentions'] = num_mentions
                ranked_term_dict.update({term_name:term_dict})
        elif dict_type == 'Keyword':
            term_dict = keyword_dict[term_name]
            term_dict['dict_type'] = dict_type
            term_mentions = term_dict['mentions']
            num_mentions = len(term_mentions)
            rel_score = term_dict['new_relevance_score']
            if rel_score > 0.001:
                term_dict['dict_type'] = dict_type
                term_dict['num_mentions'] = num_mentions
                ranked_term_dict.update({term_name:term_dict})

    relevance_score_num_mentions_list = []
    num_mentions_list = []
    ranked_term_dict_list = []
    for term in ranked_term_dict:
        term_dict = ranked_term_dict[term]
        num_mentions = term_dict['num_mentions']
        relevance_score = term_dict['relevance_score']
        num_mentions_list.append(num_mentions)
        relevance_score_num_mentions_list.append([num_mentions, relevance_score])
        ranked_term_dict_list.append(term_dict)

    mentions_threshold = int(np.average(num_mentions_list)) + 1

    sorted_list = sorted(relevance_score_num_mentions_list, key=lambda x: (x[0], -x[1]), reverse=True)

    sorted_indices = []
    for i in range(len(sorted_list)):
        temp = sorted_list[i]
        ind = sorted_list.index(temp)
        if ind not in sorted_indices:
            pass
        else:
            ind = i
        sorted_indices.append(ind)

    significant_term_dict = {}
    for ind in sorted_indices:
        term_dict = ranked_term_dict_list[ind]
        term = term_dict['name']
        significant_term_dict.update({term:term_dict})

    # Get the top terms for the article... these are the ones that we will focus on
    content_top_key_terms = {}
    for term in significant_term_dict:
        term_dict = significant_term_dict[term]
        num_mentions = term_dict['num_mentions']
        dict_type = term_dict['dict_type']
        if num_mentions > mentions_threshold:
            if dict_type == 'Key':
                content_top_key_terms.update({term:term_dict})
                
    return significant_term_dict, content_top_key_terms

"""
Summarization
"""

def generate_sentence_score_based_on_google_text_metadata(sentence, significant_term_dict):
    """
    This function takes the significant term dict and the sentence and then calculate the sentence score and returns the 
    """
    significant_terms = list(set(significant_term_dict))

    sentence_tag_dict = {}
    processed_term_dicts = []
    sentence_score = 0
    relevant_entity_count = 0
    for term in significant_term_dict:
        term_dict = significant_term_dict[term]
        dict_type = term_dict['dict_type']
        entity_type = term_dict['type']
        mentions = term_dict['mentions']
        rel_score = term_dict['relevance_score'] # we use the normal relevance score instead of new one
        unique_mentions = list(set(mentions))
        for mention in unique_mentions:
            if mention in sentence:
                if term_dict not in processed_term_dicts:
                    sentence_score += rel_score
                    if dict_type == 'Key':
                        relevant_entity_count += 1
                        tag_dict = {
                            'tag_type': 'key_entity',
                            'entity_type' : entity_type
                        }
                    elif dict_type == 'Other':
                        tag_dict = {
                            'tag_type': 'key_entity',
                            'entity_type' : entity_type
                        }
                    else:
                        tag_dict = {
                            'tag_type': 'keyword',
                            'entity_type' : 'NA'
                        }
                    sentence_tag_dict.update({term:tag_dict})
                    processed_term_dicts.append(term_dict)
    return sentence_score, relevant_entity_count, sentence_tag_dict

def generate_content_summary(num_summary_sentences, content_body, significant_term_dict):
    """
    This function takes the content body and significant_term_dict from the google text metadata
    """
    article_sentences = sent_tokenize(content_body)

    sentence_score_list = []
    relevant_entity_count_list = []
    sentence_tag_dict_list = []

    # Pass each sentence in and calculate the sentence score and other necessary metrics
    for sentence in article_sentences:
        sentence_score, relevant_entity_count, sentence_tag_dict = generate_sentence_score_based_on_google_text_metadata(sentence, significant_term_dict)
        sentence_score_list.append(sentence_score)
        relevant_entity_count_list.append(relevant_entity_count)
        sentence_tag_dict_list.append(sentence_tag_dict)

    # Sort the sentences by the sentence score
    sorted_indices, sorted_list = gen.sort_list_and_return_sorted_indices(sentence_score_list)
    summary_inds = sorted_indices[0:num_summary_sentences]

    # Generate the summary dict
    article_summary_dict = {}
    for ind in summary_inds:
        sentence = article_sentences[ind]
        sentence_score = sentence_score_list[ind]
        relevant_entity_count = relevant_entity_count_list[ind]
        sentence_tag_dict = sentence_tag_dict_list[ind]
        article_summary_dict.update({sentence:sentence_tag_dict})
    
    return article_summary_dict

"""
Main Functions
"""

def get_article_text_metadata_from_google_nlp(content_body, num_summary_sentences):
    """
    This function takes in the content body for an article and the number of summary sentences that we want and generates the key google nlp txt metedata:
    - category
    - significant terms
    - summary
    """
    # Get the content categories
    content_category_dict = get_google_text_categories(content_body)

    # Get the entity metadata for the input content
    key_entity_dict, other_entity_dict, keyword_dict = get_google_text_entities_and_keywords(content_body, entity_type_list, accepted_entity_types)
    key_entity_dict = order_text_metadata_terms_by_relevance(key_entity_dict)
    other_entity_dict = order_text_metadata_terms_by_relevance(other_entity_dict)
    keyword_dict = order_text_metadata_terms_by_relevance(keyword_dict)

    # Process the terms and restructure to enable you better process and get the right images etc etc
    significant_term_dict, content_top_key_terms = generate_content_signficant_and_top_terms(key_entity_dict, other_entity_dict, keyword_dict)

    article_summary_dict = generate_content_summary(num_summary_sentences, content_body, significant_term_dict)

    return content_category_dict, content_top_key_terms, significant_term_dict, article_summary_dict

def get_article_media_relevance_from_google_metadata(significant_term_dict):
    """
    This function takes the significant_term_dict and then counts how many key terms (terms with wiki)
    and then gets a total score
    """
    num_article_key_terms = 0
    num_key_persons = 0
    total_key_term_relevance = 0
    for term in significant_term_dict:
        term_dict = significant_term_dict[term]
        term_type = term_dict['type']
        if term_type == 'Person':
            num_key_persons += 1
        dict_type = term_dict['dict_type']
        if dict_type == 'Key':
            num_article_key_terms += 1
            total_key_term_relevance += term_dict['new_relevance_score']

    return num_article_key_terms, num_key_persons, total_key_term_relevance