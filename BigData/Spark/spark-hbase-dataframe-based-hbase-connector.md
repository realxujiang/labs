SPARK-ON-HBASE：基于HBASE连接器的DataFrame
---

我们非常高兴的宣告由Hortonworks和Bloomberg合作开发完成的[Spark-HBase](https://github.com/hortonworks/shc.git) 连接器技术预览版的发行。

Spark-HBase连接器利用Spark-1.2.0引入[Data Source API](https://databricks.com/blog/2015/01/09/spark-sql-data-sources-api-unified-data-access-for-the-spark-platform.html)（[SPARK-3247](https://issues.apache.org/jira/browse/SPARK-3247)）。它弥合了简单的HBase Key Value和复杂关联SQL查询之间的差距，使得用户可以在HBase上使用Spark执行复杂的数据分析。HBase DataFrame是一个标准的Spark DataFrame，它可以和任何其他数据源（例如Hive，ORC，Parquet，JSON等）进行交互。

### 背景

有些开源Spark HBase连接器可用作Spark软件包、独立项目包或HBaseTrunk。

Spark已经转移到提供内置的查询计划优化Dataset / DataFrame APIs。 现在，终端用户更喜欢使用基于界面的DataFrames / Datasets。

Hbase Trunk（端口汇聚）中的HBase连接器得到大量RDD支持。例如BulkPut等。但它的DataFrame支持就没那么多了。依靠标准HadoopRDD和内置TableInputFormat的HBaseTrunk连接器有一些性能限制。此外，在驱动程序中执行的BulkGet可能出现单点故障。

还有一些其他可选的执行方法，以Spark-SQL-on-HBase为例。[Spark-SQL-on-Hbase](https://github.com/Huawei-Spark/Spark-SQL-on-HBase)通过在标准的Spark Catalyst引擎中内嵌查询优化计划，传送RDD到HBase使用高级自定义优化技术执行复杂的任务。例如在HBase协处理器内部的部分聚合。这种方法能够实现高性能，但由于其复杂性和Spark的快速发展难以维持高性能。这种方法还允许任意代码在协处理器内运行，但是可能会产生安全隐患。

开发Spark-on-HBase连接器（SHC）是为了克服潜在的瓶颈和弱点。该连接器实现了标准的Spark Datasource API，并利用Spark Catalyst引擎进行查询优化。同时为了实现高性能，RDD是从头开始构建而不是使用TableInputFormat。通过这种定制的RDD，可以完全应用和实现所有关键技术，例如分区修剪，列修剪，谓词下推和数据局部性等技术。该设计不仅使维护变得简单，同时在性能和简单性之间达到了良好的平衡。

### 体系架构

我们假设Spark和HBase都部署在同一个集群中，而Spark执行器与region server位于同一位置，如下图所示。
![](https://github.com/itweet/labs/raw/master/BigData/img/age.png)
**图1. Spark-on-HBase连接器的体系架构**

连接器以类似的方式对Scan和Get进行了高级别处理，这两种操作都在Executors中执行。Driver处理查询，并基于区域元数据聚合Scan/gets，然后为每个区域生成任务。这些任务被发送到与region server同一位置的首选执行器上，并且在执行器中并行执行实现更好的数据局部性和并发性。如果某个区域不存在所需的数据，则该region server将不分配任何任务。一个任务可能由多个扫描和BulkGets组成，并且一个任务的数据请求只能从一个region server检索，该region server将为了该项任务的局部性优先。请注意，除了调度任务之外，驱动程序不涉及任何真正的作业执行。 这样可以避免驱动程序发生瓶颈问题。

### TABLE CATALOG

为了将HBase表作为关系表引入Spark，我们定义了HBase和Spark表之间的映射，称为Table Catalog。这个目录有两个关键部分。一个是行键定义，另一个是Spark中的表列与HBase中的列族和列限定符之间的映射。有关详细信息，请参阅使用部分。

### 本地支持AVRO

连接器本身支持Avro格式，因此将结构化数据作为字节数组保存到HBase中是非常常见的做法。用户可以直接将Avro记录保存到HBase中。 并在Avro架构内部把Avro记录自动转换为本地Spark Catalyst数据类型。请注意，HBase表中的两个键值部分都可以定义为Avro格式。 请参阅repo中的示例/测试用例获得准确的用法。

### 谓词下推

为了减少网路负载连接器仅从region server检索所需的列，并避免Spark Catalyst引擎中的冗余处理。现有的标准HBase过滤器用于执行谓词下推，就无需使用协处理器功能。由于HBase不知道字节数组之外的数据类型，并且Java基本类型和字节数组之间的顺序不一致，所以在扫描操作中设置过滤器之前，必须对过滤条件进行预处理，以避免任何数据丢失。在region server中，不符合查询条件的记录都将被过滤掉。

### 分区修剪

通过从谓词提取行键，我们将Scan / BulkGet拆分成多个非重叠的范围，只有具有请求数据的region server才能执行Scan/ BulkGet。目前，分区修剪是在行键的第一维度上执行。例如，如果行键为“key1：key2：key3”，则分区修剪将仅基于“key1”。 请注意，WHERE条件需要仔细定义。 否则，分区修剪可能不会生效。例如，WHERE rowkey1>“abc”OR column =“xyz”（其中rowkey1是rowkey的第一个维度，列是常规的HBase列）将发生在整个扫描过程中，，因为 OR逻辑规定我们必须涵盖所有的行列范围。

### 数据局部性

当Spark执行器与Hbase region server位于同一位置时，该执行器通过识别region server位置实现数据局部性、并尽可能与region server共同部署任,每个执行器对位于同一主机上的部分数据执行Scan/BulkGet 。

### SCAN AND BULKGET

Scan和BulkGet这两个操作符通过指定WHERE CLAUSE接触用户，例如WHERE column > x和column < y 用于扫描，WHERE column = x 用于获取。这些指定操作在执行器中执行，驱动程序仅用于创建这些操作。这两种操作符在内部被转换为扫描和获取、扫描/或者获取，而Iterator [Row]返回到catalyst引擎用于上层处理。

### 用法

以下是如何使用连接器基本步骤的说明。有关更多详细信息和高级用例，例如Avro和复合密钥支持，请参阅存储库中的[示例](https://hortonworks.com/hadoop-tutorial/spark-hbase-dataframe-based-hbase-connector/)。

** 1）定义架构映射的目录：

```
def catalog = s"""{
         |"table":{"namespace":"default", "name":"table1"},
         |"rowkey":"key",
         |"columns":{
           |"col0":{"cf":"rowkey", "col":"key", "type":"string"},
           |"col1":{"cf":"cf1", "col":"col1", "type":"boolean"},
           |"col2":{"cf":"cf2", "col":"col2", "type":"double"},
           |"col3":{"cf":"cf3", "col":"col3", "type":"float"},
           |"col4":{"cf":"cf4", "col":"col4", "type":"int"},
           |"col5":{"cf":"cf5", "col":"col5", "type":"bigint"},
           |"col6":{"cf":"cf6", "col":"col6", "type":"smallint"},
           |"col7":{"cf":"cf7", "col":"col7", "type":"string"},
           |"col8":{"cf":"cf8", "col":"col8", "type":"tinyint"}
         |}
       |}""".stripMargin
```

** 2）准备填入HBase表的数据：

```
case class HBaseRecord(col0: String, col1: Boolean,col2: Double, col3: Float,col4: Int,       col5: Long, col6: Short, col7: String, col8: Byte)

object HBaseRecord {def apply(i: Int, t: String): HBaseRecord = { val s = s”””row${“%03d”.format(i)}”””       HBaseRecord(s, i % 2 == 0, i.toDouble, i.toFloat,  i, i.toLong, i.toShort,  s”String$i: $t”,      i.toByte) }}

val data = (0 to 255).map { i =>  HBaseRecord(i, “extra”)}

sc.parallelize(data).toDF.write.options(
 Map(HBaseTableCatalog.tableCatalog -> catalog, HBaseTableCatalog.newTable -> “5”))
 .format(“org.apache.spark.sql.execution.datasources.hbase”)
 .save()
```

** 3）加载DataFrame：

```
def withCatalog(cat: String): DataFrame = {
 sqlContext
 .read
 .options(Map(HBaseTableCatalog.tableCatalog->cat))
 .format(“org.apache.spark.sql.execution.datasources.hbase”)
 .load()
}

val df = withCatalog(catalog)
```

** 4）语言集成查询：

```
val s = df.filter((($”col0″ <= “row050″ && $”col0” > “row040”) ||
 $”col0″ === “row005” ||
 $”col0″ === “row020” ||
 $”col0″ ===  “r20” ||
 $”col0″ <= “row005”) &&
 ($”col4″ === 1 ||
 $”col4″ === 42))
 .select(“col0”, “col1”, “col4”)
s.show
```

** SQL查询：

```
df.registerTempTable(“table”)
sqlContext.sql(“select count(col1) from table”).show
```


### 配置SPARK包

用户可以使用Spark-on-HBase连接器作为标准Spark软件包。 要在Spark应用程序中加入该包，请使用：

```
spark-shell, pyspark, or spark-submit
> $SPARK_HOME/bin/spark-shell –packages zhzhan:shc:0.0.11-1.6.1-s_2.10
```

用户还可以把Spark软件包附加在SBT文件中， 格式为： spark-package-name:version

```
spDependencies += “zhzhan/shc:0.0.11-1.6.1-s_2.10”
```

### 在安全的集群中的运行

在运行Kerberos授权的集群时，用户必须将HBase相关的jar包含到类路径中，因为Spark不依靠连接器就可以完成HBase令牌检索和更新。换句话说，无论是通过kinit还是通过提供委托人/秘钥表，用户必需要以正常方式启动环境。以下示例显示了如何在安全的集群中运行 yarn-client和 yarn-cluster模式。请注意，必须为这两种模式设置SPARK_CLASSPATH，而示例jar只是Spark的占位符。

```
export SPARK_CLASSPATH=/usr/hdp/current/hbase-client/lib/hbase-common.jar:/usr/hdp/current/hbase-client/lib/hbase-client.jar:/usr/hdp/current/hbase-client/lib/hbase-server.jar:/usr/hdp/current/hbase-client/lib/hbase-protocol.jar:/usr/hdp/current/hbase-client/lib/guava-12.0.1.jar
```

假设hrt_qa是一个无头帐号，用户可以使用以下命令进行kinit：

```
kinit -k -t /tmp/hrt_qa.headless.keytab hrt_qa

/usr/hdp/current/spark-client/bin/spark-submit –class org.apache.spark.sql.execution.datasources.hbase.examples.HBaseSource –master yarn-client –packages zhzhan:shc:0.0.11-1.6.1-s_2.10 –num-executors 4 –driver-memory 512m –executor-memory 512m –executor-cores 1 /usr/hdp/current/spark-client/lib/spark-examples-1.6.1.2.4.2.0-106-hadoop2.7.1.2.4.2.0-106.jar
```

```
/usr/hdp/current/spark-client/bin/spark-submit –class org.apache.spark.sql.execution.datasources.hbase.examples.HBaseSource –master yarn-cluster –files /etc/hbase/conf/hbase-site.xml –packages zhzhan:shc:0.0.11-1.6.1-s_2.10 –num-executors 4 –driver-memory 512m –executor-memory 512m –executor-cores 1 /usr/hdp/current/spark-client/lib/spark-examples-1.6.1.2.4.2.0-106-hadoop2.7.1.2.4.2.0-106.jar
```

### PUTTING IT ALL TOGETHER

我们刚刚简要介绍了HBase如何在DataFrame级上支持Spark。使用DataFrame API Spark应用程序在HBase表中处理存储数据和在其他数据源中存储数据一样简单。有了这个新功能，Spark应用程序和其他交互式工具可以轻松地使用HBase表中的数据。例如 用户可以在Spark中的HBase表之上运行复杂的SQL查询，对Dataframe执行表连接，或者与Spark Streaming集成执行更复杂的系统应用。

### 下一步是什么？

目前，连接器托管在Hortonworks repo中，并作为Spark软件包发行。该软件包正处于 Apache HBase Trunk正在迁移的流程中。在迁移期间，我们发现了HBaseTrunk中的一些关键bugs，它们可以合并修复。HBase JIRA HBASE-14789，包括HBASE-14795和HBASE-14796跟踪了整个社区的工作为了优化Scan和BulkGet的底层计算体系结构，HBASE-14801提供易于使用的JSON用户界面，HBASE-15336用于DataFrame写路径，HBASE-15334用于支持Avro，HBASE-15333支持Java原始类型，如short，int，long，float和double等等，HBASE-15335支持复合行密钥，HBASE-15572用于添加可选时间戳语义。我们期待将来更易于使用的连接器版本。

参考网址：

- [1] SHC: https://github.com/hortonworks/shc
- [2] Spark-package: http://spark-packages.org/package/zhzhan/shc
- [3] Apache HBase:  https://hbase.apache.org/
- [4] Apache Spark: http://spark.apache.org/

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

