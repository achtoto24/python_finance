import seaborn as sns
import pandas as pd
from sqlalchemy import create_engine

iris = sns.load_dataset("iris")

engine = create_engine("mysql+pymysql://root:0000@127.0.0.1:3306/shop")
iris.to_sql(name = "iris", con = engine, index = False, if_exists = "replace")  # index 생성 X, if_exists는 해당 테이블이 존재할 시 데이터 덮어씀
engine.dispose()