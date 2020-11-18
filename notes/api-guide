- [后端接口规范](#后端接口规范)
    - [名词释义](#名词释义)
    - [前后端接口协作流程](#前后端接口协作流程)
    - [接口协商要点](#接口协商要点)
    - [后端接口通用规范](#后端接口通用规范)
        - [接口地址](#接口地址)
        - [接口版本](#接口版本)
        - [接口请求方式](#接口请求方式)
        - [使用统一的资源路径格式](#使用统一的资源路径格式)
            - [资源名（Resource names）](#资源名resource-names)
            - [行为（Actions）](#行为actions)
            - [路径和属性要小写](#路径和属性要小写)
            - [支持方便的无id间接引用](#支持方便的无id间接引用)
            - [不要只接受使用名字而放弃了使用id。](#不要只接受使用名字而放弃了使用id)
            - [最小化路径嵌套](#最小化路径嵌套)
        - [提供资源的(UU)ID](#提供资源的uuid)
        - [时间戳](#时间戳)
        - [嵌套外键关系](#嵌套外键关系)
        - [保证响应JSON最小化](#保证响应json最小化)
        - [接口参数](#接口参数)
            - [GET](#get)
            - [POST DELETE 等](#post-delete-等)
        - [HTTP verbs](#http-verbs)
        - [重定向](#重定向)
        - [接口返回的数据结构](#接口返回的数据结构)
        - [Status Code](#status-code)
        - [认证](#认证)
        - [权限](#权限)
        - [Rate Limiting 限额](#rate-limiting-限额)
        - [支持CORS Cross origin resource sharing](#支持cors-cross-origin-resource-sharing)
        - [分页 Pagnination](#分页-pagnination)
        - [过滤、排序](#过滤排序)
        - [限制返回的字段](#限制返回的字段)
        - [缓存](#缓存)
            - [后端缓存](#后端缓存)
            - [前端HTTP缓存](#前端http缓存)
        - [并发处理](#并发处理)
        - [最终规范](#最终规范)
        - [参考](#参考)
# 后端接口规范

## 名词释义
随着前后端分离越来越普遍, 后端接口规范也就越来越重要了. 一套良好的接口规范可以提升工作效率, 减少沟通障碍.

通常我们都会采用 REST 方式来提供接口, 使用 [JSON](http://json.org) 来传输数据.

| 名词        | 含义 |
|:----------|:-----------|
| 前端        | Web前端, APP端, 桌面端等一切属于用户界面的这一层 |
| 后端        | 即服务器端, 指一切属于用户界面之下的这一层 |
| 前后端接口  | 前端与后端进行数据交互的统称, 也叫做数据接口, 属于一种远程调用, 一般指前端通过HTTP(ajax)请求获取到的数据或者执行的某项操作. 为确保前后端(工程师)的协作沟通, 一般由前端和后端一起来定义接口的规范, 规范的内容一般包含接口的地址, 接口的输入参数和输出的数据格式(结构), 最终由后端来实现这些规范, 为前端提供符合规范的接口 |

```
 [前端]
--------
   ^
   |
   |
前后端接口
   |
   |
--------
 [后端]
```

## 前后端接口协作流程

在开发之前一定要先定义好接口规范, 至于[接口应该由前端来定还是后端来定](https://github.com/ufologist/puer-mock/blob/master/FAQ.md#接口由前端定还是后端定), 这个还得看公司的具体情况, 但一定要让前后端都确认无误, 特别是[接口协商要点](#接口协商要点).

## 接口协商要点
* 接口返回数据即显示：前端仅做渲染逻辑处理
* 渲染逻辑禁止跨多个接口调用
* 前端关注交互、渲染逻辑，尽量避免业务逻辑处理的出现
* 接口必须返回统一的数据结构, 参考[后端接口通用规范中接口返回的数据结构](#接口返回的数据结构)
* 接口查询不到数据时, 即空数据的情况下返回给前端怎样的数据
  * 建议返回非 `null` 的对应数据类型初始值, 例如对象类型的返回空对象(`{}`), 数组类型的返回空数组(`[]`), 其他原始数据类型(`string`/`number`/`boolean`...)也使用对应的默认值
  * 这样可以减少前端很多琐碎的非空判断, 直接使用接口中的数据
  * 例如: `result.fieldName`
  * 如果 `result` 为 `null`, 可想而知会报错 `Uncaught TypeError: Cannot read property 'fieldName' of null`
* 接口需要登录时如何处理, 特别是同时涉及到 Web 端/微信端/App 端, 需要前端针对运行环境判断如何跳转到登录页面？
* 返回数据中图片 URL 是完整的
  * `http://a.res.com/path/to/img.png` 这就是完整的, 前端直接使用这个 URL
* 返回数据中页面跳转的 URL 是给完整的还是部分的
  * 内部页面、外部页面皆返回完整的, 例如广告位要跳转去谷歌
* 返回数据中日期的格式, 推荐格式化好的字符串
  * 对于纯展示用的日期值, 推荐返回字符串, 例如: `2017-1-1`

## 后端接口通用规范

### 接口地址

### 接口版本

1 Api URL 显示明确 （推荐）
 `http://api.yourdomain.com/v1` 或者 `http://yourdomain.com/api/v1`

2 通过Accept Header 明确版本和返回类型

Accept: application/vnd.github.v3+json

Accept: application/vnd.github.v3+res

### 接口请求方式

接口地址即接口的 URL, 定义时使用相对路径(即不用带上域名信息), 建议分模块来定义, 推荐 REST 风格, 例如
* `GET /user/:id` 表示获取用户信息
* `POST /user` 表示新增用户

### 使用统一的资源路径格式
#### 资源名（Resource names）

使用复数形式为资源命名，除非这个资源在系统中是单例的 (例如，在大多数系统中，给定的用户帐户只有一个)。 这种方式保持了特定资源的统一性。

#### 行为（Actions）

好的末尾不需要为资源指定特殊的行为，但在特殊情况下，为某些资源指定行为却是必要的。为了描述清楚，在行为前加上一个标准的actions：

/resources/:resource/actions/:action

例如：

/runs/{run_id}/actions/stop

#### 路径和属性要小写

为了和域名命名规则保持一致，使用小写字母并用-分割路径名字，例如：

service-api.com/users

service-api.com/app-setups

属性也使用小写字母，但是属性名要用下划线_分割，以便在Javascript中省略引号。 例如：

service_class: "first"

#### 支持方便的无id间接引用

在某些情况下，让用户提供ID去定位资源是不方便的。例如，一个用户想取得他在Heroku平台app信息，但是这个app的唯一标识是UUID。这种情况下，你应该支持接口通过名字和ID都能访问，例如:
```
$ curl https://service.com/apps/{app_id_or_name}
$ curl https://service.com/apps/97addcf0-c182
$ curl https://service.com/apps/www-prod
```

#### 不要只接受使用名字而放弃了使用id。

#### 最小化路径嵌套

在一些有父路径/子路径嵌套关系的资源数据模块中，路径可能有非常深的嵌套关系，例如:

/orgs/{org_id}/apps/{app_id}/dynos/{dyno_id}

推荐在根(root)路径下指定资源来限制路径的嵌套深度。使用嵌套指定范围的资源。在上述例子中，dyno属于app，app属于org可以表示为：

/orgs/{org_id}

/orgs/{org_id}/apps

/apps/{app_id}

/apps/{app_id}/dynos

/dynos/{dyno_id}

### 提供资源的(UU)ID
在默认情况给每一个资源一个id属性。除非有更好的理由，否则请使用UUID。不要使用那种在服务器上或是资源中不是全局唯一的标识，尤其是自动增长的id。

生成小写的UUID格式 8-4-4-4-12，例如：

"id": "01234567-89ab-cdef-0123-456789abcdef"

### 时间戳
使用UTC（世界标准时间）时间，用ISO8601进行格式化

```
All timestamps return in ISO 8601 format:

YYYY-MM-DDTHH:MM:SSZ

{
  // ...
  "created_at": "2012-01-01T12:00:00Z",
  "updated_at": "2012-01-01T13:00:00Z",
  // ...
}
```

有些资源不需要使用时间戳那么就忽略这两个字段。


### 嵌套外键关系
使用嵌套对象序列化外键关联，例如:
```
{
  "name": "service-production",
  "owner": {
    "id": "5d8201b0..."
  },
  // ...
}
```
而不是像这样:
```
{
  "name": "service-production",
  "owner_id": "5d8201b0...",
  ...
}
```

### 保证响应JSON最小化
请求中多余的空格会增加响应大小，而且现在很多的HTTP客户端都会自己输出可读格式（"prettify"）的JSON。所以最好保证响应JSON最小化，例如：
```
{"beta":false,"email":"alice@heroku.com","id":"01234567-89ab-cdef-0123-456789abcdef","last_login":"2012-01-01T12:00:00Z","created_at":"2012-01-01T12:00:00Z","updated_at":"2012-01-01T12:00:00Z"}
```
而不是这样：
```
{
  "beta": false,
  "email": "alice@heroku.com",
  "id": "01234567-89ab-cdef-0123-456789abcdef",
  "last_login": "2012-01-01T12:00:00Z",
  "created_at": "2012-01-01T12:00:00Z",
  "updated_at": "2012-01-01T12:00:00Z"
}
```
你可以提供可选的方式为客户端提供更详细可读的响应，使用查询参数（例如：?pretty=true）或者通过Accept头信息参数（例如：Accept: application/vnd.heroku+json; version=3; indent=4;


### 接口参数
#### GET
[向接口传递参数时](https://developer.github.com/v3/#parameters), 如果是少量参数可以作为 URL query string 追加到接口的 URL 中

#### POST DELETE 等

推荐在 HTTP 请求体(`body`)中包含一个 JSON 字符串作为接口的参数, 并设置 `Content-Type: application/json; charset=utf-8`.

或者作为 `Content-Type: application/x-www-form-urlencoded` 放在请求体(`body`)中(即表单提交的方式)

例如

变更 VIP 用户的接口

```
POST /users HTTP/1.1
Content-Type: application/json; charset=utf-8

{
    "name": "hanmeimei",
    "isVip": true
}
```
```
{
  "message": "Requires authentication",
  "documentation_url": "https://docs.github.com/rest/reference/users#get-the-authenticated-user"
}
```

### HTTP verbs
Where possible, API v3 strives to use appropriate HTTP verbs for each action.

| Verb	| Description | Code
| :-- | :--| :--|
| HEAD	| Can be issued against any resource to get just the HTTP header info.|
| GET| 	Used for retrieving resources.| 200
| POST| 	Used for creating resources.|201
| PATCH	| Used for updating resources with partial JSON data. For instance, an Issue resource has title and body attributes. A PATCH  request may accept one or more of the attributes to update the resource. PATCH is a relatively new and uncommon HTTP verb, so resource endpoints also accept POST requests. | 200
| PUT	| Used for replacing resources or collections. For PUT requests with no body attribute, be sure to set the Content-Length header to zero.| 200
| DELETE| 	Used for deleting resources.| 204

### 重定向

    重定向
    301 Permanent redirection. The URI you used to make the request has been superseded by the one specified in the Location header field. This and all future requests to this resource should be directed to the new URI.
    302 307  Temporary redirection. The request should be repeated verbatim to the URI specified in the Location header field but clients should continue to use the original URI for future requests.

### 接口返回的数据结构

返回的响应体类型推荐为 `Content-Type: application/json; charset=utf-8`

返回的数据包含在 HTTP 响应体中, 是一个 JSON Object.

该 Object 可能包含 4 个字段 `data`, `code`, `err`, `message`

```
curl -i https://api.github.com/user
HTTP/1.1 401 Unauthorized
date: Tue, 17 Nov 2020 01:49:06 GMT
content-type: application/json; charset=utf-8
content-length: 141
server: GitHub.com
status: 401 Unauthorized
x-github-media-type: github.v3; format=json
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, Deprecation, Sunset
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
vary: Accept-Encoding, Accept, X-Requested-With
X-Ratelimit-Limit: 60
X-Ratelimit-Remaining: 59
X-Ratelimit-Reset: 1605581346
X-Ratelimit-Used: 1
X-GitHub-Request-Id: C98F:4DE5:CA38EB:F786CC:5FB32C12

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
    "message": "给用户的提示信息",
    "data": {
        "entity": {
            id: 1,
            name: "XXX",
            code: "XXX"
        }
    },
    "code": 0,
    "err": "stackxxxxxxxxxxxxxxxxxx"
}
```

**字段名** |**字段说明**
:----------|:-----------
message |  `message` 字段作为接口处理失败时, **给予用户的友好的提示信息**, 即所有给用户的提示信息都统一由后端来处理.
data       | **业务数据**<br>必须是任意 JSON 数据类型(number/string/boolean/object/array).<br>推荐始终返回一个 object (即再包一层)以便于扩展字段.<br>例如: 用户数据应该返回 `{"user":{"name":"test"}}`, 而不是直接为 `{"name":"test"}`
code     | **状态码**<br>必须是 `>= 0` 的 JSON Number 整数.<ul><li>`0` 表示请求处理成功, 此时可以省略 `code` 字段, 省略时和为 `0` 时表示同一含义.</li><li>`非 0` 表示发生错误时的[错误码](http://open.weibo.com/wiki/Error_code "错误码格式可以参考微博API的 Error code"), 此时可以省略 `data` 字段, 并视情况输出 `message` 字段作为补充信息</li></ul>
err | </li><li>`err` 字段用来放置接口处理失败时的详细错误信息. 只是为了方便排查错误, 前端无需使用.</li></ul>

例如
* 接口处理成功时接口返回的数据

  ```
  {
      "data": "api result"
      "code": 0
  }
  ```
* 接口处理失败时接口返回的数据

  ```
  {
      "code": 1,
      "message": "服务器正忙",
      "err": "server down because many threading"
      "data": []
  }
  ```

这样我们就可以非常容易地通过判断 code 来处理数据了
```javascript
if (!response.code) {
    // code 为 0
    console.log(response.data);
} else {
    // 失败
    console.error(response.code, response.err);
    // 统一由服务端返回给用户的提示信息
    alert(response.message);
}
```

### Status Code

例如
* 用户发现错误, 可以截错误码的图, 就能够提供有效的信息帮助开发人员排查错误
* 测试人员发现错误, 可以通过错误码, 快速定位是前端的问题还是后端接口的问题

因此我们确定提示信息规范为: 当后端接口调用出错时, 接口提供一个用户可以理解的错误提示, 前端展示给用户错误提示和错误码, 给予用户反馈

对于错误码的规范, 参考行业实践, 大致有两种方案

* 做显性的类型区分, 快速定位错误的类别, 例如通过字母划分类型: `A101`, `B131`
  * [Standard ISO Response Codes](http://www.nexion.co.za/docs/merchant-access/user-manual/17.%20Standard%20ISO%20Response%20codes.pdf)
* 固定位数, 设定区间(例如手机号码, 身份证号码)来划分不同的错误类型
   * [HTTP  Status Code](https://www.django-rest-framework.org/api-guide/status-codes/)
  * [HTTP Status Code Definitions](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html "Most API services follow the HTTP error code system RFC2616 with ranges of error codes for different types of error")
  * [System Error Codes](https://docs.microsoft.com/en-us/windows/desktop/Debug/system-error-codes)

具体实践如下
* **错误码固定长度**, 以区间来划分错误类型(例如 HTTP 的状态码)

  例如: 10404 表示 HTTP 请求 404 错误, 20000 表示 API 调用失败, 30000 代表业务错误, 31000 表示业务A错误, 32000 表示业务B错误
* **错误码可不固定长度**, 以首字母来划分错误类型, 可扩展性更好, 但实际运作还是需要划分区间

  例如: H404 表示 HTTP 请求 404 错误, A100 表示 API 调用失败, B100 表示业务A错误, B200 表示业务B错误

关于错误分类的原则, 我们可以根据发送请求的最终状态来划分
- 发送失败(即请求根本就没有发送出去)
- 发送成功
  - HTTP 异常状态(例如 404/500...)
  - HTTP 正常状态(例如 200)
    - 接口调用成功
    - 接口调用失败(业务错误, 即接口规范中 status 非 0 的情况)

### 认证
* Basic authentication
```
$ curl -u "username" https://api.github.com
```
* OAuth2 token (sent in a header)
```
$ curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com
```

### 权限
Method 是否开放Delete方法给用户
Resource 用户是否具有某类资源的增删改权限
Object 用户只允许变更资源下归属自己管理的对象


### Rate Limiting 限额
* 对于登录的个人用户可以限定5000/h
* 对于登录的服务用户可以限定15000/h
* 匿名用户 限定 60/h 限定需要通过判断ip原地址
* 获取接口rate值
    GET /rate_limit
```
{
  "resources": {
    "core": {
      "limit": 5000,
      "remaining": 4999,
      "reset": 1372700873
    },
    "search": {
      "limit": 30,
      "remaining": 18,
      "reset": 1372697452
    },
    "graphql": {
      "limit": 5000,
      "remaining": 4993,
      "reset": 1372700389
    }
}
```

* 接口返回值需要返回限流的当前状态和信息
```
$ curl -i https://api.github.com/users/octocat
> HTTP/1.1 200 OK
> Date: Mon, 01 Jul 2013 17:27:06 GMT
> Status: 200 OK
> X-RateLimit-Limit: 60
> X-RateLimit-Remaining: 56
> X-RateLimit-Reset: 1372700873
```


| Verb	| Description
| :-- | :--|
| X-RateLimit-Limit	| The maximum number of requests you're permitted to make per hour.
| X-RateLimit-Remaining	| The number of requests remaining in the current rate limit window.
| X-RateLimit-Reset|	The time at which the current rate limit window resets in [UTC epoch seconds](https://en.wikipedia.org/wiki/Unix_time).

If you exceed the rate limit, an error response returns:

> HTTP/1.1 403 Forbidden
> Date: Tue, 20 Aug 2013 14:50:41 GMT
> Status: 403 Forbidden
> X-RateLimit-Limit: 60
> X-RateLimit-Remaining: 0
> X-RateLimit-Reset: 1377013266

> {
>    "message": "API rate limit exceeded for xxx.xxx.xxx.xxx. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.)",
>    "documentation_url": "https://developer.github.com/v3/#rate-limiting"
> }

### 支持CORS Cross origin resource sharing

Here's a sample request sent from a browser hitting http://example.com:
```
$ curl -i https://api.github.com -H "Origin: http://example.com"
HTTP/1.1 302 Found
Access-Control-Allow-Origin: *
Access-Control-Expose-Headers: ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval
```


### 分页 Pagnination
```
curl 'https://api.github.com/user/repos?page=2&page_size=100'
```

| Verb	| Description | Demo
| :-- | :--| :--|
| 如何限制只返回 N 条数据	| limit 参数.| ?limit=20
| 如何控制每页的数据条数| 	page_size| ?page_size=30
| 如何加载某一页的数据| 	page | ?page=2
| 第一页是从 0 开始还是从 1 开始	| 1| 默认page=1, 缺省值
| 分页信息包含什么| 	total, page, page_size| {"total_count": 200, "total_page": 30, "page": 2, "page_size": 30, "results": []}
| 分页信息何时表明已经是最后一页了 | 请求某页数据时返回的数据条数 < pageSize <br>    请求某页数据时返回的数据条数 = 0<br> 后端聚合返回， 前端获取links信息 |   {   <br>  "self": "http://example.com/articles", <br>    "first": "http://example.com/articles?page=1"   <br>  "last": "http://example.com/articles?page=10"<br>     "prev": ""<br>     "next": "http://example.com/articles?page=2",<br>  }


### 过滤、排序
/tickets?search=xxx 模糊查询

/tickets?field1=testxx key value 精确查询

/tickets?field1=testxx key value 精确查询field1是testxx的数据  判等

/tickets?field1=testxx,equal key value 同上

/tickets?field1=testxx,like key value 模糊查询field1里包含testxx的数据 包含

/tickets?name=dong&state=open&sort=-priority,created_at 排序



### 限制返回的字段
/tickets?fields=id,subject,updated_at

### 缓存
#### 后端缓存
GET Api 支持缓存/清除缓存

#### 前端HTTP缓存

HTTP 头中，有多个字段可以用于缓存处理。比较常用的有缓存控制和条件请求。

* 缓存控制：

缓存控制通常是需要客户端，缓存服务器 / 代理服务器与业务服务器一起发生作用。


HTTP 头中有“Cache-control”字段来控制如何使用缓存，常见的取值有 private、no-cache、max-age、must-revalidate 等。比如当你给返回的数据内容设置 max-age=600，那么当用户隔了 30 秒再次请求的时候，就不会导致重新请求后台数据。

另外，也可以通过“Expires”字段来指定内容过期时间，在此时间前的请求都不会导致后台程序重新请求数据。

 * 条件请求与电子标签：

很多时候，数据内容可能会几个小时甚至几天都不会发生变动，这个时候根据请求时间间隔来控制缓存，就不能满足系统的需求了。通过支持条件请求与电子标签，可以帮助我们来解决这个问题。

当用户请求数据内容时，系统在返回数据的同时，在 HTTP 头中，将返回根据服务器内容的最后修改时间 Last-Modified，或者根据服务器内容生成电子标签 ETag。 当用户再次请求数据时，就可以在 HTTP 请求中使用 If-Modified-Since 或者 If-None-Match 头信息，把上次请求得到的时间戳或者电子标签传给服务器。当收到一个有条件请求的 HTTP 头的 REST 请求的时候，我们的程序需要将收到的时间戳或者电子标签与当前内容作比较，就可以很容易的知道用户请求的数据内容在这段时间是否发生过修改，并根据比较结果返回给用户最新内容，或者用 HTTP 响应码 304 告知用户，内容没有变化。

### 并发处理

使用 HTTP 头进行并发处理
上文我们提到了使用条件请求控制缓存，其实我们还可以使用条件请求进行并发处理。

比如当用户 Alice 和 Bob 通过 REST 获取了一篇文档。Bob 阅读文档之后，通过 PUT 来修改文档；而此前几分钟，Alice 刚刚修改了这篇文档，于是 Bob 就在毫不知情的情况下不慎覆盖了 Alice 的修改。

通过在写操作中支持条件请求，我们可以更好的处理并发修改。用户在发出修改请求的同时，在 HTTP 请求中使用 If-Not-Modified-Since 或者 If-Match 头信息，把获取数据时得到的时间戳或者电子标签传给服务器；我们的程序通过与服务器当前内容的比较，就可以知道，这个修改请求是否是针对当前内容提出的。当服务器发现内容已经被其他用户修改过了，就不会执行修改请求，并返回 HTTP 响应码 412（未满足前提条件）给用户。

### 最终规范

错误码可不固定长度, 整体格式为: `字母+数字`, `字母`作为错误类型, 可扩展性更好, `数字`建议划分区间来细分错误

例如:
- `A` for **API**: API 调用失败(请求发送失败)的错误, 例如 `A100` 表示 URL 非法
- `H` for **HTTP**, HTTP 异常状态的错误, 例如 `H404` 表示 HTTP 请求404错误
- `B` for **backend or business**, 接口调用失败的错误, 例如 `B100` 业务A错误, `B200` 业务B错误
- `C` for **Client**: 客户端错误, 例如 `C100` 表示解析 JSON 失败

```
                                                       发送 HTTP 请求
                                                 ┌───────────┴───────────┐
                                              发送成功¹               发送失败²
                                                 │                       │
                                      ┌──────────┴──────────┐            A 例如: A100
                                获得 HTTP 响应       无法获得 HTTP 响应³
                                      │                     │
                                 HTTP code                A 例如: A200
                           ┌──────────┴──────────┐
                       HTTP 成功(200-300)     HTTP 异常
                           │                     |
               {data, code, message, err}        H${HTTP status} 例如: H404
               ┌───────────┴───────────┐
          接口调用成功(code:0)   接口调用失败
      ┌────────┴────────┐              |
客户端处理出错      客户端处理正常       B${code}${message} 例如: B100
      |
      C 例如: C100

- 发送成功¹: 服务端收到了 HTTP 请求并返回了 HTTP 响应
- 发送失败²: HTTP 请求没有发送出去(例如由于跨域被浏览器拦截不允许发送), 未到达服务端(即服务端没有收到这个 HTTP 请求)
- 无法获得 HTTP 响应³: 服务端收到了请求并返回了响应, 但客户端由于某些原因无法获得 HTTP 响应, 例如请求的超时处理机制
```


### 参考

* [GitHub Api](https://docs.github.com/en/free-pro-team@latest/rest)
* [API-DESIGN](https://github.com/interagent/http-api-design)
* [API](https://github.com/f2e-journey/treasure/blob/master/api.md)
* [Google JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml)
* [最佳实践：更好的设计你的 REST API](http://www.ibm.com/developerworks/cn/web/1103_chenyan_restapi)
* [RESTful API 设计指南](http://www.ruanyifeng.com/blog/2014/05/restful_api.html)
* [Best Practices for Designing a Pragmatic RESTful API](http://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)
* [HTTP API Design Guide](https://github.com/interagent/http-api-design "HTTP+JSON API design practices")
* [The RESTful Cookbook](https://github.com/sofish/restcookbook)
* [RESTful API 编写指南](http://blog.igevin.info/posts/restful-api-get-started-to-write/)
