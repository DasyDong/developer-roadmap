#理解
#具有层次结构，且使得部分和整体具有一致性
#例子
#一个经典的组合例子就是食品的分类
#Component
class food_Component(object):
    def __init__(self):
        self.food_object={}
        self.i=0
    def display_name(self):
        pass
    def Add(self,food):
        pass
    def remove(self,food):
        pass
    def getChild(self,pos):
        pass
#Composite
class Vegetable_Composite(food_Component):
    def __init__(self,name):
        self.name=name
        super(Vegetable_Composite,self).__init__()
    def display_name(self):
        print self.name
    def Add(self,food):
        self.food_object[self.i]=food
        self.i=self.i+1
    def remove(self,food):
        self.food_object.remove(food)
    def getChild(self,pos):
        return self.food_object[pos]
#leaf
class leaf(food_Component):
    def __init__(self,name):
        self.name=name
        super(leaf,self).__init__()
    def display_name(self):
        print self.name
#client
if __name__=="__main__":
    cabbage=leaf('cabbage')
    cabbage.display_name()
    composite=Vegetable_Composite('vegetable')
    green=Vegetable_Composite('green vegetable')
    composite.Add(green)
    green.Add(cabbage)
    composite.display_name()
    green.display_name()
    component=composite.getChild(0)
    component.display_name()
    component1=component.getChild(0)
    component1.display_name()  