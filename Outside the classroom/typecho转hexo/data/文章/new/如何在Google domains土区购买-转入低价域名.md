---
title: 如何在Google domains土区购买-转入低价域名
date: 2023-07-22 08:21:00
categories: 技术类
tags: []
---
>可以找我代注册代续费，在扣除的美元上只需要给我5元作为手续费

## 购买Google domains域名，需要注意:
1.如果你需要备案或者迁移到国内，需要等待60天时间，等待期过后即可迁出
迁出方式:管理->注册设置->转出(注意注册时间不得超过9年，且关闭网域锁定)
![转出截图][1]
2.Google domains在60天内，你可以使用国内dns厂商来提供dns解析，以加快转入国内注册商的速度
3.检查域名是否有建站黑历史，便宜多买了很多年但是因为黑历史导致百度"嫌弃"（被k)

## 注册方法
1.首先准备一个谷歌账户，再准备一个万事达的储蓄卡/信用卡，然后提前准备好国内厂商dns的添加。这里准备了一张现在绝版的非人哉万事达借记卡。
2.准备好后，打开网址https://domains.google.com，查看区域是否是土耳其，然后点击获取新域名(如果你需要淘一个四位字母域名，可以通过[阿里云域名批量注册-高级版][2]来查询,并在百度搜索建站历史查询的站点查询域名是否有黑产类的历史)
注册价格如下:
![注册价格][3]
3.找到自己心仪的域名后，加入购物车，填写好whois(就填最真实的),然后关闭续订(看你自己愿不愿意),绑定自己事先准备好的万事达卡，这个万事达扣费是多扣的，只是为了稳定汇率(所以多准备1美元)
4.注册好后需要修改dns到国内看这一条，点击管理->DNS->自定义域名服务器->管理域名服务器->填写后点击上面dns切换的那个标语。
![dns切换][4]
以阿里云为例，阿里云的dns地址是:
```other
ns1.alidns.com
ns2.alidns.com
```
阿里云dns添加地址:https://dns.console.aliyun.com
![阿里云dns添加][5]
输入域名确定等待就解析完成了。

## 转入方法
转入与注册大同小异，首先询问你的域名商，获取转移码后点击转移->输入转移域名->输入导入码->一键继续(如果配置whois就如实填写)->支付就完成转入


  [1]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3833482251.png
  [2]: https://check.aliyun.com/domain/bulk-search/advance.htm
  [3]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/2327792516.png
  [4]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3719657598.png
  [5]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/1029961106.png