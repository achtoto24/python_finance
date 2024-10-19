import requests as rq
from io import BytesIO
import pandas as pd

import recent_business_day

biz_day = recent_business_day.biz_day

gen_otp_url = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"

# KOSPI
gen_otp_stk = {
    'locale' : 'ko_KR',
    'mktId' : 'STK',
    'trdDd' : biz_day,
    'money' : '1',
    'csvxls_isNo' : 'false',
    'name' : 'fileDown',
    'url' : 'dbms/MDC/STAT/standard/MDCSTAT03901'
}

headers = {"Referer" : "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}  # referer란 링크를 통해서 각각의 웹사이트로 방문할 때 남는 흔적

otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers=headers).text
down_url = "http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
down_sector_stk = rq.post(down_url, {"code" : otp_stk}, headers=headers)
sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding="EUC-KR")

# KOSDAQ
gen_otp_ksq = {
    'locale' : 'ko_KR',
    'mktId' : 'KSQ',
    'trdDd' : biz_day,
    'money' : '1',
    'csvxls_isNo' : 'false',
    'name' : 'fileDown',
    'url' : 'dbms/MDC/STAT/standard/MDCSTAT03901'
}
otp_ksq = rq.post(gen_otp_url, gen_otp_ksq, headers=headers).text
down_sector_ksq = rq.post(down_url, {"code" : otp_ksq}, headers=headers)
sector_ksq = pd.read_csv(BytesIO(down_sector_ksq.content), encoding="EUC-KR")

krx_sector = pd.concat([sector_stk, sector_ksq]).reset_index(drop=True)
krx_sector["종목명"] = krx_sector["종목명"].str.strip()     
krx_sector["기준일"] = "2024.10.11"

#individual_stock_indicators

gen_otp_url = "http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd"
gen_otp_data = {
    'locale' : 'ko_KR',
    'searchType' : '1',
    'mktId' : 'ALL',
    'trdDd': biz_day,
    'csvxls_isNo' : 'false',
    'name' : 'fileDown',
    'url' : 'dbms/MDC/STAT/standard/MDCSTAT03501'
}

headers = {"Referer" : "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}
otp = rq.post(gen_otp_url, gen_otp_data, headers=headers).text

down_url = "http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"
krx_ind = rq.post(down_url, {"code" : otp}, headers=headers)
krx_ind = pd.read_csv(BytesIO(krx_ind.content), encoding = "EUC-KR")
krx_ind["종목명"] = krx_ind["종목명"].str.strip()
krx_ind["기준일"] = biz_day

#==========================================================================================================================================

diff = list(set(krx_sector["종목명"]).symmetric_difference(set(krx_ind["종목명"])))
#print(diff)

kor_ticker = pd.merge(krx_sector, krx_ind, on = krx_sector.columns.intersection(krx_ind.columns).tolist(), how='outer')

# from tabulate import tabulate
# print(tabulate(kor_ticker.head(40), headers='keys', tablefmt='pretty', showindex=False))

# print(kor_ticker[kor_ticker["종목명"].str.contains("스팩|제[0-9]+호")]["종목명"].values)   # 스팩 종목 찾기
# print()
# print(kor_ticker[kor_ticker["종목코드"].str[-1:] != '0']["종목명"].values)  # 보통주가 아닌 우선주 찾기
# print()
# print(kor_ticker[kor_ticker["종목명"].str.endswith("리츠")]["종목명"].values)   # 리츠 종목 찾기

import numpy as np

kor_ticker["종목구분"] = np.where(kor_ticker["종목명"].str.contains("스팩|제[0-9]+호"), "스팩", 
                        np.where(kor_ticker["종목코드"].str[-1:] != '0', "우선주",
                        np.where(kor_ticker["종목명"].str.endswith("리츠"), "리츠", 
                        np.where(kor_ticker["종목명"].isin(diff), "기타", "보통주"
                        ))))

kor_ticker = kor_ticker.reset_index(drop=True)
kor_ticker.columns = kor_ticker.columns.str.replace(' ', '')
kor_ticker = kor_ticker[["종목코드", "종목명", "시장구분", "종가", "시가총액", "기준일", "EPS", "선행EPS", "BPS", "주당배당금", "종목구분"]]
kor_ticker = kor_ticker.replace({np.nan: None}) # nan -> None 바꾸기
kor_ticker = kor_ticker.drop_duplicates(subset=["종목코드", "종목명"], keep='first')    # 중복된 종목 내용 제거
kor_ticker["기준일"] = pd.to_datetime(kor_ticker["기준일"])

print(kor_ticker.head(20))

#==========================================================================================================================================

import pymysql

con = pymysql.connect(user = "root",
                      passwd = "0000",
                      host = "127.0.0.1",
                      db = "stock_db",
                      charset = "utf8")

mycursor = con.cursor()
query = f""" 
        INSERT INTO kor_ticker (종목코드, 종목명, 시장구분, 종가, 시가총액, 기준일, EPS, 선행EPS, BPS, 주당배당금, 종목구분)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        종목명 = VALUES(종목명), 시장구분 = VALUES(시장구분), 종가 = VALUES(종가), 
        시가총액 = VALUES(시가총액), EPS = VALUES(EPS), 선행EPS = VALUES(선행EPS),
        BPS = VALUES(BPS), 주당배당금 = VALUES(주당배당금), 종목구분 = VALUES(종목구분);
        """

args = kor_ticker.values.tolist()

mycursor.executemany(query, args)
con.commit()

con.close()