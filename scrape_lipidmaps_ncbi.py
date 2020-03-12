import sys
import os
import datetime
import requests
from bs4 import BeautifulSoup


#query = input("Type compound of interest:   ")
query = "monoacylglycerol"
#email = input("Provide email (needed for NCBI search):  ")
email = "sgreenfield@ucdavis.udu"

currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))

if query.endswith("s"):
    query = query[-1]

#####  LIPIDMAPS_SEARCHSUMMARY.PY

def class_search(quest):
    upper = quest.upper()
    lower = quest.lower()
    text = requests.get('https://www.lipidmaps.org/data/structure/ClassFuzzySearch.php?Name=' + upper + '&s=' + lower)
    src = text.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

def counting(stew, quest, count):
    lst = []
    for table_tag in stew.find_all("table"):
        for a in table_tag.find_all('a'):
            thing = a.text
            count += 1
        lst.append(count)
        query_dic.update({quest : lst})
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
    i = i.lower()
    if i.endswith('s'):
        i = i[:-1]
    if i in dictionary:
        continue
    else:
        soup = class_search(i)
        count = 0
        second_dictionary = counting(soup, i, count)

print("LipidMaps portion done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))


#####   DATA ACQUISITION FROM NCBI  ENTREZ.PY

from Bio import Entrez
Entrez.email = email
for i in second_dictionary:
    Entrez.email = 'sgreenfield@ucdavis.edu'
    if i.endswith('s'):
        i = i[:-1]
    handle = Entrez.esearch(db="gene", term=i, retmax=100000, usehistory="y")
    record = Entrez.read(handle)
    handle.close

    UID_list = record['IdList']
    webenv = record['WebEnv']
    querykey = record['QueryKey']

    print("UID list length: " + str(len(UID_list)))
    chunks = [UID_list[x:x + 200] for x in range(0, len(UID_list), 200)]


    def make_request(db, ids):
        r = requests.post("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi", data={
            "db": db,
            "id": ",".join(ids),
            "retmode": "json"
        })
        # print(r.status_code)
        return r.json()


    total = []
    for chunk in chunks:
        data = make_request("gene", chunk)
        total.append(data)

    count = 0
    count1 = 0
    gene_count = 0
    final_results = []
    for j in total:
        r = j['result']
        # print(r)
        uids = r['uids']
        # print(uids)
        for id in uids:
            count += 1
            info = r[id]
            name = info['name']
            description = info['description']
            organism = info['organism']
            scientific_name = organism['scientificname']
            if scientific_name == "Homo sapiens":
                count1 += 1
                #print(name, description, scientific_name)
                complete_info = (name, description, scientific_name)
                if name not in final_results:
                    gene_count += 1
                    final_results.append(complete_info)
                    print(str(i)+ "gene: " + str(gene_count))
    second_dictionary[i].append(gene_count)

print("NCBI portion done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))

print('------------------------------------------------------------------------------------------')
print('{:<60} {:<15} {:<15}'.format('Compound','Count','Number of Genes'))
print('------------------------------------------------------------------------------------------')
for i in second_dictionary:
    print('{:<60} {:<15} {:<15}'.format(i, second_dictionary[i][0], second_dictionary[i][1]))
print('------------------------------------------------------------------------------------------')

print("done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))

