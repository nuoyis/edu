---
title: Thymeleaf笔记：视图模板技术-SpringBoot整合Thymeleaf
date: 2023-08-04 12:14:00
categories: Thymeleaf
tags: [Thymeleaf,模板引擎,核心语法]
---
考虑到后面SpringMVC和SpringBoot中需要使用Thymeleaf技术，初步学习，做点笔记。
[Thymeleaf官网帮助文档][1]

<!--more-->
创建maven工程，pom文件中导入Thymeleaf依赖

```xml

    <dependency>
      <groupId>org.thymeleaf</groupId>
      <artifactId>thymeleaf</artifactId>
      <version>3.0.12.RELEASE</version>
    </dependency>

```

```java
public class HelloThymeleaf {
    public static void main(String[] args) {
        //创建模板引擎
        TemplateEngine engine  = new TemplateEngine();

        //准备模板
        //模拟网页表单对象
        String input = "<input type='text' th:value='hellothymeleaf'/>";

        //准备数据，使用context
        Context context = new Context();
        //调用引擎，处理模板和数据
        /*
        engine.process();
        参数一：模板
        参数二：Context对象
        */
        String out = engine.process(input, context);
        System.out.println("结果数据" + out);
    }
}

```
![1.png][2]

可以渲染数据，写成动态的

```java
public class MyTest {
    @Test
    public void test01() {
        //创建模板引擎
        TemplateEngine engine = new TemplateEngine();

        //准备模板,name此时相当于一个占位符，提供数据，模板引擎会提供真实的数据
        String inStr = "<input type='text' th:value='${name}'/>";

        //准备数据
        Context context = new Context();
        //给name标识来指定数据
        context.setVariable("name", "李四");

        //处理模板和数据
        String html = engine.process(inStr, context);
        System.out.println("html = " + html);

    }
}

```
![2.png][3]


----------

使用模板文件

```java
    @Test
    public void test02(){
        TemplateEngine engine = new TemplateEngine();
        //读取磁盘中的模板文件
        ClassLoaderTemplateResolver resolver = new ClassLoaderTemplateResolver();

        //设置引擎使用resolver
        engine.setTemplateResolver(resolver);

        //指定数据
        Context context = new Context();
        context.setVariable("name","张三");

        //处理模板
        String html = engine.process("main.html", context);
        System.out.println("html = " + html);
    }
```
简单写一个main.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  模板:<input type="text" th:value="${name}" />
</body>
</html>
```
读取测试。
![3.png][4]

----------

这样需要指定文件名+后缀的形式，而且位置固定
 `String html = engine.process("main.html", context);` 
如果使用的文件不是在resource类路径文件下，那么还需要指定文件的路径，简化模板文件所在的目录位置和扩展名的处理，使用解析器ClassLoaderTemplateResolver。

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  <input type="text" th:value="${name}">
</body>
</html>
```

```java
    @Test
    public void test03() {
        TemplateEngine engine = new TemplateEngine();
        //创建模板引擎的解析器
        ClassLoaderTemplateResolver resolver = new ClassLoaderTemplateResolver();
        //指定前缀，相对于resources，目录自定义
        resolver.setPrefix("templates/");

        //指定后缀，文件扩展名
        resolver.setSuffix(".html");

        //设置引擎要用到的解析器
        engine.setTemplateResolver(resolver);
        Context context = new Context();
        context.setVariable("name","张三三");

        //路径制定好了，直接写名称就可以了
        String html = engine.process("index", context);
        System.out.println("html = " + html);

    }
```
![4.png][5]

----------
##SpringBoot整合
之前的内容基于MVC使用Thymeleaf，接下来在**SpringBoot中整合Thymeleaf并使用**。
在没有职业前端，不使用前后端分离开发，使用服务端渲染的情况下，需要使用模板引擎。
前后端分离开发，分工明确，协同开发，项目上线速度快。
服务端渲染，少了一次前端交互服务端，项目速度快。
依然是导入pom文件
 
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-thymeleaf</artifactId>
</dependency>
```

 - a. 所有的模板页面在`classpath:/templates/ `下面找
 - b. 找后缀名为`.html`的页面
###初体验
使用thymeleaf，通过get方式传参，在网页中显示对应的文字。

WelcomeController
```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-08 17:43
 * @description: 测试模板引擎Thymeleaf
 **/
@Controller //适配服务端渲染技术，也就是前后端不分离模式，不要使用RestController
public class WelcomeController {

    /**
     * 利用模板引擎跳转到指定页面
     * @param name
     * @param model 同以前MVC，使用Model，把所有要给页面共享的数据放到里面
     * @return
     */
    @GetMapping("/well")
    public String hello(@RequestParam("name") String name, Model model){

        //想要来到welcome.html页面，因为整合的Thymeleaf
        //默认是在类路径resource下的templates 后缀是.html。我们只需要补充上逻辑视图名就可以了
        //模板的逻辑视图地址，最终生成物理视图。物理视图 = 前缀 + 逻辑视图名 + 后缀
        //真实地址= classpath:/templates/welcome.html

        //把需要给页面共享的数据放入model中
        model.addAttribute("msg",name);
        return "welcome";
    }
}

```
效果
![5.png][6]


----------
###基本用法

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>

</head>
<body>
<h1>你好：<span th:text="${msg}"></span></h1>
<hr/>
<!-- th: text 替换标签体的内容；会转义 -->
<!-- th: utext 替换标签体的内容；不会转义html标签，真正显示成html该有的样式 -->
<h1 th:text="${msg}">哈哈</h1>
<h1 th:utext="${msg}">呵呵</h1>

<hr/>
<!--th:任意html属性：动态替换为任意属性的值-->
<!--改为动态传递图片-->
<img th:src="${imgUrl}" src="1.png" style="width:300px;"/>
<br/>
<!--th:attr:任意属性指定，所有属性都可以在attr中任意取值.我们可以将想要的东西放到域共享数据中，通过指定格式取值-->
<img th:src="${imgUrl}" src="2.png" style="width:300px;" th:attr="src=${imgUrl},style=${style}"/>
<br/>
<!--th:其他指令 th:if 要不要显示 取出表达式，如果为true就显示，如果为false就不会显示-->
<img th:src="${imgUrl}" th:style="${style}" th:if="${show}">

</body>
</html>
```
HelloController

```java
package com.atguigu.web.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * @author: TangZhiKai
 * @create: 2023-10-08 17:43
 * @description: 测试模板引擎Thymeleaf
 **/
@Controller //适配服务端渲染技术，也就是前后端不分离模式，不要使用RestController
public class WelcomeController {


    /**
     * 利用模板引擎跳转到指定页面
     * @param name
     * @param model 同以前MVC，使用Model，把所有要给页面共享的数据放到里面
     * @return
     */
    @GetMapping("/well")
    public String hello(@RequestParam("name") String name, Model model){

        //想要来到welcome.html页面，因为整合的Thymeleaf
        //默认是在类路径resource下的templates 后缀是.html。我们只需要补充上逻辑视图名就可以了
        //模板的逻辑视图地址，最终生成物理视图。物理视图 = 前缀 + 逻辑视图名 + 后缀
        //真实地址= classpath:/templates/welcome.html

        //把需要给页面共享的数据放入model中
        String text = "<span style='color:red'>"+name+"</span>";
        model.addAttribute("msg",text);

        //路径是动态的
        model.addAttribute("imgUrl","/1.png");
        //数据库查出的样式
        model.addAttribute("style","width:400px");

        model.addAttribute("show",false);
        return "welcome";
    }
}

```
###表达式取值

 - `${}`:变量取值;使用**model共享给页面的值**都直接用**${}**
 - `@{}`:url路径

```html
<!--以后@{}专门用来取各种路径
@{${imgUrl}} 解释：先去${}model里面取出imgUrl，然后被@{}封装，自动加/不加 项目的路径这样会非常安全-->
<img src="/static/girl.png" style="width:300px;" th:src="@{/static/girl.png}">
```
 - `#{}`:国际化消息
 - `~{}`:片段引用
 - `*{}`:变量选择：需要配合`th:object`绑定对象

----------
###遍历
**语法：** `th:each="元素名,迭代状态 : ${集合}"` 

 [label color="blue"]WelcomeController[/label] 

```java
    /**
     * 这里我创建一个集合通过thymeleaf语法遍历到html页面
     *
     * @param model 我需要把数据共享到页面，需要使用共享域
     * @return 跳转到list.html页面
     */
    @GetMapping("/list")
    public String list(Model model){
        List<Person> list = Arrays.asList(
                new Person(1L,"张三1","zs1@qq.com",15,"pm"),
                new Person(3L,"张三2","zs2@qq.com",15,"pm"),
                new Person(4L,"张三3","zs3@qq.com",15,"pm"),
                new Person(7L,"张三4","zs4@qq.com",15,"admin"),
                new Person(8L,"张三5","zs5@qq.com",15,"hr")
        );

        model.addAttribute("persons",list);
        return "list";
    }
```

 [label color="blue"]list.html[/label] 
```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>列表页</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>

<body>
<!--需求：将welcome中的list遍历转到当前列表页-->
<!--为了表格好看，我可以引入bootstrap样式-->
<table class="table">
    <thead>
    <tr>
        <th scope="col">#</th>
        <th scope="col">名字</th>
        <th scope="col">邮箱</th>
        <th scope="col">年龄</th>
        <th scope="col">角色</th>
        <th scope="col">状态信息</th>
    </tr>
    </thead>
    <tbody>
    <tr th:each="person,stats : ${persons}">
        <th scope="row" th:text="${person.id}">1</th>
        <td th:text="${person.userName}">Mark</td>
        <!--这里我们可以使用一下thymeleaf的行内写法-->
        <td> [[${person.email}]] </td>
        <td> [[${person.age}]] </td>
        <td th:text="${person.role}"></td>
        <td>
            index: [[${stats.index}]] <br/>
            count: [[${stats.count}]] <br/>
            size(总数量): [[${stats.size}]] <br/>
            current: [[${stats.current}]] <br/>
            even(true)/odd(false): [[${stats.even}]] <br/>
            first: [[${stats.first}]] <br/>
            last: [[${stats.last}]] <br/>
        </td>
    </tr>

    </tbody>
</table>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
        crossorigin="anonymous"></script>

</body>
</html>
```
效果图
![6.png][7]
在遍历中，还可以加入**stats**，查看当前遍历的行信息。(代码中使用了thymeleaf中的行内引用)
 - index：当前遍历元素的索引，从0开始
 - count：当前遍历元素的索引，从1开始
 - size：需要遍历元素的总数量
 - current：当前正在遍历的元素对象
 - even/odd：是否偶数/奇数行
 - first：是否第一个元素
 - last：是否最后一个元素


----------
###if,switch
list.html

```html
    <tr th:each="person,stats : ${persons}">
        <th scope="row" th:text="${person.id}">1</th>
        <td th:text="${person.userName}">Mark</td>
        <!--这里我们可以使用一下thymeleaf的行内写法-->
        <td th:if="${#strings.isEmpty(person.email)}" th:text="'联系不上'">  </td>
        <td th:if="${not #strings.isEmpty(person.email)}" th:text="${person.email}"></td>
        <td th:text="|${person.age} / ${person.age >= 18 ? '成年':'未成年' }|"> </td>
        <td th:switch="${person.role}">
            <button th:case="'admin'" type="button" class="btn btn-danger">管理员</button>
            <button th:case="'pm'" type="button" class="btn btn-primary">项目经理</button>
            <button th:case="'hr'" type="button" class="btn btn-default">人事</button>
        </td>
    </tr>

```
----------

###属性选择

我们可以将域对象共享的数据，或者是session作用域中的数据，直接放到标签体，用`th:object`标签来添加，这样添加的好处就是，在标签体中，当我们需要对象的数据的时候，我们可以直接使用`*{成员属性}`来取代 `${对象.成员属性}`的形式。

```html
<tr th:each="person,stats : ${persons}" th:if="${person.age > 10}" th:object="${person}">
        <th scope="row" th:text="${person.id}">1</th>
        <!--<td th:text="${person.userName}">Mark</td>-->
        <td th:text="*{userName}">Mark</td>
    </tr>
```
最后当前list.html的全部代码我放在此处：

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>列表页</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"
          integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
</head>

<body>
<!--导航区-->
<div th:replace="~{common :: myheader}"></div>
<!--<header class="p-3 text-bg-dark">
    <div class="container">
        <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
            <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
                <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
                    <use xlink:href="#bootstrap"></use>
                </svg>
            </a>

            <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
                <li><a href="#" class="nav-link px-2 text-secondary">Home</a></li>
                <li><a href="#" class="nav-link px-2 text-white">Features</a></li>
                <li><a href="#" class="nav-link px-2 text-white">Pricing</a></li>
                <li><a href="#" class="nav-link px-2 text-white">FAQs</a></li>
                <li><a href="#" class="nav-link px-2 text-white">About</a></li>
            </ul>

            <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
                <input type="search" class="form-control form-control-dark text-bg-dark" placeholder="Search..."
                       aria-label="Search">
            </form>

            <div class="text-end">
                <button type="button" class="btn btn-outline-light me-2">Login</button>
                <button type="button" class="btn btn-warning">Sign-up</button>
            </div>
        </div>
    </div>
</header>-->
<div class="container">
    <table class="table">
        <thead>
        <tr>
            <th scope="col">#</th>
            <th scope="col">名字</th>
            <th scope="col">邮箱</th>
            <th scope="col">年龄</th>
            <th scope="col">角色</th>
            <th scope="col">状态信息</th>
        </tr>
        </thead>
        <tbody>
        <tr th:each="person,stats : ${persons}" th:if="${person.age > 10}" th:object="${person}">
            <th scope="row" th:text="${person.id}">1</th>
            <!--<td th:text="${person.userName}">Mark</td>-->
            <td th:text="*{userName}">Mark</td>
            <!--这里我们可以使用一下thymeleaf的行内写法-->
            <td th:if="${#strings.isEmpty(person.email)}" th:text="'联系不上'">  </td>
            <td th:if="${not #strings.isEmpty(person.email)}" th:text="${person.email}"></td>
            <td th:text="|${person.age} / ${person.age >= 18 ? '成年':'未成年' }|"> </td>
            <td th:switch="${person.role}">
                <button th:case="'admin'" type="button" class="btn btn-danger">管理员</button>
                <button th:case="'pm'" type="button" class="btn btn-primary">项目经理</button>
                <button th:case="'hr'" type="button" class="btn btn-default">人事</button>
            </td>

            <td>
                index: [[${stats.index}]] <br/>
                count: [[${stats.count}]] <br/>
                size(总数量): [[${stats.size}]] <br/>
                current: [[${stats.current}]] <br/>
                even(true)/odd(false): [[${stats.even}]] <br/>
                first: [[${stats.first}]] <br/>
                last: [[${stats.last}]] <br/>
            </td>
        </tr>

        </tbody>
    </table>
</div>

<!--需求：将welcome中的list遍历转到当前列表页-->
<!--为了表格好看，我可以引入bootstrap样式-->


<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
        crossorigin="anonymous"></script>

</body>
</html>
```


----------
###片段引用
片段引用我录制了视频，用于解释。
[video title="片段引用 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E7%89%87%E6%AE%B5%E5%BC%95%E7%94%A8.mkv " container="bjerq6ed4wh" subtitle=" " poster=" "] [/video]


----------
###devtools
如果在后台IDEA修改页面，那么当前页面存在缓存，刷新是没有效果的。我们可以在pom文件中导入SpringBoot给我们整合好的一个**热启动工具devtools**

```xml
<!--热启动功能-->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
        </dependency>
```

 -  [label color="red"]CTRL + F9 重新编译[/label] 

以后不仅是页面，Java代码修改后，只要**CTRL + F9 重新编译**，就可以重新启动。
推荐修改页面后，使用devtools； [label color="red"]对于代码的修改，还是重新手动启动。java代码的修改，如果devtools热启动，可能会引起一些bug[/label] 

----------

我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://www.thymeleaf.org/documentation.html
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/2243593957.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/479676347.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/4275596574.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/1522710987.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/10/3351218590.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/10/841421327.png