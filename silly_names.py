from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import codecs

r = urllib.request.Request("https://www.drodd.com/html7/silly-nicknames.html", headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
html = urllib.request.urlopen(r)

bsObj = BeautifulSoup(html,"html.parser")

list_elements = bsObj.find("ul").findAll("li") #getting the list elements

#there are nested tags and we only want the text so it has to be stripped from
#those other tags
with codecs.open("names.txt",'w',"utf-8-sig") as f:
    for list_element in list_elements:
        for tag_content in list_element:
            f.write(tag_content)
            f.write('\n')
            break #so we only get the text (first tag_content)
