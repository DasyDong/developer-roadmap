#理解
#为了将抽象和实现都能独立的变化
#例子
#就是用面试宝典上的一个例子吧，将笔和画出的线条进行分离，例如，用蜡笔做大中小，红绿蓝三种线条就需要9只笔
#若是用毛笔，只需要3只毛笔，3种颜料即可，这样即使颜色增多也不会大量的增加笔类
#implementor
class Implementor(object):
    def OperationImp(self):
        pass
class ConcreteImplementorRed(Implementor):
    def OperationImp(self):
        print "red line"
class ConcreteImplementorBlue(Implementor):
    def OperationImp(self):
        print "blue line"
#Abstraction
class Abstraction(object):
    size=None
    def __init__(self,imple):
        self.imp=imple
    def Operation(self):
        print self.size,
        self.imp.OperationImp()
class RefinedAbstractionBig(Abstraction):
    def __init__(self, implement):
        self.size='big'
        super(RefinedAbstractionBig,self).__init__(implement)
class RefinedAbstractionsmall(Abstraction):
    def __init__(self, imple):
        self.size='small'
        super(RefinedAbstractionsmall,self).__init__(imple)
if __name__=="__main__":
    red=ConcreteImplementorRed()
    big=RefinedAbstractionBig(red)
    big.Operation()
    blue=ConcreteImplementorBlue()
    big=RefinedAbstractionBig(blue)
    big.Operation()
    small=RefinedAbstractionsmall(red)
    small.Operation()
    small=RefinedAbstractionsmall(blue)
    small.Operation()  