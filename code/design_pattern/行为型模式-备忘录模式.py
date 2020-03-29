# 理解
# Memento模式的关键是不破坏封装
# Originator
class Originator:
    def __init__(self, sta):
        self.state = sta

    def SetMemento(self, Mem):
        self.state = Mem.getState()

    def CreateMento(self):
        return Memento(self.state)


class Memento:
    def __init__(self, state):
        self.SetState(state)

    def getState(self):
        return self.state

    def SetState(self, state):
        self.state = state


if __name__ == "__main__":
    ori = Originator("hello")
    print ori.state
    mem = ori.CreateMento()
    ori.state = "world"
    print ori.state
    ori.SetMemento(mem)
    print ori.state  