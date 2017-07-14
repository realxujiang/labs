如何针对生产调整Apache Solr 的内存
---

正确配置Apache Solr内存对于生产系统的稳定性和性能至关重要。在相互矛盾的目标之间找到平衡点真的很难。还需要考虑隐含的或明确的多个因素。这篇文章介绍了内存调优的一些常见任务，并指导您完成该过程，以帮助您了解如何为生产系统配置Solr内存。

为了操作简单起见，这篇文章采用在HDFS上运行的Cloudera CDH5.11中的Solr。 该平台依赖于oracle jdk8和64位Linux。这篇文章分为两部分。

### 内存调优的常见任务

在详细介绍之前，让我们来看一下在内存调优需要解决的基本问题。为了避免JVM内存不足（OOM）或巨大的GC开销，内存调优的首要任务是JVM堆大小必须与Solr的内存需求相匹配。JVM堆大小的设置很简单。在Solr中配置配置（Cloudera Manager -> Solr configuration -> heap size）。另一方面，Solr的内存需求差异取决于索引大小、工作负载和配置。本文将向您展示如何正确估算索引大小、工作负载和配置，这样您就可以匹配JVM堆大小和Solr内存需求。

内存调优的另一个常见任务是找到内存使用情况和性能之间的最佳平衡点。 通常，Solr的内存越多，实施越好，但并不总是这样。另一方面，给出的内存越多，硬件成本越高，JVM GC开销越大。平衡点是一个固定的点，如果给出的内存大于最佳平衡点，则性能改进不能再使这些弊端被合理化接受。在本文中，我们将向您展示一些案例关于如何在选择最佳堆大小时找到最有效的点，以及一些其他通用优化Solr的最佳实践。

JVM GC调优也是一种常见的任务。 一般Solr对GC都是很友好的，在大多数情况下无需太多调整 。该博客将涵盖几个可以提高Solr性能的最关键的GC调整旋钮。

### Solr如何使用内存

在我们开始评估Solr内存需求之前，我们先看一下Solr如何使用内存。Solr使用的两种内存类型是堆内存和直接内存（通常称为off-heap。直接内存用于缓存从文件系统读取的块，类似于Linux文件系统缓存。针对堆内存，下图显示了Solr中不同类型的主要用户。

![](https://github.com/itweet/labs/raw/master/BigData/img/Cloudera_diagram_Solr_server_heap.png)

如您所见，多个缓存在使用大部分的堆内存，除了字段缓存以外，其他缓存都在per core中。Solr 内核是索引的一部分。 Solr服务器通常有多个内核。缓存能使用的最大内存由配置在solrconfig.xml中的单个缓存大小控制。

### 开始使用

调整之前，请确保您的系统在索引大小和工作负载方面的平衡。例如，使用shard router、或可以在生产工作负载下创建大小相等集合和内核的collection alias。还要确保所有的内核在所有节点上均匀分布。如果您想了解有关平衡设计的更多细节，请留意未来Cloudera工程博客。

由于Solr内存需求取决于索引大小、工作负载，而在所有Solr节点上均匀的分布索引和工作负载，大大简化了内存调整 ，避免了所有单个节点的瓶颈，最终还有助于系统性能的稳定性。该示例假设、在所有Solr节点之间均匀的分布了索引和工作负载。

而第一步在生产中部署Solr ，使用一组“safe”配置参数启动Solr是个不错的方法。可能这种方法性能不是最好的，但是能确保Solr的稳定性，并为将来的调整打下坚实的基础。这里介绍几个用于开始的调整旋钮，其中一些将在本文第2部分的调优部分再次提到。

### JVM堆大小

如上所述，JVM堆大小应符合Solr堆的需求，可以如下去评估。

```
Solr heap requirement est. = Filter cache size * (total doc in a core/ 8) * num of Cores +
                            Field value cache memory usage (if used) * num of Cores +
                            Field cache memory usage (if used) +
                            Misc memory usage (4G for busy system) +
                            Temporary workspace (4-6G for busy system)
```

如果cache auto warm被使用了，请使用cache size + cache autowarm size替换cache size。

在Solr中主要是Field cache消耗内存。要避免这种情况， 并减少内存占用的最佳方法是使用docValues。以下部分将更多的细节介绍。在 field缓存被使用了的情况下，如果faceting的工作负载很重并且单值field分类和索引尺寸很大（> 50M文档或> 10G大小），则可以粗略估算使用8-12G用于field 缓存。要不然4-8G就可以。 Field值缓存用于faceting、排序用于多值multi-valued并遵循与Field缓存类似的指导。

评估JVM堆大小需要匹配Solr堆需求和一些缓冲区。理想情况下，30％的缓冲空间有利于生产系统。这些缓存可以容纳零星内存的usage spike，例如后台合并或偶尔高消耗的查询，并允许JVM有效执行GC。针对生产系统，如果你要增加内存的话，建议使用的堆的最小尺寸16G。

### 堆外内存（直接内存）

Solr使用堆外内存缓存从磁盘读取的数据，大部分索引用于改善性能。堆外内存不会导致任何JVM GC开销，可以使用CM设置堆外内存大小（Cloudera Manager->Solr configuration->direct memory）。根据经验来看，如果docValues不在模式中使用，推荐使用的堆外内存的最小尺寸为8G，如果使用docValues，则为12-16G。其他相关配置是块缓存计数器（Cloudera Manager-> Solr configuration-> slab count），而块缓存计数器需要匹配堆外内存大小的。

```
Slab count = direct memory size * 0.7 / 128M
```

### 垃圾收集器

当CMS和G1 GC都支持Oracle JDK 8的时候。根据经验，如果堆大小小于28G，而CMS工作良好。其实G1便是更好的选择。如果您选择G1，本文的第2部分有更多关于配置G1的详细信息。 您还可以在Oracle G1调优指南中找到有价值的指导方法。

同时，启用GC日志一直都是一个不错的办法，因为GC日志的开销微乎其微，但它使我们更好地了解JVM如何在Hood中使用内存。而这些信息在GC故障排除中至关重要。 以下是GC日志设置的示例。

```
-XX:+PrintGCTimeStamps 
-XX:+PrintGCDateStamps 
-XX:+PrintGCDetails 
-XX:+PrintTenuringDistribution 
-XX:+PrintAdaptiveSizePolicy 
-XX:+PrintGCApplicationStoppedTime 
-XX:+PrintReferenceGC 
-Xloggc:/var/log/solr/solr_gc.log
```

在上面的示例中，GC日志存储在/var/log/solr/solr_gc.log中。 您可以将GC日志指向任何路径。由于Solr在CDH中的Linux user“solr”下运行，只需确保Linux user“solr”是否已经对您指向的路径具有权限。

### 架构

如果您的工作负载在facet和某些fields的排序很重，请对这些fields使用docValues。使用docValues Solr可以避免在堆上使用 field缓存和 field值缓存，这就大大降低了堆和JVM GC的内存压力。另一方面，正如上面堆外内存部分所述的一样，docValue fields可能会导致更多的磁盘I / O影响性能，并且需要大量的堆外内存。

当field用于faceting和排序时，文本field可能会导致大量内存使用。 在这种情况下使用string field代替文本field。

### 监控

Monitoring是跟踪系统健康的主要手段之一。一般情况下，良好的监控四个组成部分：关键指标，仪表板，日志和警报。本文将介绍内存相关的关键指标和仪表板。

#### 关键指标

以下是要监视的关键指标的列表。 指标分为两类：JVM metrics和缓存metrics。

![](https://github.com/itweet/labs/raw/master/BigData/img/jvm_metric.png)

Jvm_heap_used_mb告诉我们多少heap Solr 在JVM中实际使用。以及它应该在JVM Heap Size 节围绕中上下部分评估Solr内存需求。 Cloudera经理每分钟收集一个样本。因此，这种指标可能不会反映所有内存使用率上升。如前所述，确保堆内有足够的缓冲区内存，以容纳零星的内存使用率上升并降低GC开销。

缓存命中率是监视的另一个关键指标。它表示通过缓存而不是在磁盘命中索引来满足（或部分满足）总查询之外的请求数量。由于命中索引成本高，高速缓存命中率意味着缓存能满足更多的请求，这对性能有好处。本文第2部分的缓存优化部分有更多关于的缓存命中率的细节。

### 仪表板

监控这些关键指标的最简单方法是CM仪表板。您可以针对每一个指标的使用查询，利用Cloudera Manager轻松的创建一个仪表板，类似以下表格中的样本。

```
select jvm_heap_used_mb where serviceName=SOLR-1
```

这是从上面的查询创建的仪表板。

![Figure1: Example dashboard to monitor Solr JVM heap usage](https://github.com/itweet/labs/raw/master/BigData/img/Example-dashboard.png)

实时指标值和长期趋势都很重要。实时值显示Solr是如何执行的。如果系统发生变化那么长期趋势就会预示，如工作量，索引大小等，当您在查看长期趋势时，CM仪表板将执行降低采样。例如，如果您查看30天期间的JVM heap使用情况，仪表板显示三个值max，min，mean。 针对JVM堆使用，将监控平均值的最大值。

### 结论

内存调整是将Solr带入生产的关键步骤。Solr中有许多调整旋钮可以帮助您设置性能稳定的实施系统。本文介绍了：通用的内存调优技术，一些调整旋钮，如何通过一组注重是稳定性的配置启动您的第一个生产部署。该博客还介绍了Solr内存监控，这对于确保您的Solr部署在一段时间内的稳定运行至关重要。

现在我们有一个稳定运行的 Solr。 [本文的第2部分](http://blog.cloudera.com/blog/2017/06/solr-memory-tuning-for-production-part-2/)将深入展示如何调整内存，获得更多Solr之外的内存以及如何调整GC。第2部分中还描述的最佳实践方法。

第二部分最佳实践内容，将在后续持续更新。

说明：由于是工作之余进行维护，不能每天持续更新，定会保证文章的质量和原创性。相关最佳实践系列，下一阶段开启BigData系列内容，敬请期待。

参考: 

[1]. https://blog.cloudera.com/blog/2017/06/apache-solr-memory-tuning-for-production/

[2]. http://blog.cloudera.com/blog/2017/06/solr-memory-tuning-for-production-part-2/

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/