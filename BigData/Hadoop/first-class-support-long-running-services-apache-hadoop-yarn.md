Apache Hadoop Yarn 提供最好的Long Service运行支持
---

## 介绍

Apache Hadoop Yarn 做为一个大数据领域(Apache Hadoop Yarn)通用的资源管理平台而闻名，它提供复杂的集群资源管理和调度服务，从中高度抽象出通用业务逻辑，从而让更多的计算框架专注于计算本身，通过他提供的高度抽象的接口，轻松的运行任务在YARN中。

除了大数据应用框架，我们看到今天另一类工作负载是长期运行的服务，如：Hbase，Hive/LLAP和基于容器(如：docker)的服务。在过去一年里，YARN社区一直致力于为能提供长期运行服务而努力。

YARN SERVICE FRAMEWORK COMING IN APACHE HADOOP 3.1!

这个特性，我们称之为`YARN SERVICE FRAMEWORK`，在2017年11月刚刚合并到Master。总共有108个提交，33539行代码更改。预计将在Apache Hadoop 3.1版本中提供。这项工作主要包括以下内容：

- 1、一个核心框架(ApplicationMaster)运行在YARN上，用作容器编排，负责所有服务的生命周期管理。
- 2、一个RESTful API服务，使用一个简单的JSON规范，供用于在YARN上部署和管理其服务。
- 3、提供YARN DNS服务器，通过标准DNS查找可以发现YARN上的服务。
- 4、高级容器编排调度，每个容器的affinity和anti-affinity，容器大小的调整和节点标签。
- 5、容器和服务器的滚动升级支持。

YARN Service framework与其他的新特性是紧密相关的。

- 1、对Docker on YARN的一级支持
- 2、一种基于Hbase的原生YARN Timeline Service，用于记录生命周期事件和指标，并为用户提供丰富的分析API，用于查询应用程序的详细信息。
- 3、YARN UI2中提供服务UI

## EXAMPLE

在YARN上管理服务，很多底层复杂的逻辑是隐藏起来的，用户不需要关心。只需要安装规范的JSON格式，通过CLI或者REST API部署和管理运行在YARN上的服务。下面介绍如何把httpd容器部署在YARN上，用户只需通过REST API或使用CLI提交JSON文件，系统会自动处理剩下的事情-启动并且监听容器或其他任何需要保持应用程序运行的动作，比如，自动重启运行失败的容器。

1、启动服务，使用以下提供的JSON文件运行命令

```
yarn app -launch my-httpd /path/to/httpd.json
{

"name": "httpd-service",

"lifetime": "3600",

"components": [

 {

   "name": "httpd",

   "number_of_containers": 2,

   "artifact": {

     "id": "centos/httpd-24-centos7:latest",

     "type": "DOCKER"

   },

   "launch_command": "/usr/bin/run-httpd",

   "resource": {

     "cpus": 1,

     "memory": "1024"

   }

 }]

}
```

2、获得应用程序的状态

```
yarn app -status my-httpd
```

3、把容器数量增加到3：

```
yarn app -flex my-httpd -component httpd 3
```

4、停止这个服务

```
To stop the service
```

5、重新启动停止的服务

```
yarn app -start my-httpd
```

## 深度解析

下图说明了一个长期运行在YARN集群中的服务涉及到的组要组件和流程。

![](full-flesged-YARN-cluster-illustration.jpg)

典型的工作流程：

1、用户发出JSON请求，描述服务的规格，如容器内存大小，CPU内核数量，Docker映像ID等等。同样，用户也可以使用YARN CLI提交他们的服务。
2、RM在接受请求后，启动一个ApplicationMaster（即容器编排框架）。
3、编排框架根据用户的资源要求从RM中请求资源，然后在分配容器时在NodeManager上启动容器。
4、NodeManager依次启动容器进程或使用Docker在运行时启动容器。
5、YARN编配框架监视容器的健康和执行情况，对容器的故障或不健康进行处理。它将服务生命周期事件和指标写入YARN Timeline Server（由HBase支持）。它还将额外的服务元信息（如容器IP和主机）写入由ZooKeeper支持的YARN服务注册表。
6、注册DNS服务器监听ZooKeeper中的znode创建或删除，并创建各种DNS记录（如A记录和服务记录）来提供DNS查询。
7、根据JSON规范和YARN配置中提供的信息，每个Docker容器都有一个用户友好的主机名。然后，客户端可以使用标准DNS查找容器主机名从而得到容器IP。

## 有什么好处

YARN服务框架擅长哪个领域？

1、Hadoop在这个行业已经有十多年的历史了。在Hadoop2中引入YARN，是一个非常成熟的项目，并得到大规模生产环境的验证，有大量企业案例。此外，YARN容器编排框架利用了Hadoop中所有现有的稳定功能。

2、YARN已被证明可以很好地支持像MapReduce和Spark这样的批处理工作负载。此功能可以将现有的基于容器的服务带入YARN。结果是用户现在可以使用单个群集来运行批处理作业和长时间运行的服务。这也使批量作业和服务之间的资源共享成为可能，这些资源使用模式可能有很大的不同 例如，服务通常在一天中以高资源利用率运行，而批处理作业通常在夜间运行。所以资源共享可以大大提高整体的集群利用率。

3、它支持kerberos安全，并且与标准的kerberized Hadoop集群非常匹配。

4、除了Docker集装箱化的应用程序，它还支持标准的tar包应用程序，

YARN越来越往专业的资源调度和管理方面发展，将会支持批处理、长任务作业运行。让集群资源利用率更高，同一集群实现更多工作负载类型作业成为可能。

让我们期待Hadoop更多新功能。

欢迎关注微信公众号[whoami]，阅读更多内容。
![image.png](http://upload-images.jianshu.io/upload_images/9687832-2ff1ee6f489dcff3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive





