"""
These are for general funcitons that we seem to use across multiple places
"""
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from datetime import date, datetime

def get_string_similarity_score(string_a, string_b):
    """
    This function takes two strings and returns their similarity score
    """
    return SequenceMatcher(None, string_a, string_b).ratio()

def remove_stopwords_from_text(input_text):
    """
    This function takes an input text and then filters out stopwords from the text and returns input string without stop words
    """
    word_list = input_text.split()
    filtered_words = [word for word in word_list if word.lower() not in stopwords.words('english')]
    
    filtered_string = ' '.join(filtered_words)
    
    return filtered_string

def sort_list_and_return_sorted_indices(input_list):
    """
    This function takes in a python list, and then returns the sorted list as well as its sorted indices
    """
    sorted_indices = [i[0] for i in sorted(enumerate(input_list), key=lambda x:x[1], reverse=True)]
    sorted_list = sorted(input_list)
    return sorted_indices, sorted_list

def sum_up_dict_list(dict_list): # should go to utils
    """
    This function takes a list of dictionaries with values as int or float and then sums up across the keys in the dicts
    in the list
    """
    sum_dict = {}
    for myDict in dict_list:
        for key, value in myDict.items():
            sum_dict.setdefault(key, 0)
            sum_dict[key] += value
    
    return sum_dict

def normalise_dict_values(input_dict): # should go to utils
    """
    This function takes in an input dictionary that consists of values that are numbers, and then normalises the values
    so that they add up to 1 (i think this is the l2 norm)
    """
    total = sum(input_dict.values())

    norm_dict = {}
    for term in input_dict:
        curr_val = input_dict[term]
        norm_val = round(curr_val/total, 2)
        norm_dict.update({term:norm_val})

    return norm_dict

def calculate_num_days_between_two_dates(date_1, date_2):
    """
    This function gets the number of days between two dates
    """
    # Break the date town into y, m , d
    date_1_year = int(date_1[0:4])
    date_1_month = int(date_1[5:7])
    date_1_day = int(date_1[8:10])

    date_2_year = int(date_2[0:4])
    date_2_month = int(date_2[5:7])
    date_2_day = int(date_2[8:10])

    # Get the difference between the two dates
    f_date = date(date_1_year, date_1_month, date_1_day)
    l_date = date(date_2_year, date_2_month, date_2_day)
    delta = l_date - f_date
    num_days_diff = abs(delta.days)
    
    return num_days_diff