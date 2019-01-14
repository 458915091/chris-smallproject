# -*- coding: utf-8 -*-
# __author__: Chris lumpy
import re
import os
import requests
import tkinter
import PythonMagick
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
from threading import Thread
from PIL import Image
from PIL.ImageTk import PhotoImage

# 图标转换 ico
image_content = requests.get('http://img.zcool.cn/community/019b685541ad0d000001a64b63c7fa.jpg').content
f = open('logo.jpg', 'wb')
f.write(image_content)
f.close()
image = PythonMagick.Image('logo.jpg')
image.sample('128x128')
image.write('logo.ico')

# 数据列表
id_list = []
name_list = []
file = None
# 状态
sign = False


# 请求获取歌单
def get_music():
    global sign
    global file
    try:
        url = entry.get()
        start_url = url.replace('/#', '')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Host': 'music.163.com'
        }
        html = requests.get(start_url, headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        message_list = soup.find('ul', {'class': 'f-hide'}).find_all('a')
        file = soup.find('title').text.replace(' - 歌单 - 网易云音乐', '')
        for message in message_list:
            r = re.compile('[/\*?"[]|:]')
            name = r.sub('~', message.text)
            id = message.get('href').replace('/song?id=', '')
            name_list.append(name)
            id_list.append(id)
        sign = False
    except:
        sign = True
        messagebox.showinfo('错误！', '您输入的歌单网站有误！')


# 构造按钮函数
def show():
    global sign
    get_music()
    if sign == False:
        t.geometry('300x400+500+200')
        btn1['state'] = 'normal'
        var = tkinter.StringVar()
        var.set(name_list)
        listbox = Listbox(t, listvariable=var)
        listbox.place(y=80, height=300, width=300)
        label1 = Label(t, text='状态：')
        label1.place(y=380)


def show_Thread():
    show_t = Thread(target=show)
    show_t.start()


def ensurn():
    label1 = Label(t, text='状态：确认歌单成功！')
    label1.place(y=380)
    btn2['state'] = 'normal'


def download():
    if not os.path.exists('./{}'.format(file)):
        os.mkdir('./{}'.format(file))
    for i in range(len(id_list)):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }

        content = requests.get('http://music.163.com/song/media/outer/url?id={}.mp3'.format(id_list[i]),
                               headers=headers)
        print(content)
        music_file = open('./{}/{}.mp3'.format(file, name_list[i]), 'wb')
        music_file.write(content.content)
        label1 = Label(t, text='状态：歌曲 {} 下载成功！                                       '.format(name_list[i]))
        label1.place(y=380)


def download_Thread():
    download_t = Thread(target=download)
    download_t.start()


# 构造UI界面
t = Tk()
t.title('网易云音乐歌单')
t.iconbitmap('logo.ico')
t.geometry('300x90+500+200')
label = Label(t, text='歌单url：')
label.place(x=10, y=10)
entry = Entry(t, width=40)
entry.place(x=10, y=30)
entry.insert(0, '例：https://music.163.com/')
btn = Button(t, text='显示歌单', command=show_Thread)
btn.place(x=10, y=60, height=20)
btn1 = Button(t, text='确认歌单', command=ensurn)
btn1.place(x=120, y=60, height=20)
btn1['state'] = 'disabled'
btn2 = Button(t, text='开始下载', command=download_Thread)
btn2['state'] = 'disabled'
btn2.place(x=230, y=60, height=20)
t.mainloop()
