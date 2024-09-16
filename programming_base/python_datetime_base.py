import datetime

var = datetime.datetime.now()
print(var)
print(var.weekday())    #요일 반환; 월요일(0)부터...
print(var.date())
print(var.time())

dt1 = datetime.datetime(2022, 12, 31)
dt2 = datetime.datetime(2021, 12, 31)

print(dt1 - dt2)
print(dt1 + datetime.timedelta(days = 1))

print(var.strftime("%Y-%m-%d"))
print(datetime.datetime.strptime("2022-12-31 11:59:59", "%Y-%m-%d %H:%M:%S"))

from dateutil.relativedelta import relativedelta
print(dt2 + relativedelta(months=1))