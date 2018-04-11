import requests
from bs4 import BeautifulSoup
import csv
import re

"""
clawer the data from Slang Dictionary, write 'SlangDic.csv' file to support folder
"""

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def getSlangPair(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find_all("div", {"class": "dictionary-word"})

    for i in div:
        try:
            for index in i.find_all("dt"):
                key = index.text[:-2]
            for index in i.find_all("dd"):
                value = index.text
            lst[key] = value
        except:
            continue
    return lst


if __name__ == "__main__":

    slist = {}
    for i in range(26):
        stock_list_url  = 'https://www.noslang.com/dictionary/'+chr(i + ord('a'))+'/'
        getSlangPair(slist, stock_list_url)
    print (slist)


    fileObject = open('slangDic.txt', 'w')
    for index in slist:
        try:
            fileObject.write(index+':')
            fileObject.write(slist[index])
            fileObject.write('\n')
        except:
            pass
    fileObject.close()