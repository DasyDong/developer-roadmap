- [Rest](#rest)
    - [概念](#概念)
    - [设计原则](#设计原则)
    - [参考](#参考)
# Rest

## 概念

REST（Representational State Transfer）这个词，是Roy Thomas Fielding在他2000年的博士论文中提出的。

Fielding是HTTP协议（1.0版和1.1版）的主要设计者、Apache服务器软件的作者之一、Apache基金会的第一任主席。

> 本文研究计算机科学两大前沿----软件和网络----的交叉点。长期以来，软件研究主要关注软件设计的分类、设计方法的演化，很少客观地评估不同的设计选择对系统行为的影响。而相反地，网络研究主要关注系统之间通信行为的细节、如何改进特定通信机制的表现，常常忽视了一个事实，那就是改变应用程序的互动风格比改变互动协议，对整体表现有更大的影响。我这篇文章的写作目的，就是想在符合架构原理的前提下，理解和评估以网络为基础的应用软件的架构设计，得到一个功能强、性能好、适宜通信的架构。


论文：  [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

REST章节 ： [Representational State Transfer (REST)](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)


理解一下rest？ 表现层状态转化?


**将资源通过一种外在表现形式，进行数据和状态转移的定义和过程就是Rest**

不理解？ ok 我们换下面这种？

* 每一个URI代表一种资源；
* 客户端和服务器之间，传递这种资源的某种表现层；
* 客户端通过四个HTTP动词（GET、POST、PUT和DELETE方法），对服务器端资源进行操作，实现"表现层状态改变"。

不理解？ ok 我们再换下面这种？

* 看Url就知道是什么
* 看http method就知道干什么
* 看http status code就知道结果

那什么是restful ？

**可以理解成基于rest风格创建的api就是restful，是目前最流行的一种互联网软件架构。它结构清晰、符合标准、易于理解、扩展方便。**

**RESTful API是目前比较成熟的一套互联网应用程序的API设计理论**


## 设计原则

* get https://api.example.com/v1/employees/11/groups?page=1

* 协议： https or http 推荐前者
* 域名： api.example.com or example.org/api 推荐前者
* 版本： v1
* 端点endpoint： employees 复数名词
* HTTP动作: get

        GET: 获取某个资源，GET操作应该是幂等（idempotence）的，且无副作用。

        POST: 创建一个新的资源。

        PUT: 替换某个已有的资源。PUT操作虽然有副作用，但其应该是幂等的。

        PATCH（RFC5789）: 修改某个已有的资源。

        DELETE：删除某个资源。DELETE操作有副作用，但也是幂等的。

* Headers 请求头

        Accept：服务器需要返回什么样的content。如果客户端要求返回"application/xml"，服务器端只能返回"application/json"，那么最好返回status code 406 not acceptable（RFC2616），当然，返回application/json也并不违背RFC的定义。一个合格的REST API需要根据Accept头来灵活返回合适的数据。

        If-Modified-Since/If-None-Match：如果客户端提供某个条件，那么当这条件满足时，才返回数据，否则返回304 not modified。比如客户端已经缓存了某个数据，它只是想看看有没有新的数据时，会用这两个header之一，服务器如果不理不睬，依旧做足全套功课，返回200 ok，那就既不专业，也不高效了。

        If-Match：在对某个资源做PUT/PATCH/DELETE操作时，服务器应该要求客户端提供If-Match头，只有客户端提供的Etag与服务器对应资源的Etag一致，才进行操作，否则返回412 precondition failed。这个头非常重要，下文详解。

* 参数： page
* Response 状态码： 200

        GET: 200 OK
        POST: 201 Created
        PUT: 200 OK
        PATCH: 200 OK
        DELETE: 204 No Content

* Response 结果：

        GET /collection：返回资源对象的列表（数组）
        GET /collection/resource：返回单个资源对象
        POST /collection：返回新生成的资源对象
        PUT /collection/resource：返回完整的资源对象
        PATCH /collection/resource：返回完整的资源对象
        DELETE /collection/resource：返回一个空文档

* Response 错误

        {
            "error": "Invalid payoad.",
            "detail": {
                "surname": "This field is required."
            }
        }

* 嵌套还是不嵌套？没有定式， 我个人用前者嵌套类型描述了一对多的关系

        获取雇员的所在团队
        employees/11/groups or /employees/?groups_id=11

* 优雅地处理尾部斜杠 保持一致

* 分清 401 和 403


## 参考
[Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)