from selenium import webdriver
import pandas as pd
import time
from random import randint, randrange, random
from bs4 import BeautifulSoup

k = input("시작할 순서 선택")
if k == '':
    k = 0
k = int(k)
print("%d에서 부터 시작합니다." % (k))

driver = webdriver.Chrome('C:/Users/LeeMH/chrome_driver/chromedriver')
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
data_1 = pd.read_excel('./rocket_punch2.xlsx')
rocket_data = pd.DataFrame(columns=["Url", "Company", "Description","Company_detail",\
                                    "Company_info", "Service_description"])
data_1.dropna(inplace=True)
left_data = list(data_1.index)[k:]
try_number = 0
try:
    for i in left_data:
        print("남은 데이터: %d" % (len(left_data)))
        try_number += 1
        if try_number == 10:
            print(rocket_data.tail()['Invest_amount'])
        if try_number % 200 == 0:
            rocket_data.to_excel('./rocket_data_{}.xlsx'.format(try_number), index=False, encoding='cp949')
            print(try_number)
            time.sleep(30 + random())
            print(rocket_data.tail(1))
        # url = data_1.loc[i, "Url"]
        url = 'https://www.rocketpunch.com/companies/kmong#funded'
        # company = data_1.loc[i, "Company"]
        company = '크몽'
        print(company)
        # description = data_1.loc[i, "Description"]
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
        investor = soup_child.findAll('div', {'class':'nowrap content'})
        inv_list = list()
        for inv in investor:
            try:
                inv_el = inv.find('a', {"class":"header nowrap"}).text
                print(inv_el)
            except AttributeError:
                print("Value is None")
            inv_list.append(inv_el)
            invest = ', '.join(list(set(inv_list)))
        com_info = soup_child.find('div', {'class':'ui segment company-info'}).findAll('div',{'class':'content'})
        com_info_list = [ci.text for ci in com_info]
        establish_date = com_info[0].text.strip().split()[0]
        try:
            company_year = com_info[0].text.strip().split()[2]
        except:
            company_year = None
        invest_amount = com_info[1].text.strip().split('\n')[0]
        if '명'in invest_amount:
            try:
                invest_amount = com_info[2].text.strip('\n')[0]
                print(invest_amount)
            except:
                invest_amount = None
        try:
            see_more = driver.find_element_by_xpath('//*[@id="company-overview"]/div/a')
            see_more.click()
            time.sleep(randrange(1,2) + random())
            company_intro = soup_child.find('span',{'class':'full-text'}).text.strip()
        except:
            try:
                company_intro = soup_child.find('div',{'class':'break content'}).text.strip()
            except AttributeError:
                company_intro = None

        try:
            service = soup_child.find('div', {'class':'product content item'}).find('div',{'class':'overview'}).text
        except AttributeError:
            service = None
        rocket_data = rocket_data.append({'Url':url, 'Company':company, 'Description':description,\
                                        'Establish_date':establish_date, 'Investor':invest,\
                                        'Company_detail':company_intro, "Service_description": service,\
                                        'Invest_amount':invest_amount, "Company_year":company_year, }, ignore_index=True)
        print(rocket_data.shape)
        driver.close()
        driver.switch_to.window(parent_window)
    driver.quit()
except:
    rocket_data.to_excel('./rocket_data_{}.xlsx'.format(k), index=False, encoding='cp949')
#https://www.rocketpunch.com//companies/poinblack#funded
rocket_data.to_excel('./rocket_data_{}.xlsx'.format(k), index=False, encoding='cp949')
