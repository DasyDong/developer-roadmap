# spider

* [爬虫](spider.md#爬虫)   
  * [1.爬取数据后使用哪个数据库存储数据的，为什么？](spider.md#1爬取数据后使用哪个数据库存储数据的为什么)   
  * [2.你用过的爬虫框架或者模块有哪些？优缺点？](spider.md#2你用过的爬虫框架或者模块有哪些优缺点)   
  * [3.写爬虫是用多进程好？还是多线程好？](spider.md#3写爬虫是用多进程好还是多线程好)   
  * [4.常见的反爬虫和应对方法？](spider.md#4常见的反爬虫和应对方法)   
  * [5.需要登录的网页，如何解决同时限制ip，cookie,session](spider.md#5需要登录的网页如何解决同时限制ipcookiesession)   
  * [6.验证码的解决?](spider.md#6验证码的解决)   
  * [7.“极验”滑动验证码如何破解？](spider.md#7“极验”滑动验证码如何破解)   
  * [8.爬虫多久爬一次，爬下来的数据是怎么存储？](spider.md#8爬虫多久爬一次爬下来的数据是怎么存储)   
  * [9.cookie过期的处理问题？](spider.md#9cookie过期的处理问题)   
  * [10.动态加载又对及时性要求很高怎么处理？](spider.md#10动态加载又对及时性要求很高怎么处理)   
  * [11.HTTPS有什么优点和缺点？](spider.md#11https有什么优点和缺点)   
  * [12.HTTPS是如何实现安全传输数据的？](spider.md#12https是如何实现安全传输数据的)   
  * [13.谈一谈你对Selenium和PhantomJS了解](spider.md#13谈一谈你对selenium和phantomjs了解)   
  * [14.平常怎么使用代理的 ？](spider.md#14平常怎么使用代理的-)   
  * [15.怎么监控爬虫的状态?](spider.md#15怎么监控爬虫的状态)   
  * [16.描述下scrapy框架运行的机制？](spider.md#16描述下scrapy框架运行的机制)   
  * [17.谈谈你对Scrapy的理解？](spider.md#17谈谈你对scrapy的理解)   
  * [18.怎么样让 scrapy 框架发送一个 post 请求（具体写出来）](spider.md#18怎么样让-scrapy-框架发送一个-post-请求具体写出来)   
  * [19.怎么判断网站是否更新？](spider.md#19怎么判断网站是否更新)   
  * [20.图片、视频爬取怎么绕过防盗连接](spider.md#20图片、视频爬取怎么绕过防盗连接)   
  * [21.你爬出来的数据量大概有多大？大概多长时间爬一次？](spider.md#21你爬出来的数据量大概有多大大概多长时间爬一次)   
  * [22.用什么数据库存爬下来的数据？部署是你做的吗？怎么部署？](spider.md#22用什么数据库存爬下来的数据部署是你做的吗怎么部署)   
  * [23.增量爬取](spider.md#23增量爬取)   
  * [24.爬取下来的数据如何去重，说一下scrapy的具体的算法依据。](spider.md#24爬取下来的数据如何去重说一下scrapy的具体的算法依据)   
  * [25.Scrapy的优缺点?](spider.md#25scrapy的优缺点)   
  * [26.怎么设置爬取深度？](spider.md#26怎么设置爬取深度)   
  * [27.scrapy和scrapy-redis有什么区别？为什么选择redis数据库？](spider.md#27scrapy和scrapy-redis有什么区别为什么选择redis数据库)   
  * [28.分布式爬虫主要解决什么问题？](spider.md#28分布式爬虫主要解决什么问题)   
  * [29.什么是分布式存储？](spider.md#29什么是分布式存储)   
  * [30.你所知道的分布式爬虫方案有哪些？](spider.md#30你所知道的分布式爬虫方案有哪些)   
  * [31.scrapy-redis，有做过其他的分布式爬虫吗？](spider.md#31scrapy-redis有做过其他的分布式爬虫吗)   

    **爬虫**

    **1.爬取数据后使用哪个数据库存储数据的，为什么？**

    MySQL
* 数据同步插入数据库

在pipelines.py中引入数据库连接模块：

**init**是对数据进行初始化，定义连接信息如host，数据库用户名、密码、数据库名称、数据库编码, 在process\_item中进行插入数据操作，格式都是固定的

```python
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'jobbole', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = 'INSERT INTO jobbole_article (`title`, `create_date`, `url`, `url_object_id`, `content`, `front_image_path`, `comment_nums`, `fav_nums`, `praise_nums`, `tags`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['url_object_id'], item['content'], item["front_image_path"], item['comment_nums'], item['fav_nums'], item['praise_nums'], item['tags']))
        self.conn.commit()
```

最后在settings.py中把MysqlPipelint\(\)加入到系统中，需要注意的是优先级要小于之前加入处理图片路径的优先级

\(先进行ArticleimagePipeline的处理，再进行MysqlPipeline处理\)

```python
ITEM_PIPELINES = {
   'articlespider.pipelines.ArticlespiderPipeline': 300, #系统自动生成pipeline，未用
   'articlespider.pipelines.ArticleimagePipeline': 1,
   'articlespider.pipelines.MysqlPipeline': 4,
}
```

1. 异步插入数据库 异步操作需要引入twisted：

   ```python
   from twisted.enterprise import adbapi
   import MySQLdb
   import MySQLdb.cursors
   ```

   \`\`\`python class MysqlPipeline\(object\): def **init**\(self, dbpool\): self.dbpool = dbpool

   @classmethod def from\_settings\(cls, settings\): dbparms = dict\( host = settings\["MYSQL\_HOST"\], db = settings\["MYSQL\_DBNAME"\], user = settings\["MYSQL\_USER"\], passwd = settings\["MYSQL\_PASSWORD"\], charset='utf8', cursorclass=MySQLdb.cursors.DictCursor, use\_unicode=True, \) dbpool = adbapi.ConnectionPool\("MySQLdb", \*\*dbparms\)

   ```text
    return cls(dbpool)
   ```

   def process\_item\(self, item, spider\):

   **使用twisted将mysql插入变成异步执行**

   ```text
    query = self.dbpool.runInteraction(self.do_insert, item)
    query.addErrback(self.handle_error)
   ```

   def handle\_error\(self, failure\): print\(failure\)

   def do\_insert\(self, cursor, item\):

   **具体执行插入**

   ```text
    insert_sql = 'INSERT INTO jobbole_article (`title`, `create_date`, `url`, `url_object_id`, `content`, `front_image_path`, `comment_nums`, `fav_nums`, `praise_nums`, `tags`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(insert_sql, (item['title'], item['create_date'], item['url'], item['url_object_id'], item['content'], item["front_image_path"], item['comment_nums'], item['fav_nums'], item['praise_nums'], item['tags']))
   ```

\`\`\`

### 2.你用过的爬虫框架或者模块有哪些？优缺点？

1.Scrapy

Scrapy是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。。用这个框架可以轻松爬下来如亚马逊商品信息之类的数据。

2.Beautiful Soup

Beautiful Soup 是一个可以从HTML或XML文件中提取数据的Python库.它能够通过你喜欢的转换器实现惯用的文档导航,查找,修改文档的方式.Beautiful Soup会帮你节省数小时甚至数天的工作时间。

### 3.写爬虫是用多进程好？还是多线程好？

### 4.常见的反爬虫和应对方法？

从功能上来讲，爬虫一般分为数据采集，处理，储存三个部分。这里我们只讨论数据采集部分。

一般网站从三个方面反爬虫：用户请求的Headers，用户行为，网站目录和数据加载方式。前两种比较容易遇到，大多数网站都从这些角度来反爬虫。第三种一些应用ajax的网站会采用，这样增大了爬取的难度。

0x02 通过Headers反爬虫

从用户请求的Headers反爬虫是最常见的反爬虫策略。很多网站都会对Headers的User-Agent进行检测，还有一部分网站会对Referer进行检测（一些资源网站的防盗链就是检测Referer）。如果遇到了这类反爬虫机制，可以直接在爬虫中添加Headers，将浏览器的User-Agent复制到爬虫的Headers中；或者将Referer值修改为目标网站域名。对于检测Headers的反爬虫，在爬虫中修改或者添加Headers就能很好的绕过。

0x03 基于用户行为反爬虫

还有一部分网站是通过检测用户行为，例如同一IP短时间内多次访问同一页面，或者同一账户短时间内多次进行相同操作。

大多数网站都是前一种情况，对于这种情况，使用IP代理就可以解决。可以专门写一个爬虫，爬取网上公开的代理ip，检测后全部保存起来。这样的代理ip爬虫经常会用到，最好自己准备一个。有了大量代理ip后可以每请求几次更换一个ip，这在requests或者urllib2中很容易做到，这样就能很容易的绕过第一种反爬虫。

对于第二种情况，可以在每次请求后随机间隔几秒再进行下一次请求。有些有逻辑漏洞的网站，可以通过请求几次，退出登录，重新登录，继续请求来绕过同一账号短时间内不能多次进行相同请求的限制。

0x04 动态页面的反爬虫

上述的几种情况大多都是出现在静态页面，还有一部分网站，我们需要爬取的数据是通过ajax请求得到，或者通过JavaScript生成的。首先用Firebug或者HttpFox对网络请求进行分析。如果能够找到ajax请求，也能分析出具体的参数和响应的具体含义，我们就能采用上面的方法，直接利用requests或者urllib2模拟ajax请求，对响应的json进行分析得到需要的数据。

能够直接模拟ajax请求获取数据固然是极好的，但是有些网站把ajax请求的所有参数全部加密了。我们根本没办法构造自己所需要的数据的请求。我这几天爬的那个网站就是这样，除了加密ajax参数，它还把一些基本的功能都封装了，全部都是在调用自己的接口，而接口参数都是加密的。遇到这样的网站，我们就不能用上面的方法了，我用的是selenium+phantomJS框架，调用浏览器内核，并利用phantomJS执行js来模拟人为操作以及触发页面中的js脚本。从填写表单到点击按钮再到滚动页面，全部都可以模拟，不考虑具体的请求和响应过程，只是完完整整的把人浏览页面获取数据的过程模拟一遍。

用这套框架几乎能绕过大多数的反爬虫，因为它不是在伪装成浏览器来获取数据（上述的通过添加 Headers一定程度上就是为了伪装成浏览器），它本身就是浏览器，phantomJS就是一个没有界面的浏览器，只是操控这个浏览器的不是人。利用 selenium+phantomJS能干很多事情，例如识别点触式（12306）或者滑动式的验证码，对页面表单进行暴力破解等等。它在自动化渗透中还 会大展身手，以后还会提到这个。

### 5.需要登录的网页，如何解决同时限制ip，cookie,session

### 6.验证码的解决?

1.输入式验证码 解决思路：这种是最简单的一种，只要识别出里面的内容，然后填入到输入框中即可。这种识别技术叫OCR，这里我们推荐使用Python的第三方库，tesserocr。对于没有什么背影影响的验证码如图2，直接通过这个库来识别就可以。但是对于有嘈杂的背景的验证码这种，直接识别识别率会很低，遇到这种我们就得需要先处理一下图片，先对图片进行灰度化，然后再进行二值化，再去识别，这样识别率会大大提高。

验证码识别大概步骤

* 转化成灰度图
* 去背景噪声
* 图片分割

2.滑动式验证码 解决思路：对于这种验证码就比较复杂一点，但也是有相应的办法。我们直接想到的就是模拟人去拖动验证码的行为，点击按钮，然后看到了缺口 的位置，最后把拼图拖到缺口位置处完成验证。

第一步：点击按钮。然后我们发现，在你没有点击按钮的时候那个缺口和拼图是没有出现的，点击后才出现，这为我们找到缺口的位置提供了灵感。

第二步：拖到缺口位置。我们知道拼图应该拖到缺口处，但是这个距离如果用数值来表示？通过我们第一步观察到的现象，我们可以找到缺口的位置。这里我们可以比较两张图的像素，设置一个基准值，如果某个位置的差值超过了基准值，那我们就找到了这两张图片不一样的位置，当然我们是从那块拼图的右侧开始并且从左到右，找到第一个不一样的位置时就结束，这是的位置应该是缺口的left，所以我们使用selenium拖到这个位置即可。这里还有个疑问就是如何能自动的保存这两张图？这里我们可以先找到这个标签，然后获取它的location和size，然后 top，bottom，left，right = location\['y'\] ,location\['y'\]+size\['height'\]+ location\['x'\] + size\['width'\] ,然后截图，最后抠图填入这四个位置就行。具体的使用可以查看selenium文档，点击按钮前抠张图，点击后再抠张图。最后拖动的时候要需要模拟人的行为，先加速然后减速。因为这种验证码有行为特征检测，人是不可能做到一直匀速的，否则它就判定为是机器在拖动，这样就无法通过验证了。

3.点击式的图文验证 和 图标选择 图文验证：通过文字提醒用户点击图中相同字的位置进行验证。

图标选择： 给出一组图片，按要求点击其中一张或者多张。借用万物识别的难度阻挡机器。

这两种原理相似，只不过是一个是给出文字，点击图片中的文字，一个是给出图片，点出内容相同的图片。

这两种没有特别好的方法，只能借助第三方识别接口来识别出相同的内容，推荐一个超级鹰，把验证码发过去，会返回相应的点击坐标。

然后再使用selenium模拟点击即可。具体怎么获取图片和上面方法一样。

### 7.“极验”滑动验证码如何破解？

### 8.爬虫多久爬一次，爬下来的数据是怎么存储？

### 9.cookie过期的处理问题？

### 10.动态加载又对及时性要求很高怎么处理？

### 11.HTTPS有什么优点和缺点？

### 12.HTTPS是如何实现安全传输数据的？

### 13.谈一谈你对Selenium和PhantomJS了解

### 14.平常怎么使用代理的 ？

proxies = {'http':'[http://10.10.10.10:8765','https':'https://10.10.10.10:8765'}](http://10.10.10.10:8765','https':'https://10.10.10.10:8765'})

resp = requests.get\(url,proxies = proxies\)

注：免费的代理IP可以在这个网站上获取：[http://www.xicidaili.com/nn/](http://www.xicidaili.com/nn/)

### 15.怎么监控爬虫的状态?

### 16.描述下scrapy框架运行的机制？

### 17.谈谈你对Scrapy的理解？

### 18.怎么样让 scrapy 框架发送一个 post 请求（具体写出来）

### 19.怎么判断网站是否更新？

1、304页面http状态码

当第二次请求页面访问的时候，该页面如果未更新，则会反馈一个304代码，而搜索引擎也会利用这个304http状态码来进行判断页面是否更新。

首先第一次肯定是要爬取网页的，假设是A.html，这个网页存储在磁盘上，相应地有个修改时间（也即是更新这个文件的时间）。

那么第二次爬取的时候，如果发现这个网页本地已经有了，例如A.html，这个时候，你只需要向服务器发送一个If-Modified-Since的请求，把A.html的修改时间带上去。

如果这段时间内，A.html更新了，也就是A.html过期了，服务器就会HTTP状态码200，并且把新的文件发送过来，这时候只要更新A.html即可。

如果这段时间内，A.html的内容没有变，服务器就会返返回HTTP状态码304（不返回文件内容），这个时候就不需要更新文件。

2、Last-Modified文件最后修改时间

这是http头部信息中的一个属性，主要是记录页面最后一次的修改时间，往往我们会发现，一些权重很高的网站，及时页面内容不更新，但是快照却还是能够每日更新，这其中就有Last-Modified的作用。通产情况下，下载网页我们使用HTTP协议，向服务器发送HEAD请求，可以得到页面的最后修改时间LastModifed,或者标签ETag。将这两个变量和上次下载记录的值的比较就可以知道一个网页是否跟新。这个策略对于静态网页是有效的。是对于绝大多数动态网页如ASP，JSP来说，LastModifed就是服务器发送Response的时间，并非网页的最后跟新时间，而Etag通常为空值。所以对于动态网页使用LastModifed和Etag来判断是不合适的，因此Last-Modified只是蜘蛛判断页面是否更新的一个参考值，而不是条件。

### 20.图片、视频爬取怎么绕过防盗连接

### 21.你爬出来的数据量大概有多大？大概多长时间爬一次？

### 22.用什么数据库存爬下来的数据？部署是你做的吗？怎么部署？

### 23.增量爬取

### 24.爬取下来的数据如何去重，说一下scrapy的具体的算法依据。

### 25.Scrapy的优缺点?

### 26.怎么设置爬取深度？

### 27.scrapy和scrapy-redis有什么区别？为什么选择redis数据库？

### 28.分布式爬虫主要解决什么问题？

### 29.什么是分布式存储？

### 30.你所知道的分布式爬虫方案有哪些？

### 31.scrapy-redis，有做过其他的分布式爬虫吗？

