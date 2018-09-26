import pymongo
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import random
import queue

q = queue.Queue()
clint = pymongo.MongoClient('localhost',8888)
lumpy = clint['lumpy']
phone_list = lumpy['phone_list']
detall_url = lumpy['detall_url']

proxy_list = [
    'http://112.115.57.20:3128',
    'http://180.101.205.253:8888',
    'http://218.60.8.99:3129',
    'http://218.60.8.83:3129'
]
proxy_ip = random.choice(proxy_list)
proxies = {'http':proxy_ip}

print(proxies)
def get_start_url():
    start_url_list = []
    for url in phone_list.find():
        start_url = url['手机URL']
        start_url_list.append(start_url)
    return start_url_list

def get_detall_url(url):
    finall_url_list = []
    for i in range(1, 21):
        start_url = url + 'baoan/o%s' % i
        html = requests.get(start_url,proxies=proxies).text
        soup = BeautifulSoup(html,'lxml')
        detall_url = soup.select('div.infocon > table > tbody > tr > td.t > a')
        for urls in detall_url:
            finall_url = urls.get('href')
            finall_url_list.append(finall_url)
    post_time = len(finall_url_list)
    return post_time

def get_post_time(post_time):
    data ={'time':post_time}
    detall_url.insert_one(data)
    print(data)

def run(url):
    post_time = get_detall_url(url)
    get_post_time(post_time)




if __name__ == '__main__':
    p = Pool()
    p.map(run,get_start_url())


