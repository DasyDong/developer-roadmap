# 理解
# 生活中的代理的例子很多很多，计算机方面代理的应用也很多，有多种多样的目的,这个UML图和Adapter模式有点像，不过侧重点完全不一样
# 例子
# 代理最简单的应用就是通过一个对象去控制另一个对象，当然代理可以做一些对被控制者的保护等等
# subject
class AbstractSubject:
    def resquest(self):
        pass
        # Realsubject


class RealSubject(AbstractSubject):
    def request(self):
        print "i'm working"
        # Proxy


class Proxy(AbstractSubject):
    def __init__(self, subject):
        self.subject = subject

    def request(self, ip):
        if ip == '1':
            self.subject.request()
        else:
            print 'you ip isnot right'
            # client


if __name__ == "__main__":
    sub = RealSubject()
    proxy = Proxy(sub)
    proxy.request('')
    proxy.request('1')  