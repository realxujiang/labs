openstack allinone

### 必备条件
- Centos 7/Redhat7 最小化安装系统。
- openstack-mitaka 版本
- ssh 免密码登录。
- Linux基础优化/selinux关闭/关闭防火墙。

### 检测环境

检测是否符合安装openstack的基础条件，其中包括字符集、selinux、操作系统版本。

#### Centos Version

```
$ cat /etc/redhat-release 
  CentOS Linux release 7.2.1511 (Core)

$ sestatus -v
     SELinux status:                 disabled
```

`CentOS-OpenStack-mitaka.repo`地址：http://mirror.centos.org/centos/7/cloud/$basearch/openstack-mitaka/

#### 操作系统字符集
```
$ cat /etc/environment 
LANG=en_US.utf-8
LC_ALL=en_US.utf-8
```

### 一键安装openstack集群

`CentOS 7.2` 可以直接安装`centos-release-openstack-mitaka`文件，这个代表mitaka版本的openstack仓库，我们可以通过如下命令检测，可以看到多版本的openstack仓库

```
yum search openstack

centos-release-openstack.noarch : OpenStack from the CentOS Cloud SIG repo configs
centos-release-openstack-kilo.noarch : OpenStack from the CentOS Cloud SIG repo
                                     : configs
centos-release-openstack-liberty.noarch : OpenStack from the CentOS Cloud SIG repo
                                        : configs
centos-release-openstack-mitaka.noarch : OpenStack from the CentOS Cloud SIG repo
                                       : configs
centos-release-openstack-newton.noarch : OpenStack from the CentOS Cloud SIG repo
                                       : configs
centos-release-openstack-ocata.noarch : OpenStack from the CentOS Cloud SIG repo
                                      : config
```

#### packstack介绍

Packstack主要是由Redhat推出的用于概念验证（PoC）环境快速部署的工具。Packstack是一个命令行工具，它使用Python封装了Puppet模块，通过SSH在服务器上部署OpenStack。

Packstack支持三种运行模式：

- 快速运行
- 交互式运行
- 非交互式运行

Packstack支持两种部署架构：

- All-in-One，即所有的服务部署到一台服务器上
- Multi-Node，即控制节点、网络节点和计算节点分开部署

*`packstack-answers-20160928.txt`安装服务列表,可根据需要进行定制*

- Should Packstack install OpenStack Image Service (Glance) 
- Should Packstack install OpenStack Block Storage (Cinder) 
- Should Packstack install OpenStack Shared File System (Manila) 
- Should Packstack install OpenStack Compute (Nova) 
- Should Packstack install OpenStack Networking (Neutron) 
- Should Packstack install OpenStack Dashboard (Horizon) 
- Should Packstack install OpenStack Object Storage (Swift) 
- Should Packstack install OpenStack Metering (Ceilometer) 
- Should Packstack install OpenStack Telemetry Alarming (Aodh) 
- Should Packstack install OpenStack Resource Metering (Gnocchi) 
- Should Packstack install OpenStack Clustering (Sahara). If yes it'll also install Heat. 
- Should Packstack install OpenStack Orchestration (Heat) 
- Should Packstack install OpenStack Database (Trove) 
- Should Packstack install OpenStack Bare Metal (Ironic) 
- Should Packstack install OpenStack client tools 

Puppet是由Puppetlabs公司开发的系统管理框架和工具集，被用于IT服务的自动化管理。由于良好的声明式语言和易于扩展的框架设计以及可重用可共享的模块，使得Google、Cisco、Twitter、RedHat、New York Stock Exchange等众多公司和机构在其数据中心的自动化管理中用到了puppet。半年一度的PuppetConf大会也跻身于重要技术会议之列。而我们的`packstack`就是通过puppet自动化实现安装openstack的。

[PuppetOpenstack](https://wiki.openstack.org/wiki/Puppet)是Openstack社区推出的Puppet Modules项目，隶属于Openstack Goverance项目。

社区还有更多能一键部署openstack的方法

- Packstack封装了PuppetOpenstack，使得用户在终端下可以通过交互式问答或者非交互式YAML格式文件的方式去部署Openstack集群，使得用户无需了解Puppet和PuppetOpenstack的细节。

- Fuel更进一步，提供了友好的Web UI界面，使得用户对于技术细节如何实现上做到了非常好的隐藏，还提供了一些健康检查工具，确保部署符合预期。

当然还有更多其他工具，目前比较方便可靠的安装方式就两种常用的。

#### 安装openstack
我们在上面search openstack的时候可以看到多个版本,目前支持自动化部署的最新版本为`ocata`,我们这里选择安装的版本`mitaka`

```
$ sudo yum install -y centos-release-openstack-mitaka
$ sudo yum update -y  
$ sudo yum install -y openstack-packstack
```

如上我们执行的是，首先安装M版本的`yum`仓库源，然后升级操作系统包，最后安装`openstack-packstack`一键部署openstack集群工具。

#### auto configuration && 自定义配置文件安装

生成默认配置文件,定制安装服务，下面我们选择的就是`packstack` - Multi-Node 模式进行集群安装，allinone相对来说适合测试环境部署。
```
$ sudo packstack --gen-answer-file=packstack-answers-20160928.txt
  CONFIG_NAGIOS_INSTALL=n            ## 是否安装nagios ，修改为不安装
  CONFIG_SAHARA_INSTALL=y            ## 是否安装 Bigdata plugins，修改为安装
```

指定自定义配置文件进行集群安装
```
$ sudo packstack --answer-file=packstack-answers-20160613-231012.txt

**** Installation completed successfully ******
```

如上，我们通过`packstack`自动化安装openstack工具命令，生成安装配置信息，由于`openstack`包括很多组件，所以有些组件是可选的，你可以定制化服务进行安装。

- `packstack --gen-answer-file=xxx.txt` 生成默认的安装配置文件
- `packstack --answer-file=xxx.txt` 指定配置文件安装openstack集群

执行`packstack --answer-file=xxx.txt`命令后，等待`openstack`安装完成，这是一个漫长的过程，当你看到所有安装项都处于`[DONE]`后，显示一句话`**** Installation completed successfully ******`说明你已经成功安装好openstack一个节点的集群，此时`controller`、`compute`和`network`节点都在同一个节点上，在后续的章节中我们会继续教大家怎么扩容节点。

安装成功之后，我们在执行命令的当前目录下面会生成两个文件，是属于`keystone`的验证文件，如果你需要执行相关管理员的命令，就需要使用它们的身份进行执行，也是访问Dashboard的登录用户。访问地址`http://openstack-controller/dashboard`

- keystonerc_admin    超级管理员用户信息
- keystonerc_demo     demo测试用户信息，它属于一个租户

后台使用你需要执行`source`命令，你就可以`admin`或者以其他租户的身份去做一些管理员操作
```
source keystonerc_admin
```

例如：
```
[root@openstack-controller ~(keystone_admin)]# keystone user-list
[root@openstack-controller ~(keystone_admin)]# keystone service-list
[root@openstack-controller ~(keystone_admin)]# nova host-list
```
![](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-nova-hostlist.png)

***如果你想在第一次安装时就安装多个节点？***
你需要修改配置文件`packstack-answers-20160613-231012.txt`, 修改`CONFIG_COMPUTE_HOSTS`配置项。

例如：
```
egrep "CONFIG_COMPUTE_HOSTS|CONFIG_NETWORK_HOSTS|EXCLUDE_SERVERS" packstack-answers-20160613-231012.txt
EXCLUDE_SERVERS=
CONFIG_COMPUTE_HOSTS=192.168.2.110,192.168.2.111,192.168.2.112,192.168.2.113
CONFIG_NETWORK_HOSTS=192.168.2.110
```

如上图所示，是集群安装比较关键的配置信息
- EXCLUDE_SERVERS   你是新添加节点,你需要把已经安装过的`COMPUTE`节点IP集合天在这里,`packastack`会排除不去在去安装。如果是*初次安装*,这里应该留空。
- CONFIG_COMPUTE_HOSTS  填写计算节点IP集合
- CONFIG_NETWORK_HOSTS  填写网络节点IP

执行`sudo packstack --answer-file=packstack-answers-20160613-231012.txt`安装命令，然后就开始按照配置文件中的IP信息，并行的在多台服务器上安装`openstack`集群。

安装成功之后，查看安装的主机列表
```
cinder list   # 查看云硬盘信息

nova host-list # 查看主机节点角色信息
```
![](https://github.com/itweet/labs/raw/master/openstack-series/img/nova-lists.png)

如上图所示，我们按照预期安装了4个节点的openstack集群，一个控制节点，一个网络节点，4个计算节点，这就是通过`packstack`一键自动化安装openstack集群。后续章节中，我们会进一步介绍通过这样的配置方式来添加一个新的节点到已存在的openstack集群。

### 总结
`openstack系列(5)-M版_快速部署`，也同样适用于其他更高的版本安装，但是由于我在生产环境使用M版本1年多无重大故障，所以我比较推荐使用一个稳定的版本。所以继续用M版本安装方式来编写本系列教程。本系列内容希望搭建从第一篇开始看起，每一篇都是以前一篇我基础来一步步实现集群的安装的，所以这一篇也是建立在之前的内容之上的，本篇其实就手动实践了怎么通过`packstack`工具自动化部署openstack。下一小节我们进入`openstack`网络的配置，欢迎持续关注。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/

参考：https://www.rdoproject.org/install/quickstart/
    https://repos.fedorapeople.org/repos/openstack/
    http://cloud.centos.org/centos/7/images/
    https://pom.nops.cloud/Introduction/read_guide.html