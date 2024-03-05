---
title: Linux-安装nginx改造升级版(Tengine)
date: 2022-10-15 20:50:00
categories: 教程类
tags: []
---

>对于nginx开源代码基础上(nginx速度快、并发强、高稳定性等),阿里云并对此做出了更好的优化。对于淘宝和支付宝已率先证明Tengine针对大型企业网站高并发的优化以及安全稳定性    Tengine是由淘宝网发起的Web服务器项目。它在Nginx的基础上，针对大访问量网站的需求，添加了很多高级功能和特性。Tengine的性能和稳定性已经在大型的网站如淘宝网，天猫商城等得到了很好的检验。它的最终目标是打造一个高效、稳定、安全、易用的Web平台。    Tengine增添的内容:    1.继承Nginx的所有特性,兼容Nginx的配置，可用于正向代理场景；    2.支持异步OpenSSL，可使用硬件如:QAT进行HTTPS的加速与卸载；    3.增强相关运维、监控能力,比如异步打印日志及回滚,本地DNS缓存,内存监控等；    4.Stream模块支持server_name指令；    5.更加强大的负载均衡能力，包括一致性hash模块、会话保持模块，还可以对后端的服务器进行主动健康检查，根据服务器状态自动上线下线，以及动态解析upstream中出现的域名；    6.输入过滤器机制支持。通过使用这种机制Web应用防火墙的编写更为方便；    7.支持设置proxy、memcached、fastcgi、scgi、uwsgi在后端失败时的重试次数；    8.动态脚本语言Lua支持。扩展功能非常高效简单；    9.支持按指定关键字(域名，url等)收集Tengine运行状态；    10.组合多个CSS、JavaScript文件的访问请求变成一个请求；    11.自动去除空白字符和注释从而减小页面的体积    12.自动根据CPU数目设置进程个数和绑定CPU亲缘性；    13.监控系统的负载和资源占用从而对系统进行保护；    14.显示对运维人员更友好的出错信息，便于定位出错机器；；    15.更强大的防攻击（访问速度限制）模块；    16.更方便的命令行参数，如列出编译的模块列表、支持的指令等；    17.支持Dubbo协议；    18.可以根据访问文件类型设置过期时间。
介绍这么多，下载以及安装方式    [<a href="https://tengine.taobao.org/download_cn.html">https://tengine.taobao.org/download_cn.html][1]</a>    源码编译安装        ./configture
        make
        //make install
(所有文件均要解压，解压步骤不知道的操作如下:)        wget (你复制的下载链接 例如:wget [https://tengine.taobao.org/download/tengine-2.3.2.tar.gz][2])
        tar -xzvf (你的tar.gz文件名 例如:tar -xzvf tengine-2.3.2.tar.gz)
        ll //查看有没有
注:编译安装后的配置文件在/usr/local/nginx,可通过-prefix指定根路径
手动安装    警告:需要安装pcre/zlib/openssl模块(也是Linux和Centos系统中必要插件,阿里云云服务器不能使用yum只能手动编译安装
安装的软件包    openssl-*.*.*.tar.gz    pcre-<em>.*.</em>.tar.gz    zlib-*.*.*.tar.gz    tengine-<em>.*.</em>.tar.gz
这四个安装包目前博客正在准备中    后期可在本博客下载

[1]: https://tengine.taobao.org/download_cn.html
[2]: https://tengine.taobao.org/download/tengine-2.3.2.tar.gz
