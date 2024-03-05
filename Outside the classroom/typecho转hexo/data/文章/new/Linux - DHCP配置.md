---
title: Linux - DHCP配置
date: 2023-07-18 10:18:40
categories: uncategorized
tags: []
---
参数列表
```shell
subnet #分配IP地址网段
netmask #子网掩码
range #分配IP地址范围
option routers #client广播地址
option broad-address #client广播地址
default-lease-time #默认租约时间，单位为秒
max-lease-time #最大租约时间
```
设置实例
```shell
#A slightly different configuration for an internd subnet
subnet 192.168.222.0 netmask 255.255.255.0{
range 192.168.222.30 192.168.222.40;
option domain-name-servers nsl.internal.example.org;
option domain-name "internal.example.org";
option routers 192.168.222.255;
option broad-address 192.168.222.255;
default-lease-time 1200;
max-lease-time 360000;
}
```