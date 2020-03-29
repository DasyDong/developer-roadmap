# 理解
# python本身就是一种解释性的语言，通过python解释器解释问法，从而执行
# 例子
# 假设解析i = 1 ; i++ ; i++ ; i-- ; print k ;
# 分析
# Context
class Context:
    out = 0

    def __init__(self, str):
        self.str = str
        # Interpreter


class AbstractExpression:
    def interpret(self):
        pass


class AddExpression(AbstractExpression):
    def interpret(self, con):
        con.out += 1


class ConExpression(AbstractExpression):
    def interpret(self, con):
        con.out = (int)((con.str.split('='))[1])


class PrintExpression(AbstractExpression):
    def interpret(self, con):
        print con.out


class ContralExpression(AbstractExpression):
    Exp = {}
    Exp['+'] = AddExpression()
    Exp['='] = ConExpression()
    Exp['p'] = PrintExpression()

    def interpret(self, context):
        statements = context.str.split(";")
        for statement in statements:
            context.str = statement
            if '+' in statement:
                self.Exp['+'].interpret(context)
            elif '=' in statement:
                self.Exp['='].interpret(context)
            elif 'print' in statement:
                self.Exp['p'].interpret(context)

                # client


if __name__ == "__main__":
    str = "i=4;i++;i++;i++;print i;"
    con = Context(str)
    exp1 = ContralExpression()
    exp1.interpret(con)  