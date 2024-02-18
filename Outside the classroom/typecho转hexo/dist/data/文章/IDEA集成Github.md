---
title: IDEA集成Github
date: 2023-07-26 08:05:00
categories: Git
tags: [Git,IDEA,Github]
---
在开发工具中集成Git，使用IDEA集成Gitee也是同理


<!--more-->

##发布到Github
把当前创建好的项目发布到Github，**让其他开发人员共享项目**
![1.png][1]
然后进行授权登录Github网站，授权成功后点击Share，选择想要上传的文件。
##修改文件并上传
右键对应的文件
![2.png][2]
注意提交应该是 [label color="blue"]Commit and push[/label] 提交到本地仓库并上传到远程仓库
![3.png][3]
##把远程仓库的文件同步到本地
从远程仓库修改文件后，在IDEA中选择pull就可以了
![4.png][4]
##从远程仓库(Github)中下载到本地仓库
其他开发人员想要开发项目，项目已经发布到远程仓库中，从远程仓库克隆clone即可
![5.png][5]
![6.png][6]

这样不同开发人员，可以通过开发工具，对同一个仓库中的代码文件进行开发和维护了。

我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1626966696.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3133373253.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/295458294.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/976342425.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/2522435889.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/3511344724.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/4012932315.jpg