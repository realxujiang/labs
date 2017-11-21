Data Warehouses: Past, Present, and Future
---

*** 数据仓库：过去、现在和未来 ***

欢迎来到我们全新的`ITweet Talk`系列视频和博客。我是作者，我将分享数百次咨询和部署数据平台的建议和最佳实践，这些咨询和部署是由企业客户围绕数据管理需求提出的，以支撑企业海量数据分析。下面我们深入探讨数据仓库的发展。

我经常接触数据仓库建设的需求，而现有的大数据系统也希望基于大数据建设数据仓库，然而Hadoop为核心发展起来的软件适用于OLAP的数据分析需求，OLTP这样的分布式数据库系统也如火如荼的发展。

在企业数据信息数据整合过程中，往往都是不同数据源放到不同的数据库系统中，没有数据仓库的规范化建设，跨部门进行数据协作，打破数据孤岛无法实现。

分布式系统，帮助解决这些问题，我们真正深入了解数据价值的人都知道，建设统一的数据中心，数据仓库，整合行业数据可以进行多种维度的数据分析，数据驱动决策，帮助企业创新。目前在金融、电商、广告等行业已经大规模利用新技术取得了不菲的成绩。

今天，企业级数据分析平台发生了很大的变化。

### 发生什么了？ 

![旧的数据仓库架构图](https://github.com/itweet/labs/raw/master/BigData/img/datadiagram-1.jpg)

那么，对于传统的数据仓库，你有各种各样的数据来源。您正在收集、清洗和整合数据，以便您可以将其呈现在您的数据仓库中，进行统计分析、预测分析、商业智能和其他工作。

好吧，随着时间的推移，现在变得更加复杂了。

![新的数据仓库架构图](https://github.com/itweet/labs/raw/master/BigData/img/datadiagram-2.jpg)

我们有云、有移动设备、社交媒体数据、机器数据、传感器数据。越来越多的数据来源，数据爆发式增长，非结构化数据、半结构化数据、结构化数据。

有大量的关于大数据介绍中，你会看到幻灯片谈论您必须处理PB级数据量，才能利用上这些新的数据分析技术。但是对我来说，这是没有抓住重点。

数据仓库真正的意义是什么？为什么企业对数据仓库支出不断增加。这是因为不是数据量和速度问题。随着发展，我们只需要增加硬件就能增加我们数据处理的规模，这才是分布式系统的强大之处。

万物互联的时代，随着数据的多样性和异质性从而增加数据分析的复杂性。我们的需求是关联和整合这些数据。但是，我们现有的数据分析工具，Hadoop或Spark并没有带来任何神器的解决方案。我们仍然在努力解决同样的问题：如何从不同的渠道获取数据、然后将他们关联起来，这样企业可以让数据说话，数据驱动决策。为了解决这个问题，我们需要依赖更多新的工具。

### 数据仓库的演变

利用新技术，使我们能更好的解决实际业务问题。

那么，我们来看看不同的技术，是如何帮助我们解决与数据相关的需求，为业务提供数据支撑。

### 流水线式的数据分析

我们看到一个有趣的现象，每个公司几乎都建立了一个数据流水线，随着新数据的进入，他们利用NoSQL数据库来存储文档数据。就像是一个无线容量的数据库，拥有很好的扩展性，并且还能进行大数据量的高速查询和搜索。

我们可以看到很多大规模使用MongoDB、Hbase、cassandra数据库。

随着数据多样性的发展，出现了很多新型的数据库。

### Analytic DB 的发展

我们列表 `RDBMS -> MPP -> HADOOP -> NOSQL -> NEWSQL` 主流的系统。

#### RDBMS

* Oracle        Oracle
* SQLServer     Microsoft
* DB2           IBM
* PostgreSQL    community
* MySQL         Oracle & community
* MariaDB       community

#### MPP

* Greenplum     Pivotal / DeepGreen
* Teradata      Teradata Company
* GBase 8a      南大通用
* HAWQ          Pivotal             (-> Hadoop
* Impala        Cloudera            (-> Hadoop
* Vertica       HP Company          

#### Hadoop  

* CDH                       Cloudera   
* HDP                       Hortonworks   
* TDH                       Transwarp  
* CRH                       Redoop  
* MapR Platform             MapR  

#### NoSQL

* MongoDB
* Hbase
* Cassandra
* Hypertable
* Accumulo
* Elasticsearch

#### NewSQL

* Spanner 
* CockroachDB 
* TiDB 
* SearchDB 
* OceanBase

虽然NoSQL因其性能、可伸缩性与可用性而广受赞誉，但其开发与数据重构的工作量要大于SQL存储。因此，有些人开始转向了NewSQL，它将NoSQL的优势与SQL的能力结合了起来。最为重要的是使用能够满足需要的解决方案。

* OLAP场景做到极致的Hadoop生态。
* OLTP场景的NewSQL数据库的发展。

各大云厂商也在大力发展支持OLTP的分布式金融级别的关系数据库，已解决MySQL分库分表难于管理的问题，分布式以后提供弹性的伸缩能力。
















