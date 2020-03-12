import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.ncbi.nlm.nih.gov/gene/?term=acylglycerol")
src = result.content
soup = BeautifulSoup(src, 'lxml')

urls = []
for h2_tag in soup.find_all("div"):     # right click link, click inspect, notice that all of the links have an h2 class; thus we can do this to get all of the links - woo
    print(h2_tag)
    a_tag = h2_tag.find('a')           # gives us the single 'a' tag that is found under the 'h2' tag
    urls.append(a_tag.attrs['href'])

print(urls)

for link in soup.find_all('a'):
    print(link.get('href'))