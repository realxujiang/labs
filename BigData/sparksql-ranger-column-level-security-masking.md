SPARKSQL, RANGER, AND LLAP通过SPARK THRIFT SERVER为BI方案提供行，列级安全
---

Apache Spark引发了在大型数据集上进行数据挖掘的爆炸式增长。Spark在通用分布式计算访问中发挥了巨大的作用。任何在Python，Scala，Java和R中具有一定造诣的人都能大规模地探索数据。Spark提供ML(Machine Learning)作为一系列黑盒子，将数据科学民主化。对于在统计和数学中都没有PHD的我们来说也有可能做到培训人工智能。当下Spark SQL也可直接在商业中用探索数据。与Apache Hive一起使用，Spark用户可以用SQL表达式来探索非常大的数据集。然而，为了使Spark SQL真正可用于ad-hoc访问，商业分析师有必要使用BI工具的细粒度以及资源管理。Spark通过Kerberos提供了强大的身份验证、并通过SSL进行在线加密。 但是，到目前为止，授权只能通过HDFS ACL进行。当Spark用作通用计算框架时，这种工作方法相对较好。也就是说，Java / Scala / Python表达式不能封装在SQL语句中的逻辑。然而，当使用行和列的结构化模式时，细粒度的安全性就成为一种挑战。因为同一表中的数据可能属于两个不同的组，每组都有自己的监管要求。 数据可能有区域限制，时间的可用性限制，部门限制等。 

目前， Spark并未构建授权子系统。Spark根据指示读取数据集，无论成功或者失败都基于文件系统的权限。Spark没有办法定义一个包含细粒度授权指令集的可插拔模块。这意味着授权策略必须在Spark外部执行。换句话说，一些其他系统必须告诉Spark，它不被允许读取数据，因为数据中包含了受限列。这个时候，有两种可能可行的解决方案。 第一个是在Spark中创建授权子系统。第二种方案是  通过 Spark外部的守护程序将Spark配置到读取文件系统中。第二个方案特别有吸引力，因为它可以提供的好处远远不止细粒度的安全性。还有，社区创建的LLAP（Live Long and Process）LLAP和HDFS数据节点服务一起工作，是长期守护程序的集合。LLAP是可选的和模块化的，因此它可以被开启或关闭。目前，APACHE HIVE和LLAP有深度集成。而LLAP的目的是广泛的为在Yarn中运行的应用程序提供帮助。当LLAP启用后，它提供了许多性能优势： - 处理Offload - IO优化 - 缓存，由于本文的重点是Spark的安全性，有关LLAP的更多详细信息，请参阅LLAP Apache Wiki。https://cwiki.apache.org/confluence/display/Hive/LLAP

启用LLAP后，Spark可直接通过LLAP从HDFS读取数据。Spark除了提供上述所有优点之外，LLAP还是执行细粒度安全策略的天然场所。现在还需要的能力是集中授权系统。Apache Ranger满足了这一需求。 Apache Ranger为大量运行在Yarn上或依赖HDFS的数据组件提供了集中授权和审核服务。Ranger允许创建以下安全策略： - HDFS - Yarn - Hive（Spark with LLAP） - HBase - Kafka - Storm - Solr - Atlas - Knox上述每项服务通过插件与Ranger集成，该插件提供最新的安全策略，缓存这些策略，然后在运行时应用这些策略。

![](https://github.com/itweet/labs/raw/master/BigData/img/HCC-1024x659.png)

- Spark SQL列级细粒度访问控制。
- 每个用户完全动态策略，不需要视图。
- 使用标准的Ranger策略和工具来控制访问和屏蔽。

流程：

1.  SparkSQL使用“splits”从Hive Server和查询计划中获取数据的位置信息。
2.  Hive Server2使用Ranger授权访问，每个用户的策略就像应用行过滤这种策略一样。
3.  Spark基于动态安全策略调整查询计划。
4.  Spark从LLAP上读取数据，LLAP server保障数据过滤/屏蔽。

现在我们已经完成如何将细粒度授权和审核应用于Spark的定义，让我们来回顾整体架构。

1.  Spark接收查询语句，并与Hive进行通信，以获取相关的模式和查询计划。
2.  Ranger Hive插件检查缓存的安全策略，并告诉Spark什么列允许访问。
3.  Spark没有自己的授权系统，所以它尝试通过LLAP读取文件系统。
4.  LLAP审核读取请求，LLAP审核读取请求，并发现用户发出请求的列中包含没有读取权限的列。LLAP就会立即停止处理请求，并向Spark发出授权异常。

请注意，关于这些数据无需创建任何类型的抽象视图。执行细粒度安全唯一需要操作的是在Ranger中配置安全策略，并启用LLAP。Ranger还提供列屏蔽和行过滤功能，屏蔽策略类似列策略。主要区别是所有列返回后，受限列仅包含星号或原始值的Hash值。

Ranger还提供了应用行级安全性的能力。使用行级安全策略，用户可以看到表格中所有不受策略限制的行，并防止用户看到表中的某些限制行。比如这种情况，只有财务经理才能看到分配给他们的客户的情况。Ranger的行级策略指示Hive返回包含谓词的查询计划。该谓词过滤掉财务经理尝试访问但是并未分配给他所有的客户数据。Spark接收调整后的查询计划就启动处理，通过LLAP读取数据。LLAP确保谓词的应用以及不返回被限制的行。因为这一系列细粒度安全功能设置，Spark现在可以通过Thrift服务器直接使用BI工具。现在商业分析师就能使用Apache Spark的强大功能。

总体来说，LLAP集成有从性能和安全角度大大增强Spark的潜力。细粒度的安全有助于将Spark的优点应用到商业中。这种发展有助于推动更多地投资，集合和数据探索。如果您想亲自测试这些功能，请查看以下教程：
https://community.hortonworks.com/content/kbentry/72454/apache-spark-fine-grain-security-with-llap-test-dr.html

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/