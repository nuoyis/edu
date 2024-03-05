---
title: cloudflare saas接入 - 加速和抵抗海外攻击
date: 2023-08-21 03:15:19
categories: 教程类
tags: []
---
>前情提示:本文章得有备案域名，没有就不要想着默认解析使用国内的了，直接解析我提供的访问还可以的cloudflare
>本文章还得有一个嫖的顶级域名(后续文章)
>海外(或未备案)域名解析地址:dns-server-cloudflare.nuoyis.net

很多人说cloudflare是国内的减速器，但cloudflare可以反过来利用加速海外。cloudflare海外加速几乎都是1-10毫秒，少数像中国这样不支持的达到90-150毫秒。cloudflare大缓存技术可以使静态库在海外无惧攻击，github pages+cloudflare全缓存就是几乎无敌。这留在下一篇文章讲解静态库高速回国办法。
cloudflare缓存后硬抗如下
![屏幕截图 2023-08-21 110327.png][1]
首先，得添加域名，就点击右上角的添加站点->输入顶级域名->下拉选择free->修改DNS为下面->等待完成
```other
delilah.ns.cloudflare.com
lamar.ns.cloudflare.com
```
点击刚刚你添加的域名，先添加你要解析的域名，如 cloudflare 前缀 a解析到127.0.0.1
找到左侧SSL/TLS并展开，找到自定义主机名->添加回退源（如cloudflare.xxxxxxx.xxx) ，添加后将两个txt以及值分别解析到dns中。
境外解析如上域名，就可享受海外急速加速。博客也可以。

然后就是缓存，如果是静态库如下缓存
![2023-08-21T03:14:24.png][2]
博客如下
![2023-08-21T03:14:51.png][3]


  [1]: https://io.nuoyis.net/typecho/uploads/2023/08/1625808904.png
  [2]: https://io.nuoyis.net/typecho/uploads/2023/08/3169904810.png
  [3]: https://io.nuoyis.net/typecho/uploads/2023/08/1402592000.png