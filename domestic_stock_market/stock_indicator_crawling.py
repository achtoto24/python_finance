import requests as rq
from io import BytesIO
import pandas as pd

import recent_business_day

biz_day = recent_business_day.biz_day

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

'''cmd창에서 예쁘게 출력하기'''
from tabulate import tabulate

# DataFrame을 표 형식으로 출력
print(tabulate(krx_ind.head(), headers='keys', tablefmt='pretty', showindex=False))


