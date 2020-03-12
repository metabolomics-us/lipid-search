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
    text = requests.get('http://cgsc2.biology.yale.edu/Mutation.php?ID=5430')
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