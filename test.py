import os
import sys
import pandas as pd


def find_file(file: str, name: str):
    mul_file_name = os.walk(file)
    frame = list()
    for filename in mul_file_name:
        if filename[2]:
            for document_name in filename[2]:
                if name == document_name:
                    data = pd.read_excel(filename[0]+"\\"+document_name)
                    frame.append(data)
                    break
    result = pd.concat(frame)
    txt = result.groupby(['ASIN'])
    for i in txt:
        if i[0] == "B07B5Y57DC":
            print(i[1]['ASIN'])

        # print(i[0], i[1])
        pass
    return result


find_file("shop", "DJ(FR).xlsx")
test = [[], [], [], [], []]