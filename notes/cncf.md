- [CNCF](#cncf)
    - [Cloud Native](#cloud-native)
    - [CNCF Landscape](#cncf-landscape)
    - [CNCF Landscape全景图](#cncf-landscape全景图)
        - [1.App Definition and Development应用定义与开发](#1app-definition-and-development应用定义与开发)
        - [2.Orchestration Management编排管理](#2orchestration-management编排管理)
            - [Scheduling & Orchestration](#scheduling--orchestration)
            - [Coordination & Service Discovery](#coordination--service-discovery)
            - [Remote Procedure Call](#remote-procedure-call)
            - [Service Proxy](#service-proxy)
            - [API网关](#api网关)
            - [Service Mesh](#service-mesh)
        - [3.Runtime运行环境](#3runtime运行环境)
            - [Container Runtime](#container-runtime)
            - [Cloud-Native Storage](#cloud-native-storage)
            - [Cloud-Native Network](#cloud-native-network)
        - [4.Provisioning配置管理](#4provisioning配置管理)
            - [Automation & Configuration](#automation--configuration)
            - [Container Registry](#container-registry)
            - [Security & Compliance](#security--compliance)
            - [Key Management](#key-management)
        - [5.Platform平台管理](#5platform平台管理)
        - [6.Observability and Analysis监控分析](#6observability-and-analysis监控分析)
        - [7.Serverless 无服务](#7serverless-无服务)
        - [8.合作伙伴（Special）](#8合作伙伴special)
        - [9.成员构成](#9成员构成)

# CNCF

Cloud Native Computing Foundation，云原生计算基金会（以下简称CNCF）是一个开源软件基金会，它致力于云原生（Cloud Native）技术的普及和可持续发展。云原生技术是通过一系列的软件、规范和标准帮助企业和组织，在现代的动态环境（如公共云、私有云和混合云）中构建和运行敏捷的、可扩展的应用程序。容器、微服务、微服务治理、声明式API等都是代表性的云原生技术。

这些技术使松散耦合的系统具有更好的弹性、可管理性，同时更容易被监控和观察。

这些技术通过与强大的自动化工具相结合，允许工程师频繁地、可预见地对系统进行任意的更改，并尽可能减少由此带来的工作量, 而这就是云原生技术最希望为技术团队以及业务带来的价值。

## Cloud Native

Cloud Native（云原生）是以云架构为优先的应用开发模式

Cloud Native 并不是一种具体的技术，而是一类思想的集合，包括DevOps、持续交付（Continuous Delivery）、微服务（MicroServices）、敏捷基础设施（Agile Infrastructure）、康威定律（Conways Law）等，以及根据商业能力对公司进行重组。Cloud Native 既包含技术（微服务，敏捷基础设施），也包含管理（DevOps，持续交付，康威定律，重组等）。所以，Cloud Native 也可以说是一系列Cloud技术、企业管理方法的集合。

Cloud Native 具备有以下特性：

以云为基础架构

云服务

无服务

可扩展

高可用

敏捷

云优先

等等

## CNCF Landscape
[CNCF Landscape](https://github.com/cncf/landscape) 通过对云原生技术中的大多数项目和产品进行分类，来追踪整个生态中的大量应用。

CNCF Landscape路线图
CNCF Landscape最重要的产出包括一个路线图和一个全景图。路线图（Trail Map）是CNCF对云原生用户使用开源项目以及云原生技术的推荐过程。在路线图的每个步骤中，用户都可以选择供应商支持的产品或自己动手使用开源项目。
![](../pics/cncf/trailmap.png)


整个路线图分成了十个步骤，每个步骤都是用户或平台开发者将云原生技术在实际环境中落地时，需要循序渐进思考和处理的问题：

1. 容器化。目前最流行的容器化技术是Docker，你可以将任意大小的应用程序和依赖项，甚至在模拟器上运行的一些程序，都进行容器化。随着时间的推移，你还可以对应用程序进行分割，并将未来的功能编写为微服务。

2. CI/CD（持续集成和持续发布）。创建CI/CD环境，从而使源代码上的任意修改，都能够自动通过容器进行编译、测试，并被部署到预生产甚至生产环境中。

3. 应用编排。Kubernetes是目前市场上应用编排领域被最广泛应用的工具，Helm Charts可以用来帮助应用开发和发布者用于升级Kubernetes上运行的应用。

4. 监控和分析。在这一步中，用户需要为平台选择监控、日志以及跟踪的相关工具，例如将Prometheus用于监控、Fluentd用于日志、Jaeger用于整个应用调用链的跟踪。

5. 服务代理、发现和治理。CoreDNS、Envoy和LInkerd可以分别用于服务发现和服务治理，提供服务的健康检查、请求路由、和负载均衡等功能。

6. 网络。Calico、Flannel以及Weave Net等软件用于提供更灵活的网络功能。

7. 分布式数据库和存储。分布式数据库可以提供更好的弹性和伸缩性能，但同时需要专业的容器存储予以支持。

8. 流和消息处理。当应用需要比JSON-REST这个模式更高的性能时，可以考虑使用gRPC或者NATS。gRPC是一个通用的RPC（远程调用）框架（类似各种框架中的RPC调用），NATS是一个发布/订阅和负载均衡的消息队列系统。

9. 容器镜像库和运行环境。Harbor是目前最受欢迎的容器镜像库，同时，你也可以选择使用不同的容器运行环境用于运行容器程序。

10. 软件发布。最后可以借助Notary等软件用于软件的安全发布。


## CNCF Landscape全景图
[CNCF Landscape](https://landscape.cncf.io/) 路线图 从实践步骤上帮助用户梳理了整个云原生应用的最佳流程。然而整个实践过程中的每个环节，用户都需要了解有哪些具体的软件和产品选择，这就是CNCF Landscape全景图发挥作用的地方了
![](../pics/cncf/landscape.png)

这张全景图试图从云原生的层次结构，以及不同的功能组成上，让用户了解云原生体系的全貌，并帮助用户在不同组件层次去选择恰当的软件和工具进行支持。从总体来看，它将云原生生态分为以下几层：

### 1.App Definition and Development应用定义与开发
这一层就是容器平台上运行的具体应用和工具了，可以理解为容器平台的应用商店。根据应用的不同作用的使用场景，可以大致分为以下几种类型：数据库（例如MySQL、MariaDB、mongoDB、PostgreSQL、Cassandra、TiDB等）、流处理和消息队列（例如Spark、Storm、RocketMQ、Kafka、RabbitMQ等）、应用和镜像制作（用于将应用封装成标准镜像，使应用能在标准的容器平台上运行，例如Helm、Docker Composer、Packer等）、CI/CD（最常见的Jenkins、Atlassian公司开发的Bamboo等）。

### 2.Orchestration Management编排管理
这一层主要负责容器平台的编排和调度，包括服务的发现和治理，远程调用，服务代理，微服务治理等组件，包括：
#### Scheduling & Orchestration
在这个领域，Kubernetes是当仁不让的头号玩家，目前基于Kubernetes的容器生态得到了迅速发展。其它的编排工具还包括Mesos、Docker Swarm等。
#### Coordination & Service Discovery
分布式计算中很重要的一点就是各个服务之间的协同以及服务发现（或节点发现的问题），从老牌的Zookeeper到近年来在很多互联网厂商和应用中流行的Consul（Docker Swarm默认使用），都可以用于分布式服务的发现和配置，Kubernetes默认使用的则是CoreOS旗下的Etcd。
#### Remote Procedure Call
微服务间进行通信，通常有两种方式，其一为HTTP REST-JSON的方式，另一种为RPC 方式，相比起来RPC方式效率更高。常用的包括 Google 开源的 GRPC 、apache 旗下的 thrift 框架、Netflix 开源的自带负载均衡的 ribbon 和 avra 数据序列化框架。

#### Service Proxy
服务代理和负载均衡当前还是以envoy和haproxy为代表, 显然它并不能像毕业的Kubernetes那样有影响力，相反而言，硬件方式的F5是土豪们的最爱，基于Nginx的OPENRESTY或者Nginx本身即使很多务实的开发者的选择，所以在微服务的路上想要一统天下，还需要看后续的服务网格的部分。

#### API网关
CNCF没有相关的孵化中或者已毕业的项目，根据实际的使用情况务实的开发者可能会直接使用Kong，Kong本身也是在Nginx上产生的一个框架，难能可贵的是已经形成了一部分生态

#### Service Mesh
服务网格显然是后续的重头戏，相较于孵化中的LINKERD，显然Istio后来居上，俨然有成为微服务管控的集大成者之势，而在实际的项目中反而比LINKERD和envoy更具竞争性，而对于新型的微服务架构希望进行尝试的用户也有很多直接一面导向了Istio，而NETFLIX的spring cloud相关的组件仍然继续不温不火，慢慢地错失良机

### 3.Runtime运行环境
Runtime这一层可以理解为容器的整个运行环境，是云原生中最核心的部分，它包括了计算、存储、网络三大块：

#### Container Runtime

Docker是最广为人知的容器运行环境，但生产环境下也有一些其他的容器环境在运行。Containerd是满足OCI规范的核心容器运行时，从设计上就是为了嵌入大型系统的。它由Docker Inc公司启动，并且在2017年3月份捐赠给了CNCF。此外，CoreOS的RKT是一个用于在Linux上运行应用程序容器的CLI，也可以作为安全、可组合和基于标准的容器虚拟化运行环境。

#### Cloud-Native Storage

起初，容器为无状态的运行单元，容器最上一层文件系统无法保存其在运行时写入的文件或数据，容器重建或重启后，这些写入的数据将丢失。但随着数据库、消息队列等中间件逐步在容器环境中得到应用，如今用户对容器持久化存储的理解和需求也更加深入和迫切。本文稍后还将对容器存储做更深入的分析。

#### Cloud-Native Network

网络历来是虚拟化技术中最灵活多变的部分，目前，大多数客户使用的主要包括Calico、Flannel、Open vSwitch等方案。

### 4.Provisioning配置管理

有了物理机或虚拟机后，在运行容器化服务之前，需要为容器准备标准化的基础环境，这就是Provisioning这一层的作用。在Provisioning这一层中，分为以下几个功能组成模块：

#### Automation & Configuration

用于自动化部署和配置容器运行平台和环境，代表工具和厂商包括Ansible、Chef、Puppet、VMware、OpenStack。

#### Container Registry

容器镜像库是整个CNCF云原生中的核心部件之一，因为基于容器的运行环境中，所有的应用都需要借助容器镜像库来进行安装和部署。容器镜像库又分为公有和私有，公有的容器镜像库包括docker官方的registry，AWS的Elastic Container Registry，Google的Container Registry等。在私有镜像库中，VMware中国团队主导的Harbor得到了广泛的应用，大量的容器平台目前都基于Harbor构建其镜像仓库。

#### Security & Compliance
Notary和TUF（The Upgrade Framework）是这个领域两个主要的项目，其中TUF是一个开源的安全标准，Notary是其中一个实现。Notary软件除了确保软件的出处外，它还能保证在未经容器镜像提供者批准的情况下，不会在镜像供应链的任何地方修改镜像内的内容，从而确保从开发到运营的过程中，安全都被无缝统一地嵌入到整个工作流中。

#### Key Management
主要用于在整个容器平台中进行秘钥管理。

### 5.Platform平台管理
从横向上看，整个云原生还包括众多的经过认证的平台供应商。

### 6.Observability and Analysis监控分析
这个部分包含了大量用于对平台进行监控（Prometheus、Nagios、Grafana、Zabbix等）、日志（Fluentd、ElasticSearch、Logstash）、以及追踪（Jaeger）的工具。

### 7.Serverless 无服务

### 8.合作伙伴（Special）

### 9.成员构成

## 文章及视频

https://www.cncf.io/webinars/what-is-cloud-native-and-why-does-it-exist/
