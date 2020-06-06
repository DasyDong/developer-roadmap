- [Mysql](#mysql)   
    - [ORM](#orm)
    - [ACID](#acid)
        - [MySQL的四种事务隔离级别](#mysql的四种事务隔离级别)
    - [N+1](#n1)
    - [索引](#索引)
        - [索引的工作原理及其种类](#索引的工作原理及其种类)
        - [主键 超键 候选键 外键](#主键-超键-候选键-外键)
        - [视图的作用，视图可以更改么？](#视图的作用视图可以更改么)
        - [drop,delete与truncate的区别](#dropdelete与truncate的区别)
    - [连接的种类](#连接的种类)
    - [数据库优化的思路](#数据库优化的思路)
    - [存储过程与触发器的区别](#存储过程与触发器的区别)
    - [悲观锁和乐观锁是什么？](#悲观锁和乐观锁是什么)
    - [你常用的mysql引擎有哪些?各引擎间有什么区别?](#你常用的mysql引擎有哪些各引擎间有什么区别)
    - [参考](#参考)
# Mysql
## ORM

对象关系映射（Object Relational Mapping，简称ORM）是通过使用描述对象和数据库之间映射的元数据，将面向对象语言程序中的对象自动持久化到关系数据库中。本质上就是将数据从一种形式转换到另外一种形式

当我们使用关系型数据库， 譬如mysql 会使用
```
SELECT * FROM users WHERE email = 'test@test.com';
```
ORM 就是会让你通过面向对象范型的编程语言来写出上述或者更复杂的语句

**ORM优势**
* 你可以用你更擅长的语言来编写sql， 不需要你对sql很熟悉
* DRY 实现复用
* DDD架构或者MVC架构代码更整洁
* 高度抽象， 可以让你在多种数据库中mysql或者postgresSQl切换
* ORM基本都支持各种高阶特性， 譬如事务， 连接池， 迁移， 数据流等
* orm的执行语句会比你自己裸写的sql语句性能更好

**ORM劣势**
* 如果你是sql专家， 那可能你写sql比orm性能更好
* 学习ORM也是有成本的
* 一个程序员应该懂数据库或者sql的底层实现，虽然ORM简化了写sql的成本，但也可能让你不能深入理解sql原理

比较流行的ORM

* Java: Hibernate.
* PHP: Propel or Doctrine (I prefer the last one).
* Python: the Django ORM or SQLAlchemy (My favorite ORM library ever).
* C#: NHibernate or Entity Framework

## ACID

### MySQL的四种事务隔离级别
一、事务的基本要素（ACID）

　　1、原子性（Atomicity）：事务开始后所有操作，要么全部做完，要么全部不做，不可能停滞在中间环节。事务执行过程中出错，会回滚到事务开始前的状态，所有的操作就像没有发生一样。也就是说事务是一个不可分割的整体，就像化学中学过的原子，是物质构成的基本单位。

　　 2、一致性（Consistency）：事务开始前和结束后，数据库的完整性约束没有被破坏 。比如A向B转账，不可能A扣了钱，B却没收到。

　　 3、隔离性（Isolation）：同一时间，只允许一个事务请求同一数据，不同的事务之间彼此没有任何干扰。比如A正在从一张银行卡中取钱，在A取钱的过程结束前，B不能向这张卡转账。

　　 4、持久性（Durability）：事务完成后，事务对数据库的所有更新将被保存到数据库，不能回滚

二、事务的并发问题

　　1、脏读：事务A读取了事务B更新的数据，然后B回滚操作，那么A读取到的数据是脏数据

　　2、不可重复读：事务 A 多次读取同一数据，事务 B 在事务A多次读取的过程中，对数据作了更新并提交，导致事务A多次读取同一数据时，结果 不一致。

　　3、幻读：系统管理员A将数据库中所有学生的成绩从具体分数改为ABCDE等级，但是系统管理员B就在这个时候插入了一条具体分数的记录，当系统管理员A改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读。

　　小结：不可重复读的和幻读很容易混淆，不可重复读侧重于修改，幻读侧重于新增或删除。解决不可重复读的问题只需锁住满足条件的行，解决幻读需要锁表

三、MySQL事务隔离级别

事务隔离级别 | 脏读 | 不可重复读 | 幻读 |
:--- | :--- | :--- | :--- |
读未提交（read-uncommitted）|	会 | 会	| 会 |
不可重复读（read-committed）|	不会	| 会	| 会 |
可重复读（repeatable-read）| 不会 |	不会	| 会 |
串行化（serializable）|	不会 |	不会	| 不会 |

mysql默认的事务隔离级别为repeatable-read

show global variables like ‘tx_isolation’

四
https://www.cnblogs.com/wyaokai/p/10921323.html

补充：

　　1、事务隔离级别为读提交时，写数据只会锁住相应的行

　　2、事务隔离级别为可重复读时，如果检索条件有索引（包括主键索引）的时候，默认加锁方式是next-key 锁；如果检索条件没有索引，更新数据时会锁住整张表。一个间隙被事务加了锁，其他事务是不能在这个间隙插入记录的，这样可以防止幻读。

　　3、事务隔离级别为串行化时，读写数据都会锁住整张表

　　 4、隔离级别越高，越能保证数据的完整性和一致性，但是对并发性能的影响也越大。

　　 5、MYSQL MVCC实现机制参考链接：https://blog.csdn.net/whoamiyang/article/details/51901888

　　 6、关于next-key 锁可以参考链接：https://blog.csdn.net/bigtree_3721/article/details/73731377

## N+1

```
class Video(models.Model):
    url = models.URLField(unique=True)
    .....

class Comment(models.Model):
    title = models.CharField(max_length=128)
    video = models.ForeignKey('Video')
        .....
```
在orm框架中，比如python的django可以设置关联对象，比如Video对象关联comment

假如查询出n个video，那么需要做n次查询comment，查询video是一次select，查询video关联的
comment，是n次，所以是n+1问题，其实叫1+n更为合理一些。

查询主数据，是1次查询，查询出n条记录；根据这n条主记录，查询从记录，共需要n次，所以叫数据库1+n问题；这样会带来性能问题，比如，查询到的n条记录，我可能只用到其中1条，但是也执行了n次从记录查询，这是不合理的。

**解决方式：**

把N+1次查询变成2次查询

简单说 先执行 select *,category_id from article limited 0,N

然后遍历结果列表,取出所有的category_id,去掉重复项

再执行一次 select name from category where id in (category id list)


把子查询/join查询 分成两次,是 高并发网站数据库调优中非常有效的常见做法,虽然会花费更多的cpu时间,但是避免了系统的死锁,提高了并发响应能力

譬如django中就用select_related使用SQL的JOIN语句进行优化，通过减少SQL查询的次数来进行优化、提高性能。

Article.ojbects.select_related() 这就是inner join

Article.objects.prefetch_related('category') 这是2次查询


## 索引
### 索引的工作原理及其种类
一、概述

在mysql中，索引（index）又叫键（key），它是存储引擎用于快速找到所需记录的一种数据结构。在越来越大的表中，索引是对查询性能优化最有效的手段，索引对性能影响非常关键。另外，mysql的索引是在存储引擎层实现，而不是在服务器层。

二、索引的工作原理

我们知道，在看一本书某章的时候，首先我们会查找目录索引，找到对应的页码然后快速找到相应的内容。mysql索引也一样，存储引擎利用类似的方法使用索引，先在索引中找到对应的值，然后根据匹配的索引记录找到对应的数据行，然后返回结果。

例如，我们想在一个10W条记录表 table 中查询name等于“张三”的数据行，select * from table where name ='张三'。那么在没有对name字段建立索引的情况下，我们需要扫描全表也就是扫描10W条数据来找到这条数据；如果我们为name字段建立索引，我们只需要查找索引，然后根据索引找到对应的数据行，只需要查找一条记录，性能会得到很大的提高。

三、索引分类

索引按照实现方式不同可以分为 B-Tree索引、hash索引、空间数据索引以及全文索引等。如果没有特别指明，多半用的是B-Tree索引，B-Tree 对索引列是顺序存储的，因此很适合查找范围数据。它能够加快访问数据的速度，因为存储引擎不再需要进行全表扫描来获取需要的数据。

四、索引类型

索引主要分为：单列索引（普通索引、主键索引、唯一索引）和组合索引。

普通索引：

CREATE INDEX name_Index ON `table`(`name`);

1
ALTER TABLE table ADD INDEX name_Index(`name`)
唯一索引：

1
CREATE UNIQUE INDEX id_UNIQUE_Index ON `table`(`id`);
主键索引：主键索引和唯一索引类似，唯一索引允许有空值，而主键索引不允许。

组合索引：通俗的说，组合索引就是一个表中一个索引包括多个字段，一个表中多个单列索引并不是组合索引。

例如：

1
CREATE INDEX nickname_account_createdTime_Index ON `award`(`nickname`, `account`, `created_time`);
五、组合索引的查询规则（什么情况下有效，什么情况下无效）

B-Tree 索引适用于全键值、键值范围或键前缀查找，其中键前缀查找只适用于根据最左前缀查找。我们建立表user（id，last_name,first_name, age ,birthday,sex）,建立组合索引 key（last_name, first_name, birthday）,那么它实际上包括三个索引（last_name），（last_name，first_name），（last_name，first_name，birthday）。

下面我们来分析组合索引有效以及无效的情况，mysql在使用组合索引查询的时候需要遵循“最左前缀”规则，什么是“最左前缀”规则呢，就是在使用组合索引查询，where的条件要按照从左到右的顺序，last_name first_name birthday，可以是只有last_name，或者包括last_name、first_name，或者last_name、first_name、birthday，这个从左到右的顺序不能变，也不能跳过；如果是直接first_name='ruby' 组合索引不生效，或者跳过first_name，last_name=‘allon’ and birthday = ‘2012’，组合索引只有last_name生效，后面的所有不生效。

例如：1、全键值匹配：select * from user where last_name=‘allon’ and first_name='java' and birthday=‘2017-12'是生效的，如果 select * from user where first_name='java' and birthday=‘2017-12'组合索引是不生效的，因为没有key(first_name,birthday)的索引。

2、键前缀查找：select * from user where last_name=‘allon’；这个索引存在，也是有效的，但不能select * from user where first_name='java'，这样不生效。

3、like模糊查询：比如只匹配组合索引第一列的值的开头部分，查询last_name姓张的人，select * from user where last_name like ‘张%’；但是不能select * from user where last_name like ‘%张’；组合索引也无法查找以张结尾的人。 再如 select * from user where last_name='allon' and first_name like '三%' and birthday = '2012-11-06'，因为first_name用了like这个范围查询条件，那么查询只用到了组合索引的前两列，范围查询右面的列birthday无法用索引优化查询。

如果查询中有某个列的范围查询，则该列右边的所有列都无法使用索引优化查找

4、匹配范围值：select * from user where last_name between ’allon‘ and 'clitton';这里只使用了组合索引的第一列，是生效的。

六、索引的优缺点

优点：1、建立索引后，在查询的时候合理利用索引能够提高数据库性能；

2、主键索引 唯一索引能保证表中每一条数据的唯一性

3、减少分组和排序的时间

4、在表连接的连接条件上使用索引，可以加速表与表之间的相连。

缺点：

1、创建索引和维护索引需要时间消耗；

2、索引文件占用物理空间

3、当对表的数据进行insert update delete时候需要维护索引，会降低数据的维护数据。

### 主键 超键 候选键 外键
超键（super key）：在关系中能惟一标识元素属性的集称为关系模式的超键。

候选键：（Candidate Key）：不含有多余属性的超键称为候选键。也就是说在候选键中在删除属性，就不是键了。

主键（Primary Key)：用户选作元组标识的候选键为主键。一般不佳说明，键就是主键。

外键（Froeign Key）:如果模式R中的属性k是其他模式的主键，那么k在模式R中称为外键。

### 视图的作用，视图可以更改么？
### drop,delete与truncate的区别
1、drop (删除表)：删除内容和定义，释放空间。简单来说就是把整个表去掉.以后要新增数据是不可能的,除非新增一个表。

   drop语句将删除表的结构被依赖的约束（constrain),触发器（trigger)索引（index);依赖于该表的存储过程/函数将被保留，但其状态会变为：invalid。

2、truncate (清空表中的数据)：删除内容、释放空间但不删除定义(保留表的数据结构)。与drop不同的是,只是清空表数据而已。

   注意:truncate 不能删除行数据,要删就要把表清空。

3、delete (删除表中的数据)：delete 语句用于删除表中的行。delete语句执行删除的过程是每次从表中删除一行，并且同时将该行的删除操作作为事务记录在日志中保存

   以便进行进行回滚操作。

   truncate与不带where的delete ：只删除数据，而不删除表的结构（定义）

4、truncate table 删除表中的所有行，但表结构及其列、约束、索引等保持不变。新行标识所用的计数值重置为该列的种子。如果想保留标识计数值，请改用delete。

   如果要删除表定义及其数据，请使用 drop table 语句。

5、对于由foreign key约束引用的表，不能使用truncate table ，而应使用不带where子句的delete语句。由于truncate table 记录在日志中，所以它不能激活触发器。

6、执行速度，一般来说: drop> truncate > delete。

7、delete语句是数据库操作语言(dml)，这个操作会放到 rollback segement 中，事务提交之后才生效；如果有相应的 trigger，执行的时候将被触发。

   truncate、drop 是数据库定义语言(ddl)，操作立即生效，原数据不放到 rollback segment 中，不能回滚，操作不触发 trigger。

## 连接的种类
## 数据库优化的思路
## 存储过程与触发器的区别
## 悲观锁和乐观锁是什么？

悲观锁与乐观锁是两种常见的资源并发锁设计思路，也是并发编程中一个非常基础的概念。

(1). 悲观锁

定义: 假定会发生并发冲突，屏蔽一切可能违反数据完整性的操作。顾名思义，就是很悲观，每次去拿数据的时候都认为别人会修改，所以每次在拿数据的时候都会上锁，这样别人想拿这个数据就会block直到它拿到锁。
    
　　悲观锁的特点是先获取锁，再进行业务操作，即“悲观”的认为所有的操作均会导致并发安全问题，因此要先确保获取锁成功再进行业务操作。通常来讲，在数据库上的悲观锁需要数据库本身提供支持，即通过常用的select … for update操作来实现悲观锁。当数据库执行select … for update时会获取被select中的数据行的行锁，因此其他并发执行的select … for update如果试图选中同一行则会发生排斥（需要等待行锁被释放），因此达到锁的效果。select for update获取的行锁会在当前事务结束时自动释放，因此必须在事务中使用。

　　这里需要特别注意的是，不同的数据库对select… for update的实现和支持都是有所区别的，例如oracle支持select for update no wait，表示如果拿不到锁立刻报错，而不是等待，mysql就没有no wait这个选项。另外，mysql还有个问题是: select… for update语句执行中所有扫描过的行都会被锁上，这一点很容易造成问题。因此，如果在mysql中用悲观锁务必要确定使用了索引，而不是全表扫描。

(2). 乐观锁

定义：假设不会发生并发冲突，只在提交操作时检查是否违反数据完整性。顾名思义，就是很乐观，每次去拿数据的时候都认为别人不会修改，所以不会上锁，但是在提交更新的时候会判断一下在此期间别人有没有去更新这个数据。

　　乐观锁的特点先进行业务操作，只在最后实际更新数据时进行检查数据是否被更新过，若未被更新过，则更新成功；否则，失败重试。乐观锁在数据库上的实现完全是逻辑的，不需要数据库提供特殊的支持。一般的做法是在需要锁的数据上增加一个版本号或者时间戳，然后按照如下方式实现：

```
1. SELECT data AS old_data, version AS old_version FROM …;
2. 根据获取的数据进行业务操作，得到new_data和new_version
3. UPDATE SET data = new_data, version = new_version WHERE version = old_version
if (updated row > 0) {
    // 乐观锁获取成功，操作完成
} else {
    // 乐观锁获取失败，回滚并重试
}

```

　　乐观锁是否在事务中其实都是无所谓的，其底层机制是这样：在数据库内部update同一行的时候是不允许并发的，即数据库每次执行一条update语句时会获取被update行的写锁，直到这一行被成功更新后才释放。因此在业务操作进行前获取需要锁的数据的当前版本号，然后实际更新数据时再次对比版本号确认与之前获取的相同，并更新版本号，即可确认这其间没有发生并发的修改。如果更新失败，即可认为老版本的数据已经被并发修改掉而不存在了，此时认为获取锁失败，需要回滚整个业务操作并可根据需要重试整个过程。

(3). 悲观锁与乐观锁的应用场景

　　一般情况下，读多写少更适合用乐观锁，读少写多更适合用悲观锁。乐观锁在不发生取锁失败的情况下开销比悲观锁小，但是一旦发生失败回滚开销则比较大，因此适合用在取锁失败概率比较小的场景，可以提升系统并发性能。


## 你常用的mysql引擎有哪些?各引擎间有什么区别?

## 参考
[ORM-wiki](https://en.wikipedia.org/wiki/Object-relational_mapping)
[mysql锁](https://blog.csdn.net/justloveyou_/article/details/78308460)
