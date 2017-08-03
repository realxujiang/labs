企业级大数据平台部署实施参考指南 - 集群安装
---

集群的安装方式选择Ambari来进行自动化安装，目前Ambari是开源的大数据管理工具，而HDP是不开源。Ambari做为Apache顶级项目支持可插拔的管理各种不同的大数据发行版，每个公司有技术能力都可以做一个大数据版本，让Ambari进行管理，所以说Ambari其实是支持多平台的一款大数据自动化部署和管理软件。

###  Ambari安装

下载相关的repo文件，到需要安装ambari-server的主机上，命令如下：

```
curl http://you_yum_repo_ip/hdp/ambari.repo > /etc/yum.repos.d/ambari.repo
```

安装ambari-server

```
yum install ambari-server -y
```

配置Ambari-Server的JDK

```
wget http://public-repo-1.hortonworks.com/ARTIFACTS/jdk-7u67-linux-x64.tar.gz -O /var/lib/ambari-server/resources/jdk-7u67-linux-x64.tar.gz
wget http://public-repo-1.hortonworks.com/ARTIFACTS/UnlimitedJCEPolicyJDK7.zip /var/lib/ambari-server/resources/UnlimitedJCEPolicyJDK7.zip  
```

ambari-server配置

```
[root@ambari-server resources]# ambari-server setup
Using python  /usr/bin/python
Setup ambari-server
Checking SELinux...
SELinux status is 'enabled'
SELinux mode is 'permissive'
WARNING: SELinux is set to 'permissive' mode and temporarily disabled.
OK to continue [y/n] (y)? 
Customize user account for ambari-server daemon [y/n] (n)? 
Adjusting ambari-server permissions and ownership...
Checking firewall status...
Checking JDK...
[1] Oracle JDK 1.8 + Java Cryptography Extension (JCE) Policy Files 8
[2] Oracle JDK 1.7 + Java Cryptography Extension (JCE) Policy Files 7
[3] Custom JDK
==============================================================================
Enter choice (1): 2
JDK already exists, using /var/lib/ambari-server/resources/jdk-7u67-linux-x64.tar.gz
Installing JDK to /usr/jdk64/
Successfully installed JDK to /usr/jdk64/
JCE Policy archive already exists, using /var/lib/ambari-server/resources/UnlimitedJCEPolicyJDK7.zip
Installing JCE policy...
Completing setup...
Configuring database...
Enter advanced database configuration [y/n] (n)? 
Configuring database...
Default properties detected. Using built-in database.
Configuring ambari database...
Checking PostgreSQL...
Running initdb: This may take up to a minute.
Initializing database ... OK

About to start PostgreSQL
Configuring local database...
Configuring PostgreSQL...
Restarting PostgreSQL
Creating schema and user...
done.
Creating tables...
done.
Extracting system views...
ambari-admin-2.5.1.0.159.jar
...........
Adjusting ambari-server permissions and ownership...
Ambari Server 'setup' completed successfully.
```

启动ambari-server，通过提示监听8080端口，接下来就通过浏览器访问此端口进行可视化安装集群操作。

```
[root@ambari-server resources]# ambari-server start
Using python  /usr/bin/python
Starting ambari-server
Ambari Server running with administrator privileges.
Organizing resource files at /var/lib/ambari-server/resources...
Ambari database consistency check started...
Server PID at: /var/run/ambari-server/ambari-server.pid
Server out at: /var/log/ambari-server/ambari-server.out
Server log at: /var/log/ambari-server/ambari-server.log
Waiting for server start...........
Server started listening on 8080

DB configs consistency check: no errors and warnings were found.
Ambari Server 'start' completed successfully.
```

### HDP安装

浏览器访问http://your_ambari-server_ip:8080/#/login
用户名：admin
密    码：admin

通过登录页面进入集群安装向导，如下所示。

![launch-install-wizard](https://github.com/itweet/labs/raw/master/BigData/img/ambari-launch-install-wizard.png)

通过鼠标单击”Launch Install Wizard”按钮，通过11个setup引导步骤，进行可视化的集群安装。

####  Step1 - Get Started

步骤1，需要填入一个集群名称Cluster Name，点击下一步。例如：    

![Step1-Get-Started](https://github.com/itweet/labs/raw/master/BigData/img/Step1-Get-Started.png)

#### Step2 - Select Version

选择使用HDP的版本，默认支持4个HDP版本的安装部署，鼠标点击“Use Local Repository”填入之前制作的本地仓库源地址,点击下一步：

![Step2-Select-Version](https://github.com/itweet/labs/raw/master/BigData/img/Step2-Select-Version.png)

![Step2-Select-Version-2](https://github.com/itweet/labs/raw/master/BigData/img/Step2-Select-Version-2.png)

#### Step3 - Install Options

填写需要安装的目标主机节点的hosts映射名称，私钥信息填写为ambari-server所在节点，可以免密码登录所有节点的用户私钥信息。例如：一般通过root用户进行集群的安装，如下填写root用户” /root/.ssh/ id_rsa”文件内容。

![Step3-Install-Options](https://github.com/itweet/labs/raw/master/BigData/img/Step3-Install-Options.png)

点击“Register and Confirm”进入下一步。

#### Step3 - Confirm Hosts

在这个步骤ambari-server节点会并行去多台机器执行相关命令。首先scp相关的ambari-agent的setup脚本到多台机器，然后并行执行相关的命令进行ambari-agent的安装，注册ambari-agent节点到ambari-server。这里主要工作是在所有节点安装ambari-agent，并且把ambari-agent注册到ambari-server，让server可以控制所有的agent节点。之后ambari-server就可以控制所有的agent执行命令进行HDP集群的安装。

![Step3-Confirm-Hosts](https://github.com/itweet/labs/raw/master/BigData/img/Step3-Confirm-Hosts.png)

点击“Next”继续安装。

#### Step4 - Choose Services

选择你需要安装的服务，目前HDP提供了30多个组件的自动化安装和部署维护。如下图所示：

![Step4-Choose-Services](https://github.com/itweet/labs/raw/master/BigData/img/Step4-Choose-Services.png)

#### Step5 - Assign Masters

分配主节点所在主机，在分布式软件系统中，大多数都是有中心的结构，有主节点、从节点之分，所以这一步是对分布不是系统，主从架构的主节点角色分配，比如：HDFS NameNode安装在什么机器，Yarn ResourceManager安装在那个机器可以自主选择，当然如果你是第一次安装集群，就让它使用它默认自动选择的方式，避免调整角色分配导致安装失败。如下图：

![Step5-Assign-Masters-1](https://github.com/itweet/labs/raw/master/BigData/img/Step5-Assign-Masters-1.png)

![Step5-Assign-Masters-2](https://github.com/itweet/labs/raw/master/BigData/img/Step5-Assign-Masters-2.png)

#### Step6 - Assign Slaves and Clients

选择从节点和客户端所在主机，从节点和客户端是可以有多个的，可以进行自定义，默认会根据硬件做最小化选择从节点和客户端，这里可以根据需要选择从节点的分配。

- 从节点 – 有n个，一个节点就代表一台物理主机或者虚拟主机。 
- 客户端 – 有n个，一般是客户机上需要安装客户端，让客户机可以提交任务到集群。

![Step6-Assign-Slaves-and-Clients](https://github.com/itweet/labs/raw/master/BigData/img/Step6-Assign-Slaves-and-Clients.png)

#### Step7 - Customize Services

自定义服务器配置，在这个步骤可以修改一些默认识别的参数，比如：Namenode存储的元数据目录，DataNode存储数据的目录。

还有些服务，需要自己根据提示输入一些用户密码的内容，请牢记相关服务器输入的用户密码，因为这些会在后台Ambari-server数据库中创建相应的数据库。指不定那天就需要登录后台数据库解决一些问题。

![Step7-Customize-Services](https://github.com/itweet/labs/raw/master/BigData/img/Step7-Customize-Services.png)

#### Step8 - Review

在安装之前预览集群服务分配和节点相关信息是否正确，可以通过`Print`进行打印下载，查看更加详细的角色分配信息，如果检测没有任何问题，你就可以进行下一步`Deploy`了。

![Step8-Review](https://github.com/itweet/labs/raw/master/BigData/img/Step8-Review.png)

#### Step9 - Install, Start and Test

自动化安装、启动集群、自动化Test集群，根据你的硬件环境和网络相关因素，你需要等待一段时间，等集群自动化安装成功，所有主机`Status`都变成绿色进度条，那就可以点击`Next`。

![Step9-Install-Start-and-Test](https://github.com/itweet/labs/raw/master/BigData/img/Step9-Install-Start-and-Test.png)

#### Step10 – Summary

![Step10–Summary](https://github.com/itweet/labs/raw/master/BigData/img/Step10–Summary.png)

![ambari–dashboard](https://github.com/itweet/labs/raw/master/BigData/img/ambari–dashboard.png)

至此、集群安装完毕。

### 小结
本节内容主要讲解通过Ambari进行集群的自动化安装，在此过程中，一定要事先做好本地源，如果你是内网环境，需要事先具备两种源。

- HDP内网源
- LinuxOS源

一般通过Apache搭建内网源，搭建之后把相关的`os.repo`和`ambari.repo`放到ambari-server服务器`/etc/yum.repo.d/`,然后执行命令`yum search mysql && yum search ambari-server`验证是否具备相关源环境，如此这般，你才能如我文中所述步骤，顺利的一路绿色的成功部署集群。

实战内容设计的技术有Linux操作系统的安装，Linux网络配置，Linux磁盘分区，Linux基本参数优化，HDP和OS离线源搭建(Apache或者Nginx)，Ambari自动化部署大数据集群等...

《企业级大数据平台部署实施参考指南》分多节，有更多细节剖析，不妥之处欢迎指正！

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/