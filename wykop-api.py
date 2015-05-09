__author__ = 'ubuntu'

import requests
import hashlib
import operator
from tabulate import tabulate
import configparser


def get_rank(name, ignored_words):
    all_messages = []
    for page_nr in range(1,30):
        try:
            url = get_url(name, page_nr)
            r = requests.get(url, headers = get_headers(url))
            if r.json()[0]['body']:
                for index in range(len(r.json())):
                    all_messages.append(r.json()[index]['body'])
        except IndexError:
            return filter_words(all_messages, ignored_words)
        except KeyError:
            print("You have probably reached API requests limit")

def get_url(name, page_nr):
    api_key = get_key()
    url = ("http://a.wykop.pl/profile/comments/" + str(name) + "/appkey," + api_key + "/" + "page," + str(page_nr)).encode('utf-8')
    return url

def get_headers(url):
    api_secret = get_secret().encode('utf-8')
    header = api_secret + url
    headers = {'apisign' : hashlib.md5(header).hexdigest()}
    return headers

def filter_words(message_list, ignored_words):
    words = {}
    for message in message_list:
        for word in remove_interpunction(message).split():
            if not is_trash(word.lower()) and not word.isdigit():
                if word.lower() not in ignored_words:
                    if word.lower() in words:
                        words[word.lower()] += 1
                    else:
                        words[word.lower()] = 1
    return sort_data(words)

def remove_interpunction(message):
    signs = ['.',',',':','/','-','<','>','\'','(',')',';']
    for sign in signs:
        if sign in message:
            message = message.replace(sign, "")
    return message

def is_trash(word):
    trash = ['href=', '@<a', '<br', '@a', 'br', '͡°']
    for item in trash:
        if item in word:
            return True
    return False

def sort_data(data):
    """sorts a dictionary by its values, returns a tuple with tuples"""
    sorted_data = sorted(data.items(), key=operator.itemgetter(1))
    return tuple(reversed(sorted_data))

def pack_data(data, number_to_print, name):
    """returns data in pretty table, user sets how many records are printed"""
    table = [["", name, ""],["Miejsce", "Słowo", "Liczba wystąpień"], ["-----", "--------", "----------------"]]
    for index, item in enumerate(data):
        if index < number_to_print:
            table.append([index+1, item[0], item[1]])
        else:
            break
    return tabulate(table)

def save_data(data, name):
    """saves data to file called by a name """
    file_name = name + '.txt'
    try:
        with open(file_name, 'a+') as file:
            file.write(data)
    except IOError:
        print("IOError!")

def get_key():
    """gets key from key.ini"""
    config = configparser.ConfigParser()
    config.read("key.ini")
    api_key = config["KEY"]["api_key"]
    return api_key

def get_secret():
    """gets key from key.ini"""
    config = configparser.ConfigParser()
    config.read("key.ini")
    api_secret = config["KEY"]["api_secret"]
    return api_secret

def main():
    ignored_words = ['w', 'i', 'o', 'a', 'nie', 'się', 'do', 'od', 'to', 'jest', 'z', 'ale', 'jestem', 'za', 'na', \
                     'po', 'że', 'tylko', 'mieć', 'być', 'co', 'już', 'żeby', 'ten', 'jak', 'bo', 'gdy', 'także', 'ze' \
                     'też', 'tej', 'aż', 'gdyż', 'nad', 'tego', 'które', 'który', 'więc', 'taki', 'taka', 'takiej' \
                     'którą', 'ze', 'tym', 'są', 'jest', 'będą', 'sa', 'by', 'są', 'byc', 'czy', 'być', 'sa', 'dla' \
                     'aby', 'ma', 'dla', 'przez', 'aby', 'bardzo']
    nicks = ['Marian_Kowalski', 'Pawel_Tanajno', 'Korwin-Mikke', 'Andrzej-Duda', 'Janusz-Palikot', 'Adam_Jarubas']
    for name in nicks:
        packed_data = pack_data(get_rank(name, ignored_words), 20, name)
        save_data(packed_data, name)

main()