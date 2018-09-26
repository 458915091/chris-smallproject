import pymongo
import charts

# client = pymongo.MongoClient('localhost',27017)
# lumpy = client['lumpy']
# detall_list = lumpy['detall_url']
# phone_list = lumpy['phone_list']
#
# post_time_list =[]
# for post in detall_list.find():
#     post_time = post['time']
#     post_time_list.append(post_time)
#
# name_list = []
# for names in phone_list.find():
#     name = names['手机品牌']
#     name_list.append(name)
#
# def data(types):
#     length = 0
#     if length <=len(name_list):
#         for name,time in zip(name_list,post_time_list):
#             data = {
#                 'name' : name,
#                 'data' : [time],
#                 'type' : types
#             }
#             yield data
#             length +=1
#
# series = [data for data in data('column')]
# charts.plot(series,show='inline',options=dict(title=dict(text='深圳宝安手机发帖数绘图')))




"""
options = {
    'chart'   : {'zoomType':'xy'},
    'title'   : {'text': 'Monthly Average Temperature'},
    'subtitle': {'text': 'Source: WorldClimate.com'},
    'xAxis'   : {'categories': ['周一', '周二', '周三', '周四']},
    'yAxis'   : {'title': {'text': '数量'}}
    }

series = [
    {
    'name': 'OS X',
    'data': [11,2,3,4],
    'type': 'line',
    'y':5
}]

charts.plot(series, options=options,show='inline')
"""

# import pymongo
# import random
# client = pymongo.MongoClient('localhost',27017)
# lumpy = client['lumpy']
# movies = lumpy['movies']
#
# def get_categories(date1,date2):
#     x = 0
#     date_list = []
#     date_nums = int(date2)-int(date1)+1
#     while x < date_nums:
#         date = str(int(date1)+x)
#         x+=1
#         date_list.append(date)
#     return date_list
#
#
# def get_table(date1,date2,table_list):
#     date_list = get_categories(date1,date2)
#     for table in table_list:
#         start_score_list = []
#         for date in date_list:
#             score_list = []
#             for i in movies.find():
#                 start_table = i['table'].split()
#                 year = i['time']
#                 start_table.insert(0, year)
#                 # print(start_table)
#                 over_date= start_table[0]
#                 if date in start_table:
#                     if table in start_table:
#                         del start_table[0]
#                         over_table = ' '.join(start_table)
#                         # print(over_date,over_table)
#                         for i in movies.find({'time':date,'table':over_table}):
#                             score = i['score']
#                             score_list.append(int(score.replace('.','')))
#             start_score_list.append(random.choice(score_list))
#         data ={
#             'name': table,
#             'data': start_score_list,
#             'type': 'line',
#         }
#         yield data


# get_table('2010','2011',['剧情','爱情','喜剧'])
# data_list = get_categories('2010','2011')

# options = {
#     'chart'   : {'zoomType':'xy'},
#     'title'   : {'text': '{}-{}年份随机电影评分'.format('2010','2011')},
#     'subtitle': {'text': 'Source: 小鹿出品'},
#     'xAxis'   : {'categories':get_categories('2010','2011')},
#     'yAxis'   : {'title': {'text': '评分'}}
#     }

# series = [data for data in get_table('2010','2011',['剧情','爱情','喜剧'])]

# charts.plot(series, options=options,show='inline')
# print(series)


"""
options = {
    'chart'   : {'zoomType':'xy'},
    'title'   : {'text': '发帖量统计'},
    'subtitle': {'text': '可视化统计图表'},
    }

series =  [{
    'type': 'pie',
    'name': 'Browser share',
    'data':[
            ['北京二手家电', 8836],
            ['北京二手文体/户外/乐器', 5337],
            ['北京二手数码产品', 4405],
            ['北京二手服装/鞋帽/箱包', 4074],
            ['北京二手母婴/儿童用品', 3124],
            ['北京二手台式机/配件', 2863],
            ['北京二手图书/音像/软件', 2777],
            ['北京二手办公用品/设备', 2496],
            ['北京二手家具', 1903],
            ['北京二手美容/保健', 1838],
            ['北京二手手机', 1603],
            ['北京二手笔记本', 1174],
            ['北京二手设备', 1004],
            ['北京其他二手物品', 761],
            ['北京二手平板电脑', 724]
            ]
        }]
        
charts.plot(series,options=options,show='inline')
"""

import pymongo
import charts

client = pymongo.MongoClient('localhost',27017)
lumpy = client['lumpy']
movies = lumpy['movies']

def get_nums():
    table_list = []
    for movie_list in movies.find():
        movie_table = movie_list['table'].split()
        for movie_table_one in movie_table:
            table_list.append(movie_table_one)

    nums_list = []
    for table_2 in set(table_list):
        x = 0
        for table_1 in table_list:
            if table_2 == table_1:
                x+=1
        nums_list.append(x)

    for i in range(len(nums_list)):
        data = [list(set(table_list))[i],int(nums_list[i])]
        yield data


options = {
    'chart': {'zoomType': 'xy'},
    'title': {'text': '电影所属类型数量统计'},
    'subtitle': {'text': '可视化统计图表'},
}

series = [{
    'type': 'pie',
    'name': 'Movies nums',
    'data': [data for data in get_nums()]
}]

charts.plot(series, options=options, show='inline')
