- [Consul](#consul)
    - [介绍](#介绍)
    - [Consul特性](#consul特性)
        - [基础特性](#基础特性)
        - [高级特性](#高级特性)
    - [Consul工作原理](#consul工作原理)
        - [服务注册的方式](#服务注册的方式)
        - [服务发现的方式](#服务发现的方式)
    - [参考](#参考)
# Consul
## 介绍
Consul是基于GO语言开发的开源工具，是一个服务网格（微服务间的 TCP/IP，负责服务之间的网络调用、限流、熔断和监控）解决方案，它是一个分布式的，高度可用的系统，它提供了一个功能齐全的控制平面，其中包括：服务发现、健康检查、键值存储、安全服务通信、多数据中心。
## Consul特性
### 基础特性
1.服务注册/发现
为什么微服务架构下就需要做服务注册和服务发现呢？微服务的目标就是要将原来大一统的系统架构，拆分成细粒度的按功能职责分成的小系统，这样就会出现很多小的系统，部署的节点也会随之增加。试想一下，如果没有一个统一的服务组件来管理各系统间的列表，微服务架构是很难落地实现的。
Consul提供的服务注册/发现功能在数据强一致性和分区容错性上都有非常好的保证，但在集群可用性下就会稍微差一些（相比Euerka来说）。

2.数据强一致性保证
Consul采用了一致性算法Raft来保证服务列表数据在数据中心中各Server下的强一致性，这样能保证同一个数据中心下不管某一台Server Down了，请求从其他Server中同样也能获取的最新的服务列表数据。数据强一致性带来的副作用是当数据在同步或者Server在选举Leader过程中，会出现集群不可用。

3.多数据中心
Consul支持多数据中心(Data Center),多个数据中心之间通过Gossip协议进行数据同步。多数据中心的好处是当某个数据中心出现故障时，其他数据中心可以继续提供服务，提升了可用性。

4.健康检查
Consul支持基本硬件资源方面的检查，如：CPU、内存、硬盘等

5.Key/Value存储
Consul支持Key/Value存储功能，可以将Consul作为配置中心使用，可以将一些公共配置信息配置到Consul，然后通过Consul提供的 HTTP API来获取对应Key的Value。

### 高级特性
1.HTTP API
2.ACL

Consul工作模式
![Consul工作模式](./pics/consul-infos.png)
从上图可以看到，Consul中包括的3种不同的角色：Client、Server、Server-Leader。还有一个在图上没有标出来的角色Agent，一共4个角色，下面会逐一介绍它们的作用。

Agent<br>
1.是一个守护线程 <br>
2.跟随Consul应用启动而启动<br>
3.负责检查、维护节点同步<br>

Client<br>
1.转发所有请求给Server<br>
2.无状态，不持久化数据<br>
3.参与LAN Gossip的健康检查<br>

Server<br>
1.持久化数据<br>
2.转发请求给Server-Leader<br>
3.参与Server-Leader选举<br>
4.通过WAN Gossip，与其他数据中心交换数据<br>

Server-Leader<br>
1.响应RPC请求<br>
2.服务列表数据同步给Server<br>

## Consul工作原理
### 服务注册的方式
Consul服务注册有两种方式：HTTP API & JSON配置文件
方式一：HTTP API
```
http://{ip}:8500/v1/agent/service/register/:service
```

方式二：JSON 配置文件
```
{
    "services": [
            {
                    "id": "serverId",
                    "name": "serverName",
                    "tags": [
                            "primary"
                    ],
                    "address": "127.0.0.1",
                    "port": 9003,
                    "checks": [
                            {
                                    "id": "api-servie",
                                    "name": "Service 'xx' check",
                                    "http": "http://127.0.0.1:9003/public/health",
                                    "method": "GET",
                                    "interval": "10s",
                                    "timeout": "1s"
                            }
                    ]
            }
    ]
```


启动Consul增加启动参数-config-dir
```
nohup ./consul agent -dev -config-dir=/consul-conf/service.json &
```
### 服务发现的方式
服务发现的方式同时有两种：HTTP API & DNS Agent
方式一：HTTP API

获取某个service下健康的服务列表信息
```
http://{ip}:8500/v1/health/service/:service
```

方式二：DNS Agent
![](./pics/consul-agent.png)

## 参考
[Homepage](https://www.consul.io/)

[GitHub](https://github.com/hashicorp/consul)

[Consul 快速入门](https://www.jianshu.com/p/e8abae723fbb)
