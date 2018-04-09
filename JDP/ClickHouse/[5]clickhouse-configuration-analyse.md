ClickHouse相关配置剖析
---

ClickHouse是一个分布式面向列的RDBMS系统，可以单机部署也可支持集群。目前支持Centos和Ubuntu系统的部署，并且有方和第三方都发布有RPM/DEB包，可直接安装使用。

**ClickHouse仓库和包下载**

Github:

- https://github.com/Yandex/ClickHouse
- https://github.com/Yandex/clickhouse-jdbc
- https://github.com/Yandex/clickhouse-odbc

Server Packages:

- Debian/Ubuntu: http://repo.yandex.ru/clickhouse/
- RPMs: https://packagecloud.io/altinity/clickhouse
    + Source: https://github.com/Altinity/clickhouse-rpm
- Docker: https://hub.docker.com/r/yandex/clickhouse-server/

Client Packages:

- https://hub.docker.com/r/yandex/clickhouse-client/
- JDBC: https://mvnrepository.com/artifact/ru.yandex.clickhouse/clickhouse-jdbc
- ODBC: https://github.com/yandex/clickhouse-odbc/releases

我们主要讨论ClickHouse相关配置文件，主要涉及三个：

* `config.xml` - 核心配置文件，记录节点信息和相关访问端口。
* `users.xml` - 针对client和server交互的用户权限、负载和配额信息。
* `metrika.xml` - 集群配置，主要记录集群数据分片和zookeeper信息。

`config.xml`涉及的几个核心配置信息，`logger`,各种`Port`，连接数，并发查询，数据存储路径，用户配置，集群配置文件，时区配置等。

```
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

`users.xml`设置权限、负载和配额，目前支持只读和读写控制，密码建议使用sha256加密，不建议使用明文。

```
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

`metrika.xml`集群配置，主要记录集群数据分片和zookeeper信息,分片和副本决定了集群的容错和高可靠。

```
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

集群中clickhouse_remote_servers配置涉及数据分片,如果使用了分布式表，需要在集群的配置文件里，增加分片的用户名密码。

涉及完整的配置信息：

- config.xml - https://github.com/jikelab/ClickHouse/blob/master/dbms/src/Server/config.xml
- users.xml - https://github.com/jikelab/ClickHouse/blob/master/dbms/src/Server/users.xml

有关集群配置，在config.xml中有相关说明，这里就不单独列出来了。

为了更加简化管理集群和配置，降低成本，我开发了一个针对ClickHouse相关的自动化运维可扩展的工具，可视化的完成集群运维和配置管理。

正在进行Clickhouse的所有配置指标梳理，在可视化界面进行配置管理和安装，配置版本回滚。

关于安装包

> 介绍了clickhouse支持的相关系统包，还有周边配套的软件和资源列表。

关于配置文件

> 未来会推出一个完全自动化管理和安装的可视化工具，是一套针对ClickHouse生态的一揽子方案，正在努力调试中，so，导致没时间更新文章。

关于数据产品

> 完全OpenSource的方式发布,是一个综合性的产品，定位解决企业核心的OLAP和OLTP大多数场景。

关于ClickHouse数据产品，我会慢慢更新，尽请期待...

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive