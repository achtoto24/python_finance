import keyring

keyring.set_password("dart_api_key", "ach_toto24", "b7d6699289ce7d57b1bd6b4630d2c269cf8a9221")
api_key = keyring.get_password("dart_api_key", "ach_toto24")

import json
import pandas as pd
import requests as rq

corp_code = "00126380"  # 기업('삼성') 고유 번호
bsns_year = "2023"      # 사업연도
reprt_code = "11011"     # 보고서 코드

url_div = f'''https://opendart.fss.or.kr/api/alotMatter.json?crtfc_key={api_key}
&corp_code={corp_code}&bsns_year={bsns_year}&reprt_code={reprt_code}'''

div_data_ss = rq.get(url_div)
div_data_ss_df = div_data_ss.json().get("list")
div_data_ss_df = pd.DataFrame(div_data_ss_df)

print(div_data_ss_df)