import os
import pandas as pd
import random
import numpy as np
import xlwt
import json
import time
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 变化范围 [评分(升,降), 评论数(升,降), 大类排名(升,降), 小类排名(升,降)]
change_range = [(1, 1), (10, 10), (1000, 1000), (1000, 1000)]


# 登录
def login():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument("disable-web-security")
    options.add_argument('disable-infobars')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    driver = webdriver.Chrome(chrome_options=options, desired_capabilities=capa)
    wait = WebDriverWait(driver, 30)
    driver.maximize_window()

    login_url = "http://gg7.irobotbox.com/Manager/Login.aspx"
    driver.get(login_url)
    while True:
        # 商家号
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#TextCustomerID")))
        TextCustomerID = driver.find_element_by_css_selector("#TextCustomerID")
        TextCustomerID.send_keys("1921")

        # 用户名
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#TextAdminName")))
        TextAdminName = driver.find_element_by_css_selector("#TextAdminName")
        TextAdminName.send_keys("text")

        # 密码
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#TextPassword")))
        TextPassword = driver.find_element_by_css_selector("#TextPassword")
        TextPassword.send_keys("tm201606")

        # 识别验证码
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#captchaImage")))
        captchaImage = driver.find_element_by_css_selector("#captchaImage")
        location = captchaImage.location
        size = captchaImage.size
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        driver.get_screenshot_as_file('a.png')
        a = Image.open("a.png")
        a = a.convert('L')
        im = a.crop((left, top, right, bottom))
        im.save('a.png')
        f = open('a.png', 'rb')
        response = requests.post(url="http://182.61.174.27:7788/", data=f.read())
        text = json.loads(response.text)
        print(text['code'])

        # 输入验证码
        txtValidate = driver.find_element_by_css_selector("#txtValidate")
        txtValidate.send_keys(text['code'])

        # 登录按钮
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#submit")))
        submit = driver.find_element_by_css_selector("#submit")
        submit.click()
        time.sleep(2)

        try:
            if driver.current_url != login_url:
                cookies = driver.get_cookies()
                cookie = [item["name"] + "=" + item["value"] for item in cookies]
                cookie_str = '; '.join(item for item in cookie)
                driver.quit()
                return cookie_str

        except UnexpectedAlertPresentException as e:
            print("验证码错误")
            driver.refresh()


cookies = login()


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
            all_array.append([asin_name, 0, before_item[1], asin_score, '', 0, before_item[2],
                              asin_comment, '', 0, before_item[3], asin_big_ranking, '', 0,
                              before_item[4], asin_small_ranking])

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

    # 不变样式 金色
    style_not_change = xlwt.easyxf("""pattern: pattern solid, fore_colour 43""")  # 43
    # 深红
    style_deep_rise = xlwt.easyxf("""pattern: pattern solid, fore_colour 3""")  # 6
    # 深绿
    style_deep_drop = xlwt.easyxf("""pattern: pattern solid, fore_colour 6""")  # 3
    # 微红
    style_litter_rise = xlwt.easyxf("""pattern: pattern solid, fore_colour 42""")  # 45
    # 微绿
    style_litter_drop = xlwt.easyxf("""pattern: pattern solid, fore_colour 45""")  # 42

    # 写入文件标题
    sheet.write(0, 0, 'ASIN', style_heading)
    sheet.write(0, 1, '标题', style_heading)
    sheet.write(0, 2, "价格", style_heading)          # 价格
    # sheet.write(0, 3, "这周价格", style_heading)     # 价格
    # sheet.write(0, 4, "上周价格", style_heading)     # 价格
    # sheet.write(0, 5, "", style_heading)            # 价格
    sheet.write(0, 3, '这周评分', style_heading)
    sheet.write(0, 4, '上周评分', style_heading)
    sheet.write(0, 5, '趋势', style_heading)
    sheet.write(0, 6, '', style_heading)
    sheet.write(0, 7, '这周评论数', style_heading)
    sheet.write(0, 8, '上周评论数', style_heading)
    sheet.write(0, 9, '趋势', style_heading)
    sheet.write(0, 10, '', style_heading)
    sheet.write(0, 11, '这周大类排名', style_heading)
    sheet.write(0, 12, '上周大类排名', style_heading)
    sheet.write(0, 13, '趋势', style_heading)
    sheet.write(0, 14, '', style_heading)
    sheet.write(0, 15, '这周小类排名', style_heading)
    sheet.write(0, 16, '上周小类排名', style_heading)
    sheet.write(0, 17, '趋势', style_heading)

    # 写入数据
    data_row = 1
    for i in all_array:
        title, price = get_sku(i[0], cookies)
        sheet.write(data_row, 0, i[0])
        sheet.write(data_row, 1, title)
        sheet.write(data_row, 2, price)  # 价格
        sheet.write(data_row, 3, i[1])
        sheet.write(data_row, 4, i[2])
        if i[3] > 0:
            if i[3] >= change_range[0][1]:
                sheet.write(data_row, 5, i[3], style_deep_rise)
            else:
                sheet.write(data_row, 5, i[3], style_litter_rise)
        elif i[3] < 0:
            if abs(i[3]) < change_range[0][1]:
                sheet.write(data_row, 5, i[3], style_litter_drop)
            else:
                sheet.write(data_row, 5, i[3], style_deep_drop)
        else:
            sheet.write(data_row, 5, i[3], style_not_change)
        sheet.write(data_row, 6, i[4])
        sheet.write(data_row, 7, i[5])
        sheet.write(data_row, 8, i[6])
        if i[7] > 0:
            if i[7] >= change_range[1][0]:
                sheet.write(data_row, 9, i[7], style_deep_rise)
            else:
                sheet.write(data_row, 9, i[7], style_litter_rise)
        elif i[7] < 0:
            if abs(i[7]) < change_range[1][1]:
                sheet.write(data_row, 9, i[7], style_litter_drop)
            else:
                sheet.write(data_row, 9, i[7], style_deep_drop)
        else:
            sheet.write(data_row, 9, i[7], style_not_change)
        sheet.write(data_row, 10, i[8])
        sheet.write(data_row, 11, i[9])
        sheet.write(data_row, 12, i[10])
        if i[11] > 0:
            if i[11] >= change_range[2][1]:
                sheet.write(data_row, 13, -i[11], style_deep_drop)
            else:
                sheet.write(data_row, 13, -i[11], style_litter_drop)
        elif i[11] < 0:
            if abs(i[11]) < change_range[2][0]:
                sheet.write(data_row, 13, abs(i[11]), style_litter_rise)
            else:
                sheet.write(data_row, 13, abs(i[11]), style_deep_rise)
        else:
            sheet.write(data_row, 13, i[11], style_not_change)
        sheet.write(data_row, 14, i[12])
        sheet.write(data_row, 15, i[13])
        sheet.write(data_row, 16, i[14])
        if i[15] > 0:
            if i[15] >= change_range[3][1]:
                sheet.write(data_row, 17, -i[15], style_deep_drop)
            else:
                sheet.write(data_row, 17, -i[15], style_litter_drop)
        elif i[15] < 0:
            if abs(i[15]) < change_range[3][0]:
                sheet.write(data_row, 17, abs(i[15]), style_litter_rise)
            else:
                sheet.write(data_row, 17, abs(i[15]), style_deep_rise)
        else:
            sheet.write(data_row, 17, i[15], style_not_change)
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


def get_sku(asin: str, cookies: str):
    headers = {
        "Cookie": cookies
    }
    url = "http://gg7.irobotbox.com/IrobotBox/Amazon/AmazonListingList.aspx?&SearchType=0&txtNo2=3&txtNo="+asin
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    try:
        soup_text = soup.select_one('tr[skuinfo*="skuinfo"] td:nth-child(3) p:nth-child(2)')
        price = soup.select_one('input[id*="txtPrice"]').attrs['value']
        title = soup_text.get_text()
    except:
        title = ""
        price = ""
    return title, price


name_list = ['DJ(FR).xlsx', 'DJ(德国).xlsx', 'DJ(英国).xlsx', 'DreamJ(加拿大).xlsx', 'DreamJ(美国).xlsx',
             'FOR(日本).xlsx', 'Formemory(加拿大).xlsx', 'Formemory(美国).xlsx', 'HAPYSHOP(日本).xlsx',
             'HOM(日本).xlsx', 'Housestory(加拿大).xlsx', 'Housestory(美国).xlsx', 'houstory(德国).xlsx',
             'houstory(意大利).xlsx', 'houstory(英国).xlsx', 'houstory(西班牙).xlsx', 'Kicpot(加拿大).xlsx',
             'Kicpot(美国).xlsx', 'SHENGO(日本).xlsx', 'Tumao(日本).xlsx']


import time
for i in name_list:
    start = time.time()
    compare_data(["week/2019-12-20", "week/2019-12-23"], i)
    end = time.time()
    result = end-start
    print(i, " 所花时间", result)