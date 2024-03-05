---
title: 腾讯云服务器折腾1 - Opencloudos切换镜像源
date: 2023-01-23 20:26:00
categories: 技术类
tags: []
---

>最近腾讯云的Opencloudos生态经过多次使用镜像源很有些问题，网上有些博客深感其受，如这个博客的博主:[<a href="https://blog.whsir.com/post-6754.html">https://blog.whsir.com/post-6754.html][1]</a>    所以,废话不多说，我们是来换源的.    执行以下代码    vim /etc/yum.repos.d/OpenCloudOS.repo
将上述repo内容删除(建议是备份 cp /etc/yum.repos.d/OpenCloudOS.repo /etc/yum.repos.d/OpenCloudOS.repo.bak)    删掉OpenCloudOS.repo和所有内容,并替换成以下内容    OpenCloudOS.repo        # OpenCloudOS.repo
        #</p>
        #Author: OpenCloudOS &lt;infrastructure@opencloudos.tech&gt;
        #
        [BaseOS]
        name=OpenCloudOS $releasever - Base
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/BaseOS/$basearch/os/][2]
        [http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/$basearch/os/][3]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/BaseOS/$basearch/os/][4]
        gpgcheck=1
        enabled=1
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [AppStream]
        name=OpenCloudOS $releasever - AppStream
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/AppStream/$basearch/os/][5]
        [http://mirrors.tencent.com/opencloudos/$releasever/AppStream/$basearch/os/][6]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/AppStream/$basearch/os/][7]
        gpgcheck=1
        enabled=1
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [Extras]
        name=OpenCloudOS $releasever - Extras
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/Extras/$basearch/os/][8]
        [http://mirrors.tencent.com/opencloudos/$releasever/Extras/$basearch/os/][9]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/Extras/$basearch/os/][10]
        gpgcheck=1
        enabled=1
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [HighAvailability]
        name=OpenCloudOS $releasever - HighAvailability
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/HighAvailability/$basearch/os/][11]
        [http://mirrors.tencent.com/opencloudos/$releasever/HighAvailability/$basearch/os/][12]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/HighAvailability/$basearch/os/][13]
        gpgcheck=1
        enabled=1
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [PowerTools]
        name=OpenCloudOS $releasever - PowerTools
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/PowerTools/$basearch/os/][14]
        [http://mirrors.tencent.com/opencloudos/$releasever/PowerTools/$basearch/os/][15]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/PowerTools/$basearch/os/][16]
        gpgcheck=1
        enabled=1
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [ResilientStorage]
        name=OpenCloudOS $releasever - ResilientStorage
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/ResilientStorage/$basearch/os/][17]
        [http://mirrors.tencent.com/opencloudos/$releasever/ResilientStorage/$basearch/os/][18]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/ResilientStorage/$basearch/os/][19]
        gpgcheck=1
        enabled=1
<p>OpenCloudOS-Sources.repo        # OpenCloudOS-Sources.repo
        #</p>
        #Author: OpenCloudOS &lt;infrastructure@opencloudos.tech&gt;
        #
        [BaseOS-source]
        name=OpenCloudOS $releasever - Base-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/BaseOS/Source/][20]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/BaseOS/Source/][21]
        [http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/Source/][22]
        gpgcheck=1
        enabled=0
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [AppStream-source]
        name=OpenCloudOS $releasever - AppStream-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/AppStream/Source/][23]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/AppStream/Source/][24]
        [http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/Source/][22]
        gpgcheck=1
        enabled=0
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [Extras-source]
        name=OpenCloudOS $releasever - Extras-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/Extras/Source/][26]
        [http://mirrors.tencent.com/opencloudos/$releasever/Extras/Source/][27]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/Extras/Source/][28]
        gpgcheck=1
        enabled=0
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [HighAvailability-source]
        name=OpenCloudOS $releasever - HighAvailability-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/HighAvailability/Source/][29]
        [http://mirrors.tencent.com/opencloudos/$releasever/HighAvailability/Source/][30]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/HighAvailability/Source/][31]
        gpgcheck=1
        enabled=0
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [PowerTools-source]
        name=OpenCloudOS $releasever - PowerTools-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/PowerTools/Source/][32]
        [http://mirrors.tencent.com/opencloudos/$releasever/PowerTools/Source/][33]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/PowerTools/Source/][34]
        gpgcheck=1
        enabled=0
        gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-OpenCloudOS
        [ResilientStorage-source]
        name=OpenCloudOS $releasever - ResilientStorage-source
        baseurl=[http://mirrors.pku.edu.cn/opencloudos/$releasever/ResilientStorage/Source/][35]
        [http://mirrors.tencent.com/opencloudos/$releasever/ResilientStorage/Source/][36]
        [http://mirrors.opencloudos.tech/opencloudos/$releasever/ResilientStorage/Source/][37]
        gpgcheck=1
        enabled=0
<p>OpenCloudOS-Debuginfo.repo可以不修改
继续执行以下代码        yum clean all
        yum makecache
(可选) docker镜像源配置    腾讯云的OpencloudOS现有所有镜像源没有docker-ce(不用想了宝塔安装不上,论坛:[https://www.bt.cn/bbs/thread-107128-1-1.html][38]),如果还有其他没有，请发送至[wkkjonlykang@vip.qq.com][39]，然后在这里添加镜像源    代码如下        yum install -y yum-utils device-mapper-persistent-data lvm2
        
        yum-config-manager --add-repo 
        
        https://download.docker.com/linux/centos/docker-ce.repo
        
        sed -i &#039;s+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+&#039; /etc/yum.repos.d/docker-ce.repo
        
配置好后如果你需要安装,则需要使用以下代码            yum install docker-ce //安装
        
            systemctl start docker //启动
        


[1]: https://blog.whsir.com/post-6754.html
[2]: http://mirrors.pku.edu.cn/opencloudos/$releasever/BaseOS/$basearch/os/
[3]: http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/$basearch/os/
[4]: http://mirrors.opencloudos.tech/opencloudos/$releasever/BaseOS/$basearch/os/
[5]: http://mirrors.pku.edu.cn/opencloudos/$releasever/AppStream/$basearch/os/
[6]: http://mirrors.tencent.com/opencloudos/$releasever/AppStream/$basearch/os/
[7]: http://mirrors.opencloudos.tech/opencloudos/$releasever/AppStream/$basearch/os/
[8]: http://mirrors.pku.edu.cn/opencloudos/$releasever/Extras/$basearch/os/
[9]: http://mirrors.tencent.com/opencloudos/$releasever/Extras/$basearch/os/
[10]: http://mirrors.opencloudos.tech/opencloudos/$releasever/Extras/$basearch/os/
[11]: http://mirrors.pku.edu.cn/opencloudos/$releasever/HighAvailability/$basearch/os/
[12]: http://mirrors.tencent.com/opencloudos/$releasever/HighAvailability/$basearch/os/
[13]: http://mirrors.opencloudos.tech/opencloudos/$releasever/HighAvailability/$basearch/os/
[14]: http://mirrors.pku.edu.cn/opencloudos/$releasever/PowerTools/$basearch/os/
[15]: http://mirrors.tencent.com/opencloudos/$releasever/PowerTools/$basearch/os/
[16]: http://mirrors.opencloudos.tech/opencloudos/$releasever/PowerTools/$basearch/os/
[17]: http://mirrors.pku.edu.cn/opencloudos/$releasever/ResilientStorage/$basearch/os/
[18]: http://mirrors.tencent.com/opencloudos/$releasever/ResilientStorage/$basearch/os/
[19]: http://mirrors.opencloudos.tech/opencloudos/$releasever/ResilientStorage/$basearch/os/
[20]: http://mirrors.pku.edu.cn/opencloudos/$releasever/BaseOS/Source/
[21]: http://mirrors.opencloudos.tech/opencloudos/$releasever/BaseOS/Source/
[22]: http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/Source/
[23]: http://mirrors.pku.edu.cn/opencloudos/$releasever/AppStream/Source/
[24]: http://mirrors.opencloudos.tech/opencloudos/$releasever/AppStream/Source/
[25]: http://mirrors.tencent.com/opencloudos/$releasever/BaseOS/Source/
[26]: http://mirrors.pku.edu.cn/opencloudos/$releasever/Extras/Source/
[27]: http://mirrors.tencent.com/opencloudos/$releasever/Extras/Source/
[28]: http://mirrors.opencloudos.tech/opencloudos/$releasever/Extras/Source/
[29]: http://mirrors.pku.edu.cn/opencloudos/$releasever/HighAvailability/Source/
[30]: http://mirrors.tencent.com/opencloudos/$releasever/HighAvailability/Source/
[31]: http://mirrors.opencloudos.tech/opencloudos/$releasever/HighAvailability/Source/
[32]: http://mirrors.pku.edu.cn/opencloudos/$releasever/PowerTools/Source/
[33]: http://mirrors.tencent.com/opencloudos/$releasever/PowerTools/Source/
[34]: http://mirrors.opencloudos.tech/opencloudos/$releasever/PowerTools/Source/
[35]: http://mirrors.pku.edu.cn/opencloudos/$releasever/ResilientStorage/Source/
[36]: http://mirrors.tencent.com/opencloudos/$releasever/ResilientStorage/Source/
[37]: http://mirrors.opencloudos.tech/opencloudos/$releasever/ResilientStorage/Source/
[38]: https://www.bt.cn/bbs/thread-107128-1-1.html
[39]: mailto:wkkjonlykang@vip.qq.com
