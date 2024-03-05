---
title: LInux - Centos服务器搭建(网络配置)
date: 2023-07-18 10:28:17
categories: 技术类
tags: []
---
Centos下载地址:https://pan.nuoyis.com  

指令和部分地区解释
IPADDR 地址
NETMASK 子网掩码
GATEWAY 网关
DNS、DNSI 公共DNS解析
yum 一次性下载PRM自动安装
Systemctl restart NetworkManger 使配置生效
nmcli c reload 重启网卡
nmcli c up end33 启用ens33网卡
nmcli networking off 关闭网络
nmcli networking on 开启网络
nmcli device now 显示网络的详细情况

操作
/*如果在Windows环境上使用VMware Workstation，请先进入->点击新建虚拟机->自定义->下一步->安装程序镜像文件再进入输密码阶段*/
cd /etc
cd sysconfig/
cd net-work-scripts/
ls
vim ifcfg-nes33
/*增加以下内容

IPADDR = 192.168.*.*(例如：192.168.1.5)
NETMASK = 255.255.255.0
GATEWAY = 192.168.*.1
DNS1 = 8.8.8.8

//esc键后输入wq退出
(nmcli c up ens33) nmcli c reload ens33 ifconfig

//ping测试下
ping baidu.com

