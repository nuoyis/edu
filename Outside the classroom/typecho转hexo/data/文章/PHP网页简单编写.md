---
title: PHP网页简单编写
date: 2021-12-04 21:52:19
categories: 教程类
tags: []
---

>
php是指超文本预处理器，是在服务器执行的脚本语言。其语言的风格类似于C++和Java。

先尝试输出一个hallo world

```

<?php
echo"hallo world";
?>
```

或者这样输出

```
<pre class="wp-block-code">
<?php
$weikang = "hello world";
echo $weikang;
?>
```

在html镶嵌是这样

```
<pre class="wp-block-code">```
<?php
$weikang1 = "hello world";
?>

 <html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title><?php echo $weikang1; ?></title>
</head>
<body>
<p><?php echo $weikang1; ?>
</body>
</html>
```

或者是这样

```
```
<?php
$weikang1 = "hello world";
?>

 <html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<title><?=$weikang1; ?></title>
</head>
<body>
<p><?=$weikang1; ?>
</body>
</html>
```

php if结构

```
<pre class="wp-block-code">
<?php
$weikang = 1;
if (weikang==1){
echo "hallo world";
}else{
echo "bye world";
}
?>
```

php函数编写

```
<pre class="wp-block-code">
输出hallo world代码
<?php
function weikang(){
echo "hello world";
}
weikang();
?>

输出带数值版
<?php
function weikang($about){
echo $about;
}
weikang(1);
?>
```

php面向对象编写

面向函数是把问题进行抽象化

```
<pre class="wp-block-code">
<?php
class weikangnb{
public function _construct(){
echo "hallo world";
}
}
new weikangnb();
```

本片文章到此为止，有问题或者其他需要补充请联系我哦
