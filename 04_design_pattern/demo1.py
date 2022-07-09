# https://www.cnblogs.com/tangkaishou/p/9246353.html
# 常见设计模式 (python代码实现)

# 单例模式
# 某一个类只有一个实例存在
class Singleton(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"): # 反射
            Singleton._instance = object.__new_(cls)
        return Singleton._instance

object1 = Singleton
object2 = Singleton
print(object1, object2)
print(object1 == object2)

# *****************************************
# 工厂模式
# 创建对象
class Person:
    def __init__(self):
        self.name = None
        self.gender = None

    def getName(self):
        return self.name

    def getGender(self):
        return self.gender

class Male(Person):
    def __init__(self, name):
        print("Hello Mr." + name)

class Female(Person):
    def __init__(self, name):
        print("Hello Miss." + name)

class Factory:
    def getPerson(self, name, gender):
        if gender == 'M':
            return Male(name)
        if gender == 'F':
            return Female(name)

if __name__ == '__main__':
    factory = Factory()
    person = factory.getPerson('Chetan', 'M')

# *****************************************
# 建造者模式
# 将一个复杂对象的构建与它的表示分离，使得同样的构建过程可以创建不同的表示
from abc import ABCMeta, abstractmethod

class Builder():
    __metaclass__ == ABCMeta

    @abstractmethod
    def draw_left_arm(self):
        pass

    @abstractmethod
    def draw_left_arm(self):
        pass

    @abstractmethod
    def draw_right_arm(self):
        pass

    @abstractmethod
    def draw_left_root(self):
        pass

    @abstractmethod
    def draw_right_root(self):
        pass

    @abstractmethod
    def draw_head(self):
        pass

    @abstractmethod
    def draw_body(self):
        pass

class Thin(Builder):
    pass


















