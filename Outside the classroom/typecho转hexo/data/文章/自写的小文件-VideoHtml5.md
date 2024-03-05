---
title: 自写的小文件-VideoHtml5
date: 2023-01-14 16:14:00
categories: 技术类
tags: []
---

>好久没更新了，在新年的前夕我翻了翻那乱葬的备份文件
本来应该在大半年前发出来的，几次网站搬迁和静态资源移动和修复一系列问题搬没了
现在开了自动备份问题还好些
VideoHtml5本来是属于api开发调用的内容，通过iframe进行调用。
如哔哩哔哩在网页插入的那个窗口那样。
如果你把哔哩哔哩的iframe解开，就发现他们是全屏写的 我想起来刚开始写是小窗口小窗口写的，然后全屏和取消全屏就造成位置对不齐。后来改成网页全屏就没有这个问题
目前对于想开发自己的个性化播放器的可以进入我开源的源码
开源地址1:[https://gitee.com/nuoyis/VideoHtml5][1]
开源地址2:[https://github.com/nuoyis/VideoHtml5][2]
对于手机的全屏我试了试，不知道如何翻转全屏，如果会写的请在开源中改入你的代码(不推荐在gitee更改易覆盖)
调用测试:</p>

<iframe src="https://api.nuoyis.net/yu-api/videoplayer/?url=https://vod-yq-aliyun.taobao.com/vod-7651a3/78664950b5e04f8789ab1105585ac553/234150b2e7d44baf89e531b96e26c0b7-209d247f8fc4f3ba2c61b3e343bfaf8f-ld.mp4" framespacing＝"0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" oallowfullscreen="true" msallowfullscreen="true"> </iframe>

代码调用方式:

<pre data-language=HTML>`&lt;iframe src="https://api.nuoyis.net/yu-api/videoplayer/?url=https://vod-yq-aliyun.taobao.com/vod-7651a3/78664950b5e04f8789ab1105585ac553/234150b2e7d44baf89e531b96e26c0b7-209d247f8fc4f3ba2c61b3e343bfaf8f-ld.mp4" framespacing＝"0" allowfullscreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" oallowfullscreen="true" msallowfullscreen="true"&gt; &lt;/iframe&gt;
`</pre>

保留版权可以修改你想做的任何事情,遵循GNU General Public License v3.0协议

[1]: https://gitee.com/nuoyis/VideoHtml5
[2]: https://github.com/nuoyis/VideoHtml5
