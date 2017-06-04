hive1性能和hive2支持Llap的性能比较
---

### 环境

#### 硬件
- CPU ： 24
- 内存：128G
- 磁盘：300g*5/台

#### 网络
- 千兆网络 1G/S

#### 系统
- CentOS Linux release 7.2.1511 (Core) 

#### 软件
- Redoop CRH 5.0
- Hive 2.1 with LLAP
- Hive 1.2.1 with Tez 7.0
- Hadoop 2.7.3
- Tez 0.7.0
- Spark1 1.6.3
- Saprk2 2.1.0  

#### 数据量
- 266.7 G 大小的ORCFile
- 916.7 G 大小的TextFile
- 生成24张表

注：数据通过`TPC-DS`提供的数据生成程序生成1TB的TextFile，再通过这1TB文件生成ORC文件格式同样的表。

#### 资源分配

- Yarn 
    +  Memory Total：452.50 GB
    +  VCores Total：95
    +  nodeManager：5 node  
    +  resourceManager：1 node

- HDFS
    + NameNode Java heap size: 11GB
    + DataNode maximum Java heap size: 6GB
    + NameNode: 1 node
    + DataNode: 5 node

- Hive JDBC 
    
    + Hive1: beeline --hiveconf hive.execution.engine=tez -u 'jdbc:hive2://bigdata-server-3:2181,bigdata-server-1:2181,bigdata-server-2:2181/tpcds_bin_partitioned_orcfile_1000;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2' -n hive
    
    + Hive2:beeline --hiveconf hive.execution.engine=tez -u 'jdbc:hive2://bigdata-server-3:2181,bigdata-server-1:2181,bigdata-server-2:2181/tpcds_bin_partitioned_orcfile_1000;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2-hive2' -n hive 

- Spark JDBC
    + beeline -u 'jdbc:hive2://bigdata-server-1:10016/tpcds_bin_partitioned_orcfile_1000' -n spark 
    
    + /usr/hdp/current/spark2-client/bin/spark-sql --master yarn-client --conf spark.driver.memory=10G --conf spark.driver.cores=1 --conf spark.executor.memory=8G --conf spark.driver.cores=1 --conf spark.executor.cores=2  --conf spark.shuffle.service.enabled=true --conf spark.dynamicAllocation.enabled=true --conf spark.dynamicAllocation.minExecutors=1 --conf spark.dynamicAllocation.maxExecutors=114 --database tpcds_bin_partitioned_orcfile_1000 -f sample-queries-tpcds/query98.sql 

### Comparing Hive with LLAP to Hive on Tez

python Hadoopdb-tpcds-test.py spark tpcds_bin_partitioned_orcfile_1000


### hawq install 



欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)


