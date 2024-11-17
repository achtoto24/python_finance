import keyring

keyring.set_password("dart_api_key", "ach_toto24", "b7d6699289ce7d57b1bd6b4630d2c269cf8a9221")
api_key = keyring.get_password("dart_api_key", "ach_toto24")

import json
import pandas as pd
import requests as rq
from datetime import date
from dateutil.relativedelta import relativedelta

bgn_date = (date.today() + relativedelta(days= -7)).strftime("%Y%m%d")
end_date = (date.today()).strftime("%Y%m%d")
corp_code = "00126380"

notice_url_ss = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}
&corp_code={corp_code}&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data_ss = rq.get(notice_url_ss)
notice_data_ss_df = notice_data_ss.json().get("list")
notice_data_ss_df = pd.DataFrame(notice_data_ss_df)

print(notice_data_ss_df.tail())     # 츌력에서 'rcept_no'는 공시번호에 해당함
print()

# 해당 공시 보고서 페이지 url 추출하기
notice_url_exam = notice_data_ss_df.loc[2, "rcept_no"]
notice_dart_url = f'''http://dart.fss.or.kr/dsaf001/main.do?rcpNo={notice_url_exam}'''

print("url : " + notice_dart_url)

