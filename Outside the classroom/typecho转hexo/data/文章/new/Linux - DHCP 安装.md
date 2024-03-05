---
title: Linux - DHCP 安装
date: 2023-07-18 10:10:11
categories: uncategorized
tags: []
---
命令代码行  
/／编辑网卡文件  
 vi etc / sysconfig / network - scripts / ifcfg -ens33  
/／添加或更改以下内容： 
```shell
IPADDR =192.168.222.137＃本机 IP 地址  
NETMASK =255.255.255.0＃子网掩码  
GATEWAY =192.168.222.2＃默认网关  
BOOTPROTO = static /／设置IP为静态IP  
```
// 启用网络服务
```shell
sistenctl start network 
```
/／查看 IP 
```shell
ifonfig 
```
/／临时关闭防火墙、 SELinux  
iptables -f #临时关闭防火墙
setenforce o #临时关闭SELinux

//安装DHCP
yum -y install dhcp
mount /dev/src/mnt
cd /etc/yum.repos.d
mv Centos-Base.repo Centos-Base-repo.bak

//修改配置文件
locate dhcpd.conf (没有则用yum安装 yum -y install mlocate)

vi /etc/dhcp/dhcpd/conf
cp /usr/share/doc/dhcp*/dhcp.conf.example /etc/dhcp/dhcpd.conf

systemctl dhcpd
