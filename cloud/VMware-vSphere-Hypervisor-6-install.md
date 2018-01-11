VMware vSphere Hypervisor (ESXi) 6.5 安装配置
---

VMware vSphere 是业界领先且最可靠的虚拟化平台。vSphere将应用程序和操作系统从底层硬件分离出来，从而简化了IT操作。（注：从VMware vSphere Hypervisor (ESXi) 6.5开始，不在支持vSphere Client管理虚拟机，而采用WEB的方式直接管理，免去要安装客户端的麻）本次安装的镜像为：VMware-VMvisor-Installer-6.5.0-4564106.x86_64.iso

* 本次安装机器配置

| 机器型号 | CPU | 内存 | cpu cores | Disks | 数量 |
| ------ | ------ | ------ | ------ | ------ | ------ |
| Dell R710 | Intel(R) Xeon(R) CPU E5-5670 | 128G | 6 | 200G*4 | 1台|

## 制作U盘启动

- 1、打开UItraISO 文件-打开`VMware-VMvisor-Installer-6.5.0-4564106.x86_64.iso`
![](https://github.com/itweet/labs/raw/master/cloud/img/u-install-setup-1.png)

- 2、启动-写入硬盘镜像
![](https://github.com/itweet/labs/raw/master/cloud/img/u-install-setup-2.png)

- 3、选择你要写入的U盘
![](https://github.com/itweet/labs/raw/master/cloud/img/u-install-setup-3.png)

- 4、制作U盘启动会把U盘格数据式化
![](https://github.com/itweet/labs/raw/master/cloud/img/u-install-setup-4.png)

- 5、开始刻录镜像到U盘
![](https://github.com/itweet/labs/raw/master/cloud/img/u-install-setup-5.png)

## 交互式安装ESXI6.5

- 1、插入ESXI6.5光盘或U盘（镜像用UltraISO写入U盘），设置为光盘或U盘启动，进入引导，5秒钟之后自动进入安装界面（也可直接按回车进入）

![](https://github.com/itweet/labs/raw/master/cloud/img/loading-esxi-install.png)

- 2、在引导过程中，可以看到机器的CPU、内存的基本信息

![](https://github.com/itweet/labs/raw/master/cloud/img/loading-esxi-sucess.png)

- 3、单击“回车”键确认，确定安装

![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-1.png.png)

- 4、按“F11”接受VMware协议

![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-2.png)

- 5、此界面选择安装位置，选择你要安装在哪个磁盘，单击“回车”键确认。

![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-3.png)

- 6、键盘类型，保持默认美式键盘，单击“回车”键确认。

![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-4.png)

- 7、输入默认管理员root的密码，密码要求7位以上，单击“回车”键确认
![](install-esxi-5.png)

- 8、单击“F11”键确认安装
![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-6.png)

- 9、安装进行中。
![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-7.png)

- 10、安装完成，提示单击“回车”键重启进入ESXI6.5。
![](https://github.com/itweet/labs/raw/master/cloud/img/install-esxi-8.png)

## 配置ESXI6.5网络

- 1、重启系统后进入界面。上面会提示现在可以连接的地址，这个地址默认是DHCP获取，但有时候我们需要给它指定IP。此时单击“F2”进入配置界面

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-1.png)

- 2、提示输入管理员root的密码。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-2.png)

- 3、切换至Configure Management Network，单击“回车”键。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-3.png)

注：

```
Configure Password              配置root密码
Configure Lockdown Mode         配置锁定模式。启用锁定模式后，除vpxuser以外的任何用户都没有身份验证权限，也无法直接对ESXi执行操作。锁定模式将强制所有操作都通过vCenter Server执行。
Configure Management Network    配置网络
Restart Management Network      重启网络
Test Management Network         使用Ping命令测试网络
Network Restore Options         还原网络配置
Configure Keyboard              配置键盘布局
Troubleshooting Options         故障排除设置
View System Logs                查看系统日志
View Support Information        查看支持信息
Reset System Configuration      还原系统配置
```

- 4、选择IPv4 Configuration，单击“回车”键。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-4.png)

注：

```
Network Adapters            网卡选择
VLAN（optional）            设置VLan
IPv4 Configuration          设置IPv4地址
IPv6 Configuration          设置IPv4地址
DNS Configuration           设置DNS地址
Custom DNS Suffixes         自定义DNS后缀
```

- 5、按上下键定位到第三项按空格键选中，设置静态IP地址、掩码、网关的信息，单击“回车”键。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-5.png)

注：

```
Disable IPv4 configuration for management network        禁用IPv4地址
Use dynamic IPv4 address and network configuration       配置动态IPv4地址
Set static IPv4 address and network configuration        配置静态IPv4地址
```

- 6、选中DNS Configuration，按“回车”键确认。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-6.png)

- 7、根据实际需要更改DNS和本机名，按“回车”键确认。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-7.png)

- 8、按“Exit”退出配置，提示网络配置信息变更，提示保存。按“Y”保存。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-8.png)

- 9、退出配置后即可在主页面看到新的连接地址。

![](https://github.com/itweet/labs/raw/master/cloud/img/network-esxi-9.png)

## 分配ESXI6.5许可证

- 1、在主页面查看连接地址，在浏览器中打开，提示输入用户名密码登录。

![](https://github.com/itweet/labs/raw/master/cloud/img/end-1.png)

- 2、登录成功后即可看到WEB版的vSphere Client界面就相关服务器信息。

![](https://github.com/itweet/labs/raw/master/cloud/img/end-2.png)

- 3、定位到“管理”》“许可”》“分配许可证”，在弹出的窗口中输入KEY，单击“检查许可证”完成分配即可。

![](https://github.com/itweet/labs/raw/master/cloud/img/end-3.png)

基本上、都是小白式安装、小白式使用，传入镜像，安装一个基础的版本，做一个镜像或者快照，就可以生成相应版本的操作系统、类似VMware系列产品、高度一致。

欢迎关注微信公众号[Whoami]，阅读更多内容。
![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/blog/archive/












