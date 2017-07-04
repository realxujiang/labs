如何将Tableau连接到Druid
---

### HIVE / DRUID INTEGRATION MEANS DRUID IS BI-READY FROM YOUR TOOL OF CHOICE

这是与Apache Hive和Druid进行超快速OLAP分析的三部分系列的第3部分。

### 将Tableau连接到Druid

[在这之前，我们讨论了如何集成Hive / Druid传送screaming-fast分析](https://hortonworks.com/blog/sub-second-analytics-hive-druid/)，其实还有另一个集成，一个更强大，更具优势的集成。使用这种集成构建的任何Druid表其实就是Hive表，这意味着您可以使用任何BI工具中的普通SQL查询这些Druid表。在这篇文章中，我们将用非常简单的办法展示如何将Tableau与Druid挂钩，并且这种方法适用于任何BI工具，例如Qlik，Spotfire，Microstrategy和Excel。您可以利用Hortonworks提供的高品质ODBC和JDBC驱动程序使用普通的Hive连接这些工具中任何一个。

我们一起来看看Tableau到Druid是如何工作的我们从连接普通对话框开始，就像你平时连接Hive一样，在Tableau中使用Hortonworks Hadoop Hive的连接类型。

![Hortonworks Hadoop Hive](Part3Image1.png.png)

请注意，因为我们正在连接Hive LLAP，所以我们连接到的端口是10500而不是往常的端口10000。

接下来，Druid cube就像普通Hive表一样可见，可以像其他表一样加载到Tableau中。我们持续使用SSB数据，因此我们将加载SSB  druid cube作为数据源。 就Tableau而言，它关心的只是一个常规的Hive表。

![Druid Table](Part3Image2-1024x622.png)

结果是，Tableau发起的查询可以被推送到Druid，终端用户可以非常快速地访问他们的数据。

此动画显示使用Hive LLAP访问Tableau中的Druid的实时视图。

视频地址: https://youtu.be/2tCNAhAAtYs

正如您看到的那样，响应时间保持在交互式时间范围内。

Druid可用作HDP 2.6技术预览。除了Hive / Druid集成之外，Hortonworks还可以使用Apache Ambari轻松完成部署、配置和监控Druid，从而使用Druid变得很容易。通过这些简化，在Hadoop方面很博学的用户应该可以在几小时内通过[GitHub](https://github.com/cartershanklin/hive-druid-ssb)上的资料重现本文档中的所有内容。我们非常支持您尝试使用Druid，[HDP](https://hortonworks.com/downloads/)或[Hortonworks数据云](https://hortonworks.com/products/cloud/aws/)，并向[Hortonworks社区](https://community.hortonworks.com/topics/druid.html)提供您的反馈意见。

我们与[AtScale](http://blog.atscale.com/hortonworks-chooses-atscale)密切合作的一部分是定期讨论如何使BI-on-Hadoop为我们的共同客户提供更好的体验。请参阅[AtScale博客](http://blog.atscale.com/hive-druid-atscale)，了解更多有关AtScale + Hive / Druid的信息。


欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/