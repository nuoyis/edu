---
title: Miao-Yunzai - 2024年搭建教程
date: 2024-01-03 11:36:00
categories: uncategorized
tags: []
---
docker版本可能不会再出了
我将几位博主的文章进行综合，并完善搭建方法
首先用下面命令安装nodejs
ubuntu/debian
```
curl -fsSL https://deb.nodesource.com/setup_21.x | sudo -E bash -
sudo apt-get install nodejs
```

主要环境安装
```
apt install redis-server git openjdk-17-jre-headless ffmpeg libopencore-amrnb0 libopencore-amrwb0 python3 chromium-browser ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgbm1 libgcc1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils -y
```

克隆Miao-Yunzai以及其他常用插件
```
git clone --depth=1 https://gitee.com/yoimiya-kokomi/Miao-Yunzai.git
cd Miao-Yunzai 
git clone --depth=1 https://gitee.com/yoimiya-kokomi/miao-plugin.git ./plugins/miao-plugin/
git clone --depth=1 https://gitee.com/yeyang52/yenai-plugin.git ./plugins/yenai-plugin
```
指定国内源npmmirror.com安装
```
npm --registry=https://registry.npmmirror.com install pnpm -g
pnpm config set registry https://registry.npmmirror.com
pnpm install -P
```
或者采用cnpm安装
```
npm install cnpm -g
cnpm install -P
```
运行：
```
node app
```
Centos如果乱码采用以下命令
```
yum groupinstall fonts -y
```

45报错: docker安装qsign方式(需获取设备id并修改)
```
docker run -d --restart=always --name qsign -p 8080:8080 -e ANDROID_ID=[设备id] xzhouqd/qsign:8.9.63
```
然后执行如下命令
```
vim config/config/bot.yaml
翻到最底下，改
sign_api_addr: http://127.0.0.1:8080
```
如果浏览器报错请试如下命令:
```
pnpm uninstall puppeteer && pnpm add puppeteer@13.7.0 -w
```

错误处理
禁止登录 237
明天再来

禁止登录 45
需要签名

消息发送失败，可能被风控 -70 -80
先换签名，没用那就下线，明天再来

failed to send: [Group: 群号] undefined(120)
你崽被禁言了

有些来自群友，有些内容来自：[祈杰吖][1]


  [1]: http://qijieya.cn