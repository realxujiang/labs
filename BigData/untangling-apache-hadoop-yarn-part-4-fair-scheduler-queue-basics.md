解密Apache Hadoop YARN ，第四部分：Fair Scheduler Queue Basics
---

在这部分的中， 我们对Fair Scheduler如何运行进行深入了解， 以及其运行原理。

在本系列的第3部分中， 为您提供了关于Fair Scheduler的一个简介， 其一是在Apache Hadoop YARN 选择 scheduler ，（另一个是Cloudera推荐的）在第4部分中，我们将使用一些案例介绍大部分队列属性的使用方法和局限性。

### 队列属性

默认情况下Fair Scheduler默认仅使用一队队列。创建额外的队列，设置适宜的属性可让应用程序在集群上运行更多的细粒度权限。

### FairShare
FairShare是大量的YARN集群资源。我们将使用<memory: 100GB, vcores: 25>符号表示100GB和25V的FairShare。

### *Share Weights*

```
<weight>Numerical Value 0.0 or greater</weight>
```

- 请注意：
    + 权重决定了相关兄弟节点队列的资源量，例如， 下面的案例中：
        * YARN集群大小是1000GB，200 vcores。
        * X队列的权重是0.25。
        * 其他队列的总权重是0.75
        * X队列的FairShair是<内存: 250GB, vcores: 50>
        
    + 如果在队列或者子队列中至少有一个活跃的应用程序，那么这个队列精细分配的公平共享资源会被强制执行。如果集群上的可用资源是等量的，那么这种限制很快就能被满足。否则，这则这些资源就会被当做其他队列完成任务的可用资源。

    + 这是推荐的队列分配办法。

### 资源限制

以下是资源限制的两种类型：

```
<minResources>20000 mb, 10 vcores</minResources>
<maxResources>2000000 mb, 1000 vcores</maxResources>
```

- 请注意：
    + minResources限制是一种软限制，只有队列总资源需求大于或者等于minResources的需求才会被强制执行，如果以下两点是真的，那么minResources至少能分到规定的量。
        * 有足够的资源或者从其他队列抢占资源
        * minResources总和不大于集群的总资源
        
    + maxResources 限制是硬性限制， 意味着它会持续强制执行。这种队列属性使用总资源，此外它的子队列和派生队列必须遵守这种属性。
    
    + 不推荐使用minResources/maxResources。 因为以下几大缺点：
        * 所有的值都是静态值，因此， 一旦集群大小改变他们也需要更新。
        * maxResources限制集群的使用， 因此队列不能超出配置的maxResources使用集群上任何可用的资源。
        * 如果队列的minResources比FairShare大，那么它可能会给其他队列的FairShare带来不利的影响。
        * 以前， 使用minResources就可以很快抢占一大块资源，但是现在没必要了， 因为FairShare-based 抢占已经有了显著改善。我们会在后面讨论详细细节。

### 限制应用程序

有两种方式可以限制队列的应用程序

```
<maxRunningApps>10</maxRunningApps>
<maxAMShare>0.3</maxAMShare>
```

- 请注意：
    + maxRunningApps限制是硬性限制，它的队列使用总资源，此外子队列和其他派生队列都必须遵守这种属性。
    + maxAMShare限制是硬性限制，这种分数代表队列总资源分配给ApplicationMasters的百分比。
        * maxAMShare小集群上设置既简便又能运行大量的应用程序。
        * 默认值是0.5. 这种默认设置可以保证一半的资源可用于运行 non-AM 容器。

### 用户和管理员

这些属性用于控制谁可以提交到队列上， 谁可以管理队列的应用程序。

```
<aclSubmitApps>user1,user2,user3,... group1,group2,...</aclSubmitApps>
<aclAdministerApps>userA,userB,userC,... groupA,groupB,...</aclAdministerApps>
```

请注意：如果yarn.acl.enable在yarn-site.xml里设置为True。那么yarn.admin.acl 就会被认为是除了aclAdministerApps队列属性以外唯一有效的管理员。

### 队列布局策略
一旦您完成队列的配置，队列布局策略都是为以下目的服务的：
- 应用程序提交到集群上，每一个应用程序分配到相应的队列。
- 定义什么类型的队列可以创建在“on the fly”。

队列布局规则阐述了在队列的什么位置放置应用程序， 队列布局规则是：

```
<queuePlacementPolicy>
  <Rule #1>
  <Rule #2>
  <Rule #3>
  .
  .
 </queuePlacementPolicy>
```

首先配对“Rule #1”，如果配对失败，那么就配对“Rule #2”直到与某一个规则配对成功。有一条预设置规则可供选择， 他们的行为可以建模为流程表。最后一条规则必须是终端规则，既不是默认规则也不是拒绝规则。

***特殊情况：使用“create”属性在on the fly 上创建队列***

所有的队列布局规则规定支持一个称作Create的可以设置为“true”或者“false”的XML属性，例如：
```
<rule name=”specified” create=”false”>
```

如果创建属性是TRUE 并且已经不存在了，那么规则支持特殊规则创建名称决定的队列。。如果创建属性是false这种规则就不支持创建队列， 那么队列布局就会移到下一条规则。

### 队列布局规则

这一节为每种类型的队列布局策略给出了一种案例并提供了流程图，如何决定调度程序用在那个应用程序上，那种队列上，（或者应用程序是否创建一个新的队列）

#### 规则：详细说明

- 总结：明确地指定应用程序到哪一队列。
- XML的规则实例：<rule name="specified"/>
- Hadoop命令指定的队列示例: hadoop jar mymr.jar app1 -Dmapreduce.job.queuename="root.myqueue"
- 流程图：

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f1.png)

#### 规则：用户
- 总结：分配应用程序到队列，那么队列就以提交应用程序的用户命名，例如：如果Fred是启动YARN程序的用户， 那么流程图中的队列就是root.fred。
- XML的规则实例：<rule name="user"/>
- 流程图：

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f2.png)

#### 规则： primaryGroup
- 总结： 分配应用程序到队列， 队列以用户属于哪一组primaryGroup命名。例如， 如果启动应用程序的用户属于市场组， 那么队列在流程图中将是root.marketing。
- XML的规则实例：<rule name="primaryGroup"/>。
- 流程图：

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f3.png)

#### 规则：secondaryGroupExistingQueue

- 总结：分配程序到队列，队列以属于用户的以第一个有效secondary group（换句话说，不是primary group）命名。例如用户属于secondary组market_eu, market_auto, market_germany, 那么流程表里的队列将重复搜集 root.market_eu, root.market_auto, and root.market_germany.

- XML的规则实例：<rule name="secondaryGroupExistingQueue"/>

- 流程图

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f4.png)

#### 规则：nestedUserQueue
- 总结： 创建一个和`root`队列不同的`user`队列。“other queue”是由附在nestedUserQueue规则上的规则决定的。

- 模板
```
<rule name="nestedUserQueue" create=”true”>
        <!-- Put one of the other Queue Placement Policies here. -->
    </rule>
```

- XML的规则实例：
```
<rule name="nestedUserQueue" create=”true”>
        <rule name="primaryGroup" create="false" />
    </rule>
```

- 请注意：这种规则创建的用户队列在队列之下不是`root`队列。队列布局策略首先在内部计算， 然后在再下面创建用户队列。请注意， 如果nestedUserQueue规则没有设置create="true" 的属性， 那么除非有一个特殊用户队列已经存在，应用程序才可以提交。

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f5.png)

#### 规则：default
-   总结：定义默认队列。
-   XML的规则实例：<rule name="default" queue="default" />
-   流程图：

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f6.png)

#### 规则：reject
- 总结：如果你想避免最后提交应用程序的默认行为，拒绝提交应用程序通常用作最后一条规则。
- XML的规则实例：<rule name="reject"/> 。 
- 请注意：如果一条标准的Hadoop jar 被这条规则拒绝，该错误信息 java.io.IOException：无法运行作业：应用程序就会出现被 队列布局策略拒绝的情况。
- 流程图：

![](https://github.com/itweet/labs/raw/master/BigData/img/yarn4-f7.png)

---

**工具条：Application Scheduling Status**

正如本系列1讨论过的情况一样，有一个或者多个任务组成的应用程序， 每项任务都在同一个容器里面运行。这篇文章的目的是， 应用程序可能的四分之一状态是：
-   待定的应用程序尚未分配任何容器。
-   活跃的应用程序有一个或者多个容器在集群上运行。
-   饥饿程序是一种很活跃的应用程序， 对资源的需求非常突出。
-   结束了的应用程序意味着它已经完成了所有任务。

----

### 案例：运行应用程序的集群

假如我们有一个YARN集群，总共资源是 <内存: 800GB, vcpu 200V>，有两排队列： root.busy (权重=1.0)和root.sometimes_busy （权重=3.0）。以下是四种有趣的方案：

- 方案A：繁忙的队列充满了应用程序，sometimes_busy 队列只有少量的程序运行 (比如说 10%, i.e. <内存: 80GB, vcpu: 20>。很快， 大量的应用程序在相对较短的时间窗口添加到 sometimes_busy 队列。所有新的应用程序在sometimes_busy 中待定， 但是会随着繁忙队列完工后很快活跃起来。如果繁忙队列的任务是短期任务， 那么sometimes_busy 队列的应用程序不用等很久就能分配到容器。然而，如果繁忙队列的任务需要很长时间完成， 那么sometimes_busy 队列里的新应用程序就会待定很久。无论哪一种情况下，一旦应用程序在sometimes_busy 队列变得活跃起来，繁忙的队列中很多正运行的应用程序将需要更长的时间才能完成。

- 方案B：busy和sometimes_busy 的队列都满了或者接近满了活跃的待定程序。在这种情况下，集群将维持充分利用的情况。每一队列都会使用公平共享资源， 繁忙队列应用程序总数使用集群资源的25%， sometimes_busy 队列的应用程序总数使用剩余的75%。

因此， 怎么避免情况A呢？

一种解决方案是在busy队列设置maxResources 。假设设置在busy队列的maxResources等于集群的25%。因为maxResources是硬性限制， busy队列的应用程序就会一直被限制在25%的资源范围内。那么这样就可以100%使用集群资源， 集群利用率接近35%，（10%是sometimes_busy 队列， 25%是busy队列）

情况A就会显著改善，因为集群上的闲置资源只能用于sometimes_busy 队列的应用程序。 但是集群的平均利用率可能会降低。

#### 更多的公平共享资源的定义：
-   稳定的公平共享资源：理论上一个队列的公平共享值是基于集群大小和集群上队列的权重。
-   即时资源共享： 通过集群上的每个队列的资源调度器计算公平共享值。这种值和稳定的公平共享资源在两方面有所不同：
—不分配任何资源到空白队列。
—当所有队列达到或者超出容量是，该值等于稳定的公平共享资源。
-  分配：等于队列里所有运行中的程序占用的资源总和。

现在开始， 我们将即时公平共享资源当做普通的公平共享资源。

#### 抢占资源的案例

鉴于这些新定义， 之前的情况可以表述如下：

- 情况A：
    + sometimes_busy队列分配到的值是<内存: 80GB, vcpu: 20V> 而公平共享资源值是<内存: 600GB, vcpu: 150V>.
    + Busy队列分配到的值是<内存: 720GB, vcpu: 180V> 而公平共享资源值是<内存: 200GB, vcpu: 50V>.

- 情况B：
    + 两种队列的即时公平共享资源都等于稳定的公平共享资源。
    
情况A中， 您可以看到在分配和公平共享资源之间两组队列的不平衡。，平衡慢慢恢复随着容器从 busy队列释放然后分配到sometimes_busy 队列。

通过打开抢占功能， 公平调度器可以在busy队列中杀死容器然后更迅速分配把他们sometimes_busy 队列。

#### 为抢占功能配置公平调度器

为了打开抢占功能， 在yarn-site.xml中设置这种属性：
```
<property>yarn.scheduler.fair.preemption</property>
<value>true</value>
```

然后， 在您的公平调度器里分配文件， 可以通过fairSharePreemptionThreshold在队列上配置抢占，然后 fairSharePreemptionTimeout就会像下面示例中所示，fairSharePreemptionTimeout是秒的数目，在它尝试从其他队列抢占容器夺取资源之前队列是在fairSharePreemptionThreshold之下。

```
<allocations>
  <queue name="busy">
    <weight>1.0</weight>
  </queue>
  <queue name="sometimes_busy">
    <weight>3.0</weight>
    <fairSharePreemptionThreshold>0.50</fairSharePreemptionThreshold>
    <fairSharePreemptionTimeout>60</fairSharePreemptionTimeout>
  </queue>
 
 <queuePlacementPolicy>
    <rule name="specified" />
    <rule name=”reject” />
 </queuePlacementPolicy>
</allocations>
```

还记得sometimes_busy 队列的公平共享资源是 <内存: 600GB, vcpu: 150V>。这两个新属性提示公平调度器，sometimes_busy 队列在开始抢占之前会等待60秒。如果在那段时间， 它没有收到公平共享资源50%的资源， 公平调度器就会开始在busy队列杀容器并分配到sometimes_busy 队列。

* 请注意这几件事：
    - fairSharePreemptionThreshold的值比0.0大（设置成0.0类似关闭抢占功能）但是比1.0小（因为1.0会将全部的公平共享资源归还到队列需要的资源）
    - 这种配置里的抢占将杀死busy队列里的容器然后将他们分配到sometimes_busy队列。
        + 对方无法实现抢占功能因为busy队列没有设置抢占属性。
        + 抢占不会杀sometimes_busy 队列中应用程序A的容器分配到应用程序B中。

(请注意：我们不会在一个队列中覆盖minResources和minSharePreemptionTimeout。目前推荐公平共享抢占。)

### 补充阅读
如果想要获取更多关于公平调度器的信息， 可以查阅在线文档（[Apache Hadoop](http://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/FairScheduler.html) 和[CDH](http://archive.cloudera.com/cdh5/cdh/5/hadoop/hadoop-yarn/hadoop-yarn-site/FairScheduler.html)版本都可用）

### 总结

1. 队列上可以设置很多队列属性， 包括限制资源， 限制应用程序， 设置用户和管理员， 设置调度策略。
2.  队列配置文件应当包括队列布局策略，队列布局策略定义了队列上如何分配应用程序。
3.  在队列上运行的应用程序可以保持应用程序在不同的队列待定或者处于饥饿状态。在公平调度器中配置抢占功能可以更迅速的调节不平衡。

### 下一部分

[第五部分](http://blog.cloudera.com/blog/2017/02/untangling-apache-hadoop-yarn-part-5-using-fairscheduler-queue-properties/)将提供更具体的例子， 例如工作优先次序， 如何使用队列，如何利用属性处理这种情况。


译文原文：https://blog.cloudera.com/blog/2016/06/untangling-apache-hadoop-yarn-part-4-fair-scheduler-queue-basics/

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.png)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


