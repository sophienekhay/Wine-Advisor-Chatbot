"""
This is a module for finding wines that are similar in description.
"""


import wine_class as wn  # import wine class
import nltk  # import a platform for working with natural language
import csv  # import package for working with database files
# import Tf-idf vectorizer to convert a set of raw texts into a TF-IDF property matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity  # import module of Otiai coefficient


def is_float(value):
    """
    Function to check if a value is a type of float
    :param value:
    :return:
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def normalize(text):
    """
    Function to normalize tokens
    :param text:
    :return:
    """
    return [nltk.stem.WordNetLemmatizer().lemmatize(token) for token in nltk.word_tokenize(text)]


def find_similar(input_string, sentences):
    """
    Function to find a similar description for a user request
    :param input_string:
    :param sentences:
    :return:
    """
    # the initial data for the response
    response = ""
    # add the input into sentences
    sentences.append(input_string)
    # create vectorizer
    tokenizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')
    # convert sentences into vectors
    vector = tokenizer.fit_transform(sentences)
    # consider which offer is most similar to the description of the user
    values = cosine_similarity(vector[-1], vector)
    # looking for the index of the desired sentence
    idx = values.argsort()[0][-2]
    flat = values.flatten()
    flat.sort()
    req_vector = flat[-2]
    # if everything is fine, then we issue it at the output
    if req_vector == 0:
        response = "I couldn't find an appropriate wine."
        return response
    else:
        response = response + sentences[idx]
        return response


def find_description_wine(input_string, wine_in):
    """
    Function to search for wine by description.
    Submit a description of the user to enter and already known information about the wine.
    :param input_string:
    :param wine_in:
    :return:
    """
    # initial values for suitable descriptions
    descriptions = []
    wine_des = ""
    # read the file line by line
    with open("wine_data_new.csv", 'r+', errors='ignore') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            # for each line we create our own wine object
            wine = wn.Wine(line)
            # if the set of wine parameters known to us is contained in the set of wine parameters from the database
            if wine_in.is_sub(wine):
                # then we add it to the consideration
                descriptions.append(line["description"])
    # looking for a similar description of the user in the sample descriptions
    description = find_similar(input_string, descriptions)
    # looking for wine in the database according to the description and give it to the output
    with open("wine_data_new.csv", 'r+', errors='ignore') as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            if line["description"] == description:
                wine_des = wn.Wine(line)
    return wine_des


def find_price_wine(input_string):
    """
    This is a function to find the price in a line.
    :param input_string:
    :return:
    """
    # set the starting price
    price = [0, 2300]
    # if the line comes across the word "cheap", set the appropriate price range
    if input_string.find("cheap") != -1:
        price = [0, 20]
    # similar to the word "expensive"
    elif input_string.find("expensive") != -1:
        price = [100, 2300]
    # if you come across the word "cheaper", then look for the upper limit of the price
    elif input_string.find("cheaper") != -1:
        price_f = ''.join(c for c in input_string if c in "1234567890.")
        if is_float(price_f):
            price = [0, float(price_f)]
    # if the line has $, then it contains information about the price
    elif input_string.find("$") != -1 or input_string[-2] == "$":
        # replace "to" from the construction "from to", "and" from the construction "between and" and "-" with ";"
        prices = input_string.replace("-", ";")
        prices = prices.replace("to", ";")
        prices = prices.replace("and", ";")
        prices = ''.join(c for c in prices if c in "1234567890.;")
        # looking for the upper and lower price limits to the left and right of ";"
        if prices.find(";") != -1:
            # print(prices)
            price_s = prices[0:prices.rfind(";")]
            # clear the number of possible extra characters ";"
            price_s = ''.join(c for c in price_s if c in "1234567890.")
            price_f = prices[prices.rfind(";") + 1:len(prices)]
            if is_float(price_s) and is_float(price_f):
                price = [float(price_s), float(price_f)]
        # in other cases, we believe that the user has specified an exact price
        else:
            prices = ''.join(c for c in prices if c in "1234567890.")
            if is_float(prices):
                price = [float(prices), float(prices)]
    return price
