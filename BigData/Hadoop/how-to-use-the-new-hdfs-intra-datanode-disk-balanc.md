如何在Apache Hadoop中使用新版HDFS Intra-DataNode磁盘均衡器 （译文）
---

***目前HDFS包含了(在CDH 5.8.2 及更高版本)一个综合的容量管理存储方法，该方法用于跨节点移动数据。***

在HDFS内部，数据节点将数据块分布在本地文件系统目录中，该本地文件系统目录被指定用于dfs.datanode.data.dir in hdfs-site.xml. 在不同的设备中（例如，单独的HDD和SSD）用标准的方式安装，HDFS术语都将每个目录都称作是一个容量。

当给HDFS写入新的块时，数据节点为块用volume-choosing 策略选择磁盘。目前这两种策略类型都支持：轮询方式或者可用空间方式 (HDFS-1804)。

简单的说， 如图表1所示， 轮询策略跨越可用磁盘分布新的块， 而可用空间策略优先在空间更多的磁盘写入块。（根据百分比分配）

![](https://github.com/itweet/labs/raw/master/BigData/img/balancer.png)

默认情况下， 数据节点使用轮询策略写入新的块。然而在一个长期运行的集群中，因为HDFS中大量的文件删除或者通过热插拔磁盘功能添加新的数据节点磁盘，还是有可能会造成明显的容量分布不平衡，。即使你选择用基于可用空间的策略代替轮询策略，容量不平衡仍然会导致磁盘I/O效率不高的发生：例如：将新块都写入到新加的空磁盘中而在这期间其他磁盘被闲置在一旁，就给新磁盘造成了一种瓶颈状态。

最近，Apache Hadoop社区开发的服务器脱机脚本(如HDFS-1312，dev@邮件列表，和[GitHub](https://github.com/schmmd/hadoop-balancer))用于减轻数据不平衡问题。然而，由于这些脚本处于HDFS代码库以外，这就需要在磁盘之间移动数据之前，让这些数据节点处于脱机状态。因此， HDFS-1312 还引入了一个在线磁盘平衡器，这种平衡器的设计基于不同的度量完成的，用于平衡Running中数据节点的容量。类似HDFS平衡器，HDFS磁盘平衡器作为一个线程在数据节点中运行，可以跨越相同存储容量类型移动块文件。

在接下来的部分， 你将学会为什么和如何使用这种新功能。

### 磁盘平衡器101

让我们一起通过一个案例来逐步探索这项实用的功能。首先， 确认，`dfs.disk.balancer.enabled`在所有数据节点上设置为TRUE。从CDH5.8.2 开始， 在Cloudera Manager中，用户可以通过HDFS安全阀片段指定完成这项配置。

![](https://github.com/itweet/labs/raw/master/BigData/img/balancer-f2.png)

在这个例子中，我们将新磁盘添加到一个预装的HDFS数据节点(`mnt/disk1`)，并将挂载新磁盘添加到/mnt/disk2。在CDH中，每个HDFS数据目录都在一个单独的磁盘上，因此您可以使用df表示磁盘使用情况：

```
# df -h
….
/var/disk1      5.8G  3.6G  1.9G  66% /mnt/disk1
/var/disk2      5.8G   13M  5.5G   1% /mnt/disk2
```

很明显， 是再次平衡磁盘的时候了！

一个标准的磁盘平衡器的任务包括了三步：（通过hdfs `diskbalancer`执行命令）计划、执行和查询。第一步，HDFS客户将NameNode看作特定的数据节点，并从该数据节点节点上读取必不可少的信息生成执行计划。

```
# hdfs diskbalancer -plan lei-dn-3.example.org
16/08/19 18:04:01 INFO planner.GreedyPlanner: Starting plan for Node : lei-dn-3.example.org:20001
16/08/19 18:04:01 INFO planner.GreedyPlanner: Disk Volume set 03922eb1-63af-4a16-bafe-fde772aee2fa Type : DISK plan completed.Th
16/08/19 18:04:01 INFO planner.GreedyPlanner: Compute Plan for Node : lei-dn-3.example.org:20001 took 5 ms
16/08/19 18:04:01 INFO command.Command: Writing plan to : /system/diskbalancer/2016-Aug-19-18-04-01
```

正如你从输出中看到的一样，HDFS 磁盘平衡器通过数据节点将磁盘使用信息报告给NameNode，并在指定的数据节点上使用planner计算计划移动的数据步骤。每一步都明确了资源和目标移动数据量，以及预计移动的数据量。

在撰写本文时，HDFS唯一的的planner是`GreedyPlanner`，GreedyPlan的作用是不断的从最常用的设备中移动数据到使用最少的设备中直到所有的数据均匀分布在所有的设备上。用户还可以利用`plan`中的命令指定空间阈值，这样， planner就认为磁盘是平衡的除非空间利用的差异低于阈值。（另一个值得注意的设置是在规划过程中通过指定`--bandwidth`调节`diskbalancer` I/O的任务，那样disk balancer I/O就不会影响前台工作了）

在disk-balancer磁盘执行计划时被生成JSON文件存储在HDFS中，在默认情况下， 这个计划文件是存储在`/system/diskbalancer`目录中：

```
# hdfs dfs -ls /system/diskbalancer/2016-Aug-19-18-04-01
Found 2 items
-rw-r--r--   3 hdfs supergroup       1955 2016-08-19 18:04 /system/diskbalancer/2016-Aug-19-18-04-01/lei-dn-3.example.org.before.json
-rw-r--r--   3 hdfs supergroup        908 2016-08-19 18:04 /system/diskbalancer/2016-Aug-19-18-04-01/lei-dn-3.example.org.plan.json
```

为了执行数据节点上的计划，运行：

```
$ hdfs diskbalancer -execute /system/diskbalancer/2016-Aug-17-17-03-56/172.26.10.16.plan.json
16/08/17 17:22:08 INFO command.Command: Executing "execute plan" command
```

这个命令用于提交JSON计划文件到DataNode，并且是在`BlockMover`线程的后台执行。

使用`query`命令检查`diskbalancer`在数据节点上的任务状态：

```
# hdfs diskbalancer -query lei-dn-3:20001
16/08/19 21:08:04 INFO command.Command: Executing "query plan" command.
Plan File: /system/diskbalancer/2016-Aug-19-18-04-01/lei-dn-3.example.org.plan.json
Plan ID: ff735b410579b2bbe15352a14bf001396f22344f7ed5fe24481ac133ce6de65fe5d721e223b08a861245be033a82469d2ce943aac84d9a111b542e6c63b40e75
Result: PLAN_DONE
```

输出(`PLAN_DONE`)表示磁盘平衡任务完成。若要验证磁盘平衡器的有效性， 可再次使用`df -h`查看数据在两个本地磁盘上的分布情况：

```
# df -h
Filesystem      Size  Used Avail Use% Mounted on
….
/var/disk1      5.8G  2.1G  3.5G  37% /mnt/disk1
/var/disk2      5.8G  1.6G  4.0G  29% /mnt/disk2
```

只要输出确认磁盘平衡器成功降低了磁盘空间使用差异并且容量低于10%，就意味着任务完成了！

若想阅读更多关于HDFS磁盘平衡器， 请阅读[Cloudera文档](http://www.cloudera.com/documentation/enterprise/latest/topics/admin_hdfs_balancer.html)和[upstream docs](http://www.cloudera.com/documentation/enterprise/latest/topics/admin_hdfs_balancer.html)。

### 总结

与期待已久一样，HDFS-1312引入了intra-DataNode磁盘平衡器功能， 在CDH5.8.2中HDFS的传输版本或者更高版本提供了综合的存储容量管理解决方案， 该解决方案能够跨越节点（balancer），存储类型（mover）， 在单个DataNode的磁盘(Disk Balancer)移动数据.

译文原文：https://blog.cloudera.com/blog/2016/10/how-to-use-the-new-hdfs-intra-datanode-disk-balancer-in-apache-hadoop/

欢迎关注微信公众号，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


