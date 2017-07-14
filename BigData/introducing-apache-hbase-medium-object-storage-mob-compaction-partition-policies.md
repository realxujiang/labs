Apache HBase引入对象存储（MOB）压缩分区的策略
---

### 介绍：

[HBASE-11339](https://issues.apache.org/jira/browse/HBASE-11339)引入了Apache HBase介质对象存储（MOB）的功能。该功能可以提高中等尺寸值的低延迟读写访问（理想情况下，我们的测试结果是从100K到10MB），使尺寸值非常适合存储文档，图像和其他中等尺寸的对象[1]。Apache HBase MOB功能通过分离文件引用和MOB对象的IO路径来实现这一改进，将不同的压缩策略应用于MOB，从而降低HBase压缩创建的写入放大率。MOB对象存储在称作MOB区域的特殊区域中。 MOB对象表作为MOB文件存储在MOB区域，这意味着在该区域将存储大量的MOB文件。有关Apache HBase MOB架构，请参见[1]中的图1。

![](https://github.com/itweet/labs/raw/master/BigData/img/Apache-HBase-MOB-Architecture.png)

最初，MOB文件相对较小（不超过1或2个HDFS块）。为了提高Apache HDFS的效率，MOB文件通过MOB compaction合并到较大的文件中，该操作独立于正常的压缩过程。MOB压缩的初始版在一个特定日期为当天的多个MOB文件重写入更大的MOB文件。让我们使用下面示例文件列表来更清楚的解释这一规则。表t1有两个区域（r1，r2），它有一个列族（f1） 启用MOB。你可以看到有两个前缀：`D279186428a75016b17e4df5ea43d080`对应于区域r1的开始键的Hash值，`D41d8cd98f00b204e9800998ecf8427e`对应于区域r2的起始键的Hash值。针对区域r1，在1/1/2016和1/2/2016处有两个MOB文件，针对区域r2，在MOB区域的1/1/2016上有3个MOB文件，这就是`/hbase/data/mobdir/data/default/t1/78e317a6e78a0fceb27b9fa0cb9dcf5b/f1`。

```
>ls  /hbase/data/mobdir/data/default/t1/78e317a6e78a0fceb27b9fa0cb9dcf5b/f1

D279186428a75016b17e4df5ea43d08020160101f9d9713ab2fb4a8b825485f6a8acfcd5

D279186428a75016b17e4df5ea43d08020160101af7713ab2fbf4a8abc5135f6a8467ca8

D279186428a75016b17e4df5ea43d080201601029013ab2fceda8b825485f6a8acfcd515

D279186428a75016b17e4df5ea43d080201601029a7978013ab2fceda8b825485f6a8acf

D41d8cd98f00b204e9800998ecf8427e20160101fc94af623c2345f1b241887721e32a48

D41d8cd98f00b204e9800998ecf8427e20160101d0954af623c2345f1b241887721e3259

D41d8cd98f00b204e9800998ecf8427e20160101439adf4af623c2345f1b241887721e32
```

在MOB压缩之后，区域r1的1/1/2016和1/2/2016的两个MOB文件每天都会被压缩成一个文件。 区域r2的1/1/2016上的三个MOB文件被压缩成一个文件。

```
D279186428a75016b17e4df5ea43d08020160101f49a9d9713ab2fb4a8b825485f6a8acf
D279186428a75016b17e4df5ea43d08020160102bc9176d09424e49a9d9065caf9713ab2
D41d8cd98f00b204e9800998ecf8427e20160101d9cb0954af623c2345f1b241887721e3
```

由于只有同一个区域、同一天的MOB文件可以一起压缩，所以一年中针对一个特定家族的单个MOB区域目录下的MOB文件的最小限制将为365 x区域数量。1000个区域在经历10年的MOB压缩后将生成365×1000×10,365万个文件，并且不断增长！不幸的是，Apache HDFS对同一个目录下的文件数量有内存限制[2]。MOB文件的数量超过此HDFS限制后，MOB表不可再写入。 Apache HDFS单个目录默认最大文件数量为100万。而1000个区域则大约将在3年内达到极限。区域越多，达到极限的速度越快。

HBASE-16981引入了每周和每月的MOB压缩分区聚合策略，因数分别为7天或30天，以分别改善MOB文件计数缩放问题。

每周和每月MOB压缩分区的设计策略（HBASE-16981）

HBASE-16981的基本思路是将一个日历周或一个日历月中的MOB文件压缩成少量、较大的文件。日历周由[ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)定义，从星期一开始，星期日结束。通常情况下，使用每周策略，MOB压缩后每个区域每周将有一个文件; 使用每月策略，MOB压缩之后，每个区域每月将有一个文件。在一年内一个特定家庭的MOB区域目录下的MOB文件数量，将通过利用每周策略和每月策略的12×区域数量，减少到52×区域数量。大大减少了压缩后MOB文件的数量。

### 最初的方法

当MOB进行压缩时，HBase负责选择、聚合日历月或者日历周的MOB文件到少量大型文件中。根据MOB压缩频率，文件可能被多次压缩。例如，假设使用每月聚合策略进行每日的MOB压缩操作。在第1天，MOB压缩将第1天的所有文件压缩为一个文件。 第2天，MOB压缩将文件从第1天和第2天的文件压缩成新的文件; 第3天，MOB压缩将第2天的文件和第3天的文件压缩成一个新文件，直到最后一个月。在这种情况下，第1天的文件被压缩了30次以上，从而写入IO的放大量将超过30x。Apache HBase MOB的设计目标是降低MOB压缩创建的写入放大文件。但这种天真的方法难以实现设计目标。

### 最终实施的方法

为了克服最初提出的方法的不足之处，HBASE-16981采用了新的每周和每月策略，分阶段MOB压缩方法。图2展示了每月策略的使用，每周策略的使用方法类似途中的方法。

![Figure 2 Staging MOB compaction with monthly policy](https://github.com/itweet/labs/raw/master/BigData/img/Figure-2-Staging-MOB-compaction-with-monthly-policy.png)

正如如图2所示，MOB压缩发生在11/15/2016。基于配置了MOB阈值的每日分区中压缩当前日历周中的文件。在图2中，11/14/2016的文件被压缩在一起，11/15/2016的文件被压缩在一起。本月的日历周文件都是基于每周分区与每周阈值进行压缩。（配置为MOB-threshold x 7）。在图2中， 11/1/2016 到
11/6/2016的文件被压缩在一起，11/7/2016 到11/13/2016 的文件被压缩在一起。过去几个月的文件基于月阈值分区（配置为MOB-threshold×28）进行压缩。在图2中，10/1/2016到10/31/2016的文件被压缩在一起。值得注意的是，2016年11月的第一个日历周是从10/31/2016到11/6/2016。 由于10/31/2016在过去一个月内，当天的文件按月分区进行压缩，这就导致每周分区只剩下6天（11/1/2016〜11/6/2016）。压缩之后，如果配置MOB压缩阈值和MOB压缩批量大小配置适宜的话，则有5个文件。

因为这种设计，MOB文件通过了2阶段或3阶段的压缩。并在每个阶段，每日分区，每周分区或每月分区应用增大的MOB压缩阈值。MOB文件按照每月策略通常压缩3次，在每周策略中通常的仅压缩2次。

有关设计的更多细节，请参见[[3](https://issues.apache.org/jira/browse/HBASE-16981)]。

### 用法

默认情况下，按天使用MOB压缩分区策略。要应用每周或每月策略，就需要为MOB列族添加了一个新属性MOB_COMPACT_PARTITION_POLICY。用户可以在HBase shell创建表时设置此属性。

```
create 't1', {NAME => 'f1', IS_MOB => true, MOB_THRESHOLD => 1000000, MOB_COMPACT_PARTITION_POLICY => 'weekly’}
```

用户还可以从HBase shell更改现有表的MOB_COMPACT_PARTITION_POLICY。

```
alter 't1', {NAME => 'f1', MOB_COMPACT_PARTITION_POLICY => 'monthly'}
```

如果策略从每天更改为每周或每月，或每周更改为每月，则下一个MOB压缩将重新压缩之前策略压缩过的MOB文件。如果策略从每月或每周更改为每天或每月，每周更新已经压缩的MOB文件与以前的策略不会被新策略重新压缩。

### 总结

HBASE-16981解决了Apache HBase MOB的文件数量缩放问题。这种技术将可用于Apache HBase 2.0.0发行版。CDH支持CDH 5.4.0+中的Apache HBase MOB。 HBASE-16981被移植在CDH 5.11.0中。

参考：

- [1] https://blog.cloudera.com/blog/2015/06/inside-apache-hbases-new-support-for-mobs/
- [2] https://blog.cloudera.com/blog/2009/02/the-small-files-problem/
- [3] https://issues.apache.org/jira/browse/HBASE-16981
- [4] https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.5.0/bk_data-access/content/ch_MOB-support.html

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/