openstack M版本之后，可视化程度越来越高，曾经网络配置，用户创建，管理等功能全都是后台命令行操作生成，现在全都是可视化操作，现在开始我们揭开云主机神秘的面纱吧。

### 官方镜像
镜像是云主机最基础的依赖，没有镜像就无法创建云主机。跟没有操作系统安装软件包，就无法安装操作系统是一样的道理。

openstack安装成功后，默认会有一个公共镜像`cirros`，你可以通过这个镜像轻松的完成云主机的创建，并且通过`vnc`的方式连接到云主机中。

如果你安装成openstack之后并没有公共镜像`cirros`生成，那么你可以通过下面的地址到官方网站下载。

- cirros镜像：http://download.cirros-cloud.net/0.3.4/
- 更多镜像：http://cloud.centos.org/centos/7/images/

Openstack的开发，基本都使用这个image来测试，因为他比较小，只有10M。生产环境中基本都是自己制作镜像，或者通过官方提供的镜像镜像定制，然后才开始使用。

Cirros，是可以使用用户名和密码登陆，也可以使用密钥登陆
- user:cirros
- password:cubswin:)

#### glance上传镜像

这里我们下载`cirros-0.3.4`版本的镜像

```
$ wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
```

上传镜像可以选择在`dashboard`或者命令行

- `dashboard`上传，使用openstack-cloud租户登录，项目 > 计算 > 镜像 > 创建镜像
    + 根据提示填写，注意镜像格式的选择，一般我们都使用`QCOW2`镜像

- 命令行上传，参考`glance`命令

#### 查看镜像
```
# openstack image list              
+--------------------------------------+-----------------------------------------+--------+
| ID                                   | Name                                    | Status |
+--------------------------------------+-----------------------------------------+--------+
| c5747007-e11f-4362-8908-fc1d0e54c78f | centos-6.8                              | active |
| b62b640f-f104-4824-8d64-1e2c17fed839 | sahara-mitaka-cloudera-5.5.0-centos-6.7 | active |
| baf22807-fe7e-4fac-9197-440f7340b5e0 | CentOS-7-x86_64-GenericCloud            | active |
| 90fb2f59-b774-4a37-a950-318708c09e5a | CentOS-7-x86_64-GenericCloud-1604       | active |
| 91c5cae5-e7d0-4747-95b7-fc771ba6c69f | CentOS-6-x86_64-GenericCloud-1604       | active |
| c9bd8440-d278-4228-a54d-3ff90c3c59b3 | cirros                                  | active |
+--------------------------------------+-----------------------------------------+--------+
```


#### 镜像制作和详细介绍
参考：[openstack image guide](http://www.itweet.cn/blog/2016/08/09/openstack%20image%20guide)

### 云主机的创建
openstack中已经存在相关的镜像，如果你看到过之前的<openstack系列(1)-Kvm虚拟化技术>章节，会了解到云主机如果底层是用的`kvm`技术，那么需要提前通过kvm技术去生成模板虚拟机镜像文件,他可以支持多种格式,常用的`QCOW2`，通过这个镜像文件生成云主机。

通过`dashboard`创建云主机

- 步骤1  项目 > 计算 > 云主机 > 创建云主机
    + Instance Name：test   #云主机名称
    + 可用区域：nova
    + Count : 1   # 云主机个数,可以填写多个
    + 下一步
    + 选择，添加`cirros`选项
    + 下一步
    + 选择，添加`m1.tiny`选项
    + 下一步
    + 选择，`private`选项
    + 下一步
    + 下一步
    + 选择，`default`选项
    + 下一步
    + 选择，`coud`选项
    + 单机，`启动实例`    

    至此，云主机已经创建完成，等待初始化，启动完成。

- 步骤2  登录后台，检测云主机情况

```
# virsh list --all
 Id    Name                           State
----------------------------------------------------
 1     instance-00000001              running
```

如上通过kvm底层命令，查看云主机启动状态。

```
$ openstack server list
+--------------------------------------+------------------+--------+------------------------------------+
| ID                                   | Name             | Status | Networks                           |
+--------------------------------------+------------------+--------+------------------------------------+
| 757ac3bf-f61f-4118-9f28-7ce60fc7ae41 | test             | ACTIVE | private=172.16.12.51, 192.168.0.27  |
+--------------------------------------+------------------+--------+------------------------------------+
```
通过openstack查看云主机运行状态。

### 云主机的使用
云主机创建成功之后，我们通过`dashboard`可以登录云主机，也可以给云主机绑定一个公共的IP地址，通过这个IP地址去访问。
- 用户名：cirros
- 密码：cubswin:)

```
$ ssh cirros@192.168.0.27
cirros@192.168.0.27's password:

$ df -h
Filesystem                Size      Used Available Use% Mounted on
/dev                    242.3M         0    242.3M   0% /dev
/dev/vda1                23.2M     18.0M      4.1M  82% /
tmpfs                   245.8M         0    245.8M   0% /dev/shm
tmpfs                   200.0K     72.0K    128.0K  36% /run

$ hostname
test

$ ping www.baidu.com
PING www.baidu.com (220.181.111.188): 56 data bytes
64 bytes from 220.181.111.188: seq=0 ttl=53 time=2.306 ms

$ ifconfig eth0
eth0      Link encap:Ethernet  HWaddr FA:16:3E:20:E4:12
          inet addr:172.16.12.51  Bcast:172.16.12.255  Mask:255.255.255.0
```

通过如上操作，可以看到云主机已经正常工作，并且我们也可以登录到云主机去进行各种操作，云主机也能正常访问公网。

### 总结
本小节，主要是讲解如何通过可视化界面使用`openstack`最核心的云主机功能，并且开始正常使用云主机，云主机官方还提供更多版本，我们可以直接下载上传开始应用在我们的不同业务中，镜像文件是可以定制的，制作的时候可以让镜像具备某些功能，就和公有云，阿里云，aws云一样，创建好之后，云主机自带大数据服务能力、自带数据库能力等，底层即使用kvm相关技术进行制作，需要多实践才能深刻体会。下一节我们介绍openstack自动化扩容一个节点，欢迎关注。


原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


参考：http://www.itweet.cn/blog/2016/08/09/openstack%20image%20guide
