import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor
import matplotlib.dates as mdate
import pandas as pd


class ShowData(object):

    def __init__(self):
        self.path = None
        pass

    def open(self, path):
        get_data = pd.read_excel(path)
        return get_data

    def plot(self, path):
        data = self.open(path)
        shop_name = data['ASIN']
        shop_score = data['评分'].fillna('0')
        shop_comment = data['评论数'].fillna('0')
        shop_big_ranking = data['大类排名'].fillna('0')
        shop_small_ranking = data['小类排名'].fillna('0')

        fig = plt.figure(figsize=(10, 6))
        (ax1, ax2, ax3, ax4) = fig.subplots(nrows=4)
        plt.rcParams['font.sans-serif'] = ['SimHei']

        ax1.plot(shop_score.index, shop_score, "red", label="评分")
        ax1.legend(title="评分")
        ax1.grid(True)

        ax2.plot(shop_comment.index, shop_comment, "red", label="评论数")
        ax2.legend(title="评论数")
        ax2.grid(True)

        ax3.plot(shop_big_ranking.index, shop_big_ranking, "red", label="大类")
        ax3.grid(True)
        ax3.legend(title="大类")

        ax4.plot(shop_small_ranking.index, shop_small_ranking, "red", label="小类")
        ax4.grid(True)
        ax4.legend(title="小类")

        multi = MultiCursor(fig.canvas, (ax1, ax2, ax3, ax4), color='r', lw=1, linestyle=':',
                    horizOn=False, vertOn=True)

        plt.xlabel("店名")
        plt.show()


s = ShowData()
s.plot("./shop/2019-12-05/DJ(FR).xlsx")


class ReadFile(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        pass


