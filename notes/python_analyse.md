- [sorted](#sorted)
    - [内置函数sorted()/list.sort()的使用](#内置函数sorted/listsort的使用)
        - [1.简单应用](#1简单应用)
        - [2.按照指定关键词排序](#2按照指定关键词排序)
        - [3.operator.itemgetter](#3operatoritemgetter)
    - [原理](#原理)
- [list 列表](#list-列表)
    - [数据结构](#数据结构)
    - [数组大小变更](#数组大小变更)
- [Dict 字典](#dict-字典)
    - [数据结构](#数据结构)
    - [Hash 实现](#hash-实现)
# sorted

排序,在编程中经常遇到的算法,我也在README中介绍了一些关于排序的算法, 当然python内置了一些排序函数

## 内置函数sorted()/list.sort()的使用

### 1.简单应用

python对list有一个内置函数：sorted(),专门用于排序.举例：

	>>> a=[5,3,6,1,9,2]
	>>> sorted(a)       #a经过sorted之后,得到一个排序结果
	[1, 2, 3, 5, 6, 9]  #但是,原有的a并没有受到影响
	>>> a
	[5, 3, 6, 1, 9, 2]

也可以使用list.sort()来进行上述操作.

    >>> a.sort()
    >>> a               #注意这里,经过list.sort()之后,原有
    [1, 2, 3, 5, 6, 9]  #a的顺序已经发生变化,与上述不同之处.

**sorted和list.sort()的区别:**  list.sort()只能对list类型进行排序.如下：

    >>> b_dict={1:'e',3:'m',9:'a',5:'e'}
    >>> b_dict.sort()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      AttributeError: 'dict' object has no attribute 'sort'

而sorted则不然,看例子：

    >>> b_dict
    {1: 'e', 3: 'm', 5: 'e', 9: 'a'}
    >>> sorted(b_dict)
    [1, 3, 5, 9]

sorted之后,上述对dictinoary中,将key值取出并排序,返回list类型的排序结果.

### 2.按照指定关键词排序

在list.sort()和sorted中,都可以根据指定的key值排序.例如：

sorted的例子：

    >>> qw="I am Qiwsir you can read my articles im my blog".split()
    >>> qw
    ['I', 'am', 'Qiwsir', 'you', 'can', 'read', 'my', 'articles', 'im', 'my', 'blog']
    >>> sorted(qw,key=str.lower)        #按照字母升序排列
    ['am', 'articles', 'blog', 'can', 'I', 'im', 'my', 'my', 'Qiwsir', 'read', 'you']

list.sort()的例子：

    >>> qw
    ['I', 'am', 'Qiwsir', 'you', 'can', 'read', 'my', 'articles', 'im', 'my', 'blog']
    >>> qw.sort(key=str.lower)
    >>> qw
    ['am', 'articles', 'blog', 'can', 'I', 'im', 'my', 'my', 'Qiwsir', 'read', 'you']

此外,key还可以接收函数的单一返回值,按照该值排序.例如：

    >>> name_mark_age = [('zhangsan','A',15),('LISI','B',14),('WANGWU','A',16)]
    >>> sorted(name_mark_age, key = lambda x: x[2])     #根据年龄排序
    [('LISI', 'B', 14), ('zhangsan', 'A', 15), ('WANGWU', 'A', 16)]

    >>> sorted(name_mark_age, key = lambda x: x[1])     #根据等级排序
    [('zhangsan', 'A', 15), ('WANGWU', 'A', 16), ('LISI', 'B', 14)]

    >>> sorted(name_mark_age, key = lambda x: x[0])     #根据姓名排序
    [('LISI', 'B', 14), ('WANGWU', 'A', 16), ('zhangsan', 'A', 15)]

### 3.operator.itemgetter

除了上述方式,python中还提供了一个选择循环选择指定元组值的模块

    >>> from operator import itemgetter    #官方文档：https://docs.python.org/2/library/operator.html#module-operator
	>>> name_mark_age.append(('zhaoliu','B',16))
	>>> name_mark_age
	[('zhangsan', 'A', 15), ('LISI', 'B', 14), ('WANGWU', 'A', 16), ('zhaoliu', 'B', 16)]

    >>> sorted(name_mark_age,key=itemgetter(2))     #按照年龄排序
	[('LISI', 'B', 14), ('zhangsan', 'A', 15), ('WANGWU', 'A', 16), ('zhaoliu', 'B', 16)]

	>>> sorted(name_mark_age,key=itemgetter(1,2))   #先按照等级排序,相同等级看年龄
	[('zhangsan', 'A', 15), ('WANGWU', 'A', 16), ('LISI', 'B', 14), ('zhaoliu', 'B', 16)]


在官方文档上,有这样一个例子,和上面的操作是完全一样的.

    >>> class Student:
            def __init__(self, name, grade, age):
                self.name = name
                self.grade = grade
                self.age = age

            def __repr__(self):
                return repr((self.name, self.grade, self.age))

    >>> student_objects = [
            Student('john', 'A', 15),       #注意这里,用class Student来生成列表内的值
            Student('jane', 'B', 12),       #因此,可以通过student_objects[i].age来访问某个名称的年龄,i=0,则是john的年龄
            Student('dave', 'B', 10),
            ]

    >>> sorted(student_objects, key=lambda student: student.age)
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

也可以引用operator模块来实现上述排序

    >>>from operator import attrgetter
    >>> sorted(student_objects, key=attrgetter('age'))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]
    >>> sorted(student_objects, key=attrgetter('grade', 'age'))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

**总结：**sorted的能力超强,不仅实现排序,还能按照指定关键词排序.

以上例子都是升序,如果,增加reverse=True.例如：

    >>>from operator import itemgetter
    >>> name_mark_age
    [('zhangsan', 'A', 15), ('LISI', 'B', 14), ('WANGWU', 'A', 16), ('zhaoliu', 'B', 16)]
    >>> sorted(name_mark_age, key=itemgetter(2),reverse=True)
    [('WANGWU', 'A', 16), ('zhaoliu', 'B', 16), ('zhangsan', 'A', 15), ('LISI', 'B', 14)]

## 原理

通常如果我们不看sorted源码, 我们可能会认为sorted用的是快排或者归并排序, 因为这毕竟是普通排序算法中比较快的nlog(n) 算法, 那归并因为空间复杂度是O(n),所以在大数据量上排序会占用较大的内存,快排虽然空间复杂度是O(1), 但是最坏时间复杂度可能达到O(n^2),并且还是不稳定排序算法.更别说虽然高大上的桶排序, 计数排序(O(N))等都对要处理的数据有苛刻的要求.

所以看着这里我们应该得到一个共识, 就是没有任何一种排序算法是完美的, 要不然其他排序算法还留着干嘛

这也就是为什么很多语言的内部排序方法的实现都是基于多种算法的组合.

Golang：

    标准库中是Sort用的是快排+ 希尔 + 插排

    1 数据量大于12时用快排

    2 小于等于12时用6做为gap做一次希尔排序,然后走一遍普通的插排（插排对有序度高的序列效率高）

Java：

    Array.sort

    1.当 数组length小于47 时 使用插入排序

    2.当小于286时,使用快速排序

    3.超过286使用合并排序

    其中快速排序的pivot是采用5数取中的方法,五个数分别在数组的中间,并以长度的 1/7 向
    前后再各取两个.并且快速排序中增加了有序序列的监测

Python:
 Timsort算法

本质上 Timsort 是一个经过大量优化的归并排序,而归并排序已经到达了最坏情况下,比较排序算法时间复杂度的下界,所以在最坏的情况下,Timsort 时间复杂度为 O(nlogn)O(nlogn)O(nlogn).在最佳情况下,即输入已经排好序,它则以线性时间运行O(n)O(n)O(n).可以看出Timsort是目前最好的排序方式

完善的基本工作过程是：

 1.扫描数组,确定其中的单调上升段和严格单调下降段,将严格下降段反转.我们将这样的段称之为run.

 2.定义最小run长度,短于此的run通过插入排序合并为长度高于最小run长度；

 3.反复归并一些相邻run,过程中需要避免归并长度相差很大的run,直至整个排序完成；

 4.如何避免归并长度相差很大run呢, 依次将run压入栈中,若栈顶run X,run Y,run Z 的长度违反了X>Y+Z 或 Y>Z 则Y run与较小长度的run合并,并再次放入栈中. 依据这个法则,能够尽量使得大小相同的run合并,以提高性能.注意Timsort是稳定排序故只有相邻的run才能归并.

 5.Merge操作还可以辅之以galloping

混用插入排序与归并排序,二分搜索等算法,亮点是充分利用待排序数据可能部分有序的事实,并且依据待排序数据内容动态改变排序策略——选择性进行归并以及galloping

请看 wiki的解释：http://en.wikipedia.org/wiki/Timsort

国内有一个文档,适当翻译：http://blog.csdn.net/yangzhongblog/article/details/8184707


从时间复杂度来看,Timsort是威武的.更详细各种排序对比请看README中内容

![](../pics/python/timsort1.png)

从空间复杂度来讲,需要的开销在数量大的时候会增大.

![](../pics/python/timsort2.png)


# list 列表

大多数语言中列表有两种实现方式数组和链表,

Python中的列表是由对其它对象的引用组成的连续数组.指向这个数组的指针及其长度被保存在一个列表头结构中.这意味着,每次添加或删除一个元素时,由引用组成的数组需要该标大小（重新分配）.幸运的是,Python在创建这些数组时采用了指数分配,所以并不是每次操作都需要改变数组的大小.但是,也因为这个原因添加或取出元素的平摊复杂度较低

我们看下c中是怎么实现python 的list

## 数据结构

```
typedef struct {
    PyObject_VAR_HEAD
    PyObject **ob_item;
    Py_ssize_t allocated;
} PyListObject;
```
其中可以看到 ob_item,这是指向列表元素的指针数组,allocated 是指申请的内存的槽的个数.

简单的说下就是列表对象在 C 程序中的数据结构：有一个指针数组用来保存列表元素的指针,和一个可以在列表中放多少元素的标记.

## 数组大小变更

insert/append

list先分配一个对象的内存块, 再给这个对象分配一个内存槽的大小. 这个内存槽的大小不等于元素的个数, 会比元素个数大一点,目的就是为了防止在每次添加元素的时候都去调用分配内存的函数,或者涉及到数据的搬移, 这块内容可以了解下数组的这种结构

pop/remove

同样在pop或删除元素时, 如果发现元素个数已经小于槽数的一半,就会缩减槽的大小


# Dict 字典
## 数据结构

字典是通过散列表或说哈希表实现的，字典也被称为关联数组，还称为哈希数组等,数组的索引是键经过哈希函数处理后得到的散列值。

哈希函数的目的是使键均匀地分布在数组中，并且可以在内存中以O(1)的时间复杂度进行寻址，从而实现快速查找和修改

Python中所有不可变的内置类型都是可哈希的.可变类型（如列表,字典和集合）就是不可哈希的,因此不能作为字典的键.

字典的三个基本操作（添加元素,获取元素和删除元素）的平均事件复杂度为O(1),但是他们的平摊最坏情况复杂度要高得多,为O(N)

字典中的每个键都占用一个单元, 一个单元分为两部分, 分别是对键的引用和对值的引用,

使用hash函数获得键的散列值, 散列值对数组长度取余, 取得的值就是存放位置的索引

**哈希冲突(数组的索引相同), 使用开放寻址法解决**
这也是python中要求字典的key必须可hash的原因

数组中1/3的位置为空, 增加元素可能会导致扩容, 引发新的散列冲突, 导致新的散列表中键的次序发生变化, 这也是字典遍历时不能添加和删除的原因

字典在内存中开销很大, 实际上是以空间换时间


## Hash 实现

通常情况下建立哈希表的具体过程如下：

1 数据添加：把key通过哈希函数转换成一个整型数字，然后就将该数字对数组长度进行取余，取余结果就当作数组的下标，将value存储在以该数字为下标的数组空间里。

2 数据查询：再次使用哈希函数将key转换为对应的数组下标，并定位到数组的位置获取value

哈希函数就是一个映射，因此哈希函数的设定很灵活，只要使得任何关键字由此所得的哈希函数值都落在表长允许的范围之内即可。本质上看哈希函数不可能做成一个一对一的映射关系，其本质是一个多对一的映射，这也就引出了下面一个概念–哈希冲突或者说哈希碰撞。哈希碰撞是不可避免的，但是一个好的哈希函数的设计需要尽量避免哈希碰撞。


常见的哈希碰撞解决方法：

1 开放寻址法（open addressing）

开放寻址法中，所有的元素都存放在散列表里，当产生哈希冲突时，通过一个探测函数计算出下一个候选位置，如果下一个获选位置还是有冲突，那么不断通过探测函数往下找，直到找个一个空槽来存放待插入元素。

开放地址的意思是除了哈希函数得出的地址可用，当出现冲突的时候其他的地址也一样可用，常见的开放地址思想的方法有线性探测再散列，二次探测再散列等，这些方法都是在第一选择被占用的情况下的解决方法。

2 再哈希法

这个方法是按顺序规定多个哈希函数，每次查询的时候按顺序调用哈希函数，调用到第一个为空的时候返回不存在，调用到此键的时候返回其值。

3 链地址法

将所有关键字哈希值相同的记录都存在同一线性链表中，这样不需要占用其他的哈希地址，相同的哈希值在一条链表上，按顺序遍历就可以找到。

4 公共溢出区

其基本思想是：所有关键字和基本表中关键字为相同哈希值的记录，不管他们由哈希函数得到的哈希地址是什么，一旦发生冲突，都填入溢出表。

5 装填因子α

一般情况下，处理冲突方法相同的哈希表，其平均查找长度依赖于哈希表的装填因子。哈希表的装填因子定义为表中填入的记录数和哈希表长度的比值，也就是标志着哈希表的装满程度。直观看来，α越小，发生冲突的可能性就越小，反之越大。一般0.75比较合适，涉及数学推导。

    在python中一个key-value是一个entry，

    entry有三种状态。

    Unused： me_key == me_value == NULL

    Unused是entry的初始状态，key和value都为NULL。插入元素时，Unused状态转换成Active状态。这是me_key为NULL的唯一情况。

    Active： me_key != NULL and me_key != dummy 且 me_value != NULL

    插入元素后，entry就成了Active状态，这是me_value唯一不为NULL的情况，删除元素时Active状态刻转换成Dummy状态。

    Dummy： me_key == dummy 且 me_value == NULL

    此处的dummy对象实际上一个PyStringObject对象，仅作为指示标志。Dummy状态的元素可以在插入元素的时候将它变成Active状态，但它不可能再变成Unused状态。

为什么entry有Dummy状态呢？这是因为采用开放寻址法中，遇到哈希冲突时会找到下一个合适的位置，例如某元素经过哈希计算应该插入到A处，但是此时A处有元素的，通过探测函数计算得到下一个位置B，仍然有元素，直到找到位置C为止，此时ABC构成了探测链，查找元素时如果hash值相同，那么也是顺着这条探测链不断往后找，当删除探测链中的某个元素时，比如B，如果直接把B从哈希表中移除，即变成Unused状态，那么C就不可能再找到了，因为AC之间出现了断裂的现象，正是如此才出现了第三种状态---Dummy，Dummy是一种类似的伪删除方式，保证探测链的连续性。
