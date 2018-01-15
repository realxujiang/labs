GitHub给软件开发领域带来的改变
---

Git是分布式代码开发的最佳选择，今天把我常用的一些Git命令给列表一下。

说起Git，就不得不提一下Github，它几乎成为一种全球最大的在线协作社区。

目前几乎最知名的大规模上生成的开源项目，基本都是在GitHub社区通过全球几十万开发者共同协作，开发完成。

比如：Hadoop、Spark、Hive等，几乎都是全世界开发者协作的伟大作品。

在Github上，如何开启一个开源项目。

- 1、你需要注册一个GitHub账号
- 2、你需要建立一个项目，需要填写一些基本信息
- 3、开源许可证选择、这块你可以需要认真了解
- 4、初始化你的项目到GitHub，附有完整的文档
- 5、文档简洁、附有快速启动、有个GIF动画介绍
- 6、社区秀一下作品、帮助快速了解
- 7、制定计划、新功能、待开发列表，让更多人参与开发
- 8、每天按照计划、`pull->add->commit->push`代码

GitHub有完整的体系，如何在GitHub启动一个新的project

> https://help.github.com/articles/adding-an-existing-project-to-github-using-the-command-line/

GitHub上，如何贡献一个开源项目。

由于我的日常工作都是混迹社区，也给很多知名软件提过`issues`和`pull requests`，对于如何贡献别人的代码，略有经验。

> Pull Requests: https://help.github.com/articles/about-pull-requests/

首先，你需要`fork`你想贡献的软件项目，并且你需要系统的学习一下关于GitHub上支持的软件开源协议，如果因为公司而基于社区某个开源版本进行深度开发，避免引起不必要的纠纷。

你需要完整的了解整个软件设计解决什么样的问题，还有那些待开发功能，或者待完善的功能，完整查看开发者手册和规范，很多优秀的开源软件，一开始就拥有严格的代规范，参与共享代码，可以提`patch`，避免别人和你一样做了重复的功能，可以一起协作完成某项功能。初期如果仅仅是感兴趣，可以试试修复一些BUG，发起`pull requests`，体验一次贡献源代码。

如果，你严格按照要求的规范编写代码，发起的`pull requests`初步检测通过，接下来会有社区负责人和你一起讨论此功能他们是否接受、为什么，或者接受引发那些新的问题，需要继续完成，或者有更多的人参与讨论，因为他们可不想偏离自己软件的设计初衷，如果你贡献的是一个大`PR`。

如果`Code Review`都通过，讨论结束，那么接下来就是合并代码到主干。

其实流程就是这么简单，你fork别人的代码，然后增加新功能，发起一个pull requests，等待审核，通过你就可以合并你的代码到主干。

为什么需要fork ？

因为想要参与主干开发，必须经过严密的审核，从commit->contribution需要经过考察，并且得到大部分此项目管理员的认可，不是什么人都能把自己的代码贡献、并且运行在全世界的服务器。

我的意思是，你贡献的如果是一个非常知名和用户群超大的项目。

比如：Hadoop、MySQL、Linux

如果你有幸参与全球知名的开源软件项目，很多人都会感到很自豪和不可思议，你写的代码真的运行在全世界的服务器中，那是一种什么样的体验，无法描述。

所谓`代码不朽`就是这个意思吧，这是做为程序员，最大的追求了吧。。。

![](https://linode.com/docs/assets/git-github-workflow-650w.png)

我记录的Git命令: 

+++++++Git: release branch+++++++
```
git tag v1.0

git push origin v1.0
```

+++++++Git: 创建新的分支，在分支开发+++++++
```
git branch twts-boot
git checkout twts-boot

```

+++++++++++Git: 回退版本+++++++++++
```

git reset --hard HEAD~3

git push --force
```


+++++++++++Git: Delete a branch (local or remote)+++++++++++

- 1、To delete a local branch
```
git branch -d the_local_branch
```

- 2、To remove a remote branch (if you know what you are doing!)
```
git push origin :the_remote_branch
```

or simply use the new syntax (v1.7.0)
```
git push origin --delete the_remote_branch
```

+++++++++++Git: 删除本地分支和远程分支+++++++++++
```
git checkout master

git branch -d xxx-rdf-1.2.1

git push origin --delete xxx-rdf-1.2.1
```

+++++++++++Git: 多个commit信息合并+++++++++++

```
git rebase -i b951229892864f71eaf23bcd7a8e09131da7a615

git push --force
```


目前我每天都在使用Git。Git是一个分布式版本控制软件，最初由林纳斯·托瓦兹创作，于2005年以GPL发布。最初目的是为更好地管理Linux内核开发而设计。应注意的是，这与GNU Interactive Tools有所不同。 Git最初的开发动力来自于BitKeeper和Monotone。

**参考：**

- [1] https://git-scm.com/book/en/v2/Getting-Started-Git-Basics
- [2] https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000
- [3] http://www.ruanyifeng.com/blog/2015/08/git-use-process.html

欢迎关注微信公众号[Whoami]，阅读更多内容。

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/


