#-*-coding=utf-8-*-
#理解：
"""
创建型设计模式
"""
"""
"""
"""
工厂模式：实例化延迟到子类
缺点是使用类作为代价，且factory修改不封闭，每增加product就要修改
但可以使用配置文件，就可以封闭了
"""
class Product_opt:
    def getResult(self):
        pass
class Product_add(Product_opt):
    def getResult(self):
        return self.num1+self.num2
class Product_sub(Product_opt):
    def getResult(self):
        return self.num1-self.num2
class Product_err(Product_opt):
    def getResult(self):
        print "error"
        return 0
class Factory:
    operation={}
    operation["+"]=Product_add()
    operation["-"]=Product_sub()
    def createproduct(self,ch):
        if ch in self.operation:
            op = self.operation[ch]
        else:
            op = Product_err()
        return op
if __name__=="__main__":
    num1=input("a:")
    op=raw_input("operation:")
    num2=input("b:")
    factory=Factory()
    product=factory.createproduct(op)
    product.num1=num1
    product.num2=num2
    print product.getResult()
