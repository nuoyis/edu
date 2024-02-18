---
title: Git笔记：命令操作
date: 2023-07-26 07:34:00
categories: Git
tags: [Git,Git命令]
---
Git可以通过可视化的图形界面来操作，也可以根据命令行来进行操作


<!--more-->

##查看版本
**指令：** [label color="red"]git -v[/label] 
![1.png][1]


----------

##创建仓库

###从本地创建仓库
**指令：** [label color="red"]git init[/label] 
在 [label color="default"]仓库[/label] 中创建一个文件夹，然后进入文件夹路径，在文件夹路径下启动命令行窗口，输入 `git init` 初始化仓库。
![2.png][2]


###从远程仓库克隆一个到本地(下载)
**指令：** [label color="red"]git clone HTTPS网址[/label]
**指令：** [label color="red"]git clone HTTPS网址 (想要修改成的昵称)[/label]
在仓库中，进入命令行窗口输入 `git clone HTTPS网址` ，文件夹路径和远程仓库的名称保持一致
![3.png][3]
![4.png][4]
当然，在网址后也可以加上修改的昵称**重命名**
![5.png][5]
####配置仓库
**指令：** [label color="red"]git config user.name/user.email 账户/邮箱[/label] 
**全局配置指令：** [label color="red"]git config --global user.name/user.email 账户/邮箱[/label] 
**需要注意的是：config后面的两个参数必须都传递。**

![6.png][6]


----------
##文件操作
![7.png][7]
###暂存区和工作区
进入当前某个文件夹路径中，查看暂存区的操作
**指令：** [label color="red"]git status[/label] 
![8.png][8]
将**工作区**的文件添加到**暂存区**
**指令：** [label color="red"]git add 文件名[/label] 
**指令：** [label color="red"]git add *.后缀名(通配符)[/label] 
![9.png][9]
将**暂存区**的文件返回到**工作区**
**指令：** [label color="red"]git rm --cached 文件名[/label] 
![10.png][10]

###暂存区和存储区
####提交
**指令：** [label color="red"]git commit -m 新增消息[/label] 
![11.png][11]
####查看当前提交文件记录
**指令：** [label color="red"]git log[/label] 
**指令：** [label color="red"]git log --oneline[/label] 
![12.png][12]
当然也可以修改文件删除文件,操作一致
![13.png][13]

####文件误删除
如果是文件**误删除**，在工作区删除了，而在存储区中还有这样的文件。也就是没有提交(commit)删除操作的情况下**可以恢复**。
**指令：** [label color="red"]git restore 文件名[/label] 
![14.png][14]

#####版本回溯
如果是提交了删除操作，可以采用版本回溯,git log --oneline查询到历史记录
**指令：** [label color="red"]git reset --hard 版本号[/label] 

```other
Alfonso Kevin@DESKTOP-OROG5BQ MINGW64 /e/Git/warehouse/test/local-rep-3 (master)
$ git log --oneline
8c6b885 (HEAD -> master) delete
db8051b 增加

Alfonso Kevin@DESKTOP-OROG5BQ MINGW64 /e/Git/warehouse/test/local-rep-3 (master)
$ git reset --hard db8051b
HEAD is now at db8051b 增加

Alfonso Kevin@DESKTOP-OROG5BQ MINGW64 /e/Git/warehouse/test/local-rep-3 (master)
$ git log --oneline
db8051b (HEAD -> master) 增加

```
![15.png][15]
#####历史保留恢复已经提交的误删除文件
**指令：** [label color="red"]git revert 提交删除的版本号[/label] 
注意：这里的版本号是提交删除的版本号，会恢复到这个版本号之前的一次状态

```other
Alfonso Kevin@DESKTOP-OROG5BQ MINGW64 /e/Git/warehouse/test/local-rep-3 (master)
$ git revert a8f4f88
hint: Waiting for your editor to close the file... "E:\\JDK\\Notepad++\\notepad++.exe" -multiInst -notabbar -nosession -noPlugin: line 1: E:\JDK\Notepad++\notepad++.exe: No such file or directory
error: There was a problem with the editor '"E:\\JDK\\Notepad++\\notepad++.exe" -multiInst -notabbar -nosession -noPlugin'.
Please supply the message using either -m or -F option.


```
![16.png][16]
----------

##分支操作
###添加分支
**指令：** [label color="red"]git branch 分支名[/label] 
添加分支一定是基于commmit操作，也就是在 [label color="blue"].git\refs\heads[/label] 中已经有master的操作后添加其他的分支。
![17.png][17]

###查看有多少个分支
**指令：** [label color="red"]git branch -v[/label] 
![18.png][18]
###切换分支
**指令：** [label color="red"]git checkout 分支名[/label] 
###创建一个分支并切换
**指令：** [label color="red"]git checkout -b 分支名[/label]
###删除分支
**指令：** [label color="red"]git branch -d 分支名[/label]

----------
##分支操作-合并与冲突
需要在master分支中合并，所以需要先切换到master分支
**指令：** [label color="red"]git checkout master[/label]
合并
**指令：** [label color="red"]git merge 分支名[/label]
对于重复的文件名需要 [label color="red"]手动修改[/label] ，对应手动修改后的文件名再次**add**并**commit**即可。
![19.png][19]


----------
##标签操作
给当前的提交版本增加一个**别名**，以后可以通过别名访问
###添加标签
**指令：** [label color="red"]git tag 标签名 历史版本号[/label]
历史版本号可以通过 `git log` 进行查询,每一个版本都可以增加一个标签，但是不能重复

![20.png][20]
###通过标签查看该历史记录
**指令：** [label color="red"]git log 标签名[/label]
![21.png][21]

###删除标签
**指令：** [label color="red"]git tag -d 标签名[/label]

###通过标签创建分支
**分支就是引用了一个提交的版本号，标签就是给标签增加了别名**
**指令：** [label color="red"]git checkout -b 标签名[/label]

----------
##远程仓库
###将本地仓库文件推送到远程仓库
**指令：** [label color="red"]git push origin[/label]
origin的值在config文件中可以查询
![22.png][22]
如果origin中url的值是ssh的形式，那么在yes发送后，会报错，对于ssh需要我们提供安全认证功能：
**指令：** [label color="red"]ssh-keygen -t rsa -C url(SSH的形式)[/label]
这样就会获得一个SSH安全密钥，储存在 [label color="blue"]C:\Users\用户\.ssh[/label] 的路径中，复制pub文件内容
在对应的github/gitee个人中找到SSH安全密钥并认证即可。在使用： `git push origin` 就可以推送了。
###将远程仓库拉取文件到本地仓库
**指令：** [label color="red"]git pull origin[/label]

我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/3082422305.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/419845443.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/3358746962.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/1247006239.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/3867739987.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/3644756589.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/221299862.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/2932811235.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/07/2426057455.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/07/2684448617.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/07/1351228645.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/07/3144221335.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/07/3110078277.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/07/2807430087.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/07/1149012139.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/07/523357109.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/07/1717707478.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/07/2840058386.png
  [19]: https://img.kaijavademo.top/typecho/uploads/2023/07/3629626473.png
  [20]: https://img.kaijavademo.top/typecho/uploads/2023/07/2286074250.png
  [21]: https://img.kaijavademo.top/typecho/uploads/2023/07/3895977117.png
  [22]: https://img.kaijavademo.top/typecho/uploads/2023/07/3828900084.png