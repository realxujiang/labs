极简主义喜欢的ngx-admin项目
---

业余时间计划搞搞设计，最近翻阅前端资料，真是千变万化，很多新名词。

三端融合技术、前后端分离、前端也可以搞非常复杂的自动化测试、可以独立开发。

日新月异，计算机世界永恒的话题。

框架：react、angular、vue.js等。

语言：nodejs、typescripts、JavaScript、ES7、ES8晕的不行。

构建工具更：Gulp、npm、webpack、Grunt、Browserify、RequireJs、brunch等。

我选择angular框架，通过知乎、youtube、twitter、微博等Research研究，发现几大框架思想都有些类似，比如angular vs vue一度产生过网络战争，就在去年吧，我也有所耳闻，带着膜拜大神的态度曾经认真看完，发现很多思想都是相互借鉴。

1. 今天，我介绍angular的`hello world`小程序。

2. 奉上我在网络空间大肆搜索收获的基于angular主题模板ngx-admin。

我在mac上面完成我们以上两个小目标。

## 基础环境

在Mac下我选择的，包管理方式是Homebrew。

通过如下命令，我们安装好`node`、`npm`、并更新到最新版本。

```
brew install node

brew install npm
```

> 请先在终端/控制台窗口中运行命令 node -v 和 npm -v， 来验证一下你正在运行 node 6.9.x 和 npm 3.x.x 以上的版本。 更老的版本可能会出现错误，更新的版本则没问题。

```
➜ /usr/local git:(master) ✗ npm -v
5.6.0
➜ /usr/local git:(master) ✗ node -v
v5.10.1
```

如上，node不符合要求，在`build run`的时候会报错，执行如下命令升级你的node，如果发现无法升级成功，一般是由于brew版本低，导致无法获取到网络上最新的node版本，可以选择升级brew到最新版本，升级之后在更新node到最新版本，重写node的连接，不然新版本不生效。

* 升级brew

```
➜ /data/github brew -v
Homebrew 0.9.9 (git revision 1d99; last commit 2016-04-08)
Homebrew/homebrew-core (git revision 46b5; last commit 2016-04-08)

➜ /data/github /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

➜ /data/github brew -v
Homebrew 1.4.2
Homebrew/homebrew-core (git revision a678; last commit 2018-01-02)
```

* 升级node

```
brew update

brew upgrade node

brew link --overwrite node
```

`注意：由于brew老版本，需升级brew，否则无法搜索到最新的node版本，挺奇怪。参考：https://brew.sh/index_zh-cn.html`

升级之后成功
```
➜ /usr/local git:(master) ✗ node -v                                                           
v9.3.0

➜ /usr/local git:(master) ✗ npm -v                                                    
5.6.0
```

基础环境准备好，让我们开始第一个angular小程序。

## 你的第一个angular应用

首先，安装angular

```
npm install -g @angular/cli
```

创建angular应用，通过`ng server --open`启动程序

```
ng new my-app

cd my-app

ng serve --open
```

访问`http://localhost:4200`，你就可以看到熟悉的`angular hello world`页面。

![](https://angular.cn/generated/images/guide/cli-quickstart/my-first-app.png)

## 极简主义ngx-admin应用

github克隆ngx-admin主题，进入ngx-admin，执行`npm i`安装所有项目依赖，执行npm start启动项目。

```
git clone https://github.com/jikelab/ngx-admin.git

cd ngx-admin && npm i

npm start
```

如果，如果一切顺利，你可以看到提示。

```
$ npm start                                                       

> ngx-admin@2.0.1 start /data/github/ngx-admin
> ng serve

** NG Live Development Server is listening on localhost:4200, open your browser on http://localhost:4200/ **
Date: 2018-01-07T12:44:29.954Z                                                     t Hash: 09df24cf30b4055cb989
Time: 35763ms

webpack: Compiled successfully.
```

你可以，访问`http://localhost:4200/`，开始浏览所有漂亮的组件化模板。

![](https://camo.githubusercontent.com/33036bf7ec00d508575b5207a5799052cda93825/68747470733a2f2f692e696d6775722e636f6d2f586f4a7466764b2e676966)

在线演示：http://akveo.com/ngx-admin/?utm_source=nebular_documentation&utm_medium=demo_button

如果你遇到，s3无法访问，无法找到`fsevents@1.1.2` ：

```
> fsevents@1.1.2 install /data/github/ngx-admin/node_modules/fsevents
> node install

node-pre-gyp ERR! Tried to download(404): https://fsevents-binaries.s3-us-west-2.amazonaws.com/v1.1.2/fse-v1.1.2-node-v59-darwin-x64.tar.gz

node-pre-gyp ERR! Pre-built binaries not found for fsevents@1.1.2 and node@9.3.0 (node-v59 ABI) (falling back to source compile with node-gyp)
```

问题讨论：https://github.com/akveo/ngx-admin/issues/1474

## 小结

ngx-admin可用三端都支持的主题，支持大量主流的页面设计模块，可以直接引用，让我们快速完成一个三端项目的开发工作，当然还支持安卓、IOS，只需一套代码，支持三端融合，是一个非常优秀的框架。未来我会用ngx-admin来开启我新的2018年的项目，去年我用spring-boot开发了itweet-boot开源项目，感兴趣的可以Github去fork一下，一定帮助star。

`twts-boot-v1.0.war`直接可部署，只需要一个MySQL服务，直接放到tomcat启动即可使用。

演示：http://www.itweet.cn

下载: https://github.com/realxujiang/itweet-boot/releases

今年计划，我会开启一个支持三端融合的开源项目，注册了优秀域名，需要适配优秀项目。

哈哈，就这样。

- JikeLab.com
- JikeLab.cn
- bb8lab.com
- bb8lab.cn
- skynet.org

小域名，觉得怎么样，欢迎留言，给我点灵感，目前还没计划出来用途。

***参考：***

[1]. https://akveo.github.io/nebular/#/docs/installation/based-on-starter-kit-ngxadmin

[2]. https://github.com/realxujiang/itweet-boot/releases

[3]. https://akveo.github.io/nebular/#/home

欢迎关注微信公众号[whoami]，阅读更多内容。
![image.png](http://upload-images.jianshu.io/upload_images/9687832-2ff1ee6f489dcff3.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive