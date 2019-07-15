#####   https://www.youtube.com/watch?v=87Gx3U0BDlo
#####   freecodecamp.org
#####   Beautiful Soup Tutorial - Web Scraping in Python

import requests
from bs4 import BeautifulSoup

result = requests.get("http://www.google.com")   ##  access the website provided

print(result.status_code)                        ##  make sure the website is accessible; get 200 code = OK response

print(result.headers)                            ## check the HTTP header to verify we accessed the right website
                                                 ##  here it's a bit more info on the google.com (domain) homepage
src = result.content                             ##  extract the content of the page; returns the source of the page

features="html.parser"
soup = BeautifulSoup(src, 'lxml')                ##  creates a soup object that allows us to extract some types of info we want
                                                 ##  should be (src, 'lxml') but not work; fine, just get warning without
links = soup.find_all("a")                       ##  give me all of the links on the page aka "a tags"
print(links)                                     ##  presents a python list of the links
print("\n")

for link in links:                               ##  search through the list of links to find all the links with the word "About"
    if "About" in link.text:                     ##  turning it into a list allows us to use the .text function (find thing in text of link)
        print(link)
        print(link.attrs['href'])                ##  print out the actual thing that it goes to as well; give me the content of the 'href' inside of that link tag  (. . .  got a lot of errors, but still seemed to work . . .)
