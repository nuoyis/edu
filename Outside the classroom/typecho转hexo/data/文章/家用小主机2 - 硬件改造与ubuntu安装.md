---
title: 家用小主机2 - 硬件改造与ubuntu安装
date: 2023-08-11 03:35:40
categories: 教程类
tags: []
---
之前的这个小主机目前网站重新移到云端后，小主机用来内网下载和直播录制以及直播回放。
但是有一个问题，小主机就30g，内存不够做更多这方面的内容。
所以，本期文章就出现了:改造我们小主机的存储内存。
好家伙，小主机的存储接口是msata的，在某宝上搜索，三星300多元的一块就把我吓得劝退。于是我就找到了这家店
![Screenshot_20230811_105039_com.taobao.taobao.jpg][1]
这家可以把msata转sata,让我闲置的廉价且高质量的sata有了用场。
这里采用的是爱国者128G(S500),配件和硬盘截图如下
![IMG_20230809_105313.jpg][2]
![IMG_20230809_105325.jpg][3]
然后首先打开小主机的背板，然后把配件插进去对位，因为线有一根插上去很难拔下来
![IMG_20230809_105528.jpg][4]
对位好后先将线排版好，不遮挡其他主要工作区域，装好后效果图
![IMG_20230809_153944.jpg][5]
上盖，然后u盘装载镜像，去找个显示屏安装
这里由于当时没拍照截图，就用虚拟机展示下对比底下有没有绿色按钮,有就直接点就完事了，没有需要修改
![{00151A3A-7C2B-4dc4-BBAF-725450B48767}.png][6]
![{B33FBE68-0CB7-481b-80B6-3FBE8BFBA395}.png][7]
![{6B12557F-3BFF-4beb-8A10-FF4E750A875A}.png][8]
![{669DF1BF-DD41-4a81-BDF8-091603880E37}.png][9]
![{3D5FBB77-D59C-4905-AF10-EBB490D80EC7}.png][10]
![{02D4136E-D20C-4d5c-AA17-F332D8E71C26}.png][11]
![{57FFDD92-A7F3-42f1-B9F1-482837C4EEB3}.png][12]
![{BBEE3B8E-B2AA-4685-A178-FA9398D1CA55}.png][13]
![{7436B6FF-CFE5-42ad-B8E0-2D6998698D9B}.png][14]
![{61051C63-5238-43f2-99FF-6B8805833631}.png][15]
![{3721B01C-E6E5-41f3-A0A8-314CBE09F78A}.png][16]
![{AA6B45C4-69CD-462f-870C-47A0FDE8CA74}.png][17]
![{EE61EC13-FEE4-481e-9658-169FA51BB786}.png][18]
![{825C3FE1-52C1-4f01-BE58-913FB11296E2}.png][19]
![{825C3FE1-52C1-4f01-BE58-913FB11296E2}.png][20]
![{708DE4DD-E9B9-4d8b-A325-414FC7718138}.png][21]
等待，然后出现reboot那个按钮点击，点击后出现这种情况就需要ctrl+c
![{774B22CA-0416-4550-B6B6-89D77F0D1C74}.png][22]

系统如果没有全部分配完，需要操作以下代码
```shell
sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
```
ubuntu默认不允许root登陆，请查阅以下文章

>https://www.nuoyis.net/969.html


  [1]: https://io.nuoyis.net/typecho/uploads/2023/08/3740030666.jpg
  [2]: https://io.nuoyis.net/typecho/uploads/2023/08/1138999.jpg
  [3]: https://io.nuoyis.net/typecho/uploads/2023/08/2034333085.jpg
  [4]: https://io.nuoyis.net/typecho/uploads/2023/08/2342553711.jpg
  [5]: https://io.nuoyis.net/typecho/uploads/2023/08/2420240448.jpg
  [6]: https://io.nuoyis.net/typecho/uploads/2023/08/2985625782.png
  [7]: https://io.nuoyis.net/typecho/uploads/2023/08/931813565.png
  [8]: https://io.nuoyis.net/typecho/uploads/2023/08/4163279373.png
  [9]: https://io.nuoyis.net/typecho/uploads/2023/08/2010363333.png
  [10]: https://io.nuoyis.net/typecho/uploads/2023/08/877727979.png
  [11]: https://io.nuoyis.net/typecho/uploads/2023/08/53535396.png
  [12]: https://io.nuoyis.net/typecho/uploads/2023/08/1304625918.png
  [13]: https://io.nuoyis.net/typecho/uploads/2023/08/1003239841.png
  [14]: https://io.nuoyis.net/typecho/uploads/2023/08/3209792368.png
  [15]: https://io.nuoyis.net/typecho/uploads/2023/08/496840674.png
  [16]: https://io.nuoyis.net/typecho/uploads/2023/08/3191457542.png
  [17]: https://io.nuoyis.net/typecho/uploads/2023/08/947116754.png
  [18]: https://io.nuoyis.net/typecho/uploads/2023/08/1528954107.png
  [19]: https://io.nuoyis.net/typecho/uploads/2023/08/4127976584.png
  [20]: https://io.nuoyis.net/typecho/uploads/2023/08/3892764151.png
  [21]: https://io.nuoyis.net/typecho/uploads/2023/08/4193026396.png
  [22]: https://io.nuoyis.net/typecho/uploads/2023/08/266839298.png