# 理解
# 职责链模式也是一个比较常见的模式，通过消息在处理模块的传递，将消息发送模块和各个处理模块解耦合
# 例子
# 这个模式的应用也是很多的，比如windows的消息机制，在产品保修时，如果当地的营销点，就会发回上一级的营销点，直到能够维修为止
# Handler
class Handler(object):
    successor = None

    def setSuccessor(self, suc):
        self.successor = suc


class ConcreteHandle1(Handler):
    def HandleRequest(self):
        if self.successor == None:
            pass
        else:
            print "模块1处理"
            self.successor.HandleRequest()


class ConcreteHandle2(Handler):
    def HandleRequest(self):
        if self.successor == None:
            print "结束处理"
        else:
            self.successor.HandleRequest()
            # client


if __name__ == "__main__":
    Con1 = ConcreteHandle1()
    Con2 = ConcreteHandle2()
    Con1.setSuccessor(Con2)
    Con1.HandleRequest()  