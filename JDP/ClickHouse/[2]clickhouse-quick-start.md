Clickhouse快速上手
---

Clickhouse优雅的设计，超高的性能，让我忍不住想深入研究。边研究边总结，今天，我们介绍一下clickhouse快速上手，全文涉及一些具体配置，内容略多，主要介绍几种主要的安装方式。

- 单机安装
- 容器安装
- 集群安装

由于目前官方没有提供RPM，默认只提供Deb包。当然也有第三方机构提供RPM包，国内主要使用CentOS/RedHat系，所以方便了很多。

> ClickHouse is an open-source column-oriented database management system.

## ClickHouse快速启动

### Ubuntu/Debian安装

```
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv E0C56BD4    # optional

sudo apt-add-repository "deb http://repo.yandex.ru/clickhouse/deb/stable/ main/"
sudo apt-get update

sudo apt-get install clickhouse-server-common clickhouse-client -y

sudo service clickhouse-server start
clickhouse-client
```

单机的安装部署，很简单，安装上基本就可以启动体验它的强大功能，你会发现clickhouse单机性能也很强。对于其他操作系统，最简单的使用方式是官方提供的[Clickhouse Docker images](https://hub.docker.com/r/yandex/clickhouse-server/)。或者通过官方文档源码构建Clickhouse。

### Docker安装

官方Docker镜像提供也是基于Ubuntu之上的，Docker提供强大的底层系统兼容性，所以基本在任何能安装启动Docker系统之上都可以运行clickhouse，官方提供的docker镜像，也提供`docker file`，可以根据自己的需要进行定制化，由于官方镜像默认监听得是IPV6地址，可能启动无法正常使用，可以进入容器修改相关配置项，方可正常使用。

#### 启动clickhouse-server实例

```
$ docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 yandex/clickhouse-server
```

#### clickhouse-client连接

```
$ docker run -it --rm --link some-clickhouse-server:clickhouse-server yandex/clickhouse-client --host clickhouse-server
```

关于[ClickHouse client](https://clickhouse.yandex/docs/en/interfaces/cli/)

#### 快速体验

```
CREATE TABLE ontime_local (FlightDate Date,Year UInt16) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192);

insert into ontime_local (FlightDate,Year) values('2001-10-12',2001);

select count(*) from ontime_local;
```

如何？是否感觉怪怪的，ENGINE是啥？我们慢慢理解，它的语法如此。

#### ClickHouse容器配置

容器需要公开用于HTTP通信的`8123`端口和用于主机间通信的`9000`端口。

ClickHouse的配置文件"config.xml"([documentation](https://clickhouse.yandex/docs/en/operations/configuration_files/))

使用自定义配置启动clickhouse-server实例

```
$ docker run -d --name some-clickhouse-server --ulimit nofile=262144:262144 -v /path/to/your/config.xml:/etc/clickhouse-server/config.xml yandex/clickhouse-server
```

注意：`这里有docker的知识，挂载了一个宿主机的配置文件替代容器中的默认配置，实现自定义配置`

### Clickhouse Dockerfile

通过自定义Dockerfile制作基于其他系统的Docker Imange，可以自学docker的知识。

```
FROM ubuntu:16.04

ARG repository="deb http://repo.yandex.ru/clickhouse/deb/stable/ main/"
ARG version=\*

RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    mkdir -p /etc/apt/sources.list.d && \
    echo $repository | tee /etc/apt/sources.list.d/clickhouse.list && \
    apt-get update && \
    apt-get install --allow-unauthenticated -y clickhouse-server-common=$version clickhouse-server-base=$version && \
    rm -rf /var/lib/apt/lists/* /var/cache/debconf && \
    apt-get clean

COPY docker_related_config.xml /etc/clickhouse-server/config.d/
RUN chown -R clickhouse /etc/clickhouse-server/

USER clickhouse
EXPOSE 9000 8123 9009
VOLUME /var/lib/clickhouse

ENV CLICKHOUSE_CONFIG /etc/clickhouse-server/config.xml

ENTRYPOINT exec /usr/bin/clickhouse-server --config=${CLICKHOUSE_CONFIG}
```

快速启动介绍了基于deb的安装方式以及容器化的安装方式，单机的话足够使用和体验clickhouse功能，基于rpm安装方式类似，集群版安装会介绍RPM安装。

如果在生产使用，都是冲着集群功能来的，接下来介绍一下集群的安装。

## ClickHouse集群安装

既然，都是冲着集群来的，我们就介绍一下集群的安装，其实也很简单。

### 环境准备

我使用VMware虚拟3台服务器，配置如下：

| CPU | Memory | Storage  | Cluster  | 操作系统  |
| :--- | :----: | ----: | ----: |----: |
| 2c | 15g | 180g |3 node |7.2.1511 (core)  |

### 准备数据

通过官方提供的Testing data，我们使用[`OnTime`](https://clickhouse.yandex/docs/en/getting_started/example_datasets/ontime/)数据进行测试。

| 原始数据 | 入库数据 | 字段  | 数据量  | 表引擎  | 默认压缩  |
| :--- | :----: | ----: | ----: | ----: | ----: |
| 6.3g | 15g | 100 |177033339 | MergeTree | lz4 |

### 安装集群

集群安装之前，必须先准备好一个正常可用的zookeeper集群，因为在使用集群和复制表的时候会用到。

接下来，假设已经具备zookeeper集群环境。

| IP | 用户 | 密码  | 主机名 | 操作系统  |
| :--- | :----: | ----: | ----: |----: |
| 192.168.0.113-115 | root | node{1..3} | 具备 | 7.2.1511 (core)  |

操作系统`7.2.1511 (core)以上，安装顺利。

#### 基础环境准备

[1] 修改hostname和hosts && 关闭selinux && 关闭firewalld

所有主机，修改hosts

```
$ tail -3 /etc/hosts

192.168.0.113   node1.jikelab.com   node1
192.168.0.114   node2.jikelab.com   node2
192.168.0.115   node3.jikelab.com   node3
```

所有主机，关闭Selinux

```
$ sudo sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
setenforce 0

$ sudo grep SELINUX=disabled /etc/selinux/config
```

所有主机，关闭firewalld

```
$ sudo systemctl stop firewalld
$ sudo systemctl disable firewalld
```

[2] 打开最大文件数

所有主机操作

```
vi /etc/security/limits.d/clickhouse.conf

clickhouse      soft    nofile  262144
clickhouse      hard    nofile  262144
```

### 安装clickhouse

[1] 准备YUM源

```
yum install -y yum-utils

yum-config-manager --add-repo http://repo.red-soft.biz/repos/clickhouse/repo/clickhouse-el7.repo

yum install -y clickhouse-server clickhouse-client clickhouse-server-common clickhouse-compressor
```

使用第三方提供的clickhouse的yum源仓库，相比之前要在RedHat/CentOS系统安装都需要自己源码构建安装方便很多。

[2] 安装clickhouse

```
yum install -y clickhouse-server clickhouse-client clickhouse-server-common clickhouse-compressor

Installed:
  clickhouse-client.x86_64 0:1.1.54236-4.el7
  clickhouse-compressor.x86_64 0:1.1.54236-4.el7
  clickhouse-server.x86_64 0:1.1.54236-4.el7
  clickhouse-server-common.x86_64 0:1.1.54236-4.el7

Dependency Installed:
  libicu.x86_64 0:50.1.2-15.el7          libtool-ltdl.x86_64 0:2.4.2-22.el7_3
  unixODBC.x86_64 0:2.3.1-11.el7

```

如上，clickhous几乎没有什么依赖，系统非常干净。

[3] 修改配置文件

方便管理，我们把日志、配置文件都存储到一个统一的根路径。

首先修改`/etc/rc.d/init.d/clickhouse-server`文件。

```
CLICKHOUSE_LOGDIR=/data/clickhouse/log
CLICKHOUSE_DATADIR_OLD=/data/clickhouse/data_old
CLICKHOUSE_CONFIG=/data/clickhouse/config.xml
```

`CLICKHOUSE_DATADIR_OLD`为兼容老版本，新版本已经弃用。

> 修改最核心配置文件`config.xml`。

```
$ vi /data/clickhouse/config.xml

<?xml version="1.0"?>
<yandex>
    <logger>
        <level>trace</level>
        <log>/data/clickhouse/log/server.log</log>
        <errorlog>/data/clickhouse/log/error.log</errorlog>
        <size>1000M</size>
        <count>10</count>
    </logger>

    <!-- For HTTPS over native protocol. -->
    <!--
    <https_port>8443</https_port>
    -->
    <http_port>8123</http_port>
    <tcp_port>9000</tcp_port>

    <!-- Port for communication between replicas. Used for data exchange. -->
    <interserver_http_port>9009</interserver_http_port>

    <!-- 本机域名 -->
    <interserver_http_host>node1.jikelab.com</interserver_http_host>
    
    <!-- 监听IP -->
    <listen_host>0.0.0.0</listen_host>
    
    <!-- 最大连接数 -->
    <max_connections>64</max_connections>
    
    <!-- 没搞懂的参数 -->
    <keep_alive_timeout>3</keep_alive_timeout>
    
    <!-- 最大并发查询数 -->
    <max_concurrent_queries>16</max_concurrent_queries>
   
    <!-- 单位是B -->
    <uncompressed_cache_size>8589934592</uncompressed_cache_size>
    <mark_cache_size>10737418240</mark_cache_size>
   
    <!-- 存储路径 -->
    <path>/data/clickhouse/</path>
    <tmp_path>/data/clickhouse/tmp/</tmp_path>
    
    <!-- user配置 -->
    <users_config>users.xml</users_config>
    
    <default_profile>default</default_profile>
    
    <log_queries>1</log_queries>

    <default_database>default</default_database>

     <!-- Configuration of clusters that could be used in Distributed tables.
         https://clickhouse.yandex/docs/en/table_engines/distributed/
      -->
    <remote_servers incl="clickhouse_remote_servers" />

    <zookeeper incl="zookeeper-servers" optional="true" />

     <!-- Substitutions for parameters of replicated tables.
          Optional. If you don't use replicated tables, you could omit that.
         See https://clickhouse.yandex/docs/en/table_engines/replication/#creating-replicated-tables
      -->
    <macros incl="macros" optional="true" />
     
     <!-- Reloading interval for embedded dictionaries, in seconds. Default: 3600. -->
    <builtin_dictionaries_reload_interval>3600</builtin_dictionaries_reload_interval>

    <!-- 控制大表的删除 -->
    <max_table_size_to_drop>0</max_table_size_to_drop>

    <!-- 集群配置文件 -->
    <include_from>/data/clickhouse/metrika.xml</include_from>
</yandex>
```

需要注意`interserver_http_host`配置每个主机都不同，，其他配置保持一致，建议使用域名映射，方便数据入库的时候轮训写入各节点均衡数据。

> 修改集群的配置文件`metrika.xml`。

```
$ vi /data/clickhouse/metrika.xml

<?xml version="1.0"?>
<yandex>
<!-- 集群配置 -->
<clickhouse_remote_servers>
    <bip_ck_cluster>
        <!-- 数据分片1  -->
        <shard>
            <internal_replication>false</internal_replication>
            <replica>
                <host>node1.jikelab.com</host>
                <port>9000</port>
                <user>default</user>
                <password>6lYaUiFi</password>
            </replica>
        </shard>
        <!-- 数据分片2  -->
        <shard>
            <internal_replication>false</internal_replication>
            <replica>
                <host>node2.jikelab.com</host>
                <port>9000</port>
                <user>default</user>
                <password>6lYaUiFi</password>
            </replica>
        </shard>
        <!-- 数据分片3  -->
        <shard>
            <internal_replication>false</internal_replication>
            <replica>
                <host>node3.jikelab.com</host>
                <port>9000</port>
                <user>default</user>
                <password>6lYaUiFi</password>
            </replica>
        </shard>
    </bip_ck_cluster>
</clickhouse_remote_servers>
<!-- 本节点副本名称，创建复制表时有用，每个节点不同，整个集群唯一，建议使用主机名） -->
<macros>
    <replica>node1</replica>
</macros>
<!-- 监听网络 -->
<networks>
   <ip>::/0</ip>
</networks>
<!-- ZK集群  -->
<zookeeper-servers>
  <node index="1">
    <host>192.168.0.245</host>
    <port>2181</port>
  </node>
  <node index="2">
    <host>192.168.0.246</host>
    <port>2181</port>
  </node>
  <node index="3">
    <host>192.168.0.247</host>
    <port>2181</port>
  </node>
</zookeeper-servers>
<!-- 数据压缩算法  -->
<clickhouse_compression>
<case>
  <min_part_size>10000000000</min_part_size>
  <min_part_size_ratio>0.01</min_part_size_ratio>
  <method>lz4</method>
</case>
</clickhouse_compression>
</yandex>
```

如上集群配置，所有节点配置一致，比较关键的是zookeeper和`macros(此配置，每个节点必须不一致，在集群需保持唯一性，建议使用主机名或递增字符串)`配置，集群中clickhouse_remote_servers配置涉及数据分片,如果使用了分布式表，需要在集群的配置文件里，增加分片的用户名密码，关于配置文件我们需要单独一节介绍剖析配置。

> 修改users.xml配置，设置权限、负载和配额。

```
$ vi /data/clickhouse/users.xml 

<?xml version="1.0"?>
<yandex>
    <profiles>
        <!-- 读写用户设置  -->
        <default>
            <max_memory_usage>10000000000</max_memory_usage>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>random</load_balancing>
        </default>
        <!-- 只写用户设置  -->
        <readonly>
            <max_memory_usage>10000000000</max_memory_usage>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>random</load_balancing>
            <readonly>1</readonly>
        </readonly>
    </profiles>
    <!-- 配额  -->
    <quotas>
        <!-- Name of quota. -->
        <default>
            <interval>
                <duration>3600</duration>
                <queries>0</queries>
                <errors>0</errors>
                <result_rows>0</result_rows>
                <read_rows>0</read_rows>
                <execution_time>0</execution_time>
            </interval>
        </default>
    </quotas>
    <users>
        <!-- 读写用户  -->
        <default>
            <password_sha256_hex>967f3bf355dddfabfca1c9f5cab39352b2ec1cd0b05f9e1e6b8f629705fe7d6e</password_sha256_hex>
            <networks incl="networks" replace="replace">
                <ip>::/0</ip>
            </networks>
            <profile>default</profile>
            <quota>default</quota>
        </default>
        <!-- 只读用户  -->
        <ck>
            <password_sha256_hex>967f3bf355dddfabfca1c9f5cab39352b2ec1cd0b05f9e1e6b8f629705fe7d6e</password_sha256_hex>
            <networks incl="networks" replace="replace">
                <ip>::/0</ip>
            </networks>
            <profile>readonly</profile>
            <quota>default</quota>
        </ck>
    </users>
</yandex>
```

有关配置文件，我们专门用一节介绍，这里就不过多叙述，不然篇幅太长。

[4] 创建相关目录
```
mkdir -p /data/clickhouse/log
mkdir -p /data/clickhouse
chown -R clickhouse:clickhouse /data/clickhouse
```

[5] 启动集群

```
service clickhouse-server start
```

例如：

```
[root@node1 clickhouse]# lsof -i :8123
COMMAND     PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
clickhous 13180 clickhouse   12u  IPv4  54805      0t0  TCP *:8123 (LISTEN)
[root@node1 clickhouse]# lsof -i :9000
COMMAND     PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
clickhous 13180 clickhouse   13u  IPv4  54806      0t0  TCP *:cslistener (LISTEN)
```

[6] clickhouse client

使用clickhouse client连接集群某节点，开启clickhouse之旅。

```
clickhouse-client -h 127.0.0.1 -d default -m -u default --password 6lYaUiFi

:) use system;

:) select * from clusters;

SELECT *
FROM clusters

┌─cluster────────┬─shard_num─┬─shard_weight─┬─replica_num─┬─host_name─────────┬─host_address──┬─port─┬─is_local─┬─user────┬─default_database─┐
│ bip_ck_cluster │         1 │            1 │           1 │ node1.jikelab.com │ 192.168.0.113 │ 9000 │        1 │ default │                  │
│ bip_ck_cluster │         2 │            1 │           1 │ node2.jikelab.com │ 192.168.0.114 │ 9000 │        0 │ default │                  │
│ bip_ck_cluster │         3 │            1 │           1 │ node3.jikelab.com │ 192.168.0.115 │ 9000 │        0 │ default │                  │
└────────────────┴───────────┴──────────────┴─────────────┴───────────────────┴───────────────┴──────┴──────────┴─────────┴──────────────────┘

3 rows in set. Elapsed: 0.003 sec.

```

如上，进入系统system库，查看集群状态。

[7] 创建clickhouse表和库

```
CREATE TABLE ontime_local (FlightDate Date,Year UInt16) ENGINE = MergeTree(FlightDate, (Year, FlightDate), 8192);

CREATE TABLE ontime_all AS ontime_local ENGINE = Distributed(bip_ck_cluster, default, ontime_local, rand());

insert into ontime_local (FlightDate,Year)values('2001-10-12',2001);

insert into ontime_local (FlightDate,Year)values('2002-10-12',2002);

insert into ontime_local (FlightDate,Year)values('2003-10-12',2003);

insert into ontime_all (FlightDate,Year)values('2003-10-12',2008);

select count(*) from ontime_all;
```

如上创建了一张本地表，创建一张分布式表去关联本地表，这样就可以在全局查询到数据。

- 因为clickhouse数据都存储在本地表或者复制表，分布式表仅仅是请求转发，执行是在各节点的本地表执行，所以并不是真正的分布式。
- 建议所有数据写入本地表，轮训写各个节点本地表，通过查询分布式表来在全局进行查询汇总数据。
- 由于clickhouse元数据信息不同步，其实也不应该同步，因为clickhouse本来就不是真正意义上的分布式，全都是用户控制，如果你要查询使用分布式表，必须在所有节点或部分节点创建`local`表，在每个节点创建一张`Distributed`表关联，只要查询分布式表即可查询所有节点数据。
- 复制表，解决单副本故障问题，通过复制表可以保障节点损坏也不丢数据。
- 由于分布式表只是简单解析SQL下发到具体节点去执行，最后汇总，避免写`Distributed`表造成数据不均衡，所以用户自己控制轮训写本地表控制数据均衡。

## 小结

[1] 目前遇到的一个问题，数据目录不能写多快盘，只能写一块，让我有点怀疑官网宣传，单节点几十TB数据，按照目前情况只能做raid5，所有数据盘融在一起，IO无法隔离，多查询并发是否会有问题？

[2] 好消息是，只能读写一个数据目录，官方打算今年`2018 Q2`解决。

```
Store data at multiple disk volumes of a single server.

That will make it easier to extend disk system as well as use different disk systems for different DBs or tables. Currently, users have to use symlinks if DB/table needs to be stored in another volume.
```

[3] 复制表一直没搞明白，如果复制表+分布式表解决数据高可靠问题，但是操作过程会出现重复数据，比较奇怪。

[4] 由于不是真正的分布式，各节点元数据独立，通过分布式表关联在一起，clickhouse把个节点当做一个个单独的库和表，通过不携带任何数据的分布式表把他们联系一起工作，提供单机的条件下推执行，在汇总。

[5] 由于提供了一个http端口，刚开始安装成功，我单独去访问了一下，显示`ok`，我以为我安装问题，多方打探，原来没问题，囧.

[6] Q1 2018将支持Update/Delete功能。

[7] 为何如此高效率？确实测试结果非常快，上一篇我们有介绍并且百度云盘放了测试结果文件，仅仅从目前了解的来看，实现上面分布式还有很多工作要完成，比较简陋，有点难以置信为何如此快，作者的设计哲学和核心理念一直没公布，很神秘。

[8] 各种不同的引擎，对表的创建和使用有比较大影响，建议熟读文档，多动手实践，了解清楚在使用。

关于第一次使用clickhouse

> 我创建了一个库和表，发现其他节点无法查询到，让我非常困惑，各种咨询打探，怀疑集群模式没安装成功，之后发现根本就没有元数据同步功能，每个节点维护自己的元数据，分布式数据库目前都没这么玩的吧。没有全局元数据概念，这设计，这脑洞。

关于元数据

> 目前MPP架构集群，无法超过50个节点，因为元数据信息同步和磁盘，限制集群扩展和性能。Impala分布式SQL on Hadoop架构，通过pub/sub方式同步元数据，如果在某个机器创建表，如果在其他机器需要查询到，必须先执行刷新元数据信息的。也比较坑，频繁刷新还会导致系统性能急剧下降，这是impala系统实现问题，点到为止。所以分布式元数据一致性、每个节点保留一份元数据，需同步。或者统一集中某个节点，跨网络，加载延迟，单点都是问题，所以每个系统都是设计来解决某方面问题，不存在完美的系统。不同的系统设计，有不同的权衡，也会有各种优劣。

关于clickhouse专题

> 我会慢慢完善我对clickhouse的理解，写一些更深入和具体的内容，今年计划，死磕分布式数据库技术。

未来，一篇介绍Clickhouse基本使用、性能、导数。

## 推荐阅读

[1] 初识ClickHouse《First Time ClickHouse》

[2] 大规模数据处理的演变(2003-2017)

[3] Apache Impala 性能优化

[4] 数据仓库：过去、现在和未来

***参考：***

[1] https://clickhouse.yandex/#quick-start
[2] https://hub.docker.com/r/yandex/clickhouse-server
[3] https://clickhouse.yandex/docs/en/development/build.html
[4] https://github.com/red-soft-ru/clickhouse-rpm
[5] http://jackpgao.github.io/2017/12/13/ClickHouse-Cluster-Beginning-to-End/
[6] https://clickhouse.yandex/docs/en/roadmap/

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive