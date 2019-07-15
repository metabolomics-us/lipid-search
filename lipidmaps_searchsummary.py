import sys
import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

query = input("Type compound of interest:   ")

#####  THIS GETS US TO THE WEBPAGE WITH THE LIPID CATEGORY/CLASS/SUBCLASS

def class_search(quest):
    upper = quest.upper()
    lower = quest.lower()
    text = requests.get('https://www.lipidmaps.org/data/structure/ClassFuzzySearch.php?Name=' + upper + '&s=' + lower)
    src = text.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

def counting(stew, quest, count):
    for table_tag in stew.find_all("table"):
        for a in table_tag.find_all('a'):
            thing = a.text
            count += 1
        query_dic.update({quest : count})
    return query_dic

def new_searches(stoup, seq_query):
    for table_tag in stoup.find_all("table"):
        for a in table_tag.find_all("a"):
            thing = a.text
            space = thing.find(" ")
            next_query = (thing[: space])
            seq_query.append(next_query)
    return seq_query


soup = class_search(query)

count = 0
query_dic = {}
dictionary = counting(soup, query, count)
second_query = []
second_query = new_searches(soup, second_query)


for i in second_query:
    if i in dictionary:
        continue
    else:
        soup = class_search(i)
        count = 0
        second_dictionary = counting(soup, i, count)


print('-------------------------------------------------------------------')
print('{:<60} {:<15}'.format('Compound','Count'))
print('-------------------------------------------------------------------')
for k, v in second_dictionary.items():
    print('{:<60} {:<15}'.format(k, v))
print('-------------------------------------------------------------------')