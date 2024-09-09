import yfinance as yf
import matplotlib.pyplot as plt

aapl = yf.download('AAPL', start='2022-08-01')
pltr = yf.download('PLTR', start='2022-08-01')

#print(appl.head(10))
#pltr = pltr.drop(columns='Adj Close')
#print(pltr.tail(10))
#print(pltr.index)
#print(pltr.columns)


plt.plot(aapl.index, aapl.Close, 'black', label = 'AAPL')
plt.plot(pltr.index, pltr.Close, 'b', label = 'PALANTIR')
plt.legend(loc = 'best')
print(plt.show())

aapl_rate = (aapl['Close'] / aapl['Close'].shift(1) - 1) * 100
aapl_rate.iloc[0] = 0
plt.hist(aapl_rate, bins = 20)
plt.grid(True)
print(plt.show())
print(aapl_rate.describe())