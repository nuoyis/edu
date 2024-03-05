---
title: 腾讯云服务器折腾2 - 切换成openanolis系统
date: 2023-01-24 12:10:00
categories: 技术类
tags: []
---

>一开始觉得centos8非常好，不想换成Opencloudos,然后想着我阿里云服务器采用的openanolis,腾讯有个什么opencloudos吧，再加上他们传的centos8停止更新服务了,所以就换成国产的系统了。
好家伙，这一换docker直接用不成了，直接熄火,宝塔安装直报错
我用systemctl status docker查看了docker运行状态,**运行了个寂寞，连安装都没安装**
果然yum install docker-ce 安装docker显示 没有找到包名docker-ce
然后我就反馈到宝塔帖子去了(地址:[点击这里][1])
但是我重装后docker不见了又是这种情况，相反我买的阿里云香港轻量云上搭建的openanolis就没问题
然后按照宝塔官方给的建议,先配置源。但我想着配置后再用宝塔安装,好家伙一堆未找到包什么什么的,最后还没安装上
-------openanolis安装方法-------
点击[这里][2]进入openanolis停服专区链接地址查看安装步骤和版本
首先选腾讯云,腾讯云是我的备案后国内使用的云厂商(阿里云备份好重要数据直接点重装openanolis就行了,无需重新制作)
首先也同样备份数据，如果没重要的直接重装成Centos7.6(Centos8被删掉无法重装)
官方给出了两种安装方法
**一.从本地 yum 源安装迁移工具**
**1. 如果待迁移系统无法访问龙蜥mirror或者未连接网络，首先建议在内网搭建一套本地yum源。([如何做本地yum源][3] 用户名： rsync_user ， 密码： Rsync@2020) ，然后通过本地源安装迁移工具。假设本地源地址为 [http://local.repo.com/anolis][4] ， 则下载迁移工具软件源：**
        wget https://mirrors.openanolis.cn/anolis/migration/anolis-migration.repo -O /etc/yum.repos.d/anolis-migration.repo

**2. 然后执行下述命令将 /etc/yum.repos.d/anolis-migration.repo 里面的baseurl地址替换为本地源地址**
        sed -i &quot;s#baseurl=https://mirrors.openanolis.cn/#baseurl=http://local.repo.com/#&quot; /etc/yum.repos.d/anolis-migration.repo
        
        sed -i &quot;s#gpgkey=https://mirrors.openanolis.cn/#gpgkey=http://local.repo.com/#&quot; /etc/yum.repos.d/anolis-migration.repo

**3. 安装迁移工具：**
        yum install -y python-pip
        
        yum remove -y python-requests python-urllib3; /usr/bin/pip2 uninstall requests urllib3 -y 2&gt;/dev/null || echo &quot;not installed&quot;
        
        yum -y install leapp

***注：重新安装 python-requests 和 python-urllib3 是为了解决迁移过程中可能发生的软件包升级冲突。***
**4. 执行下述命令将 /etc/leapp/files/leapp_upgrade_repositories.repo 里面的baseurl地址替换为本地源地址**
        leapp customrepo --seturl http://local.repo.com/&lt;version_number&gt;

**二.从社区 yum 源（mirrors.openanolis.cn) 安装迁移工具**
**1. 如果待迁移系统可以联网且能访问龙蜥mirror，则下载迁移工具软件源：**
        wget https://mirrors.openanolis.cn/anolis/migration/anolis-migration.repo -O /etc/yum.repos.d/anolis-migration.repo

**2. 安装迁移工具：**
        yum install -y python-pip
        
        yum remove -y python-requests python-urllib3; /usr/bin/pip2 uninstall requests urllib3 -y 2&gt;/dev/null || echo &quot;not installed&quot;
        
        yum -y install leapp

再就是系统评估，建议上述操作后使用以下代码将centos源设为.bak文件，以防后续评估出现重复定义现象
错误教训:
        Upgrade has been inhibited due to the following problems:
            1. Inhibitor: A YUM/DNF repository defined multiple times
        Consult the pre-upgrade report for details and possible remediation.

代码:
        cd /etc/yum.repos.d/
        
        ll
        
        mkdir bak
        
        mv CentOS-*.repo ./bak

操作源站更名bak后输入以下指令
        chkconfig cloud-init off
        
        leapp answer --section remove_pam_pkcs11_module_check.confirm=True
        
        sed -i &#039;s/#PermitRootLogin yes/PermitRootLogin yes/&#039; /etc/ssh/sshd_config

开始系统体检，如果出现全绿即可进行下一步
        leapp preupgrade --no-rhsm

***注:上述命令执行成功后，还可以通过/var/log/leapp/leapp-report.txt查看迁移报告，该报告除了包含评估报告外，还包含对目标系统repo的可行性评估，如果目标系统软件包不符合迁移要求，会给出提示。***
出现以下图片即可执行下一步
        leapp upgrade --no-rhsm // ANCK 内核的龙蜥OS
        
        leapp upgrade --no-rhsm --disablerepo=anolis_plus //RHCK 内核的龙蜥OS

至此，你的准备工作已经结束，使用reboot慢慢迁移
迁移完成后你还需要进入腾讯的vpc观看是否重启一次，重启后有个cloud-init一直连接不上，但你又没办法,只能等待3分钟超时后进入。根据官网给的文本,你需要将cloud.cfg修改成腾讯云的
代码如下:
        cp /etc/cloud/cloud.cfg /etc/cloud/cloud.cfg.bak //每次操作需备份
        vim /etc/cloud/cloud.cfg

cloud.cfg内容
        users:
         - default
        
        disable_root: 0
        ssh_pwauth:   1
        
        datasource_list: [ ConfigDrive, TencentCloud ]
        datasource:
          ConfigDrive:
            dsmode: local
          TencentCloud:
            metadata_urls: [&#039;http://169.254.0.23&#039;, &#039;http://metadata.tencentyun.com&#039;]
        
        cloud_init_modules:
         - migrator
         - bootcmd
         - write-files
         - growpart
         - resizefs
         - set_hostname
         - update_hostname
         - [&#039;update_etc_hosts&#039;, &#039;once-per-instance&#039;]
         - rsyslog
         - users-groups
         - ssh
        
        cloud_config_modules:
         - mounts
         - locale
         - set-passwords
         - rh_subscription
         - yum-add-repo
         - package-update-upgrade-install
         - ntp
         - timezone
         - resolv_conf
         - puppet
         - chef
         - salt-minion
         - mcollective
         - disable-ec2-metadata
         - runcmd
        
        unverified_modules: [&#039;resolv_conf&#039;]
        
        cloud_final_modules:
         - rightscale_userdata
         - scripts-per-once
         - scripts-per-boot
         - scripts-per-instance
         - scripts-user
         - ssh-authkey-fingerprints
         - keys-to-console
         - phone-home
         - final-message
         - power-state-change
        
        system_info:
          default_user:
            name: root
            lock_passwd: false
            gecos: Cloud User
            groups: [wheel, adm, systemd-journal]
            sudo: [&quot;ALL=(ALL) NOPASSWD:ALL&quot;]
            shell: /bin/bash
          distro: rhel
          paths:
            cloud_dir: /var/lib/cloud
            templates_dir: /etc/cloud/templates
          ssh_svcname: sshd
        
        # vim:syntax=yaml

替换完后执行以下代码
rm -rf /var/lib/cloud //删除 cloudinit 的缓存记录
reboot //重启
上述代码执行完后进入vnc看看进入速度是否快了许多
至于少了一些东西(例如yum等),可自行询问社区技术人员
对于两大云计算运营商没有一个共同的linux系统(不包括其他非国产操作系统),也就算了，但是软件源腾讯还需努力,很多都是空缺的,也是未完善完毕的。前几天我下了镜像,好家伙Opencloud OS才10个G都没到,Openanolis os超过了15个G,加油两大运营商
文章到这里就结束了，感谢你的观看

[1]: https://www.bt.cn/bbs/thread-107128-1-1.html
[2]: https://openanolis.cn/centos-eol#Background
[3]: https://www.yuque.com/anolis-docs/kbase/gkutwr
[4]: http://local.repo.com/anolis
