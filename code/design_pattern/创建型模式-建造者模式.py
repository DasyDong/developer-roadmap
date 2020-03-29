# 理解
# 个人理解builder模式的重点就是聚合，就像我们新建一个工程的时候有一些向导，
# 跟着这些向导，通过不同的选项，其中前面的选项可能影响后面的出现的向导，
# 最终得出不同的模版，也就是对象的构建与表示分离，也不知道我理解的对不对，要是不对希望大家指正
"""
创建型设计模式
"""
# 例子
# 我们就以创建一个函数(c函数和python函数)模版为例吧，也不知道合不合适
# product
class Product:
    def __init__(self):
        self.ReturnName = None
        self.functionName = None
        self.Parameter = None
        self.body = None

    def __repr__(self):
        return "%s %s %s \n%s" % (self.ReturnName, self.functionName, self.Parameter, self.body)
        # director


class Director:
    def __init__(self):
        self.builder = None

    def Construct(self):
        self.builder.builderCommonPart()
        self.builder.builderReturnType()
        self.builder.builderparameter()
        self.builder.builderbodyPart()

    def getProduct(self):
        return self.builder.Product
        # builder


class builder:
    def __init__(self):
        self.Product = None

    def builderCommonPart(self):
        self.Product = Product()
        self.Product.functionName = "function"


class ConcreateBuilder_C(builder):
    def builderbodyPart(self):
        self.Product.body = '{\n}'

    def builderReturnType(self):
        self.Product.ReturnName = 'void'

    def builderparameter(self):
        self.Product.Parameter = '(int a)'


class ConcreateBuilder_Python(builder):
    def builderbodyPart(self):
        self.Product.body = '    pass'

    def builderReturnType(self):
        self.Product.ReturnName = 'def'

    def builderparameter(self):
        self.Product.Parameter = '(self,a):'
        # client


if __name__ == "__main__":
    director = Director()
    director.builder = ConcreateBuilder_C()
    director.Construct()
    print director.getProduct()
    print '#create Python function'
    director.builder = ConcreateBuilder_Python()
    director.Construct()
    print director.getProduct()