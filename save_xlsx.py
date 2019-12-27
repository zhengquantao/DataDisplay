import os
import pandas as pd
import random
import numpy as np
import datetime


def find_file(file: str, name: str):
    mul_file_name = os.walk(file)
    frame = list()      # 所有dataframe数组
    # datetime_list = list()
    for filename in mul_file_name:
        if filename[2]:
            # datetime.append(filename[0][5:])
            for document_name in filename[2]:
                if name == document_name:
                    data = pd.read_excel(filename[0]+"/"+document_name)
                    # data["date"] = filename[0][5:]  # 加入时间
                    frame.append(data)
                    # datetime_list.append(filename[0][5:])
                    break
    result = pd.concat(frame)
    sort_result = result.sort_values(by=['ASIN', 'date'])
    group_data = sort_result.groupby(['ASIN'])  # .apply(lambda x: x.sort_values("date", ascending=True))

    group_count = group_data['ASIN'].size().to_dict()  # 转化成字典
    group_rank = sorted(group_count, key=lambda x: group_count[x], reverse=True)  # 字典排序

    names = name.split(".")[0]
    today = str(datetime.date.today())
    create_file("week/"+today)

    shop_array = list()

    for good in group_data:
        asin_id = good[0]
        asin_count = len(good[1])
        asin_score = round(sum(good[1]['评分'].fillna(0)) / asin_count, 2)
        asin_comment = round(sum(good[1]['评论数'].fillna(0)) / asin_count, 2)
        asin_small_ranking = round(sum(good[1]['小类排名'].fillna(0))/asin_count, 2)
        asin_big_ranking = round(sum(good[1]['大类排名'].fillna(0))/asin_count, 2)
        shop_array.append([asin_id, asin_score, asin_comment, asin_big_ranking, asin_small_ranking])
    data_obj = pd.DataFrame(shop_array, columns=['ASIN', '评分', '评论数', '大类排名', '小类排名'])
    writer = pd.ExcelWriter("week/"+today+"/"+name)
    data_obj.to_excel(writer, "Sheet", index=False)
    writer.save()


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