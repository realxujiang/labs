ClickHouse源码阅读环境之Centos编译
---

ClickHouse源码阅读环境之Centos编译，主要介绍如何在Centos7.x版本成功构建ClickHouse，生成可部署的二进制文件。

## 基础环境

我已经做好可以直接编译的镜像，直接pull获取镜像即可开始愉快的编译。

```
docker pull jikelab/centos-7-clickhouse:v1.1.54370-stable

docker run -itd -v /data/gitlab/jdp:/opt --workdir /opt jikelab/centos-7-clickhouse:v1.1.54370-stable /bin/bash

docker exec -it 容器ID /bin/bash      # 进入容器后，clone源码，即可开始building...
```

获取Clickhouse源码，进去源码目录。

```
cd /opt

git clone -b stable --recursive https://github.com/yandex/ClickHouse.git

cd ClickHouse
```

## 编译clickhouse

Basic environment

```
export CMAKE=cmake3
export CC=/opt/rh/devtoolset-7/root/usr/bin/gcc
export CXX=/opt/rh/devtoolset-7/root/usr/bin/g++
```

Detect number of threads to run 'make' command

```
export THREADS=$(grep -c ^processor /proc/cpuinfo)

echo "CMAKE=$CMAKE"
echo "CC=$CC"
echo "CXX=$CXX"
echo "THREADS=$THREADS"
```

Build clickhouse RDBMS

```
rm -rf build
mkdir build
cd build
$CMAKE .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE:STRING=Release  -DHAVE_THREE_PARAM_SCHED_SETAFFINITY=1 -DOPENSSL_SSL_LIBRARY=/usr/lib64/libssl.so -DOPENSSL_CRYPTO_LIBRARY=/usr/lib64/libcrypto.so -DOPENSSL_INCLUDE_DIR=/usr/include/openssl
make -j $THREADS
cd ..
```

build successful

![clickhouse-build-sucessful](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/build-clickhouse.png)

安装clickhouse，注意需要依赖如下两个包，一般打包为RPM的时候依赖上即可。

```
yum install -y unixODBC libicu
```

如上就是clickhouse在centos下的编译过程，由于提前准备好了编译环境，跳过了很多坑，这样比较顺利。

至于构建出RPM，则需要自己定制自己的spec文件，学习通过spec文件，通过rpmbuild构建rpm包。

我们在单独内容，来介绍一个通用的构建RPM包的方法和示例，包括我们是有自动化流水线的从源码拉取到生成RPM的系统。

![auto-to-rpm](https://github.com/itweet/labs/raw/master/JDP/ClickHouse/img/auto-to-rpm.png)

## 推荐阅读

[1] 初识ClickHouse《First Time ClickHouse》

[2] 大规模数据处理的演变(2003-2017)

[3] Clickhouse快速上手

[4] 数据仓库：过去、现在和未来

[5] ClickHouse相关配置剖析

[6] ClickHouse源码阅读环境之ubuntu编译

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive







