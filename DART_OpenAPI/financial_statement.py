import keyring

keyring.set_password("dart_api_key", "ach_toto24", "b7d6699289ce7d57b1bd6b4630d2c269cf8a9221")
api_key = keyring.get_password("dart_api_key", "ach_toto24")

import json
import pandas as pd
import requests as rq

corp_code = "00126380"  # 기업('삼성') 고유 번호
bsns_year = "2021"      # 사업연도
reprt_code = "11011"     # 보고서 코드

url_fs = f'''https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={api_key}
&corp_code={corp_code}&bsns_year={bsns_year}&reprt_code={reprt_code}&fs_div=OFS'''

fs_data_ss = rq.get(url_fs)
fs_data_ss_df = fs_data_ss.json().get("list")
fs_data_ss_df = pd.DataFrame(fs_data_ss_df)

print(fs_data_ss_df.head())