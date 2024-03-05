---
title: 博客(wordpress,typecho)安装教程
date: 2022-08-13 21:24:00
categories: guing
tags: []
---
>最近我的朋友给我发了一条消息，说他不会安装博客之类的东西。  
下面我来教大家如何安装wordpress和typecho.  
首先你需要域名并把域名解析到一台服务器或虚拟主机。  
这里推荐星辰云虚拟主机，很好用也很快.  
博客最后是视频讲解部分，如果文字看不懂可以看下面  
本搭建的内容到时候全部在移动云盘内下载  
网盘下载地址:https://www.bilibili.com/read/cv29085115/
首先下载wordpress安装包,或者typecho安装包.  
wordpress下载地址:[](https://wordpress.org)<https://wordpress.org>  
这里已经下载好了。我们打开星辰云进行上传(宝塔也是)  
wordpress一开始有个数据库填入，一般情况下数据库名是和数据库表相同(特殊情况请联系你的数据库服务商寻求帮助)  
自定义前缀开头可以改，但是请不要删除\_符号  
然后进入下一步设置(/wp-admin)站点用户名和密码，按要求和个性自己定制下  
安装主题直接进入设置，点击主题再点击  
typecho  
typecho下载地址:[](https://typecho.org)<https://typecho.org>  
这里已经下载好了。我们打开星辰云进行上传(宝塔也是)  
这好像是开发版有些bug  
再推荐使用个主题，主题非常漂亮好看，地址:[](https://github.com/bhaoo/cuckoo)<https://github.com/bhaoo/cuckoo>  
搭建也是wordpress同理，建议选择pdo驱动器,其他可以根据自身情况选择  
主题安装方法是找到usr/themes目录，创建Cuckoo  
再把本云盘内主题解压后删除zip文件并在后台(/admin)设置中启用  
问题综合  
1.后台被别人一下识别出地址为/admin怎么办?  
首先在config.inc.php中的`define **TYPECHO_ADMIN_DIR** /admin/`改名为其他(或者就改成wordpress那样什么-admin)，并将文件夹重命名为相同名字  
2.正常访问文章出现一些404报错怎么办  
需要配置伪静态typecho没有伪静态用wordpress的  
视频教程  
[\#BV#](https://www.bilibili.com/video/BV1yN4y157HD)
