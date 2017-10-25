searchdb-performance-exploration
---

分布式搜索数据库产品，能满足很多企业高速检索的业务场景，海量的单表数据秒级搜索和全文检索，完全支持SQL语法，支持数据的增删改查，兼容MySQL/PostgreSQL协议，企业级分布式搜索数据库解决海量数据检索问题。

### 环境准备

必须修改如下相关的配置文件，不然会无法正常启动集群。

```
vi /etc/sysctl.conf
vm.max_map_count=262144

sysctl -p

vi /etc/security/limits.conf 
*   soft nofile 65536
*   hard nofile 65536

vi /etc/profile
export CRATE_HEAP_SIZE=100g
```

创建数据存储目录，创建用户searchdb，cratedb集群安装在searchdb用户下。

```
wget https://cdn.crate.io/downloads/releases/crate-2.1.5.tar.gz -O /opt/

tar -zxvf crate-2.1.5.tar.gz

mkdir /disk0{1..4}/searchdb

useradd searchdb
chown searchdb:searchdb /disk0{1..4}/searchdb
chown searchdb:searchdb -R /opt/crate-2.1.5

rm -rf /disk0{1..4}/searchdb/*
```

注意：需要提前安装好JDK，配置`JAVA_HOME`信息，特别注意`JDK版本`需要`jdk1.8.0_45`以上。

### 集群安装 

三节点集群软件，需要注意的信息`network.host`为每个节点的主机名,`node.name`填写为主机名,`my_cluster`必须是唯一的,编辑`crate.yml `文件。

```
cluster.name: my_cluster

node.name: node1

discovery.zen.ping.unicast.hosts:
  - node1:4300
  - node2:4300
  - node3:4300

discovery.zen.minimum_master_nodes: 2

gateway:
  recover_after_nodes: 2
  recover_after_time: 5m
  expected_nodes: 2

path.data: /disk01/searchdb,/disk02/searchdb,/disk03/searchdb/,/disk04/searchdb

network.host: node1

psql.enabled: true
psql.port: 5432
```

* 启动集群

```
bin/crate -d
```

* 访问集群

```
bin/crash

cr> \c node1:4200 
+-------------------+-----------+---------+-----------+---------+
| server_url        | node_name | version | connected | message |
+-------------------+-----------+---------+-----------+---------+
| http://node1:4200 | node1     | 2.1.5   | TRUE      | OK      |
+-------------------+-----------+---------+-----------+---------+
```

* 简单测试

```
create table tweets (
   created_at timestamp,
   id string primary key,
   retweeted boolean,
   source string INDEX using fulltext,
   text string INDEX using fulltext,
   user_id string
);

insert into tweets values (1394182937, '1', true, 'web', 'Don''t panic', 'Douglas');

insert into tweets
 values (
     1394182938,
     '2',
     true,
    'web',
    'Time is an illusion. Lunchtime doubly so',
    'Ford'
 );

insert into tweets values (1394182937, '3', true, 'address', '中国，北京', '北京');

select * from tweets where id = '2';

select user_id, _score from tweets where match(text, 'is') order by _score desc;

select user_id, _score from tweets where match(text, '北京') order by _score desc;

select user_id, _score from tweets where match(text, '京城') order by _score desc;

DELETE FROM tweets where id=3;
```

使用一些基础SQL语法测试，进行简单测试，包括带有的全文检索、分词能力，支持Update,Delete数据。

### 性能测试

生成测试数据，生成`books`表数据，平均`6.0K/条`，100G大小，通过一个`py`脚本把文本数据转换为json数据。

```
nohup java -cp dbgen-1.0-jar.jar DBGen -p ./data -b 100 &  --Total Time: 2610 seconds

cat books | python csv2json.py --columns id:integer isbn:string category:string publish_date:string publisher:string price:float > books.json
```

数据示例：

```
$ head data/books/books 
0|6-20386-216-4|STUDY-AIDS|1998-05-31|Gakken|166.99
1|0-60558-466-8|JUVENILE-NONFICTION|1975-02-12|Holtzbrinck|128.99
2|3-16551-636-9|POETRY|1988-01-24|Oxford University Press|155.99
3|4-75505-741-2|COMICS-GRAPHIC-NOVELS|1992-02-24|Saraiva|101.99
4|3-32982-589-8|PERFORMING-ARTS|2011-03-09|Cambridge University Press|183.99
```

基础命令：

```
 ./crash --help
 ./crash  --hosts node1 --sysinfo 

 ./crash  --hosts node1 -c "show tables"
```

创建表结构，导入数据。

```
CREATE TABLE books (
    id integer,
    isbn string,
    category string,
    publish_date string,
    publisher string,
    price float
);

COPY books FROM '/disk01/data/books/books.json';
```

通过如上命令，可以生成不同级别大小的测试数据，根据参数可以生成不同大小的表。

**测试场景1**

* 表级别：千万级
* 效率：15m/s (node)
* JSON大小：6.6 g
* 入库CrateDB大小：5.2 g
* 数据量：47582950
* 分片数量：6
* 副本数：2
* memory：16g
* vcpu：24 
* storage：1.4T （4*280g）
* network：千兆

主要针对单表的查询测试。

```
select category,count(*) from books group by category limit 100;   -- 3.137 s

select category,count(*) as num from books group by category order by num limit 100;    --2.929 sec

select category,count(*) as num from books where category='SCIENCE' group by category order by num limit 100;   --0.143 sec

select count(*) from books where category='SCIENCE' limit 100;  -- 0.022 sec 

select count(distinct category) from books limit 100;  -- 2.990 sec

select distinct category from books limit 100;  -- 3.032 sec 
```

**修改 number_of_shards 看是否提升性能**

```
ALTER TABLE books SET (number_of_shards = 48)

OPTIMIZE table books;  -- 这个参数比较有用，可以提升性能

SELECT count(*) as num_shards, sum(num_docs) as num_docs FROM sys.shards WHERE schema_name = 'doc' AND table_name = 'books';
```

**测试场景2**

* 表级别：亿级表 
* 效率：17285.888 sec
* JSON大小：33g
* 入库CrateDB大小：27g
* 数据量：235265838
* node_num: 3
* 分片数量：1024
* 副本数：2
* memory：100g
* vcpu：24 
* storage：1.4T （4*280g）
* 每入库秒钟：13610 条/s 
* network：千兆

创建表，导入数据。

```
CREATE TABLE books_t1 (
    id integer,
    isbn string,
    category string INDEX using fulltext,
    publish_date string,
    publisher string INDEX using fulltext,
    price float
) CLUSTERED BY (category) INTO 1024 SHARDS with (number_of_replicas = 2, refresh_interval=10000);

COPY books_t1 FROM '/disk01/data/books/books.json';  -- COPY OK, 235265838 rows affected  (17285.888 sec)
```

测试性能。

```
OPTIMIZE table books_t1;

select category,count(*) from books_t1 group by category limit 100;   -- 2.556 sec

select category,count(*) as num from books_t1 group by category order by num limit 100; -- 2.763 sec

问题：Error! SQLActionException[SQLParseException: Cannot GROUP BY 'category': grouping on analyzed/fulltext columns is not possible]

select count(*) from books_t1 where match(category, 'PERFORMING-ARTS'); -- limit 100; -- 0.256 sec

select * from books_t1 where match(category, 'ARTS'); -- limit 100; -- 0.256 sec; -- 0.928 sec
```

`注意：fulltext字段的都无法做聚合分析操作，不带全文索引，只能做全文搜索match，重新导数据在测试.`

**测试场景3**

* 表级别：亿级表 
* 效率：5662.132 sec
* JSON大小：33g
* 入库CrateDB大小：25.3g
* 数据量：235265838
* node_num: 3
* 分片数量：1024
* 副本数：2
* memory：100g
* vcpu：24 
* storage：1.4T （4*280g）
* 每入库秒钟：13610 条/s 
* network：千兆 

创建表，插入数据。

```
CREATE TABLE books_t2 (
    id integer,
    isbn string,
    category string,
    publish_date string,
    publisher string,
    price float
) CLUSTERED BY (category) INTO 1024 SHARDS;

COPY books_t2 FROM '/disk01/data/books/books.json';

insert into books_t2 select * from books_t1; -- INSERT OK, 235265838 rows affected  (5662.132 sec)
```

性能测试。

```
OPTIMIZE table books_t2;

select category,count(*) from books_t2 group by category limit 100;   -- 3.994 sec

select category,count(*) as num from books_t2 group by category order by num limit 100; -- 4.159 sec

select category,count(*) as num from books_t2 where category='SCIENCE' group by category order by num limit 100;    -- 1.731 sec

select count(*) from books_t2 where category='SCIENCE' limit 100;  -- 0.001 sec

select count(distinct category) from books_t2 limit 100;  -- 4.677 sec

select distinct category from books_t2 limit 100;  -- 3.914 sec

select id,price,publisher from books_t2 where publish_date='1999-02-02' and category='SCIENCE' limit 100; -- 0.014 sec
```

注意：`分片数量过多导致Heap Usage一直居高不下达到57%，表建立全局索引1024个分片，2个索引字段`

**测试场景4**

* 表级别：15亿级
* 效率：15m/s (node)
* JSON大小：215 G
* 入库CrateDB大小： 175.6g
* 数据量：1551303191
* 分片数量：500
* 副本数：2
* memory：100g
* vcpu：24 
* storage：1.4T （4*280g） * 4节点
* network：千兆

生成的文本数据，转换为JSON格式。

```
nohup cat /disk01/searchdb/data/books/books | python csv2json.py --columns id:integer isbn:string category:string publish_date:string publisher:string price:float > /disk02/searchdb/books.json &
```

切割一个215g数据文件为22个10g大小的数据文件，并行入库。

```
split -b 10000m /disk02/searchdb/books.json -d -a 3 split_file   
```

创建表。

```
CREATE TABLE books (
    id integer,
    isbn string,
    category string,
    publish_date string,
    publisher string,
    price float
) CLUSTERED BY (category) INTO 500 SHARDS;
```

批量入库数据。

```
 /opt/crate-2.1.7/bin/crash  --hosts node1 -c "COPY books FROM '/disk01/searchdb/split_file000'"
```

主要针对15亿单表的查询 - 性能测试。

```
OPTIMIZE table books;

select category,count(*) from books_t2 group by category limit 100;   -- 3.994 sec

select category,count(*) as num from books_t2 group by category order by num limit 100; -- 4.159 sec

select category,count(*) as num from books_t2 where category='SCIENCE' group by category order by num limit 100;    -- 1.731 sec

select count(*) from books_t2 where category='SCIENCE' limit 100;  -- 0.001 sec

select count(distinct category) from books_t2 limit 100;  -- 4.677 sec

select distinct category from books_t2 limit 100;  -- 3.914 sec

select id,price,publisher from books_t2 where publish_date='1999-02-02' and category='SCIENCE' limit 100; -- 0.014 sec
```

**测试场景5**

测试SQL如下，主要是针对单表的性能测试，无分区。

```
OPTIMIZE table books;

select category,count(*) from books group by category limit 100;   -- 37.878 sec

select category,count(*) as num from books group by category order by num limit 100; -- 46.603 sec

select category,count(*) as num from books where category='SCIENCE' group by category order by num limit 100;    -- 11.808 sec

select count(*) from books where category='SCIENCE' limit 100;  -- 0.002 sec

select count(distinct category) from books limit 100;  -- 44.924 sec

select distinct category from books limit 100;  -- 44.335 sec

select id,price,publisher from books where publish_date='1999-02-02' and category='SCIENCE' limit 100; -- 0.347 sec

select price,count(publisher) from books where publish_date='1999-02-02' and category='SCIENCE' group by price order by price desc limit 100; -- 0.981 sec

select price,category from books where publisher='Kyowon' group by price,category order by price limit 100;  --
3.602 sec

select price,category,count(*) from books where publisher='Kyowon' group by price,category order by price limit 100;  -- 1.406 sec
```

- 场景1 数据量：496928035  4节点(mem:128g vcore: 24 storage: 4*250g)  大小：56.2g  shards: 500 平均：`6.0K/条`   网络：千兆

- 场景2 数据量：993106194  4节点(mem:128g vcore: 24 storage: 4*250g)  大小：112g  shards: 500  平均：`6.0K/条`  网络：千兆

- 场景3 数据量：1551303103  4节点(mem:128g vcore: 24 storage: 4*250g)  大小：174.4g  shards: 500  平均：`6.0K/条`  网络：千兆

![crate-performance](https://github.com/itweet/labs/raw/master/startup/img/crate-performance.png)

注意：`如上测试并没有专业优化并发，除内存外，所有参数使用默认。`

在单表15亿+，五分区，4台服务器，千兆网络，表现出来的性能还是非常强劲的，主要针对单表各种统计分析并且还带有全文检索的功能， 此数据库可以把它称为是分布式搜索数据库。底层用到了很多搜索引擎存储的技术，包括倒排索引，数据分片，利用大内存，细粒度索引，如果能支持多实例，目前CPU还没完全使用，磁盘IO和内存都满载。每一个字段都带索引，所以入库比较慢，在单机上入库是瓶颈，可以分开在多台机器入库，这样避免IO堵在一台机器；压力过大容易导致节点奔溃脱离集群；join性能没深入探索，不好评价。

- 全文搜索(Fulltext Search)、分词等能力通过特殊SQL语法匹配，搜索结果可以进行复杂的统一分析。
- Geo Search，支持基于地理位置信息的复杂算法分析，响应迅速。
- 支持分区表，可以基于分区进行检索分析。
- 支持多副本，自带容错，检索分流，提高性能。
- 海量数据实时入库，实时检索、复杂统计分析。
- Blob(binary large object)，二进制大对象存储分析。
- 仅支持JSON/CSV入库。

一个分布式搜索数据库，支持标准SQL和JDBC，用来替代ES做一些全文检索并支持复杂统计分析能力，很有实际意义。

我目前参与过最大的ES集群，也就60节点300亿+doc(3个主节点，6T&2块SATA)，数据量`400TB`，还有一个小集群20节点70亿+doc(3主节点，4T&2块SSD)，性能基本能满足要求，存储近3年的数据，历史数据HDFS为Backup。

参考：

- [1]. https://github.com/baidu/Elasticsearch
- [2]. http://www.itweet.cn/blog

欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/






