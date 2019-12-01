from urllib import parse
from bs4 import BeautifulSoup
from datetime import datetime
import json

from bs4 import BeautifulSoup
from selenium import webdriver
import time

url = "https://tv.naver.com/cjenm.producex101/playlists"

driver = webdriver.Chrome('driver/chromedriver')
driver.get(url)

found_element = True
while found_element:
    try:
        element = driver.find_element_by_xpath("//a[@class='bt_more']") # 더보기 div를 찾아서 클릭하는 것
        print(element)
        element.click()
        time.sleep(3) # wait for page loading

    except Exception:
        found_element = False

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

names = ["김요한", "김우석", "송형준", "이은상", "남도현", "김민규", "구정모", "한승우", "이진혁", "손동표", "차준호", "송유빈", "이한결", "조승연", "함원진", "금동현", "황윤성", "강민희", "이세진"]
data = []

video_lists = soup.find_all("ul", class_="item_list")
for i in range(len(video_lists)):
    video_list = video_lists[i]

    videos = video_list.find_all("li")
    for video in videos:
        if "단독" in video.text:
            title = video.find("tooltip")["title"]
            
            mentioned = []
            for name in names:
                if name[1:] in title:
                    mentioned.append(name)

            item = {
                "id": video.find("a")["href"],
                "title": title,
                "timestamp": (12 - i),
                "mentioned": mentioned,
                "view_count": video.find("span", class_ = "hit").text[4:],
                "like_count": video.find("span", class_ = "like").text[5:]
            }
            data.append(item)

for item in data:
    print(item["title"])
    print(item["mentioned"])
    print(item["view_count"])
    print(item["like_count"])