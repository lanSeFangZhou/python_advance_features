# https://www.cnblogs.com/fengff/p/11011000.html
# threading模块中的timer
from datetime import datetime
from threading import Timer
# 打印时间函数
def printTime(inc):
    print(datetime.now().strftime('%Y-%m-%d %H-%M-%S'))
    t = Timer(inc, printTime, (inc,))
    t.start()
# 5s
printTime(5)