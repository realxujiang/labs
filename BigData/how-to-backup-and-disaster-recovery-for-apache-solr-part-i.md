怎么备份和灾难复原Apache Solr (part 1)
---

Cloudera Search（是Apache Solr和 Apache Hadoop 生态系统的集成）现在对Solr Connections`支持（作为5.9版本）备份和恢复`。

在这篇文章中我们将讨论在Cloudera Search 内部备份的基本知识和灾难恢复能力。下一篇文章中我们将讨论Solr快照功能的设计 Hadoop生态系统的集成 和公有平台（例如，亚马逊 AWS）

对于大部分组织和最终用户来说数据可用性是至关重要的。大量的生产数据作为关键业务通过Cloudera Search提供服务。当然改变从未停歇过： 升级， 应用开发， 配置的变化等, 无论它是通过cloudera Search还是独立Solr  长期以来对于组织降低风险一直都是一种挑战。

***备份和恢复灾难的能力具体的解决了在Sorl里存储关键业务数据的后顾忧。***

- 怎么样恢复Search索引的意外情况，例如因为意外丢失了索引数据或者恶意管理操作（删除了一个集合）数据增加/减少（例如删除了一个或者多了一个）

- 怎么样迁移现存的Solr索引到其他集群上去（在perm或云上）

- 怎么样在Solr 集群升级过程中减少风险？

备份过程中的允许管理员创建索引文件的独立副本并对Solr connection配置数据，对Solr connection态的任何后续改变（例如移动文件， 删除索引文件或者改变connection配置）都不会影响备份的状态，作为灾难修复的一部分，还原操作要创建一个新的Solr connection然后通过Solr connection备份初始化到最初的状态。

### 备份操作如下所示
- 1，获取潜在Apache Lucene 相应索引的一致性和指定的时间点视图到Solr集合 上备份，在Lucene术语中， 这种索引一致性和时间点视图表示为索引提交。
solr中的数据快照功能实施这一步是为了确保备份状态是否还存在并行索引（或者查询）操作，这就要求用户在Solr集群中没有任何中断（或者宕机）时备份Solr connection。

- 2，复制Lucene索引文件并关联在Apache管理员里获取提交的索引值和元数据集合到用户指定的共享文件系统 上（例如，Apache HDFS 或者基于文件系统的NFS）

现在我们将探讨并展示如何使用 Cloudera Search提供的常用命令去快速简单的执行Solr connection备份和灾难恢复。

首先创建一个叫books的connection，然后索引一些样本数据到connection上， 这仅用于演示目的。你肯定是有一个存有数据的环境在你的connection里。

```
$ solrctl instancedir --generate books
$ solrctl instancedir --create books books/
$ solrctl collection --create books
```

然后用示例数据初始化集合，接下来的插入一个单文件到这个集合中并issues a hard-commit，因为Solr备份功能只在hard-committed 数据上运行， 请记得在执行备份操作之前发起个hard-commit。

```
$ curl 'http://localhost:8983/solr/books/update?commit=true' \
> -H 'Content-type:application/json' -d '
> [
>  {"id" : "book1",
>   "title" : "American Gods",
>   "author" : "Neil Gaiman"
>  }
> ]'
{"responseHeader":{"status":0,"QTime":444}}
```

这样之后我们就已经为创建一个books的集合做好了准备。 数据快照是指特定的 Lucene 索引提交的一块元数据，Solr 保证提交的索引值是在快照数据的生命期被保存的，尽管索引值随后会被优化。这使得 Solr集合的数据快照需要提供一个指定的时间点，索引数据是否一致性的状态，甚至是并行索引操作是否存在，要注意快照数据的创建是非常迅速的因为它只需要保存快照元数据不需要复制相关的索引文件。

下一步命令是创建一个叫‘my-nap’的快照数据。

```
$ solrctl collection --create-snapshot my-snap -c books
Successfully created snapshot with name my-snap for collection books
```

接下来创建快照数据的细节
```
$ solrctl collection --describe-snapshot my-snap -c books
Name: my-snap
Status: Successful
Time of creation: Fri, 28 Oct 2016 12:17:45 PDT
Total number of cores with snapshot: 1
-----------------------------------
Core [name=books_shard1_replica1, leader=true, generation=1, indexDirPath=hdfs://name-node-host:8020/solr/books/core_node1/data/index/]
```

你还可以使用下命令将现有集合中的数据快照做成列表
```
$ solrctl collection --list-snapshots books my-snap
```

一旦数据快照创建完成， 你就可以用它来恢复操作失误的数据。 例如多插入了一个新文件或者删除（更新）了一个现存的文件。但是从灾难恢复的角度来看， 创建一个数据快照还不够，在很多情况下创建数据快照也可能导致数据丢失。例如Lucene里的软件bug/ Solr损坏索引文件对快照数据的关联， 或者管理员意外删除集合或者执行其他管理操作，例如删除一个副本或者拆分一个或者多个碎片。因此， 备份快照数据的状态到其他位置非常重要（最好是在Solr的权限之外）

Solr的备份功能需要一个共享文件系统存储Solr集合的索引文件和配置元数据。在执行备份之前请确认你安装的solr.xml 包含相关配置（注——重启Solr服务器必须是在添加了相关配置到solr.xml之后）。

在HDFS中创建一个用来存储Solr集合备份的目录，Solr服务器用户(solr默认情况下)必须能够读取和写入此目录。上传这篇博客的目的也是为了让 Solr服务器用户拥有备份目录，但是你也可以用HDFS ACLs 的功能让其他用户备份和存储Solr集合。

```
$ sudo -u hdfs hdfs dfs -mkdir /solr-backups
$ sudo -u hdfs hdfs dfs -chown solr:solr /solr-backups
```

注——hdfs是HDFS的管理用户

这个时候我们就可以准备备份之前创建的数据快照了（即“my-snap"）为此请使用一下命令。一旦备份操作完成你就可以查看备份目录的内容了。

```
$ sudo -u solr solrctl collection --export-snapshot my-snap -c books -d /solr-backups
```

备份成功创建以后， 你就可以安全的删除早期创建的数据快照， 这就要求Solr 删除关联提交的Lucene索引值并清理集群上的内存空间，以下命令删除数据快照。

```
$ solrctl collection --delete-snapshot my-snap -c books
Successfully deleted snapshot with name my-snap for collection books
```

此时， 我们就准备复原早先创建的备份了， 复原操作是在备份的时候在Solr里创建一个配置完全相同的新集合作为原始集合。Solr还支持一些配置参数的重写， 例如， 复制因素，配置命名等。

还原操作完成需要的时间取决于原始集合（备份）索引值的大小和复制配置的因素。因此，要恢复大量的集合建议使用支持Solr的异步集合管理API。Cloudera Search里solrctl工具为此授权用户传输一个独特的识别符 作为还原操作的一部分。还原命令只要启动了还原操作就要立刻返回。

运行以下命令还原备份。

```
$ sudo -u solr solrctl collection --restore books_restored -l /solr-backups -b my-snap -i req_0
```

这种操作的状态可以重复调用以下命令进行监视直到完成（或者失败）状态。

```
$ solrctl collection --request-status req_0
<?xml version="1.0" encoding="UTF-8"?>
<response>
  <lst name="responseHeader">
    <int name="status">0</int>
    <int name="QTime">1</int>
  </lst>
  <lst name="status">
    <str name="state">completed</str>
    <str name="msg">found req_0 in completed tasks</str>
  </lst>
</response>
```

此命令打印指定request_id. 的状态 ，这种状态可以是下面其中的一种。

+ 运行
+ 完成（i.e.成功）
+ 失败
+ 未发现服务

### 总结

在这篇文章中我们讨论了基础的备份和在Cloudera Search上的灾难复原。有关详细信息请参阅Cloudera Search文档。你也可以在SFBay apachelucene/Solr meetup上Search我对于备份和恢复Solr的观点。

译文原文：https://blog.cloudera.com/blog/2017/05/how-to-backup-and-disaster-recovery-for-apache-solr-part-i/

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/