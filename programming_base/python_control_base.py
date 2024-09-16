a = [1, 2, 3]
result = []

for i in a :
    result.append(i**2)
print(result)
print([i**2 for i in a])    #리스트 내포

number = [1, 2, 3, "4", 5]

for i in number :
    try :
        print(i**2)
    except :
        print("error :", i)
        print("error : " + i)

"""============================================
==============================================="""

def multiply(x, y) :
    res = x**y
    return res
print("def multiply:", multiply(2, 4))

def divide(x, y = 2) :
    res = x / y
    return res
print("def divide(default):", divide(6))

plus_lam = lambda x, y : x + y
print("plus(lamda):", plus_lam(2, 3))

"""============================================
==============================================="""

import selenium.webdriver   #상위패키지는 selenium, 하위패키지는 webdriver
print(dir(selenium.webdriver))

import seaborn as sns   #seaborn 패키지 내에 있는 모든 함수를 쓰겠다
print(sns.load_dataset('iris'))

from seaborn import load_dataset    #from 패키지명 import 함수명 : 특정 패키지 안의 특정 함수만 쓰겠다 
print(load_dataset("iris"))


