---
title: 学习测试脚本 死亡ping
date: 2023-11-21 11:05:05
categories: uncategorized
tags: []
---
最近实在是太忙了，还有篇工具箱的文章等着出。目前先把测试感觉良好的死亡ping cmd脚本提供给大家使用。
同时，死亡ping可以测试你真正cpu和内存的承受能力，开到400我的笔记本就差不多有些卡了。
![屏幕截图 2023-11-21 081409.png][1]
代码如下:
```shell
set num=300
for /l %%i in (1,1,%num%) do (
start cmd /k "ping -l 65000 192.168.43.1 -t"
)
pause
```

  [1]: https://io.nuoyis.net/typecho/uploads/2023/11/4193386853.png