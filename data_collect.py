from bs4 import BeautifulSoup
import requests

url = 'http://smroadmap.smtech.go.kr/'
user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
req = requests.get(url, headers= user_agent, auth=('user', 'pass'))

soup = BeautifulSoup(req.text, 'html.parser')
forth = soup.findAll("li", {"class":"color01"})

big_category = dict()
for cat in forth:
    key = cat.find('p', {'class':'i-name'}).text
    first_url = cat.find('article', {"class":"group"}).find('h2').find('a')['href']
    big_category[key] = 'http://smroadmap.smtech.go.kr/' + first_url

download_dict = dict()
for key in big_category.keys():
    print(key)
    req2 = requests.get(big_category[key], headers= user_agent, auth=('user', 'pass'))
    soup2 = BeautifulSoup(req2.text, 'html.parser')
    download_url = soup2.find('span', {'class':'res_ttBtn'}).find('a')['href']
    download_dict[key] = 'http://smroadmap.smtech.go.kr' + download_url


def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = requests.get(url)               # get request
        file.write(response.content)      # write to file

for d_key in list(download_dict.keys())[10:]:
    file_key = d_key
    if '/' in d_key:
        print(d_key)
        file_key = d_key.replace('/','_')
    download(download_dict[d_key], '../roadmap/raw/2018/2018_{}.pdf'.format(file_key))

past_url_dict = dict()
year_list = [2016, 2017]
for year in year_list:
    past_url = 'http://smroadmap.smtech.go.kr/0301/index/year/{}'.format(year)
    req_past = requests.get(past_url, headers= user_agent, auth=('user', 'pass'))
    soup_past = BeautifulSoup(req_past.text, 'html.parser')
    url_list = soup_past.find('ul', {'class':'tab-style01 down-list02'}).findAll('a')
    for url in url_list:
        url_key =  'http://smroadmap.smtech.go.kr' + url['href']
        if '/' in url.text:
            print(url.text)
            file_key = url.text.replace('/','_')
        else:
            file_key = url.text
        download(url_key, '../roadmap/raw/{0}/{0}_{1}.pdf'.format(year, file_key))
