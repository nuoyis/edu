---
title: Linux - vsftpd 配置
date: 2023-07-15 10:44:00
categories: 技术类
tags: []
---
中文全名：网络文件存储服务器
ftp =＞文件传输协议
TFTP:简单文件传输协议
3种认证方式
匿名 anon
本地 local 
虚拟 guest 
PAM =＞可插拔认证模块
FTP 常用端口
20（数据传输）
21（接受数据）
工作模式：主动模式，被动模式
安装命令
```shell
yum - y install usftpd
```
vsftpd 参数表
```shell
listen =[ YES | NO ]
```
是否以独立运行的方式监听服务
```shell
listen_address =IP地址
```
设置要监听的 IP 地址
```shell
listen_port =21
```
设置 FTP 服务的监听端口
```shell
download_enable =[ YES | NO ]
```
是否允许下载文件
```shell
userlist _ enable =[ YES | NO ]
userlist - deny =[ YES | NO ]
```
设置用户列表为"允许"还是"禁止"操作
```shell
max_clients =0
```
最大客户端连接数，0为不限制
```shell
max_per_ip = o
```
同一 IP 地址的最大连接数，0为不限制
```shell
ancnymous_enable [ YES I NO ]
```
是否允许匿名用户访问
```shell
anon _ upload _ enable =[ YES | No ]
```
是否允许匿名用户上传文件
```shell
anon _ wnask =022
```
匿名用户上传文件的 umark 值
```shell
anon _ root =/var/ftp
```
匿名用户的 FTP 根目录
```shell
 anon _ mkdir _ wribe _ enable =[ YES | NO ]
```
是否允许匿名用户创建目录
```shell
 anon _ other _ write _ enable =[ YES / NO ]
```
是否开放匿名用户的其他写入权限
```shell
 anon - max - rate = 0
```
匿名用户的最大传输速率（字节／秒，0为不限制）
```shell
 local _ enable =[ YES | No ]
```
是否允许本地用户登录 FTP
```shell
local Umask =022
```
本地用户上传文件的 umark 值
```shell
local bot =/ varlftp 
```
本地用户的 FTP 根目录
```shell
chroot _ local _ user =[ YES | No ]
```
是否将用户权限禁锢在 FTP 目录，以确保安全
```shell
local_max_rate = 0
```
本地用户最大传输速率（字节1秒）,0为不限制
程序环境及配置
主程序目录：/usr/sbin/vsftpd
配置文件：/etc/vsftpd/vs/vsftpd.conf 
数据跟目录：/var/ftp 
rpm -9c vsftpd // vsftpd 配置文件
cat / etc / passwork / grep fip /／查看 f 印主机上用户的信息
yum install Iftp ftp /／在同一网络内的另一台主机安装 p
