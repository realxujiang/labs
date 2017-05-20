
主要介绍openstack需要依赖的环境和网络配置信息,使用静态IP地址，vmware桥接模式。

*一台服务器虚拟4个虚拟机，服务器配置信息如下：*
- 24核心、CPU x5650*2、32G内存、240G SSD，2TB硬盘.

### openstack主机配置信息

![主机配置信息](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-hardware-configuration-list.png)

### openstack网络规划配置

![网络拓扑图](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-network.png)

openstack主机功能分类:

![网络拓扑图](https://github.com/itweet/labs/raw/master/openstack-series/img/openstack-role-list.png)

### Linux系统安装及基础优化 

安装`Linux CentOS 7.2`系统时，使用最小化安装，在使用系统过程中，按需安装软件，避免引入带漏洞软件，导致服务器处于危险境地。

#### 配置网络

如下所示，你需要修改主机IP地址为静态IP，所有主机都类似修改，所有主机需要修改的地方，如下需要改动的地方就是`BOOTPROTO`,`ONBOOT`,`IPADDR`,`NETMASK`,`GATEWAY`,`DNS1`,`DNS2`内容，其他保持不变即可：

```
$ ip addr|grep "inet "|grep dynamic
    inet 192.168.2.110/23 brd 192.168.1.255 scope global dynamic eno16777736

$  vi /etc/sysconfig/network-scripts/ifcfg-eno16777736 
BOOTPROTO="static"
ONBOOT="yes"
IPADDR=192.168.2.110
NETMASK=255.255.255.0
GATEWAY=192.168.2.1
DNS1=114.114.114.114
DNS2=119.29.29.29
```

重启网卡，让网络配置生效
```
sudo systemctl restart network.service
```

执行如下命令，检测是否修改已经生效，看到如下信息说明已经配置正确
```
$ ip addr|grep "inet "|grep eno16777736
inet 192.168.2.110/24 brd 192.168.2.255 scope global eno16777736
```

检测是否可以上外网,我们在安装openstack整个过程中，所有节点都必须处于联网状态
```
ping www.baidu.com
PING www.a.shifen.com (61.135.169.125) 56(84) bytes of data.
64 bytes from 61.135.169.125: icmp_seq=1 ttl=52 time=2.39 ms
```

#### 配置hostname

通过命令修改主机名，其他主机的主机名修改参考如下命令

```
$ sudo hostnamectl set-hostname openstack-controller
$ cat /etc/hostname 
openstack-controller
```

#### 检测Linux版本

```
$ hostnamectl status
   Static hostname: openstack-controller
         Icon name: computer-vm
           Chassis: vm
        Machine ID: f6133ba53e254a81a20c0fd6d5cf4f39
           Boot ID: 96f32a152edc4a20b29a1fa9a2ec891f
    Virtualization: vmware
  Operating System: CentOS Linux 7 (Core)
       CPE OS Name: cpe:/o:centos:centos:7
            Kernel: Linux 3.10.0-327.el7.x86_64
      Architecture: x86-64

$ cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core)

```

#### 关闭Selinux

关闭Selinux自动化shell命令
```
# sed -i 's#SELINUX=enforcing#SELINUX=disabled#g' /etc/selinux/config
```

让关闭SELinux立即生效
```
# setenforce 0
```

检测关闭selinux配置,是否修改正确
```
# grep SELINUX=disabled /etc/selinux/config
SELINUX=disabled
```

#### 关闭防火墙
```
sudo systemctl status firewalld.service
sudo systemctl stop firewalld.service          
sudo systemctl disable firewalld.service
```

#### 精简开机启动项

systemctl可以列出正在运行的服务状态,通过如下命令检测服务启动情况，可以关闭那些不需要的开机自动启动服务。

- 启动一个服务：systemctl start postfix.service
- 关闭一个服务：systemctl stop postfix.service
- 重启一个服务：systemctl restart postfix.service
- 显示一个服务的状态：systemctl status postfix.service
- 在开机时启用一个服务：systemctl enable postfix.service
- 在开机时禁用一个服务：systemctl disable postfix.service
- 查看服务是否开机启动：systemctl is-enabled postfix.service
- 查看已启动的服务列表：systemctl list-unit-files|grep enabled

```
# systemctl list-unit-files|grep enabled
auditd.service                              enabled 
... 省略 ...
```

#### 管理员用户

添加openstack管理员用户，并赋予相应的sudo权限

```
# useradd openstack
# echo "openstack123"|passwd --stdin openstack
# echo 'openstack  ALL=(ALL)       NOPASSWD: ALL' >> /etc/sudoers
```

#### 修改文件描述符
```
# echo '* - nofile 65535'  >>  /etc/security/limits.conf
```

#### 配置ntp服务器

让所有服务器时间保持一致，如果是非内网服务器可以直接安装启动`ntp`。

```
# yum install ntp –y
# systemctl start ntpd.service  # 如果同步公网时间，则不需要启动此服务
# systemctl enable ntpd.service # 如果同步公网时间，则不需要设置此服务
# ntpq –p                       # 查询网络中的NTP服务器
# ntpdate time.nist.gov         ＃同步公网时间
```

例如：
```
[openstack@openstack-controller ~]$ sudo ntpdate time.nist.gov
    13 Jun 22:22:20 ntpdate[2365]: step time server 216.229.0.179 offset 6.132085 sec
```

#### 配置hosts映射&&节点相互能ssh免密码访问

hosts映射配置: 
```
[root@openstack-controller ~]# cat /etc/hosts|tail -4
192.168.2.110  openstack-controller
192.168.2.111  openstack-compute-1
192.168.2.112  openstack-compute-2
192.168.2.113  openstack-compute-3

[root@openstack-controller ~]# scp -r /etc/hosts  openstack-compute-1:/etc/
[root@openstack-controller ~]# scp -r /etc/hosts  openstack-compute-2:/etc/
[root@openstack-controller ~]# scp -r /etc/hosts  openstack-compute-3:/etc/
```

配置ssh免密码登陆

在openstack-controller  &&  openstack-compute-2  &&  openstack-compute-3 执行
```
ssh-keygen -t rsa

ssh-copy-id -i ~/.ssh/id_rsa.pub openstack-compute-1
```

在 “openstack-compute-1” 节点执行
```
ssh-keygen -t rsa

ssh-copy-id -i ~/.ssh/id_rsa.pub openstack-compute-1

scp -r ~/.ssh/authorized_keys openstack-compute-2:~/.ssh/
scp -r ~/.ssh/authorized_keys openstack-compute-3:~/.ssh/
scp -r ~/.ssh/authorized_keys openstack-controller:~/.ssh/
```

`注意：`如果，在安装完openstack集群之后，还需要进行扩容添加节点，那么就不能删除免密码互信登录。

### 总结
openstack系列4，重点内容是在安装openstack集群之前的基础环境的准备，如何环境没有准备好，很可能导致安装失败，我们将会在下一节介绍一键部署openstack集群的方法。openstack部署方式多样，我们介绍的是最简单的一种，小白式安装，当然在后续我也会逐一展开说明，帮助大家进一步理解，更容易维护集群。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/