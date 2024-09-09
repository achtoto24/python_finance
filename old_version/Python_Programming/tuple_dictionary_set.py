mytuple = ('a', 'b', 'c', [1, 2, 3])
print(mytuple[3])
#mytuple[0] = 'A'
print(mytuple)

'''============================================'''
Nasdaq = {'NVDA' : "Nvidia", 'APPL' : "Apple", 'TSLA' : "Tesla"}
print(Nasdaq['APPL'])
Nasdaq['MSFT'] = "Microsoft"
print(Nasdaq)

for x in Nasdaq :
    print("%s : %s" % (x, Nasdaq[x]))

for x in Nasdaq :
    print('{} , {}'.format(x, Nasdaq[x]))

#f-strings
for x in Nasdaq :
    print(f'{x} & {Nasdaq[x]}')

'''============================================'''
s = {'A', 'P', 'P', 'L', 'E'} #'set' type prints output randomly
print(s)

if 'B' in s :
    print("'B' exists in ", s)
else :
    print("nothing")

setA = {1, 2, 3, 4, 5}
setB = {3, 4, 5, 6, 7}
print(setA & setB)
print(setA | setB)
print(setA - setB)
print(setB - setA)

s_empty = set() #empty set













