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