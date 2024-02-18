---
title: JavaScript笔记：初步学习JS
date: 2023-08-12 10:48:00
categories: JavaScript
tags: [JavaScript,BOM,class原型,DOM树]
---
JS是世界上一门最流行的脚本语言，有这样一句话：如果能够重新来过，我一定选择JS。对于一名合格的后端程序员来说，必须要精通JS，而学习vue必不可少的就是JS。
这篇笔记是站在**后端**的基础上快速学习JS所作(IDEA)，后期需要花费一定的成本在深入学习一下(期待我后期的笔记，我已经找到了一套非常优雅的课程，但是恕我没有安排在最近学习)


<!--more-->

[note type="primary flat"]
变量
var a = 1;

number
js不区分小数和整数，统一都用Number表示


```javascript
123 //整数123
123.1 //浮点数123.1
1.123e3 //科学计数法
-99 //负数
Nan //not a number 不是一个数字
Infinity //表示无限大
```


字符串
'abc'  "abc"


比较运算符 (重要)

= 赋值

== 等于(类型不一样，值一样，也会判断为true)

=== 绝对等于(必须要类型一样，值一样，结果为true)
这是一个JS的缺陷，坚持不要使用==比较
须知:
-NaN === NaN ,这个与所有的数值都不相等，包括自己
-只能通过(isNaN) 来判断这个数是否是NaN

浮点数问题:
经量避免使用浮点数进行运算，存在精度问题！
- `console.log((1/3) === (1-2/3))` //false会有精度损失

//true
- `console.log(Math.abs(1 / 3 - (1 - 2 / 3)) < 0.000000001)` 

**null** 和 **undefined**
-null 空
-undefined 未定义

数组
一系列相同类型的对象
//保证代码的可读性，尽量使用[]
 `var arr = [1, 2, 3, 4, 5, 'hello', null, true];` 

 `new Array(1, 2, 3, 46, 'hello', null, true);` 
取数组下标，如果越界了就会undefined

对象
对象是大括号，数组是中括号
每个属性之间使用,隔开，最后一个不需要添加
 
```javascript
var person = {
     name:"zhangsan",
     age:3,
     tags:['js','java','web','...']
 }
```

取对象的值
person.name
**>**'zhangsan'
person.age
**>**3


[/note]


----------
##严格检查模式

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>严格检查模式</title>
    <script>
        /*
        IDEA：需要设置ES6语法
        'use strict';严格检查模式，预防JS的随意性导致产生了问题
        必须写在JavaScript的第一行
        变量建议都是用let定义 ~
        */
        'use strict';

        //不建议使用 var 定义
        /*var i = 1;*/

        //ES6中局部变量用 let定义
        let i = 1;


    </script>
</head>
<body>


</body>
</html>
```


----------
一些笔记(很水的啦，跳过跳过。。。说真的JS真的太随意了，感觉什么都可以。不喜欢QAQ)

[note type="primary flat"]字符串
1.正常字符串我们使用'' "" 包裹
2.注意转义字符 \      \'  \t \n \u \u#### Unicode字符
3.多行字符串编写 ``

"use strict";
/*console.log('a');
console.log("a");
console.log('a\'');*/
4.``(Esc键下面 Tab键上面)模板字符串
var msg1 = `Hello
world
你好啊
你好
`;
let age  = 3;
let name = 'zhangsan';

let msg = `你好啊， ${name}`;

5.字符串长度str.length
6.字符串的可变性，不可变

7.大小写转换
注意，这里是方法，不是属性了student.toUpperCase()

8.student.index('t');
9.substring(1,3)包左不包右



数组
1.var arr = [1,2,3,5,6,7];
长度 arr.length
注意：加入给arr.length赋值，数组大小就可以发生变化，
如果赋值过小，元素就会丢失

2.indexOf 通过元素获取下标索引
字符串的"1"和数字的1 是不同的
3.slice() 截取Array的一部分，返回一个新数组，类似于String 中的subString
4.**push()  ,pop()**
-push 从数组后面压入元素,
-pop 弹出尾部的元素
5.**unshift() ,shift()**
-push 从数组前面压入入元素,
-pop 弹出头部的元素
6.排序sort();

7.元素反转
arr.reverse();

8.**concat()**
注意：concat()并没有修改原先数组，只是会返回一个新的数组

9.连接符join()
打印拼接数组使用特定的字符串连接

10.多维数组

数组：存储数据（如何存，如何取，方法都可以自己实现）[/note]


[note type="default flat"]字符串
1.正常字符串我们使用'' "" 包裹
2.注意转义字符 \      \'  \t \n \u \u#### Unicode字符
3.多行字符串编写 ``

"use strict";
/*console.log('a');
console.log("a");
console.log('a\'');*/
4.``(Esc键下面 Tab键上面)模板字符串
var msg1 = `Hello
world
你好啊
你好
`;
let age  = 3;
let name = 'zhangsan';

let msg = `你好啊， ${name}`;

5.字符串长度str.length
6.字符串的可变性，不可变

7.大小写转换
注意，这里是方法，不是属性了student.toUpperCase()

8.student.index('t');
9.substring(1,3)包左不包右



数组
1.var arr = [1,2,3,5,6,7];
长度 arr.length
注意：加入给arr.length赋值，数组大小就可以发生变化，
如果赋值过小，元素就会丢失

2.indexOf 通过元素获取下标索引
字符串的"1"和数字的1 是不同的
3.slice() 截取Array的一部分，返回一个新数组，类似于String 中的subString
4.push()  ,pop()
-push 从数组后面压入元素,
-pop 弹出尾部的元素
5.unshift() ,shift()头部
-push 从数组前面压入入元素,
-pop 弹出头部的元素
6.排序sort();

7.元素反转
arr.reverse();

8.concat()
注意：concat()并没有修改原先数组，只是会返回一个新的数组

9.连接符join()
打印拼接数组使用特定的字符串连接

10.多维数组



对象
若干个键值对
var 对象名 = {
    属性名：属性值,
    属性名：属性值,
    属性名：属性值,
    属性名：属性值

}

JS中的对象，{...}表示一个对象，键值对描述属性xxxx:xxxx,
多个属性之间使用逗号隔开，最后一个属性不加逗号(,)

JS中的所有的键都是字符串，值是任意对象

1.对象赋值
person.name = "lisi";

2.使用一个不存在的对象属性,不会报错!
> person.haha
< undefined
3.动态的删减属性,通过delete删除对象的属性
> delete person.name;
< true

4.动态的添加，直接给新的属性添加值即可
person.haha = "haha";
> 'haha'
< person
5.判断属性值是否在这个对象中! xxx in xxx!
> "age" in person;
< true
可以通过in找到父类中的方法
>"toString" in person
<true

6.判断一个属性是否是这个对象自身拥有的 hasOwnProperty
> person.hasOwnProperty("toString");
< false
> person.hasOwnProperty("age");
< true

流程控制

判断：
let age  = 3;
if(age > 3){
    alert("haha")
}else {
    alert("kuwa~")
}

循环：
while(age < 100){
    age += 1;
    console.log(age)
}

for循环：
for (let i = 0; i < 100; i++) {
    console.log(i)
}
数组循环：
for (let i = 0; i < age.length; i++) {
    console.log(age[i])
}

console.log("=============================")

//for(var index in object)
for(var num in age){
console.log(age[num])
}

for(var num of age){
console.log(num)
}


age.forEach(function(value){
    console.log(value)
})

Map 和 Set(ES6的新特性)
Map:
let map =  new Map([['tom',100],['jack',98],['haha',80]]);
let name = map.get('tom');//通过key获得value
map.set("admin",123456);
console.log(name);
console.log(map)

Set:无序不重复的集合

let set = new Set([1,1,333,1,333]);
set.add(2);//添加
set.delete(1);//删除一个元素

//判断是否包含某个元素,has
console.log(set.has(333));

[/note]


----------
##JS中的面向对象
面向对象编程,什么是面向对象?
JavaScript有一些区别
-类：模板
-对象：具体的实例
类是对象的抽象，对象是类的具体表现

在JS中，
-原型：模板，可以理解为**父类**。
继承:
 - **class**继承

-**class**关键字，是在ES6引入的


```javascript
class Student{
    //构造器
    constructor(name) {
        this.name = name;
    }

    hello(){
        alert("hello")
    }
}
var zhangsan  = new Student("zhangsan");
var lisi  = new Student("lisi");
zhangsan.hello();
```

源码:

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Class继承</title>

</head>
<body>

<script>

    function Student(name){
        this.name = name;
    }
    //给Student新增一个方法，要么去修改原代码
    //要么得到Student的原型
    /*    Student.prototype.hello = function (){
            alert('Hello');
        }
        */

    //ES6 之后=================================
    //定义一个学生类
    class Student {
        //构造器
        constructor(name) {
            this.name = name;
        }

        hello() {
            alert("hello")
        }
    }

    class pupil extends Student {
        constructor(name, grade) {
            super(name);
            this.grade = grade;
        }

        myGrade() {
            alert("我是一名小学生")
        }


    }


    var zhangsan = new Student("zhangsan");
    var lisi = new pupil("lisi", 1);

</script>


</body>
</html>
```

 - 原型链(自行百度)：

**_proto_**

----------
##操作BOM对象(重点)

 - JS和浏览器的关系：

JS的诞生就是为了能够让它在浏览器中运行！

 - BOM：浏览器对象模型

-浏览器：IE(6-11) Chrome Safari FireFox(Linux默认使用火狐)...
操作BOM 就是操作浏览器对象

 - window对象

window代表 浏览器窗口|全局作用域

```javascript
window.innerHeight
window.innerWidth
window.outerHeight
window.outerWidth
window.alert(1);
```


 - Navigator(浏览器信息)
**Navigator**，封装了浏览器的信息
 `navigator.appVersion` 
![navigator1.png][2]
大多数的时候，我们不会使用 [label color="blue"]navigator[/label] 对象，因为会被**人为修改**!
不建议使用这些属性来判断和编写代码

 - screen
代表屏幕尺寸

 - local(重要)
local代表当前页面的url信息，我们会用它实现一些重定向。
![location1.png][1]

```javascript
host:"www.baidu.com"
href:"https://www.baidu.com/"
protocal:"https:"
reload: ƒ reload() //刷新网页
//设置新的地址
location.assign('https://www.kaijavademo.top');
```

 - document(文本内容,DOM会提及)
document代表当前的页面，HTML DOM文档树
 `document.title` 
获取具体的文档树结点，就能动态的删除结点和删除结点，就可以动态修改网页了
 `document.cookie` 获取cookie

劫持cookie原理
在网页中夹杂一个恶意js文件，文件中写入 `document.cookie`,获取到你登录的cookie，然后上传到他的服务器。

服务器端可以设置 cookie:httpOnly

 - history(不建议使用)
hisory代表浏览器的历史记录
```javascript
history.back();
history.forward();
```
----------
##操作DOM对象
DOM:文档对象模型
**核心：整个浏览器网页就是一个DOM树形结构！**

 - 更新：更新DOM结点
 - 遍历：遍历DOM结点
 - 删除：删除一个DOM结点
 - 添加：添加一个新的结点
要操作一个DOM结点，就必须要先获得DOM结点
###获得DOM结点

```javascript
    //对应CSS的选择器
    var h1 = document.getElementsByTagName('h1');//通过标签获取节点
    var p1 = document.getElementById('p1');//通过id获取节点
    var p2 = document.getElementsByClassName('p2'); //通过class获取节点
    var father = document.getElementById('father');
    
    var child = father.children; //获取父节点下的所有子节点
    //father.firstChild
    //father.lastChild
    

```
这是原生代码之后我们经量使用jQuery。

###更新DOM结点
 `id1.innerText=  '456';` 修改文本的值
 `id1.innerHTML='<strong>123</strong>'` 可以解析HTML文本标签
操作JS
 `id1.style.color = 'red';//属性使用 字符串 包裹` 
 `id1.style.fontSize='20px';//驼峰命名问题` 
 `id1.style.padding = '2em';` 
###删除DOM结点
 - 先获取父节点，再通过父节点删除自己

注意：删除多个结点的时候，children是在时刻变化的，删除节点的时候一定要注意。


```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>删除DOM节点</title>
</head>
<body>
<div id="father">
    <h1>标题一</h1>
    <p id="p1">p1</p>
    <p class="p2">p2</p>
</div>
<script>
    var self = document.getElementById('p1');
    var father = p1.parentElement;
    father.removeChild(self);

    //删除是一个动态的过程，请看注意
    /*father.removeChild(father.children[0])
    father.removeChild(father.children[1])
    father.removeChild(father.children[2])*/

</script>

</body>
</html>
```
###创建和插入DOM节点
我们获得了某个DOM节点，假设整个DOM节点是空的，我们通过innerHTML就可以增加一个元素了，但是这个DOM节点已经存在元素了，我们就不能这么干了，会产生覆盖。

 - 追加操作append
####对于已存在的节点

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>插入DOM节点</title>


</head>
<body>

<p id="js">JavaScript</p>

<div id="list">
    <p id="se">JavaSE</p>
    <p id="ee">JavaEE</p>
    <p id="me">JavaME</p>
</div>

<script>
    var js = document.getElementById('js');
    var list = document.getElementById('list');
    list.appendChild(js);

</script>


</body>
</html>
```
####通过js创建一个标签实现插入


```javascript
    var js = document.getElementById('js');
    var list = document.getElementById('list');
    //通过js创建一个新的节点
    var newP = document.createElement('p');//创建一个p标签，标签里没有任何东西
    newP.id = 'newP';//给标签设置属性id   -->     <p id="newP"></p>
    //newP.setAttribute('id','newP');   和上面的操作等效
    newP.innerText = 'Hello,AlfonsoKevin';//给标签中创建文字，这样就给p标签创建出来了

    //添加标签
    list.appendChild(newP);
    
    
    //创建一个script标签 (通过这个属性可以设置任意的值)
    var myScript = document.createElement('script');
    myScript.setAttribute('type','text/javascript')
```


 - insert

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>插入DOM节点</title>
    <link rel="stylesheet" href="" type="text/css">
    <script type="text/javascript" src=""></script>

</head>
<body>

<p id="js">JavaScript</p>


<div id="list">
    <p id="se">JavaSE</p>
    <p id="ee">JavaEE</p>
    <p id="me">JavaME</p>
</div>

<script>
    var ee = document.getElementById('ee');
    var js = document.getElementById('js');
    var list = document.getElementById('list');
    //要包含的节点 insertBefore(newNode,targetNode)
    list.insertBefore(js,ee);//获取父节点/节点 将js节点插入到ee前面

</script>


</body>
</html>
```

----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/08/690699189.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/13219267.png