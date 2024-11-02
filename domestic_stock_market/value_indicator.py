from sqlalchemy import create_engine
import pandas as pd

"""삼성전자 분기 재무제표 불러오기"""

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/stock_db")

tikcer_list = pd.read_sql("""
    select * from kor_ticker
    where 기준일 = (select max(기준일) from kor_ticker)
          and 종목구분 = "보통주";
    """, con=engine)

sample_fs = pd.read_sql("""
    select * from kor_fs
    where 공시구분 = 'q'
    and 종목코드 = '005930'
    and 계정 in ("당기순이익", "자본", "영업활동으로인한현금흐름", "매출액");
    """, con=engine)

engine.dispose()    # DB와의 연결 종료

sample_fs = sample_fs.sort_values(["종목코드", "계정", "기준일"])

from tabulate import tabulate

# print(tabulate(sample_fs, headers='keys', tablefmt='pretty', showindex=False))

#===========================================================================================================

"""삼성전자 가치지표 추출하기"""

"""최근 4분기 데이터를 이용해 계산하는 TTM(Trailing Twelve Months) 방법을 많이 사용함"""

sample_fs["ttm"] = sample_fs.groupby(
    ["종목코드", "계정"], as_index=False)["값"].rolling(window=4, min_periods=4).sum()["값"]    # rolling()을 통해 4개 기간씩 합계를 구함, min_periods 인자를 통해 데이터가 최소 4개는 있을 경우에만 값을 구함, 

# print(tabulate(sample_fs, headers='keys', tablefmt='pretty', showindex=False))

import numpy as np

# "ttm" 열에 조건 달기
sample_fs["ttm"] = np.where(sample_fs["계정"] == "자본", sample_fs["ttm"] / 4, sample_fs["ttm"])    # np.where(조건식, 참값, 거짓값)을 통해 이전 값들 수정
sample_fs = sample_fs.groupby(["계정", "종목코드"]).tail(1) # tail(1)을 통해 가장 최근 데이터만 선택함

# print(tabulate(sample_fs, headers='keys', tablefmt='pretty', showindex=False))

# "시가총액", "기준일" 열 추가하기 
sample_fs_merge = sample_fs[["계정", "종목코드", "ttm"]].merge(
    tikcer_list[["종목코드", "시가총액", "기준일"]], on = "종목코드")
sample_fs_merge["시가총액"] = sample_fs_merge["시가총액"] / 100000000   # 억 단위로 수정

# print(tabulate(sample_fs_merge, headers='keys', tablefmt='pretty', showindex=False))

sample_fs_merge["value"] = sample_fs_merge["시가총액"] / sample_fs_merge["ttm"]
sample_fs_merge["지표"] = np.where(sample_fs_merge["계정"] == "매출액", "PSR",
                                 np.where(sample_fs_merge["계정"] == "영업활동으로인한현금흐름", "PCR",
                                          np.where(sample_fs_merge["계정"] == "자본", "PBR",
                                                   np.where(sample_fs_merge["계정"] == "당기순이익", "PER", None))))

print(tabulate(sample_fs_merge, headers='keys', tablefmt='pretty', showindex=False))
print()
# 배당수익률 계산하기 
tikcer_list_sample = tikcer_list[tikcer_list["종목코드"] == "005930"].copy()
tikcer_list_sample["DY"] = tikcer_list_sample["주당배당금"] / tikcer_list_sample["종가"]

print(tabulate(tikcer_list_sample, headers='keys', tablefmt='pretty', showindex=False))
