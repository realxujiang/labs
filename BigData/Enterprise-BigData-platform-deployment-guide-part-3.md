企业级大数据平台部署实施参考指南 - 集群设计
---

集群设计主要为了说明几个比较实用的分布式软件安装过程中角色分配问题，不同的角色所在机器磁盘划分的主意事项。

### 角色分配

由于您选择使用Ambari Manager进行集群的自动化部署方式，下面图表显示了在大多数集群的安装时合理化的角色划分方式。

![](https://github.com/itweet/labs/raw/master/BigData/img/ambari_service_layout.png)

在较大的集群(超过100+个节点)中，可能需要涉及到5个管理节点，比如Namenode HA和ResourceManager HA需要专有节点，此外Ambari Manager也需要专有节点，此节点可以部署Hive Metastore，Hive Server2,Spark Thrift Server等对外提供服务的角色。

我们建议每个管理节点128G内存，工作节点256-512G。内存相对便宜，并且随着对计算引擎越来越高的要求，引入内存计算充分利用内存，快速响应。

角色分配原则，有单点的问题的服务集中在一台机器，方便管理，可视化相关对外提供服务的放置和监控管理节点在用一个机器。如果监控节点(Ambari Server)没有HA功能，可以通过定时对监控服务节点进行备份数据和数据库快照，即使在监控服务器损坏的情况下，依然可以通过数据库备份数据在一个全新的服务器上恢复监控服务，而不会影响任何管理组件的正常运行。

目前Ambari Server是可以支持迁移到新的服务器节点恢复，可以参考我历史文章。

需要注意，在大集群(50+ 节点)中，一定要提前统计好服务器所属机架，尽量把不同的管理节点在物理上分配到不同的机架。

- Master1/Master2： Namenode、ResourceManager，HMaster，ZKServer，Journalnode
- Ambari Manager：Ambari Server、ZKServer，Journalnode

ZKServer，Journalnode保证基数个节点，这里涉及到3个管理节点，物理上对应着3台物理服务器，在物理逻辑上保证他们尽量放置于不同的机架。

### 磁盘划分

下面图标，介绍不同的角色如何合理的划分磁盘。

![](https://github.com/itweet/labs/raw/master/BigData/img/master_disk_allocation.png)

如图Master1/Master2管理节点， 针对可以支持HA功能的角色服务，比如Namenode HA,Resource Manager HA，Hbase HMaser HA等。

此类型的节点只有Namenode用来存储元数据信息占用空间相对大，建议4块2T SAS通过JBDO管理，其中2块盘用来存储Namenode元数据信息，另两块盘存储Zookeeper，Journalnode角色的数据信息。

有条件情况 -> 生产环境中尽量保证，重要的角色管理的数据目录在物理上区分开，分而治之，方便管理。

![](https://github.com/itweet/labs/raw/master/BigData/img/ambari_manager_disk_allocation.png)

我们在部署Ambari Manager数据库中指定使用LVM，但RAID0也是一种选择。    

![](https://github.com/itweet/labs/raw/master/BigData/img/worker_disk_allocation.png)

所有节点操作系统都是2块盘做RAID1，根据不同的管理节点角色磁盘划分有区别，所有Worker节点磁盘都使用JBOD，每块盘都是裸盘方式直接挂载用于存储HDFS数据。

### 小结

参与太多大数据相关项目，还是那句话最合适自己的才是最好，很多企业其实不需要大数据，如果硬上只会导致提供大数据平台的越做越痛苦，客户也很痛苦。不能太盲目，过去几年我接触的很多公司，都被炒概念者的忽悠的近乎狂热，认为大数据技术是万能的，什么都能搞定？真的如此么？

![](https://github.com/itweet/labs/raw/master/BigData/img/bigAll_aa.png)

A君：用100台服务器干一台服务器的事，然后在用30台服务器把他们管理起来。

B君：服务器跑不满怎么办？拿来搭建测试/实践环境，然后出炉各种技术/架构文章，曰"XX”著名互联网公司XX服务XX端技术架构“。

C君：装X，钱、钱、钱...

如上，是微薄上程序员大拿们讨论的一个话题，我盗图来说明一下问题？

还是那句话，适合自己的是最好的，搞分布式、多机集群，除非业务真的需要，不然会面临尴尬局面。

扯远了，今天思维跳跃了，我的主要工作还是帮助需要大数据的企业和个人输出经验 ~@^_^@~。

《企业级大数据平台部署实施参考指南》分多节，有更多细节剖析，不妥之处欢迎指正！

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/