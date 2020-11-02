"""
This is a module to define the classes of wines
"""

import string  # import package for working with strings


def check_in(sentence, inputs):
    """
    Auxiliary function to check the presence of keywords in a sentence
    :param sentence:
    :param inputs:
    :return:
    """
    remove_punctuation = dict((ord(symbol), None) for symbol in string.punctuation)  # Removing punctuation marks
    for word in sentence.translate(remove_punctuation).split():
        if word.lower() in inputs:
            return word


class UserWine:
    """
    The class of wine that is created by the description of the user
    """

    def __init__(self, input_string, keys, price):
        """
        Function to create an object by user description
        :param input_string:
        :param keys:
        :param price:
        """
        self.variety = check_in(input_string, keys['variety'])
        self.country = check_in(input_string, keys['country'])
        self.province = check_in(input_string, keys['province'])
        self.winery = check_in(input_string, keys['winery'])
        self.price = price

    # Return an array of keys with non-empty values
    @property
    def nonempty_keys(self):
        keys = []
        if self.variety is not None:
            keys.append('variety')
        if self.country is not None:
            keys.append('country')
        if self.province is not None:
            keys.append('province')
        if self.winery is not None:
            keys.append('winery')
        if self.price[0] == self.price[1]:
            keys.append('price')
        return keys

    # Return an array of non-empty values
    @property
    def nonempty_values(self):
        keys = []
        if self.variety is not None:
            keys.append(self.variety.lower())
        if self.country is not None:
            keys.append(self.country.lower())
        if self.province is not None:
            keys.append(self.province.lower())
        if self.winery is not None:
            keys.append(self.winery.lower())
        return set(keys)

    def is_equal(self, wine):
        """
        Function to determine the equivalence of two wines
        :param wine:
        :return:
        """
        if self.nonempty_values == wine.nonempty_values and self.price == wine.price:
            return True
        else:
            return False

    def is_sub(self, wine):
        """
        Function to determine that the current wine fits the description of the specified
        :param wine:
        :return:
        """
        if self.nonempty_values <= wine.nonempty_values and self.price[0] <= wine.price <= self.price[1]:
            return True
        else:
            return False


class Wine(UserWine):
    """
    Wine class from database
    """

    def __init__(self, keys):
        """
        Load wine data from the database when creating an object
        :param keys:
        """
        keys_sub = {'variety': keys['variety'], 'country': keys['country'], 'province': keys['province'],
                    'winery': keys['winery']}
        UserWine.__init__(self, "", keys_sub, [0, 2300])
        self.variety = keys['variety']
        self.country = keys['country']
        self.province = keys['province']
        self.winery = keys['winery']
        self.price = float(keys['price'])
        self.description = keys['description']


class WineSet:
    """
    Class for a set of wines
    """

    def __init__(self, wines):
        """
        Creating a set from array of wines
        :param wines:
        """
        self.wines = wines
        self.amount = len(wines)

    def add(self, wine):
        """"
        Adding new wine to the set
        :param wine:
        :return:
        """
        self.wines.append(wine)
        self.amount += 1

    @property
    def return_names(self):
        """
        Returns a variety of wines in a set
        :return:
        """
        wine_names = set()
        for wine in self.wines:
            wine_names.add(wine.variety)
        return wine_names
