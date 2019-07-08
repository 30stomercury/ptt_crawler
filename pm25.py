import requests
from bs4 import BeautifulSoup
import sys
import re
import numpy as np
import sys
import time

url_pei = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/North.aspx?fm=AqiMap'
url_chung = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/Central.aspx?fm=AqiMap' 
url_hsin = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/Chu-Miao.aspx?fm=AqiMap'
url_nan = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/Yun-Chia-Nan.aspx?fm=AqiMap' 
url_kao = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/KaoPing.aspx?fm=AqiMap'
url_yilan = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/Yilan.aspx?fm=AqiMap'
url_hua = 'https://taqm.epa.gov.tw/taqm/tw/Aqi/Hua-Tung.aspx?fm=AqiMap'
url = [url_pei, url_chung, url_hsin, url_nan, url_kao, url_yilan, url_hua]

start = time.time()
pm25_dic = {}
for url_ in url:
    response = requests.get(url_)
    soup = BeautifulSoup(response.text, 'lxml')
    a = soup.find_all('tr')
    a = [i for i in a if 'linkSite' in str(i)]
    a = a[1:]
    for i in a:
        for pm in i:
            if 'labPM25' in str(pm):
                pm25 = pm.text
        pm25_dic[i.find('a').text] = pm25.replace('\n','')
end = time.time()

print('cost {} s'.format(-start+end))
print('Total {} stations pm25 crawled.'.format(len(pm25_dic)))
print('\n')
stations = []
for i in pm25_dic.items():
    if i[1] != 'ND':
        stations.append((int(i[1]),i[0]))
    # print('PM2.5 of station {}: {}'.format(i[0], i[1]))

s_ = sorted(stations, reverse=True)
for i in s_[:10]:
    print('PM2.5 of station {}: {} μg/m3'.format(i[1], i[0]))