
docker run --rm -v /data/gitlab/rdf:/ws -v /data/software/maven/repository:/root/.m2/repository -v ~/.npm:/root/.npm -v ~/.cache:/root/.cache -v ~/.gradle:/root/.gradle -v ~/.ivy2:/root/.ivy2 -v /tmp:/tmp  --workdir /ws bigtop/slaves:trunk-centos-7 bash -l -c "cd bigtop ; ./gradlew allclean"

+++++++git release branch+++++++

git tag v1.0

git push origin v1.0

+++++++创建新的分支，在分支开发+++++++

git branch twts-boot
git checkout twts-boot

++++++++mac 安装ng和使用ng模板+++++++++

包管理方式Homebrew

brew install node

brew install npm

brew update

brew upgrade node

brew link --overwrite node

➜ /usr/local git:(master) ✗ npm -v
5.6.0
➜ /usr/local git:(master) ✗ node -v
v5.10.1

你的第一个angular应用。

```
npm install -g @angular/cli

ng new my-app

cd my-app

ng serve --open
```

https://akveo.github.io/nebular/#/docs/installation/based-on-starter-kit-ngxadmin

cd ngx-admin && npm i

npm start

由于brew版本老，升级brew，否则无法搜索到最新的node版本，挺奇怪 参考：https://brew.sh/index_zh-cn.html

➜ /data/github brew -v
Homebrew 0.9.9 (git revision 1d99; last commit 2016-04-08)
Homebrew/homebrew-core (git revision 46b5; last commit 2016-04-08)

➜ /data/github /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

➜ /data/github brew -v
Homebrew 1.4.2
Homebrew/homebrew-core (git revision a678; last commit 2018-01-02)

➜ /data/github brew update

接下来，升级node版本，因为`angular 5`依赖特定node版本。

```
请先在终端/控制台窗口中运行命令 node -v 和 npm -v， 来验证一下你正在运行 node 6.9.x 和 npm 3.x.x 以上的版本。 更老的版本可能会出现错误，更新的版本则没问题。
```

执行命令升级node，之后在启动ngx-admin

```
brew upgrade node

brew link --overwrite node
```


报错，s3无法访问：

> fsevents@1.1.2 install /data/github/ngx-admin/node_modules/fsevents
> node install

node-pre-gyp ERR! Tried to download(404): https://fsevents-binaries.s3-us-west-2.amazonaws.com/v1.1.2/fse-v1.1.2-node-v59-darwin-x64.tar.gz

node-pre-gyp ERR! Pre-built binaries not found for fsevents@1.1.2 and node@9.3.0 (node-v59 ABI) (falling back to source compile with node-gyp)

xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance

xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance

```
xcode-select: error: tool 'xcodebuild' requires Xcode, but active developer directory '/Library/Developer/CommandLineTools' is a command line tools instance
```

xcode-select --install

sudo xcode-select -switch /Library/Developer/CommandLineTools


++++++++++++++docker操作++++++++++++++

bash -c "clear && docker exec -it 403d1139e769 sh"









