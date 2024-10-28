import pymysql
from sqlalchemy import create_engine
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
import re
from tqdm import tqdm
import time

# DB 연결
engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")
con = pymysql.connect(user = "root",
                      passwd = "0000",
                      host = "127.0.0.1",
                      db = "stock_db",
                      charset = "utf8"
                      )
mycursor = con.cursor()

# 티커리스트 불러오기
ticker_list = pd.read_sql("""
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
    and 종목구분 = "보통주";
    """, con = engine)

# DB 저장 쿼리
query = """
    insert into kor_fs (계정, 기준일, 값, 종목코드, 공시구분)
    values (%s, %s, %s, %s, %s)
    on duplicate key update
    값 = values(값)
"""

# 오류 발생 시 저장할 리스트 생성
error_list = []

# 재무제표 클렌징 함수
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

# for loop
for i in tqdm(range(0, len(ticker_list))):
    
    # 티커 선택
    ticker = ticker_list["종목코드"][i]

    #오류 발생 시 이를 무시하고 다음 루프로 진행
    try :
        url = f"http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A{ticker}"

        # 데이터 받아 오기
        data = pd.read_html(url, displayed_only=False)

        #연간 데이터 
        data_fs_y = pd.concat([data[0].iloc[:, ~data[0].columns.str.contains("전년동기")], data[2], data[4]])
        data_fs_y = data_fs_y.rename(columns={data_fs_y.columns[0] : "계정"})

        # 결산년 찾기
        page_data = rq.get(url)
        page_data_html = BeautifulSoup(page_data.content, "html.parser")

        fiscal_data = page_data_html.select("div.corp_group1 > h2")
        fiscal_data_text = fiscal_data[1].text
        fiscal_data_text = re.findall("[0-9]+", fiscal_data_text)

        # 결산년에 해당하는 계정만 남기기
        data_fs_y = data_fs_y.loc[:, (data_fs_y.columns == "계정") | (data_fs_y.columns.str[-2:].isin(fiscal_data_text))]

        # 클렌징
        data_fs_y_clean = clean_fs(data_fs_y, ticker, 'y')

        # 분기 데이터
        data_fs_q = pd.concat(
        [data[1].iloc[:, ~data[1].columns.str.contains("전년동기")], data[3], data[5]])
        data_fs_q = data_fs_q.rename(columns={data_fs_q.columns[0]:"계정"})

        data_fs_q_clean = clean_fs(data_fs_q, ticker, 'q')

        # 2개 합치기
        data_fs_bind = pd.concat([data_fs_y_clean, data_fs_q_clean])

        # 재무제표 데이터를 DB에 저장
        args = data_fs_bind.values.tolist()
        mycursor.executemany(query, args)
        con.commit()

    except :
        # 오류 발생 시 해당 종목명을 저장하고 다음 루프로 이동
        print(ticker)
        error_list.append(ticker)

    # 타임슬립 적용 
    time.sleep(2)

# DB 연결 종료
engine.dispose()
con.close()