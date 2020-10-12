# api

* [Rest](api.md#rest)
  * [概念](api.md#概念)
  * [设计原则](api.md#设计原则)
* [身份验证](api.md#身份验证)
  * [初探OAuth,Token和JWT](api.md#初探oauthtoken和jwt)
    * [什么是OAuth?](api.md#什么是oauth)
    * [什么是Token?](api.md#什么是token)
    * [什么又是JWT？](api.md#什么又是jwt)
    * [三者之间又是什么关系?](api.md#三者之间又是什么关系)
  * [OAuth](api.md#oauth)
    * [概念](api.md#概念)
    * [设计思路](api.md#设计思路)
    * [原理](api.md#原理)
    * [名词](api.md#名词)
    * [应用场景](api.md#应用场景)
  * [Token](api.md#token)
    * [概念](api.md#概念)
    * [原理](api.md#原理)
      * [Access Token 类型](api.md#access-token-类型)
      * [认证请求方式](api.md#认证请求方式)
  * [JWT](api.md#jwt)
    * [概念](api.md#概念)
    * [原理](api.md#原理)
    * [应用场景](api.md#应用场景)
      * [无状态的分布式API](api.md#无状态的分布式api)
  * [参考](api.md#参考)

    **Rest**

### 概念

REST（Representational State Transfer）这个词，是Roy Thomas Fielding在他2000年的博士论文中提出的。

Fielding是HTTP协议（1.0版和1.1版）的主要设计者、Apache服务器软件的作者之一、Apache基金会的第一任主席。

> 本文研究计算机科学两大前沿----软件和网络----的交叉点。长期以来，软件研究主要关注软件设计的分类、设计方法的演化，很少客观地评估不同的设计选择对系统行为的影响。而相反地，网络研究主要关注系统之间通信行为的细节、如何改进特定通信机制的表现，常常忽视了一个事实，那就是改变应用程序的互动风格比改变互动协议，对整体表现有更大的影响。我这篇文章的写作目的，就是想在符合架构原理的前提下，理解和评估以网络为基础的应用软件的架构设计，得到一个功能强、性能好、适宜通信的架构。

论文： [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

REST章节 ： [Representational State Transfer \(REST\)](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)

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

### 设计原则

* get [https://api.example.com/v1/employees/11/groups?page=1](https://api.example.com/v1/employees/11/groups?page=1)
* 协议： https or http 推荐前者
* 域名： api.example.com or example.org/api 推荐前者
* 版本： v1
* 端点endpoint： employees 复数名词
* HTTP动作: get

  ```text
    GET: 获取某个资源，GET操作应该是幂等（idempotence）的，且无副作用。

    POST: 创建一个新的资源。

    PUT: 替换某个已有的资源。PUT操作虽然有副作用，但其应该是幂等的。

    PATCH（RFC5789）: 修改某个已有的资源。

    DELETE：删除某个资源。DELETE操作有副作用，但也是幂等的。
  ```

* Headers 请求头

  ```text
    Accept：服务器需要返回什么样的content。如果客户端要求返回"application/xml"，服务器端只能返回"application/json"，那么最好返回status code 406 not acceptable（RFC2616），当然，返回application/json也并不违背RFC的定义。一个合格的REST API需要根据Accept头来灵活返回合适的数据。

    If-Modified-Since/If-None-Match：如果客户端提供某个条件，那么当这条件满足时，才返回数据，否则返回304 not modified。比如客户端已经缓存了某个数据，它只是想看看有没有新的数据时，会用这两个header之一，服务器如果不理不睬，依旧做足全套功课，返回200 ok，那就既不专业，也不高效了。

    If-Match：在对某个资源做PUT/PATCH/DELETE操作时，服务器应该要求客户端提供If-Match头，只有客户端提供的Etag与服务器对应资源的Etag一致，才进行操作，否则返回412 precondition failed。这个头非常重要，下文详解。
  ```

* 参数： page
* Response 状态码： 200

  ```text
    GET: 200 OK
    POST: 201 Created
    PUT: 200 OK
    PATCH: 200 OK
    DELETE: 204 No Content
  ```

* Response 结果：

  ```text
    GET /collection：返回资源对象的列表（数组）
    GET /collection/resource：返回单个资源对象
    POST /collection：返回新生成的资源对象
    PUT /collection/resource：返回完整的资源对象
    PATCH /collection/resource：返回完整的资源对象
    DELETE /collection/resource：返回一个空文档
  ```

* Response 错误

  ```text
    {
        "error": "Invalid payoad.",
        "detail": {
            "surname": "This field is required."
        }
    }
  ```

* 嵌套还是不嵌套？没有定式， 我个人用前者嵌套类型描述了一对多的关系

  ```text
    获取雇员的所在团队
    employees/11/groups or /employees/?groups_id=11
  ```

* 优雅地处理尾部斜杠 保持一致
* 分清 401 和 403

## 身份验证

### 初探OAuth,Token和JWT

#### 什么是OAuth?

OAuth是一个开放标准,提供了一种简单和标准的安全授权方法,允许用户无需将某个网站的用户名密码提供给第三方应用就可以让该第三方应用访问该用户在某网站上的某些特定信息\(如简单的个人信息\),现在一般用的是OAuth 2.0\(不兼容1.0\).

#### 什么是Token?

Token就是获取信息的凭证,就是Access Token,让客户端无需用户密码即可获取用户授权的某些资源.

#### 什么又是JWT？

JSON Web Tokens, 这是一个开放的标准,规定了一种Token实现方式,以JSON为格式.

#### 三者之间又是什么关系?

这三个相互连接且是由大到小的一种关系,OAuth规定授权流程,Token为其中一环的一个信息载体,具体的一种实现方式由JWT规定

### OAuth

#### 概念

OAuth 2.0: 是一个开放标准,提供了一种简单和标准的安全授权方法,允许用户无需将某个网站的用户名密码提供给第三方应用就可以让该第三方应用访问该用户在某网站上的某些特定信息\(如简单的个人信息\)。

> The OAuth 2.0 authorization framework enables a third-party application to obtain limited access to an HTTP service, either on behalf of a resource owner by orchestrating an approval interaction between the resource owner and the HTTP service, or by allowing the third-party application to obtain access on its own behalf. [RFC6749](https://tools.ietf.org/html/rfc6749) [rfc6749](http://www.rfcreader.com/#rfc6749)

#### 设计思路

OAuth在"客户端"与"服务提供商"之间，设置了一个授权层（authorization layer）。"客户端"不能直接登录"服务提供商"，只能登录授权层，以此将用户与客户端区分开来。"客户端"登录授权层所用的令牌（token），与用户的密码不同。用户可以在登录的时候，指定授权层令牌的权限范围和有效期。

"客户端"登录授权层以后，"服务提供商"根据令牌的权限范围和有效期，向"客户端"开放用户储存的资料。

#### 原理

```text
  +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+
```

```text
（A）用户打开客户端以后，客户端要求用户给予授权。

（B）用户同意给予客户端授权。

（C）客户端使用上一步获得的授权，向认证服务器申请令牌。

（D）认证服务器对客户端进行认证以后，确认无误，同意发放令牌。

（E）客户端使用令牌，向资源服务器申请获取资源。

（F）资源服务器确认令牌无误，同意向客户端开放资源。
```

更详细的可以看这篇文章 [理解OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)

#### 名词

**Roles角色**

应用程序或者用户都可以是下边的任何一种角色：

* 资源拥有者
* 资源服务器
* 客户端应用
* 认证服务器

**Client Types客户端类型**

这里的客户端主要指API的使用者。它可以是的类型：

* 私有的
* 公开的

**Client Profile客户端描述**

OAuth2框架也指定了集中客户端描述，用来表示应用程序的类型：

* Web应用
* 用户代理
* 原声应用

**Authorization Grants认证授权**

认证授权代表资源拥有者授权给客户端应用程序的一组权限，可以是下边几种形式：

* 授权码
* 隐式授权
* 资源拥有者密码证书
* 客户端证书
* Endpoints终端

**OAuth2框架需要下边几种终端：**

* 认证终端
* Token终端
* 重定向终端

#### 应用场景

* 外部认证服务器

  通过第三方认证服务， 来完成服务授权控制

  优势

  * 快速开发
  * 实施代码量小
  * 维护工作减少

* 大型企业解决方案

  API调用方很多， 并且每个app使用方式不一样， 应该抽象出独立灵活的安全策略

  优势

  * 灵活的实现方式
  * 可以和JWT同时使用
  * 可针对不同应用扩展

### Token

#### 概念

Token就是获取信息的凭证, 关于Token的具体使用有相应的RFC文件指导: [The OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6750)

#### 原理

**Access Token 类型**

Token的类型可分为两种:

1 **bearer**. 包含一个简单的Token字符串.

2 **mac**. 由消息授权码\(Message Authentication Code\)和Token组成.

示例:

```text
// bearer
GET /resource/1 HTTP/1.1
Host: example.com
Authorization: Bearer mF_9.B5f-4.1JqM

// mac
GET /resource/1 HTTP/1.1
Host: example.com
Authorization: MAC id="h480djs93hd8",
                   nonce="274312:dj83hs9s",
               mac="kDZvddkndxvhGRXZhvuDjEhGeE="
```

**认证请求方式**

使用Token的认证请求的方式有三种,客户端可以选择一种来实现,但是不能同时使用多种:

* 放在请求头
* 放在请求体
* 放在URI

  详细如下:

**1 放在请求头**

放在Header的Authorization中,并使用Bearer开头:

```text
GET /resource HTTP/1.1
Host: server.example.com
Authorization: Bearer mF_9.AAW3_AH
```

**2 放在请求体**

放在body中的access\_token参数中,并且满足以下条件:

* HTTP请求头的Content-Type设置成application/x-www-form-urlencoded.
* Body参数是single-part.
* HTTP请求方法应该是推荐可以携带Body参数的方法,比如POST,不推荐GET.

示例:

```text
POST /resource HTTP/1.1
Host: server.example.com
Content-Type: application/x-www-form-urlencoded

access_token=mF_9.B5f-4.1JqM
```

**3 放在URI**

放在uri中的access\_token参数中

```text
GET /resource?access_token=mF_9.B5f-4.1JqM
Host: server.example.com
```

### JWT

#### 概念

[JWT](https://jwt.io/)是一种安全标准。基本思路就是用户提供用户名和密码给认证服务器，服务器验证用户提交信息信息的合法性；如果验证成功，会产生并返回一个Token（令牌），用户可以使用这个token访问服务器上受保护的资源。

> JSON Web Token \(JWT\) is a compact URL-safe means of representing claims to be transferred between two parties. The claims in a JWT are encoded as a JSON object that is digitally signed using JSON Web Signature \(JWS\). -[RFC7519](https://tools.ietf.org/html/rfc7519)

#### 原理

JWT的结构分为三个部分header.payload.signature:

* Header: 存放Token类型和加密的方法
* Payload: 包含一些用户身份信息.
* Signature: 签名是将前面的Header,Payload信息以及一个密钥组合起来并使用Header中的算法进行加密

最终生成的是一个有两个.号连接的字符串,前两个部分是Header和Payload的Base64编码,最后一个是签名,如下:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFONFh7HgQ
```

**HEADER:ALGORITHM & TOKEN TYPE**

```text
头部分简单声明了类型(JWT)以及产生签名所使用的算法
```

```text
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**PAYLOAD:DATA**

```text
声明部分是整个token的核心，表示要发送的用户详细信息。
```

```text
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```

**VERIFY SIGNATURE**

```text
签名的目的是为了保证上边两部分信息不被篡改。如果尝试使用Bas64对解码后的token进行修改，签名信息就会失效。一般使用一个私钥（private key）通过特定算法对Header和Claims进行混淆产生签名信息，所以只有原始的token才能于签名信息匹配。
        这里有一个重要的实现细节。只有获取了私钥的应用程序（比如服务器端应用）才能完全认证token包含声明信息的合法性。所以，永远不要把私钥信息放在客户端（比如浏览器）。
```

```text
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),

your-256-bit-secret

) secret base64 encoded
```

#### 应用场景

**无状态的分布式API**

JWT的主要优势在于使用无状态、可扩展的方式处理应用中的用户会话。服务端可以通过内嵌的声明信息，很容易地获取用户的会话信息，而不需要去访问用户或会话的数据库。在一个分布式的面向服务的框架中，这一点非常有用。 但是，如果系统中需要使用黑名单实现长期有效的token刷新机制，这种无状态的优势就不明显了。

**优势**

* 快速开发
* 不需要cookie
* JSON在移动端的广泛应用
* 不依赖于社交登录
* 相对简单的概念理解

**限制**

* Token有长度限制
* Token不能撤销
* 需要token有失效时间限制\(exp\)
* OAuth2使用场景

### 参考

[Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

[JWT官方网站](http://jwt.io)

[OAuth2官方网站](http://oauth.net/2/)

[理解OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)

[OAuth2和JWT - 如何设计安全的API](https://www.jianshu.com/p/1f2d6e5126cb)

[OAuth,Token和JWT](https://www.jianshu.com/p/9f80be6ba2e9)

[OAuth 2.0 Tutorial](http://tutorials.jenkov.com/oauth2/overview.html)

