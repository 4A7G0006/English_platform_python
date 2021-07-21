import requests, random, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import urllib3
urllib3.disable_warnings()
ua = UserAgent()
User_Agent_choices = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 '
    'Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 '
    'Safari/604.5.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
    'Safari/537.36']
U_A = random.choice(User_Agent_choices)
headers1 = {'User-Agent': U_A,
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'}

headers2 = {'User-Agent': "'" + ua.random + "'"}

options = Options()
options.add_argument("--incognito")  # 開啟無痕模式
options.add_argument("--headless")  # 不開啟實體瀏覽器背景執行
options.add_argument('--no-sandbox')  # 繞過作業系統安全模型，最高權限運作
options.add_argument('--disable-gpu')  # 規避bug，僅適用於Windows操作系統
options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖片
options.add_argument('--disable-plugins')  # 不載入插件
browser = webdriver.Chrome("./chromedriver.exe", options=options)
delay_choices = [3, 4, 5, 6, 7]


def Connection_Check(html):
    if html.status_code != requests.codes.ok:
        return False
    else:
        return True


def Get_Next_Page(page, url):
    for p in range(1, page + 1):
        print("第" + str(p) + "頁")
        browser.get(url)
        U_A = random.choice(User_Agent_choices)
        r = requests.get(url, verify=False, headers={'User-Agent': U_A, 'Host': 'www.google.com', 'Referer': 'https://www.google.com/'})
        if Connection_Check(r):
            soup = BeautifulSoup(r.text, 'html.parser')
            for container in soup.find_all('div', class_='tF2Cxc'):
                title = container.find('h3').text
                href = container.find('a')['href']
                print(title)
                print(href)
                if href.strip()[-4:] == ".pdf" or href.strip()[:4] != "http" or href.strip()[-4:] == ".doc" or href.strip()[-4:] == ".ppt" or href.strip()[-4:] == ".PDF":
                    pass
                else:
                    with open("wenfa_V1.txt", "a", encoding='utf-8') as file:
                        file.write(href + "\n")
        else:
            print("disconnect")

        delay = random.choice(delay_choices)
        time.sleep(delay)
        try:
            if p < page:
                browser.find_element_by_link_text('下一頁').click()
                url = browser.current_url
        except:
            print('error')
            browser.quit()
            return


path = "./source.txt"
count = 1
link = "http://google.com/search?q="

with open(path, "r", encoding="utf-8") as search_file:
    for queries in search_file.read().splitlines():
        if count <= 3:
            search = link + queries
            print("現在正在搜尋:" + queries)
            Get_Next_Page(10, search)
            print("搜尋結束>> " + queries)
        else:
            quit()
        count = count + 1
browser.quit()
