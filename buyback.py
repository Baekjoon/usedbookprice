#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) > 1:
    isbns = sys.argv[1:]
else:
    with open('isbn.txt','r') as fp:
        isbns = fp.readlines()

for isbn in isbns:
    url = 'http://www.yes24.com/Mall/buyback/Search?CategoryNumber=018&SearchWord='+isbn+'&SearchDomain=BOOK,FOREIGN&BuybackAccept=N'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.select('div.bbGoodsList')
    assert len(divs) > 0
    ul = divs[0].find('ul')
    li = ul.find_all('li')[0]
    prices = li.select('div.bbG_info div.bbG_price table tbody tr td')
    print('yes24')
    prices = [p.text.strip() for p in prices]
    print(prices)
    url = 'https://www.aladin.co.kr/shop/usedshop/wc2b_search.aspx?ActionType=1&SearchTarget=Book&KeyWord='+isbn+'&x=0&y=0'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    temp = soup.find(id='searchResult')
    if not temp:
        print('aladin')
        print('not exists')
        continue
    tr = temp.find('tr')
    td = temp.find_all('td')[2]
    table = td.find_all('table')[1]
    tr = table.find_all('tr')[3]
    prices = tr.find_all('td')
    prices = [p.text.strip() for p in prices]
    print('aladin')
    print(prices)
