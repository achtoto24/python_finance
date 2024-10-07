import pymysql

con = pymysql.connect(
    user = "root",
    passwd = "0000",
    host = "127.0.0.1",  # typical localhost
    db = "shop",
    charset = "utf8"
)

mycursor = con.cursor() # mycursor는 데이터베이스에서 데이터 중에서 특정 위치, 특정 행을 가르킬 때 사용, 즉 현재 작업 중인 행을 나타내는 객체

query = """
select * from goods;
"""

print(mycursor.execute(query))  # send the query to database through execute()  

data = mycursor.fetchall()  # load all data from mysql server through fetchall()
print(data)

query = """
    insert into goods (goods_id, goods_name, goods_classify, sell_price, buy_price, register_date)
    values ("0009", "스테이플러", "사무용품", "2000", "1500", "2020-12-30");
"""
print(mycursor.execute(query))
con.commit()    # 데이터의 확정 갱신하는 작업 실행

con.close() # close connect with database