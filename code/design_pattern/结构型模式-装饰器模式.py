# 理解
# 动态的给一个对象添加额外的职责
# 例子
# 假如有一只会叫的dog，现在让它叫的时候会张嘴
# Component
class Animal(object):
    def speak(self):
        pass
        # ConcreateComponent


class dog(Animal):
    def speak(self):
        print 'wangwang'
        # Decorator


class Decorator(object):
    Component = None

    def speak(self):
        self.Component.speak()
        # ConcreateDecorator


class ConcreateDecorator(Decorator):
    def __init__(self, Com):
        self.Component = Com

    def speak(self):
        self.openmouth()
        super(ConcreateDecorator, self).speak()

    def openmouth(self):
        print 'open mouth'
        # client


if __name__ == '__main__':
    ComcreateComponent = dog()
    dec = ConcreateDecorator(ComcreateComponent)
    dec.speak()
