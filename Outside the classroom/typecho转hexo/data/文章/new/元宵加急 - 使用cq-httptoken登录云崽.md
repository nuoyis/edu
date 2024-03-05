---
title: 元宵加急 - 使用cq-httptoken登录云崽
date: 2023-02-05 14:35:00
categories: guing
tags: []
---

>资源下载地址:[https://caiyun.139.com/m/i?135Ce8H2tpZTS](https://caiyun.139.com/m/i?135Ce8H2tpZTS) 
提取码:qHeX 
最近发的那个视频没有说明清楚如何下载和云崽登陆异常的解决方案,文字叙述下 
你需要在云盘内下载go-cqhttp和云崽资源包内的token转换器 
建议开始前,创建个文件夹,把两个exe文件放置到本地电脑上 
![cq-http和token转换器](https://images.nuoyis.net/blog/typecho/uploads/202302051429/1.jpg "cq-http和token转换器") 
下一步,运行cq-http,要求运行bat生成成功后即走下一步 
![界面](https://images.nuoyis.net/blog/typecho/uploads/202302051429/2.jpg "界面") 
双击bat，选择3,生成config.yml后关闭窗口 
![生成config.yml](https://images.nuoyis.net/blog/typecho/uploads/202302051429/3.jpg "生成config.yml") 
第四步,在config.yml中account下找到uin然后改成你的QQ号(直接扫码获取token) 
第五步,运行bat文件,生成虚拟设备后按ctrl+c 
![ctrl+c取消](https://images.nuoyis.net/blog/typecho/uploads/202302051429/4.jpg "ctrl+c取消") 
第六步,修改 protocol 字段,修改成你想要的设备(安卓手机为1) 
设备获取链接:[](https://docs.go-cqhttp.org/guide/config.html#%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF)[https://docs.go-cqhttp.org/guide/config.html#%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF](https://docs.go-cqhttp.org/guide/config.html#%E8%AE%BE%E5%A4%87%E4%BF%A1%E6%81%AF) 
![设备修改](https://images.nuoyis.net/blog/typecho/uploads/202302051429/5.jpg "设备修改") 
第七步,重新运行bat，然后等待扫码,扫码登录成功后,生成session.token 
![session.token生成](https://images.nuoyis.net/blog/typecho/uploads/202302051429/6.jpg "session.token生成") 
第八步,将session.token与转换器放在同一目录,双击exe生成token 
![token生成](https://images.nuoyis.net/blog/typecho/uploads/202302051429/7.jpg "token生成") 
第九步,将cq-http的device.json改名为device-QQ号.json 
第十步,将生成的token和放置在yunzai-bot/yunzai/data/QQ号/device-QQ号.json 相同的文件夹内 
![放置wen](https://images.nuoyis.net/blog/typecho/uploads/202302051429/8.jpg "放置wen") 
第十一步,node app重新启动试试,本地能登陆,云端就能使用 
---------视频教程--------- 
[#BV#](https://www.bilibili.com/video/BV1t24y1z7Wp?p=2)
