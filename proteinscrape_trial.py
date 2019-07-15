import sys
import os
import requests
from bs4 import BeautifulSoup


text = requests.get('http://www.uniprot.org/uniprot/' + 'Q9D880').text
features="lxml"
soup = BeautifulSoup(text, 'lxml')

links = soup.find_all('a')

for link in links:                               ##  search through the list of links to find all the links with the word "About"
    if "MGI" in link.text:                     ##  turning it into a list allows us to use the .text function (find thing in text of link)
#        print(link.text)
        MGI = link.text
print(MGI + " here ya go")