# -*- encoding=utf-8 -*-
print '----------------------方法1--------------------------'


# 方法1,实现__new__方法
# 并在将一个类的实例绑定到类变量_instance上,
# 如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
# 如果cls._instance不为None,直接返回cls._instance
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class MyClass(Singleton):
    a = 1


one = MyClass()
two = MyClass()

two.a = 3
print one.a
# 3
# one和two完全相同,可以用id(), ==, is检测
print id(one)
# 29097904
print id(two)
# 29097904
print one == two
# True
print one is two
# True

print '----------------------方法2--------------------------'


# 方法2,共享属性;所谓单例就是所有引用(实例、对象)拥有相同的状态(属性)和行为(方法)
# 同一个类的所有实例天然拥有相同的行为(方法),
# 只需要保证同一个类的所有实例具有相同的状态(属性)即可
# 所有实例共享属性的最简单最直接的方法就是__dict__属性指向(引用)同一个字典(dict)
# 可参看:http://code.activestate.com/recipes/66531/
class Borg(object):
    _state = {}

    def __new__(cls, *args, **kw):
        ob = super(Borg, cls).__new__(cls, *args, **kw)
        ob.__dict__ = cls._state
        return ob


class MyClass2(Borg):
    a = 1


one = MyClass2()
two = MyClass2()

# one和two是两个不同的对象,id, ==, is对比结果可看出
two.a = 3
print one.a
# 3
print id(one)
# 28873680
print id(two)
# 28873712
print one == two
# False
print one is two
# False
# 但是one和two具有相同的（同一个__dict__属性）,见:
print id(one.__dict__)
# 30104000
print id(two.__dict__)
# 30104000

print '----------------------方法3--------------------------'


# 方法3:本质上是方法1的升级（或者说高级）版
# 使用__metaclass__（元类）的高级python用法
class Singleton2(type):
    def __init__(cls, name, bases, dict):
        super(Singleton2, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton2, cls).__call__(*args, **kw)
        return cls._instance


class MyClass3(object):
    __metaclass__ = Singleton2


one = MyClass3()
two = MyClass3()

two.a = 3
print one.a
# 3
print id(one)
# 31495472
print id(two)
# 31495472
print one == two
# True
print one is two
# True

print '----------------------方法4--------------------------'


# 方法4:也是方法1的升级（高级）版本,
# 使用装饰器(decorator),
# 这是一种更pythonic,更elegant的方法,
# 单例类本身根本不知道自己是单例的,因为他本身(自己的代码)并不是单例的
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class MyClass4(object):
    a = 1

    def __init__(self, x=0):
        self.x = x


one = MyClass4()
two = MyClass4()

two.a = 3
print one.a
# 3
print id(one)
# 29660784
print id(two)
# 29660784
print one == two
# True
print one is two
# True
one.x = 1
print one.x
# 1
print two.x
# 1


Python单例模式和Borg惯用法及相关问题

一、单例模式

如果你想保证某个类从始至终最多只能有一个实例，那么单例模式可能会是你首先想到的，使用__new__静态方法可以很简单的解决：

class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if '_inst' not in vars(cls):
            cls._inst = super(Singleton, cls).__new__(cls)
        return cls._inst

    Python
    2.
    X
    里你可能看到的实现代码：

    class Singleton(object):
        def __new__(cls, *args, **kwargs):
            if '_inst' not in vars(cls):
                cls._inst = super(Singleton, cls).__new__(cls, *args, *kwargs)
            return cls._inst

        它们这间的细微不同之处在于 * args, ** kwargs：

        cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)

        而这在Python
        3.
        x里将会引发异常：TypeError: object()
        takes
        no
        parameters

        如果我们查看
        CPython
        源码，我们将会看到：

        （1）在__new__
        被overridden或者__init__没有被overridden
        的情况下，如果调用
        object.__new__的时候传递了除cls之外的参数将会报错；

        （2）在__new__
        没有被overridden或者__init__被overridden
        的情况下，如果调用
        object.__init__
        的时候传递了除cls之外的参数将会报错；

        （3）*args，和 * kwds
        在object.__new__除了用来判断报错，并没有什么其它用处

    static
    int
    object_init(PyObject * self, PyObject * args, PyObject * kwds)
    {
        int
    err = 0;
    PyTypeObject * type = Py_TYPE(self);
    if (excess_args(args, kwds) & &
            (type->tp_new == object_new | | type->tp_init != object_init)) {
    PyErr_SetString(PyExc_TypeError, "object.__init__() takes no parameters");
    err = -1;
    }
    return err;
    }

    static
    PyObject *
    object_new(PyTypeObject * type, PyObject * args, PyObject * kwds)
    {
    if (excess_args(args, kwds) & &
            (type->tp_init == object_init | | type->tp_new != object_new)) {
    PyErr_SetString(PyExc_TypeError, "object() takes no parameters");
    return NULL;
    }
    ...
    }



    二、Borg惯用法

    如果你想保证某个类从始至终只创建了一个实例：你并不关心生成实例的id，只关心其状态和行为方式，而且你还想确保它具有子类化的能力，那么可以使用Borg惯用法：



    class Borg(object):
        _state = {}

        def __new__(cls, *args, **kwargs):
            obj = super(SingletonBorg, cls).__new__(cls)
            obj.__dict__ = cls._state
            return obj

        和单例模式不同的是，Borg惯用法允许多个实例被创建，但所有的实例都共享状态和行为方式。通过这种“数据重载”，你的类不会从Borg继承_shared_state属性，而是自己的数据。为了允许这种“数据重载”，Borg的__new__应当使用cls._shared_state，而不是Borg._shared_state。

        如果你想Borg的所有类实例都能够共享状态：

        class SingletonSpam_02(Borg): pass

        如果你想你的类实例能够相互共享状态，但却不和Borg的其它子类共享，需要在类作用域中加入这样的声明：

        class SingletonSpam_03(Borg):
            _state = {}

    测试：

    if __name__ == '__main__':
        class SingletonSpam_02(Borg): pass

        class SingletonSpam_03(Borg):
            _state = {}

        one = SingletonSpam_02()
        two = SingletonSpam_02()
        one.name = 'lilei'
        two.name = 'hanmeimei'
        print(one.name, two.name)

        three = SingletonSpam_03()
        four = SingletonSpam_03()
        three.name = 'liuxing'
        four.name = 'baiyun'
        print(three.name, four.name)

        执行后，发现在子类中加入_state = {}
        就可以实现：自己的类实例能够相互共享状态，但却不和Borg的其它子类共享：

        ('hanmeimei', 'hanmeimei')
        ('baiyun', 'baiyun')

