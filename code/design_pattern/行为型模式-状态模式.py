# 理解
# 事物往往有多种状态，对于每一种状态，响应同一种输入的反应不同，最典型的是有限状态机
# 与策略模式不同的是State模式关注的是状态，将每一种状态封装，简化复杂的switch或驱动表对状态机的维护
# 例子
# 我们知道水有三种状态，冰，水，水汽，而且在加热或冷却的操作下会相互转化
class state:
    def heat(self, con):
        pass

    def cool(self, con):
        pass


class water(state):
    def heat(self, con):
        con.changeState(vapour())

    def cool(self, con):
        con.changeState(ice())


class ice(state):
    def heat(self, con):
        con.changeState(water())


class vapour(state):
    def cool(self, con):
        con.changeState(water())
        # Context


class Context:
    def __init__(self, state):
        self.state = state

    def heat(self):
        self.state.heat(self)  # 与Strategy最大的区别

    def cool(self):
        self.state.cool(self)  # 与Strategy最大的区别

    def changeState(self, state):
        self.state = state
        # client


if __name__ == "__main__":
    Ice = ice()
    context = Context(Ice)
    for i in range(0, 3):
        print context.state
        context.heat()
    for i in range(0, 3):
        print context.state
        context.cool()  