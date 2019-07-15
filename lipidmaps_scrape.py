import sys
import os
import requests
from bs4 import BeautifulSoup


#result = requests.get("https://www.lipidmaps.org/data/classification/LM_classification_exp.php")

#src = result.content
#soup = BeautifulSoup(src, 'lxml')
#links = soup.find_all("a")
#for link in links:
#    print(link)

#####  THIS GETS US THE WEBPAGE WITH A LINK TO THE THREE CATEGORIES (LIPID CATEGORY; STRUCTURE; AND GENE/PROTEIN)
print("LOOK BELOW 1" + '\n')
text = requests.get('https://www.lipidmaps.org/search/quicksearch.php?Name=' + 'acylglycerol')
print(text.headers)
src = text.content
soup = BeautifulSoup(src, 'lxml')
#print(soup.prettify())
#print("LOOK ABOVE")

#####  THIS GETS US TO THE WEBPAGE WITH THE LIPID CATEGORY/CLASS/SUBCLASS
print("LOOK BELOW 2" + '\n')
text = requests.get('https://www.lipidmaps.org/data/structure/ClassFuzzySearch.php?Name=' + 'ACYLGLYCEROL' + '&s=' + 'acylglycerol')
print(text.headers)
src = text.content
soup = BeautifulSoup(src, 'lxml')
#print(soup.prettify())
#print("LOOK ABOVE")

#####  THIS GETS US TO TEH WEBPAGE WITH THE LMSD: STRUCTURE BASED SEARCH RESULTS
print("LOOK BELOW 3" + '\n')
text = requests.get('https://www.lipidmaps.org/data/structure/LMSDFuzzySearch.php?Name=' + 'ACYLGLYCEROL' + '&s=' + 'acylglycerol' + '&SortResultsBy=Name')
print(text.headers)
src = text.content
soup = BeautifulSoup(src, 'lxml')
#print(soup.prettify())
#print("LOOK ABOVE")

#####  THIS GETS US TO THE WEBPAGE WITH THE LIPID MAPS GENE/PROTEIN DATABASE
print("LOOK BELOW 4" + '\n')
text = requests.get('https://www.lipidmaps.org/data/structure/LMPDFuzzySearch.php?Name=' + 'ACYLGLYCEROL' + '&s=' + 'acylglycerol')
print(text.headers)
src = text.content
soup = BeautifulSoup(src, 'lxml')
#print(soup.prettify())
#print("LOOK ABOVE")


#features="lxml"
#soup = BeautifulSoup(text, 'lxml')

#links = soup.find_all('a')

#for link in links:
#    if "MGI" in link.text:
#        print(link.text)
#        MGI = link.text
#print(MGI + " here ya go")