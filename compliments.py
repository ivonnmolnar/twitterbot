from urllib.request import urlopen
from bs4 import BeautifulSoup
import codecs

html = urlopen("https://www.happier.com/blog/nice-things-to-say-100-compliments")
bsObj = BeautifulSoup(html,"html.parser")

list_elements = bsObj.findAll("ol") #getting the list elements
compliments = []
with codecs.open("compliments.txt", "w","utf-8-sig") as f:
    for list_element in list_elements:
        for i in list_element.findAll("li"):
            f.write(i.text)
            f.write('\n')
