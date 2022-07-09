# 参考：https://blog.csdn.net/zhong_jay/article/details/91799459
def generator_example():
    yield 1
    yield 2

if __name__ == '__main__':
    for e in generator_example():
        print(e)
        # output 1 2

# generator function产生的generator与普通的function有什么区别呢？
# 1.function每次都是从第一行开始运行的，而generator从上一次yield开始的地方运行
# 2.functiond调用一次返回一个（一组）值，而generator可以多次返回
# 3.function可以被无数次重复调用，而一个generator实例在yield最后一个值或者return之后就不能再继续调用了

# 在函数中使用Yield，然后调用该函数是生成generator的一种方式。另一种常见的方式是使用generator expression, for example:
gen = (x * x for x in range(5))
print(gen)

# generator应用
# generator基础应用
# 按需生成并返回结果，而不是一次性产生所有的返回值，况且有时候根本就不知道返回的所有值。例如
RANGE_NUM = 100
for i in [x*x for x in range(RANGE_NUM)]: #第一种方法：对列表进行迭代
    # do sth for example
    print(i)
# 返回一个列表，占用内存比较大

for i in (x*x for x in range(RANGE_NUM)): #第二种方法：对generator进行迭代
    # do sth for example
    print(i)
# 返回的是一个generator对象，并且随着RANGE_NUM的变大，内存占用不会变大

# 返回无穷多次的例子：
def fib():
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b
# 这个generator拥有生成无数多返回值的能力，使用者可以自己决定什么事后停止迭代

# generator高级应用
# 使用场景一
# Generator可用于产生数据流,generator并不立刻产生返回值，而是等到被需要的时候才会产生返回值，相当于一个主动拉取的过程(pull),
# 比如现在有一个日志文件，每行产生一条记录，对于每一条记录，不同部门的人可能处理方式不同，但是我们可以提供一个公用的、按需生成的
# 数据流。
def gen_data_from_file(file_name):
    for line in file(file_name):
        yield line

def gen_words(lines):
    for word in (w for w in line.split() if w.strip()):
        yield word

def count_words(file_name):
    word_map = {}
    for line in gen_data_from_file(file_name):
        for word in gen_words(line):
            if word not in word_map:
                word_map[word] = 0
            word_map[word] += 1
    return word_map

def count_total_chars(file_name):
    total = 0
    for line in gen_data_from_file(file_name):
        total += len(line)
    return total

if __name__ == '__main__':
    print(count_words('tests.txt'), count_total_chars('test.txt'))
# PyCon讲座
# gen_words_gen_data_from_file是数据生产者，而count_words count_total_chars是数据的消费者。
# 数据只有在需要的时候去拉取，而不是提前准备好
# 另外gen_words中(w for w in line.split() if w.strip())也是产生了一个generator

# 使用场景二
# 一些编程场景中，一件事情可能需要执行一部分逻辑，然后等待一段时间、或者等待某个异步的结果、或者等待某个状态，然后继续执行另一部分逻辑。比如
# 微服务架构中，服务Az执行了一段逻辑之后，去服务B请求一些数据，然后在服务A上继续执行。或者在游戏编程中，一个技能分成多段，先执行一部分动作
# （效果），然后等待一段时间，然后再继续。对于这种需要等待、而又不希望阻塞的情况，我们一般使用回调（callback）的方式。下面举一个简单的例子：
def do(a):
    print('do', a)
    CallBackMgr.callback(5, lambda a = a : post_do(a))

def post_do(a):
    print('post_do', a)

# 这里的CallBackMgr注册了一个5s后的时间，5s后再调用lambda函数，可见一段逻辑被分裂到两个函数，而且还需要上下文的传递(如这里的参数a)。我们
# 用yield来修改一下这个例子，yield返回值代表等待的时间。
@yield_dec
def do(a):
    print('do', a)
    yield 5
    print('post_do', a)

# 这里需要实现一个YieldManager，通过yield_dec这个decorator将do这个generator注册到YieldManager，并在5s后调用next方法。
# Yield版本实现了和回调一样的功能，但是看起来要清晰很多。下面给出一个简单的实现以供参考：
import sys
import Timer
import types
import time

class YieldManager(object):
    def __init__(self, tick_delta=0.01):
        self.generator_dict = {}
        # self._tick_timer = Timer.addRepeatTimer(tick_delta, lambda: self.tick())

    def tick(self):
        cur = time.time()
        for gene, t in self.generator_dict.items():
            if cur >= t:
                self._do_resume_generator(gene, cur)

    def _do_resume_generator(self, gene, cur):
        try:
            self.on_generator_execute(gene, cur)
        except StopIteration,e:
            self.remove_generator(gene)
        except Exception,e:
            print('unexpect error', type(e))
            self.remove_generator(gene)

    def add_generator(self, gen, deadline):
        self.generator_dict[gen] = deadline

    def remove_generator(self, gene):
        del self.generator_dict[gene]

    def on_generator_execute(self, gen, cur_time = None):
        t = gen.next()
        cur_time = cur_time or time.time()
        self.add_generator(gen, t + cur_time)

g_yield_mgr = YieldManager()

def yield_dec(func):
    def _inner_func(*args, **kwargs):
        gen = func(*args, **kwargs)
        if type(gen) is types.GeneratorType:
            g_yield_mgr.on_generator_execute(gen)

        return gen
    return _inner_func

@yield_dec
def do(a):
    print('do', a)
    yield 2.5
    print('post_do', a)
    yield 3
    print('post_do_again', a)

if __name__ == '__main__':
    do(1)
    for i in range(1, 10):
        print('simulate a timer, %s seconds passed' % i)
        time.sleep(1)
        g_yield_mgr.tick()
























