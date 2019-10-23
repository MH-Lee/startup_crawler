from selenium import webdriver
import pandas as pd
import time, re
from random import randint, randrange, random
from bs4 import BeautifulSoup

k = input("시작할 순서 선택")
if k == '':
    k = 0
k = int(k)
print("%d에서 부터 시작합니다." % (k))

driver = webdriver.Chrome('C:/Users/sunboangel/driver/chromedriver')
driver.implicitly_wait(3)
driver.get('https://www.rocketpunch.com/investments/funded_companies?page=1')
parent_window = driver.current_window_handle
try:
    close = driver.find_element_by_xpath('//*[@id="company_signup_popup"]/div[1]/i')
    close.click()
    time.sleep(randrange(1,2) + random())
except:
    pass
time.sleep(randrange(1,2) + random())
data_1 = pd.read_excel('./final/rocket_punch2.xlsx')
# url = data_1.loc[i, "Url"]
url = 'https://www.rocketpunch.com/companies/kmong#funded'
company = '크몽'
print(company)
description = '재능마켓 크몽'
driver.execute_script("window.open('{}')".format(url))
all_windows = driver.window_handles
child_window = [window for window in all_windows if window != parent_window][0]
driver.switch_to.window(child_window)
try:
    close = driver.find_element_by_xpath('//*[@id="company_signup_popup"]/div[1]/i')
    close.click()
    time.sleep(randrange(1,2) + random())
except:
    pass
html = driver.page_source
soup_child = BeautifulSoup(html, 'html.parser')
overview = soup_child.find("div", {"id": "company-overview"})
if overview is None: overview = 'none'
else : overview = overview.text
fund_list = []
funding_info = soup_child.find("section", {"id": "company-funded"}).find_all("div", {"class": "ui funded-item funding segment"})
funding_info
for fund in funding_info:
    fund_date = fund.find_all('span',{"class":'item'})[0].text
    fund_amount = fund.find('strong',{ "class":"amount"}) #투자금액
    if fund_amount is None : fund_amount= '비공개'
    else : fund_amount = text = re.sub(r"\s{1,}", " ", fund_amount.text.strip())
    if fund_amount is None : fund_value= '비공개'
    else : fund_value = re.sub('[-=.#/?:$}]', '', fund.find('span',{ "class":"valuation"}).text.strip() ) #기업가치
    fund_header = fund.find_all('a',{'class':'header nowrap'})
    header = []
    for head in fund_header :
        header.append(re.sub('[-=.#/?:$}]', '', head.text))
    fund_list.append({'fund_date':fund_date,'fund_amount': fund_amount, 'fund_value':fund_value,'header':header})

sub_information = soup_child.find("section", {"id": "company-info"})
if sub_information is None : sub_info= ['none']
else :
    sub_info = []
    sub_information = soup_child.find("section", {"id": "company-info"}).find_all("div", {"class": "item"})
    for sub in sub_information:
        sub_info.append(re.sub(r"\s{2,}", " ",re.sub('[\n\xa0]', ' ', sub.text).strip()))

category = []
labels = soup_child.find_all("a", {"class": "ui circular basic label"})
for label in labels:
    category.append(label.text)
try:
    service = soup_child.find('div', {'class':'product content item'}).find('div',{'class':'overview'}).text
except AttributeError:
    service = None


driver = webdriver.Chrome('C:/Users/sunboangel/driver/chromedriver')
driver.implicitly_wait(3)
driver.get('https://www.rocketpunch.com/investments/funded_companies?page=1')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

tags = soup.find('div', {'id':'company-list'}).findAll("div", {"class": "content"})

tags[2].find('a', {'class':'link'})['href']
tags[2].find('strong').text
tags[3].find('div', {'class':'description'}).text is None

invest_num = tags[2].find('a',{'class':'item'}).text
invest_num = int(re.findall('\d+', invest_num)[0])
invest_num
