# 理解
# 运用共享技术，减少大量细粒度对象对存储的开销
# 例子
# 我们知道我们现在网上会注册很多帐号和密码，一些不重要的都是相同的，这样如果很多很多的话就会占用大量的空间
# Flyweight
class Flyweight:
    def Operation(self):
        pass
        # ConcreateFlyweight


class password(Flyweight):
    def __init__(self, pwd):
        self.pwd = pwd

    def Operation(self):
        pass
        # FlyweightFactory


class FlyweightFactory:
    object = {}
    i = 0

    def getFlyweight(self, pwd):
        for ii in range(0, self.i):
            if self.object[ii].pwd == pwd:
                return self.object[ii]
        self.object[self.i] = password(pwd)
        self.i = self.i + 1
        return self.object[self.i - 1]
        # client


if __name__ == '__main__':
    fc = FlyweightFactory()
    fw = fc.getFlyweight("123")
    fw1 = fc.getFlyweight("345")
    fw2 = fc.getFlyweight("123")
    print fw, fw.pwd
    print fw1, fw1.pwd
    print fw2, fw2.pwd