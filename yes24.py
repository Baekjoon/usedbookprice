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
    url = 'http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=BOOK&qdomain=%B1%B9%B3%BB%B5%B5%BC%AD&query=' + isbn
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.select('div.goodsList.goodsList_list')
    assert len(divs) > 0
    trs = divs[0].find('table').find_all('tr')
    tr = trs[0]
    td = tr.select('td.goods_infogrp')[0]
    title = td.select('p.goods_name strong')[0].text.strip()
    temp = td.select('div.goods_info a')
    for a in temp:
        if not a.get('href'):
            continue
        href = a.get('href')
        if 'company_yn=Y' in href:
            company = a.text.strip()
    print('%s\t%s'%(company,title))
