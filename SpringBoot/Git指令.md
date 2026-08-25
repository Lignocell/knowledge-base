# Git版本控制

注意：我们这里的远程仓库使用的是GitHub。

所谓版本控制，就是我们每一个版本都有新加的东西，通过对于版本的添加，删除，回滚等操作，来让结果呈现出最好的状态，当然，也有多人开发同样也需要版本控制。

## 走进Git

我们开发的项目，也需要一个合适的版本控制系统来协助我们更好地管理版本迭代，而Git正是因此而诞生的，首先我们来了解一个Git是如何工作的：

![点击查看源网页](https://oss.itbaima.cn/internal/markdown/2023/03/06/ZxY3MGkWRpOLVU6.jpg)

可以看到，它大致分为四个模块：

- 工作目录存放我们正在写的代码（一般通过编译环境来展示）。
- 暂存区：暂时保存待提交的内容。
- 本地仓库：位于我们电脑上的一个版本控制仓库（存放的是当前项目中各个版本代码的增删信息）。
- 远程仓库：位于服务器的版本控制仓库。

它是一个分布式的控制系统，因此一般情况下我们每个人的电脑上都有一个本地仓库，由大家共同向远程仓库去推送版本迭代信息。

通过这一系列操作，我们就可以实现每开发完一个版本或是一个功能，就提交一次新版本，这样，我们就可以很好地控制项目的版本迭代，想回退到之前的版本随时都可以回退，想查看新版本添加或是删除了什么代码，随时都可以查看。

## 安装Git

首先请前往Git官网去下载最新的安装包：https://git-scm.com/download/win

安装完成后，需要设定用户名和邮箱来区分不同的用户：

```shell
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

## 基本命令介绍

### 创建本地仓库

我们可以将任意一个文件夹作为一个本地仓库（也就是一个项目），输入：

```shell
git init
```

输入后，会自动生成一个git目录，注意这个目录是一个隐藏目录。

创建成功后，我们可以查看一下当前的一个状态，输入：

```shell
git status
```

如果我们已经成功配置了Git仓库，那么输入后可以看到：

```bash
On branch master

No commits yet
```

这表示我们还没有向仓库存放内容，还是一个空状态。

### 添加和提交

接着看看如何通过git来管理我们的版本，首先创建一个txt文档，然后随便写一点内容，接着输入：

```shell
git status
```

我们会得到提示：

```shell
Untracked files:
  (use "git add <file>..." to include in what will be committed)
	hello.txt

nothing added to commit but untracked files present (use "git add" to track)
```

其中Untracked files是未追踪文件的意思，也就是说，如果一个文件处于未追踪状态，那么git不会记录他的版本变化，这里我们将它添加到暂存区，那么他会自动变为追踪状态：

```shell
git add hello.txt #也可以add . 一次性添加目录下所有的
```
再次查看状态：

```shell
Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   hello.txt
```
现在文件的名称已经标为绿色，并且处于Changes to be committed下，因此我们的Hello.text已经被添加到暂存区了。

接着我们尝试提交到Git本地仓库里，注意需要输入描述方便后续查看：

```shell
git commit -m "你好"
```
接着，我们可以查看提交记录：

```shell
git log
git log --graph #表示绘制一张历史提交树状图
```
我们也可以查看最近一次变更的详细内容：

```shell
git show 0xxjaidi #这是提交后的id
```
再次查看状态，会显示已经是清空状态了

```shell
On branch master
nothing to commit, working tree clean
```
接着我们可以尝试修改一下文档，由于此时文档处于被追踪状态，那么git会去跟踪它的变化，如果说文件发生了修改，那么我们可以再次查看状态：

```shell
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   hello.txt
```
也就是说此时文件处于已修改的状态，我们可以再次提交新版本：

```shell
git add .
git commit -m '修改：你的修改内容' #m表示message，适合简单记录，不加会进入nano长篇说明
```
接着，我们查询一下提交记录，可以看到有两次提交记录。

我们可以创建一个`.gitignore`来确定文件忽略列表，如果忽略列表中的文件且不是追踪状态，那么git不会对他进行检查：

```yaml
# 这样就会匹配所有以txt结尾的文件
*.txt
# 虽然上面排除了所有txt结尾的文件，但是这个不排除
!666.txt
# 也可以直接指定一个文件夹，文件夹下的所有文件将全部忽略
test/
# 目录中所有以txt结尾的文件，但不包括子目录
xxx/*.txt
# 目录中所有以txt结尾的文件，包括子目录
xxx/**/*.txt
```
### 回滚

顾名思义，回滚到以前版本：

```shell
git reset --hard commitID
```
执行后，会重置当前状态，并且日志之后的日志全部清除了。

那么我要是想要回去呢？我们可以查看所有分支的操作记录：

```shell
git reflog
```
这样就能找到commitID，再次重置即可。

## 分支

分支就像我们树上的一个树枝一样，它们可能一开始的时候是同一根树枝，但是长着长着就开始分道扬镳了，这就是分支。我们的代码也是这样，可能一开始写基础功能的时候使用的是单个分支，但是某一天我们希望基于这些基础的功能，把我们的项目做成两个不同方向的项目，比如一个方向做Web网站，另一个方向做游戏服务端。

### 创建分支

我们可以通过以下命令来查看当前仓库中存在的分支：

```shell
git branch
```
我们发现，默认情况下有一个mater分支，即为主分支，通常为正式版本，其他分支一般在开发中频繁更新，我们现在基于当前分支来创建一个新的分支：

```shell
git branch test
# 删除对应分支
git branch -d test
```

现在我们修改文件后提交：

```sh
git commit -a -m 'master分支提交' 
# -a表示all，即跳过git add这一步，自动把之前追踪后的所有文件的修改和删除全部打包提交
```

此时查看日志，我们发现，我们当前的提交只适用于master提交，而新的test分支并没有发生修改。

现在我们切换到另一个分支：

```sh
git checkout test
```

此时，文件处于test分支下（即原来master分支下的文件并不存在），说明两个分支是独立的。

我们现在再来提交一次变更，会发现它只生效在test分支上。我们可以看看当前的分支状态：

```sh
git log --all --graph
```

### 合并分支

我们也可以将两个分支更新的内容合并到一个分支上，我们先切回主分支：

```sh
git checkout master
```

接着使用分支合并命令：

```sh
git merge test
```

会得到以下提示：

```sh
Auto-merging hello.txt
CONFLICT (content): Merge conflict in hello.txt
Automatic merge failed; fix conflicts and then commit the result.
```

合并过程中产生了冲突，因为两个分支都对同一个文件进行了修改，那么系统就会认为，我到底应该选哪一个呢：

我们可以查看哪里发生了冲突：

```sh
git diff
```

因此，此时我们有两个选项：

- 把master（test）分支退回到之前那个版本。
- 或者直接修改为最新版本的内容。

这样就不会冲突了。

### 变基分支

除了直接将分支进行合并以外，我们还可以进行变基操作，即修改分支开始的位置（合并是将分支收回主干），比如我们可以把test变基到master上，那么test会将分支起点，移动到master`最后一次提交的位置`：

```sh
git rebase master
```

变基后，test分支相当于同步了此前master分支的全部提交。

### 优点

我们还可以选择将其他分支上的提交作用于当前分支上，正中操作被称为cherrypick：

```sh
git cherry-pick commitID
```

这里我们在master分支上创建一个新的文件，提交此次更新，接着通过cherry-pick的方式将此次更新作用于test分支上。

IDEA当然可以将Git进行可视化的版本控制而不是手敲命令行。

## 远程仓库

远程仓库其实就是服务器上的仓库，他能远端保存我们的提交历史，并且实现多人合作，相当于我们将代码放到平台上进行托管。

远程仓库分为公有和私有，国内有gitee，国外有GitHub。

### 远程账户认证和推送

我们现在GitHub上创建一个自定义的仓库。

创建仓库后，我们可以通过推送来将本地的内容推送到远程仓库。

```sh
git remote add 名称 远程仓库地址
git push 远程仓库名称 本地分支名称 远端名称
```

push后面的两个参数，一个是远端名称，还有一个本地分支名称，但是如果本地分支名称和远端分支名称一致，那么不用指定远端分支名称，但是如果我们希望推送的分支在远端没有同名的，那么需要额外指定。推送前需要登陆账户，GitHub现在不允许使用用户名密码验证，只允许使用个人AccessToken来验证身份，所以我们需要先去生成一个Token才可以。

推送后，我们发现远程仓库中的内容已经与我们本地仓库中的内容保持一致了，注意，远程仓库也可以有很多个分支。

接着我们修改一下工作区的内容，提交到本地仓库后，再推送到远程仓库，提交的过程中我们注意观察提交记录：

```sh
git commit -a -m '修改文件'
git log --all --oneline --graph
git push origin master 
git log --all --oneline --graph
```

我们可以将远端和本地的分支进行绑定，绑定后就不需要指定分支名称了：

```sh
git push --set-upstream origin master:master
git push origin
```

在一个本地仓库对应一个远程仓库的情况下，远程仓库基本上就是纯粹的代码托管了（就像是网盘，就纯粹是存放代码的地方）

### 克隆项目

我们如果想要在另一台电脑上更改源码，或者添加另一个人来合作，那么clone就可以快速下载：

```sh
git clone 远程仓库地址
```

### 抓取，拉取和冲突解决

此时，会出现多个本地仓库加一台远程仓库，那么此时需要协同工作。

比如A完成了A的模块，并提交到了远程仓库，B还没有，当B提交时，B的本地仓库版本和远程仓库不一致，会发生冲突报错，此时B需要先pull（抓取操作），更新本地代码后再进行提交：

```sh
git fetch 远程仓库 #抓取：只获取但不合并（只是查看），后面需要我们手动合并（git merge）后提交
git pull 远程仓库 #拉取：获取合并
```

如果远程仓库中的提交和本地仓库中的提交没有去编写同一个文件，那么就可以直接拉取：

```sh
git pull 远程仓库
```

拉取后会自动进行合并，合并完成之后我们再提交即可。

但是如果两次提交都修改了同一个文件，那么就会遇到和多分支合并一样的情况，在合并时会产生冲突，这时就需要我们自己去解决冲突了。
