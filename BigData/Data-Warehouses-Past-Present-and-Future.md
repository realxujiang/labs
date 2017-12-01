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

万物互联的时代，随着数据的多样性和异质性从而增加数据分析的复杂性。我们的需求是关联和整合这些数据。但是，我们现有的数据分析工具，Hadoop或Spark并没有带来任何神器的解决方案。我们仍然在努力解决同样的问题：如何从不同的渠道获取数据、然后将他们关联起来，这样企业可以让数据说话，数据驱动决策。为了解决这些问题，我们需要依赖更多新的工具。

### 数据仓库的演变

利用新技术，使我们能更好的解决实际业务问题。

那么，我们来看看不同的技术，是如何帮助我们解决与数据相关的需求，为业务提供数据支撑。

OLAP场景的Hadoop解决方案，OLTP场景的NewSQL解决方案。

### 流水线式的数据分析

我们看到一个有趣的现象，每个公司几乎都建立了一个数据流水线，随着新数据的进入，他们利用NoSQL数据库来存储文档数据。就像是一个无线容量的数据库，拥有很好的扩展性，并且还能进行大数据量的高速查询和搜索。

我们可以看到很多大规模使用MongoDB、Hbase、cassandra数据库，还有NewSQL的发展。

随着数据多样性的出现，出现了很多新型的数据库。

### 新型数据分析需求

越来越高的数据分析需求和数据多样性的探索，导致了数据库系统的蓬勃发展，国产数据库也有了非常大的进步可以进入国际顶级的数据库会议发表论文，2017年腾讯的开源项目VLDB也发文了，而做为去IOE发起者的阿里在云端阿里云也如火如荼的发展数据库服务，比如：`PolarDB`、蚂蚁金服金融级数据库分布式数据库`OceanBase`都是黑科技级别的产品。为了在云端兼顾OLTP和OLAP的数据分析引擎，各大云厂商阿里云、腾讯云、XX云都使劲的推广各自的数据库技术，也采取与开源数据库厂商广泛合作的方式。

底层数据库系统，特别是NewSQL几大巨头也有有在长期招聘相关职位。可见目前分布式OLTP/OLAP数据库发展的势头，必然是与`Cloud`相结合，也只有云化才有机会大把捞金，不然开源数据库这样的生态下，底层基础软件出路在何方？

![新型数据分析需求](https://github.com/itweet/labs/raw/master/BigData/img/new-data-requirements-analysis.png)

### Analytic DB 的发展

我们列表 `RDBMS -> MPP -> HADOOP -> NOSQL -> NEWSQL` 主流的系统，根据我接触过的公司或产品来列举，个人认知有限，如未能列表全面，欢迎补充。

#### RDBMS

|    数据库     |              公司               |
| ------------ | ------------------------------- |
|  Oracle      |            Oracle               |
| SQLServer    |           Microsoft             |
|     DB2      |              IBM                |
| PostgreSQL   |           community             |
| MySQL        |       Oracle & community        |
| MariaDB      |       MariaDB & community       |

#### MPP

|    数据库     |                 公司            |
| ------------ | ------------------------------- |
|  Greenplum   |            Pivotal / DeepGreen  |
| Teradata     |           Teradata              |
| GBase 8a     |             南大通用             |
| HAWQ         |       Pivotal(SQL on Hadoop)    |
| Impala       |       Cloudera(SQL on Hadoop)   |
| Vertica      |          HP                     |

#### Hadoop  Ecosystem

|  大数据发行版  |              公司               |
| ------------ | ------------------------------- |
|    CDH       |            Cloudera             |
|    HDP       |            Hortonwork           |
|    MapR      |            MapR                 |
|    TDH       |            Transwarp            |
|    CRH       |            Redoop               |
|    XXX       |            Unknown              |

#### NoSQL

|   NoSQL系统   |              公司               |
| ------------ | ------------------------------- |
|    MongoDB   |        MongoDB Company          |
|    Hbase     |            Community            |
|    Cassandra |            DataStax             |
|   Hypertable |            Zvents               |
|   Accumulo   |            Community            |
| Elasticsearch|            Elastic              |

#### NewSQL

|  NewSQL系统   |              公司               |
| ------------ | ------------------------------- |
|    Spanner   |            Google Cloud         |
| CockroachDB  |   CockroachLabs & Community     |
|    TiDB      |   PingCAP  & Community          |
|   OceanBase  |            阿里巴巴              |
|   CrateDB    |         CrateDB & Community     |

虽然NoSQL因其性能、可伸缩性与可用性而广受赞誉，但其开发与数据重构的工作量要大于SQL存储。因此，有些人开始转向了NewSQL，它将NoSQL的优势与SQL的能力结合了起来。

* OLAP场景做到极致的Hadoop生态。
* OLTP场景的NewSQL数据库的发展。

![新型数据库](https://github.com/itweet/labs/raw/master/BigData/img/db_type.png)

各大云厂商也在大力发展支持OLTP的分布式金融级别的关系数据库，已解决MySQL分库分表难于管理的问题，底层直接提供分布式能力，而不用在业务层大动干戈，平滑迁移关系型单机数据库到分布式数据库集群，分布式以后提供弹性的伸缩能力，利用云端优势，发展基础软件即服务，帮助客户轻松应对海量数据多维度分析需求。

关于如今高速发展的数据引擎发展与详细设计细节，会通过`ITweet Talk`系列逐一介绍。

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/









