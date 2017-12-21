Gitlab服务器迁移
---

由于资源紧张，为了完成CI/CD的自动化，所以打算把一台128g、24c、10T存储的一台独立GitLab服务器虚拟化为多台服务器。完成持续集成平台的迁移，减少资源浪费，现在记录一下操作过程。

1. 备份原GIT服务器数据

```
gitlab-rake gitlab:backup:create RAILS_ENV=production 
```

注：默认备份后文件一般位于`/var/opt/gitlab/backups/`，文件名：`1513578325_2017_12_18_gitlab_backup.tar`

2. 新服务器上安装与原服务器一样版本的Gitlab.

这里说明下为什么要一样，原因应该是由于Gitlab自身的兼容性问题，高版本的Gitlab无法恢复低版本备份的数据.

原Gitlab安装版本: `gitlab-ce-8.7.0-ce.0.el6.x86_64`.

* 下载对应的Gitlab版本

```
wget https://packages.gitlab.com/gitlab/gitlab-ce/packages/el/6/gitlab-ce-8.7.0-ce.0.el6.x86_64.rpm
```

* 安装GitLab

通过rpm命令安装GitLab服务，配置并启动GitLab

```
rpm -i gitlab-ce-8.7.0-ce.0.el6.x86_64.rpm

sudo gitlab-ctl reconfigure
```

3.将步骤1生成的tar文件拷贝到新服务器上相应的backups目录下

可以利用scp进行直接拷贝。

```
scp /var/opt/gitlab/backups/1513578325_2017_12_18_gitlab_backup.tar username@src_ip:/var/opt/gitlab/backups
```

注: username为新服务器的用户名，src_ip新服务器IP地址

4.新GitLab服务数据恢复

```
# This command will overwrite the contents of your GitLab database!
gitlab-rake gitlab:backup:restore RAILS_ENV=production   BACKUP=1513578325_2017_12_18
```

注：BACKUP的时间点必须与原服务器备份后的文件名一致

版本不匹配问题

```
GitLab version mismatch:
  Your current GitLab version (8.7.0) differs from the GitLab version in the backup!
  Please switch to the following version and try again:
  version: 9.0.5
```

5.重启GitLab服务并检测恢复数据情况

```
sudo gitlab-ctl restart
sudo gitlab-rake gitlab:check SANITIZE=true
```

如果check命令出现错误，说明备份的GitLab服务和新的GitLab服务版本不匹配，请安装正确的版本。

6.总结

GitLab是一款企业级私有Git服务最佳选择。可以完成企业持续集成平台代码库管理的工作。也可以和很多持续集成工具进行无缝结合，让开发人员专注开发，部署、打包、测试、上线的工作自动化完成。关键是它免费的，`linus`真年神人也。`GIT`也是他的作品。

膜拜大神，进一步了解，最近在看《只是为了好玩:Linux之父林纳斯自传》Linux之父`Linu`s`写的一本书，关于开源软件做了很好的阐述。


欢迎关注微信公众号，第一时间，阅读更多有关云计算、大数据文章。
![Itweet公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/





