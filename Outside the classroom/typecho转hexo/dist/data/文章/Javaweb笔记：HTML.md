---
title: Javaweb笔记：HTML
date: 2023-07-13 11:12:00
categories: JavaWeb
tags: [HTML,JavaWeb,JavaWeb笔记]
---
Javaweb的学习笔记，Html的基础标签


<!--more-->


```html
<html>
	<head>
		<title>这是我的第一个网页</title>
		<meta charset="UTF-8">
	</head>
	<body>
	<!--	
	 HELLO WORLD!<br/>你好,HTML!
	 <p>这里是一个段落</p>
	 <p>这里是第二个段落</p>
	 <img src="E:\学习\java\javaweb\imgs\girl.jpg" width="192" height="108" alt="这里是一张图片"/>
	 <h1>标题一</h1>
	 <h2>标题一</h2>
	 <h3>标题一</h3>
	 <h4>标题一</h4>
	 <h5>标题一</h5>
	 <h6>标题一</h6>
	 -->
	 武林高手排行榜：
	 <ol type="i" start="3">
		<li>扫地僧</li>
		<li>萧远山</li>
		<li>慕容博</li>
		<li>虚竹</li>
		<li>阿紫</li>
	 </ol>
	 武林大会人员名单：
	 <ul type="circle">
		<li>乔峰</li>
		<li>阿朱</li>
		<li>马夫人</li>
		<li>白世镜</li>
	 </ul>
	 
	 你是<b><i><u>喜欢</u></i></b>是<b>甜</b>月饼还是<i>咸</i><u>月饼</u>?
	 <br/>
	 
	 水分子的化学式：H<sub>2</sub>O<br/>
	 氧气的化学式:O<sup>2</sup><br/>
	 
	 5&lt;10
	 10&gt;5
	 5&le;10
	 10&ge;5
	 
	 注册商标 &reg;
	 版权符号 &copy;
	 
	 <span>赵又廷</span>，夺妻之仇
	 
	 <a href="http://www.baidu.com" target="_self">百度一下</a>
	 
	 
	 
	</body>



</html>
<!--
1)
html语言是解释型语言，不是编译型。
浏览器是容错的，允许错误在里面，尽量展示

2)
html页面中有一对标签组成：<html></html>
<html>称之为 开始标签
</html>称之为 结束标签
3)
title 表示网页的标题
4)
可以在meta标签中设置编码方式
5)
<br/> 表示换行,br 标签是一个单标签 。单标签：开始标签和结束标签是同一个，因此/写在单词后面，表示单标签。
6)
p 表示段落标签 换行之间的间隙 没有段落标签大
7)
img 标签 图片标签
	src 属性表示图片文件的路径
	width和heigh表示图片的大小
	alt表示图片的提示
8)
 路径的问题：
	1.相对路径
	2.绝对路径
9)
h1 ~ h6 标题标签
10)
列表标签
-ol 有序列表
	start 表示从*开始，type 显示的类型：A a I i 1(default)

-ul 无序列表
	type disc(default),circle,square

11) u 下划线 b粗体 i斜体


12)上标sup 下标sub
13)HTML 中的实体：小于号&lt;大于等于号 &ge; 版权 &copy;

14)span 不换行的块标记

15)a表示超链接
	href 链接的地址
	target:
	_self 在本窗口打开
	_blank 在一个新窗口打开
	_parent 在父窗口打开
	_top 在顶层窗口打开
	
16）div 层 


-->

```
![1.png][1]


----------

```html
<html>
	<head>
		<title>这是我的第一个网页</title>
		<meta charset="UTF-8">
		<style type="text/css">
		 div{
			width:200px;
			height:200px;
			position:absolute;
		 }
		 
		 #div1{
			background-color:#AF8;
		 }
		 #div2{
			background-color:#8BC;
			left:100px;
			top:100px;
		 }
		 #div3{
			background-color:#FF8;
			left:200px;
			top:200px;
		 }
		 
		</style>
	</head>
	<body>
		<div id="div1">div1</div>
		<div id="div2">div2</div>
		<div id="div3">div3</div>
	</body>



</html>
<!--
16）div 层 


-->

```
![2.png][2]


<!--more-->
##HTML中的table标签


```html
html>
	<head>
		<title>表格标签的学习</title>
		<meta charset="UTF-8">
		 
		</style>
	</head>
	<body>
		<table border="1" width="600" cellspacing="0" cellpadding="4">
		<tr align="center">
			<th>姓名</th>
			<th>门派</th>
			<th>成名绝技</th>
			<th>内功值</th>
		
		</tr >
		<tr align="center">
		<td>乔峰</td>
		<td>丐帮</td>
		<td>少林长拳</td>
		<td>5000</td>
		</tr>
		
		<tr align="center">
		<td>虚竹</td>
		<td>灵鹫宫</td>
		<td>北冥神功</td>
		<td>15000</td>
		</tr>
		
		<tr align="center">
		<td>扫地僧</td>
		<td>少林寺</td>
		<td>七十二绝技</td>
		<td>未知</td>
		</tr>
		
		
		</table>
		<hr/>
		<table border="1" cellspacing="0" cellpadding="4" width="600">
		<tr align="center">
		<th>名称</th>
		<th>单价</th>
		<th>数量</th>
		<th>小计</th>
		<th>操作</th>
		
		</tr>
		
		<tr align="center">
		<td>苹果</td>
		<td rowspan="2">5</td>
		<td>20</td>
		<td>100</td>
		<td><img src="imgs/delete.jpg" width="24" height="24"/></td>
		</tr>
		
		<tr align="center">
		<td>菠萝</td>

		<td>15</td>
		<td>45</td>
		<td><img src="imgs/delete.jpg" width="24" height="24"/></td>
		</tr>
		
		<tr align="center">
		<td>西瓜</td>
		<td>6</td>
		<td>6</td>
		<td>36</td>
		<td><img src="imgs/delete.jpg" width="24" height="24"/></td>
		</tr>
		
		<tr align="center">
		 <td>总计</td>
		 <td colspan="4">181</td>
		</tr>
		
		</table>
		
	</body>



</html>
<!--
17）表格 table
	行   tr
	列	 td
	表头列 th
	
	table 中有如下属性（虽然以及淘汰，但是最好了解一下）
	-border:表格边框的粗细
	-width:表格的宽度
	-cellspacing:单元格间距
	-cellpadding:单元格填充
	
	tr中一个属性: align->center ,left,right
	
	rowspan：行合并
	colspan: 列合并
	
-->

```

![3.png][3]

<!--more-->
##HTML中的表单标签


```html
<html>
	<head>
		<title>表单标签的学习</title>
		<meta charset="UTF-8">
		 
		</style>
	</head>
	<body>
		<form action="demo04.html" method="post">
			昵称：<input type="text" name="nickName" value="请输入你的昵称"/><br/>
			密码：<input type="password" name="pwd"/><br/>
			性别：<input type="radio" name="gender" value="male"/>男
				  <input type="radio" name="gender" value="female" checked/>女<br/>
			爱好：<input type="checkbox" name="hobby" value="basketball"/>篮球
				   <input type="checkbox" name="hobby" value="football" checked/>足球
				   <input type="checkbox" name="hobby" value="earth" checked/>地球<br/>
			星座：<select name="star">
					<option value="1">白羊座</option>
					<option value="2">金牛座</option>
					<option value="3">双子座</option>
					<option value="4">天秤座</option>
					<option value="5">天蝎座</option>
					<option value="6" selected>巨蟹座</option>
				  </select><br/>
			备注：<textarea name="remark" rows="4" cols="50"></textarea><br/>
			<input type= "submit" value="注 册"/>
			<input type="reset" value="重置"/>
			<input type= "button" value="这是一个普通按钮"/>
		</form>
		
	</body>



</html>
<!--
18）表单 form

19) input type = "text" 表示文本框，其中name属性必须要指定，否则这个文本框的数据将来是不会发送给服务器的
	input type = "password"表示密码框
	input type = "radio"表示单选按钮，需要注意的是，name属性值保持一致，这样才会有互斥的效果；可以通过check属性设置默认选中的项
	input type = "checkbox"表示复选框，name属性值建议保持一致，将来我们服务器端获取值的时候获取的是一个数组
	select 表示下拉列表，每一个选项是option，其中value属性是发送给服务器的值，selected表示默认选中的项
	textarea 表示多行文本框(或者称之为文本域)不要轻易换行，它的value值就是开始结束标签之间的内容
	input type = "submit"表示提交按钮
	input type = "reset"表示重置按钮
	input type = "button"表示普通按钮
	
-->

```

![4.png][4]


```html
<html>
	<head>
		<title>表单标签的学习</title>
		<meta charset="UTF-8">
		 
		</style>
	</head>
	<body>
		<h1><font color='red'>注册成功</font></h1>
		
	</body>

</html>
<!--
18）表单 form

19) input type = "text" 表示文本框，其中name属性必须要指定，否则这个文本框的数据将来是不会发送给服务器的
	input type = "password"表示密码框
	
-->

```

![5.png][5]


<!--more-->

##frameset


```html
<html>
	<head></head>
	<frameset rows="20%,*" ><!-- frameborder="no"-->
		<frame src="frames/top.html"/>
		<frameset cols="15%,*">
			<frame src="frames/left.html"/>
			<frameset rows="80%,*">
				<frame src="frames/main.html"/>
				<frame src="frames/bottom.html"/>
			</frameset>
		</frameset>
	</frameset>
</html>

<!--
frameset 表示页面框架 ，这个标签已经淘汰，了解，不需要掌握
frame表示框架中的具体页面的引用

iframe
-->
```
![6.png][6]

##iframe


```html
<html>
	<head>
		<meta charset="utf-8"> 
	</head>
	<body>
		这里是demo06页面的内容！！
		<iframe src="frame/top.html"/>
		
		
		
	</body>
	
</html>

<!--
frameset 表示页面框架 ，这个标签已经淘汰，了解，不需要掌握
frame表示框架中的具体页面的引用


iframe 在一个页面中嵌入一个子页面


总结：
1.HTML是解释型的标记语言，不区分大小写
2.html，head，titile，meta，body，br，p，hr，div，table，form，u，i，b,sub，sup，&nbsp，span，ul，ol，li，tr，td，th，h1
-h6，img,textarea,input,select,a
2-1.html,head,title,meta,body,br,ul,ol,h1-h6,a,img,&nbsp,p,div,span
2-2 table,tr,th,td,表格标签
2-3 form(action="",method="post") input type=text,password,radio,checkbox,submit,button,reset



-->
```
![7.png][7]


----------


我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/3822629203.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/2175635554.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/1653534462.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/2503423969.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/130942293.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/1832475637.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/3360663992.png