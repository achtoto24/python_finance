import time
import json
import requests as rq
import pandas as pd
from tqdm import tqdm

import recent_business_day

biz_day = recent_business_day.biz_day

sector_code = [
    "G25", "G35", "G50", "G40", "G10", "G20", "G55", "G30", "G15", "G45"
]

data_sector = []

for i in tqdm(sector_code) :    # tqdm()은 진행속도를 확인해 줌 
    url = f'''https://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt={biz_day}&sec_cd={i}'''
    data = rq.get(url).json()   # json 형식의 파일로 요청
    data_pd = pd.json_normalize(data["list"])   # Dictionary 형태를 DataFrame 형태로 바꿈
    
    data_sector.append(data_pd)

    time.sleep(2)

kor_sector = pd.concat(data_sector, axis=0)
kor_sector = kor_sector[["IDX_CD", "CMP_CD", "CMP_KOR", "SEC_NM_KOR"]]
kor_sector["기준일"] = biz_day
kor_sector["기준일"] = pd.to_datetime(kor_sector["기준일"])

import pymysql

con = pymysql.connect(user = "root",
                      passwd="0000",
                      host="127.0.0.1",
                      db="stock_db",
                      charset="utf8")

mycursor = con.cursor()
query = f"""
    insert into kor_sector (IDX_CD, CMP_CD, CMP_KOR, SEC_NM_KOR, 기준일)
    values (%s,%s,%s,%s,%s) 
    on duplicate key update
    IDX_CD = values(IDX_CD), CMP_KOR = values(CMP_KOR), SEC_NM_KOR = values(SEC_NM_KOR) 
"""

args = kor_sector.values.tolist()

mycursor.executemany(query, args)
con.commit()

con.close()