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

notice_url = f'''https://opendart.fss.or.kr/api/list.json?crtfc_key={api_key}
&bgn_de={bgn_date}&end_de={end_date}&page_no=1&page_count=100'''

notice_data = rq.get(notice_url)
notice_data_df = notice_data.json().get("list")
notice_data_df = pd.DataFrame(notice_data_df)

print(notice_data_df.tail())