"""
This is a chatbot of recommendatory type to help in the selection of wines.
"""

import csv  # import package for working with database files
import random  # import package for random phrases selection
import warnings  # import package to turn off alerts
import wine_class as wn
import search_wine as sw


"""
This is the main code of a program.
"""


warnings.filterwarnings('ignore')  # to disable warnings
bot_name = "Wine adviser: "  # to determine the name of the bot
limit = 10  # to set a limit for displaying the number of different wines on the screen
KEYS = ['variety', 'country', 'province', 'winery', 'description', 'price']  # array of keys
# Different sets of inputs and responses
GREETING_INPUTS = ('hello', 'hi', 'greetings', 'hey', 'afternoon')
BYE_INPUTS = ('thanks', 'thank', 'bye', 'bye-bye', 'bb', 'arividerchi')
NO_INPUTS = ('no', 'nope', 'none', 'not', 'return')
GREETING_RESPONSES = ('Hi', 'Hey', 'Good afternoon', 'Hello')
BYE_RESPONSES = ('Bye! You are welcome.', 'Have a nice day.', 'You are welcome.')
COUNTRY_INPUTS = ('country', 'state', 'government')
PROVINCE_INPUTS = ('province', 'region', 'area')
WINERY_INPUTS = ('winery', 'factory')
VARIETY_INPUTS = ('variety', 'name', 'sort', 'grade', 'class')
DESCRIPTION_INPUTS = ('description', 'specification', 'taste')
PRICE_INPUTS = ('price', 'cost', 'value', 'rate')
PRICES_KEYS = ('cheap', 'expensive', 'cheaper')

# To set the initial data for the keys
varieties = set()
countries = set()
provinces = set()
wineries = set()
dif = KEYS.copy()
# To fill a arrays of keys
with open("wine_data_new.csv", 'r+', errors='ignore') as f:
    reader = csv.DictReader(f, delimiter=',')
    for line in reader:
        varieties.add(line['variety'].lower())
        countries.add(line['country'].lower())
        provinces.add(line['province'].lower())
        wineries.add(line['winery'].lower())
key_words = {'variety': varieties, 'country': countries, 'province': provinces, 'winery': wineries}
# Initial data for list of wines and wine for search
offered_wine = wn.UserWine("", key_words, [0, 2300])
clarify_wine = wn.UserWine("", key_words, [0, 2300])
offers = wn.WineSet([])

# This is a short welcome speech of bot
print(bot_name + "My name is %s. I could help you with choosing a wine. Please ask your question." % bot_name[0:-2])

"""
This is a conversation with the user.
"""


while True:
    # To read the answer and translate the text in lower case
    user_response = input().lower()
    # These are the answers to the greetings and the final replicas of the user
    if wn.check_in(user_response, GREETING_INPUTS) is not None:
        print(bot_name + random.choice(GREETING_RESPONSES))
    elif wn.check_in(user_response, BYE_INPUTS) is not None:
        print(bot_name + random.choice(BYE_RESPONSES))
        break
    # If the appropriate wine was not found, then we start the search from the beginning. We are reset the data.
    elif wn.check_in(user_response, NO_INPUTS) is not None:
        print(bot_name + "Okay. Let's start once again. Please tell me what are you looking for?")
        dif = KEYS.copy()
        offers = wn.WineSet([])
        offered_wine = wn.UserWine("", key_words, [0, 2300])
    else:
        # If we find a suitable wine, we offer the user information about it
        if offers.amount == 1:
            if wn.check_in(user_response, VARIETY_INPUTS) is not None:
                print(bot_name + "This wine variety is %s." % offered_wine.variety)
            if wn.check_in(user_response, COUNTRY_INPUTS) is not None:
                print(bot_name + "This wine is produced in %s" % offered_wine.country)
            if wn.check_in(user_response, PROVINCE_INPUTS) is not None:
                print(bot_name + "This wine is produced in %s" % offered_wine.country + ", " + offered_wine.province)
            if wn.check_in(user_response, WINERY_INPUTS) is not None:
                print(bot_name + "This wine is produced in %s" % offered_wine.winery)
            if wn.check_in(user_response, DESCRIPTION_INPUTS) is not None:
                print(bot_name + offered_wine.description)
            if wn.check_in(user_response, PRICE_INPUTS) is not None:
                print(bot_name + "It costs %s$" % offered_wine.price)
            print(bot_name + "If you have any other questions please ask me.")
        # otherwise, we are looking for a suitable wine in the database
        else:
            # to add old wine information to new request
            user_response += " " + " ".join(offered_wine.nonempty_values)
            # if the price is not specified in the request, then add the old price to the request
            if sw.find_price_wine(user_response) == [0, 2300]:
                user_response += " " + str(offered_wine.price[0]) + "to" + str(offered_wine.price[1]) + "$"
            # to create a new wine object with new updated information
            clarify_wine = wn.UserWine(user_response, key_words, sw.find_price_wine(user_response))
            # if new key values have appeared
            if not offered_wine.is_equal(clarify_wine):
                # we change the parameters of the proposed wine
                offered_wine = wn.UserWine(user_response, key_words, sw.find_price_wine(user_response))
                # we are looking for an entity in the database that fits the new description
                with open("wine_data_new.csv", 'r+', errors='ignore') as f:
                    reader = csv.DictReader(f, delimiter=',')
                    for line in reader:
                        # for each line we create our own wine object
                        wine = wn.Wine(line)
                        # if it satisfies the user's requests, then add it to the list
                        if offered_wine.is_sub(wine):
                                offers.add(wine)
                    # if the number of sentences is greater than 0
                    if offers.amount > 0:
                        #  remove the keys whose values we already know
                        for k in offered_wine.nonempty_keys:
                            if k in dif:
                                dif.remove(k)
                        # if the number of offers exceeds the limit, we invite the user to give us more information
                        if offers.amount > limit:
                            print(bot_name + "There are %s different offers found for you request. You can specify"
                                             " your request by indication of " % offers.amount + ", ".join(dif))
                            offers = wn.WineSet([])
                        # otherwise we create a list of wines
                        else:
                            # if there is more than one wine in the list, we offer the user a choice
                            if len(offers.return_names) > 1:
                                print(bot_name + "I could offer you the following wines: " +
                                      ", ".join(offers.return_names) + ". What wine are you interested in?")
                            # if there is only one wine in the list, the conversation continues about it
                            else:
                                offered_wine = random.choice(offers.wines)
                                print(bot_name+"It seems to me that you are looking %s. I can tell you about its "
                                      % offered_wine.variety + ", ".join(dif) + ". What do you want to know?")
                                offers = wn.WineSet([offered_wine])
                    # if nothing suitable is found, then reset the data and repeat the search again
                    else:
                        print(bot_name + "Unfortunately I couldn't found any appropriate offers for you. "
                                         "Please repeat your request.")
                        dif = KEYS.copy()
                        offers = wn.WineSet([])
                        offered_wine = wn.UserWine("", key_words, [0, 2300])
            # if there are no new values of keys, then we are looking for wine by description
            else:
                # it takes a little longer, so ask the user to wait
                print(bot_name + "Please wait. Your request is being processed...")
                # we are looking for wine by description
                offered_wine = sw.find_description_wine(user_response, offered_wine)
                dif = KEYS.copy()
                dif.remove('variety')
                # we inform the user about it
                print(bot_name + "It seems to me that you are looking for %s. I can tell you about its "
                      % offered_wine.variety + ", ".join(dif) + ". What do you want to know?")
                offers = wn.WineSet([offered_wine])
