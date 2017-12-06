HDP2.6中APACHE SPARK & APACHE ZEPPELIN 的新功能
---

任何数据值和它内部的派生值都是成正比的。因为[Data Lake Architecture](https://hortonworks.com/blog/enterprise-hadoop-journey-data-lake/)，所有的企业数据提供在一个位置。从数据湖深入驱动的关键是Apache Spark & Apache Zeppelin。两者都是预测分析和机器学习的关键工具。HDP最进发布的版本为 Spark & Zeppelin 提供了几个关键的功能和改进，有助于预测分析和机器学习的进步。

### APACHE SPARK 2.1

现在Apache Spark 2.1.1使用的是HDP 2.6 的GA. 。这次发布的Spark是在Spark代码上发布的最稳定&功能最丰富的版本。Spark2.1版本的主要重点是Structured Streaming， 机器学习， 和SparkR。Spark流借助Apache Kafka 0.10.0 版本利用 Kafka 连接SSL。Structured Streaming越来越成熟， 但仍然很差， 所以我们不建议在关键生产环境中使用structured streaming除非技术变得更成熟。你很快可以在Hortonworks Data Cloud上尝试[Spark 2.1](https://hortonworks.com/blog/try-apache-spark-2-1-zeppelin-hortonworks-data-cloud/)。

### SPARKR & PYSPARK

大部分数据科学家在SparkR & PySpark 中分别使用 R & Python 语言，他们可以持续使用他们所熟悉的R & Python 语言。然而他们需要Spark API 利用Spark的机器学习达到充分利用分布式计算。SparkR & PySpark正在迅速演变，SparkR 现在支持大量的机器学习算法，例如 LDA, ALS, RF, GMM GBT等。SparkR的另一个关键改变是[部署交互式包](https://community.hortonworks.com/articles/104114/using-r-packages-with-sparkr-1.html)的能力。这有助于数据科学家在他们自己的环境部署他们最爱的包，不用和其他用户用同一个环境。

PySpark现在还支持在虚拟环境中部署，这将使PySpark用户可以独立的在单独的部署环境中部署libraries（函数库）。

### SPARKSQL的行/列级访问权限
也许这次Spark发布的最重要的功能就是Spark [LLAP](https://hortonworks.com/blog/llap-enables-sub-second-sql-hadoop/) & [Ranger](https://hortonworks.com/apache/ranger/)的集成。这种集成提供了[fine-grained access control to SparkSQL](https://hortonworks.com/blog/row-column-level-control-apache-spark/). 现在安全管理员可以指定行/列级访问权限以及对SparkSQL的屏蔽。现在 SparkSQL 和Apache Hive 用户有一样的细粒度访问权限。

### REAT Spark访问

因为HDP2.6版本中， 我们为了 [REST-based access to Spark](https://hortonworks.com/blog/livy-a-rest-interface-for-apache-spark/)已经通过Livy提交。Spark的REST-based 访问对于那些想不打开集群就可以远程访问Spark用户的大型企业很有用。REST 访问还可以提交需求处理身份验证。

### 改善大数据作业的追踪

Spark作业经常和其他HDP组件交互工作， 例如， 他们从HDFS上读取然后在YARN上运行。追踪系统调用这些组件很困难并且也很难纠正这些行为。因为这一版本中， 我们提供了通过组件关联这些行为，可以将复杂的[Spark作业调试](https://community.hortonworks.com/articles/103610/providing-tracing-with-spark-caller-context.html)的更简单。

### Apache Zeppelin 0.7

这次HDP的发布还提供了Apache Zeppelin 0.7.1版本。关键的改善是 Zeppelin 0.7 支持Apache Spark 2.1。另一个重大[improvement is in Zeppelin’s integration with Livy](https://hortonworks.com/blog/recent-improvements-apache-zeppelin-livy-integration/)。因为这个版本，Zeppelin的Livy interpreter 可以自动发现过期的会话，不需要重启Livy过期会话。再一个关键改善是支持在JDBC interpreter中多行SQL statement。

### 总结
HDP 2.6是Apache Spark & Zeppelin 的主要版本引入了大量重要的功能。请试用我们的最新版本， 我们恨期待您的反馈以便我们持续改进。

译文原文：https://hortonworks.com/blog/new_apache-spark-zeppelin-hdp-2-6_enterprise_data/

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


