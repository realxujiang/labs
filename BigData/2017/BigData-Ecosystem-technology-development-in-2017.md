2017年大数据技术的回顾与展望(迟...)
---

回往，我从事大数据行业已经第5年了。

可以说，从大数据非常技术，很难商业化，到今天各种各样的大数据创业公司井喷式发展。

2017年，非常特殊，已经有人开始唱衰Hadoop

而此时，人工智能AI，开始在国内外大肆炒作，这样的场面何其相似。

2007年，Hadoop面世，2009年国内开始有人尝试Hadoop，到今天Hadoop在互联网公司大规模部署，帮助企业实现高效率的数据变现。

Hadoop最早是始于Yahoo孵化，用于存储海量的日志数据和爬虫数据，并且定期清洗、聚合数据。

互联网公司，有海量的数据，需要这样的分布式系统帮助解决日志问题。

随着Hadoop的开放性，Hadoop受到了更多的应用场景的检测，逐渐显现出不足，但是他强大的可扩展性和容错依旧优秀。

由于开源的特性，导致更多的公司尝试利用Hadoop解决生成问题，不足之处很多。

慢慢的Hadoop生态圈的概念出来了，最开始就是pig、hive这样封装MapReduce的框架出现，大大降低企业使用Hadoop的门槛。

国内，最早使用Hadoop解决业务问题的是电商(互联网企业)，推荐系统；传统企业最早始于运营商、银行、金融；开始渗透到公安、交通、政府、工业等领域。

在海里数据中，可以高并发写入和查询，于是就社区发起了Hbase项目，到目前为止依然是个大互联网公司热爱的技术，社区非常活跃。

为保障Hadoop生态圈个组件之间数据一致性、以及Hbase高并发写入多节点数据一致，通过zookeeper进行协调。

Hadoop无法支持低延迟数据分析，出现了流处理技术storm。

MapReduce中间结果写磁盘特别慢，而如今硬件发展快，可以大量利用内存，出现了内存计算技术spark。

今天，以Hadoop为中心，已经出现太多的针对各种场景特殊优化的组件。

目前主要分一下几个方向:

* 批处理系统
    + MapReduce
    + Spark

* 流处理系统
    + Storm
    + Flink
    + Heron
    + SparkStreaming (勉强)

* 即席查询 (SQL on Hadoop)
    + Impala
    + Drill
    + Persto
    + HAWQ
    + Hive2 LLAP (勉强）
    + SparkSQL (勉强）

* 机器学习 & 深度学习
    + SystemML
    + TensorFlow
    + Mllib
    + MADLab

* NoSQL
    + Cassandra 
    + Hbase+Phoenix

* 集群安全
    + Ranager
    + Sentry
    + Kerberos
    + Konx
    + Cloudera Navigator (闭源)
    + Navigator Encrypt & Key (闭源)

* 企业级发行版
    + CDH
    + HDP
    + MapR

目前Hadoop主要分为：批处理灵活可编程系统、流处理系统、SQL即席查询、机器学习&深度学习系统、NoSQL目前使用广泛的如上所示，随着Hadoop进入各行各业，集群安全和数据安全也是Hadoop各大发行版公司重点研发的方向。

目前Cloudera CDH和Hortonworks HDP，都在不同程度上完成对集群数据安全和访问安全的控制。

目前CDH和HDP主流的企业级大数据发行版，CDH产品成熟度和企业级安全方面做做得最成熟和可靠的，属于半闭源产品。HDP是大而全的功能，并且以完全开放的路线在发展，让更多的公司能参与其中，让客户有更多选择。

国内企业，大都以CDH和HDP做为参考目标，产品也都有各自的特色，帮助客户更要的解决生产问题。

2017年，Hadoop整体开始回归SQL，各家都在发力，因为在企业级市场，SQL on Haodop的SQL语法兼容度和高性能是很关键的特性，包括兼容现有客户投资的DB系统。

**2017年**

+ SparkSQL宣布完整通过TPC-DS的99个SQL性能测试。
+ MADlab，SQL中编写数据挖掘&机器学习算法。
+ TensorFlow on Hadoop框架层出不穷。
+ Hive2 LLAP低延迟数据分析发布，即席查询。  hortonworks 务实。
+ Impala 解析引擎更智能，高性能响应，分布式查询优化。
+ Hadoop发行版，强调支持数据访问权限、数据安全、集群安全。
+ Apache Hadoop 3.3.0 GA发布，期待的新功能。
+ 更多Hadoop上云需求，面临架构的整体变化，社区&厂商都在努力。
+ SQL on Cloud（GreenPlum系）和 NewSQL系获得更多融资。
+ NoSQL开始别唱衰、但是Hbase依然坚挺，服务于海量数据业务。
+ SQL on Hadoop很多框架，眼花缭乱，残酷的淘汰，社区慢慢变冷。
+ 一统批处理和流处理的Apache Beam框架发布。
+ 企业大数据即席查询BI可视化。

## 2017年是Hadoop在企业级市场更多落地，解决实际问题，更务实的一年。

SQL on Hadoop系统，在更多传统客户那里更受青睐，驳杂的技术词汇，客户浪费大量时间调研和考察。

商业Hadoop发行版公司都提出了自己Hadoop on Cloud方案，弹性伸缩，按需建立集群、数据统一存储Cloud Storage Pool。

Spark、Impala、greenplum、NewSQL、NoSQL与Hadoop结合没那么紧密的独立系统，更容易云化，底层直接读写S3、Azure Blob Storage，基本抛弃了Hadoop。

## 2018年，Hadoop会变得更加的成熟和适应企业现有基础设施架构。

SQL on Hadoop系统，大浪淘沙、只留精品。

Hadoop on Cloud有更加优秀的平台和产品出现。

DL&ML on Hadoop有更加成熟的产品和方案。

BigData on Cloud涌现更多商业企业和开源软件。

企业级流处理系统，务必更加易用和可商业化。

Hadoop 3.0更多案例，更高的性能。

Hadoop系统的选择，更多企业会变得更加慎重。

中小规模企业，寻找Hadoop之外的系统方案，管理企业数据。

GreenPlume OpenSource 将会有越来越多的案例，本地和云端。

真正的批处理和流处理系统Flink将会有更多应用案例。

没人真正关心流处理和批处理模型，我们要的是快、超快、超超超快。

OpenSource 企业级BI工具更加成熟，原生支持SQL on Hadoop系统。

Hadoop将会在数据安全、集群安全、访问控制提供完整的产品。

## 文末

非常繁忙的年底，新的一年研发新一代的企业级流处理系统，支持完整的BI可视化工具，完整的数据采集可视化。目前正在争取年后发布一个版本，一个纯粹的企业级流处理系统。

2018年，专注于企业级数据仓库技术，业余计划撸一套分布式OLAP数据库产品，极致性能、数据可视化；积极学习业界领先的分布式数据技术，闲暇之余玩faceswap，DL App产品。

关于FaceFake，可以关注我的`GitHub`，一种基于深度学习的换脸技术，我觉得可以做成一个app，把你喜欢的明星变成任何影视作品的男女主。

技术成熟，已经用在了歪门邪道上，国外有个工程师因此火爆了一把，上了头条。

关于FaceFake，GitHub空空如也，目前还是我的想象啦，上线再通知各位。

> 文章，是即兴创作，如未描述清楚，请留言讨论。

欢迎关注微信公众号[whoami]，阅读更多内容。

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/