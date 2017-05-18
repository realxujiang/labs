KVM（Kernel-based Virtual Machine的英文缩写）是内核内建的虚拟机。有点类似于 Xen ，但更追求更简便的运作，比如运行此虚拟机，仅需要加载相应的 kvm 模块即可后台待命。和 Xen 的完整模拟不同的是，KVM 需要芯片支持虚拟化技术（英特尔的 VT 扩展或者 AMD 的 AMD-V 扩展）。

本章节我们主要介绍通过VMware技术虚拟出相关的Linux软件环境，在Linux系统中，安装KVM虚拟化软件，实实在在的去实践一下KVM到底是一个什么样的技术？

### VMware虚拟机支持Kvm虚拟化技术？
在VMware创建的虚拟机中，默认不支持Kvm虚拟化技术，需要芯片级的扩展支持，幸好VMware提供完整的解决方案，可以通过修改虚拟化引擎。

VMware软件版本信息，`VMware® Workstation 11.0.0 build-2305329`
 
首先，你需要启动VMware软件，新建一个`CentOS 6.x`类型的虚拟机，正常安装完成，这个虚拟机默认的`虚拟化引擎`，`首选模式`为"自动"。

如果想让我们的VMware虚拟化出来的CentOS虚拟机支持KVM虚拟化，我们需要修改它支持的`虚拟化引擎`,打开新建的虚拟机，虚拟机状态必须处于`关闭`状态，通过双击`编辑虚拟机设置` > `硬件` ，选择`处理器`菜单，右边会出现`虚拟化引擎`区域，选择`首选模式`为 ***Intel Tv-x/EPT或AMD-V/RVI***,接下来勾选`虚拟化Intel Tv-x/EPT或AMD-V/RVI(v)`，点击`确定`。

KVM需要虚拟机宿主（host）的处理器带有虚拟化支持（对于Intel处理器来说是VT-x，对于AMD处理器来说是AMD-V）。你可以通过以下命令来检查你的处理器是否支持虚拟化：
```
 grep --color -E '(vmx|svm)' /proc/cpuinfo 
```

如果运行后没有显示，那么你的处理器不支持硬件虚拟化，你不能使用KVM。

* 注意: 如果是硬件服务器，您可能需要在BIOS中启用虚拟化支持，参考 [Private Cloud personal workstation](http://www.itweet.cn/blog/2016/06/14/Private%20Cloud%20personal%20workstation)

### 安装Kvm虚拟化软件
安装kvm虚拟化软件，我们需要一个Linux操作系统环境，这里我们选择的Linux版本为`CentOS release 6.8 (Final)`，在这个VMware虚拟化出来的虚拟机中安装kvm虚拟化软件，具体步骤如下：
- 首选安装epel源
```
sudo rpm -ivh http://mirrors.ustc.edu.cn/fedora/epel/6/x86_64/epel-release-6-8.noarch.rpm
```

- 安装kvm虚拟化软件
```
sudo yum install qemu-kvm qeum-kvm-tools virt-manager libvirt
```

- 启动kvm虚拟化软件
```
sudo /etc/init.d/libvirtd start
```

启动成功之后你可以通过`/etc/init.d/libvirtd status`查看启动状态，这个时候，kvm会自动生成一个本地网桥 `virbr0`，可以通过命令查看他的详细信息
```
# ifconfig virbr0
virbr0    Link encap:Ethernet  HWaddr 52:54:00:D7:23:AD  
          inet addr:192.168.122.1  Bcast:192.168.122.255  Mask:255.255.255.0
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 b)  TX bytes:0 (0.0 b)
```

KVM默认使用NAT网络模式。虚拟机获取一个私有 IP（例如 192.168.122.0/24 网段的），并通过本地主机的NAT访问外网。

```
# brctl show
bridge name     bridge id               STP enabled     interfaces
virbr0          8000.525400d723ad       yes             virbr0-nic
```

创建一个本地网桥virbr0，包括两个端口：virbr0-nic 为网桥内部端口，vnet0 为虚拟机网关端口（192.168.122.1）。

虚拟机启动后，配置 192.168.122.1（vnet0）为网关。所有网络操作均由本地主机系统负责。

DNS/DHCP的实现，本地主机系统启动一个 dnsmasq 来负责管理。
```
ps aux|grep dnsmasq
```

`注意：` 启动libvirtd之后自动启动iptables，并且写上一些默认规则。

```
# iptables -nvL -t nat
Chain PREROUTING (policy ACCEPT 304 packets, 38526 bytes)
 pkts bytes target     prot opt in     out     source               destination         

Chain POSTROUTING (policy ACCEPT 7 packets, 483 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 MASQUERADE  tcp  --  *      *       192.168.122.0/24    !192.168.122.0/24    masq ports: 1024-65535 
    0     0 MASQUERADE  udp  --  *      *       192.168.122.0/24    !192.168.122.0/24    masq ports: 1024-65535 
    0     0 MASQUERADE  all  --  *      *       192.168.122.0/24    !192.168.122.0/24    

Chain OUTPUT (policy ACCEPT 7 packets, 483 bytes)
 pkts bytes target     prot opt in     out     source               destination 
```

### kvm创建虚拟机

上传一个镜像文件：`CentOS-6.6-x86_64-bin-DVD1.iso`

通过`qemu`创建一个raw格式的文件(注：QEMU使用的镜像文件：qcow2与raw，它们都是QEMU(KVM)虚拟机使用的磁盘文件格式)，大小为5G。

```
qemu-img create -f raw /data/Centos-6.6-x68_64.raw 5G
```

查看创建的raw磁盘格式文件信息
```
qemu-img info /data/Centos-6.6-x68_64.raw 

image: /data/Centos-6.6-x68_64.raw
file format: raw
virtual size: 5.0G (5368709120 bytes)
disk size: 0
```

启动，kvm虚拟机，进行操作系统安装
```
virt-install  --virt-type kvm --name CentOS-6.6-x86_64 --ram 512 --cdrom /data/CentOS-6.6-x86_64-bin-DVD1.iso --disk path=/data/Centos-6.6-x68_64.raw --network network=default --graphics vnc,listen=0.0.0.0 --noautoconsole
```

启动之后，通过命令查看启动状态，默认会在操作系统开一个`5900`的端口，可以通过虚拟机远程管理软件`vnc`客户端连接，然后可视化的方式安装操作系统。

```
# netstat -ntlp|grep 5900
tcp        0      0 0.0.0.0:5900                0.0.0.0:*                   LISTEN      2504/qemu-kvm   
```

`注意`：kvm安装的虚拟机，不确定是那一台，在后台就是一个进程，每增加一台端口号+1，第一次创建的为5900！

### 虚拟机远程管理软件
我们可以使用虚拟机远程管理软件VNC进行操作系统的安装，我使用过的两款不错的虚拟机远程管理终端软件，一个是Windows上使用，一个在Mac上为了方便安装一个Google Chrome插件后即可开始使用，软件信息 `Tightvnc` 或者 `VNC@Viewer for Google Chrome`

如果你和我一样使用的是`Google Chrome`提供的VNC插件，使用方式，在`Address`输入框中输入，宿主机IP:59000,`Picture Quality`选择框使用默认选项，点击`Connect`进入到安装操作系统的界面，你可以安装常规的方式进行安装，等待系统安装完成重启，然后就可以正常使用kvm虚拟化出来的操作系统了。

`Tightvnc`软件的使用，请参考官方手册。

- Tightvnc下载地址：http://www.tightvnc.com/download.php
- Tightvnc下载地址：http://www.tightvnc.com/download/2.7.10/tightvnc-2.7.10-setup-64bit.msi
- Tightvnc下载地址：http://www.tightvnc.com/download/2.7.10/tightvnc-2.7.10-setup-32bit.msi

### KVM虚拟机管理
kvm虚拟机是通过virsh命令进行管理的，libvirt是Linux上的虚拟化库，是长期稳定的C语言API，支持KVM/QEMU、Xen、LXC等主流虚拟化方案。链接：http://libvirt.org/
virsh是Libvirt对应的shell命令。

查看所有虚拟机状态
```
virsh list --all
```

启动虚拟机
```
virsh start [NAME]
```

列表启动状态的虚拟机
```
virsh list 
```

- 常用命令查看
```
 virsh --help|more less
```

### libvirt虚拟机配置文件
虚拟机libvirt配置文件在`/etc/libvirt/qemu`路径下，生产中我们需要去修改它的网络信息。

```
# ll
total 8
-rw-------. 1 root root 3047 Oct 19  2016 Centos-6.6-x68_64.xml
drwx------. 3 root root 4096 Oct 17  2016 networks
```

`注意`：不能直接修改xml文件，需要通过提供的命令！

```
 virsh edit Centos-6.6-x68_64
```

kvm三种网络类型,桥接、NAT、仅主机模式，默认NAT模式,其他机器无法登陆，生产中一般选择桥接。

### 监控kvm虚拟机

- 安装软件监控虚拟机

```
yum install virt-top -y
```

- 查看虚拟机资源使用情况

```
virt-top

virt-top 23:46:39 - x86_64 1/1CPU 3392MHz 3816MB
1 domains, 1 active, 1 running, 0 sleeping, 0 paused, 0 inactive D:0 O:0 X:0
CPU: 5.6%  Mem: 2024 MB (2024 MB by guests)

   ID S RDRQ WRRQ RXBY TXBY %CPU %MEM    TIME   NAME                                                                                                 
    1 R    0    1   52    0  5.6 53.0   5:16.15 centos-6.8
```

### KVM修改NAT模式为桥接[案例]

在开始案例之前，需要知道的必要信息，宿主机IP是`192.168.2.200`，操作系统版本`Centos-6.6-x68_64`。

启动虚拟网卡
```
ifup eth0
```

这里网卡是NAT模式，可以上网，ping通其他机器，但是其他机器无法登陆！

宿主机查看网卡信息
```
brctl show

ifconfig virbr0

ifconfig vnet0
```

*** 实现网桥，在kvm宿主机完成 ***

- 步骤1，创建一个网桥，新建网桥连接到eth0,删除eth0,让新的网桥拥有eth0的ip

```
brctl addbr br0  #创建一个网桥

brctl show       #显示网桥信息

brctl addif br0 eth0 && ip addr del dev eth0 192.168.2.200/24 && ifconfig br0 192.168.2.200/24 up

brctl show      #查看结果
ifconfig br0    #验证br0是否成功取代了eth0的IP
```

`注意`: 这里的IP地址为 *宿主机ip* 

- 修改虚拟机桥接到br0网卡，在宿主机修改

```
virsh list --all

ps aux |grep kvm

virsh stop Centos-6.6-x68_64

virsh list --all             
```

修改虚拟机桥接到宿主机，修改52行type为`bridge`，第54行bridge为`br0`

```
# virsh edit Centos-6.6-x68_64  # 命令

52     <interface type='network'>
     53       <mac address='52:54:00:2a:2d:60'/>
     54       <source network='default'/>
     55       <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
     56     </interface>

修改为：
52     <interface type='bridge'>
     53       <mac address='52:54:00:2a:2d:60'/>
     54       <source bridge='br0'/>
     55       <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
     56     </interface>
```

启动虚拟机，看到启动前后，桥接变化，vnet0被桥接到了br0

启动前：
```
# brctl show
bridge name     bridge id               STP enabled     interfaces
br0             8000.000c29f824c9       no              eth0
virbr0          8000.525400353d8e       yes             virbr0-nic

```

启动后：
```
# virsh start CentOS-6.6-x86_64
Domain CentOS-6.6-x86_64 started

# brctl show                   
bridge name     bridge id               STP enabled     interfaces
br0             8000.000c29f824c9       no              eth0
                                                        vnet0
virbr0          8000.525400353d8e       yes             virbr0-nic
```

Vnc登陆后，修改ip地址，看到dhcp可以使用，被桥接到现有的ip段，ip是自动获取,而且是和宿主机在同一个IP段.
```
# ifup eth0
```

从宿主机登陆此服务器，可以成功。
```
# ssh 192.168.2.108
root@192.168.2.108's password: 
Last login: Sat Jan 30 12:40:28 2016
```

从同一网段其他服务器登陆此虚拟机,也可以成功,至此让kvm管理的服务器能够桥接上网就完成了，在生产环境中，桥接上网是非常必要的。

### 总结
通过kvm相关的命令来创建虚拟机，安装和调试是非常必要的，因为现有的很多私有云，公有云产品都使用到了kvm这样的技术，学习基本的kvm使用对维护`openstack`集群有非常要的作用，其次所有的`openstack image`制作也得通过kvm这样的底层技术来完成，最后上传到`openstack`的镜像管理模块，才能开始通过`openstack image`生成云主机。

到此，各位应该能够体会到，其实kvm是一个非常底层和核心的虚拟化技术，而openstack就是对`kvm`这样的技术进行了一个上层封装，可以非常方便，可视化的操作和维护`kvm`虚拟机，这就是现在`牛`上天的`云计算`技术最底层技术栈，具体怎么实现请看下图。

![Libvirt_support](https://github.com/itweet/labs/raw/master/openstack-series/img/Libvirt_support.png)

如上图，没有`openstack`我们依然可以通过，`libvirt`来对虚拟机进行操作，只不过比较繁琐和难以维护。通过openstack就可以非常方便的进行底层虚拟化技术的管理、维护、使用。

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/



