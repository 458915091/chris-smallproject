import requests
from bs4 import BeautifulSoup
import pymongo

clint = pymongo.MongoClient('localhost',8888)
lumpy = clint['lumpy']
phone_list = lumpy['phone_list']

def get_links_url():
    start_url = 'http://sz.ganji.com/shouji/'
    began_url = 'http://sz.ganji.com'
    # various_brands_url
    html = requests.get(start_url).text
    soup = BeautifulSoup(html,'lxml')
    url_id_list = soup.select('div > dl:nth-of-type(1) > dd > a')
    ##seltion > div > dl:nth-child(1)
    for url_id_href in url_id_list:
        url_id = url_id_href.get('href')
        name = url_id_href.text.replace('\n','')
        if 'shouji'in url_id :
            pass
        else:
            id_data = {
                '手机品牌':name,
                '手机URL':began_url+url_id,
                'URLID':url_id
            }
            phone_list.insert_one(id_data)
            print(url_id,name,'插入数据库成功！！！')




get_links_url()