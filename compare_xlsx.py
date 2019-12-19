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
    pass


def save_data():
    pass


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
    compare_data("week/2019-12-19", i)
    end = time.time()
    result = end-start
    print(i, " 所花时间", result)

    # wb = xlwt.Workbook(encoding='utf8')
    # # 创建一个sheet对象
    # sheet = wb.add_sheet('order-sheet')
    #
    # # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
    # style_heading = xlwt.easyxf("""
    #             font:
    #                 name Arial,
    #                 colour_index white,
    #                 bold on,
    #                 height 0xA0;
    #             align:
    #                 wrap off,
    #                 vert center,
    #                 horiz center;
    #             pattern:
    #                 pattern solid,
    #                 fore-colour 0x19;
    #             borders:
    #                 left THIN,
    #                 right THIN,
    #                 top THIN,
    #                 bottom THIN;
    #             """)
    #
    # # 写入文件标题
    # sheet.write(0, 0, '编号', style_heading)
    # sheet.write(0, 1, '地点名称', style_heading)
    # sheet.write(0, 2, '类型名称', style_heading)
    # sheet.write(0, 3, '手机号码', style_heading)
    # sheet.write(0, 4, '时间日期', style_heading)
    #
    # # 写入数据
    # data_row = 1
    # # 这个是查询条件,可以根据自己的实际需求做调整.
    # if types:
    #     if start_time != '' and start_time == end_time:
    #         start = start_time.replace('-', ',').split(',')
    #         # print(start[1])
    #         Excel = Execel.objects.filter(datetime__year=int(start[0]),
    #                                         datetime__month=int(start[1]),
    #                                         datetime__day=int(start[2]), type=types)
    #     elif start_time and end_time:
    #         Excel = Execel.objects.filter(datetime__range=(start_time, end_time), type=types)
    #     elif start_time:
    #         Excel = Execel.objects.filter(datetime__gte=start_time, type=types)
    #     elif end_time:
    #         Excel = Execel.objects.filter(datetime__lte=end_time, type=types)
    #     else:
    #         Excel = Execel.objects.filter(type=types)
    # else:
    #     if start_time != '' and start_time == end_time:
    #         start = start_time.replace('-', ',').split(',')
    #         # print(start[1])
    #         Excel = Execel.objects.filter(datetime__year=int(start[0]),
    #                                         datetime__month=int(start[1]),
    #                                         datetime__day=int(start[2]))
    #     elif start_time and end_time:
    #         Excel = Execel.objects.filter(datetime__range=(start_time, end_time))
    #     elif start_time:
    #         Excel = Execel.objects.filter(datetime__gte=start_time)
    #     elif end_time:
    #         Excel = Execel.objects.filter(datetime__lte=end_time)
    #     else:
    #         Excel = Execel.objects.all()
    #
    # for i in Excel:
    #     # 格式化datetime
    #     datetime = i.datetime.strftime('%Y-%m-%d %H:%M:S')
    #     sheet.write(data_row, 0, i.id)
    #     sheet.write(data_row, 1, i.area)
    #     sheet.write(data_row, 2, i.type)
    #     sheet.write(data_row, 3, i.phone)
    #     sheet.write(data_row, 4, datetime)
    #
    #     data_row = data_row + 1
    #
    # # 写出到IO
    # output = BytesIO()
    # wb.save(output)
    # # 重新定位到开始
    # output.seek(0)
    # response.write(output.getvalue())
    # return response