Clickhouse基本使用
---

今天，我们来简单测试一下clickhouse性能，通过测试学习clickhouse基本使用。

官方教程中有直接提供相关测试案例数据，跑一些场景，我选择了`OnTime`数据来做测试。

`OnTime`性能测试case由`Vadim Tkachenko`创建，安装官方文档操作。

## 下载测试数据

运行如Shell脚本，下载`1987-2017`所有On_Time数据。

```
for s in `seq 1987 2017`
do
for m in `seq 1 12`
do
wget http://transtats.bts.gov/PREZIP/On_Time_On_Time_Performance_${s}_${m}.zip
done
done
```

`Shell`地址：[download.sh](https://github.com/Percona-Lab/ontime-airline-performance/blob/master/download.sh)

## 命令行客户端

通过`clickhouse-client`命令，连接clickhouse-server进行相关的数据库操作。

```
clickhouse-client -h 127.0.0.1 -d default -m -u admin --password admin
```

如上，`-h`代表数据库IP地址，`-d`代表模式连接数据库，`-u`代表用户名，`--password`代码用户密码，`-m`允许运行多行查询。

### 创建表

clickhouse建表语言并非标准的SQL，看上去比较奇怪，因为它支持多种引擎，不同的Engine有不同的业务场景使用，其中某些是为了灵活或者临时的解决方案。官方文档`Roadmap`计划`Q3-Q4 2018`支持`ANSI SQL JOIN`语法，建表未来很长时间一直应该都这样吧，这就是Clickhouse最大的侧点。

学习Clickhouse，最主要的先学各种Engine的区别和联系，用来解决实际问题，在场景中探索。

由于它的各种设计，导致如果要使用分布式，那么需要使用local表和分布式表结合才能达到一个SQL过来分布式执行Query，请参考早期内容。

```
CREATE TABLE test.a_local (date Date, ……) ENGINE = MergeTree(date, (date, hour, datetime), 8192);

CREATE TABLE test.a_cluster (date Date, ……) ENGINE = Distributed(bip_ck_cluster, test ,a_local , rand());
```

创建一个test库，在进入库，创建一张`ontime_local`表，此表拥有`100`个字段，属于典型的大宽表，适合列式存储。

```
create database test;

use test;

CREATE TABLE `ontime_local` (
  `Year` UInt16,
  `Quarter` UInt8,
  `Month` UInt8,
  `DayofMonth` UInt8,
  `DayOfWeek` UInt8,
  `FlightDate` Date,
  `UniqueCarrier` FixedString(7),
  `AirlineID` Int32,
  `Carrier` FixedString(2),
  `TailNum` String,
  `FlightNum` String,
  `OriginAirportID` Int32,
  `OriginAirportSeqID` Int32,
  `OriginCityMarketID` Int32,
  `Origin` FixedString(5),
  `OriginCityName` String,
  `OriginState` FixedString(2),
  `OriginStateFips` String,
  `OriginStateName` String,
  `OriginWac` Int32,
  `DestAirportID` Int32,
  `DestAirportSeqID` Int32,
  `DestCityMarketID` Int32,
  `Dest` FixedString(5),
  `DestCityName` String,
  `DestState` FixedString(2),
  `DestStateFips` String,
  `DestStateName` String,
  `DestWac` Int32,
  `CRSDepTime` Int32,
  `DepTime` Int32,
  `DepDelay` Int32,
  `DepDelayMinutes` Int32,
  `DepDel15` Int32,
  `DepartureDelayGroups` String,
  `DepTimeBlk` String,
  `TaxiOut` Int32,
  `WheelsOff` Int32,
  `WheelsOn` Int32,
  `TaxiIn` Int32,
  `CRSArrTime` Int32,
  `ArrTime` Int32,
  `ArrDelay` Int32,
  `ArrDelayMinutes` Int32,
  `ArrDel15` Int32,
  `ArrivalDelayGroups` Int32,
  `ArrTimeBlk` String,
  `Cancelled` UInt8,
  `CancellationCode` FixedString(1),
  `Diverted` UInt8,
  `CRSElapsedTime` Int32,
  `ActualElapsedTime` Int32,
  `AirTime` Int32,
  `Flights` Int32,
  `Distance` Int32,
  `DistanceGroup` UInt8,
  `CarrierDelay` Int32,
  `WeatherDelay` Int32,
  `NASDelay` Int32,
  `SecurityDelay` Int32,
  `LateAircraftDelay` Int32,
  `FirstDepTime` String,
  `TotalAddGTime` String,
  `LongestAddGTime` String,
  `DivAirportLandings` String,
  `DivReachedDest` String,
  `DivActualElapsedTime` String,
  `DivArrDelay` String,
  `DivDistance` String,
  `Div1Airport` String,
  `Div1AirportID` Int32,
  `Div1AirportSeqID` Int32,
  `Div1WheelsOn` String,
  `Div1TotalGTime` String,
  `Div1LongestGTime` String,
  `Div1WheelsOff` String,
  `Div1TailNum` String,
  `Div2Airport` String,
  `Div2AirportID` Int32,
  `Div2AirportSeqID` Int32,
  `Div2WheelsOn` String,
  `Div2TotalGTime` String,
  `Div2LongestGTime` String,
  `Div2WheelsOff` String,
  `Div2TailNum` String,
  `Div3Airport` String,
  `Div3AirportID` Int32,
  `Div3AirportSeqID` Int32,
  `Div3WheelsOn` String,
  `Div3TotalGTime` String,
  `Div3LongestGTime` String,
  `Div3WheelsOff` String,
  `Div3TailNum` String,
  `Div4Airport` String,
  `Div4AirportID` Int32,
  `Div4AirportSeqID` Int32,
  `Div4WheelsOn` String,
  `Div4TotalGTime` String,
  `Div4LongestGTime` String,
  `Div4WheelsOff` String,
  `Div4TailNum` String,
  `Div5Airport` String,
  `Div5AirportID` Int32,
  `Div5AirportSeqID` Int32,
  `Div5WheelsOn` String,
  `Div5TotalGTime` String,
  `Div5LongestGTime` String,
  `Div5WheelsOff` String,
  `Div5TailNum` String
) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192);
```

创建分布式表结合本地表，使得Query能分布式执行。

```
CREATE TABLE ontime_all AS ontime_local ENGINE = Distributed(bip_ck_cluster, test, ontime_local, rand());
```

## 导入数据

进入到download数据目录，执行如下shell命令。

```
for i in *.zip; do echo $i; unzip -cq $i '*.csv' | sed 's/\.00//g' | clickhouse-client -h 127.0.0.1  -d default -m -u default --password admin --query="INSERT INTO ontime_local FORMAT CSVWithNames"; done
```

## 测试SQL

我使用VMware虚拟3台服务器，配置如下：

| CPU | Memory | Storage  | Cluster  | 操作系统  |
| :--- | :----: | ----: | ----: |----: |
| 2c | 15g | 180g |3 node |7.2.1511 (core)  |

一共`16`个SQL,来自官方的[`ontime`](https://clickhouse.yandex/docs/en/getting_started/example_datasets/ontime/)数据。

| 原始数据 | 入库数据 | 字段  | 数据量  | 表引擎  | 默认压缩  |
| :--- | :----: | ----: | ----: | ----: | ----: |
| 6.3g | 15g | 100 |177033339 | MergeTree | lz4 |

链接:https://pan.baidu.com/s/1F1vRFtf7rsxH3twhimb7DA  密码:x63k

![](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/onetime_clickhouse_histogram.png)

![](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/Clickhouse-OnTime-table.png)

如图，测试分三种情况，根据clickhouse自身的特点。

[1] local表，数据集中在一台机器，所有Query均发生在一体机器。
[2] cluster表，数据集中在一台机器，Query分布式执行，多台机器参与执行。
[3] all cluster表，数据集中在多台机器，Query分布式执行，多台机器参与执行。

注意：`生产环境，理想状态，数据集均衡分片到所有节点，每个节点local表存储部分数据，轮训写入多个节点的local表。`

通过测试我们能直观的看到，分布式表多机并行执行性能远高于`local`执行。Cluster和All Cluster区别不是很大，因为我的环境是在`虚拟机`，是一台服务器虚拟出3台搭建Clickhouse集群。

虽然在逻辑上为三台服务器，其实物理上都是跑在一台服务器和一块磁盘。

测试目的，熟悉clickhouse一些基本使用和原理，动手研究，深入理解clickhouse系统，不具备参考性；待有物理性能测试结果，在大肆总结一番。

我们可以看到，结果是clickhouse性能真的是没话说，SQL支持度和特殊语法使得它普及变得困难。如果希望变成一个大众化的`RDBMS System`，那还需要在SQL语法和兼容性中完成大量工作。

> ClickHouse is an open source column-oriented database management system capable of real time generation of analytical data reports using SQL queries.

官方`Roadmap`2018年计划，我们也能看到他们正在往这个方向靠近，成为一个标准的`RDBMS System.` 比如：`Initial support for UPDATE and DELETE`，`Store data at multiple disk volumes of a single server`，`ANSI SQL JOIN syntax`，`LDAP integration`。

我今天跑了一个100多个字段的大宽表，列式存储，单表各种复杂查询，性能都在秒级，在一些即席查询、聚合分析场景你可以使用clickhouse帮助你解决实际业务问题。

ClickHouse是OLAP领域，当之无愧的黑马，一骑绝尘.

![](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/Dark-horse.jpg)

## 推荐阅读

[1] 初识ClickHouse《First Time ClickHouse》

[2] Clickhouse快速上手

[3] MPP的进化 - 深入理解Batch和MPP优缺点

[4] Clickhouse基本使用


***参考：***

[1] https://clickhouse.yandex/docs/en/getting_started/example_datasets/ontime/
[2] https://www.percona.com/blog/2017/10/04/clickhouse-mysql-silicon-valley-meetup-oct-25-uber-engineering/
[3] https://www.percona.com/blog/author/vadim/
[4] https://clickhouse.yandex/docs/en/interfaces/cli/

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive