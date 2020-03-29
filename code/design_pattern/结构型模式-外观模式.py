# 理解
# 减少各个子系统之间及与客户之间的依赖，为客户提供统一的接口
# 例子
# 假设同学毕业要去图书馆去审核借阅记录，去教务处办理离校手续，去生活部注销校园卡
# 现在提供一个学生办事处提供统一的外观

# library
class library:
    def comeLibrary(self):
        print "come lib"
        # office


class office:
    def comeOffice(self):
        print "come office"
        # LifeDepartment


class LifeDepartment:
    def comeLife(self):
        print "come life"
        # Facade


class committee:
    def __init__(self):
        self.life = LifeDepartment()
        self.office = office()
        self.lib = library()

    def comeCom(self):
        self.life.comeLife()
        self.lib.comeLibrary()
        self.office.comeOffice()
        # client


if __name__ == '__main__':
    com = committee()  