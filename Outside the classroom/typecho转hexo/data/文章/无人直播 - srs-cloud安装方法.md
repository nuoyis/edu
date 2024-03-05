---
title: 无人直播 - srs-cloud安装方法
date: 2023-08-08 07:05:00
categories: 技术类
tags: []
---
由于本博客之前编写过安装docker和宝塔的方法，所以我将安装docker教程和安装宝塔教程放在下面。

>宝塔安装教程:https://www.nuoyis.net/244.html
>docker安装教程:https://www.nuoyis.net/492.html

这里用宝塔就会方便许多，直接插件内搜索 直播 就行了。找到SRS音视频服务器安装后点击启动。
如下图所示
![宝塔1][1]
看到安装完成即可
![宝塔2][2]
![宝塔3][3]

docker版本搭建方法：输入以下命令
官方库:https://github.com/ossrs/srs-cloud
```shell
docker run --rm -it -p 2022:2022 -p 1935:1935/tcp -p 1985:1985/tcp \
  -p 8080:8080/tcp -p 8000:8000/udp -p 10080:10080/udp --name srs-cloud \
  -v $HOME/db:/data ossrs/srs-cloud:1
```

搭建好后，直接如下图配置好(推流地址和密钥每个平台获取必须实名认证)
![配置][4]
检查状态
![检查状态][5]
查看直播是否在播放(我的直播间:http://live.bilibili.com/22771547)
![直播生效][6]
如果你需要播放一些视频电影，必须找无版权的，不然等待封号或者法律诉讼


  [1]: https://io.nuoyis.net/typecho/uploads/2023/08/470005383.png
  [2]: https://io.nuoyis.net/typecho/uploads/2023/08/3092235857.png
  [3]: https://io.nuoyis.net/typecho/uploads/2023/08/729303847.png
  [4]: https://io.nuoyis.net/typecho/uploads/2023/08/1808604671.png
  [5]: https://io.nuoyis.net/typecho/uploads/2023/08/708829982.png
  [6]: https://io.nuoyis.net/typecho/uploads/2023/08/973339907.png