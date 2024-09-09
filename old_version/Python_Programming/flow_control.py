# RSH : Relative Strengh Index
# If_practice
rsi = 88
if rsi > 78 :
    print('RSI', rsi, 'means overbought.')
elif rsi < 30 :
    print('RSI', rsi, 'means oversold.')
else :
    print('...')

''' for statements ''' 
#for i in[1, 2, 3] :
#    print(i)

#for i in range(1, 7, 2) :
#    print(i)

FANNG = ['FB', 'AMZN', 'APPL', 'NFLX', 'GOOGL']

for i, symbol in enumerate(FANNG) : #if you don't write second paratmeter, the interpreter shows a result as tuple form. 
    print(i, symbol)

''' while statements'''
#i = 1
#while i < 7 :
#    print(i)
#    i += 2

i = 0
while i < 4 :
    i += 1
    if (i % 2) == 0 : 
        continue
    if i > 5 :
        break
    print(i)
else :
    print('Condition is False.')

'''try-except process'''
try :
    1/0
except Exception as t :
    print('Exception occured : ', str(t))