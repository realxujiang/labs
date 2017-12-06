about-ambari-new-feature
---

### Ambari 2.5 的新功能

Ambari 2.5，我们的专注点是继续提高日常Hadoop集群的运维和管理工作，Ambari整个社区都在努力让Ambari更加智能化易用的提供Hadoop集群的运营。Ambari 2.5 做出的重点改进如下：

- Service Management

- Log Management

- Configuration Management

- Monitoring

- Security

- Upgrades

### Service Management

支持`Service Auto Start`(AMBARI-2330, [文档](https://docs.hortonworks.com/HDPDocuments/Ambari-2.5.1.0/bk_ambari-operations/content/enable_service_auto_start.html))能力，集群管理人员可以设置策略，以确保组件在运行失败后能自动重新启动，并确保在服务器重启后组件重启。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/1-ServiceRestart-1024x624.png)

基于每个主机上的Ambari agent会主动检测托管组件是否异常退出，并且根据管理员设定的策略重启该组件。在启动时Agent会参考相关策略，并根据需要自动启动相关组件。

对于大型生产集群，我们增加了易于维护的功能特性，可以非常方便的`添加`或者`删除`JournalNodes(AMBARI-7748，[文档](https://docs.hortonworks.com/HDPDocuments/Ambari-2.5.1.0/bk_ambari-operations/content/manage_journal_nodes.html)）。此功能可以指导集群管理员通过可视化的方式对JournalNodes节点进行添加、删除和移动，对于大型集群来说启用HA功能保障集群高可靠，那么对`JournalNodes`节点的管理就显得非常重要。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/2-ManageJournalNodes-1024x623.png)

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/3-AssignJournalNodes-1024x624.png)

### Log Management

Hadoop生产环境中往往会产生大量的日志数据，日志的管理通常需要管理员非常熟悉Log4j的工作原理。通过最新的`日志轮询`(AMBARI-16880，[文档](https://docs.hortonworks.com/HDPDocuments/Ambari-2.5.1.0/bk_ambari-upgrade/content/upgrading_log_rotation_configuration.html))功能简化配置。目前在最新的版本中管理员可以非常容易的配置应该保留多少个文件，以及在什么时候轮询日志(基于文件大小)。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/4-LogRotation-1024x624.png)

`LogSearch`（技术预览）目前是最受欢迎的功能之一，在此版本中可以看到漂亮的UI，并可以根据用户操作进行后端刷新。日志的聚合搜索在下一个版本Ambari 3.0中UI将被简化，后端将会有更加强大的日志保留和扩展功能。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/5-Logsearch-1024x703.png)

### Configuration Management

Ambari在进行单一配置更改时，在不同服务中由于有配置依赖共用参数，某些参数修改会导致多个配置更改？Ambari希望在配置发生更改时，Ambari能及时更新相关的从属配置。如果集群某些配置发生改变，而从属配置的修改没有让管理员能可视化的看到这样是非常不正确的。我们做了许多研究，通过配置更改通知功能，以确定目前集群最佳的配置建议。此外，我们还添加了可视化的弹出窗口和对话框通知，以确保管理员能看到配置建议，并根据经验选择保存修改或者修改部分配置。使得集群在修改部分配置的时候，及时出错了，也不会影响其他组件的正常工作。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/6-ServiceAdvisor-1024x624.png)

一个大型的集群通常分工明确，有架构师、运维、开发、测试、管理，不同的人对集群的关注点不同，对于开发来说需要完整的集群客户端相关的配置信息，这个时候集群组件客户端配置导出功能就显得很重要。现在通过`下载所有客户端配置`功能，我们可以轻松的导出具有Ambari管理的每个服务的客户端配置gz文件包。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/7-DownloadClientConfig-1024x624.png)

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/8-DownloadClientConfigFile-1024x331.png)

### Monitoring

HDFS集群的监控非常重要，当你尝试找出NameNode为什么压力这么大，可能是那些原因导致的时候，缩小范围，通常直接排查像HDFS发送请求前10名用户，并且随着时间的推移，监控HDFS最常用的10个操作信息。使HDFS TopN用户和常用操作可视化，Grafana现在可以看到这些指标，使得故障排除更容易，并帮助您减少MTTB（mean time to blame），找出相关问题负责人。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/9-topn-1024x623.png)

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/10-topn-1024x652.png)

Ambari相关的监控指标已经通过可以很好的帮助运营一个Hadoop集群，利用好集群资源。而服务于Ambari监控指标存储的相关组件一直以来都有单点问题，如果该数据收集存储节点AMS奔溃将会导致指标完全丢失，对于一个企业级的大数据软件来说是不可承受的灾难，所以在Ambari 2.5中我们引入了`AMS Collector High Availability`做为技术预览。这意味着此功能可用，但尚未推荐用于生产环境部署。此功能针对大型集群多维度收集数据、写入和聚合指标优化，保障大量监控指标实时入库和快速读取，添加相关监控指标项无需重启集群组件优点。这种高可靠对企业级用户来说，可以最大化保障AMS的价值。

![](https://2xbbhjxc6wk3v21p62t8n4d4-wpengine.netdna-ssl.com/wp-content/uploads/2017/08/11-AMS-HA.png)

### Security

对于集群安全性一直是我们重点关注的方向，在最新的版本中Hive，Oozie，Ranger和Log Search增加了`Password Credential Store Management `功能。此功能使得Hadoop集群更加的安全。

此外还支持自动化的LDAP和Kerberos支持。

Ambari REST API在未来的版本中会支持基于Kerberos的身份认证能力。

### Upgrades

没有人想要停机进行集群的升级，甚至为了不想数据丢失风险而进行数据备份升级。Ambari最新的滚动升级功能，可以避免在升级过程中停机时间太长，这里提供一种保守的方法，确保升级过程中不会有数据丢失风险。通过滚动升级总持续时间会比快速升级更长。在Ambari 2.5中，提供了滚动升级期间有能力`暂停`，以获得重新对集群的操作控制，防止出现的任务状况。一个常见的问题，如果滚动升级需要几天时间，如果我的HiveServer2实例有个问题，需要重启，会发生生么？这就是为什么要添加`暂停`功能。你只需要点击`暂停`按钮，最小化升级窗口，然后完全控制集群以重新启动HiveServer2。完成此操作之后，只需要点击`Resume`即可继续完成升级。

### DID YOU KNOW?

脚本报警：在于客户交流中，我们会经常被问到Ambari如何配置发送报警信息到HipChat或Slack或Pager Duty的问题。Ambari其实是有提供这样的功能的[脚本报警](https://cwiki.apache.org/confluence/display/AMBARI/Creating+a+Script-based+Alert+Dispatcher)。此功能允许您定义在Ambari中触发警报时应调用的脚本，以便您轻松地与外部系统集成。所以下次如果你想发送一个Ambari Alert到你的自定义接收系统，配置一个脚本报警即可。

**下半年是项目季，好忙...研发告一段落，开始奔波各种项目**

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/



