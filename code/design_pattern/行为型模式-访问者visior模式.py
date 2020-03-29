# 理解
# 关键是双分派的理解
# 例子
# http://my.oschina.net/coolwater/blog/27676
# Element
class Problem:
    def getProblem(self, s):  # accept
        print "一般问题",
        s.solve(self)


class SpecialProblem(Problem):
    def getProblem(self, s):
        print "特殊问题",
        s.solve(self)
        # visitor


class Supporter:
    def solve(self, p):
        print "由一级支持解决"


class SeniorSupporter(Supporter):
    def solve(self, p):
        print "由资深支持解决"
        # client


if __name__ == "__main__":
    s = Supporter()
    ss = SeniorSupporter()
    p = Problem()
    sp = SpecialProblem()
    p.getProblem(s)
    p.getProblem(ss)
    sp.getProblem(s)
    sp.getProblem(ss)  