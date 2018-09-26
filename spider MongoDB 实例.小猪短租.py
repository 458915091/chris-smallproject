import requests
from bs4 import BeautifulSoup
import pymongo

#http://bj.xiaozhu.com/search-duanzufang-p1-0/
#http://bj.xiaozhu.com/search-duanzufang-p2-0/

class xiaozhu():
    def __init__(self):
        self.url_list = []
        for i in range (1,14):
            self.start_url = 'http://bj.xiaozhu.com/search-duanzufang-p1-0/'
            url = 'http://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(i)
            self.url_list.append(url)
            self.headers ={
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Cookie': 'abtest_ABTest4SearchDate=b; xzuuid=a0b5e818; PHPSESSID=c6m06cploffp7i1nfk42r7a0m3; xz_guid_4se=b42390c6-e04c-4240-bb45-c0d07010a85c; gr_user_id=b1f410ed-b39f-4b64-8d96-492f13dc61c6; gr_session_id_59a81cc7d8c04307ba183d331c373ef6=7d980aca-b4ea-4696-8aa3-84a8e018adde; gr_session_id_59a81cc7d8c04307ba183d331c373ef6_7d980aca-b4ea-4696-8aa3-84a8e018adde=true'
            }

    def get_message(self,url):
        html = requests.get(url,headers=self.headers).text
        # print(html)
        soup = BeautifulSoup(html,'lxml')

        name_list = []
        name_all = soup.select('#page_list > ul > li > div > div > a ')
        for names in name_all :
            name = names.text
            name_list.append(name)

        infor_list = []
        infor_all = soup.select('#page_list > ul > li > div > div > em')
        for infors in infor_all :
            infor = infors.text.strip().replace('\n','').replace(' ','')
            infor_list.append(infor)

        price_list = []
        price_all = soup.select('#page_list > ul > li > div > span.result_price')
        for prices in price_all :
            price = prices.text.strip()
            price_list.append(price)

        dict_list = []
        for i in range(24):
            dict = {}
            dict['标题'] = name_list[i]
            dict['内容'] = infor_list[i]
            dict['价格'] = price_list[i]
            dict_list.append(dict)
        return dict_list



    def save_dict_in_mongo(self,dict_list):
        client = pymongo.MongoClient('localhost',8888)
        lumpy = client['lumpy']
        xiaozhu = lumpy['小猪短租']
    #     print(dict)
        for i in dict_list:
            xiaozhu.insert(i)
        for y in range (1,14):
            print('正在写入第{}页...'.format(y))
            for n in range (1,25):
                print('写入数据库成功！文档编码：{}'.format(n))

    def run(self):
        for url in self.url_list:
            dict_list=self.get_message(url)
            self.save_dict_in_mongo(dict_list)

if __name__=='__main__':
    xz = xiaozhu()
    xz.run()
    # xz.get_message()


