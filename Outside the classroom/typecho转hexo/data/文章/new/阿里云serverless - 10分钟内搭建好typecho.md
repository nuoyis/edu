---
title: 阿里云serverless - 10分钟内搭建好typecho
date: 2023-12-07 07:57:00
categories: 教程类
tags: []
---
首先你需要从我仓库复制一份我改造好版本的serverless-typecho
仓库地址:```https://github.com/nuoyis/serverless-typecho```
然后阿里云登录，在搜索中搜索函数计算FC
点击应用，然后创建应用(已经创建了一个的情况下需要点击)
![请输入图片描述](https://images.nuoyis.net/blog/typecho/uploads/2023/12/1425095997.png)
用你的github账户绑定，填写这一块就可以点击下方的创建并部署默认环境。
![请输入图片描述](https://images.nuoyis.net/blog/typecho/uploads/2023/12/2301635979.png)
然后自备一个mysql数据库或者直接使用sqlite3，使用sqlite3得自己想办法备份，复制到nas的内容可能需要开一台小时服务器来拷贝数据。
（数据库如果太贵，[点击这里](https://www.west.cn/?ReferenceID=1902196)进入注册，然后点击上方虚拟主机->mysql数据库，100M才100元一年）
typecho填好数据库，一直下一步就行了。

