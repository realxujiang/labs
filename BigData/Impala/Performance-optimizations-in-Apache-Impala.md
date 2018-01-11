Apache Impala 性能优化
---

前几天，`ApacheImpala`社区发布了性能优化的一个topics，干货慢慢，我第一次见到的完整Impala整体的侧重优化和架构设计权衡的Slide。

去年底，`ApacheImpala`已经成为Apache顶级项目，我还写文章介绍过，做为企业级SQL on Hadoop解决方案，已经大规模商业应用，随着CDH的发展，家喻户晓，Hadoop生态圈的贡献不可限量，性能也很优秀，曾经很长一段时间很多朋友咨询过Impala的生产环境问题，它拥有完整的权限、审计、高性能。

- 1、SparkSQL、Hive不支持即席查询。
- 2、支持更新和删除数据。
- 3、支持横向扩展高性能OLAP分析
- 4、兼容Hadoop生态，低门槛

如上，那么可以尝试ApacheImpala，完美发挥性能，需大内存，Impalad节点128G~256G。

Outline一览，全是能讲清楚Apache Impala的好东西，可以看到Impala在分布式聚合和分布式扫描统计方面一些独特的实现，它是一个真正的分布式SQL查询引擎，完美兼容HDFS，调度查询灵活。

- Impala项目的历史原因和动机
- Impala架构设计
- 侧重于性能优化概述
    + 查询计划概述
    + 查询优化
    + 元数据和统计信息
- Back-end
    + Partitioning and sorting for Selective scans
    + Code-generation using LLVM
    + Streaming Aggregation
    + Runtime filters
    + Handling cache misses for Joins and Aggs

由于内容太多，摘录部分，精彩slide片段，获取完整内容，点击[阅读原文]。

![impala-1](https://github.com/itweet/labs/raw/master/BigData/img/impala-1.png)

![impala-logical-vivew](https://github.com/itweet/labs/raw/master/BigData/img/impala-logical-vivew.png)

![multi-storage-select](https://github.com/itweet/labs/raw/master/BigData/img/multi-storage-select.png)

![query-optimization-join](https://github.com/itweet/labs/raw/master/BigData/img/query-optimization-join.png)

![scanner-query](https://github.com/itweet/labs/raw/master/BigData/img/scanner-query.png)

![llvm-codegen](https://github.com/itweet/labs/raw/master/BigData/img/llvm-codegen.png)

![codegen-order-top](https://github.com/itweet/labs/raw/master/BigData/img/codegen-order-top.png)

![straming-agg](https://github.com/itweet/labs/raw/master/BigData/img/straming-agg.png)

![runtime-filters](https://github.com/itweet/labs/raw/master/BigData/img/runtime-filters.png)

![impala-roadmap](https://github.com/itweet/labs/raw/master/BigData/img/impala-roadmap.png)

介绍了一些核心的优化思路和代码实现，非常值得，通过实战系统研究优化成果，探索高性能Impala使用方式。

Slide地址：https://github.com/jikelab/labs/tree/master/slide

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
