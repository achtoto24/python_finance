import pymysql
from sqlalchemy import create_engine
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import requests as rq
import time
from tqdm import tqdm
from io import BytesIO

# DB 연결
engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")
con = pymysql.connect(user = "root",
                      passwd = "0000",
                      host = "127.0.0.1",
                      db = "stock_db",
                      charset = "utf8"
                      )
mycursor = con.cursor()     # 커서 객체 불러오기

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
    and 종목구분 = "보통주";
    """, con = engine)

# DB 저장 쿼리
query = """
    insert into kor_price (날짜, 시가, 고가, 저가, 종가, 거래량, 종목코드)
    values (%s, %s, %s, %s, %s, %s, %s) 
    on duplicate key update
    시가 = values(시가), 고가 = values(고가), 저가 = values(저가),
    종가 = values(종가), 거래량 = values(거래량);
"""

# 오류 발생 시 저장할 리스트 생성
error_list = []

# 전 종목 주가 다운로드 및 저장
for i in tqdm(range(0, len(ticker_list))) :

    # 티커선택
    ticker = ticker_list["종목코드"][i]

    # 시작일과 종료일
    fr = (date.today() + relativedelta(years= - 5)).strftime("%Y%m%d")
    to = (date.today()).strftime("%Y%m%d")

    # 오류 발생 시 이를 무시하고 다음 루프로 진행
    try : 
        url = f"""https://m.stock.naver.com/front-api/external/chart/domestic/info?symbol={ticker}&requestType=1
            &startTime={fr}&endTime={to}&timeframe=day"""
        
        data = rq.get(url).content
        data_price = pd.read_csv(BytesIO(data))

        price = data_price.iloc[:, 0:6]
        price.columns = ["날짜", "시가", "고가", "저가", "종가", "거래량"]
        price = price.dropna()
        price["날짜"] = price["날짜"].str.extract("(\d+)")
        price["날짜"] = pd.to_datetime(price["날짜"])
        price["종목코드"] = ticker

        args = price.values.tolist()
        mycursor.executemany(query, args)
        con.commit()

    except :
        # 오류 발생 시 error_list에 티커 저장하고 넘어가기
        print(ticker)
        error_list.append(ticker)

    time.sleep(2)

engine.dispose()
con.close()

'''
절대 실행하지 말 것!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
이미 한 번 실행함!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
'''