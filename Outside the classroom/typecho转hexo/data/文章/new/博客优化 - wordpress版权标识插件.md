---
title: 博客优化 - wordpress版权标识插件
date: 2023-02-21 02:22:00
categories: 技术类
tags: []
---

>Hi,正在观看本片文章的同学们，我又开始开干wordpress了奥,wordpress几乎都是在主题上面添加版权标识，万一主题要是更新了那不就覆盖没有了。
于是我就编写了一个小插件，效果如图下所示
![在这里插入图片描述](https://img-blog.csdnimg.cn/60913dd623534002a5e904d80fc71808.png#pic_center)
代码部分借鉴了typecho那边大佬的写法
地址:https://blog.csdn.net/qintaiwu/article/details/120099861
代码如下
```php
<?php
/**
Plugin Name:wordpress版权标识
Plugin slug :nuoyis-copyright

Plugin URI: https://blog.nuoyis.com
Description:在文章中进行版权标识,避免主题更新后恢复
Version: 1.0
Author: 诺依阁
Author URI: https://www.nuoyis.com
*/
function nuoyis_copyright_style(){
    wp_enqueue_style( 'nuoyis_copyright_stylesheets', plugins_url('./copyright.css', __FILE__), array(), '1.0', 'all' );
}

function nuoyis_copyright($content) {
    if(is_single() or is_feed()) {
        $content.= '
        <div class="post-end">
            <span><a style="color:#F17B8F; border-bottom: 0px solid #999!important;">-------------------------此篇文章到此结束-------------------------</a></span>
        </div>
        <ul class="post-copyright">
            <li class="post-copyright-author">**本文作者：**['.get_the_author().'][1]</li>
            <li class="post-copyright-link">**本文链接地址：**<a title="'.get_the_title().'" href="'.get_permalink().'">'.get_permalink().'</a></li>
            <li class="post-copyright-license">**版权声明：**本站所有文章除特别声明外，均采用：<a title="文章协议" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>许可协议。转载请注明来自<a href="./" data-pjax-state="">'.get_bloginfo('name').'</a></li>
        </ul>
        ';
        $content.= "</blockquote>";
    }
    return $content;
}
add_action('wp_enqueue_scripts', 'nuoyis_copyright_style');
add_filter ('the_content', 'nuoyis_copyright');
```
css代码
```css
/*版权信息&正文结束分割线 CSS
本插件css部分和部分html来源如下:
版权声明：本文为CSDN博主「qintaiwu」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qintaiwu/article/details/120099861*/
.post-end {
    border-top: 1px dotted #ccc;
    height: 1px;
    margin: 20px 0;
    text-align: center;
    width: 100%;
}
.cutline span {
    background-color: rgb(236, 237, 238);
    border: 1px solid #d6d6d6;
    font: 12px Arial,Microsoft JhengHei;
    padding: 2px 4px;
    position: relative;
    top: -10px;
}
.post-copyright {
    font-size: 13px;
    margin: 8px 0;
    padding: 10px;
    border-left: 4px solid #ff5252;
    background-color: rgba(220, 220, 220, 0.1);
    list-style: none;
    word-break: break-all;
    position: relative;
    overflow: hidden;
}
.post-copyright li {
    display: list-item;
    text-align: -webkit-match-parent;
}
.post-copyright a {
    color: rgba(0, 120, 231, 1);
    text-decoration: none;
    transition: color .1s;
}
```
代码经过反复修改，大致是没有什么问题的。目前已经上传到gitee上
地址:https://gitee.com/nuoyis/nuowp_copyright

[1]: '.get_author_posts_url(get_the_author_meta( 'ID')).'
