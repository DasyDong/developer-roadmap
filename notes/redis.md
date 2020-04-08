- [Redis](#redis)   
        - [1.架构原理及应用实践](#1架构原理及应用实践)   
        - [2.Redis 的基本类型。](#2redis-的基本类型)   
        - [3.Redis集群方案该怎么做?都有哪些方案](#3redis集群方案该怎么做都有哪些方案)   
        - [4.redis和mecached的区别，以及使用场景](#4redis和mecached的区别以及使用场景)   
        - [5.Redis是单线程的，但Redis为什么这么快](#5redis是单线程的但redis为什么这么快)   
# Redis
### 1.架构原理及应用实践
https://www.jianshu.com/p/6c970eb652d5

### 2.Redis 的基本类型。
string, hash, list, set , zset(sorted set)

### 3.Redis集群方案该怎么做?都有哪些方案
https://blog.csdn.net/weixin_42117262/article/details/84196498
### 4.redis和mecached的区别，以及使用场景
1、redis和Memcache都是将数据存放在内存中，都是内存数据库。不过memcache还可以用于缓存其他东西，例如图片，视频等等

2、Redis不仅仅支持简单的k/v类型的数据，同时还提供list,set,hash等数据结构的存储

3、虚拟内存-redis当物流内存用完时，可以将一些很久没用的value交换到磁盘

4、过期策略-memcache在set时就指定，例如set key1 0 0 8，即永不过期。Redis可以通过例如expire设定，例如expire name 10

5、分布式-设定memcache集群，利用magent做一主多从，redis可以做一主多从。都可以一主一丛

6、存储数据安全-memcache挂掉后，数据没了，redis可以定期保存到磁盘(持久化)

7、灾难恢复-memcache挂掉后，数据不可恢复，redis数据丢失后可以通过aof恢复

8、Redis支持数据的备份，即master-slave模式的数据备份

9、应用场景不一样，redis除了作为NoSQL数据库使用外，还能用做消息队列，数据堆栈和数据缓存等;Memcache适合于缓存SQL语句，数据集，用户临时性数据，延迟查询数据和session等

使用场景

1,如果有持久方面的需求或对数据类型和处理有要求的应该选择redis

2,如果简单的key/value存储应该选择memcached.

### 5.Redis是单线程的，但Redis为什么这么快

https://segmentfault.com/a/1190000017375843
1、完全基于内存，绝大部分请求是纯粹的内存操作，非常快速。数据存在内存中，类似于HashMap，HashMap的优势就是查找和操作的时间复杂度都是O(1)；

2、数据结构简单，对数据操作也简单，Redis中的数据结构是专门进行设计的；

3、采用单线程，避免了不必要的上下文切换和竞争条件，也不存在多进程或者多线程导致的切换而消耗 CPU，不用去考虑各种锁的问题，不存在加锁释放锁操作，没有因为可能出现死锁而导致的性能消耗；

4、使用多路I/O复用模型，非阻塞IO；

5、使用底层模型不同，它们之间底层实现方式以及与客户端之间通信的应用协议不一样，Redis直接自己构建了VM 机制 ，因为一般的系统调用系统函数的话，会浪费一定的时间去移动和请求；
