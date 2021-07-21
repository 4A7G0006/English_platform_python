import time, random
import requests.packages.urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

requests.packages.urllib3.disable_warnings()

fake_user = UserAgent()
User_Agent_choices = [
    'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36']

headers = {
    'User-Agent': random.choice(User_Agent_choices),  # 隨機選擇fake_user agent
    # 'User-Agent': "'" + ua.random + "'",
    'Host': 'www.google.com',
    'Referer': 'https://www.google.com/%27%7D'}  # 選擇不同header減少連續嘗試發生錯誤

# headers = {'User-Agent': "'" + fake_user.random + "'"}
options = Options()
options.add_argument("--incognito")
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')  # 規避bug，僅適用於Windows操作系統
options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖片
options.add_argument('--disable-plugins')  # 不載入插件
driver = webdriver.Chrome("./chromedriver.exe")


# driver = webdriver.Chrome(options=options)


def get_page_title(page, Url):
    for page in range(1, page + 1):
        driver.get(Url)
        html = requests.get(Url, verify=False, headers=headers).content
        soup = BeautifulSoup(html, 'html.parser')
        for content in soup.find_all('div', class_='g'):  # 從網址中得到 google整頁的搜尋結果
            if str(content).find('class="g"') != -1:  # 只去抓取 google搜尋結果中的各選項 排除其他例外像是wiki出現的狀況 避免擷取錯誤
                print(content.find('h3').text)  # 取得各標頭
                print(content.find('a')['href'])  # 取得各標頭下的網址
                Extension = content.find('a')['href'].strip()[-4:]
                if Extension != ".pdf" or Extension != ".doc" or Extension != ".ppt":
                    with open("7000word_link.txt", "a", encoding='utf-8') as win:
                        win.write(content.find('a')['href'] + "\n")
                    pass
                else:
                    pass
        print("\n第" + str(page) + "頁\n")
        try:
            driver.find_element_by_link_text('下一頁').click()
            time.sleep(0.5)
            Url = driver.current_url  # 取得現在網頁
        except:
            print("這字搜尋完囉~")
            return


# file's search
path = ".\\"  # <<--- 7000單輸入路徑打這裡
page = 15
link = "http://google.com/search?q="

with open(path, "r", encoding="utf-8") as search_file:
    for queries in search_file.read().splitlines():
        search = link + queries
        print("現在正在搜尋:" + queries)
        get_page_title(page, search)
driver.quit()
