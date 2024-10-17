import requests as rq
from bs4 import BeautifulSoup

url = "https://finance.naver.com/sise/sise_deposit.naver"
data = rq.get(url)
# print(data)
data_html = BeautifulSoup(data.content)

# 날짜가 중복되서 여러 개 반환될 경우, select()가 아닌 select_one()을 사용함
parse_day = data_html.select_one(
    "div.subtop_sise_graph2 > ul.subtop_chart_note > li > span.tah"
).text

#print(parse_day)

import re

biz_day = "".join(re.findall("[0-9]+", parse_day))

#print(biz_day)
#print()