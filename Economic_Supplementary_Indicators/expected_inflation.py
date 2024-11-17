import pandas_datareader as web
import pandas as pd

bei = web.DataReader("T10YIE", "fred", start = "2000-01-01")

print(bei.tail())

import matplotlib.pyplot as plt

bei.plot(figsize = (10, 6), grid = True)
plt.axhline(y = 2, color = 'r', linestyle = '-')

plt.show()