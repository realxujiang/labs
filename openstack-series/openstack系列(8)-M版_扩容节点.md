
### Adding a compute node

Expanding your single-node OpenStack cloud to include a second compute node requires a second network adapter, if you want to separate the Neutron tenant network traffic.

### Edit the answer file

First, edit the "answer file" generated during the initial Packstack setup. You'll find the file in the directory from which you ran Packstack.

`NOTE:` by default, $youranswerfile is called packstack-answer-$date-$time.txt

```
[root@openstack-controller ~]# ls packstack-answers-20160517-215941.txt
packstack-answers-20160517-215941.txt
```

### Change IP addresses
Change the value for `CONFIG_COMPUTE_HOSTS` from the value of your first host IP address to the value of your second host IP address. Ensure that the key `CONFIG_NETWORK_HOSTS` exists and is set to the IP address of your first host.

### Skip installing on an already existing servers
In case you do not want to run the installation over again on the already configured servers, add the following parameter to the answerfile:
```
EXCLUDE_SERVERS=<serverIP>,<serverIP>,...
```

Example:
```
[root@openstack-controller ~]# egrep "CONFIG_COMPUTE_HOSTS|CONFIG_NETWORK_HOSTS|EXCLUDE_SERVERS" packstack-answers-20160613-231012.txt
EXCLUDE_SERVERS=192.168.2.110
CONFIG_COMPUTE_HOSTS=192.168.2.110,192.168.2.111,192.168.2.112,192.168.2.113
CONFIG_NETWORK_HOSTS=192.168.2.110
```

### Re-run packstack with the new values
Run packstack again, specifying your modified answer file:

`NOTE:` by default $youranswerfile is called packstack-answer-$date-$time.txt

Example:
```
[root@openstack-controller ~]# cp packstack-answers-20160613-231012.txt packstack-answers-20160613-231012.txt.bak

[root@openstack-controller ~]# vi packstack-answers-20160613-231012.txt 

[root@openstack-controller ~]# egrep "CONFIG_COMPUTE_HOSTS|CONFIG_NETWORK_HOSTS|EXCLUDE_SERVERS" packstack-answers-20160613-231012.txt
EXCLUDE_SERVERS=192.168.2.110
CONFIG_COMPUTE_HOSTS=192.168.2.110,192.168.2.111,192.168.2.112,192.168.2.113
CONFIG_NETWORK_HOSTS=192.168.2.110

[root@openstack-controller ~]# sudo packstack --answer-file=packstack-answers-20160613-231012.txt
```

![Dilatation Node](https://github.com/itweet/labs/raw/master/openstack-series/img/dilatation-node.png)

check new compute node `openstack-compute-5`

```
# nova host-list
+----------------------+-------------+----------+
| host_name            | service     | zone     |
+----------------------+-------------+----------+
| openstack-controller | cert        | internal |
| openstack-controller | consoleauth | internal |
| openstack-controller | scheduler   | internal |
| openstack-controller | conductor   | internal |
| openstack-controller | compute     | nova     |
| openstack-compute-1  | compute     | nova     |
| openstack-compute-2  | compute     | nova     |
| openstack-compute-3  | compute     | nova     |
| openstack-compute-4  | compute     | nova     |
| openstack-compute-5  | compute     | nova     |
+----------------------+-------------+----------+
```

check Cloud-Host State
```
# virsh list --all
 Id    Name                           State
----------------------------------------------------
 1     instance-00000032              running
 2     instance-00000030              running
 3     instance-00000010              running
 4     instance-0000000e              running
 5     instance-00000034              running
```

adding a compute node done. check service normal.

reference：https://www.rdoproject.org/install/adding-a-compute-node/

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/