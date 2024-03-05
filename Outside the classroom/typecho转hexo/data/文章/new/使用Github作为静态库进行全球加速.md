---
title: 使用Github作为静态库进行全球加速
date: 2023-09-25 08:00:18
categories: uncategorized
tags: []
---
>前言：自从群内很多群友oss，cos等这些云存储被刷NG或者NT，我就采用了Github作为源站静态库，cloudflare作为海外cdn缓存，如果你没有备案，国内可直接使用[netlify][1]进行国内加速

#配置方法
Github作为源站好处:微软不倒，静态库不倒，如果实在用国内cdn扛不住，用本站cloudflare优选节点死扛到底(当然你的cdn如果能禁海外最好)
本站优选聚合域名:dns-server-cloudflare.nuoyis.net
备案后全球实际访问速度
![static.nuoyis.net_多地区多线路HTTP测速.png][2]
cloudflare加速海外要用到Saas技术，可以查看https://blog.nuoyis.net/1002.html这篇文章
国内采用[netlify][3]进行初次加速，如果备案后可以采用腾讯云edgeone等国内CDN进行基础加速。
打开Netlify官网(可能需要加速器进行加速访问)，点击右上角的Sign up注册账号，这里推荐Github账号注册，注册后进入Netlify的后台页面，点击New site from Git
选择网站源码托管的代码仓库类型，选择GitHub
然后会进入Github的认证授权页面，点击Authorize Netlify by Netlify
点击Only select repositories选择要授权的Github仓库，当然也可以直接选择授权所有仓库，这个授权在设置中可以改
授权完成回到Netlify后台页面，选择我们刚刚授权的Github仓库继续配置自定义域名，自定义域名前一定要解析到分配的这个域名上，等待txt验证完毕以及ssl配置完成，Netlify与Github就算绑定完成，可以通过自定义域名访问网站了。之后你每一次提交代码到Github，都会自动发布至Netlify。
如果国内备案后实在想白嫖，多吉云设置好峰值以及限速，以及CDN缓存和浏览器缓存后就行。每月送20G。即使20G不太够100G一年21元，1T105元
注册地址:[点击这里][4]
缓存配置如下
![屏幕截图 2023-09-25 152849.png][5]
如果你原来静态内容错误，可以只刷新部分文件。当然大调改就需要全部刷新

#注意事项
1.DNS解析必须让cloudflare和netlify检测到，可以先解析cloudflare一条，然后暂停netlify的解析，再都done了后，再反过来操作。
2.国内cdn加速netlify只需要解析到分配的二级域名上即可，带宽非常大，而且无限带宽
3.DNS解析一般国内厂商都有默认和境外解析两种，这里提供我的通配符解析方法
![屏幕截图 2023-09-25 155713.png][6]


  [1]: https://www.netlify.com/
  [2]: https://images.nuoyis.net/blog/typecho/uploads/2023/09/2826680047.png
  [3]: https://www.netlify.com/
  [4]: https://www.dogecloud.com/?iuid=6807
  [5]: https://images.nuoyis.net/blog/typecho/uploads/2023/09/3411112956.png
  [6]: https://images.nuoyis.net/blog/typecho/uploads/2023/09/646736529.png