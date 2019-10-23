from selenium import webdriver
import pandas as pd
import time, re
from random import randint
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:/Users/sunboangel/driver/chromedriver')
driver.implicitly_wait(5)
data = pd.DataFrame(columns=["Url", "Company", "Description"])
driver.get('https://www.rocketpunch.com/investments/funded_companies?page=1')
data = pd.DataFrame(columns=["Url", "Company","Description","Invest_num"])

for k in range(1, 110):
    page = k
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(page)
    for tags in soup.find('div', {'id':'company-list'}).findAll("div", {"class": "content"}):
        url = 'https://www.rocketpunch.com/' + tags.find('a', {'class':'link'})['href']
        try :
            company_name = tags.find('strong').text
            description = tags.find('div', {'class':'description'})
            if description is None: description = 'none'
            else: description = description.text.strip()
            invest_num = tags.find('a',{'class':'item'}).text
            invest_num = int(re.findall('\d+', invest_num)[0])
            data = data.append({'Url':url, 'Company':company_name, 'Description':description, "Invest_num":invest_num}, ignore_index=True)
        except AttributeError:
            print(tags.find('strong'))
            continue
    if page == 1:
        next = driver.find_element_by_xpath('//*[@id="search-results"]/div[3]/div/div[1]/a['+ str(2) +']')
    elif page < 5:
        next = driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div/div[1]/a['+ str(page+1) +']')
    else:
        next = driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div/div[1]/a[5]')
    try:
        next.click()
    except:
        try:
            close = driver.find_element_by_xpath('//*[@id="company_signup_popup"]/div[1]/i')
            close.click()
            time.sleep(1)
            next.click()
        except:
            next = driver.find_element_by_xpath('//*[@id="search-results"]/div[2]/div/div[1]/a[5]')
            next.click()
    if page % 20 == 0:
        time.sleep(5+randint(3,6))
    else:
        time.sleep(randint(3,6))
data.to_excel('./rocket_punch2.xlsx', index=False, encoding='cp949')
