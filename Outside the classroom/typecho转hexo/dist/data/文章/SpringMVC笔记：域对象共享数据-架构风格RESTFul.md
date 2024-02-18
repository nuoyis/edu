---
title: SpringMVC笔记：域对象共享数据-架构风格RESTFul
date: 2023-08-15 19:16:00
categories: SpringMVC
tags: [request,session,application,域对象]
---
springMVC中间阶段学习笔记，包括域对象中共享数据，通过RESTFul实现不同的增删改查，还要过滤器源码解析


<!--more-->

##域对象共享数据
之前笔记中有提及[会话][1]
处理请求的时候，[设置编码][2]SpringMVC为我们提供了编码过滤器，注册在web.xml里面就行。[获取请求参数][3]，能够获取请求参数，下一步就是将请求参数作为条件，调用Service层处理业务逻辑，Service调用Dao访问数据库。将最终的结果返回给Service最后到控制层。如果我们有数据往页面中去发送的，需要将数据在域对象中进行共享。
域对象：**Request**一次请求,**Serssion**一次会话(浏览器开启到浏览器关闭),**ServletContext**(Application服务器开启到服务器关闭)。
[note type="primary flat"]session中的数据和服务器是否关闭没有关系，只和浏览器是否关闭有关系。因为session中有**钝化**和**活化**。**钝化**指的是服务器关闭了，但是浏览器没有关闭，表名会话仍然在继续，我们存储在session中的数据就会序列化,序列化到磁盘上。如果浏览器仍然没有关闭，但是服务器又重新开启了，会将我们钝化之后文件中的内容，重新读取到Session中，这就是**活化**。所以说session中的数据只和浏览器是否关闭有关系。

ServletContext只和服务器的关闭有关系，表示上下文对象，只在我们服务器启动时创建，在服务器关闭时候销毁，从头到尾之创建一次，这就是为什么能在域对象中共享数据，就是因为使用的对象都是同一个，所以说才能在同一个对象中获取数据。[/note]
选择域对象应该选择能实现功能的，范围最小的域对象。

**Session**经常用来保存用户的登陆状态，登录之后只要浏览器不关闭，在当前的会话就一直是登陆成功， [label color="red"]除非超过30分钟没有访问session中的数据，那session会自动失效(默认最大时效)[/label] 。

原生的Servlet里面往域对象中共享数据，我们需要有request,session,servletcontext才能向对应域中共享数据。
###原生Servlet向request域对象共享数据
ScopeController类

```java
/*Scope域属性*/
@Controller//要想让SpringMVC找到我们的控制器，那么我们的控制器必须是IoC容器中的组件
public class ScopeController {
    @RequestMapping("/testRequestByServletAPI")
    public String testRequestByServletAPI(HttpServletRequest request){
        /*
        测试当前的域对象，
        通过原生ServletAPI往request域对象创建共享数据setAttribute("键","值");
        getAttribute("");获取共享数据
        removeAttribute("")删除共享数据

        转发到success.html,在success.html中可以获取域对象的数据
        */
        request.setAttribute("testRequestScope","hello,servletAPI");
        //属于转发，WEB-INF下面的资源重定向访问不了，只能使用转发访问success.html
        return "success";
    }
}

```
success.html

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
success<br>
<!--通过p标签中的text代替当前标签中的文本,${}里添加共享数据的键
如果直接写在p标签中无法动态解析通过 th:属性 动态获取
在html中只有th:所对应的属性中的内容才会被解析
如果访问的是request(请求域)中的数据，直接写共享数据的键。
如果写共享到session中的数据，直接写session.共享数据的键
如果写共享到servletcontext中的数据，直接写application.共享数据的键
-->
<p th:text="${testRequestScope}"></p>
</body>
</html>
```

![1.png][4]

----------
上面使用原生方式过于过时，在springMVC中提供了其他许多的方式。
###ModelAndView向request域对象获取数据
**Model**模型指的是往域对象中共享数据的功能
**View**视图指的是我们最终所设置的视图名称，经过视图解析器解析，跳转到我们指定页面的过程。
 [label color="red"]需要注意的是，使用ModelAndView，书写方法的时候，返回值传递的是一个封装的ModelAndView对象。[/label] 

```java
  @RequestMapping("/testModelAndView")
    public ModelAndView testModelAndView(){
        /*方法的返回值必须是ModelAndView
        因为ModelAndView是两个功能，模型功能和视图，作为方法的返回值，
        返回给DispatcherServlet，DispatcherServlet才能去解析他。
        两个功能：
        model 往请求域中共享功能 view 视图功能
        */
        ModelAndView mav = new ModelAndView();

        //处理模型数据，即向请求域request中共享数据
        mav.addObject("testRequestScope","Hello,ModelAndView");

        //设置视图名称，相当于return "success";
        mav.setViewName("success");
        return mav;
    }
```
![2.png][5]

----------
###Model、Map、ModelMap向request域对象共享数据
####Model向request域对象共享数据

```java
    @RequestMapping("/testModel")
    public String testModel(Model model){
        /*
        形参位置创建一个Model类型的形参model,有点类似于原生servlet
        往我们的请求域中共享数据
        */
        model.addAttribute("testRequestScope","Hello,Model");
        return "success";
    }
```
####Map向request域对象共享数据

```java
    @RequestMapping("/testMap")
    public String testMap(Map<String, Object> map) {
        /*
        形参位置创建一个Map集合，
        往Map集合中存放的数据，就是往域对象中共享的数据
        键一般都是String
        值与当前存储的数据相关Object
        */
        map.put("testRequestScope","Hello,Map");
        return "success";
    }
```
![3.png][6]
####ModelMap向request域对象共享数据

```java
    @RequestMapping("/testModelMap")
    public String testModelMap(ModelMap modelMap) {
        modelMap.addAttribute("testRequestScope", "Hello,ModelMap");
        return "success";
    }

```
SringMVC已经为我们提供了四种方式，所以说我们就不要使用原生Servlet。
####Model、ModelMap、Map的关系
在后面三种，都要在控制器方法中创建形参，然后形参具有向请求域中共享数据的功能

Model、Map形参都是一个接口，无法直接创建对象，通过实现类创建对象，将三个方法输出形参，发现是一样的内容，表明toString重写之后的内容是一样的。三个对象在实例化的时候，用的是同一个对象实例化。使用反射，将真正实例化类型的全类名，进行一个输出。发现是同一个类，表明为我们当前的形参进行赋值的对象，使用的是同一个。
![4.png][7]

ModelMap继承于LinkedHashMap类，相当于也是顶层接口Map的实现类，**BindingAwarModelMap**继承于**ExtendedModelMap**，ExtendedModelMap类实现了Model接口，所以说**BindingAwarModelMap**可以**实例化ModelMap**，也可以**实例化Model**,也可以**实例化Map**。

[note type="primary flat"]ModelMap实现了Map接口，在下面有一个类ExtendedModelMap实现Model接口。Model、ModelMap、Map类型的参数其实本质上都是 BindingAwareModelMap 类型的[/note]

![5.png][8]

不管使用的方式是什么，最终都会将我们的模型数据，和视图信息封装到一个**ModelAndView**中。
Debug断点调试。
![6.png][9]

----------

###向Session域共享数据
虽然springMVC也为我们提供了对应的向session作用域中共享数据的方式(使用注解@SessionAttribute)，但是原生的方式更加简单。在方法中添加一个HttpSession的形参即可。

```java
    @RequestMapping("/testSession")
    public String testSession(HttpSession session){
        session.setAttribute("testSessionScope","Hello,Session");
        return "success";
    }
```
success.html
```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
success<br>
<p th:text="${testRequestScope}"></p>
<!--thymeleaf中想要访问session中的数据通过session.键的方式，当前请求域不显示，因为在控制器方法中没有往请求域中共享数据。-->
<p th:text="${session.testSessionScope}"></p>
</body>
</html>
```

![7.png][10]

----------
###向Application(ServeltContext)域共享数据
只需要获取ServletContext对象，方法很多，向Session域中共享数据是通过设置形参，我们可以在当前方法中通过session获取当前的servletcontext。


```java
    @RequestMapping("/testApplication")
    public String testApplication(HttpSession session) {
        //获取当前的Application对象
        ServletContext application = session.getServletContext();
        /*它所对应的范围是当前整个工程的范围
        因为当前的servletcontext对象是在我们服务器启动时候创建的
        而我们当前服务器整个工作过程中我们创建的ServletContext都是同一个*/
        application.setAttribute("testApplicationScope", "Hello,application");
        return "success";
    }

```
![8.png][11]


----------
###三种springMVC视图
####ThymeleafView视图
如果控制器方法的返回值，也就是**视图名称**没有任何前缀的话，此时的视图名称会被SpringMVC配置文件中所配置的视图解析器解析，并通过**转发**的形式跳转到对应**视图页面**。

```java
    @RequestMapping("/testThymeleafView")
    public String testThymeleafView(){
        /*返回的视图名称没有任何前缀，
        说明返回的视图名称一定被springMVC.xml中视图解析器解析.
        什么情况下创建的是ThymeleafView?
        如果视图名称没有任何前缀,就会被ThymeleafViewResolver解析,
        被它解析之后的视图一定是一个ThymeleafView
        */
        return "success";
    }
```
####InternalResourceView视图（转发试图）
 `forward:` 为前缀
```java
    @RequestMapping("/testThymeleafView")
    public String testThymeleafView(){
        return "success";
    }

    @RequestMapping("/testForward")
    public String testForward(){
        /*
        返回的是视图名称,视图名称本身没有前缀也是转发的效果.
        通过该控制器方法转发到testThymeleafView请求中
        会将当前的前缀forward:截取掉,剩下部分直接通过转发跳转到对应的资源
        此时创建的视图就不再是ThymeleafView
        会帮我们创建两次视图
        截取将剩余部分转发就是InternalResourceView
        当找到请求映射的时候,还要在创建一次视图,此时就是ThymeleafView

        */
        return "forward:/testThymeleafView";

    }
```
![9.png][12]

####RedirectView视图(重定向试图)
重定向可以改变地址栏中的地址，相当于浏览器再一次发送请求访问。某一个业务逻辑成功之后和我们原先的请求没有关系了，需要重定向跳转到下一个功能，如果使用转发还保存了上一次请求的路径。所以说在业务逻辑操作成功之后，都要通过重定向实现页面跳转。
重定向也有指定的前缀，如果没有前缀情况下，肯定指定的创建ThymeleafView.

[note type="info flat"]回顾：转发和重定向的**区别**
①转发一次请求，第一次是浏览器发送，第二次发生在服务器内部。所说一次指的是浏览器发送的请求。
②重定向是浏览器发送了两次请求，第一次访问的是servlet，第二次访问的是我们重定向中的地址。
③转发的服务器地址栏还是第一次发送的地址，而重定向是浏览器发送了两次请求，所以说地址栏中的地址是重定向中的地址。
④转发可以获取请求域中的数据，重定向不可以获取。因为转发是一次请求，用到的request对象是同一个。能不能来获取域对象的数据主要就是看所使用的对象是不是同一个。重定向浏览器发送了两次请求，对应两个request对象。
⑤转发能访问WEB-INF下的资源，但是重定向不可以。因为WEB-INF下的资源具有**安全性**，具有**隐藏性**，只能通过**服务器内部**来访问，不能通过浏览器来访问。
⑥转发不能跨域，而重定向可以跨域。什么叫跨域，就是说转发是发生在服务器内部的，那只能访问服务器内部资源。而重定向是浏览器发送的两次请求，通过浏览器可以访问任何资源。[/note]

 `redirect:` 前缀

```java
    @RequestMapping("/testRedirect")
    public String testRedirect(){
        /*
        重定向到HTML页面也访问不了,因为页面存放在WEB-INF下面
        而重定向是不能访问WEB-INF下面的内容
        要重定向,重定向到的也是一个请求,而不是一个具体的页面

        */
        return "redirect:/testThymeleafView";
    }


```
![10.png][13]
好好对比**url**地址，就能解释转发和重定向的回顾的第三点。

----------
####视图控制器
视图控制器也是帮助我们实现当前的**请求地址**，和**视图**之间的映射关系的。
[label color="red"]在当前的请求映射所对应的控制器方法中,没有其他任何请求过程的处理,只需要来设置(返回)一个视图名称,就可以使用**view-controller**.需要引入mvc命名空间[/label] 

 [label color="orange"]springMVC.xml[/label] 

```xml
xmlns:mvc="http://www.springframework.org/schema/mvc"       xsi:schemaLocation="http://www.springframework.org/schema/context/spring-context.xsd       http://www.springframework.org/schema/mvc
https://www.springframework.org/schema/mvc/spring-mvc.xsd"
```
**全部源码**
**springMVC.xml**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/mvc
       https://www.springframework.org/schema/mvc/spring-mvc.xsd">

    <!--扫描组件-->
    <context:component-scan base-package="com.atguigu.mvc.controller"></context:component-scan>


    <!--配置视图解析器-->
    <!-- 配置Thymeleaf视图解析器 -->
    <bean id="viewResolver" class="org.thymeleaf.spring5.view.ThymeleafViewResolver">
        <property name="order" value="1"/>
        <property name="characterEncoding" value="UTF-8"/>
        <property name="templateEngine">
            <bean class="org.thymeleaf.spring5.SpringTemplateEngine">
                <property name="templateResolver">
                    <bean class="org.thymeleaf.spring5.templateresolver.SpringResourceTemplateResolver">

                        <!-- 视图前缀 -->
                        <property name="prefix" value="/WEB-INF/templates/"/>

                        <!-- 视图后缀 -->
                        <property name="suffix" value=".html"/>
                        <property name="templateMode" value="HTML5"/>
                        <property name="characterEncoding" value="UTF-8" />
                    </bean>
                </property>
            </bean>
        </property>
    </bean>

    <!--
    path:设置请求地址,和@RequestMapping中value值保持一致
    view-name:设置当前的视图名称
    在什么情况下才可以使用:
    在当前的请求映射所对应的控制器方法中,没有其他请求过程的处理,
    只需要来设置一个视图名称的时候,就可以使用view-controller.需要引入mvc命名空间

    如果只是设置了任何一个view-controller,控制器中的所有映射将全部失效,点击首页其他超链接出现(404)
    必须添加一个标签<mvc:annotation-driven/>
    -->
    <mvc:view-controller path="/" view-name="index"></mvc:view-controller>

    <mvc:view-controller path="/test_rest" view-name="test_rest" ></mvc:view-controller>

    <!--开启MVC的注解驱动,本标签功能也非常强大,比如说java转json对象,

    这个标签之后一定要配置,在不同情况下配置的功能不同-->
    <mvc:annotation-driven/>

</beans>
```


```xml
    <!--
    path:设置请求地址,和@RequestMapping中value值保持一致
    view-name:设置当前的视图名称
    在什么情况下才可以使用:
    在当前的请求映射所对应的控制器方法中,没有其他请求过程的处理,
    只需要来设置一个视图名称的时候,就可以使用view-controller.需要引入mvc命名空间

    如果只是设置了任何一个view-controller,控制器中的所有映射将全部失效,点击首页其他超链接出现(404)
    必须添加一个标签<mvc:annotation-driven/>
    -->
    <mvc:view-controller path="/" view-name="index"></mvc:view-controller>

    <!--开启MVC的注解驱动,本标签功能也非常强大,比如说java转json对象,

    这个标签之后一定要配置,在不同情况下配置的功能不同-->
    <mvc:annotation-driven/>

```
![11.png][14]
我也不知道这里IDEA为什么会报红(我猜是犯病了)但并不影响运行
附上全部的springMVC.xml源码

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/mvc
       https://www.springframework.org/schema/mvc/spring-mvc.xsd">

    <!--扫描组件-->
    <context:component-scan base-package="com.atguigu.mvc.controller"></context:component-scan>


    <!--配置视图解析器-->
    <!-- 配置Thymeleaf视图解析器 -->
    <bean id="viewResolver" class="org.thymeleaf.spring5.view.ThymeleafViewResolver">
        <property name="order" value="1"/>
        <property name="characterEncoding" value="UTF-8"/>
        <property name="templateEngine">
            <bean class="org.thymeleaf.spring5.SpringTemplateEngine">
                <property name="templateResolver">
                    <bean class="org.thymeleaf.spring5.templateresolver.SpringResourceTemplateResolver">

                        <!-- 视图前缀 -->
                        <property name="prefix" value="/WEB-INF/templates/"/>

                        <!-- 视图后缀 -->
                        <property name="suffix" value=".html"/>
                        <property name="templateMode" value="HTML5"/>
                        <property name="characterEncoding" value="UTF-8" />
                    </bean>
                </property>
            </bean>
        </property>
    </bean>

    <!--
    path:设置请求地址,和@RequestMapping中value值保持一致
    view-name:设置当前的视图名称
    在什么情况下才可以使用:
    在当前的请求映射所对应的控制器方法中,没有其他请求过程的处理,
    只需要来设置一个视图名称的时候,就可以使用view-controller.需要引入mvc命名空间

    如果只是设置了任何一个view-controller,控制器中的所有映射将全部失效,点击首页其他超链接出现(404)
    必须添加一个标签<mvc:annotation-driven/>
    -->
    <mvc:view-controller path="/" view-name="index"></mvc:view-controller>

    <!--开启MVC的注解驱动,本标签功能也非常强大,比如说java转json对象,

    这个标签之后一定要配置,在不同情况下配置的功能不同-->
    <mvc:annotation-driven/>

</beans>
```

----------
##RESTFul(☆)
RESTFul叫做**表述层资源状态转移**,通过转移和操作资源的表述，来间接实现操作资源的目的。
**REST**指的是表述层(表现层)资源状态转移，表述层是前端的控制页面(视图)到后端的控制层。
将web工程放在服务器上的过程叫做部署，当工程部署在Tomcat服务器，当前工程中的内容在服务器上都叫**资源**。
资源表现形式不一样，有可能是个xml、html、json···，资源的状态不一样，资源的状态指的是资源的表现形式(表述)
状态转移说的是：在客户端和服务器端之间转移，来代表资源状态的表述。描述的就是当前浏览器和服务器进行交互的一种状态，将我们当前访问的内容由服务器转移到客户端。
我们需要通过HTTP协议里面**四种不同的请求方式**，来表示我们不同的操作。
 - GET查询
 - POST添加
 - PUT修改
 - DELETE删除
而使用RESTful作为统一的规则，只要知道操作的资源是什么，只要为资源设置一个描述它的名词，可以通过**同一个请求路径**，来进行不一样的操作。
我们不再用 **？** 进行传参，而是把所有数据都以 **/** 来拼接到请求地址中。

> REST 风格提倡 URL 地址使用统一的风格设计，从前到后各个单词使用斜杠分开，不使用问号键值对方
式携带请求参数，而是将要发送给服务器的数据作为 URL 地址的一部分，以保证整体风格的一致性。


操作|传统方式|**REST风格**
:--:|:--:|:--:
查询操作|getUserById?id=1|user/1**(get请求方式)**
保存操作|saveUser|user**(post请求方式)**
删除操作|deleteUser?id=1|user/1**(delete请求方式)**
更新操作|updateUser|user**(put请求方式)**


----------
###模拟get和post请求
UserController类

```java
@Controller
public class UserController {
    /*

    使用RESTFul模拟用户资源资源的增删改查
    /user
    一套完整的增删改查应该是五个功能：查询所有数据，根据id查询单个数据，删除，添加，修改
    /user   GET请求   查询所有用户信息
    /user/1   GET请求   根据用户id来查询用户信息
    /user   POST请求   添加用户信息
    /user/1   DELETE请求   删除用户信息(主键)
    /user   PUT请求   更新用户信息

     @RequestMapping(value = "",method = )对应属性应该需要两个value , method
     如果使用了派生注解，就可以只使用value
     */


    @RequestMapping(value = "/user", method = RequestMethod.GET)
    public String getAlluser() {
        //方法名随意
        System.out.println("查询所有用户信息");
        return "success";
    }


    @RequestMapping(value = "/user/{id}", method = RequestMethod.GET)
    public String getUserById(){
    /*
    要想接收id，需要用占位符来表示：{id}
    用户无法看到方法，方法名随意
     */
        System.out.println("根据id来查询用户信息");
        return "success";
    }


    @RequestMapping(value = "/user",method = RequestMethod.POST)
    public String insertUser(String username,String password){
        System.out.println("添加用户信息:" + username + "," + password);
        return "success";
    }


}

```
test_rest.html

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <!--模拟发送这些请求-->
    <a th:href="@{/user}">查询所有用户信息</a><br>
    <!--首先超链接的请求方式就是get请求
    对于RESTFul以斜线的方式拼接到请求地址，真正使用案例需要按照具体信息的id来决定
    -->
    <a th:href="@{/user/1}">根据id来查询用户信息</a><br>

<!--因为添加需要post请求，目前为止能够发送post请求方式只有两种ajax，post-->
<form th:action="@{/user}" method="post">
    用户名:<input type="text" name="username"><br>
    密码:<input type="password" name="password"><br>
    <input type="submit" value="添加"><br>
</form>

</body>
</html>
```
![12.png][15]

----------
###模拟put和delete请求
如果form表单中写put/delete等其他请求，那么会默认以get请求为准，所以说form表单中发送put请求不起作用，delete同理。在MVC中提供了一套过滤器HiddenHttpMethodFilter。
web.xml

```xml
    <!--配置HiddenHttpMethodFilter-->
    <filter>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <!--/* 表示对所有请求进行处理-->
        <url-pattern>/*</url-pattern>
    </filter-mapping>

```
####HiddenHttpMethodFilter源码
翻看**源码HiddenHttpMethodFilter**，只展示部分

```java
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        HttpServletRequest requestToUse = request;
        if ("POST".equals(request.getMethod()) && request.getAttribute("javax.servlet.error.exception") == null) {
            String paramValue = request.getParameter(this.methodParam);
            if (StringUtils.hasLength(paramValue)) {
                String method = paramValue.toUpperCase(Locale.ENGLISH);
                if (ALLOWED_METHODS.contains(method)) {
                    requestToUse = new HttpMethodRequestWrapper(request, method);
                }
            }
        }

        filterChain.doFilter((ServletRequest)requestToUse, response);
    }

    private static class HttpMethodRequestWrapper extends HttpServletRequestWrapper {
        private final String method;

    private static class HttpMethodRequestWrapper extends HttpServletRequestWrapper {
        private final String method;

        public HttpMethodRequestWrapper(HttpServletRequest request, String method) {
            super(request);
            this.method = method;
        }

        public String getMethod() {
            return this.method;
        }
    }

```
![13.png][16]
创建一个过滤器，重写其中所有的抽象方法，真正要重写的就是**doFilter**方法。

该源码告诉我们，如果想要发送put或delete请求，需要做两件事

 - **原本请求方式必须为POST**
 - **必须传递过来请求参数_method** `(this.methodParam)` 


----------

最终我们的请求方式就是**_method**转换为大写的结果。
调整表单，添加隐藏域，这也就证明了为什么要叫**Hidden**HttpMethodFilter的原因。
test_rest.html

```html
    <form th:action="@{/user}" method="post">
        <!--我们不适用ajax的情况下必须使用form表单-->
        <!--不想让有用户看到，所以使用隐藏域-->
        <input type="hidden" name="_method" value="PUT">
        <!--如果form表单写的不是get/post，会默认以get方式为准,设置为put不会起作用-->
        用户名:<input type="text" name="username"><br>
        密码:<input type="password" name="password"><br>
        <input type="submit" value="修改"><br>
    </form>
```
![14.png][17]
测试
![15.png][18]

 - 想要实现**DELETE**请求，但是需要解决如果删除是一个**超链接**应该怎么处理这个问题？

需要使用 [label color="blue"]vue[/label] 在超链接上绑定一个点击事件，点击事件里面先阻止超链接的默认行为跳转，然后获得当前某一个表单，表单里面不需要有任何数据，只需要写一个form表单(不适用ajax情况下)，将请求方式设置为post，里面写个隐藏域( `name="_method",value="delete"`)，不需要书写提交按钮。本身是要通过超链接控制表单的提交。通过 [label color="blue"]vue[/label] 为超链接绑定事件，在所绑定的事件里面获取表单，通过submit方法，让表单提交，再取消超链接的默认行为。


[note type="primary flat"]在**HttpMethodFilter**里已经获取了参数，在CharacterEncodingFilter里设置编码**没有任何作用**，所以说，当我们需要同时使用这两个过滤器的时候(以后也必不可少，两个过滤器，一个Servlet)，顺序一定要先配置处理编码的，再设置处理请求方式的过滤器。因为设置编码之前不能获取任何的请求参数，只要获取，设置编码没有任何的效果了。[/note]
![16.png][19]

web.xml
```xml
    <!--配置编码过滤器-->
    <filter>
        <filter-name>CharacterEncodingFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <init-param>
            <param-name>forceResponseEncoding</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>CharacterEncodingFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>

    <!--配置HiddenHttpMethodFilter-->
    <filter>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
    </filter>
    <filter-mapping>
        <filter-name>HiddenHttpMethodFilter</filter-name>
        <!--/* 表示对所有请求进行处理-->
        <url-pattern>/*</url-pattern>
    </filter-mapping>
```

那这样,一个标配 [label color="orange"]web.xml[/label] 格式我添加到了之前的[框架搭建][20]中。你可以跳转到该页面去访问对应的最终格式

----------
###RESTFul案例实现删除功能
这里有使用到**Vue**，我提前浅浅学习了一下下[Vue笔记][21]可以参考
见视频
[video title="删除功能解释 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-16%2001-35-53.mkv " container="b37gilvt87c" subtitle=" " poster=" "] [/video]


----------

####开放对静态资源的访问
在这里我配置了 `<mvc:default-servlet-handler/>` ，它和 `<mvc:annotation-driven/>` 一样重要，在spring.xml中必不可少，我把完整的配置写在这里。当然我配置了一定的**视图控制器**，它基于我的RESTFul案例，你可以根据你的需要进行修改。在框架搭建中我设置了跳转方便在这里参考。


springMVC.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd
       http://www.springframework.org/schema/mvc
       https://www.springframework.org/schema/mvc/spring-mvc.xsd">


    <!--扫描组件-->
    <context:component-scan base-package="com.atguigu.rest"></context:component-scan>
    
    <!-- 配置Thymeleaf视图解析器 -->
    <bean id="viewResolver" class="org.thymeleaf.spring5.view.ThymeleafViewResolver">
        <property name="order" value="1"/>
        <property name="characterEncoding" value="UTF-8"/>
        <property name="templateEngine">
            <bean class="org.thymeleaf.spring5.SpringTemplateEngine">
                <property name="templateResolver">
                    <bean class="org.thymeleaf.spring5.templateresolver.SpringResourceTemplateResolver">

                        <!-- 视图前缀 -->
                        <property name="prefix" value="/WEB-INF/templates/"/>

                        <!-- 视图后缀 -->
                        <property name="suffix" value=".html"/>
                        <property name="templateMode" value="HTML5"/>
                        <property name="characterEncoding" value="UTF-8" />
                    </bean>
                </property>
            </bean>
        </property>
    </bean>


    <!--配置视图控制器-->
    <mvc:view-controller path="/" view-name="index"></mvc:view-controller>
    <mvc:view-controller path="/toAdd" view-name="employee_add"></mvc:view-controller>

    <!--开放对静态资源的访问 相对于配置了一个默认(default)的servlet-->
    <mvc:default-servlet-handler/>

    <!--开启MVC的注解驱动-->
    <mvc:annotation-driven/>
    
</beans>
```


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://www.kaijavademo.top/85.html#cl-5
  [2]: https://www.kaijavademo.top/259.html#cl-24
  [3]: https://www.kaijavademo.top/259.html#cl-15
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/2309589347.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/1774747051.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/3267159502.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/952848351.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/08/3737538478.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/08/1161499293.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/08/1963548412.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/703498071.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/2477566591.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/08/1147115150.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/1858100834.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/08/3539631210.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/08/619030439.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/08/2268219479.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/08/3979645098.png
  [19]: https://img.kaijavademo.top/typecho/uploads/2023/08/2094893232.png
  [20]: https://www.kaijavademo.top/259.html#cl-5
  [21]: https://www.kaijavademo.top/323.html