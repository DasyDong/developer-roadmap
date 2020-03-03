# coding: utf-8
def test_legb():
    fun = [lambda x, i=i: x*i for i in range(4)]
    for item in fun:
        print(item(1))


def func():
    fun_lambda_list = []
    for i in range(4):

        def lambda_(x):
            print('Lambda函数中 i {} 命名空间为：{}:'.format(i, locals()))
            return x*i
        fun_lambda_list.append(lambda_)
        print('外层函数 I 为：{} 命名空间为:{}'.format(i, locals()))

    return fun_lambda_list


def test_legb_func():
    for item in func():
        print(item(1))


def run_test_legb():
    test_legb()

##################################################


if __name__ == "__main__":
    test_legb_func()
