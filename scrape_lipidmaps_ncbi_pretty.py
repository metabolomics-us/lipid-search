import sys
import os.path
import datetime
import requests
from bs4 import BeautifulSoup
from xlrd import open_workbook

output_folder1 = "query_results"

if not os.path.exists(output_folder1):
    os.makedirs(output_folder1)

#query = input("Type compound of interest:   ")
query = "acylglycerol"
#excel_sheet = "text_python_excel.xlsx"
#email = input("Provide email (needed for NCBI search):  ")
email = "sgreenfield@ucdavis.udu"


def list_from_xlsheet(excel_sheet):
    rb = open_workbook(excel_sheet)
    sheet = rb.sheet_by_index(0)
    query_list = []
    for i in range(sheet.nrows):
        try:
            query_list.append(sheet.cell_value((i+9), 2))
            print(sheet.cell_value((i+9), 2))
        except:
            continue

if query.endswith("s"):
    query = query[-1]

lst = query.split()
length = len(lst)

print("\n")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))
print("LipidMaps")


#####  LIPIDMAPS_SEARCHSUMMARY.PY

def class_search_one(query_list):
    upper = query_list[0].upper()
    lower = query_list[0].lower()
    text = requests.get('https://www.lipidmaps.org/data/structure/ClassFuzzySearch.php?Name=' + upper + '&s=' + lower)
    src = text.content
    soup = BeautifulSoup(src, 'lxml')
    return soup

def class_search_two(query_list):
    upper1 = query_list[0].upper()
    lower1 = query_list[0].lower()
    upper2 = query_list[1].upper()
    lower2 = query_list[1].lower()
    text = requests.get('https://www.lipidmaps.org/data/structure/ClassFuzzySearch.php?Name=' + upper1 + upper2 + "&s=" + lower1 + "%20" + lower2 + "&SortResultsBy=Name")
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

if length == 1:
    soup = class_search_one(lst)
elif length == 2:
    soup = class_search_two(lst)

count = 0
query_dic = {}
dictionary = counting(soup, query, count)
second_query = []
second_query = new_searches(soup, second_query)


for i in second_query:
    count = 0
    i = i.lower()
    if i.endswith('s'):
        i = i[:-1]
    if i in dictionary:
        continue
    else:
        lst = i.split()
        length = len(lst)
        count = 0
        if length == 1:
            soup = class_search_one(lst)
        elif length == 2:
            soup = class_search_two(lst)
        count = 0
        second_dictionary = counting(soup, i, count)

print("number of compounds related to " + str(query) + ":   " + str(second_dictionary[query][0]))
print("LipidMaps portion done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p") + "\n")
print("NCBI (related gene information - runtime directly related to how many compounds were found related to your query)")


#####   DATA ACQUISITION FROM NCBI  ENTREZ.PY

from Bio import Entrez
Entrez.email = email

def entrez_UID_list(i):
    Entrez.email = email
    if i.endswith('s'):
        i = i[:-1]
    handle = Entrez.esearch(db="gene", term=i, retmax=100000, usehistory="y")
    record = Entrez.read(handle)
    handle.close

    UID_list = record['IdList']
    webenv = record['WebEnv']
    querykey = record['QueryKey']

    print("UID list length for " + str(i) + " : " + str(len(UID_list)))
    chunks = [UID_list[x:x + 200] for x in range(0, len(UID_list), 200)]
    return chunks


def make_request(db, ids):
    r = requests.post("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi", data={
        "db": db,
        "id": ",".join(ids),
        "retmode": "json"
    })
    # print(r.status_code)
    return r.json()

def information_parsing(total, i):
    count = 0
    count1 = 0
    gene_count = 0
    final_results = []
    if len(total) > 0:
        with open(os.path.join(output_folder1, i + "_genes.txt"), 'a') as file:
            file.write('{:<15} {:<15} {:<220} {:<15}'.format('UID', 'Gene Name', 'Description', 'Organism') + "\n")
    for j in total:
        #with open(os.path.join(output_folder1, i + "_genes.txt"), 'a') as file:
            #file.write('{:<15} {:<15} {:<220} {:<15}'.format('UID', 'Gene Name', 'Description', 'Organism') + "\n")
        r = j['result']
        uids = r['uids']
        for id in uids:
            count += 1
            info = r[id]
            name = info['name']
            description = info['description']
            organism = info['organism']
            scientific_name = organism['scientificname']
            if scientific_name == "Homo sapiens":
                count1 += 1
                complete_info = (id, name, description, scientific_name)
                if id not in final_results:
                    gene_count += 1
                    final_results.append(complete_info)
                    if gene_count % 5 == 0:
                        print(str(i)+ " gene: " + str(gene_count))
                    #print("gene information:  " + id, name, description, scientific_name)
                    with open(os.path.join(output_folder1, i + "_genes.txt"), 'a') as file:
                        file.write('{:<15} {:<15} {:<220} {:<15}'.format(id, name, description, scientific_name) + "\n")
    return gene_count

###
for i in second_dictionary:
    chunks = entrez_UID_list(i)
    total = []
    for chunk in chunks:
        data = make_request("gene", chunk)
        total.append(data)
    gene_count = information_parsing(total, i)
    second_dictionary[i].append(gene_count)
###


print("NCBI portion done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))

print('--------------------------------------------------------------------------------------------------')
print('{:<60} {:<20} {:<15}'.format('Compound','Related Compounds','Number of Genes'))
print('--------------------------------------------------------------------------------------------------')
for i in second_dictionary:
    print('{:<60} {:<20} {:<15}'.format(i, second_dictionary[i][0], second_dictionary[i][1]))
print('--------------------------------------------------------------------------------------------------')

print("done")
currentDT = datetime.datetime.now()
print(currentDT.strftime("%I:%M:%S %p"))


with open(os.path.join(output_folder1, query + "_summary.txt"), 'a') as f:
    f.write('{:<60} {:<15} {:<15}'.format('Compound','Count','Number of Genes') + "\n")
    for i in second_dictionary:
        f.write('{:<60} {:<15} {:<15}'.format(i, second_dictionary[i][0], second_dictionary[i][1]) + "\n")

