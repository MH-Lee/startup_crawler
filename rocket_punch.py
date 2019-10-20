from selenium import webdriver
import pandas as pd
import time
from random import randint
from bs4 import BeautifulSoup

driver = webdriver.Chrome('C:/Users/LeeMH/chrome_driver/chromedriver')
driver.implicitly_wait(5)
data = pd.DataFrame(columns=["Url", "Company", "Description"])
driver.get('https://www.rocketpunch.com/investments/funded_companies?page=1')

for k in range(1, 100):
    page = k
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    if page == 1:
        i = 5
    else:
        i = 1
    print(page)
    for tags in soup.findAll('a', {'class':'link'})[i:-3]:
        url = 'https://www.rocketpunch.com/' + tags['href']
        try :
            company_name = tags.find('strong').text
            description = tags.find('div', {'class':'description'}).text.strip()

            data = data.append({'Url':url, 'Company':company_name, 'Description':description}, ignore_index=True)
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
    time.sleep(randint(3,6))
data.to_csv('./rocket_punch2.csv', index=False)
data.to_excel('./rocket_punch2.xlsx', index=False, encoding='cp949')


driver.execute_script("window.open('{}')".format(url))
all_windows = driver.window_handles
child_window = [window for window in all_windows if window != parent_window][0]
driver.switch_to.window(child_window)
html_child = driver.page_source
soup_child = BeautifulSoup(html_child, 'html.parser')
investor = soup_child.findAll('div', {'class':'nowrap content'})
inv_list = list()
for inv in investor:
    inv_list.append(inv.find('a', {'class':'header nowrap'}).text)
    invest = ', '.join(inv_list)
invest
com_info = soup_child.find('div', {'class':'ui segment company-info'}).findAll('div',{'class':'content'})
establish_date = com_info[0].text.strip().split()[0]
company_year = com_info[0].text.strip().split()[2]
driver.close()
driver.switch_to.window(parent_window)
