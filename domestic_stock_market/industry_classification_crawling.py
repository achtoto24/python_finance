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
''' 
header부분에 우리가 서버를 거쳐온 과정(첫번째 URL로부터 otp를 받고 두번째 URL에 otp를 제출하여 원하는 파일 다운로드)
을 흔적으로 남겨야 데이터를 받을 수 있음, 만약 두 번째 URL만 거친다면 서버는 우리를 로봇으로 판단함
'''

otp_stk = rq.post(gen_otp_url, gen_otp_stk, headers=headers).text

down_url = "http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd"

down_sector_stk = rq.post(down_url, {"code" : otp_stk}, headers=headers)
sector_stk = pd.read_csv(BytesIO(down_sector_stk.content), encoding="EUC-KR")

#=======================================================================================
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

#=======================================================================================

krx_sector = pd.concat([sector_stk, sector_ksq]).reset_index(drop=True)
krx_sector["종목명"] = krx_sector["종목명"].str.strip()     # strip()은 공백을 없애줌
krx_sector["기준일"] = "2024.10.11"

print(krx_sector.head())


