OpenStack网络（neutron）管理您OpenStack环境中虚拟网络基础设施（VNI）所有网络方面和物理网络基础设施（PNI）的接入层方面。OpenStack网络允许租户创建包括像 firewall，`load balancer`和`virtual private network (VPN)`等这样服务的高级网络虚拟拓扑。

网络提供网络，子网和路由作为对象抽象的概念。每个概念都有自己的功能，可以模拟对应的物理对应设备：网络包括子网，路由在不同的子网和网络间进行路由转发。

每个路由都有一个连接到网络的网关，并且很多接口都连接到子网中。子网可以访问其他连接到相同路由其他子网的机器。

我们在使用openstack过程中，网络配置可选项很多，比如:['local','flat', 'vlan', 'gre', 'vxlan']等。在上一篇<openstack系列(5)-M版_快速部署>中，我们自动化部署默认选择的网络就是vxlan模式，并且在更早的文章中介绍过几种网络模式的选择问题，下面我们将选择vxlan进行集群网络的设置，我们分后端网络和前端网络进行实践配置。

### 网络配置-后端

为了让我们的公共网络和物理环境在同一个网段，我们需要在网络节点把`br-ex`替代`ifcfg-eno16777736`的位置，然后把`ifcfg-eno16777736`通过`OVS_BRIDGE`接到`br-ex`上。

```
[root@openstack-controller ~(keystone_admin)]# cat  /etc/sysconfig/network-scripts/ifcfg-br-ex
NAME="br-ex"
DEVICE="br-ex"
DEVICETYPE=ovs
TYPE=OVSBridge
ONBOOT=yes
IPV6INIT=no
BOOTPROTO=none
DNS1=114.114.114.114
DOMAIN=openstack-controller
DEFROUTE=yes
IPV4_FAILURE_FATAL=no
IPADDR=192.168.2.110
PREFIX=24
GATEWAY=192.168.2.1

[root@openstack-controller ~(keystone_admin)]# cat /etc/sysconfig/network-scripts/ifcfg-eno16777736
NAME="eno16777736"
DEVICE="eno16777736"
ONBOOT="yes"
IPV6INIT=no
BOOTPROTO=none
DEVICETYPE=ovs
TYPE=OVSPort
OVS_BRIDGE=br-ex
```

重启网卡，让修改生效
```
[root@openstack-controller ~(keystone_admin)]# systemctl status network.service
[root@openstack-controller ~(keystone_admin)]# systemctl restart network.service
```

查看ovs信息，这里网络为何这样配置，请参考之前的文章进行了解。
```
[root@openstack-controller ~(keystone_admin)]# ovs-vsctl show
3969c3c6-a08f-4d69-a8f3-717a7551b13d
    Bridge br-int
        fail_mode: secure
        Port "tapf8c9d8d0-2a"
            tag: 1
            Interface "tapf8c9d8d0-2a"
                type: internal
        Port patch-tun
            Interface patch-tun
                type: patch
                options: {peer=patch-int}
        Port br-int
            Interface br-int
                type: internal
        Port "qr-e28efd98-0f"
            tag: 1
            Interface "qr-e28efd98-0f"
                type: internal
    Bridge br-tun
        fail_mode: secure
        Port br-tun
            Interface br-tun
                type: internal
        Port patch-int
            Interface patch-int
                type: patch
                options: {peer=patch-tun}
    Bridge br-ex
        Port "eno16777736"
            Interface "eno16777736"
        Port br-ex
            Interface br-ex
                type: internal
    ovs_version: "2.5.0"
```

这里我们就完成的后端网络的配置，让宿主机网络和云主机浮动IP网络在同一个网段。

### 配置网络－前端

#### admin用户登录操作

1、首先通过admin登陆，首先建立一个openstack-cloud用户，做为另外一个租户创建一个单独私有网段。

- `身份管理` > `角色` > `创建角色` > 键入openstack-cloud，回车
    
- `身份管理` > `组` > `创建组` > 键入openstack-cloud，回车
    
- `身份管理` > `项目` > 选择 “openstack-cloud” > 点击 `管理成员` 
    + 项目信息 > 名称: openstack-cloud ; 描述：openstack-cloud project
    + 项目成员 > 项目成员 > 选择`openstack-cloud`
    + 项目组 > 项目组 > 选择`openstack-cloud`
    + 配额 > 根据目前总的资源情况，配置`openstack-cloud`租户可以使用多少资源
    + 勾选 `激活`
    + 保存
 
- `身份管理` > `用户` > `创建用户` 
    + 用户名：openstack-cloud
    + 描述：openstack-cloud manager user
    + 密码：123456
    + 邮箱：openstack@itweet.cn
    + 主项目：openstack-cloud
    + 角色：openstack-cloud
    + 勾选 `激活`
    + 创建用户

2、首先通过admin登陆，管理员 > 系统 > 删除“路由”，“网络”中的所有内容。(packstack默认创建,用不上)。

- 管理员 > 网络 > 创建网络 
    + 名称：public
    + 项目：admin
    + 供应商网络类型：VXLAN
    + 段ID：0
    + 管理状态：UP
    + 勾选 `共享的`
    + 勾选 `外部网络`
    + 提交

*点击public网络,进去添加子网,点击下一步,最后点击创建。*

- 步骤1
    + 创建子网 > 子网
    + 子网名称：public-subnet
    + 网络地址：192.168.2.0/24
    + IP版本：IPv4
    + 网关IP：192.168.2.1
    + 下一步

- 步骤2
    + 创建子网 > 子网详情
    + 勾选 `激活DHCP`
    + 分配IP地址：192.168.2.120,192.168.2.199
    + DNS服务器：219.141.140.10 219.141.136.10
    + 点击 `已创建`

至此通过，超级管理员创建公共网络已经完成。稍后我们将针对不同的租户创建单独的网络，并且不同的租户共享同一个公共网络。如图：
![](https://github.com/itweet/labs/raw/master/openstack-series/img/public-subnet.png)

#### openstack-cloud用户登录操作

1、设置租户网络，项目 －> 网络 －>网络，创建私有网络

- 步骤1
    + 项目 > 网络 > 网络 > 创建网络 - 网络
    + 网络名称：private
    + 管理状态：UP
    + 勾选 `创建子网`
    + 前近
    
- 步骤2
    + 项目 > 网络 > 网络 > 创建网络 - 子网
    + 子网名称：private-subnet
    + 网络地址：172.16.12.0/24
    + IP版本：IPv4
    + 网关IP: 172.16.12.1
    + 前进

- 步骤3
    + 项目 > 网络 > 网络 > 创建网络 - 子网详情
    + 勾选 `激活DHCP`
    + 分配地址池：172.16.12.2,172.16.12.100
    + DNS服务器：192.168.2.1
    + 点击 `已创建`

至此，完成租户`openstack-cloud`网络创建，每个租户可以拥有自己独立的网络，共享超级用户创建的公共网络资源，其实就是浮动IP，后续我们就会了解到这个公共网络的用处。如图：
![](https://github.com/itweet/labs/raw/master/openstack-series/img/public-private-network-config.png)

2、设置租户路由，项目 －> 网络 －> 路由

- 步骤1：
    + 项目 > 网络 > 路由 > 新建路由
    + 路由名称：router
    + 管理状态：UP
    + 外部网络：public
    + 点击 `新建路由`

- 步骤2：
    + 点击新建的路由router，设置公网＋私网路由通信, 点击 > 接口 > 增加接口
    + 子网：选择private-subnet
    + IP地址：172.16.12.1
    + 路由名称：router
    + 点击 `提交`

至此完成租户openstack-cloud的路由配置，成功让public和private网络连接起来。如下图：  
![](https://github.com/itweet/labs/raw/master/openstack-series/img/router.png)
    

3、网络拓扑检测，项目 > 网络 > 网络拓扑

![](https://github.com/itweet/labs/raw/master/openstack-series/img/network-topology.png)

openstack-cloud租户网络和公共网络打通之后，就如上图所示，网络拓扑图。

4、访问规则设置,项目 > 计算 > 访问 & 安全

- 步骤1：
    + 项目 > 计算 > 访问 & 安全 > 安全组
    + 点击 `管理规则`
    + 选中两个`入口`规则，删除
    + 点击 > `添加规则`
    + 规则：其他协议
    + 方向：入口
    + 远程：CIDR
    + CIDR：0.0.0.0/0

- 步骤2：
    + 项目 > 计算 > 访问 & 安全 > 安全组
    + 点击 > `添加规则`
    + 规则：其他协议
    + 方向：入口
    + 远程：CIDR
    + CIDR：::/0

完成，租户openstack-cloud的访问规则设置，效果如下，如果设置不正确，会导致无法连接云主机。
![](https://github.com/itweet/labs/raw/master/openstack-series/img/network-rule.png)

5、访问安全设置,访问 & 安全 - 密钥

`openstack`用户下，生成秘钥，让openstack用户秘钥，可以免密码登录到云主机中。

```
[openstack@openstack-controller ~]$ ssh-keygen -t rsa -f cloud.key
```

- 步骤1：
    + 项目 > 计算 > 访问 & 安全 > 秘钥对
    + 导入秘钥，根据提示导入刚刚生成的秘钥信息

- 步骤2：
    + `ssh -i cloud.key <username>@<instance_ip>`可以免密码登录云主机
    + 需要使用在openstack用户下面的秘钥登录，可以免密码

### 总结
openstack系列，网络配置，其实openstack网络是最复杂的模块，因为能把网络搞懂的人多，包括我自己对网络这块的认知还很肤浅，如果有问题，欢迎反馈。本小节带大家一步步实践了openstack网络相关的配置，下一节我们就可以开始云主机内容，欢迎关注。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/
