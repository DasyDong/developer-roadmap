# 理解
# Abstract_Factory模式是Factory的扩展，
# Factory用于生产一类产品而抽象工厂用于生产多个产品系列
"""
创建型设计模式
"""
""" 例子：
# 两个工厂，一个生产狗玩具，一个生产猫玩具，而玩具共有两类一类机器玩具，一类毛绒玩具
"""
class Abstract_Factory:
    def __init__(self, factory=None):
        self.toy_factory = factory


class cat_Factory(Abstract_Factory):
    # 当然这里可以象Factory_Method使用查表
    def create_soft_cat(self):
        return soft_cat_toy();

    def create_machine_cat(self):
        return machine_cat_toy()


class dog_Factory(Abstract_Factory):
    def create_soft_dog(self):
        return soft_dog_toy();

    def create_machine_dog(self):
        return machine_dog_toy();


class Abstract_Product_dog:
    def getname(self):
        pass

    def speak(self):
        print "wangwang"


class soft_dog_toy(Abstract_Product_dog):
    def getname(self):
        return "soft dog toy"


class machine_dog_toy(Abstract_Product_dog):
    def getname(self):
        return "machine dog toy"


class Abstract_Product_cat:
    def getname(self):
        pass

    def speak(self):
        print "miaomiao"


class soft_cat_toy(Abstract_Product_cat):
    def getname(self):
        return "soft cat toy"


class machine_cat_toy(Abstract_Product_cat):
    def getname(self):
        return "machine cat toy"


if __name__ == "__main__":
    factory = Abstract_Factory(dog_Factory());
    dog1 = factory.toy_factory.create_soft_dog()
    dog1.speak()
    print dog1.getname()
    dog2 = factory.toy_factory.create_machine_dog()
    dog2.speak()
    print dog2.getname()
    factory = Abstract_Factory(cat_Factory())
    cat1 = factory.toy_factory.create_soft_cat()
    cat1.speak()
    print cat1.getname()
    cat2 = factory.toy_factory.create_machine_cat()
    cat2.speak()
    print cat2.getname()