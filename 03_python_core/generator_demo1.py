# 参考：https://blog.csdn.net/zhong_jay/article/details/91799459
# generator使用场景：
# 1.当我们需要一个公用的，an按需生成的数据；
# 2.某个事情执行一部分，另一部分在某个事件发生后再执行下一部分，实现异步。

# 注意事项：
# 1.yield from generator_obj 本质上类似于 from item in generator_obj:yield item
# 2.generator函数中允许使用return，但是return后不允许有返回值

# generator基础
def gen_generator():
    yield 1
    
def gen_value():
    return 1

if __name__ == '__main__':
    ret = gen_generator()
    print(ret, type(ret))
    ret = gen_value()
    print(ret, type(ret))

# 从上面的代码可以看出：gen_generator函数返回的是一个generator实例，generator有一下特别：
# 1.遵循迭代器(iterator)协议，迭代器协议需要实现__iter__、next接口
# 2.能够多次进入、多次返回，能够暂停函数中代码的执行

# 测试代码
def gen_example():
    print('before any yield')
    yield 'first yield'
    print('between yields')
    yield 'second yield'
    print('no yield anymore')

gen = gen_example()
# 第一次调用next
gen.next()
# before yield
# 'first yield'

# 第二次调用next
gen.next()
# between yields
# 'second yield'

# gen.next() # 第三次调用next
# no yield anymore
# Traceback



