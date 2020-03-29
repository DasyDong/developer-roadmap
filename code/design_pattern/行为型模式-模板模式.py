# 理解
# 就是普通通过继承实现多态的方法，对于通用操作在父类中实现，不同操作的细节在子类中实现，父类只声明接口
# 注意的是要遵循DIP原则
# 例子
# 灯泡发光，不同的灯泡发不同的光

# AbstractClass
class AbstractClass:
    def TemplementMethod(self):
        self.operator1()
        self.operator2()

    def operator1(self):
        pass

    def operator2(self):
        pass


class LedLight(AbstractClass):
    def operator1(self):
        print "connect 5V"

    def operator2(self):
        print "give out white light"


class bulbLight(AbstractClass):
    def operator1(self):
        print "connect 3V"

    def operator2(self):
        print "give out yallow light"
        # client


if __name__ == '__main__':
    led = LedLight()
    led.TemplementMethod()
    bulb = bulbLight()
    bulb.TemplementMethod()  