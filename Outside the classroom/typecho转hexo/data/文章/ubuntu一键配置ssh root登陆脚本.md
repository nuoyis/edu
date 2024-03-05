---
title: ubuntu一键配置ssh root登陆脚本
date: 2023-08-09 13:17:32
categories: 技术类
tags: []
---
这几天实在是没有什么灵感，不如来淦我的服务器吧。
我发现ubuntu一开始注册账户，或者使用账户，都类似管理员级别的账号，不进入到root就不能安装各种需要root的应用
宝塔就是这样，每次点击docker终端都会提示权限不足。每次进入ssh都要su root.为了解决以上困扰，我写了个小脚本
脚本如下:
```shell
#!/bin/bash
clear
echo "欢迎使用ubuntu切换root登陆程序"
echo "博客:<a href="<a href="<a href="https://www.nuoyis.net"""" title="https://www.nuoyis.net"""">https://www.nuoyis.net"""</a> title="<a href="https://www.nuoyis.net""">https://www.nuoyis.net""" title="https://www.nuoyis.net""">https://www.nuoyis.net""">https://www.nuoyis.net""">https://www.nuoyis.net""</a></a> title="<a href="<a href="https://www.nuoyis.net"">https://www.nuoyis.net""" title="https://www.nuoyis.net"">https://www.nuoyis.net""">https://www.nuoyis.net"">https://www.nuoyis.net""</a> title="<a href="https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"" title="https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"">https://www.nuoyis.net"</a></a></a>
if [ "$(whoami)" != "root" ]; then
echo -e "\033[31m 未切换root用户模式 \033[0m"
echo -e "\033[34m 如果是第一次请先执行sudo passwd root ，然后执行su root\033[0m"
else
echo "开始执行，执行完成出现一个done"
cd /etc/ssh
echo "PermitRootLogin yes" >> sshd_config
echo "PermitEmptyPasswords no" >> sshd_config
echo -e "\033[32m done \033[0m"
systemctl restart ssh
fi
```
网上去查了下，就两行代码添加到里面去就可以了，然后重启ssh就可以做到了。
这里也插入个直接运行脚本的方法
```shell
 wget --no-check-certificate -O rootstart.sh https://static.nuoyis.com/lib/sh/rootstart.sh && bash rootstart.sh
```
重启连接的ssh，再尝试使用root直接登陆
宝塔内置修改方法(如下图)
![{2EFEE706-0711-4bfb-8435-D532C060C00C}.png][1]
![{BD8D923B-651D-4126-B847-41B19E33C0CE}.png][2]
![{8E45140E-D916-4fd2-A908-375F75CFA976}.png][3]


  [1]: https://io.nuoyis.net/typecho/uploads/2023/08/4154087682.png
  [2]: https://io.nuoyis.net/typecho/uploads/2023/08/902665671.png
  [3]: https://io.nuoyis.net/typecho/uploads/2023/08/2796809723.png