# 理解
# 模式的关键是将命令的封装
# 例子
# 将碰到句号自动分行和撤销的命令
class Command:
    def __init__(self, rev):
        self.rev = rev

    def execute(self):
        pass

    def undo(self):
        pass


class Concreate(Command):
    def execute(self):
        self.rev.str = self.rev.str.replace('.', '\n')
        self.rev.printf()

    def undo(self):
        self.rev.str = self.rev.str.replace('\n', '.')
        self.rev.printf()
        # invoker


class invoker:
    def __init__(self, command):
        self.com = command

    def invoke(self):
        self.com.execute()

    def undo(self):
        self.com.undo()
        # reciever


class Reciever:
    str = "hello.world"

    def printf(self):
        print self.str


if __name__ == "__main__":
    rev = Reciever()
    com = Concreate(rev)
    inv = invoker(com)
    inv.invoke()
    print "undo:"
    inv.undo()  