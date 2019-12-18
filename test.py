import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random


font = FontProperties(fname="/home/zhengquantao/python/DataDisplay/font/FangSong.ttf")


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
    sort_result = result.sort_values(['ASIN', 'date'])
    group_data = sort_result.groupby(['ASIN'])  # .apply(lambda x: x.sort_values("date", ascending=True))
    names = name.split(".")[0]

    # ===============评分===========
    fig = plt.figure(figsize=(14, 7))
    ax1 = fig.subplots(nrows=1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for good in group_data:

        create_file("image/"+names)

        shop_score = good[1]['评分'].fillna(0)

        datetime = good[1]['date'].fillna('0')

        ax1.plot(datetime, shop_score, random_color(), label=good[0])
        ax1.legend(title=u"评分", loc='right', bbox_to_anchor=(-0.015, 0.6))
        ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.savefig('./image/'+names+'/'+'评分.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================评论==========
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for good in group_data:

        create_file("image/" + names)

        shop_comment = good[1]['评论数'].fillna(0)

        datetime = good[1]['date'].fillna('0')
        ax1.plot(datetime, shop_comment, random_color(), label=good[0])
        ax1.legend(title=u"评论数", loc='right', bbox_to_anchor=(-0.04, 0.6))
        ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.savefig('./image/'+names+'/'+'评论数.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================大类排名=================
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for good in group_data:

        create_file("image/" + names)
        shop_big_ranking = good[1]['大类排名'].fillna(0)
        datetime = good[1]['date'].fillna('0')
        ax1.plot(datetime, -shop_big_ranking, random_color(), label=good[0])
        ax1.legend(title=u"大类排名", loc='right', bbox_to_anchor=(-0.03, 0.6))
        ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
    plt.savefig('./image/'+names+'/'+'大类排名.png')
    # plt.cla()
    # plt.close()
    # plt.show()

    # ================小类排名=================
    fig = plt.figure(figsize=(14.5, 7))
    ax1 = fig.subplots(nrows=1)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    for good in group_data:

        create_file("image/" + names)

        shop_small_ranking = good[1]['小类排名'].fillna(0)
        datetime = good[1]['date'].fillna('0')
        ax1.plot(datetime, -shop_small_ranking, random_color(), label=good[0])
        ax1.legend(title=u"小类排名", loc='right', bbox_to_anchor=(-0.04, 0.6))
        ax1.grid(True)
    plt.xlabel(name, fontproperties=font)
    plt.xticks(rotation=45)
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
    color_arr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += color_arr[random.randint(0, 14)]
    return "#"+color


def plot(data: object, filename: str, name: str):
    """
    展示数据
    data: 数据
    datetime: 时间
    filename: 文件夹
    name: 文件名
    """
    shop_score = data['评分'].fillna('0')
    shop_comment = data['评论数'].fillna('0')
    shop_big_ranking = data['大类排名'].fillna('0')
    shop_small_ranking = data['小类排名'].fillna('0')
    datetime = data['date'].fillna('0')

    fig = plt.figure(figsize=(11, 6))
    (ax1, ax2, ax3, ax4) = fig.subplots(nrows=4)
    plt.rcParams['font.sans-serif'] = ['SimHei']

    ax1.plot(datetime, shop_score, "red", label=name)
    ax1.legend(title="评分")
    ax1.grid(True)

    # ax2.plot(datetime, shop_comment, "red", label="评论数")
    # ax2.legend(title="评论数")
    # ax2.grid(True)
    #
    # ax3.plot(datetime, shop_big_ranking, "red", label="大类")
    # ax3.grid(True)
    # ax3.legend(title="大类")
    #
    # ax4.plot(datetime, shop_small_ranking, "red", label="小类")
    # ax4.grid(True)
    # ax4.legend(title="小类")

    # multi = MultiCursor(fig.canvas, (ax1, ax2, ax3, ax4), color='r', lw=1, linestyle=':',
    #             horizOn=False, vertOn=True)


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