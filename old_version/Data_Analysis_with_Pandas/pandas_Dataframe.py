import pandas as pd
df = pd.DataFrame({'KOSPI' : [1915, 1961, 2026, 2467, 2041],
                   'KOSDAQ' : [542, 682, 631, 798, 675]},
                   index = [2014, 2015, 2016, 2017, 2018])
print(df)
print(df.describe())
print(df.info())

'''=========================================================='''
kospi = pd.Series([1915, 1961, 2026, 2467, 2041], index = [2014, 2015, 2016, 2017, 2018], name = 'KPSPI')
#print(kospi)
kosdaq = pd.Series([542, 682, 631, 798, 675], index = [2014, 2015, 2016, 2017, 2018], name = 'KOSDAQ')
#print(kosdaq)
df = pd.DataFrame({kospi.name : kospi, kosdaq.name : kosdaq})
print(df)

'''=========================================================='''
# forming DataFrame using a list
rows = []
rows.append([1915, 542])
rows.append([1961, 682])
rows.append([2026, 631])
rows.append([2067, 798])
rows.append([2041, 675])
df = pd.DataFrame(rows, columns = ['KOSPI', 'KOSDAQ'], index = [2014, 2015, 2016, 2017, 2018])
print(df)

'''=========================================================='''
for i in df.index :
    print(i, df['KOSPI'][i], df['KOSDAQ'][i])

for row in df.itertuples(name = 'KRX') :    #itertuples() is namedtuple
    print(row)

for row in df.itertuples() :
    print(row[0], row[1], row[2])

for idx, row in df.iterrows() :
    print(idx, row[0], row[1])


