import requests
from bs4 import BeautifulSoup
import sys
import re
import numpy as np
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## 找出表特版2017第一篇文的文章列表url (2017/12/31)
def find_first_url(start_date, start_year, url):
    '''
    input: start_date: 1/01 (str), 
           start_year: 2017(str), 
           url: url of the last page of beauty
    output: url: 該年的第一天所在的文章列表網址
    '''
    #######################################################
    payload = {
    'from':'/bbs/Gossiping/index.html',
    'yes':'yes'
    }
    rs = requests.session()
    #######################################################
    ptt = 'https://www.ptt.cc'
    lst = []
    year_tempt = 0
    flag_0 = 0 #date
    flag_1 = 0 #year
    while flag_1 == 0:
        print(url)
        response = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
        response = rs.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', 'r-ent') 
        # 照時間順序sorting
        for article in articles:
            meta = article.find('div', 'title').find('a')
            if meta != None: # not exist, 被刪除的文章不用抓
                date = article.find('div', 'date').getText().replace('/','').replace(' ','') # 日期格式轉換
                lst.append(date)

        if start_date in lst: # find the correct date
            flag_0 = 1
            meta = articles[-1].find('div', 'title').find('a')
            if meta == None:
                meta = articles[-2].find('div', 'title').find('a')
            link_article = meta.get('href')
            response_article = rs.get(ptt+link_article, verify=False)
            soup_article = BeautifulSoup(response_article.text, 'lxml')
            a = soup_article.find_all('span', 'article-meta-value')
            if len(a) > 0:
                data_in_article = soup_article.find_all('span', 'article-meta-value')[-1]
                year_tempt = data_in_article.getText()[-4:]
                if year_tempt == start_year:
                    flag_1 = 1
                else:
                    flag_0 = 0
                    lst = []


        if flag_0 == 0:
            controls = soup.find('div', 'btn-group-paging').find_all('a', 'btn wide')
            link_next = controls[1].get('href')
            url = ptt + link_next  
            #print(url)

    controls = soup.find('div', 'btn-group-paging').find_all('a', 'btn wide')
    link_next = controls[1].get('href')
    url_next = ptt + link_next # url of the next page
    lst_next = [start_date]
    #print(url_next)

    #找出start day的第一頁
    while start_date in lst_next:
        lst_next = []
        # check if last page contains start_date
        response_next = rs.get(url_next)
        soup_next = BeautifulSoup(response_next.text, 'lxml')
        articles_next = soup_next.find_all('div', 'r-ent') 
        for article in articles_next:
            meta = article.find('div', 'title').find('a')
            if meta != None: # not exist, 被刪除的文章不用抓
                date = article.find('div', 'date').getText().replace('/','').replace(' ','') # 日期格式轉換
                lst_next.append(date)
        if start_date in lst_next: # update url
                url = url_next
                controls = soup_next.find('div', 'btn-group-paging').find_all('a', 'btn wide')
                link_next = controls[1].get('href')
                url_next = ptt + link_next # url of the next page
        else:
            print('The url of the the first page ' + start_year + '/' + start_date + ':' + '\n' + url)
            return url

## 找出表特版2017最後一篇文的文章列表url (2017/12/31)
def find_last_url(last_date, last_year, url):
    ## 找出2017最後一篇文的文章列表url (2017/12/31)
    flag_0 = 0 #date
    flag_1 = 0 #year
    lst = []
    #######################################################
    payload = {
    'from':'/bbs/Gossiping/index.html',
    'yes':'yes'
    }
    rs = requests.session()
    #######################################################
    while flag_1 == 0:
        response = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
        response = rs.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', 'r-ent') 
        for article in articles:
            meta = article.find('div', 'title').find('a')
            if meta != None: # not exist, 被刪除的文章不用抓
                date = article.find('div', 'date').getText().replace('/','').replace(' ','') # 日期格式轉換
                lst.append(date)
                #print(date)
        if last_date in lst:
            flag_0 = 1
            meta = articles[0].find('div', 'title').find('a')
            if meta == None:
                meta = articles[1].find('div', 'title').find('a')
            link_article = meta.get('href')
            response_article = rs.get(ptt+link_article)
            soup_article = BeautifulSoup(response_article.text, 'lxml')
            a = soup_article.find_all('span', 'article-meta-value')

            data_in_article = soup_article.find_all('span', 'article-meta-value')[-1]
            year_tempt = data_in_article.getText()[-4:]
            if year_tempt == last_year:
                flag_1 = 1
            else:
                flag_0 = 0
                lst = []

        if flag_0 == 0:
            controls = soup.find('div', 'btn-group-paging').find_all('a', 'btn wide')
            link = controls[1].get('href')
            url = ptt + link
            #print(url)
    print('The url of the the last page ' + last_year + '/' + last_date + ':' + '\n' + url)
    return url

## 開始爬文
def crawler(url_start, url_end, start_date, last_date):
    ptt = 'https://www.ptt.cc'
    f_articles = open('all_news.txt','w',encoding = 'utf-8-sig')
    f_articles.close()
    #######################################################
    payload = {
    'from':'/bbs/Gossiping/index.html',
    'yes':'yes'
    }
    rs = requests.session()
    #######################################################
    flag_0 = 0 # while link == url_start, flag_0 = 1
    flag_1 = 0 # while link == url_last, flag_1 = 1
    j = 0
    url = url_start
    while flag_1 == 0:
        response = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=payload)
        response = rs.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', 'r-ent')
        for article in articles:
            meta = article.find('div', 'title').find('a')
            if meta != None: # not exist, 被刪除的文章不用抓
                title = meta.getText().strip()
                link = meta.get('href')
                date = article.find('div', 'date').getText().replace('/','').replace(' ','') # 日期格式轉換
                if date == start_date and url == url_start:
                    flag_0 = 1

                if date != last_date and url == url_end:
                    flag_0 = 0
                    flag_1 = 1
                    break

                if (title[1:3] != '公告'): # start crawling
                    if flag_0 == 1:
                        res = rs.get(ptt + link)
                        soup =  BeautifulSoup(res.text,'lxml')
                        main_content = soup.find(id='main-content')
                        content_0 = []
                        if main_content != None:
                            for v in main_content.stripped_strings:
                                if '--' not in v and 'imgur' not in v and 'http' not in v:
                                    if v != '':
                                        content_0.append(v.replace('\n','').replace('」', ' ').replace('「', ' ').replace('…', ' ').replace('，',' ').replace('？',' ').replace('。',' ').replace('。',' ').replace('...',' ').replace('、',' ').replace('；',' ').replace(';',' ')+' ')
                                else:
                                    break

                            
                            content_1 = ''
                            for i in content_0[8:]:
                                content_1 += i
                            content_1 = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%\※\◆\～\！\、\《\》\_\：\-\（\）\／\【\】\─\║\〔\〕\●\％\★\▲\↑\+]", "", content_1)
                            
                            if content_1 != '':
                                for key in keywords:
                                    if key in content_1 or key in title:
                                        # save contents into articles    
                                        f_articles = open('all_articles_{}_{}.txt'.format(start_date,last_date),'a',encoding = 'utf-8-sig')
                                        # f_articles.write(content_1 + ' ')
                                        f_articles.write('{},{},{}\n'.format(date, title, ptt+link))
                                        f_articles.close()
                                        j += 1
                                        break


        # controls: [最舊, 上頁, 下頁, 最新]
        response = rs.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        controls = soup.find('div', 'btn-group btn-group-paging').find_all('a', 'btn wide')
        link = controls[2].get('href')
        ptt = 'https://www.ptt.cc'
        url = ptt + link
        print(url)

    print('data crawled!!!')
    print('total %d articles.' % j)

if len(sys.argv) < 4:
    print('No action specified.')
    sys.exit()



# 表特版最新頁
url = 'https://www.ptt.cc/bbs/Gossiping/index.html' 
# ptt首頁
ptt = 'https://www.ptt.cc'
# 設置 key words
keywords = ['空汙', '廢氣', '空氣品質', '空氣汙染', 'PM', 'PM2.5', '空氣質量', 'Pm2.5', 'pm2.5', '霧霾', '霾害']
# 設置日期
start_date = sys.argv[1]
start_year = sys.argv[2]
last_date = sys.argv[3]
last_year = sys.argv[4]
print('Start searching...')
# 從url start的列表開始爬
url_start = find_first_url(start_date, start_year, url)
url_end = find_last_url(last_date, last_year, url) 
print('Start crawling...')
crawler(url_start, url_end, start_date, last_date)

# input python ptt_crawler 101 2016 1231 2018