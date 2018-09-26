# -*- coding: utf-8 -*-
# __author__: Chris lumpy

# tesseract-ocr
import re
import requests
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver

class ziroom (object):

    def __init__(self):
        self.url = 'http://www.ziroom.com/z/nl/z2.html?p=3'
        self.driver = webdriver.Chrome()

    def get_content(self):
        div_list = self.driver.find_elements_by_xpath('//*[@id="houseList"]/li')
        number = self.get_image_number()
        for div in div_list[1:]:
            try:
                price_list = []
                for i in range(2,6):
                    start_price = div.find_element_by_xpath('.//div[3]/p/span[{}]'.format(i)).get_attribute('style').split(' ')[1].replace('-','').replace('px','')
                    price = number[int(int(start_price)/30)]
                    price_list.append(price)

                price = '￥{}元/每月'.format(''.join(price_list))
                title = div.find_element_by_xpath('.//div/h3/a').text.replace(' ', '')
                location = div.find_element_by_xpath('.//div/h4/a').text.replace(' ', '')
                area = div.find_element_by_xpath('.//div/div/p[1]').text.replace(' ', '')
                nerarby = div.find_element_by_xpath('.//div/div/p[2]').text.replace(' ', '')

                data = {
                    '房源': title,
                    '价格': price,
                    '面积': area,
                    '位置': location,
                    '附近': nerarby
                }
                print(data)
            except:
                pass

    def get_image_number(self):
        html = self.driver.execute_script("return document.documentElement.outerHTML")
        photo = re.findall('var ROOM_PRICE = {"image":"(//.*?.png)"',html)[0]
        image = requests.get('http:'+photo).content
        f = open('price.png','wb')
        f.write(image)
        f.close()
        num = []
        number = pytesseract.image_to_string(Image.open("price.png"),config="-psm 8 -c tessedit_char_whitelist=1234567890")
        for i in number:
            num.append(i)
        return num

    def run(self):
        self.driver.get(self.url)
        self.get_image_number()
        content = self.get_content()
        

if __name__ == '__main__':
    z = ziroom()
    z.run()
