---
title: 随身WIFI折腾 - 改造成宝塔小主机
date: 2023-07-16 18:38:51
categories: 技术类
tags: []
---
首先先上个配置截图和购买截图
![d71cc89861c78483bd8eaacf5050c0df.png][1]
![Screenshot_20230717_024342_com.taobao.taobao.jpg][2]

# 下面大部分图片或者文章内容由B站大佬[千牛不是牛][3]和QQ好友分享的[酷安大佬][4]，我将两者文章和我的经历融合了一下

首先确定你手里的棒子是高通的CPU，此方法安装的是纯净版，安装好后4G内存的棒子还剩2.4G,不像别人做好的刷机包，他里面安装了很多东西，有些我们根本用不到，对于棒子内存小来说就是浪费资源。

## 第一、准备软件
> - 9008免签名驱动
> - MiKo (备份固件，以免成砖块)
> - 随身WiFi助手
> - Debian刷机包

这四个必须提前安装，并安装至同一目录下便于管理

## 第二、下载Debian固件包
找你主板上等桶型号的固件包，如我的固件为UFI103S_v2,找UFI001C(都适配)的包，然后下载

## 第三、备份固件
用miko进行备份,miko安装有个破解包,记得直接替换(鼠标右键图标跳转文件位置后复制名称删掉),然后拆下随身WiFi的外壳，按住随身WiFi的reset键并插入USB口，然后到设备管理器看是否是9008端口。然后点击read->Paetition Backup/Erase,点击Load Partition Structure。选个地址进行保存。

## 第四、解压整理包
将下载好的整理包解压，然后可以放置一边。

## 第五、刷机
备份好之后把棒子拔下来，重新插上。
一.打开ADB
鼠标右键随身WiFi助手
(如果打开power shell显示adb有问题,确保有adb.exe下可以直接使用./adb xxxxxx)
输入一下指令:
查看设备
```shell
./adb devices
```
如果下面多了一行则执行进入fastboot模式
```shell
./adb reboot bootloader
```
二.打开随身WiFi刷机助手
进入fastboot模式，打开随身wifi助手，输入K
![202304272230381.png][5]

先刷base包：进入base目录，点击flash.bat
再刷debian包：进入固件包目录，点击flash.bat，并一顺回车。
刷机完成后，把棒子拔下来，重新插拔(如果刷机失败,请使用miko->Flash->emmc block0 flasher恢复)。

## 第五、设置驱动和网络共享
查看设备管理器中是否有NDIS，如果有直接跳过后面的操作，进入下面。
![202304281110735.png][6]
![202304281110577.png][7]
---
这里会有一个驱动异常的rndis设备，右键，选择更新驱动，浏览我的电脑，以查找驱动程序
![202304281119967.png][8]
![202304281121286.png][9]
![202304281121364.png][10]
![202304281121236.png][11]
![202304281122596.png][12]
找到Microsoft，然后选择基于RNDIS网络共享设备（不同的系统可能不一样，但大同小异）。
![202304281122177.png][13]

如果任务管理器是ADB模式，则需要按以下步骤操作:
1.卸载该驱动

安装完驱动设备就可以被正常识别了，然后打开ssh（xshell、WindTerm等等都可以）。

## 第七、设置root账户

```bash
#配置root用户密码 123456
sudo passwd root

#切换到root用户
sudo su -

#允许root用户远程登录，重启服务或系统后生效 
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

#重启设备
reboot

#用root设备登录ssh(密码是刚才设置的123456)
root---123456

#删掉已经没用的自带用户
userdel -r user
```

## 第八、连接网络

在终端输入`nmtui`，点击`Activate a connection`
![202304272242452.png][14]
如果你下面这个不是显示的WiFi，你需要退出并进入Edit a connection然后在bridge里面删掉带有WiFi的然后点击保存再退出，回来就行下面界面
![202304272243459.png][15]
![202304272245861.png][16]
在wifi名称前面带有*，就表示连接成功了。
![202304272246098.png][17]

## 第九、安装软件+设定镜像源

### a安装系统常用软件

```bash
#创建一个空mobian.list文件：
true > /etc/apt/sources.list.d/mobian.list

#更新APT软件包：
apt-get update


#安装常用的软件包
apt-get install curl
apt-get install -y wget
apt update
apt install vim git cron dnsutils unzip lrzsz fdisk gdisk exfat-fuse exfat-utils
```

### b设定阿里镜像源

```bash
#打开/etc/apt/sources.list文件
sudo vim /etc/apt/sources.list


#粘贴以下内容
deb https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src https://mirrors.aliyun.com/debian-security/ bullseye-security main
deb https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src https://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
```

### 设定镜像后再次更新APT软件包

```shell
# 该命令会更新本地的软件包列表，会连接到远程软件源并检查可用的更新。
sudo apt update

# 这个命令会下载并安装系统中已经安装的软件包的最新版本，如果有新的依赖项则也会一并下载安装。
sudo apt-get upgrade
```

## 第十、配置系统时间

`dpkg-reconfigure tzdata` 选6.然后选70（亚洲 上海）
![202304272307023.png][18]

## 第十一、把Debian 设置中文环境

```shell
要支持区域设置，首先要安装locales软件包：
apt-get install locales

然后配置locales软件包：
dpkg-reconfigure locales

在界面中钩选487. zh_CN.UTF-8 UTF-8
输入487

然后输入3

#重启设备
reboot
```
![202304272310153.png][19]

设备重启后，再输入nmtui，就可以看到中文界面了：
![202304272313849.png][20]

宝塔安装只需要输入以下指令，安装非常非常的慢
```shell
if [ -f /usr/bin/curl ];then curl -sSO https://download.bt.cn/install/install_panel.sh;else wget -O install_panel.sh https://download.bt.cn/install/install_panel.sh;fi;bash install_panel.sh ed8484bec
```


  [1]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3110921041.png
  [2]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/1286651712.jpg
  [3]: https://www.bilibili.com/video/BV1po4y1t7CY/?spm_id_from=333.999.0.0
  [4]: https://i7z73kxt0i.feishu.cn/docx/doxcnRO4mwUfI0odES7g5PLlNbh
  [5]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3870304197.png
  [6]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3058697286.png
  [7]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3463047828.png
  [8]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/805918896.png
  [9]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/4151593293.png
  [10]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/2212943341.png
  [11]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3407302322.png
  [12]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/1050792005.png
  [13]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/1263337348.png
  [14]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/990396467.png
  [15]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/137603513.png
  [16]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/2737589279.png
  [17]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/2426641172.png
  [18]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/3839553561.png
  [19]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/1687147262.png
  [20]: https://images.nuoyis.net/blog/typecho/uploads/2023/07/4112690753.png