import keyring

keyring.set_password("dart_api_key", "ach_toto24", "b7d6699289ce7d57b1bd6b4630d2c269cf8a9221")

api_key = keyring.get_password("dart_api_key", "ach_toto24")

import requests as rq
from io import BytesIO
import zipfile

codezip_url = f'''https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}'''
codezip_data = rq.get(codezip_url)
print(codezip_data.headers)
print()
print(codezip_data.headers["Content-Disposition"])  # CORPCODE.zip 파일로 압축됨

# 압축 풀기
codezip_file = zipfile.ZipFile(BytesIO(codezip_data.content))
#print(codezip_file.namelist())
#print(codezip_file.read("CORPCODE.xml").decode("utf-8"))

import xmltodict
import json
import pandas as pd
code_data = codezip_file.read("CORPCODE.xml").decode("utf-8")   # xml 파일 형태
data_odict = xmltodict.parse(code_data)    # 딕셔너리 형태로 변경
data_dict = json.loads(json.dumps(data_odict))  # 위 데이터를 dumps() 함수를 통해 JSON 형태로 바꿔 준 후, loads() 함수를 통해 불러옴
data = data_dict.get("result").get("list")  # get() 함수를 통해 result 내에서 list 부분만 불러옴
corp_list = pd.DataFrame(data)

print(corp_list.head())

# stock_code가 None 즉 상장되지 않은 종목은 삭제해 줌
corp_list = corp_list[~corp_list.stock_code.isin([None])].reset_index(drop=True)

import pymysql
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")
corp_list.to_sql(name="dart_code", con=engine, index=True, if_exists="replace")

