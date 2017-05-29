Openstack系列-自动化部署完成之后，此篇文章讲解企业级私有云后端云盘存储选型。按照之前系列文章中介绍的openstack集群安装之后，系统自带一个基于lvm vloume的cinder存储。

## Dependencies
```
[root@openstack-controller ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 
[root@openstack-compute ~]# cat /etc/redhat-release 
CentOS Linux release 7.2.1511 (Core) 
```

##  使用Gluster && LVM Vloume

### 1. Install glusterfs

`RDO`安装的时候，已经自动安装了部分glusterfs包,并且需要通过rdo提供的源来安装glusterfs,
否则会有一些依赖冲突问题,导致无法安装成功。

以下命令在所有准备安装glusterfs集群的服务器都执行：
```
$ rpm -qa | grep gluster*     

glusterfs-client-xlators-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-api-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-libs-3.7.1-16.0.1.el7.centos.x86_64

$ yum install wget -y

$ yum install centos-release-gluster37         # ==> CentOS-Gluster-3.7.repo

$ rpm -qa *gluster*
glusterfs-client-xlators-3.7.1-16.0.1.el7.centos.x86_64
centos-release-gluster37-1.0-4.el7.centos.noarch
glusterfs-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-api-3.7.1-16.0.1.el7.centos.x86_64
glusterfs-libs-3.7.1-16.0.1.el7.centos.x86_64

$ yum clean all

$ yum install glusterfs-server

$ service glusterd start / systemctl start glusterd.service
$ service glusterd status / systemctl status glusterd.service

$ systemctl enable glusterd.service
$ systemctl is-enabled glusterd.service

$ ps aux|grep gluster|wc -l
2
```

### 2. glusterfs cluster configuratioin
```
From "server1"
    gluster peer probe server2

From "server2"
    gluster peer probe server1

[root@openstack-controller ~]# gluster peer probe openstack-compute-1
peer probe: success. 
[root@openstack-controller ~]# gluster peer probe openstack-controller
peer probe: success. Probe on localhost not needed
```

### 3. glusterfs volume manager

你需要在两台主机执行如下命令，创建出glusterfs使用的本地磁盘目录地址。
```
mkdir /var/glusterfs/exp1 -p
```

你需要在glusterfs任意一台主机执行,如下命令,replica代表副本数量，可以理解为raid1,这个是glusterfs做为分布式文件系统，为cinder提供数据安全的有效保障：
```   
[root@openstack-controller ~]# gluster volume create cinder-volome01 replica 2 openstack-centos:/var/glusterfs/exp1 openstack-compute:/var/glusterfs/exp1 

＃创建带2份数据拷贝的卷
volume create: cinder-volome01: success: please start the volume to access data

[root@openstack-controller ~]# gluster volume start cinder-volome01 #启动卷

volume start: cinder-volome01: success

[root@openstack-controller ~]# gluster volume info

Volume Name: cinder-volume01
Type: Replicate
Volume ID: efe3c9a1-4bf9-4e45-a136-00ce8cd05d9f
Status: Started
Number of Bricks: 1 x 2 = 2
Transport-type: tcp
Bricks:
Brick1: openstack-centos:/var/glusterfs/exp1
Brick2: openstack-compute:/var/glusterfs/exp1
Options Reconfigured:
performance.readdir-ahead: on

[root@openstack-controller ~]# gluster
gluster> peer status
Number of Peers: 1

Hostname: openstack-compute
Uuid: bbcc8087-a584-4b7d-9631-cbd1e2e7151b
State: Peer in Cluster (Connected)

gluster> pool list
UUID                                    Hostname                State
bbcc8087-a584-4b7d-9631-cbd1e2e7151b    openstack-compute       Connected 
bc854ea5-8f67-4637-bf13-d2a46b109eb4    localhost               Connected 

gluster> volume info 
Volume Name: cinder-volume01
Type: Replicate
Volume ID: efe3c9a1-4bf9-4e45-a136-00ce8cd05d9f
Status: Started
Number of Bricks: 1 x 2 = 2
Transport-type: tcp
Bricks:
Brick1: openstack-controller:/var/glusterfs/exp1
Brick2: openstack-compute:/var/glusterfs/exp1
Options Reconfigured:
performance.readdir-ahead: on
```

### 4. Cinder plugin glusterfs and lvm volume
默认cinder自带lvm volume卷功能，其实cinder可以同时支持多种后端存储方式共存，下面介绍lvm,glusterfs共存的配置信息内容。

以下内容请在cinder安装节点执行：
```
[root@openstack-controller ~]# vim /etc/cinder/glusterfs_shares
  192.168.0.11:/cinder-volume01

[root@openstack-controller ~]# vim /etc/cinder/cinder.conf
  
enabled_backends=lvm,GlusterFS_Driver

[lvm]
iscsi_helper=lioadm
volume_group=cinder-volumes
iscsi_ip_address=192.168.0.11
volume_driver=cinder.volume.drivers.lvm.LVMVolumeDriver
volumes_dir=/var/lib/cinder/volumes
iscsi_protocol=iscsi
volume_backend_name=lvm

[GlusterFS_Driver]
volume_group=GlusterFS_Driver
volume_driver=cinder.volume.drivers.glusterfs.GlusterfsDriver
volume_backend_name=GlusterFS-Storage
glusterfs_shares_config = /etc/cinder/glusterfs_shares
glusterfs_mount_point_base = /var/lib/cinder/glusterfs

[root@openstack-controller ~]# mkdir /var/lib/cinder/glusterfs
[root@openstack-controller ~]# chown cinder:cinder /var/lib/cinder/glusterfs/

[root@openstack-controller ~]# systemctl restart openstack-cinder-volume.service

[root@openstack-controller ~(keystone_admin)]# cinder type-create GlusterFS
+--------------------------------------+-----------+-------------+-----------+
|                  ID                  |    Name   | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| 4e236e8f-6592-45fc-a25a-b2f189f90439 | GlusterFS |      -      |    True   |
+--------------------------------------+-----------+-------------+-----------+

[root@openstack-controller ~(keystone_admin)]# source keystonerc_admin 

[root@openstack-controller ~(keystone_admin)]# cinder type-key GlusterFS set volume_backend_name=GlusterFS-Storage

[root@openstack-controller ~]# mount|grep glusterfs   #验证完成，说明glusterfs挂载成功
192.168.0.11:/cinder-volume01 on /var/lib/cinder/glusterfs/3e58f5c16b6f5406de3c8f9eb2623ad0 type fuse.glusterfs (rw,relatime,user_id=0,group_id=0,default_permissions,allow_other,max_read=131072)

[root@openstack-controller ~]# cat /etc/cinder/cinder.conf |grep glusterfs_shares
glusterfs_shares_config = /etc/cinder/glusterfs_shares
```

通过此命令可以查看openstack相关命令：
```
# systemctl |grep openstack|wc -l
35
```

cinder相关命令：
```
[root@openstack-controller ~(keystone_admin)]# cinder type-list
+--------------------------------------+-----------+-------------+-----------+
|                  ID                  |    Name   | Description | Is_Public |
+--------------------------------------+-----------+-------------+-----------+
| 038cb62b-6905-43bd-a4b2-632d171c6d3d |   iscsi   |      -      |    True   |
| 5e8fa387-cb4d-4dee-b0d2-9646f82c2008 | GlusterFS |      -      |    True   |
+--------------------------------------+-----------+-------------+-----------+

[root@openstack-controller ~(keystone_admin)]# cinder list
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |        Name       | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+
| 8d320989-f6f0-4c36-9ffc-9955e65d5390 | available | glusterfs-test-01 |  1   |  GlusterFS  |  false   |             |
| af4777b6-7ab1-4b00-a4d6-757f6c03bb7c | available | glusterfs-test-02 |  1   |  GlusterFS  |  false   |             |
| cd2b9a15-b3d8-4e4e-8fa0-9b27e6503144 | available |     test-iscsi    |  1   |    iscsi    |  false   |             |
+--------------------------------------+-----------+-------------------+------+-------------+----------+-------------+

[root@openstack-controller ~(keystone_admin)]# cinder service-list 
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+
|      Binary      |                Host               | Zone |  Status | State |         Updated_at         | Disabled Reason |
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+
|  cinder-backup   |          openstack-controller         | nova | enabled |   up  | 2016-05-26T19:37:18.000000 |        -        |
| cinder-scheduler |          openstack-controller         | nova | enabled |   up  | 2016-05-26T19:37:23.000000 |        -        |
|  cinder-volume   | openstack-controller@GlusterFS_Driver | nova | enabled |   up  | 2016-05-26T19:37:22.000000 |        -        |
|  cinder-volume   |        openstack-controller@lvm       | nova | enabled |   up  | 2016-05-26T19:37:16.000000 |        -        |
+------------------+-----------------------------------+------+---------+-------+----------------------------+-----------------+

-- volume - lvm
$ systemctl status openstack-cinder-volume.service

-- lvm 查看lv信息
$ lvdisplay 
```

## Dashboard
 登录到可视化页面，点击选择卷，创建云硬盘按钮，即可看到两种云硬盘类型，基于lvm创建iscsi类型和glusterfs的类型。最终效果如下图：
![](http://itweet.github.io/screenshots/openstack-cinder-volume.png)

## NFS and Other Storage driver
  按照相关文档完成安装,最后修改cinder.conf文件，和cinder整合，举列如下:

For NFS:
```
yum install -y nfs-utils rpcbind

mkdir /data/nfs -p

cat /etc/exports
/data/nfs 192.168.0.0/24(rw,sync,no_root_squash)

/bin/systemctl start  rpcbind.service
/bin/systemctl status  rpcbind.service  
/bin/systemctl start nfs.service  
/bin/systemctl status nfs.service  
/bin/systemctl reload nfs.service 

$ sudo exportfs -rv 
exporting 192.168.0.0/24:/data/nfs

$ showmount -e  192.168.0.11
Export list for 192.168.0.11:
/data/nfs 192.168.0.0/24

cat /etc/cinder/nfs_shares
192.168.0.11:/data/nfs
```

Cinder Multiple Storage configuartion: 
```
$ vim /etc/cinder/cinder.conf
[DEFAULT]  
enabled_backends = lvm,GlusterFS_Driver,ibm,NFS-Driver
  
[lvm]  
volume_driver = cinder.volume.drivers.lvm.LVMVolumeDriver  
volume_backend_name=LVM  
volume_group = cinder-volumes  
iscsi_protocol = iscsi  
iscsi_helper = lioadm  
  
[GlusterFS_Driver]
volume_group=GlusterFS_Driver
volume_driver=cinder.volume.drivers.glusterfs.GlusterfsDriver
volume_backend_name=GlusterFS-Storage
glusterfs_shares_config = /etc/cinder/glusterfs_shares
glusterfs_mount_point_base = /var/lib/cinder/glusterfs 

[NFS-Driver]
volume_group=NFS-Driver
volume_driver=cinder.volume.drivers.nfs.NfsDriver
volume_backend_name=NFS-Storage
nfs_shares_config=/etc/cinder/nfs_shares
nfs_mount_point_base=$state_path/mnt

[ibm]  
volume_driver = cinder.volume.drivers.ibm.storwize_svc.StorwizeSVCDriver  
san_ip = 192.168.0.11  
san_login = www.itweet.cn  
san_password = 123456  
storwize_svc_volpool_name = vtt1  
storwize_svc_connection_protocol = iSCSI  
volume_backend_name=IBM  

$ cinder type-create NFS
$ cinder type-key NFS set volume_backend_name=NFS-Storage

$ systemctl restart openstack-cinder-volume

$ cinder service-list
```

## Openstack Glance
 openstack image
```
(openstack) help image 
Command "image" matches:
  image add project
  image create
  image delete
  image list
  image remove project
  image save
  image set
  image show

openstack image create "demo" --file /tmp/demo.img --disk-format qcow2 --container-format bare --public
```

## openstack ceph
[待续...](http://my.oschina.net/JerryBaby/blog/376858)

## 总结
 openstack多种后端存储，也是由于商业案例越来越多，导致需要多种存储系统满足不同的业务需求，从这一点看前途光明的确解决很多现实问题。cinder发展为支持多后端存储方式是必然趋势，因为有很多企业级存储系统需要整合；而很多大厂对openstack不予余力的投入社区开发也促使他更快的成熟。swift，glance组件用来存储其他类型数据,解决块存储，对象存储,镜像存储问题，也是分而治之的道理。在玩openstack的时候就会发现，各种各样的组件，无意是增加了学习的复杂度，使用维护上面也非常复杂，进而导致安装非常复杂。安装根本就不是安，就只剩下装，装完这个装那个，这组件安装失败，另外组件起不来，说多了都是泪啊。不过redhat做了一个基于puppet自动化安装脚本，相对来说方便了不少；这样一键安装的缺点也显而易见，都不知道有多少组件，出问题怎么排查，所以还得对各个组件的功能和配置非常熟悉，才能对症下药解决问题。我写openstack实际使用系列文章，也是为了让想学习openstack的人更容易入门，后续openstack系列完结后，我会开源一个基于saltstack自动化部署openstack的软件开源到我的[Github](https://github.com/itweet)上面。欢迎关注。

## FAQ
 Centos6.x --> Centos7.x 多了些变化，慢慢熟悉
```
systemctl is-enabled iptables.service
systemctl is-enabled servicename.service #查询服务是否开机启动
systemctl enable *.service #开机运行服务
systemctl disable *.service #取消开机运行
systemctl start *.service #启动服务
systemctl stop *.service #停止服务
systemctl restart *.service #重启服务
systemctl reload *.service #重新加载服务配置文件
systemctl status *.service #查询服务运行状态
systemctl --failed #显示启动失败的服务
```

参考：http://gluster.readthedocs.io/en/latest/Quick-Start-Guide/Quickstart/
     http://www.gluster.org/community/documentation/index.php/GlusterFS_Cinder
     https://www.gluster.org/