---
title: 思科交换机模拟器配置vlan互通
date: 2021-11-30 09:48:21
categories: 教程类
tags: []
---

>Cisco Packet Tracer（思科模拟器)配交换机指令

en

config //配置

int vlan 1 //创建一个vlan1

ip add 10.0.10.1 255.255.255.0 //创建vlan1的地址范围

no shutdown //不要关机(重启)

exit //退出

int vlan 2 //创建一个vlan2

ip add 10.0.20.1 255.255.255.0 //创建vlan2的地址范围

no shutdown //不要关机(重启)

exit //退出

int vlan 3 //创建一个vlan3

ip add 10.0.30.1 255.255.255.0 //创建vlan3的地址范围

no shutdown //不要关机(重启)

exit //退出

interface fastethernet 0/2 //进入接口类型为fastethernet，0号槽口中2号端口的配置状态

switch mode access //强制接口成为access接口，并且可以与对方主动进行协商，诱使对方成为access模式

switch access vlan 2  //绑定vlan2为2号口


