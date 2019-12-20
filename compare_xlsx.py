import os
import pandas as pd
import random
import numpy as np
import datetime
import xlwt


def read_file(file: str, name: str):
    mul_file_name = os.walk(file)
    for filename in mul_file_name:
        if filename[2]:
            # datetime.append(filename[0][5:])
            for document_name in filename[2]:
                if name == document_name:
                    data = pd.read_excel(filename[0]+"/"+document_name)
                    return data


def compare_data(file: str, name: str):
    last_week = file[0]
    now_week = file[1]
    before_data = read_file(last_week, name)
    now_data = read_file(now_week, name)
    # print(before_data)
    # print(now_data)
    all_array = list()
    np_before_data = before_data.values
    np_now_data = now_data.values
    n = np.where(np_before_data == "B07CG9BJ9H")
    m = np.where(np_now_data == "B07CG9BJ9H")

    for now_item in np_now_data:
        for before_item in np_before_data:
            if now_item[0] == before_item[0]:
                asin_name = now_item[0]
                asin_score = now_item[1]-before_item[1]
                asin_comment = now_item[2]-before_item[2]
                asin_big_ranking = now_item[3]-before_item[3]
                asin_small_ranking = now_item[4]-before_item[4]
                all_array.append([asin_name, now_item[1], before_item[1], asin_score, '', now_item[2], before_item[2],
                                  asin_comment, '', now_item[3], before_item[3], asin_big_ranking, '', now_item[4],
                                  before_item[4], asin_small_ranking])
                break
        else:
            asin_name = now_item[0]
            asin_score = now_item[1] - 0
            asin_comment = now_item[2] - 0
            asin_big_ranking = now_item[3] - 0
            asin_small_ranking = now_item[4] - 0
            all_array.append([asin_name, now_item[1], 0, asin_score, '', now_item[2], 0,
                              asin_comment, '', now_item[3], 0, asin_big_ranking, '', now_item[4],
                              0, asin_small_ranking])

    for before_item in np_before_data:
        for now_item in np_now_data:
            if now_item[0] == before_item[0]:
                break
        else:
            asin_name = before_item[0]
            asin_score = 0 - before_item[1]
            asin_comment = 0 - before_item[2]
            asin_big_ranking = 0 - before_item[3]
            asin_small_ranking = 0 - before_item[4]
            all_array.append([asin_name, 0, before_item[1], asin_score, '', 0, before_item[1],
                              asin_comment, '', 0, before_item[1], asin_big_ranking, '', 0,
                              before_item[1], asin_small_ranking])

    print(all_array)
    print("="*80)
    last_week_date = last_week.split("/")[1]
    create_file(now_week+"A"+last_week_date)

    wb = xlwt.Workbook(encoding='utf8')
    # 创建一个sheet对象
    sheet = wb.add_sheet('order-sheet')

    # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    style_heading = xlwt.easyxf("""
                font:
                    name Arial,
                    colour_index white,
                    bold on,
                    height 0xA0;
                align:
                    wrap off,
                    vert center,
                    horiz center;
                pattern:
                    pattern solid,
                    fore-colour 0x19;
                borders:
                    left THIN,
                    right THIN,
                    top THIN,
                    bottom THIN; 
                """)
    # 上升样式 红色升
    style_rise = xlwt.easyxf("""pattern: pattern solid, fore_colour 0x0A""")
    # 下降样式 绿色降
    style_drop = xlwt.easyxf("""pattern: pattern solid, fore_colour 0x2A""")
    # 不变样式 金色
    style_not_change = xlwt.easyxf("""pattern: pattern solid, fore_colour 0x33""")

    # 深红
    style_deep_rise = xlwt.easyxf("""pattern: pattern solid, fore_colour red""")
    # 深绿
    style_deep_drop = xlwt.easyxf("""pattern: pattern solid, fore_colour green""")
    # 微红
    style_litter_rise = xlwt.easyxf("""pattern: pattern solid, fore_colour dark_red""")
    # 微绿
    style_litter_drop = xlwt.easyxf("""pattern: pattern solid, fore_colour light_green""")

    # 写入文件标题
    sheet.write(0, 0, 'ASIN', style_heading)
    sheet.write(0, 1, '这周评分', style_heading)
    sheet.write(0, 2, '上周评分', style_heading)
    sheet.write(0, 3, '趋势', style_heading)
    sheet.write(0, 4, '', style_heading)
    sheet.write(0, 5, '这周评论数', style_heading)
    sheet.write(0, 6, '上周评论数', style_heading)
    sheet.write(0, 7, '趋势', style_heading)
    sheet.write(0, 8, '', style_heading)
    sheet.write(0, 9, '这周大类排名', style_heading)
    sheet.write(0, 10, '上周大类排名', style_heading)
    sheet.write(0, 11, '趋势', style_heading)
    sheet.write(0, 12, '', style_heading)
    sheet.write(0, 13, '这周小类排名', style_heading)
    sheet.write(0, 14, '上周小类排名', style_heading)
    sheet.write(0, 15, '趋势', style_heading)

    # 写入数据
    data_row = 1
    for i in all_array:
        sheet.write(data_row, 0, i[0])
        sheet.write(data_row, 1, i[1])
        sheet.write(data_row, 2, i[2])
        if i[3] > 0:
            sheet.write(data_row, 3, i[3], style_rise)
        elif i[3] < 0:
            sheet.write(data_row, 3, i[3], style_drop)
        else:
            sheet.write(data_row, 3, i[3], style_not_change)
        sheet.write(data_row, 4, i[4])
        sheet.write(data_row, 5, i[5])
        sheet.write(data_row, 6, i[6])
        if i[7] > 0:
            sheet.write(data_row, 7, i[7], style_rise)
        elif i[7] < 0:
            sheet.write(data_row, 7, i[7], style_drop)
        else:
            sheet.write(data_row, 7, i[7], style_not_change)
        sheet.write(data_row, 8, i[8])
        sheet.write(data_row, 9, i[9])
        sheet.write(data_row, 10, i[10])
        if i[11] > 0:
            sheet.write(data_row, 11, -i[11], style_drop)
        elif i[11] < 0:
            sheet.write(data_row, 11, abs(i[11]), style_rise)
        else:
            sheet.write(data_row, 11, i[11], style_not_change)
        sheet.write(data_row, 12, i[12])
        sheet.write(data_row, 13, i[13])
        sheet.write(data_row, 14, i[14])
        if i[15] > 0:
            sheet.write(data_row, 15, -i[15], style_drop)
        elif i[15] < 0:
            sheet.write(data_row, 15, abs(i[15]), style_rise)
        else:
            sheet.write(data_row, 15, i[15], style_not_change)
        data_row = data_row + 1

    shop_name = name.split(".")[0]
    wb.save(now_week+"A"+last_week_date+"/"+shop_name+".xls")


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
    compare_data(["week/2019-12-19", "week/2019-12-25"], i)
    end = time.time()
    result = end-start
    print(i, " 所花时间", result)

