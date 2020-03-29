# 理解
# Observer模式是最多应用的模式之一
# 在很多的编程语言中，都实现了这种模式，并利用了这种模式
# 例子
# 订报的例子应该比较合适吧
#行为型设计模式
class publisher(object):
    observers = list()
    msg = None

    def register(self, observer):
        self.observers.append(observer)

    def disregister(self, observer):
        self.observers.remove(observer)

    def Notify(self):
        for ob in self.observers:
            ob.update()


class newspublisher(publisher):
    def getMessage(self):
        return self.msg

    def setMessage(self, msg):
        self.msg = msg


class observer:
    def update(self):
        pass


class people(observer):
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.register(self)

    def disregister(self):
        self.publisher.disregister(self)

    def update(self):
        print self.publisher.getMessage()


if __name__ == "__main__":
    news = newspublisher()
    person1 = people(news)
    person2 = people(news)
    news.setMessage("nihao")
    news.Notify()
    person1.disregister()
    news.setMessage("hello")
    news.Notify()