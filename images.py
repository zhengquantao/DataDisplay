import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random


font = FontProperties(fname="/home/zhengquantao/python/DataDisplay/font/FangSong.ttf")

appear_day = 3


def find_file(file: str, name: str):
    mul_file_name = os.walk(file)
    frame = list()      # 所有dataframe数组
    datetime_list = list()
    for filename in mul_file_name:
        if filename[2]:
            # datetime.append(filename[0][5:])
            for document_name in filename[2]:
                if name == document_name:
                    data = pd.read_excel(filename[0]+"/"+document_name)
                    data["date"] = filename[0][5:]  # 加入时间
                    frame.append(data)
                    datetime_list.append(filename[0][5:])
                    break
    result = pd.concat(frame)
    sort_result = result.sort_values(by=['ASIN', 'date'])
    group_data = sort_result.groupby(['ASIN'])  # .apply(lambda x: x.sort_values("date", ascending=True))

    group_count = group_data['ASIN'].size().to_dict()  # 转化成字典
    group_rank = sorted(group_count, key=lambda x: group_count[x], reverse=True)  # 字典排序

    names = name.split(".")[0]

    # ===============评分===========
    fig = plt.figure(figsize=(14, 7))
    ax1 = fig.subplots(nrows=1)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    for rank in group_rank:
        for good in group_data:
            if rank == good[0] and len(good[1]) > appear_day:
                create_file("image/"+names)
                shop_score = good[1]['评分'].fillna(0)
                datetime = good[1]['date'].fillna('0')
                ax1.plot(datetime, shop_score, random_color(), label=good[0])
                ax1.legend(title=u"GOODS", loc='right', bbox_to_anchor=(-0.015, 0.6))
                ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.title(names+" 评分", fontproperties=font)
    plt.savefig('./image/'+names+'/'+'评分.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================评论==========
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    create_file("image/" + names)
    for rank in group_rank:
        for good in group_data:
            if rank == good[0] and len(good[1]) > appear_day:
                shop_comment = good[1]['评论数'].fillna(0)
                datetime = good[1]['date'].fillna('0')
                ax1.plot(datetime, shop_comment, random_color(), label=good[0])
                ax1.legend(title=u"GOODS", loc='right', bbox_to_anchor=(-0.04, 0.6))
                ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.title(names+" 评论数", fontproperties=font)
    plt.savefig('./image/'+names+'/'+'评论数.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================大类排名=================
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    create_file("image/" + names)
    for rank in group_rank:
        for good in group_data:
            if rank == good[0] and len(good[1]) > appear_day:
                shop_big_ranking = good[1]['大类排名'].fillna(0)
                datetime = good[1]['date'].fillna('0')
                ax1.plot(datetime, -shop_big_ranking, random_color(), label=good[0])
                ax1.legend(title=u"GOODS", loc='right', bbox_to_anchor=(-0.03, 0.6))
                ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.title(names+" 大类排名", fontproperties=font)
    plt.savefig('./image/'+names+'/'+'大类排名.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================小类排名=================
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    create_file("image/" + names)
    for rank in group_rank:
        for good in group_data:
            if rank == good[0] and len(good[1]) > appear_day:
                shop_small_ranking = good[1]['小类排名'].fillna(0)
                datetime = good[1]['date'].fillna('0')
                ax1.plot(datetime, -shop_small_ranking, random_color(), label=good[0])
                ax1.legend(title=u"GOODS", loc='right', bbox_to_anchor=(-0.04, 0.6))
                ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.title(names+" 小类排名", fontproperties=font)
    plt.savefig('./image/'+names+'/'+'小类排名.png')
    # plt.cla()
    # plt.close()
    # plt.show()


def create_file(file: str):
    """
    创建文件夹
    file: 文件夹
    """
    if not os.path.isdir(file):
        os.makedirs(file)


def random_color():
    """
    颜色函数
    """
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#"+color


# find_file("shop")

name_list = ['DJ(FR).xlsx', 'DJ(德国).xlsx', 'DJ(英国).xlsx', 'DreamJ(加拿大).xlsx', 'DreamJ(美国).xlsx',
             'FOR(日本).xlsx', 'Formemory(加拿大).xlsx', 'Formemory(美国).xlsx', 'HAPYSHOP(日本).xlsx',
             'HOM(日本).xlsx', 'Housestory(加拿大).xlsx', 'Housestory(美国).xlsx', 'houstory(德国).xlsx',
             'houstory(意大利).xlsx', 'houstory(英国).xlsx', 'houstory(西班牙).xlsx', 'Kicpot(加拿大).xlsx',
             'Kicpot(美国).xlsx', 'SHENGO(日本).xlsx', 'Tumao(日本).xlsx']

import time
for i in name_list:
    start = time.time()
    find_file("shop", i)
    end = time.time()
    result = end-start
    print(i, " 所花时间", result)