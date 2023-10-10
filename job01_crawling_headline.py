from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import datetime

category = ['Politic', 'Economic', 'Social', 'Culture', 'World', 'IT']
url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"}
# as if the client is a web browser

# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# title_tags = soup.select('.sh_text_headline')
#
# titles = []
# for title_tag in title_tags:
#     titles.append(re.compile('[^가-힣|a-z|A-Z]').sub(' ', title_tag.text))

df_titles = pd.DataFrame()
title_pattern = re.compile('[^가-힣|a-z|A-Z]')

for i in range(len(category)):
    response = requests.get(url[:-1] + str(i), headers=headers)
