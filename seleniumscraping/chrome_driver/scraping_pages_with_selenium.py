import os
import csv
from selenium import webdriver
from helpers.pathfinder import get_current_dir


# Code to Scrap information from a Web page, and then save it to a CSV file for
# after processing or later use. Using Chrome driver for Google Chrome on
# Windows (Win 10 x64)

# Author : Jose Gabriel Kordahi Amair
# This Code Use the webdriver from selenium Package to open/scrap a desire
# chunk of information from a Web page.
# The Web Driver can be downloaed from the oficial web page:
# https://sites.google.com/a/chromium.org/chromedriver/downloads


# GLOBAL VARIABLES
# Pages to dive in
MAX_PAGE_NUM = 5
# number digits allowed for the URL
MAX_PAGE_DIG = 3
# URL to scrap information of
BASE_URL = "http://econpy.pythonanywhere.com/ex/"
# CSV file file names
CSV_FILE_NAME = '\\results-chrome.csv'

# Creates the results folder if it does not exists.
if not os.path.isdir(os.getcwd() + '\\results'):
    os.mkdir('results')

# CSV Path to save the file
CSV_PATH = get_current_dir() + "\\results"


def get_csv_len(file_path, file_name):

    """
    Get the len of the CSV file
    :param file_path: Path to the file_name file
    :param file_name: file name of the
    :return: returns the len of the csv file
    """

    try:

        input_file = open(file_path + file_name, "r+")

        reader_file = csv.reader(input_file)
        value = len(list(reader_file))

        if value-1 == 0:
            print('Empty CSV File')
        # print('{} Records in the file'.format(value-1))
        return value

    except Exception as err:

        print('Error retreiving csv len file: ', err)
        return 0


def initialize_csv(file_path, file_name):

    """
    Initilialize the CSV file if it does not exists.
    :param file_name: name of the file to create
    """

    try:
        # Get CSV file lenght
        value = get_csv_len(file_path, file_name)

        if value <= 0:

            print('Creating new CSV file name {}'.format(file_name))
            with open(file_path + file_name, 'w') as f:
                f.write("Buyers, Price \n")

    except Exception as err:

        print('File Error: ', err)


def open_chrome_webdriver():

    """
    This Function Instantiates a new web driver
    :return: A chrome web Driver isntance or error
    """

    try:
        print('Initializing web driver')
        return webdriver.Chrome()
    except Exception as err:
        print('Error Opening the Driver: ', err)
        return None


def close_chrome_webdriver(driver):

    """
    Close an instantiated webdriver
    :param driver: Driver Instance
    :return:
    """

    try:
        driver.close()
        print('Web driver closed')
        return '0'
    except Exception as err:
        print('Error Closing the Driver: ', err)
        return '-1'


def save_to_csv(file_path, file_name, buyers, prices):

    """
    Saves new data to CSV file.
    :param file_name: The name of the file to Open and save the records
    :param buyers: a List with the buyers data (names)
    :param prices: a List with the prices of the Buyers
    :return: excecution code report error
    """

    try:

        old_recods = get_csv_len(file_path, file_name)
        print('{} old records on file'.format(old_recods-1))

        if len(buyers) != len(prices):
            print('Error Saving on File, no data consistency to save')
            print('Number of Buyers rows: {} '.format(len(buyers)),
                  'NUmber of Prices rows: {} '.format(len(prices)))
            print('{} Not equal to {}'.format(len(buyers), len(prices)))
            return '-1'

        else:

            with open(file_path + file_name, 'a') as f:
                for i in range(len(buyers)):
                    # f.write(buyers[i].text + "," + prices[i].text + '\n')
                    f.write(buyers[i] + "," + prices[i] + '\n')

        len_file = get_csv_len(file_path, file_name)

        added = len_file - old_recods

        if len(buyers) != added:

            print('CSV file data integrity compromised')
            print('{} new records added'.format(added))
            print('{} records on file'.format(len_file-1))
            return '-2'

        else:
            print('{} new records added'.format(added))
            print('{} records on file'.format(len_file-1))
            return '0'

    # Too Wide Exception
    except Exception as err:
        print('Error trying to open/write on csv file: ', err)


def single_url_build(inter, base_url, page_num, page_dig):

    """
    This function generates a string with a new URL due some supplied criteria
    :param inter: string word to add to the url
    :param base_url: string word to add to the url
    :param page_num: max number page that will be supplied
    :param page_dig: max number of digits for page number supplied
    :return: a string with the url built
    """

    # due to the i iteration, the page number is created
    # Page digit = 3 - 2 * times '0' | '0' + '12'
    page_num_url = (page_dig - len(str(inter))) * '0' + str(inter)
    # Create the URL string
    url = base_url + page_num_url + ".html"

    return url


def multi_url_build(base_url, page_num, page_dig):

    """
    This function builds a list of links built one by one using a certain
    criteria
    :param base_url: string world with the base for the url build
    :param page_num: max number page that will be supplied
    :param page_dig: max number of digits for page number supplied
    :return: a list with the built urls
    """

    link_list = []

    for i in range(1, page_num + 1):

        link_list.append(single_url_build(i, base_url, page_num, page_dig))

    print('{} links were built'.format(len(link_list)))
    return link_list


def scrap_single_url(url, driver, *conditions):

    """
    Function to Scrap a single URL and retrive its desired values
    :param url: URL to Scrap
    :param driver: Instance of Web Driver (chrome Web driver)
    :return: two lists of buyers and prices if both list hava the same lenghts
    """

    # List of conditions for Xpath to Search
    if len(conditions) == 0:
        pass

    try:
        # Open and get URL information
        driver.get(url)

        # Scrap the HTML to search for Desired Conditions
        buyers = driver\
            .find_elements_by_xpath('//div[@title="buyer-name"]')
        prices = driver\
            .find_elements_by_xpath('//span[@class="item-price"]')

        ret_buyers = []
        ret_prices = []

        for i in range(0, len(buyers)):

            ret_buyers.append(buyers[i].text)
            ret_prices.append(prices[i].text)

        # Valid values
        if len(buyers) == len(prices):
            return ret_buyers, ret_prices
        else:
            return [], []

    except Exception as err:
        print('Error Trying to opening the URL:', url, ' Wrong Request')
        print(err)
        # Empty lists
        return [], []


def multi_scrap(link_list, driver):

    """
    This function collect all the information generated by scraping each url
    and returns it as a list for post-processing the data and save it.
    :param link_list: a list with the links to scrap information
    :param driver: the instance of the web driver
    :return: two lists with the information retrieve from web scrapping the
            provided links
    """

    if link_list:

        if isinstance(link_list, list):

            # Aux List Vars
            buyers = []
            prices = []

            for link in link_list:
                # Unpack values from new list and add elements to existing list
                b, p = scrap_single_url(link, driver, None)
                buyers += [*b]
                prices += [*p]

            return buyers, prices

        # If only one link(string) is generated
        elif isinstance(link_list, str):

            return scrap_single_url(link_list, driver, None)

    else:
        print('No links where generated')


# Main Program
if __name__ == '__main__':

    driver = open_chrome_webdriver()
    initialize_csv(CSV_PATH, CSV_FILE_NAME)
    link_list = multi_url_build(BASE_URL, MAX_PAGE_NUM, MAX_PAGE_DIG)
    buyers, prices = multi_scrap(link_list, driver)
    save_to_csv(CSV_PATH, CSV_FILE_NAME, buyers, prices)
    close_chrome_webdriver(driver)
