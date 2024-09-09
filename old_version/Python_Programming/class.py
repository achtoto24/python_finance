class MyFirstClass : 
    clsVar = 'The best way to predict the future is to invent it.'
    def clsMethod(self) :
        print(MyFirstClass.clsVar + '\t- Alan Curtis Kay -')

mfc = MyFirstClass()

mfc.clsVar
mfc.clsMethod()

'''==================================================='''
class A :
    def methodA(self) :
        print("Calling A's methodA")
    def method(self) :
        print("Calling A's method")

class B :
    def methodB(self) :
        print("Calling B's methodB")

class C (A, B) :
    def methodC(self) :
        print("Calling C's methodC")
    def method(self) :
        print("Calling C's overridden method")
        super().method()

c = C()
c.methodA()
c.methodB()
c.methodC()
c.method()
'''==================================================='''
class NasdaqStock :
    """Class for NASDAQ stocks"""   #docstring
    count = 0   #class variable
    
    def __init__(self, symbol, price) :
        """Constructor for NasdaqStock"""   #docstring
        self.symbol = symbol    #instacne variable
        self.price = price      #instance variable
        NasdaqStock.count += 1
        print('Calling __init__({}, {:.2f}) > count : {}'.format(self.symbol, self.price, NasdaqStock.count))

    def __del__(self) :
        """Destructor for NasdaqStock"""
        print('Calling __del__({})'.format(self))

gg = NasdaqStock('GOOG', 1154.05)
del(gg)
ms = NasdaqStock('MSFT', 102.44)
del(ms)
amz = NasdaqStock('AMZN', 1746.00)
del(amz)

help(NasdaqStock)