First time ClickHouse
---

初识ClickHouse，大概是在去年12月份，Clickhouse受邀来中国开第一次Meetup. 那天我去参加了，很多小伙伴都是被官方那页[Benchmark](https://clickhouse.yandex/benchmark.html)吸引而来，我猜测。

让我前往参加的一个很大原因，我朋友说clickhouse挺牛的，他从深圳过来参加Meetup。

ClickHouse 一个来自俄罗斯的凶猛彪悍的分析数据库。

Clickhouse总体来说有几个优势：

* 高性能，官方数据
* 多功能，支持很多系统无缝结合使用
* 设计简洁，自成体系

今天内容分成三个部分，介绍ClickHouse这个凶悍的分布式数据库。第一部分介绍由来，第二部分介绍架构演化，第三部分介绍我初步使用的感受。

### First time ClickHouse

ClickHouse - 开源的分布式列式DBMS数据库。

Yandex在2016年6月15日开源了一个数据分析的数据库Clickhouse。

有尔罗斯"百度"之称的"Yandex"是一家俄罗斯互联网企业，旗下的搜索引擎在俄国内拥有逾60%的市场占有率，同时也提供其他的一系列互联网产品和服务。数据显示，Yandex是目前世界第五大搜索引擎：在2012年4月，平均每日的搜索量超过1.5亿次；5月份，每日访客超过2550万。


我们来看一下Clickhouse简介：

> ClickHouse is an open source distributed column-oriented database management system that allows generating analytical data reports in real time using SQL queries. Сreated by Yandex ClickHouse manages extremely large volumes of data in a stable and sustainable manner.

clickhouse的性能可以吊打很多商业级的分布式MPP数据库。让人非常惊讶，我在虚拟机里面运行它性能依然让我眼前一亮。

官方宣称：

* 高性能
* 线性扩张
* 高效利用硬件
* 功能丰富
* 高可靠，无中心、数据分片
* 简单易用

#### 高性能

clickhouse的性能超过了现有市面上主流的列式数据库系统。每秒钟可处理数亿的数据，每个节点可以存储数十TB的数据，高效率利用硬件快速扫描数据。

clickhouse尽其所能的使用硬件来快速的处理每个查询，单个查询处理性能峰值每秒超过2TB。

ClickHouse的查询效率比传统方法快`100-1,000`倍。

![Analytical-DBMS](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/analytical-DBMS.png)

#### 线性扩张

ClickHouse允许在任何时候，按需添加新的服务器到集群中，而无需话费任何代价，节点会自动发现，扩张集群的存储和计算能力。目前已经成功服务于Yandex.Metrica业务，生产集群两年间从60个扩张到394个，此集群分布于6个不同的数据中心，ClickHouse具备跨数据中心访问能力。

Clickhouse即可以在虚拟机里面高速运行，也可以轻松适应在数百个节点的集群运行。目前，每个节点的存储容量为100TB，无单点故障。

#### 高效利用硬件

clickhouse相比传统的面向行的数据库拥有更高的IO吞吐量，处理典型的分析快两到三个数量级。还支持大量利用内存，把热数据直接存储在RAM中，从而缩短响应时间。

基于硬盘存储的优化，提高磁盘转动效率，为连续存储拥有特殊优化。

高CPU利用率，向量化执行和CPU指令集优化，运行时代码生成(局部)。

#### 容错

clickhouse支持多主机异步复制，可以跨多个数据中心进行部署。单个节点或整个数据中心的停机时间不会影响系统读取和写入的可用性。分布式读取会自动平衡到可用副本以避免增加延迟。复制数据在服务器停机恢复后会自动或半自动同步。

#### 功能丰富

clickhouse具有用户友好的SQL查询支持和许多内置的分析函数。比如: URL、IP统计函数。

可支持本地和分布式连接，支持多种数据源，可以简单和现有数据库系统融合。

#### 何时使用clickhouse

ClickHouse适合用于很多厂家，如：结构化日志流或IoT 监控数据。属于OLAP的分析型高性能数据管理系统。

ClickHouse不适用，事务性（OLTP）业务，目前不支持Update/Delete，在今年第一季度计划支持。高效率的键值访问，Blob或文档存储，非结构化数据。

### 关键特征

- 列式存储
- 矢量化执行
- 数据压缩
- 并行和分布式查询
- 实时查询处理
- 实时数据导入
- 磁盘参考位
- 跨数据中心复制
- 高可用性
- SQL支持
- 本地和分布式连接
- 可远程查询外部系统数据
- 近似查询处理
- 统计类函数
- 全面支持IPv6
- 网站分析特性
- 最先进的算法
- 详细文档

#### 谁在用

- [Yandex.Metrica](https://clickhouse.yandex/docs/en/introduction/ya_metrika_task.html)
- [CloudFlare DNS Analytics](https://blog.cloudflare.com/how-cloudflare-analyzes-1m-dns-queries-per-second/)
- [Migrating to Yandex ClickHouse by LifeStreet (machine translation from Russian)](https://translate.yandex.com/translate?url=https%3A%2F%2Fhabrahabr.ru%2Fpost%2F322620%2F&lang=ru-en)
- [How to start ClickHouse up and win the jackpot by SMI2 (machine translation from Russian)](https://translate.yandex.com/translate?url=https%3A%2F%2Fhabrahabr.ru%2Fcompany%2Fsmi2%2Fblog%2F314558%2F&lang=ru-en)
- [First place at Analysys OLAP algorithm contest (machine translation from Chinese)](https://translate.yandex.com/translate?url=http%3A%2F%2Fwww.jianshu.com%2Fp%2F4c86a2478cca&lang=zh-en)
- [LHCb experiment by CERN](https://www.yandex.com/company/press_center/press_releases/2012/2012-04-10/)

### ClickHouse架构演化

MySQL (MyISAM) 2008-2011

Metrage, 2010-2015

ClickHouse，In 2012 it was in production state. In 2014 we re-lauched Yandex.Metrica as Metrica 2.

关于架构演化参考：

- 百度云 - Clickhouse Introduction.pdf

官方没有任何ClickHouse相关架构设计的文章，显得非常神秘，但是Meetup中，作者多次提到MySQL，ClickHouse底层使用类似LSM Tree，变种LSM Tree，不写内存表，不记录log，直接落地磁盘，异步merge，分块写。

列式存储+向量化+Code generation(局部)+CPU底层指令集(SIMD)优化+MPP架构= 高性能

百度云: 

- 链接:https://pan.baidu.com/s/1F1vRFtf7rsxH3twhimb7DA  密码:x63k

- 竞品
    + Vertica 
    + Greenplum 
    + Impala
    + Drill
    + Palo
    + Redshift
    + CrateDB
    + BigQuery

我基本都使用过以上产品，有SQL on Hadoop系统，依赖特别多，非独立系统，难维护。

也有独立系统和纯粹的MPP架构系统，但是性能远无法和它相比，商业级数据库贵。

刚开始接触，不好过多评论，带我在研究一段时间，会把架构篇补上，带大家一探究竟。

### 初谈ClickHouse

- 1、由于分布式表参数传错，导致传到其他库的表引用，导致乌龙，我发现我把所有表和库都删除，重新建立一模一样的表和库，依然有数据。

- 2、最后发现分布式表引用了其他库的东西，我还去底层一顿翻阅，并没有看出啥来，坑。。。

- 3、分布式表不存储任何数据，而是分发请求，类似路由功能，读取本地表，分布式执行局部请求。

- 4、元数据信息不会同步是大坑，需自己手动去所有节点创建表和库，在需要查询的节点创建分布式表去关联，否则某些节点库和表都无法查询，你需要手动维护元数据信息，傲娇吧。

- 5、为什么要创建分布式表去关联本地表？因为他并没有自动分片的功能，相比HDFS，ES，CrateDB而言，它是全手动的，分片需要使用者自己控制，包括分布式数据均衡，找时间画几张图给大家解释。

- 6、local表和Distributed表如何关联？

```
CREATE TABLE ontime_local (FlightDate Date,Year UInt16) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192);

CREATE TABLE ontime_all AS ontime_local ENGINE = Distributed(bip_ck_cluster, default, ontime_local, rand());
```

它主要有两类引擎：Tree | Distributed 哎，慢慢体会吧。

- 7、部署是非常简单的，复制表依赖zookeeper，不知道集群表是否也依赖，还没看代码。

- 8、建议写本地表，轮训方式写，需使用者控制，避免数据不均衡。

- 9、通过tpcdump监听tcp端口，执行分布式表请求确实是分布式执行的，有部分查询下推到各节点本地表执行过滤，然后在汇总结果返回客户端。

- 10、其实它并非是分布式数据库，而是一个带复制表和分布式表的数据库，要数据分布式多节点查询，需要使用者控制数据分片到多个节点，相信不久的将来会完善的。

- 11、复制表，通过多表同时引用同一个zk的路径，实现相互同步数据。例如: 

```
ReplicatedMergeTree('/clickhouse/tables/{layer}-{shard}/hits', '{replica}', EventDate, intHash32(UserID), (CounterID, EventDate, intHash32(UserID), EventTime), 8192)

ENGINE = ReplicatedMergeTree('<path_in_zookeper>', '{replica}', <date_partition_column>, (sort columns), 8192)
```

这里，有个坑，`{replica}`使用，需要每个节点配置文件都有这些参数，并且这里这个参数必须唯一。

- 12、复制表+分布式表结合使用，我探索了一番，发现插入一条数据居然在分布式表中看到3条，我的天，明显使用不当，不知道为何会出现这个情况，带我在深入研究一番，接下来的系列文章深入介绍。

- 13、使用下来，让我感觉HDFS这个文件系统还是非常智能化的，但是也有不可改变的致命缺点，而正是有了它，很多分析型引擎类的系统才能在它基础上成长，没有它就不会有Spark/Impala/Hive/Drill/PrestoDB/MR/MPP on HDFS/BigSQL/Phoenix/Tajo/Flink/Tez/More，分析型系统依赖他保障文件系统层面的高可靠和稳定性。clickhouse直走自己的路，极致的性能就是他的目标。一般太完美的存在，一定会有致命缺陷，重点是是否在你可忍受范围内，值得权衡。

- 14、通过官方提供的数据和SQL，测试结果确实非常强大，参考我CreateDB性能一篇，发现那是三台物理机测试结果，是我测试3台虚拟机几倍的硬件，远不及这个性能，正真的高性能。天生丽质，你得忍受他的不足。 参考 - 百度云：`first-time-clickhouse-benchmark.txt`

- 15、粗粒度索引，提高查询性能，还未深究，未来继续探索。写入是直接刷磁盘，没有缓冲，所以如果每秒钟几万次频繁插入数据，每次一条，会导致底层merge引擎非常忙碌，会导致写入失败，所以官方建议以导入数据的方式，分批次写入数据，每次至少10w+/s，而不适合频繁多次插入少量数据。

- 16、不支持Transaction，OLAP就是追求极致的快。

- 17、底层存储透明，所以我猜测copy底层数据到其他路径，创建同结构的表关联，依然可以正常使用，像HDFS+Hive，但是带来安全挑战，文件系统层保护吧。

接下来，我会继续进一步研究clickhouse，写一下架构相关内容、安装和更多细节，欢迎继续关注。

下一篇，介绍《clickhouse快速上手》

英语能力有限，有些官网看到的资料内容，白话后不准确，还望海涵，如有不准确或错漏，欢迎指正。

***参考：***

[1] http://itweet.cn/blog/2017/11/22/Data-Warehouses-Past-Present-and-Future
[2] https://clickhouse.yandex/
[3] https://clickhouse.yandex/benchmark.html
[4] https://www.altinity.com/blog/2017/7/3/clickhouse-vs-redshift-2
[5] https://www.altinity.com/blog/2017/6/5/clickhouse-data-distribution

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive


