
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if 'cls' not in instances:
            instances['cls'] = cls(*args, **kwargs)
        return instances['cls']
    return wrapper


@singleton
class TestSingle(object):
    pass


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class TestSingle2(Singleton):
    pass


def run_test_single():
    for i in range(10):
        foo = TestSingle2()
        print id(foo)

##################################################


if __name__ == '__main__':
    run_test_single()
