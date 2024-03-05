---
title: 利用cloudflare搭建二次元随机图片刷新图床
date: 2023-01-18 00:17:00
categories: 教程类
tags: []
---

>之前我的api([https://api.xuvce.com][1])一直都是采用的新浪的随机调用。虽然快吧但不能稳定用。虽然国内云存储付费贵又快，可是我是对外提供，难免会出现有人刷图片问题。
对于图片，我采用的是[https://api.ouyangqiqi.cn][2]贡献的图床，支持webp的图片格式
我同步时候由于将部分png后缀强制转换成了jpg，所以部分图片实际是png(这就影响我后面的图片加水印的api文章的编写)
首先,你得在github上建立一个库或者同步我的也行
我的仓库地址:[https://github.com/nuoyis/imagesbed][3]
创建仓库需要登陆，创建账户仅需一个邮箱。具体请百度下如何操作
找到右上角的加号,点击New repository,随便在Repository name输入库名，再选个自述和通行证(声明)
![创建仓库](https://images.nuoyis.net/blog/typecho/uploads/202301180020/1.png "创建仓库")
![创建仓库](https://images.nuoyis.net/blog/typecho/uploads/202301180020/2.png "创建仓库")
然后点击Create repository开始创建,你就得到了如下的页面中的自述和通行证(声明)
![仓库内容](https://images.nuoyis.net/blog/typecho/uploads/202301180020/3.png "仓库内容")
再可以克隆我的仓库或者下载经过文件夹改名以及文件重整
接着来到cloudflare(登陆页面:[https://dash.cloudflare.com][4])，创建好或者拿着你现有的账号用你现有的域名，点击左上角的添加站点，输入域名，找到最底下的免费，点击继续。DNS如果你有解析，可以按照网盘的dns.txt文件来归整导入
点击继续，修改dns服务器等待生效，就可以进入我们的主要内容了。
主页中点击Pages,点击创建项目，连接到git。
它会叫你授权登陆，可以授权一个库。不会就全部授权。
点击开始设置。接下来框架不选，分支需要看github有内容的那个分支
直接点击保存并部署
然后有个什么后台运行的选项吧，让它在后台慢慢构建
回到Pages，点击你的项目名称,找到自定义域，然后填写你的二级域名(你要一级也可以)
![自定义域名](https://images.nuoyis.net/blog/typecho/uploads/202301180020/4.png "自定义域名")
到此搭建就完成了。
穿插自家内容:
我的API欢迎调用，地址: [https://api.xuvce.com][1] 图片调用越多加载越快哦
再就是自家服务器随机刷新的代码，这里是用PHP编写的随机刷新代码，支持分webp和jpg格式
也可输出json格式
代码:
        &lt;?php
        $server = rand(1,836);
        if(isset($_GET[&#039;yasuo&#039;]) &amp;&amp; $_GET[&#039;yasuo&#039;]==1)
        {
        $url = &#039;https://acgpictures.xuvce.com/img-webp/yupic&#039;.$server.&#039;.webp&#039;;
        }else {
        $url = &#039;https://acgpictures.xuvce.com/img/yupic&#039;.$server.&#039;.jpg&#039;;
        }
        $result=array(&quot;code&quot;=&gt;&quot;200&quot;,&quot;acgurl&quot;=&gt;&quot;$url&quot;);
        $type=$_GET[&#039;type&#039;];
        
        switch ($type)
        {   
        //格式解析                             
        case &#039;json&#039;:
        $path = &quot;$url&quot;;
        $pathinfo = pathinfo($path);
        $imageInfo = getimagesize($url);  
        $result[&#039;size&#039;]=&quot;$pathinfo[extension]&quot;; 
        header(&#039;Content-type:text/json&#039;);
        echo json_encode($result);
        break;
        //不输出图片链接直接显示                             
        case &#039;img&#039;:
        $img = file_get_contents($url,true);
        header(&quot;Content-Type: image/jpeg;&quot;);
        echo $img;
        break;
        //IMG
        default:
        header(&quot;Location:&quot;.$result[&#039;acgurl&#039;]);
        break;
        }
        
        ?&gt;

感谢你的观看，谢谢你的支持

[1]: https://api.xuvce.com
[2]: https://api.ouyangqiqi.cn
[3]: https://github.com/nuoyis/imagesbed
[4]: https://dash.cloudflare.com
[5]: https://api.xuvce.com
