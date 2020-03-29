#理解
#原型与工厂模式的区别应该是少一个与与产品平行的工厂类，通过克隆自己，可以创造多个对象
"""
创建型设计模式
"""
#例子
#有一个哺乳动物的原型，每个动物有名称，
#人有很多，所以有很多Object,我们通过clone得到人的对象，然后在附上不同属性
#猴子也有很多，我们也可以通过clone得到多个猴子
class Prototype(object):
    typename='mammalian'
    def __init__(self):
        pass
    def clone(self):
        pass
class Person(Prototype):
    def __init__(self):
        self.hair='black'
        self.Name='Person'
        Prototype.__init__(self)#调用父类初始化函数的一种方法
    def clone(self):
        return Person()
class monkey(Prototype):
    def __init__(self):
        self.hair='red'
        self.Name='monkey'
        super(Prototype,self).__init__()#调用父类初始化的另一种方法
    def clone(self):
        return monkey()
#client
if __name__=="__main__":
    p=Person()
    p1=p.clone()
    print p
    print p.typename,p.hair,p.Name
    print p1
    print p1.typename,p1.hair,p.Name
    Monkey=monkey()
    Monkey1=Monkey.clone()
    print Monkey
    print Monkey.typename,Monkey.hair,Monkey.Name
    print Monkey1
    print Monkey.typename,Monkey1.hair,Monkey.Name