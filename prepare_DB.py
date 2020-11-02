"""
This is a module for database processing
"""

import csv  # import package for working with database files
import string  # import package for working with strings
import os  # import the module to work with files


def is_float(value):
    """
    Function to check whether a value is a float type.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def prepare_file(file_input, file_output):
    """
    The function to clear the database of garbage and the selection of keys of interest.
    :param file_input:
    :param file_output:
    :return: return an array that consists of countries
    """
    # we open the file for reading; the key values are separated by commas
    reader = csv.DictReader(file_input, delimiter=',')
    # we create a vector of keys of interest
    columns = ['variety', 'country', 'province', 'winery', 'description', 'price']
    # open the second file to write
    writer = csv.writer(file_output, delimiter=',')
    # write the header
    writer.writerow(columns)
    # create an array of countries
    names = set()
    # for each key in each line, remove the garbage and write the processed line to a new file
    for line in reader:
        variety = ''.join(c for c in line['variety'] if c in string.ascii_letters or " ")
        country = ''.join(c for c in line['country'] if c in string.ascii_letters or " ")
        province = ''.join(c for c in line['province'] if c in string.ascii_letters or " ")
        winery = ''.join(c for c in line['winery'] if c in string.ascii_letters or " ")
        description = ''.join(c for c in line['description'] if c in string.ascii_letters or " ")
        # if the price is specified with an error, set the standard price
        if is_float(line['price']):
            price = float(line['price'])
        else:
            price = 100
        writer.writerow([variety, country, province, winery, description, price])
        # we are add new countries to the array
        names.add(country)
    return names


def change_similarities(file_input, file_output, names):
    """
    The function to change duplicates in the names of countries and provinces.
    :param file_input:
    :param file_output:
    :param names:
    :return:
    """
    # open the file for reading, the key values are separated by commas
    reader = csv.DictReader(file_input, delimiter=',')
    # create a vector of keys of interest
    columns = ["variety", "country", "province", "winery", "description", "price"]
    # open the second file to write
    writer = csv.DictWriter(file_output, delimiter=',', fieldnames=columns)
    # write the header
    writer.writeheader()
    # look for matches in the names of countries and provinces and change it
    for line in reader:
        if line["province"] in names:
            line["province"] = "None"
        writer.writerow(line)


if __name__ == "__main__":
    # open files and process them
    with open("wine_data.csv", 'r', errors='ignore') as f_in:
        with open("wine_data_h.csv", 'w', newline="") as f_out:
            varieties = prepare_file(f_in, f_out)
    with open("wine_data_h.csv", 'r', errors='ignore') as f_in:
        with open("wine_data_new.csv", 'w', newline="") as f_out:
            change_similarities(f_in, f_out, varieties)
    # delete auxiliary file
    os.remove("wine_data_h.csv")
