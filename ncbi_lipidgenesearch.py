import sys
import os
import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

#query = input("Type compound of interest:   ")
query = "acylglycerol"

#####  THIS GETS US TO THE WEBPAGE WITH THE LIPID CATEGORY/CLASS/SUBCLASS

def class_search(quest):
    upper = quest.upper()
    lower = quest.lower()
    text = requests.get('https://www.ncbi.nlm.nih.gov/gene/?term=' + lower)
    src = text.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

### displays the number of results NCBI found
#def counting(stew, quest, count):
#    for table_tag in stew.find_all("table"):
#        for a in table_tag.find_all('a'):
#            thing = a.text
#            count += 1
#        query_dic.update({quest : count})
#    return query_dic


### get the genes, function, and species from first page of NCBI gene search
def ncbi_genesearch(stoup):
    genes = []
    for table_tag in stoup.find_all("table"):
        for a in table_tag.find_all("a"):
            thing = a.text
            upper_thing = thing.upper()
            if upper_thing not in genes:
                genes.append(upper_thing)
                print(upper_thing)
        td_list = []
        for td_tag in table_tag.find_all('td'):
            td_list.append(td_tag)
        description = (td_list[1])
        function = str(description).split("<td>")[-1].split("[<em>")[0]
        specie = str(description).split("[<em>")[-1].split("</em>")[0]
        #print(function)
        #print(specie)
        #print("---")
    print(len(genes))


### TAKE TWO - CONSIDER SPECIE: get the genes, function, and species from first page of NCBI gene search
def HUMANncbi_genesearch(stoup):
    genes = []
    td_list = []
    for table_tag in stoup.find_all("table"):
        for tr_tag in table_tag.find_all("tr"):
            #print(tr_tag.find(class = "gene-id"))
            for td_tag in tr_tag.find_all('td'):
                td_list.append(td_tag)
            if len(td_list) == 0:
                continue
            else:
                description1 = (td_list[1])                       ####  DIFFERENT FOR DIFFERENT ENTRIES!!!  NEED TO FIX
            if "(human)" not in str(description1):
                continue
            else:
                for span in tr_tag.find("span"):
                    print(span)
                    #gene_id = span
                    #print(gene_id)
                for a in tr_tag.find("a"):
                    thing = a
                    upper_thing = thing.upper()
                    name = ("-" + upper_thing + "-")
                    if name not in genes:
                        genes.append(name)
                        print(name)
                        function = str(description1).split("<td>")[-1].split("[<em>")[0]               ###  NEED TO FIX
                        specie = str(description1).split("[<em>")[-1].split("</em>")[0]
                        #print(function)
                        #print(specie)
                        td_list = []
    print(len(genes))








soup = class_search(query)
ncbi_genesearch(soup)
print("---------------------------------------------")
HUMANncbi_genesearch(soup)



#print('-------------------------------------------------------------------')
#print('{:<60} {:<15}'.format('Compound','Count'))
#print('-------------------------------------------------------------------')
#for k, v in second_dictionary.items():
#    print('{:<60} {:<15}'.format(k, v))
#print('-------------------------------------------------------------------')