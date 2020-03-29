理解
#中介模式可能看起来比较像代理模式，但是却有很大不同，Mediator强调行为，及对象的交互
#例子
#生活中有时候找房子或是找工作要通过中介
#Mediator
class Mediator:
   def introCelleague(self,c1,c2):
      self.colleague1=c1
      self.colleague2=c2
#HouseMediator
class HouseMediator(Mediator):
    def DoActionFrompTob(self):
        print "mediator give b 80 yuan"
        self.colleague2.giveHouse()
    def DoActionFrombTop(self):
        print "give House to p"
        self.colleague1.getHouse()
#Colleague
class Colleague:
    def __init__(self,mediator):
        self.Med=mediator
#businessman
class businessman(Colleague):
    def giveHouse(self):
        print "give mediator house"
        self.Med.DoActionFrombTop()
#person
class person(Colleague):
    def giveMoney(self):
       print "give 100 yuan"
       self.Med.DoActionFrompTob()
    def getHouse(self):
       print "i have house"
#client
if __name__=="__main__":
   med=HouseMediator()
   p=person(med)
   b=businessman(med)
   med.introCelleague(p, b)
   p.giveMoney()  