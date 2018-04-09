ClickHouse源码阅读环境之Ubuntu编译
---

ClickHouse源码阅读环境之Ubuntu编译，主要介绍如何在Ubuntu 17版本成功构建ClickHouse，生成可部署的二进制文件。

## 基于Ubuntu 17编译ClickHouse

获取Ubuntu 17.10版本，并且运行此版本镜像，把宿主机/data/gitlab/jdp目录挂载到容器/opt目录。 通过docker exec命令进入容器，执行相关编译操作。

```
docker run -itd -v /data/gitlab/jdp:/opt --workdir /opt ubuntu:17.10 /bin/bash

docker exec -it angry_edison /bin/bash
```

接下来就是容器内的操作，为了方便，一般我在我的Ubuntu和macos机器上都是通过docker来跑各种系统和测试的，基本当做虚拟机用，关于docker知识查阅资料吧。

```
# cat /etc/issue
Ubuntu 17.10

# uname -ar
Linux 88fb00182673 4.9.60-linuxkit-aufs #1 SMP Mon Nov 6 16:00:12 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
```

在Ubuntu 17.10容器中安装相关编译环境软件包。

```
apt update -y 

apt install -y cmake libssl-dev libcrypto++-dev libglib2.0-dev libltdl-dev libicu-dev libmysql++-dev libreadline-dev libmysqlclient-dev unixodbc-dev gcc-7 g++-7 unixodbc-dev devscripts dupload fakeroot debhelper liblld-5.0-dev libclang-5.0-dev liblld-5.0
```

进入宿主机映射容器目录，为了持久化保存编译目录数据。

```
cd /opt
git clone -b stable --recursive https://github.com/yandex/ClickHouse.git

cd ClickHouse
```

开始编译ClickHouse

```
mkdir -p build

cd build

cmake .. -DENABLE_EMBEDDED_COMPILER=1 -DENABLE_TESTS=0

make -j $(nproc || grep -c ^processor /proc/cpuinfo)

```

编译成功 - 尾部信息

```
[100%] Linking CXX static library libclickhouse-benchmark-lib.a
[100%] Built target clickhouse-benchmark-lib
Scanning dependencies of target clickhouse-local-lib
[100%] Building CXX object dbms/src/Server/CMakeFiles/clickhouse-local-lib.dir/LocalServer.cpp.o
[100%] Linking CXX static library libclickhouse-copier-lib.a
[100%] Built target clickhouse-copier-lib
[100%] Linking CXX static library libclickhouse-local-lib.a
[100%] Built target clickhouse-local-lib
Scanning dependencies of target clickhouse
[100%] Building CXX object dbms/src/Server/CMakeFiles/clickhouse.dir/main.cpp.o
[100%] Linking CXX executable clickhouse
[100%] Built target clickhouse
Scanning dependencies of target clickhouse-lld
Scanning dependencies of target clickhouse-extract-from-config
[100%] Built target clickhouse-lld
[100%] Built target clickhouse-extract-from-config
Scanning dependencies of target clickhouse-clang
Scanning dependencies of target clickhouse-copier
[100%] Built target clickhouse-copier
[100%] Built target clickhouse-clang
Scanning dependencies of target clickhouse-format
Scanning dependencies of target clickhouse-compressor
[100%] Built target clickhouse-format
[100%] Built target clickhouse-compressor
Scanning dependencies of target clickhouse-benchmark
Scanning dependencies of target clickhouse-server
[100%] Built target clickhouse-benchmark
[100%] Built target clickhouse-server
Scanning dependencies of target clickhouse-client
Scanning dependencies of target clickhouse-local
[100%] Built target clickhouse-client
[100%] Built target clickhouse-local
Scanning dependencies of target clickhouse-performance-test
[100%] Built target clickhouse-performance-test
Scanning dependencies of target clickhouse-bundle
[100%] Built target clickhouse-bundle

```


为了便于使用，我把上述编译环境变成镜像已经上传到jikelab仓库，你可以通过如下命令获取。

```
docker pull jikelab/ubuntu-17.10-clickhouse:v1.1.54370-stable

docker run -itd -v /data/gitlab/jdp:/opt --workdir /opt jikelab/ubuntu-17.10-clickhouse:v1.1.54370-stable /bin/bash

docker exec -it 容器ID /bin/bash   # 进入容器后，clone源码，即可开始building...
```

我是如何制作此镜像呢？

Examples:

Push一个新的image到公共镜像仓库。

[1] 通过正在运行的容器ID快速保存成新的镜像。

```
$ docker commit c16378f943fe ubuntu-17.10-clickhouse:v1.1.54370-stable
```

[2] 现在通过image ID Push镜像到公共镜像仓库。

```
$ docker tag ubuntu-17.10-clickhouse:v1.1.54370-stable jikelab/ubuntu-17.10-clickhouse:v1.1.54370-stable

$ docker push jikelab/ubuntu-17.10-clickhouse:v1.1.54370-stable
```

[3] 通过运行如下命令检查镜像生成是否生效。

```
$ docker images
```

你应该能看到`ubuntu-17.10-clickhouse:v1.1.54370-stable`和`jikelab/ubuntu-17.10-clickhouse:v1.1.54370-stable`镜像列表。

关于ClickHouse源码阅读环境之Centos编译

> 正在整理相关编译环境和文档，会通过自动化的持续集成平台发布，可关注镜像仓库。

关于构建deb包

> 类似rm -f ../clickhouse*.deb && ./release && ls -l ../clickhouse*.deb命令，然后，愉快的部署和调试ClickHouse。

## 小结

介绍clickhouse在Ubuntu中进行源码编译和涉及到的Docker容器相关技术，对于想深入源码研究clickhouse的人来说，此步骤后就可以愉快的阅读代码，调试和改代码啦，简单看了一下clickhouse的代码量还是相当惊人的，相当于2个大型的C++项目，不得不佩服开发者，是在短短几年内完成的工作，而且还能保证测试覆盖率和高性能，那是相当厉害。

参考：

[1] https://docs.docker.com/engine/reference/commandline/push/#examples
[2] https://clickhouse.yandex/docs/en/development/build/

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive




