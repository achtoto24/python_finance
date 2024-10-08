import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database

#create_database("mysql+pymysql://root:0000@127.0.0.1:3306/exam")    # exam 데이터베이스 만들기

price = pd.DataFrame({
    "날짜" : ["2021-01-02", "2021-01-03"],
    "티커" : ["000001", "000001"],
    "종가" : [1340, 1315],
    "거래량" : [1000, 2000]
})

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/exam")
price.to_sql("price", con = engine, if_exists = "append", index = False)
data_sql = pd.read_sql("price", con = engine)
engine.dispose()


new = pd.DataFrame({
    "날짜" : ["2021-01-04"],
    "티커" : ["000001"],
    "종가" : [1320],
    "거래량" : [1500]
})
price = pd.concat([price, new])

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/exam")
price.to_sql("price", con = engine, if_exists = "append", index = False)
data_sql = pd.read_sql("price", con = engine)
engine.dispose()

""" 
테이블의 데이터들이 중복되는 문제가 발생, 기존의 데이터에 (기존 데이터 + 새로운 데이터)를 더하는 방식이기 때문
하지만 if_exists = replace로 할 경우에는 기존 데이터에 새로운 데이터로 대체되기 떄문에 제대로 업데이트를 할 수 x
"""