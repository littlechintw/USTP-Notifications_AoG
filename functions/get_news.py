import json
from bs4 import BeautifulSoup
import urllib
from urllib.parse import unquote as decode
from flask import Flask, request, make_response
import requests 
import datetime
import time as timelibrary
import feedparser
from functions.logs import logs_red, logs_green, logs_yellow, logs_blue

max_data = 10

headers = {
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "Content-type": "application/json; charset=UTF-8"
}

ntpu_headers = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://new.ntpu.edu.tw/news",
    "Origin": "https://new.ntpu.edu.tw",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
    "DNT": "1",
    "Sec-Fetch-Mode": "cors",
    "Content-type": "application/json; charset=UTF-8"
}
    

def takePublished(elem):
    return elem['published']

def get_ntut():
    try:
        url = 'https://news.ntut.edu.tw/p/503-1000-1080.php'
        rss = feedparser.parse(url)
    except:
        logs_yellow('[Get data!] Fail')
        return 'fail'
    else:
        logs_yellow('[Get data!] Success')
        data = rss['entries'] 
        response = []
        for notification in data:
            if len(response) < max_data:
                notification_data = {
                    'title': notification['title'],
                    'link': notification['link'],
                    'published': notification['published']
                }
                response.append(notification_data)
        return response

def get_ntou():
    try:
        r = requests.get("https://www.ntou.edu.tw/post/學校公告", headers=headers)
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')
        logs_yellow('Get data!')
    except:
        logs_yellow('[Get data!] Fail')
        return 'fail'
    else:
        logs_yellow('[Get data!] Success')
        # print(soup)
        notification_div = soup.find(class_="tab-content").find('ul', role="tabpanel")
        notification_form = notification_div.find_all('li')
        get_data = []
        for notification in notification_form:
            time = notification.find(class_="tabpanel_date").text[-9::]
            time_detail = time.split('/')
            y = int(time_detail[0]) + 1911
            m = int(time_detail[1])
            d = int(time_detail[2])
            convert = timelibrary.mktime(datetime.datetime(y,m,d).timetuple())
            notification_data = {
                'title': notification.find('a').get('title'),
                'link': notification.find('a').get('href'),
                'published': convert
            }
            get_data.append(notification_data)

        get_data.sort(key=takePublished, reverse=True)
        response = []
        for data in get_data:
            if len(response) < max_data:
                t = timelibrary.localtime(data['published'])
                t = timelibrary.strftime('%Y-%m-%d %H:%M:%S',t)
                data['published'] = t
                response.append(data)

        return response

def get_tmu():
    try:
        url = 'http://noda.tmu.edu.tw/board.rss'
        rss = feedparser.parse(url)
    except:
        logs_yellow('[Get data!] Fail')
        return 'fail'
    else:
        logs_yellow('[Get data!] Success')
        if rss.status == 200:
            data = rss['entries'] 
            response = []
            for notification in data:
                if len(response) < max_data:
                    notification_data = {
                        'title': notification['title'],
                        'link': notification['link'],
                        'published': notification['published']
                    }
                    response.append(notification_data)
        else:
            try:
                r = requests.get("http://glbsys.tmu.edu.tw/board/default4.aspx", headers=headers)
                r.encoding = 'utf8'
                soup = BeautifulSoup(r.text, 'html.parser')
                logs_yellow('Get data! (Back Website) ')
            except:
                logs_yellow('[Get data! (Back Website) ] Fail')
                return 'fail'
            else:
                logs_yellow('[Get data! (Back Website) ] Success')
                all_news = soup.find('table', class_="boardList table table-bordered table-condensed table-striped table-hover")
                news_list = all_news.find_all('tr')
                response = []
                for data in range(1,max_data+1,1):
                    news_detail = news_list[data].find_all('td')
                    published = news_detail[2].string[:4] + '/' + news_detail[2].string[4:6] + '/' + news_detail[2].string[6:8]
                    notification_data = {
                        'title': news_detail[0].string,
                        'link': 'http://35.194.235.225/open/super_pages.php?ID=open1&Sn=39',
                        'published': published
                    }
                    response.append(notification_data)
        return response

def get_ntpu():
    now_time = str(timelibrary.strftime("%Y-%m-%dT%H:%M:%S.000Z", timelibrary.localtime()))
    data_init  = "\n{\npublications(\nstart: 0,\nlimit: "
    data_init += str(max_data)
    data_init += ",\nsort: \"publishAt:desc,createdAt:desc\",\nwhere: {\nsitesApproved: \"www_ntpu\",\npublishAt_lte: \""
    data_init += now_time
    data_init += "\",\nunPublishAt_gte: \""
    data_init += now_time
    data_init += "\"\n}\n)\n{_id title tags contactPerson publishAt coverImage{url}}\n}"
    data = json.dumps({"query":data_init})
    
    try:
        r = requests.post("https://cms.carrier.ntpu.edu.tw/graphql", headers=ntpu_headers, data=data)
        r.encoding = 'utf8'
        soup = BeautifulSoup(r.text, 'html.parser')
        logs_yellow('Get data!')
    except:
        logs_yellow('[Get data!] Fail')
        return 'no'
    else:
        logs_yellow('[Get data!] Success')
        json_dict = json.loads(str(soup))
        response = []
        for notification in json_dict['data']['publications']:
            if len(response) < max_data:
                notification_data = {
                    'title': notification['title'],
                    'link': 'https://new.ntpu.edu.tw/news/' + notification['_id'],
                    'published': notification['publishAt']
                }
                response.append(notification_data)
        return response