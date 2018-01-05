Mac用户如何打造史上最强终端
---

## 简介

捣鼓一下，Mac下的终端主题，最开始我选择的是[`on-my-zsh`](https://github.com/robbyrussell/oh-my-zsh)，非常强大，用起来基本停不下来。

通过oh-my-zsh提供的[`External-themes`](https://github.com/robbyrussell/oh-my-zsh/wiki/External-themes)列表，支持多种漂亮的UI。

我选择的是`powerlevel9k`，安装还挺复杂，接下来我介绍一下。

![](https://camo.githubusercontent.com/31da002de611cfef95f6daaa8b1baedef4079703/687474703a2f2f6268696c6275726e2e6f72672f636f6e74656e742f696d616765732f323031352f30312f706c396b2d696d70726f7665642e706e67)

## 安装powerlevel9k

[powerlevel9k安装方式](https://github.com/bhilburn/powerlevel9k#installation)如下：

* 安装`powerlevel9k`

```
git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
```

你需要修改`~/.zshrc`中的`ZSH_THEME="powerlevel9k/powerlevel9k"`，重新运行终端iTerm2，如果出现`乱码框`，你需要通过 `iTerm2` > `Preferences` > `Profile` > `Text` ；修改终端字体和Non-ASCII字体为Roboto Mono for Powerline

* 安装`powerline-fonts`

```
# clone
git clone https://github.com/powerline/fonts.git --depth=1
# install
cd fonts
./install.sh
# clean-up a bit
cd ..
rm -rf fonts
```

[`炫酷主题地址`](https://github.com/bhilburn/powerlevel9k/wiki/Show-Off-Your-Config)

* 安装`SourceCodePro`字体

```
brew tap caskroom/fonts && brew cask install font-source-code-pro
```

* 安装`Awesome Regular 12`字体

克隆字体成功后，进入build目录，点击字体进行安装。
```
git clone git@github.com:gabrielelana/awesome-terminal-fonts.git
```

#### 安装成功如下：

![](https://cloud.githubusercontent.com/assets/990216/17275518/d954bb16-56d0-11e6-9a1d-a7d89b86ae1a.png)

详情访问：https://github.com/gabrielelana/awesome-terminal-fonts/wiki/OS-X

系统可加载字体，需要如下操作，必须先通过`csrutil`命令disable，可修改系统保护文件。

重启按住command + R 键进入recovery模式，打开`终端`，才能执行，执行效果如下，重启验证机器。

##### 关闭SIP
```
csrutil disable; reboot
```

![关闭SIP](https://github.com/itweet/labs/raw/master/mac/img/csrutil-disabled.jpg)

##### 验证SIP Status

![](https://github.com/itweet/labs/raw/master/mac/img/csrutil-status.png)

##### 复制默认字体文件
```
cp /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreText.framework/Resources/DefaultFontFallbacks.plist ~/Desktop
```

##### 修改字体文件通过`Xcode`，并且备份默认字体文件
```
open -a Xcode.app ~/Desktop/DefaultFontFallbacks.plist

cp /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreText.framework/Resources/DefaultFontFallbacks.plist ~/DefaultFontFallbacks.plist.bak
```

##### 移动改过的字体文件覆盖，系统默认的字体文件
```
sudo mv ~/Desktop/DefaultFontFallbacks.plist /System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreText.framework/Resources/DefaultFontFallbacks.plist
```

##### 恢复`csrutil`为enable模式

需要重复之前操作，把系统进入recovery模式，否则执行命令报错
```
csrutil: failed to modify system integrity configuration. This tool needs to be executed from the Recovery OS.
```

进入recovery模式执行
```
csrutil enable; reboot
```

需要突破系统一些限制，所以稍微有点繁琐。

## 小结

废话少说，上效果图。

![效果图](https://camo.githubusercontent.com/80ec23fda88d2f445906a3502690f22827336736/687474703a2f2f692e696d6775722e636f6d2f777942565a51792e676966)




