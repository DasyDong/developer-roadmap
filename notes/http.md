# HTTP 基础

* [HTTP基础-外链](https://github.com/CyC2018/CS-Notes/blob/master/notes/HTTP.md)

# HTTP 进阶

## 概念
![知识地图](../pics/http/http_sum.png)

HTTP协议始于三十年前蒂姆·伯纳斯-李的一篇论文；
* HTTP/0.9是个简单的文本协议，只能获取文本资源；
* HTTP/1.0确立了大部分现在使用的技术，但它不是正式标准；
* HTTP/1.1是目前互联网上使用最广泛的协议，功能也非常完善；
* HTTP/2基于Google的SPDY协议，注重性能改善，但还未普及；
* HTTP/3基于Google的QUIC协议，是将来的发展方向。

互联网上绝大部分资源都使用HTTP协议传输；
浏览器是HTTP协议里的请求方，即User Agent；
服务器是HTTP协议里的应答方，常用的有Apache和Nginx；
CDN位于浏览器和服务器之间，主要起到缓存加速的作用；
爬虫是另一类User Agent，是自动访问网络资源的程序。
TCP/IP是网络世界最常用的协议，HTTP通常运行在TCP/IP提供的可靠传输基础上；
DNS域名是IP地址的等价替代，需要用域名解析实现到IP地址的映射；
URI是用来标记互联网上资源的一个名字，由“协议名+主机名+路径”构成，俗称URL；
HTTPS相当于“HTTP+SSL/TLS+TCP/IP”，为HTTP套了一个安全的外壳；
代理是HTTP传输过程中的“中转站”，可以实现缓存加速、负载均衡等功能。

##