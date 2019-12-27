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
                return cookie_str
            driver.quit()

        except UnexpectedAlertPresentException as e:
            print("验证码错误")
            time.sleep(2)
            driver.refresh()


def get_sku(asin: str, cookies: str):
    headers = {
        "Cookie": cookies
    }
    url = "http://gg7.irobotbox.com/IrobotBox/Amazon/AmazonListingList.aspx?&SearchType=0&txtNo2=3&txtNo="+asin
    html = requests.get(url=url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    try:
        soup_text = soup.select_one('tr[skuinfo*="skuinfo"] td:nth-child(3) p:nth-child(2)')
        soup_price = soup.select_one('input[id*="txtPrice"]').attrs['value']
        print(soup_text.get_text(), '----', soup_price)
    except:
        soup_text = ""
        soup_price = ""
    return soup_text, soup_price

cookies = login()
get_sku("B07M5XKQ71", cookies)

#
# code_url = "http://gg7.irobotbox.com/Manager/Tools/ValidateCode.ashx"
#
# login_url = "http://gg7.irobotbox.com/Manager/Login.aspx"
#
# index_url = "http://gg7.irobotbox.com/Manager/index.aspx"
#
# find_item = "http://gg7.irobotbox.com/IrobotBox/Amazon/AmazonListingList.aspx?&SearchType=0&txtNo2=3&txtNo="
# import requests
# import json
#
# header = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "no-cache",
#     "Connection": "keep-alive",
#     "Content-Length": "40",
#     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#     "Host": "gg7.irobotbox.com",
#     "Pragma": "no-cache",
#     "Upgrade-Insecure-Requests": "1",
#     "Cookie": "_ati=1353840465818; Hm_lvt_bd5c92691c7aa293cbae57b8424ee1e8=1576805861,1577174104; \
#     irobotbox_cookie_language=zh_CN; ASP.NET_SessionId=dtzj1u0h0wp3ckpwtl4xcana; irobotbox_cookie_time=\
#     2019-12-26+17%3a03%3a17; ValidCode=2HsNAisFZqw%3d",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
# }
# session = requests.session()
# login = session.get(login_url, headers=header)
#
# image = session.get(code_url)
# print(login.history)
# response = requests.post(url="http://182.61.174.27:7788/", data=image.content)
#
# code = json.loads(response.text)
# user_msg = {
#     "actions": "SendCaptchaCode",  # UserLogin
#     "userLoginView": {
#         "CustomerId": "1921",
#         "UserName": "text",
#         "Password": "tm201606",
#         "CaptchaCode": code['code'],
#         "LocalIp": "192.168.200.128",
#         "RedirectUrl": "Index.aspx",
#         "IsNewDeviceLogin": False,
#     }
# }
#
# r = session.post(login_url, data=user_msg)
# print(r.text)
# if r:
#     # m = session.get(index_url)
#     # print(m.text, m.cookies)
#     s = session.get(find_item+"B07CG9BJ9H")
#     print(s.text)
# print(r)