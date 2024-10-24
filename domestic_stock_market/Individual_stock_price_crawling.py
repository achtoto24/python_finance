from sqlalchemy import create_engine
import pandas as pd

# mysql 데이터베이스에서 조건에 충족하는 데이터를 데이터프레임 형식으로 가져오기
engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")
query = """
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
    and 종목구분 = "보통주";
"""

ticker_list = pd.read_sql(query, con=engine)
engine.dispose()

from tabulate import tabulate

print(tabulate(ticker_list.head(), headers='keys', tablefmt='pretty', showindex=False))

#==================================================================================================================
print()

# 개별종목 주가 크롤링
from dateutil.relativedelta import relativedelta
import requests as rq
from io import BytesIO
from datetime import date

i = 0
ticker = ticker_list["종목코드"][i]
fr = (date.today() + relativedelta(years=-5)).strftime("%Y%m%d")
to = (date.today()).strftime("%Y%m%d")

url = f"""https://m.stock.naver.com/front-api/external/chart/domestic/info?symbol={ticker}&requestType=1
&startTime={fr}&endTime={to}&timeframe=day"""

data = rq.get(url).content

data_price = pd.read_csv(BytesIO(data))

print(tabulate(data_price.head(), headers='keys', tablefmt='pretty', showindex=False))

#==================================================================================================================
print()

# 데이터 클렌징
import re

price = data_price.iloc[:, 0:6]     #전체 행, 0번째부터 5번째 열까지 
price.columns = ["날짜", "시가", "고가", "저가", "종가", "거래량"]
price = price.dropna()  # NA 데이터 삭제
price["날짜"] = price["날짜"].str.extract("(\d+)")  # 숫자만 추출
price["날짜"] = pd.to_datetime(price["날짜"])
price["종목코드"] = ticker

print(tabulate(price.head(), headers='keys', tablefmt='pretty', showindex=False))
