import pandas as pd
from sqlalchemy import create_engine

#create_engine("mysql+pymysql://[사용자명]:[비밀번호]@[호스트:포트]/[사용할 데이터베이스]")
engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/shop")

query = """select * from goods;"""
goods = pd.read_sql(query, con = engine)
engine.dispose()    # close connect

print(goods)