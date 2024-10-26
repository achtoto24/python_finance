from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")
query = """
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
    and 종목구분 = "보통주";
"""

ticker_list = pd.read_sql(query, con = engine)
engine.dispose()

i = 0
ticker = ticker_list["종목코드"][i]

url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}"

data = pd.read_html(url, displayed_only=False)  # displayed_only=Flase는 해당 url페이지에서 안 보이는 내용까지 전부 추출함

'''
data 즉 재무제표 내역에는 
[0] : 포괄손익계산서(연간)
[1] : 포괄손익계산서(분기)
[2] : 재무상태표(연간)
[3] : 재무상태표(분기)
[4] : 현금흐름표(연간)
[5] : 현금흐름표(분기)
'''
print(data[0].columns.tolist(), '\n',   # 연간 기준 포괄손익계산서
      data[2].columns.tolist(), '\n',   # 연간 기준 재무상태표
      data[4].columns.tolist()          # 연간 기준 현금흐름표
      )
print()
data_fs_y = pd.concat(
    [data[0].iloc[:, ~data[0].columns.str.contains("전년동기")], data[2], data[4]]  # iloc columns부분에서 "전년동기"가 들어간 열은 뺌
    )
data_fs_y = data_fs_y.rename(columns={data_fs_y.columns[0] : "계정"})

from tabulate import tabulate
print(tabulate(data_fs_y.head(), headers='keys', tablefmt='pretty', showindex=False))

#=========================================================================================================
print()

#연간 재무제표 날짜만 추출하기
import requests as rq
from bs4 import BeautifulSoup
import re

page_data = rq.get(url)
page_data_html = BeautifulSoup(page_data.content, "html.parser")

fiscal_data = page_data_html.select("div.corp_group1 > h2")
fiscal_data_text = fiscal_data[1].text
fiscal_data_text = re.findall("[0-9]+", fiscal_data_text)
print(fiscal_data_text)
print()
data_fs_y = data_fs_y.loc[:, (data_fs_y.columns == "계정") | (data_fs_y.columns.str[-2:].isin(fiscal_data_text))]   # 열 이름이 '계정'인 것과 끝 두 글자가 '12'로 되어 있는 것들만 추출
print(tabulate(data_fs_y.head(), headers='keys', tablefmt='pretty', showindex=False))

