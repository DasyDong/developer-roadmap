# 理解
# 策略模式与模版模式相似，不同的是Strategy模式，将抽象接口封装到了另一个类
# Strategy
class Strategy:
    def AlgrithmInterface(self):
        pass
        # ConcreteStrategy


class ConcreteStrategyA(Strategy):
    def AlgrithmInterface(self):
        print "eat food"


class ConcreteStrategyB(Strategy):
    def AlgrithmInterface(self):
        print "drink water"


class Context:
    def __init__(self, Strategy):
        self.Strategy = Strategy

    def DoAction(self):
        self.Strategy.AlgrithmInterface()
        # client


if __name__ == "__main__":
    strategy = ConcreteStrategyA()
    context = Context(strategy)
    context.DoAction()  