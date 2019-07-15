# YouTube Link: https://www.youtube.com/watch?v=87Gx3U0BDlo

# Let's obtain the links from teh following website:
# https://www.whitehouse.gov/briefings-statements

# One of the things this website consists of is records of presidential
# briefings and statements

# Goal: Extract all of the links on the page that point to the
# briefings and statements.


import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.whitehouse.gov/briefings-statements")
src = result.content
soup = BeautifulSoup(src, 'lxml')

urls = []
for h2_tag in soup.find_all("h2"):     # right click link, click inspect, notice that all of the links have an h2 class; thus we can do this to get all of the links - woo
    a_tag = h2_tag.find('a')           # gives us the single 'a' tag that is found under the 'h2' tag
    urls.append(a_tag.attrs['href'])

print(urls)

for link in soup.find_all('a'):
    print(link.get('href'))