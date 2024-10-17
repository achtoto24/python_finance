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

#=========================================================================================

diff = list(set(krx_sector["종목명"]).symmetric_difference(set(krx_ind["종목명"])))
print(diff)

kor_ticker = pd.merge(krx_sector, krx_ind, on = krx_sector.columns.intersection(krx_ind.columns).tolist(), how='outer')

from tabulate import tabulate
print(tabulate(kor_ticker.head(40), headers='keys', tablefmt='pretty', showindex=False))
