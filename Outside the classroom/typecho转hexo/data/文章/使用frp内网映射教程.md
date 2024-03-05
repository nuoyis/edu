---
title: 使用frp内网映射教程
date: 2023-08-08 12:18:00
categories: 技术类
tags: []
---
之前写过一篇，目前可能有部分丢失，现在重新写了一份。
frp是内网或者超大内网内的数据与资源映射到公网的一款软件，我们用它来完成家庭内部局域网的访问/网站搭建，目前能做到稳定内网映射的是下面三家

>openfrp地址:https://openfrp.net
>SAKURA FRP地址:https://www.natfrp.com
>花生壳地址:https://hsk.oray.com

花生壳虽然较坑，域名得转入花生壳，还得忍受只有80端口的样子，流量就1到2g。
樱花frp听过没正式使用过，和我现用openfrp差不多的样子。
openfrp目前我觉得免费速度可以的是30 # 香港-5「CN2」 31 # 香港-6「CN2」,在可用不足前这两个可以做到国内一片绿。
付费就无脑选1和2就行了，速度和免费方面感觉没啥差别。

下面正式搭建
frps(服务器方面)
首先服务端下载frp的压缩包，如果你是linux 64位不是arm就选那个amd64，反之选386
下载地址:https://github.com/fatedier/frp/releases
下载好后解压命令(记得文件夹内解压):
```shell
mkdir /usr/local/frp
cd /usr/local/frp && tar -xzvf frp_0.51.2_linux_amd64.tar.gz
```
修改frps.ini为以下内容
```shell
[common]
bind_port = 你的端口
dashboard_port = 7500 //管理端口
dashboard_user = username //管理面板用户名
dashboard_pwd = password //管理面板密码

token = token //对接token
tcp_mux = true

log_file = /usr/local/frp/frps.log //日志
log_level = info
log_max_days = 3
```
frpc(客户端方面)
```shell
[common]
server_addr = 你的地址
server_port = 你的端口
token = nuosawea
log_file = /usr/local/frp/frps.log
log_level = info
log_max_days = 3

[webside]
type = tcp
local_ip = 127.0.0.1
local_port = 80
remote_port = 80

[webside_https]
type = tcp
local_ip = 127.0.0.1
local_port = 443
remote_port = 443

[bt]
type = tcp
local_ip = 127.0.0.1
local_port = 1024
remote_port = 1024
```

[note type="warning flat"]映射的时候一定注意做好防护，对于站点的管理界面一定是采用内网管理方案，域名可以解析个内网ip[/note]