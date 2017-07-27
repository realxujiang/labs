企业级大数据平台部署实施参考指南 - 硬件配置
---

我最近打算聊一聊上前台服务器集群的部署细节，今天我们聊硬件配置。

### 机架

操作系统版本CentOs6.8，用户名root，密码123456.

![服务器列表](https://github.com/itweet/labs/raw/master/BigData/img/server_list.png)

### 网络

![集群网络](https://github.com/itweet/labs/raw/master/BigData/img/cluster_network.png)

如上图所示，可容纳2560个节点的集群网络结构，构建10GE网络的庞大集群，网络设备是典型和核心层交换机、汇聚层交换机。图示为Dell的交换机产品，类似H3C、华为也有相关的硬件。需要Z9000*16台设备，Z9000是全40gb的汇聚交换。
分为64个rack，每个rack最大可容纳40台1RU服务器，总共可支撑2560个节点。具体部署过程中，注意主节点相关角色放到不同的机架上，Zookeeper，JournalNode节点放到不同机架。在后续内容有更加详细的介绍。
硬件配置和网络都需要有非常专业的工程师调试好，只有所有的环节优化到最佳，方才能在软件层面最大化把硬件资源利用起来，快速完成数据分析任务。

### 磁盘

* 主备NameNode的配置：
    - 2*300G SSD、10*600G SAS
    - 2*SSD RAID1安装操作系统，10*600G SAS RAID10

* DataNode的配置
    - 1*1.5T SSD、2*600G SAS、12*8T SATA
    - 2*SAS RAID1安装操作系统、12*SATA,SSD裸盘挂载

* 设备盘符
    - sda：SSD盘
    - sdb-sdm：12*SATA盘
    - sdn：2*SAS RAID1盘

* CPU与内存
    - NameNode的配置：32核CPU，128G内存
    - DataNode的配置：28核CPU，512G内存

### 总结

我们在10GE网络的庞大集群设计中，网络、硬件、大数据软件选型都非常重要，从硬件到软件都需紧密的配合达到最优性能，才能最大化发挥集群的性能。每台计算节点配置SSD盘做集群加速，利用HDFS的多级存储支持，让热数据存储在SSD中加速数据存取分析效率。

在这样庞大的集群规模下，集群前期POC调优让软硬件达到最佳状态，把服务器上架开始算起少则1-3个月，多则2-4个月，所耗费的人力物力...，对很大多数公司来说如此庞大的集群没有意义，但是对正真需要这样庞大集群的公司来说，意义重大。

《企业级大数据平台部署实施参考指南》分为多节，有更多细节剖析！

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/




