import os
import pandas as pd
import matplotlib.pyplot as plt


def find_file(file: str, name: str):
    mul_file_name = os.walk(file)
    frame = list()      # 所有dataframe数组
    for filename in mul_file_name:
        if filename[2]:
            # datetime.append(filename[0][5:])
            for document_name in filename[2]:
                if name == document_name:
                    data = pd.read_excel(filename[0]+"\\"+document_name)
                    data["date"] = filename[0][5:]  # 加入时间
                    frame.append(data)
                    break
    result = pd.concat(frame)
    group_data = result.groupby(['ASIN'])
    names = name.split(".")[0]
    for good in group_data:
        # if i[0] == "B07B5Y57DC":
        #     print(i[1])
        create_file("image/"+names)
        plot(good[1], names, good[0])


def create_file(file: str):
    """
    创建文件夹
    file: 文件夹
    """
    if not os.path.isdir(file):
        os.makedirs(file)


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

    ax1.plot(datetime, shop_score, "red", label="评分")
    ax1.legend(title="评分")
    ax1.grid(True)

    ax2.plot(datetime, shop_comment, "red", label="评论数")
    ax2.legend(title="评论数")
    ax2.grid(True)

    ax3.plot(datetime, shop_big_ranking, "red", label="大类")
    ax3.grid(True)
    ax3.legend(title="大类")

    ax4.plot(datetime, shop_small_ranking, "red", label="小类")
    ax4.grid(True)
    ax4.legend(title="小类")

    # multi = MultiCursor(fig.canvas, (ax1, ax2, ax3, ax4), color='r', lw=1, linestyle=':',
    #             horizOn=False, vertOn=True)

    plt.xlabel(name)
    plt.savefig('./image/'+filename+'/'+name+'.png')
    plt.cla()
    plt.close()
    # plt.show()


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