企业级大数据平台部署实施参考指南 - 环境准备
---

各位，今天我们主要聊一下，集群安装前需要做的准备工作，内容会以HDP做为案例，进行相关的规划和设计工作，经验是通用了，适用于各种大数据发行版。

我的画风一直比较严肃，哈哈，其实我是一个很喜欢搞怪的，感觉写程序傻了。

今天这个内容啊，主要还是围绕集群实施安装过程，非常关键的环节环境准备阶段，通过我们前期收集的一些相关指标，对集群进行基础环境的准备工作。

我们以HDP集群部署来说明相关问题?

### 必备条件

0、选择操作系统版本

可选版本有centos/redhat 6.5,6.6,6.7,6.8和 centos/redhat 7.2

1、Ambari-server所在的服务器能够ssh免密码登录到所有机器

2、所有机器关闭selinux

```
setenforce 0  && sed –i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
```

3、所有机器主机名统一格式

例如： 

```
      - NameNode: namenode{1..2}.hadoop.org
      - DataNode: datanode{1..3000}.hadoop.org
```

4、所有主机名和IP地址进行映射hosts

5、所有机器关闭iptables

```
systemctl stop firewalld.service && systemctl disable firewalld.service 
```

6、所有主机必须通过ntp服务使时间保持一致。

公网NTP同步；如果是内网，需要自己做一个内网的NTP服务器；让服务器时间和硬件时钟同步，避免重启操作系统导致时间不同步，集群组件无法正常工作。

```
ntpdate asia.pool.ntp.org && hwclock -w
```

集群组件利用时间戳进行存储的，需要保障集群所有节点时间一致性，不然会导致集群异常，目前在分布式数据库领域，对于分布式集群时间一致性的误差不能超过秒级，在大数据中Hbase、Zookeeper组件，如果在集群安装之前你没有主动的去让所有节点时间一致，安装完成之后再去同步时间，会导致Hbase、Zookeeper服务无法正常工作。

目前出现了NewSQL数据库系统也是严格要求必须保证同一数据中心时间一致，甚至通过硬件时钟来做时间同步。

### 系统分区

Linux系统分区，在做Linux系统分区的时候， 决定了后续集群是否能够在底层提供合理的数据存储保障能力。比如：操作系统”os/log”需要安装在SSD，那么SSD需要2块做raid1,保障即使有一块盘损坏，保障集群操作系统正常运行。

`注意：系统安装的时候，请使用最小化安装方式，不安装图形化界面.`

- NameNode节点分区方式：

![](https://github.com/itweet/labs/raw/master/BigData/img/namenode_os_parted.png)

这是一个例子，可根据实际情况调整，需要注意的第一点是/var目录单独分出来，避免日志太多导致根目录爆满，导致操作系统无法正常工作。第二点，namenode元数据存储目录，底层硬件上需要保证带有RAID1，一般原则4块盘，每两个做RAID1。第三点，namenode元数据信息存储不需要非常大的空间，它主要负责存储一些数据块切分后存储在那些datanode上这样的记录，你可以把他看做一本书的目录，不会特别大，但是章节过多(block过多)也会导致目录暴涨，建议4块1-2T的SAS/SATA盘，可以动态增加磁盘。

```
NameNode元数据信息案例：
    - 文件个数 22328188 
    - 文件夹个数 711845
    - block个数 32774913
    - 总容量 4.12 PB
    - 容量使用 3.34 PB
    - 元数据大小  5.4g
```

如上，元数据信息占用空间是非常小的，而且它常驻内存，如果集群大量小文件，会导致元数据暴增，大集群重启主节点会超级慢；如果重启后整个集群会导致block块信息汇报，导致主节点非常繁忙长时间处于安全模式。

- DataNode节点分区方式：

![](https://github.com/itweet/labs/raw/master/BigData/img/datanode_disk_parted.png)

这是一个例子，可根据实际情况调整，需要注意的第一点是/var目录单独分出来，避免日志太多导致根目录爆满，导致操作系统无法正常工作。第二点，datanode数据存储目录，底层硬盘为RAID0/JBOD，一般原则12块盘 。第三点，datanode存储一般需要非常大的空间，因为所有的集群数据都存储在datanode管理的磁盘上， 建议单块盘大小4-6T。

- Ambari-Server节点分区方式：

![](https://github.com/itweet/labs/raw/master/BigData/img/ambari-server-parted.png)

这是一个例子，对于集群监控主节点的部署，无论是你使用Ambari-Server、ClouderaManager监控集群或者其他工具监控集群，原则是操作系统建议使用lvm分区管理，方便动态扩展容量，避免出现某些目录占满的情况。监控相关的数据一定要放到大盘去存储，设置好数据清理周期，避免存储数据过大，导致查询时主节点压力过大。

- Gaeteway-Node节点分区方式：

![](https://github.com/itweet/labs/raw/master/BigData/img/gateway-disk-parted.png)

Gateway节点，没有任何集群服务和组件，通常是用来和集群沟通提交任务的节点，主要功能，在Hadoop集群中提供一个桥梁，可以对数据进行接入 。Gateway节点链接到主要局域网的入口， 有时也被称作网关节点。Gateway节点是可选或者不选择的，但常被强烈推荐，对集群瓶颈和性能均有很大的提升作用。

Linux系统分区方案说明：

在很多业务服务器数量多且复杂的运维场景，会有专门的系统安装工程师，由于这些基础系统安装工程师无法确定服务器的业务需求，因此，会根据公司的要求只分出：
- /boot   200M
- Swap    内存*2
- /   （列如： 100G）

然后剩余的分区保留不分，fdisk(不适合大于2t的分区)，parted(适合大于2T的分区)
这样后续使用的服务器的不同业务产品的运维部门就可以根据具体的业务在规划后面的分区，这样的方法也是值得推荐的分区思路！

上面的/data{1..12}目录，表示，如果有12块硬盘，挂载点为12个目录，取名/data1, /data2, /data3, /data..这些目录都用来存储hdfs数据的数据目录！

有关根目录/ ，主要是存储/home，/tmp，/opt等！

有关/var目录主要存储相关组件所有的日志记录信息，所以单独划分，避免根目录出现使用100%的情况，导致操作系统无法正常工作。

### 制作本地源

HDP本地源：

![](https://github.com/itweet/labs/raw/master/BigData/img/hdp-repo.png)

LinuxOS本地源：

![](https://github.com/itweet/labs/raw/master/BigData/img/linuxos_repo.png)

今天内容依然比较干，介绍了一下生产环境中，大数据集群底层系统分区划分，操作系统需要具备的环境，制作内网离线repo仓库。

企业级大数据平台部署实施参考指南》分多节，有更多细节剖析，不妥之处欢迎指正！

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

