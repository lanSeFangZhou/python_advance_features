# 参考：https://blog.csdn.net/zhong_jay/article/details/91799459
# 注意事项
# （1）Yield是不能嵌套的！
def visit(data):
    for elem in data:
        if isinstance(elem, tuple) or isinstance(elem, list):
            visit(elem) # here value returned is generator
        else:
            yield elem

if __name__ == '__main__':
    for e in visit([1, 2, (3, 4), 5]):
        print(e)

# 上面的代码访问嵌套序列里面的每一个元素，我们期望的输出是 1 2 3 4 5，而实际输出是 1 2 5。为什么呢，如注释所示，visits是一个generator
# function,所以第4行返回的是generator object，而代码也没这个generator实例迭代。这么改改代码，对这个临时的generator进行迭代就行了
def visit(data):
    for elem in data:
        if isinstance(elem, tuple) or isinstance(elem, list):
            for e in visit(elem):
                yield e
        else:
            yield elem

# 或者在python3.3中可以使用yield from,这个语法是在pep380加入的
def visit(data):
    for elem in data:
        if isinstance(elem, tuple) or isinstance(elem, list):
            yield from visit(elem)
        else:
            yield elem

# (2) generator function中使用return
# 在python doc中， 明确提到是可以使用return的， 当generator执行到这里的时候抛出StopIteration一场。
def gen_with_function(range_num):
    if range_num < 0:
        return
    else:
        for i in xrange(range_num):
            yield i

if __name__ == '__main__':
    print(list(gen_with_return(-1)))
    print(list(gen_with_return(1)))

# 但是，generator function中的return是不能带任何返回值的
def gen_with_return(range_num):
    if range_num < 0:
        return 0
    else:
        for i in xrange(range_num):
            yield i
# 上面的代码会报错： SyntaxError: 'return' with argument inside generator

# References：
#
# http://www.dabeaz.com/generators-uk/
# https://www.python.org/dev/peps/pep-0380/
# http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
# http://stackoverflow.com/questions/15809296/python-syntaxerror-return-with-argument-inside-generator























