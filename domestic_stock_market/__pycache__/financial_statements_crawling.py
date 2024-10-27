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

#=========================================================================================================

#데이터 클렌징
def clean_fs (df, ticker, frequency) :
    
    df = df[~df.loc[:, ~df.columns.isin(["계정"])].isna().all(axis=1)]               # 모든 연도의 데이터가 NaN인 항목은 제외
    df = df.drop_duplicates(["계정"], keep="first")                                  # 계정명이 중복되는 경우 drop_duplicates() 함수를 이용해 첫 번째에 위치하는 데이터만 남김
    df = pd.melt(df, id_vars="계정", var_name="기준일", value_name="값")              # melt() 함수를 이용해 열로 긴 데이터를 행으로 긴 데이터로 변경함
    df = df[~pd.isnull(df["값"])]                                                    # 계정값이 없는 항목은 제외
    df["계정"] = df["계정"].replace({"계산에 참여한 계정 펼치기" : ''}, regex=True)     # '계산에 참여한 계정 펼치기'라는 글자는 실제 페이지의 [+]에 해당하는 부분이므로 replace() 메서드로 제거함
    df["기준일"] = df["기준일"].str.replace('/', '-')                                 # '기준일' 열 값을 수정하기
    df["기준일"] = pd.to_datetime(df["기준일"], 
                                format="%Y-%m") + pd.tseries.offsets.MonthEnd()      # to_datetime() 메서드를 통해 기준일을 'yyyy-mm'형태로 바꾼 후, MonthEnd()를 통해 월말에 해당하는 일을 붙임
    df["종목코드"] = ticker
    df["공시구분"] = frequency                                                        # '공시구분' 열에는 연간 또는 분기에 해당하는 값을 입력함

    return df

data_fs_y_clean = clean_fs(data_fs_y, ticker, 'y')
# print(data_fs_y_clean.head())
data_fs_q = pd.concat(
    [data[1].iloc[:, ~data[1].columns.str.contains("전년동기")], data[3], data[5]])
data_fs_q = data_fs_q.rename(columns={data_fs_q.columns[0]:"계정"})

data_fs_q_clean = clean_fs(data_fs_q, ticker, 'q')

data_fs_bind = pd.concat([data_fs_y_clean, data_fs_q_clean])
print(tabulate(data_fs_bind.head(), headers='keys', tablefmt='pretty', showindex=False))