def getCAGR(first, last, years) :
    return (last/first) ** (1/years) - 1

cagr = getCAGR(65300, 2669000, 20)

print("SEC CAGR : {:.2%}".format(cagr))

#mutiple reusults available
def myFunc() :
    var1 = 'a'
    var2 = [1, 2, 3]
    var3 = max
    return var1, var2, var3 # Multiple result values are returned by default to 'tuple' type

print(myFunc())
s, l, f = myFunc()
print(s,'\n', l,'\n', f)

#lambda
insertComma = lambda x : format(x, ',')
print(insertComma(123456789))

print(help('modules'))