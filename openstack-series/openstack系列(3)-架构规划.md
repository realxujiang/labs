随着虚拟机技术的发展，企业环境云化对于增强企业级应用开发，核心竞争力有非常大的好处。
对于内部，每个人都有机会拥有独立的开发调试环境，整个公司开发应用，测试，上线等内容都云化，可以便利开发人员，运维人员，节省成本，长远发展来看，可以帮助企业自动化软件架构，实现自动化系统的构建。节省运营，开发，维护，调试，测试等过程费用，减少成本。

对外部，企业自己的产品，可以通过云app，云web，云主机等环境，网络大批开发者，来这个平台开发不同的行业应用，帮助企业级把大平台微应用实现。

### 规划硬件部署
硬件说明，本次为模拟生产环境而编写，所以是在虚拟化的环境下进行搭建，但是完全是按照企业级生产环境的方式进行的安装部署。

- 操作系统信息
```
CentOS Linux release 7.3.1611 (Core) 

Linux openstack-controller 3.10.0-514.10.2.el7.x86_64 x86_64 GNU/Linux
```

- RAID划分
```
Linux OS
    : Raid1     大小：250G     磁盘类型：SSD

Nova-instances
    : Raid5     大小：5.5TB    磁盘类型：SATA

Glusterfs-data
    : Raid0     大小：4T * 4块     磁盘类型：SATA

Ceph-data
    : JBDO      大小：4T * 4块     磁盘类型：SATA
```

Raid配置之后，在操作系统中会以`/dev/sd[x]`的方式呈现。如上有`Linux OS`的系统盘，`Noav-instances`盘用来存储`云主机`,因为云主机默认会自带一块盘进行操作系统的安装，会占用一定的空间，所以这里每个节点我配置为5.5T大小`RAID5`类型的磁盘。Glusterfs和Ceph则为分布式块存储和对象存储系统，用来给云主机提供`云硬盘`,提供大的存储资源池，可以申请后挂载到云主机中使用，它们本身自带着容错和分布式存储能力，所以只需要裸盘进行挂载，glusterfs和ceph就能把所有的磁盘管理起来，形成大的存储资源池。

- 分区规划
```
LinuxOS
    : /     100G
    : /var  80G
    : /boot 500MB
    : swap  20G

Nova-instances
    :  /var/lib/nova/instances   5.5TB   # 所有nova所在节点都需要大空间,存储云主机

Glance-images
    :  /var/lib/glance/images/   4TB # glance所在的节点,需要让存储image需大空间,建议存在GlusterFS中

Glusterfs-data
    ： /data/glusterfs-data[1..4]     # 每台机器4块glusterfs存储
    ： /data/ceph-data[1..4]          # 每台机器4块ceph存储
```

- 硬件配置
    +  CPU   24  Intel(R) Xeon(R) CPU E5-2620 v2 @ 2.10GHz
    +  Memory 128G
    +  硬盘   8块 * 4T 、2块 * 3T、2块 * 250G
    +  万兆网络
    +  节点数  10 Node

### 网络规划
在使您能够评估 OpenStack 的单节点配置中，一个网络接口卡就足够了。但是，对多节点配置使用单个网络接口不足以提供带宽来服务于云的大量网络通信。如果在企业 OpenStack 设置中使用单个网络接口，性能很快就会成为严重问题。

#### 隔离不同类型的网络通信

不同类型的网络通信遍布整个云基础结构。您应该具有单独的网络或子网来托管每种类型的通信，例如：

- 个人用户或租户网络－托管 OpenStack 云中虚拟机 (virtual machine, VM) 间的通信。

- 存储网络－托管 VM 及其位于外部存储系统上的应用程序数据集之间的通信。

- 管理或 API 网络－托管用于管理云基础结构的整个操作的 OpenStack 组件间的通信，包括管理员生成的通信。

- 外部网络－托管 VM 等虚拟实体及其在 OpenStack 云中的专用网络与更广泛的网络（包含公司网络和 Internet）之间的通信。

下图是多节点 OpenStack 配置中的多网络体系结构的示例。
![图 1  多网络体系结构的示例](https://github.com/itweet/labs/raw/master/openstack-series/img/data-networks.jpg)

在此示例中，您可以根据需要进一步扩展体系结构。例如，如果决定使用冗余存储系统，则需要创建单独存储子网来管理到每个系统的通信。

对特定通信使用不同网络，可以实现以下好处：

- *网络的可靠性和可用性*－多个网络可以避免单网络配置固有的单点故障。

- *性能和可伸缩性*－与使用单个网络接口相比，具有多个接口用作不同的网络通信路径可以防止潜在的拥塞及其导致的性能下降。

- *安全性*－分隔网络可以确保控制对 OpenStack 框架的不同部分的访问。

- *可管理性*－对于云管理员，管理整个 OpenStack 框架更容易。

#### 分配逻辑主机名
使用逻辑主机名是适用于任何网络配置方案的良好实践。使用 DNS 或 /etc/hosts 文件进行名称解析。测试配置以确保其正常运行。

#### 选择GRE/VXLAN网络
![vxlan](https://github.com/itweet/labs/raw/master/openstack-series/img/Snap12_thumb.gif)

Compute 节点上由Neutron-OVS-Agent负责：
- br-int：每个虚机都通过一个Linux brige连到该OVS桥上
- br-tun：转化网络packet中的VLAN ID 和 Tunnel ID
- GRE tunnel：虚拟GRE通道

Neutron节点上：
- br-tun/br-int：同Compute节点，由Neutron-OVS-Agent负责
- br-ex：连接物理网卡，用于和外网通信
- Network namespace：用于tenant 网络DHCP服务的qDHCP由Neutron-DHCP-Agent负责，和用于网络间routing的qRouter由Neutron-L3-Agent负责
 
### 部署拓扑
![openstack topology](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-deploy.png)

- Controller 节点安装服务

```
== Nova services ==
openstack-nova-api:                     active
openstack-nova-compute:                 active
openstack-nova-network:                 inactive  (disabled on boot)
openstack-nova-scheduler:               active
openstack-nova-cert:                    active
openstack-nova-conductor:               active
openstack-nova-console:                 inactive  (disabled on boot)
openstack-nova-consoleauth:             active
openstack-nova-xvpvncproxy:             inactive  (disabled on boot)
== Glance services ==
openstack-glance-api:                   active
openstack-glance-registry:              active
== Keystone service ==
openstack-keystone:                     inactive  (disabled on boot)
== Horizon service ==
openstack-dashboard:                    active
== neutron services ==
neutron-server:                         active
neutron-dhcp-agent:                     active
neutron-l3-agent:                       active
neutron-metadata-agent:                 active
neutron-openvswitch-agent:              active
neutron-metering-agent:                 active
== Swift services ==
openstack-swift-proxy:                  active
openstack-swift-account:                active
openstack-swift-container:              active
openstack-swift-object:                 active
== Cinder services ==
openstack-cinder-api:                   active
openstack-cinder-scheduler:             active
openstack-cinder-volume:                active
openstack-cinder-backup:                active
== Ceilometer services ==
openstack-ceilometer-api:               inactive  (disabled on boot)
openstack-ceilometer-central:           active
openstack-ceilometer-compute:           active
openstack-ceilometer-collector:         active
openstack-ceilometer-notification:      active
== Heat services ==
openstack-heat-api:                     active
openstack-heat-api-cfn:                 inactive  (disabled on boot)
openstack-heat-api-cloudwatch:          inactive  (disabled on boot)
openstack-heat-engine:                  active
== Support services ==
mariadb:                                active
openvswitch:                            active
dbus:                                   active
target:                                 active
rabbitmq-server:                        active
memcached:                              active
```

- Compute 节点安装服务
```
openstack-ceilometer-common-6.1.3-2.el7.noarch
openstack-neutron-8.3.0-1.el7.noarch
centos-release-openstack-mitaka-1-5.el7.noarch
openstack-selinux-0.7.13-2.el7.noarch
openstack-ceilometer-polling-6.1.3-2.el7.noarch
openstack-nova-common-13.1.2-1.el7.noarch
openstack-nova-compute-13.1.2-1.el7.noarch
openstack-neutron-common-8.3.0-1.el7.noarch
openstack-neutron-openvswitch-8.3.0-1.el7.noarch
openstack-ceilometer-compute-6.1.3-2.el7.noarch
```


### 云平台功能
![openstack-feature](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-feature-list.png)

### 总结
由于OpenStack的灵活性，您可以使用多种方式在多个节点或系统中分布其组件。比如：系结构仅显示一种在三个节点上部署组件的方式：
- 存储节点

- 计算节点

- 控制器节点

不过，还可以进一步细分组件。例如，您可以在五个节点中进行以下组件分布：

- 节点 1：RabbitMQ

- 节点 2：MySQL 数据库

- 节点 3：OpenStack 控制器组件，例如 Keystone、Glance、Horizon 等

- 节点 4：弹性虚拟交换机

- 节点 5：L3 代理

此外，您还可以有多个存储和计算节点。其他非核心 OpenStack 组件（例如 Ironic）还可以位于其各自的节点中。

由于此灵活性，您可以根据可用资源以及您希望在每个节点中对组件进行分组的方式来设计 OpenStack 基础结构。然后，您可以在每个系统上仅安装需要的 OpenStack 软件包，而不是在所有系统上安装整个 OpenStack 软件包。下一节将进入基础环境准备内容，欢迎关注。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

参考：http://www.infocool.net/OpenStack/index.htm
    http://www.cnblogs.com/sammyliu/p/4204190.html