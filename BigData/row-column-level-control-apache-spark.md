简介Apache Spark的行/列级的访问权限
---

Hortonworks数据平台(HDP)的最新版本的功能为我们的客户提供了大量重大的改良，例如，现在HDP 2.6.0支持Apache Spark™2.1和Apache Hive™2.1(LLAP™)作为GA。通常客户在Hive里面存储数据，用Hive和SparkSQL分析这些数据。这种方案一个很重要的需求是不管是否是用Hive 和SparkSQL分析数据，都要在Hive数据中应用相同细粒度的访问权限规则，。这种细粒度访问权限包括的功能有行/列级访问或者屏蔽数据。Spark SQL 2.1的 HDP 2.6.0行/列级安全性是预定了GA并且即将发布的 HDP 2.6.1的技术预览版。

企业最基本的需求一直是安全性。例如，在一个公司里记账、数据科学、区域销售团队可能都需要访问权限查看客户数据，而敏感的数据，像信用卡卡号仅仅只有财务团队可以访问。此前，Apache Hive™和Apache Ranger™的规则就是针对处理这种情况的。

### 使用HDP 2.6之后 SparkSQL的核心价值

-   共享访问权限规则：同一集群上可以安全的共享数据，还可以通过SparkSQL和 Hive之间通用的访问权限规则持续控制数据。

-   审计：SparkSQL所有的访问通道都可以通过Ranger的集中式接口监控和搜索。

-   资源管理： 每个用户都可以用一个唯一的队列访问安全的共享数据。

-   最低过渡成本：因为这种功能在SQL中提供了行/列级安全性，所以目前 Spark 2.1 apps 、脚本、所有的Spark shells(spark-shell, pyspark, sparkR, spark-sql)无需任何修改都支持这种功能。

使用行/列级安全性不同SQL，用户基于用过的规则，做相同的查询得到的结果不同。换句话说，用户只能基于每个Kerberos主体的身份信息查看数据。细粒度的样式限制了对数据库的访问， 表的访问， 行的访问和列的访问。

### SparkSQL访问模式

Spark SQL 有多种不同的访问模式—Spark Thrift Server over JDBC/ODBC, Spark shells, 和 Spark 应用程序. 也可以用Spark Thrift Server经由Apache  Zeppelin的JDBC解释器访问SparkSQL，HDP 2.6都支持这些访问模式。

### 示例数据和Ranger的访问控制策略
我们假设一下我们有一个客户表，t_customer'，在数据库'db_spark中包含以下数据`。

![](https://github.com/itweet/labs/raw/master/BigData/img/Screen-Shot-2017-05-16-at-10.02.06-PM.png)

例如有两个用户，“datascience” 和“billing”。 用访问权限规则定义Apache Ranger限制“datascience” 用户只能访问男性顾客，并且只能访问前四个名称字符。“billing”用户没有这种限制。

### SQL用JDBC/ODBC通过 Spark Thrift Server访问Hive表
下方示例中，`datascience`用户登录 `beeline` 和 `Zeppelin` ，仅访问男性用户并屏蔽用户的姓。

![](https://github.com/itweet/labs/raw/master/BigData/img/Screen-Shot-2017-05-16-at-10.06.43-PM.png)

![](https://github.com/itweet/labs/raw/master/BigData/img/Screen-Shot-2017-05-16-at-10.07.58-PM.png)

### 使用 Scala/ Python/ R编程访问Hive表格
当两个用户运行同样的SQL query从客户表中检索所有的数据 ，结果会有所不同。接下来的环节展示了两种 spark-shell 命令，一个用于‘billing’ 用户， 另一个用于限制更多的“datascience” 用户。

![](https://github.com/itweet/labs/raw/master/BigData/img/Screen-Shot-2017-05-16-at-10.13.57-PM.png)

![](https://github.com/itweet/labs/raw/master/BigData/img/Screen-Shot-2017-05-16-at-10.20.23-PM.png)

### 总结：
访问权限是企业的关键需求，现在SparkSQL的行/列级访问权限，屏蔽和密文等提供了企业级细粒度的访问权限。SparkSQL的访问通道遵循的是Hive用户遵循的同样的访问权限规则。此操作可以移除SparkSQL的关键限制， 我们认为还可以采纳更多的SparkSQL功能。

A demo of this feature can be viewed in this youtube video:

视频地址：https://youtu.be/o6M4eljSIOQ

如果您要在您的 HDP 2.6环境重尝试这种功能， 请参阅这篇HCC文章，里面提供了更多的细节说明。

译文原文：https://hortonworks.com/blog/row-column-level-control-apache-spark/

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

