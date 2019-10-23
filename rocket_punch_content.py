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
data = pd.DataFrame(columns=["Url", "Company", "Company_detail"\
                            "Investor", "Invest_amount", "Company_info"])
driver.get('https://www.rocketpunch.com/investments/funded_companies?page=1')
parent_window = driver.current_window_handle
try:
    close = driver.find_element_by_xpath('//*[@id="company_signup_popup"]/div[1]/i')
    close.click()
    time.sleep(randrange(1,2) + random())
except:
    pass
time.sleep(randrange(1,2) + random())
data_1 = pd.read_excel('./final/rocket_punch3.xlsx')
rocket_data = pd.DataFrame(columns=["Url", "Company", "Overview", "Category",\
                                    "Fund_info", "Sub_info", "Service_description"])
left_data = list(data_1.index)[k:]
try_number = 0
try:
    for i in left_data:
        try_number += 1
        print("남은 데이터: %d" % (len(left_data) - try_number))
        if try_number == 10:
            print(rocket_data.tail()['Company'])
            print(rocket_data.tail()['Fund_info'])
            print(rocket_data.tail()['Sub_info'])
        if try_number % 200 == 0:
            rocket_data.to_excel('./rocket_data_{}.xlsx'.format(try_number), index=False, encoding='cp949')
            print(try_number)
            time.sleep(30 + random())
            print(rocket_data.tail(1))
        url = data_1.loc[i, "Url"]
        company = data_1.loc[i, "Company"]
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
        rocket_data = rocket_data.append({'Url':url, 'Company':company,'Overview':overview,\
                                          "Category":category, "Fund_info": fund_list ,"Sub_info": sub_info,\
                                          "Service_description": service}, ignore_index=True)
        print(rocket_data.shape)
        driver.close()
        driver.switch_to.window(parent_window)
    driver.quit()
except Exception as e:
    print(e)
    rocket_data.to_excel('./rocket_data_{}.xlsx'.format(k), index=False, encoding='cp949')
#https://www.rocketpunch.com//companies/poinblack#funded
rocket_data = rocket_data.drop_duplicates(['Company'], keep='last')
rocket_data.to_excel('./rocket_data_{}.xlsx'.format(k), index=False, encoding='cp949')
