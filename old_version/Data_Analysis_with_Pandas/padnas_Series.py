import pandas as pd
import matplotlib.pyplot as plt

s = pd.Series([0.0, 3.6, 2.0, 5.8, 4.2, 8.0])   #receive a list as a constructor argument for Series
print(s)
s.index = pd.Index([0.0, 1.2, 1.8, 3.0, 3.6, 4.8])
s.index.name = 'MY_IDX'
s.name = 'MY_SERIES'
s[5.9] = 5.5
print(s)

ser = pd.Series([6.7, 4.2], index = [6.8, 8.0]) #make new Series
#s = s.append(ser)
#print(s)

'''======================================================================='''
print()
print(s.index[-1], ':', s.values[-1])
print(s.loc[1.8])   #location indexer
print(s.iloc[2])    #integer location indexer
print()
print("s.values()_result : ", s.values[:])
print("s.iloc_result : ", s.iloc[:])
s = s.drop(5.9)
print(s)
print(s.describe())

'''======================================================================='''
plt.title("ELLIOT_WAVE")  
plt.plot(s, 'bs--') # 시리즈를 bs--(푸른 사각형과 점선) 형태로 출력
plt.xticks(s.index) 
plt.yticks(s.values)
plt.grid(True)
print(plt.show())







