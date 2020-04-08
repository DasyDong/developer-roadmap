- [常用高阶命令](#常用高阶命令)
    - [git log](#git-log)
    - [git add](#git-add)
    - [git rebase](#git-rebase)
    - [Git revert](#git-revert)
    - [开始一个无历史的新分支](#开始一个无历史的新分支)
    - [无切换分支的从其它分支Checkout文件](#无切换分支的从其它分支checkout文件)
    - [使用rebase推送而非merge](#使用rebase推送而非merge)
    - [检查丢失的提交](#检查丢失的提交)
    - [克隆指定的远程分支](#克隆指定的远程分支)
    - [检测 你的分支的改变是否为其它分支的一部分](#检测-你的分支的改变是否为其它分支的一部分)
- [高阶](#高阶)
    - [分支的衍合 rebase](#分支的衍合-rebase)
    - [重写历史](#重写历史)
        - [改变最近一次提交](#改变最近一次提交)
        - [修改多个提交说明](#修改多个提交说明)
        - [核弹级选项: filter-branch](#核弹级选项-filter-branch)
    - [Stash](#stash)
        - [取消储藏(Un-applying a Stash)](#取消储藏un-applying-a-stash)
        - [从储藏中创建分支](#从储藏中创建分支)
    - [Git 调试](#git-调试)
        - [文件标注 git blame](#文件标注-git-blame)
        - [二分查找 git bisect](#二分查找-git-bisect)
    - [子模块](#子模块)
        - [子模块初步](#子模块初步)
        - [克隆一个带子模块的项目](#克隆一个带子模块的项目)
- [架构](#架构)
- [底层原理](#底层原理)
    - [底层命令 (Plumbing) 和高层命令 (Porcelain)](#底层命令-plumbing-和高层命令-porcelain)
    - [对象](#对象)
        - [tree (树) 对象](#tree-树-对象)
        - [Commit 对象](#commit-对象)
    - [Git References](#git-references)
        - [HEAD 标记](#head-标记)
        - [Tags](#tags)
        - [Remotes](#remotes)
    - [维护及数据恢复](#维护及数据恢复)
- [参考书](#参考书)
# 常用高阶命令
Git 是一套内容寻址文件系统
## git log

git log --pretty=format:"%h %s" --graph

* --oneline- 压缩模式，在每个提交的旁边显示经过精简的提交哈希码和提交信息，以一行显示。
* --graph- 图形模式，使用该选项会在输出的左边绘制一张基于文本格式的历史信息表示图。如果你查看的是单个分支的历史记录的话，该选项无效。
* --all- 显示所有分支的历史记录

## git add
暂存文件的部分改动
一般情况下，创建一个基于特性的提交是比较好的做法，意思是每次提交都必须代表一个新特性的产生或者是一个bug的修复。如果你修复了两个bug，或是添加了多个新特性但是却没有提交这些变化会怎样呢？在这种情况下，你可以把这些变化放在一次提交中。但更好的方法是把文件暂存(Stage)然后分别提交。
例如你对一个文件进行了多次修改并且想把他们分别提交。这种情况下，你可以在 add 命令中加上 -p 参数
```
git add -p [file_name]
```


## git rebase

如果你想要压缩最后两个commit，你需要运行下列命令。
```
git rebase -i HEAD~2
```

## Git revert
Git revert用来撤销某次操作，此次操作之前和之后的commit和history都会保留，并且把这次撤销作为一次最新的提交。git revert是提交一个新的版本，将需要revert的版本的内容再反向修改回去，版本会递增，不影响之前提交的内容。


## 开始一个无历史的新分支
```
git checkout --orphan NEW_BRANCH_NAME_HERE
```

## 无切换分支的从其它分支Checkout文件
```
git checkout BRANCH_NAME_HERE -- PATH_TO_FILE_IN_BRANCH_HERE
```


## 使用rebase推送而非merge
如果您正在团队中工作并且整个团队都在同一条branch上面工作，那么您就得经常地进行fetch/merge或者pull。Git中，分支的合并以所提交的merge来记录，以此表明一条feature分支何时与主分支合并。但是在多团队成员共同工作于一条branch的情形中，常规的merge会导致log中出现多条消息，从而产生混淆。因此，您可以在pull的时候使用rebase，以此来减少无用的merge消息，从而保持历史记录的清晰。
```
git pull --rebase
```

## 检查丢失的提交

尽管 reflog 是唯一检查丢失提交的方式。但它不是适应用于大型的仓库。那就是 fsck（文件系统检测）命令登场的时候了。

git fsck --lost-found

## 克隆指定的远程分支
```
git init
git remote add -t BRANCH_NAME_HERE -f origin REMOTE_REPO_URL_PATH_HERE
git checkout BRANCH_NAME_HERE
```

## 检测 你的分支的改变是否为其它分支的一部分
```
git cherry -v OTHER_BRANCH_NAME_HERE
#例如: 检测master分支
git cherry -v master
```

# 高阶

## 分支的衍合 rebase
把一个分支中的修改整合到另一个分支的办法有两种：merge 和 rebase（译注：rebase 的翻译暂定为“衍合”）

![](../pics/git/git-rebase1.png)

```
$ git checkout experiment
$ git rebase master
First, rewinding head to replay your work on top of it...
Applying: added staged command
```
原理是回到两个分支最近的共同祖先，根据当前分支（也就是要进行衍合的分支 experiment）后续的历次提交对象（这里只有一个 C3），生成一系列文件补丁，然后以基底分支（也就是主干分支 master）最后一个提交对象（C4）为新的出发点，逐个应用之前准备好的补丁文件，最后会生成一个新的合并提交对象（C3'），从而改写 experiment 的提交历史，使它成为 master 分支的直接下游, 如图所示
![](../pics/git/git-rebase2.png)


## 重写历史
### 改变最近一次提交
```
git commit --amend
```

### 修改多个提交说明
```
git rebase -i HEAD~3
```

### 核弹级选项: filter-branch

如果你想用脚本的方式修改大量的提交，还有一个重写历史的选项可以用——例如，全局性地修改电子邮件地址或者将一个文件从所有提交中删除。这个命令是filter-branch，这个会大面积地修改你的历史，所以你很有可能不该去用它，除非你的项目尚未公开，没有其他人在你准备修改的提交的基础上工作。尽管如此，这个可以非常有用。你会学习一些常见用法，借此对它的能力有所认识。

从所有提交中删除一个文件
这个经常发生。有些人不经思考使用git add .，意外地提交了一个巨大的二进制文件，你想将它从所有地方删除。也许你不小心提交了一个包含密码的文件，而你想让你的项目开源。filter-branch大概会是你用来清理整个历史的工具。要从整个历史中删除一个名叫password.txt的文件，你可以在filter-branch上使用--tree-filter选项：
```
$ git filter-branch --tree-filter 'rm -f passwords.txt' HEAD
Rewrite 6b9b3cf04e7c5686a9cb838c3f36a8cb6a0fc2bd (21/21)
Ref 'refs/heads/master' was rewritten
```

全局性地更换电子邮件地址
```
 git filter-branch --commit-filter '
        if [ "$GIT_AUTHOR_EMAIL" = "schacon@localhost" ];
        then
                GIT_AUTHOR_NAME="Scott Chacon";
                GIT_AUTHOR_EMAIL="schacon@example.com";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' HEAD
```

## Stash
### 取消储藏(Un-applying a Stash)
在某些情况下，你可能想应用储藏的修改，在进行了一些其他的修改后，又要取消之前所应用储藏的修改。Git没有提供类似于 stash unapply 的命令，但是可以通过取消该储藏的补丁达到同样的效果：
```
$ git stash show -p stash@{0} | git apply -R
```
同样的，如果你沒有指定具体的某个储藏，Git 会选择最近的储藏：
```
$ git stash show -p | git apply -R
```
你可能会想要新建一个別名，在你的 Git 里增加一个 stash-unapply 命令，这样更有效率。例如：
```
$ git config --global alias.stash-unapply '!git stash show -p | git apply -R'
$ git stash apply
$ #... work work work
$ git stash-unapply
```

### 从储藏中创建分支
如果你储藏了一些工作，暂时不去理会，然后继续在你储藏工作的分支上工作，你在重新应用工作时可能会碰到一些问题。如果尝试应用的变更是针对一个你那之后修改过的文件，你会碰到一个归并冲突并且必须去化解它。如果你想用更方便的方法来重新检验你储藏的变更，你可以运行 git stash branch，这会创建一个新的分支，检出你储藏工作时的所处的提交，重新应用你的工作，如果成功，将会丢弃储藏。
```
$ git stash branch testchanges
Switched to a new branch "testchanges"
# On branch testchanges
# Changes to be committed:
# (use "git reset HEAD <file>..." to unstage)
#
# modified:   index.html
#
# Changes not staged for commit:
# (use "git add <file>..." to update what will be committed)
#
# modified:   lib/simplegit.rb

Dropped refs/stash@{0} (f0dfc4d5dc332d1cee34a634182e168c4efc3359)
```

这是一个很棒的捷径来恢复储藏的工作然后在新的分支上继续当时的工作。

## Git 调试

Git 同样提供了一些工具来帮助你调试项目中遇到的问题。由于 Git 被设计为可应用于几乎任何类型的项目，这些工具是通用型，但是在遇到问题时可以经常帮助你查找缺陷所在。

### 文件标注 git blame

如果你在追踪代码中的缺陷想知道这是什么时候为什么被引进来的，文件标注会是你的最佳工具。它会显示文件中对每一行进行修改的最近一次提交。因此，如果你发现自己代码中的一个方法存在缺陷，你可以用git blame来标注文件，查看那个方法的每一行分别是由谁在哪一天修改的。下面这个例子使用了-L选项来限制输出范围在第12至22行：
```
$ git blame -L 12,22 simplegit.rb
^4832fe2 (Scott Chacon  2008-03-15 10:31:28 -0700 12)  def show(tree = 'master')
^4832fe2 (Scott Chacon  2008-03-15 10:31:28 -0700 13)   command("git show #{tree}")
^4832fe2 (Scott Chacon  2008-03-15 10:31:28 -0700 14)  end
^4832fe2 (Scott Chacon  2008-03-15 10:31:28 -0700 15)
9f6560e4 (Scott Chacon  2008-03-17 21:52:20 -0700 16)  def log(tree = 'master')
79eaf55d (Scott Chacon  2008-04-06 10:15:08 -0700 17)   command("git log #{tree}")
9f6560e4 (Scott Chacon  2008-03-17 21:52:20 -0700 18)  end
9f6560e4 (Scott Chacon  2008-03-17 21:52:20 -0700 19)
42cf2861 (Magnus Chacon 2008-04-13 10:45:01 -0700 20)  def blame(path)
42cf2861 (Magnus Chacon 2008-04-13 10:45:01 -0700 21)   command("git blame #{path}")
42cf2861 (Magnus Chacon 2008-04-13 10:45:01 -0700 22)  end
```


### 二分查找 git bisect

标注文件在你知道问题是哪里引入的时候会有帮助。如果你不知道，并且自上次代码可用的状态已经经历了上百次的提交，你可能就要求助于bisect命令了。bisect会在你的提交历史中进行二分查找来尽快地确定哪一次提交引入了错误。

例如你刚刚推送了一个代码发布版本到产品环境中，对代码为什么会表现成那样百思不得其解。你回到你的代码中，还好你可以重现那个问题，但是找不到在哪里。你可以对代码执行bisect来寻找。首先你运行git bisect start启动，然后你用git bisect bad来告诉系统当前的提交已经有问题了。然后你必须告诉bisect已知的最后一次正常状态是哪次提交，使用git bisect good [good_commit]：
```
$ git bisect start
$ git bisect bad
$ git bisect good v1.0
Bisecting: 6 revisions left to test after this
[ecb6e1bc347ccecc5f9350d878ce677feb13d3b2] error handling on repo
```
Git 发现在你标记为正常的提交(v1.0)和当前的错误版本之间有大约12次提交，于是它检出中间的一个。在这里，你可以运行测试来检查问题是否存在于这次提交。如果是，那么它是在这个中间提交之前的某一次引入的；如果否，那么问题是在中间提交之后引入的。假设这里是没有错误的，那么你就通过git bisect good来告诉 Git 然后继续你的旅程：
```
$ git bisect good
Bisecting: 3 revisions left to test after this
[b047b02ea83310a70fd603dc8cd7a6cd13d15c04] secure this thing
```
现在你在另外一个提交上了，在你刚刚测试通过的和一个错误提交的中点处。你再次运行测试然后发现这次提交是错误的，因此你通过git bisect bad来告诉Git：
```
$ git bisect bad
Bisecting: 1 revisions left to test after this
[f71ce38690acf49c1f3c9bea38e09d82a5ce6014] drop exceptions table
```
这次提交是好的，那么 Git 就获得了确定问题引入位置所需的所有信息。它告诉你第一个错误提交的 SHA-1 值并且显示一些提交说明以及哪些文件在那次提交里修改过，这样你可以找出缺陷被引入的根源：
```
$ git bisect good
b047b02ea83310a70fd603dc8cd7a6cd13d15c04 is first bad commit
commit b047b02ea83310a70fd603dc8cd7a6cd13d15c04
Author: PJ Hyett <pjhyett@example.com>
Date:   Tue Jan 27 14:48:32 2009 -0800

    secure this thing

:040000 040000 40ee3e7821b895e52c1695092db9bdc4c61d1730
f24d3c6ebcfc639b1a3814550e62d60b8e68a8e4 M  config
```
当你完成之后，你应该运行git bisect reset来重设你的HEAD到你开始前的地方，否则你会处于一个诡异的地方：
```
$ git bisect reset
```
这是个强大的工具，可以帮助你检查上百的提交，在几分钟内找出缺陷引入的位置。事实上，如果你有一个脚本会在工程正常时返回0，错误时返回非0的话，你可以完全自动地执行git bisect。首先你需要提供已知的错误和正确提交来告诉它二分查找的范围。你可以通过bisect start命令来列出它们，先列出已知的错误提交再列出已知的正确提交：
```
$ git bisect start HEAD v1.0
$ git bisect run test-error.sh
```
这样会自动地在每一个检出的提交里运行test-error.sh直到Git找出第一个破损的提交。你也可以运行像make或者make tests或者任何你所拥有的来为你执行自动化的测试。

## 子模块
经常有这样的事情，当你在一个项目上工作时，你需要在其中使用另外一个项目。也许它是一个第三方开发的库或者是你独立开发和并在多个父项目中使用的。这个场景下一个常见的问题产生了：你想将两个项目单独处理但是又需要在其中一个中使用另外一个。

Git 通过子模块处理这个问题。子模块允许你将一个 Git 仓库当作另外一个Git仓库的子目录。这允许你克隆另外一个仓库到你的项目中并且保持你的提交相对独立。

### 子模块初步
假设你想把 Rack 库（一个 Ruby 的 web 服务器网关接口）加入到你的项目中，可能既要保持你自己的变更，又要延续上游的变更。首先你要把外部的仓库克隆到你的子目录中。你通过git submodule add将外部项目加为子模块：
```
$ git submodule add git://github.com/chneukirchen/rack.git rack
Initialized empty Git repository in /opt/subtest/rack/.git/
remote: Counting objects: 3181, done.
remote: Compressing objects: 100% (1534/1534), done.
remote: Total 3181 (delta 1951), reused 2623 (delta 1603)
Receiving objects: 100% (3181/3181), 675.42 KiB | 422 KiB/s, done.
Resolving deltas: 100% (1951/1951), done.

```

### 克隆一个带子模块的项目

这里你将克隆一个带子模块的项目。当你接收到这样一个项目，你将得到了包含子项目的目录，但里面没有文件：
```
$ git clone git://github.com/schacon/myproject.git
Initialized empty Git repository in /opt/myproject/.git/
remote: Counting objects: 6, done.
remote: Compressing objects: 100% (4/4), done.
remote: Total 6 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (6/6), done.
$ cd myproject
$ ls -l
total 8
-rw-r--r--  1 schacon  admin   3 Apr  9 09:11 README
drwxr-xr-x  2 schacon  admin  68 Apr  9 09:11 rack
$ ls rack/
$
```
rack目录存在了，但是是空的。你必须运行两个命令：git submodule init来初始化你的本地配置文件，git submodule update来从那个项目拉取所有数据并检出你上层项目里所列的合适的提交：
```
$ git submodule init
Submodule 'rack' (git://github.com/chneukirchen/rack.git) registered for path 'rack'
$ git submodule update
Initialized empty Git repository in /opt/myproject/rack/.git/
remote: Counting objects: 3181, done.
remote: Compressing objects: 100% (1534/1534), done.
remote: Total 3181 (delta 1951), reused 2623 (delta 1603)
Receiving objects: 100% (3181/3181), 675.42 KiB | 173 KiB/s, done.
Resolving deltas: 100% (1951/1951), done.
Submodule path 'rack': checked out '08d709f78b8c5b0fbeb7821e37fa53e69afcf433'
```


# 架构
GIT的架构，可以分为几个部分：

本地工作区(working directory)
暂存区(stage area, 又称为索引区, index)、
本地仓库(local repository)、
远程仓库副本
远程仓库(remote repository)。
如图：
![](../pics/git/git.png)

工作区(working directory)
工作区，简言之就是你工作的区域。对于git而言，就是的本地工作目录。工作区的内容会包含提交到暂存区和版本库(当前提交点)的内容，同时也包含自己的修改内容。

暂存区(stage area, 又称为索引区index)
暂存区是git中一个非常重要的概念。是我们把修改提交版本库前的一个过渡阶段。查看GIT自带帮助手册的时候，通常以index来表示暂存区。在工作目录下有一个.git的目录，里面有个index文件，存储着关于暂存区的内容。git add命令将工作区内容添加到暂存区。

本地仓库(local repository)
版本控制系统的仓库，存在于本地。当执行git commit命令后，会将暂存区内容提交到仓库之中。在工作区下面有.git的目录，这个目录下的内容不属于工作区，里面便是仓库的数据信息，暂存区相关内容也在其中。

远程版本库(remote repository)
远程版本库与本地仓库概念基本一致，不同之处在于一个存在远程，可用于远程协作，一个却是存在于本地。通过push/pull可实现本地与远程的交互；

远程仓库副本
可以理解为存在于本地的远程仓库缓存。如需更新，可通过git fetch/pull命令获取远程仓库内容。使用fech获取时，并未合并到本地仓库，此时可使用git merge实现远程仓库副本与本地仓库的合并。


# 底层原理

## 底层命令 (Plumbing) 和高层命令 (Porcelain)
```
$ ls
HEAD
branches/
config
description
hooks/
index
info/
objects/
refs/
```
该目录下有可能还有其他文件，但这是一个全新的 git init 生成的库，所以默认情况下这些就是你能看到的结构。

四个重要的文件或目录：HEAD 及 index 文件，objects 及 refs 目录。这些是 Git 的核心部分

objects 目录存储所有实际的数据数据内容

refs 目录存储指向数据 (分支) 的提交对象的指针

HEAD 文件指向当前分支, 其实就是工作区的在版本库中的那个提交点，最终会指向一个40位的HASH值；

index 文件保存了暂存区域信息

新版本的 Git 不再使用 branches 目录

description 文件仅供 GitWeb 程序使用

config 文件包含了项目特有的配置选项

info 目录保存了一份不希望在 .gitignore 文件中管理的忽略模式 (ignored patterns) 的全局可执行文件

hooks 目录保存了客户端或服务端钩子脚本。

## 对象

在之前我们提到过，Git是一套内容寻址（content-addressable）文件系统，那么Git是怎么进行寻址呢？其实，寻址无非就是查找，而Git采用HashTable的方式进行查找，也就是说，Git只是通过简单的存储键值对（key-value pair）的方式来实现内容寻址的，而key就是文件（头+内容）的哈希值（采用sha-1的方式，40位），value就是经过压缩后的文件内容。因此，在接下来的实践中，我们会经常通过40位的hash值来进行plumbing操作，几乎每一个plumbing命令都需要通过key来指定所要操作的对象。

Git对象的类型包括：BLOB、tree对象、commit对象。

BLOB对象可以存储几乎所有的文件类型，全称为binary large object，顾名思义，就是大的二进制表示的对象，这种对象类型和数据库中的BLOB类型（经常用来在数据库中存储图片、视频等）是一样的，当作一种数据类型即可；tree对象是用来组织BLOB对象的一种数据类型，你完全可以把它想象成二叉树中的树节点，只不过Git中的树不是二叉树，而是"多叉树"；commit对象表示每一次的提交操作，由tree对象衍生，每一个commit对象表示一次提交，在创建的过程中可以指定该commit对象的父节点，这样所有的commit操作便可以连接在一起，而这些commit对象便组成了提交树，branch只不过是这个树中的某一个子树罢了。如果你能理解commit树，那Git几乎就已经理解了一半了。

Git对象的存储方式也很简单，基本可以用如下表达式来表示：
```
Key = sha1(file_header + file_content)

Value = zlib(file_content)
```
简单来说，Git 将文件头与原始数据内容拼接起来，并计算拼接后的新内容的 40位的sha-1校验和，将该校验和的前2位作为object目录中的子目录的名称，后38位作为子目录中的文件名；然后，Git 用zlib的方式对数据内容进行压缩，最后将用 zlib 压缩后的内容写入磁盘。文件头的格式为 "blob #{content.length}\0"，例如"blob 16\000"，这种文件头格式也是经常采用的格式。对于tree对象和commit对象，文件头的格式都是一样的，但是其文件数据却是有固定格式的，鉴于本次只是Git原理的基本介绍，这里不再详细描述，有兴趣的可以去Git的官网查找相关文档进行了解；其实也可以自己按照理解构思一下，如果让你来设计这种格式，应该如何设计：tree对象类似于树中节点的定义，在tree对象中要包含对连接的BLOB对象的引用，而commit对象与tree对象类似，要包含提交的tree对象的引用，想到这里，我觉得文档的阅读大概也就可以省去了。


对象暂存区
在procelain命令中，为了将修改的文件加入暂存区（也叫索引库，将修改的文件key-value化，.git根目录下的index文件记录该暂存区中的文件索引），我们会使用git add filename命令。那么在git add这个命令的背后，Git是如何使用plumbing命令来完成文件的索引操作呢？其实，git add命令对应着两个基本的plumbing命令：
```
git hash-object #获取指定文件的key，如果带上-w选项，则会将该对象的value进行存储

git update-index #将指定的object加入索引库，需要带上—add选项
```
因此，git add命令在plumbing命令中其实是分成了两步：首先，通过hash-object命令将需要暂存的文件进行key-value化转换成Git对象，并进行存储，拿到这些文件的key；然后，通过update-index命令将这些对象加入到索引库进行暂存，这样便完成了Git文件的暂存操作。如果要根据Git对象的key来查看文件的信息，还需要涉及下面的一个plumbing命令：
```
git cat-file –p/-t key #获取指定key的对象信息，-p打印详细信息，-t打印对象的类型
```
利用该命令可以查看已经key-value化的Git对象的详细信息。

### tree (树) 对象

接下去来看 tree 对象，tree 对象可以存储文件名，同时也允许存储一组文件。Git 以一种类似 UNIX 文件系统但更简单的方式来存储内容。所有内容以 tree 或 blob 对象存储，其中 tree 对象对应于 UNIX 中的目录，blob 对象则大致对应于 inodes 或文件内容。一个单独的 tree 对象包含一条或多条 tree 记录，每一条记录含有一个指向 blob 或子 tree 对象的 SHA-1 指针，并附有该对象的权限模式 (mode)、类型和文件名信息。以 simplegit 项目为例，最新的 tree 可能是这个样子：
```
$ git cat-file -p master^{tree}
100644 blob a906cb2a4a904a152e80877d4088654daad0c859      README
100644 blob 8f94139338f9404f26296befa88755fc2598c289      Rakefile
040000 tree 99f1a6d12cb4b6f19c8655fca46c3ecf317074e0      lib
```
master^{tree} 表示 master 分支上最新提交指向的 tree 对象。请注意 lib 子目录并非一个 blob 对象，而是一个指向另一个 tree 对象的指针：
```
$ git cat-file -p 99f1a6d12cb4b6f19c8655fca46c3ecf317074e0
100644 blob 47c6340d6459e05787f644c2447d2595f5d3a54b      simplegit.rb
```

从概念上来讲，Git 保存的数据如图  所示。
![](../pics/git/git-commit.png)

### Commit 对象

```
$ git cat-file -p fdf4fc3
tree d8329fc1cc938780ffdd9f94e0d364e0ea74f579
author Scott Chacon <schacon@gmail.com> 1243040974 -0700
committer Scott Chacon <schacon@gmail.com> 1243040974 -0700

first commit
```

commit 对象有格式很简单：指明了该时间点项目快照的顶层树对象、作者/提交者信息（从 Git 设置的 user.name 和 user.email中获得)以及当前时间戳、一个空行，以及提交注释信息。

## Git References

你可以执行像 git log 1a410e 这样的命令来查看完整的历史，但是这样你就要记得 1a410e 是你最后一次提交，这样才能在提交历史中找到这些对象。你需要一个文件来用一个简单的名字来记录这些 SHA-1 值，这样你就可以用这些指针而不是原来的 SHA-1 值去检索了。

在 Git 中，我们称之为“引用”（references 或者 refs，译者注）。你可以在 .git/refs 目录下面找到这些包含 SHA-1 值的文件。在这个项目里，这个目录还没不包含任何文件，但是包含这样一个简单的结构：
```
$ find .git/refs
.git/refs
.git/refs/heads
.git/refs/tags
$ find .git/refs -type f
$
```

### HEAD 标记

HEAD 文件是一个指向你当前所在分支的引用标识符。这样的引用标识符——它看起来并不像一个普通的引用——其实并不包含 SHA-1 值，而是一个指向另外一个引用的指针。如果你看一下这个文件，通常你将会看到这样的内容：
```
$ cat .git/HEAD
ref: refs/heads/master
```
如果你执行 git checkout test，Git 就会更新这个文件，看起来像这样：
```
$ cat .git/HEAD
ref: refs/heads/test
```

### Tags

Tag 对象非常像一个 commit 对象——包含一个标签，一组数据，一个消息和一个指针。最主要的区别就是 Tag 对象指向一个 commit 而不是一个 tree。它就像是一个分支引用，但是不会变化——永远指向同一个 commit，仅仅是提供一个更加友好的名字。

正如我们在第二章所讨论的，Tag 有两种类型：annotated 和 lightweight 。你可以类似下面这样的命令建立一个 lightweight tag：
```
$ git update-ref refs/tags/v1.0 cac0cab538b970a37ea1e769cbbde608743bc96d
```
这就是 lightweight tag 的全部 —— 一个永远不会发生变化的分支。 annotated tag 要更复杂一点。如果你创建一个 annotated tag，Git 会创建一个 tag 对象，然后写入一个指向指向它而不是直接指向 commit 的 reference。你可以这样创建一个 annotated tag（-a 参数表明这是一个 annotated tag）：
```
$ git tag -a v1.1 1a410efbd13591db07496601ebc7a059dd55cfe9 -m 'test tag'
```
这是所创建对象的 SHA-1 值：
```
$ cat .git/refs/tags/v1.1
9585191f37f7b0fb9444f35a9bf50de191beadc2
```

### Remotes

如果你添加了一个 remote 然后推送代码过去，Git 会把你最后一次推送到这个 remote 的每个分支的值都记录在 refs/remotes 目录下。例如，你可以添加一个叫做 origin 的 remote 然后把你的 master 分支推送上去：
```
$ git remote add origin git@github.com:schacon/simplegit-progit.git
$ git push origin master
Counting objects: 11, done.
Compressing objects: 100% (5/5), done.
Writing objects: 100% (7/7), 716 bytes, done.
Total 7 (delta 2), reused 4 (delta 1)
To git@github.com:schacon/simplegit-progit.git
   a11bef0..ca82a6d  master -> master
```
然后查看 refs/remotes/origin/master 这个文件，你就会发现 origin remote 中的 master 分支就是你最后一次和服务器的通信。
```
$ cat .git/refs/remotes/origin/master
ca82a6dff817ec66f44342007202690a93763949
```

## 维护及数据恢复
[维护及数据恢复](http://iissnan.com/progit/html/zh/ch9_7.html)

# 参考书

[Git内部原理](http://iissnan.com/progit/html/zh/ch9_0.html)

[Progit](https://github.com/progit/progit2)

