---
title: JavaWeb笔记-Servlet
date: 2023-07-15 12:05:00
categories: JavaWeb
tags: [JavaWeb,JavaWeb笔记,Servlet]
---
JavaWeb-Servlet入门


<!--more-->

实现收到http协议后获取对应的参数
 [label color="blue"]准备工作[/label] 

 1. 在模块中新建项目，并且勾选对应的Web Application,部署Tomcat8
![1.png][1]

 2. 导入对应的servlet依赖，当然，可以直接导入整个Tomcat中的jar包
![2.png][2]

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form action="add" method="post">
        名称:<input type="text" name="fname"/><br/>
        价格:<input type="text" name="price"/><br/>
        库存:<input type="text" name="fcount"/><br/>
        备注:<input type="text" name="remark"/><br/>
        <input type="submit" value="添加"/>
    </form>
</body>
</html>
```
 我们需要接收到对应从浏览器发过来的请求，我们在当前模块下 [label color="blue"]src下[/label] 新建一个**AddServlet**类，接收 [label color="red"]对应名为add[/label] 的请求。
防止有 [label color="red"]中文乱码[/label] 的问题，方法中我们还应该第一行加入 `request.setCharacterEncoding("UTF-8");` 

**总结笔记**
[note type="default flat"]1.设置编码
tomcat8之前，设置编码：
    1) get请求方式:
        //get方式目前不需要设置编码（基于tomcat8）
        //如果是get请求发送的中文数据，转码稍微有点麻烦(tomcat8之前)
        /*String fname = request.getParameter("fname");
        //1.将字符串打散成字节数组
        byte[] bytes = fname.getBytes("ISO-8859-1");
        //2.将字节数组按照设定的编码重新组装成字符串
        fname = new String(bytes,"UTF-8");*/
    2) post请求方式:
        request.setCharacterEncoding("UTF-8");
        tomcat8开始，设置编码，只需要针对post方式
        //post方式下，设置编码，防止中文乱码
    注意：
        需要注意的是，设置编码(post)这一句代码，必须在所有获取参数动作之前
[/note]


```java
/*注意，还需要设置add对应的该类*/
public class AddServlet extends HttpServlet {
    /*
    此方法能响应post请求，我们发送一个post请求过来,此方法会被调用
    此方法需要抛出异常 IOException , ServletException
    方法有两个参数 HttpServletRequest request, HttpServletResponse response
    参数一：HttpServletRequest request 表示客户端给服务器端发送请求的时候，服务器端就把请求封装成一个对象request；我们可以获取里面的信息
    */
    @Override
    public void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException { //快捷键doPost
        //get方式目前不需要设置编码（基于tomcat8）
        //如果是get请求发送的中文数据，转码稍微有点麻烦(tomcat8之前)
        /*String fname = request.getParameter("fname");
        //1.将字符串打散成字节数组
        byte[] bytes = fname.getBytes("ISO-8859-1");
        //2.将字节数组按照设定的编码重新组装成字符串
        fname = new String(bytes,"UTF-8");*/

        //post方式下，设置编码，防止中文乱码
        //需要注意的是，设置编码这一句代码，必须在所有获取参数动作之前
        request.setCharacterEncoding("UTF-8");
        String fname = request.getParameter("fname");
        String priceStr = request.getParameter("price");
        int price = Integer.parseInt(priceStr);
        String fcountStr = request.getParameter("fcount");
        int fcount = Integer.parseInt(fcountStr);
        String remark = request.getParameter("remark");

        FruitDao fruitDao = new FruitDao();

        try {
             fruitDao.addFruit(fname, price, fcount, remark);
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        System.out.println("添加成功");

    }


}
```


那么我们怎么让服务器知道add请求对应的就是这个类呢，我们需要配置
##让请求对应类的配置

 1. 补充 [label color="red"]<servlet>标签[/label] (以后没有提到单标签默认双标签)

 - 在 `<servlet>` 标签中添加 `<servlet-name>` 其中表示对应的类
 - 在 `<servlet>` 标签中添加  `<servlet-class>` 写出`<servlet-name>`中对应类的 [label color="red"]全类名[/label] 

 2. 补充 `<servlet-mapping>` 映射标签
 -  `<servlet-name></servlet-name><!--这里需要和上面的servlet-name保持一致-->` 
 - 补充 `<url-pattern>` 标签，里面为请求的表单名，这里就是上面form表单中add. [label color="red"]servlet映射地址需要以/开头[/label] 。

 [label color="green"]实际操作流程，请看XML表单中的注释。[/label] 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    <servlet>
        <servlet-name>AddServlet</servlet-name>
        <servlet-class>com.atguigu.servlets.AddServlet</servlet-class> <!--这里不能随便写，写对应的全类名-->
    </servlet>
    <servlet-mapping><!--<servlet-mapping>叫做映射-->
        <servlet-name>AddServlet</servlet-name><!--这里需要和上面的servlet-name保持一致-->
        <url-pattern>/add</url-pattern><!--表示add对应AddServlet-->
    </servlet-mapping>
    <!--
    1.用户发请求，action = add
    2.项目中,web.xml中找到url-pattern = /add ->第十二行
    3.找第11行名字servlet-name = AddServlet
    4.找servelet-mapping 中 servlet-name一致的servlet ,找到第七行
    5.找第八行的servlet-class -> com.atguigu.servlets.AddServlet
    6.用户发送的是post请求，(method = post) ,因此 tomcat会执行AddServlet中的dopost方法-->

</web-app>
```

![3.png][3]
----------


##Servlet的继承关系和service方法

[note type="primary flat"]2.Servlet的继承关系-重点查看的是服务方法(Service)
    1.继承关系
    javax.servlet.Servlet接口
        javax.servlet.GenericServlet抽象类
            javax.servlet.http.HttpServlet抽象子类
    2.相关方法
    javax.servlet.Servlet接口
    void init(config) -初始化方法
    void service(request,response)  -服务方法,当客户端向服务器发送请求，这个方法会自动执行
    void destory() -销毁方法

    javax.servlet.GenericServlet抽象类：

        void service(request,response) -仍然是抽象的

    javax.servlet.http.HttpServlet抽象子类

        void service(request,response) -不是抽象的
       1.String method = req.getMethod();获取请求的方式(get/post)
       2.各种if判断，根据请求方式的不同，决定去调用不同的do方法
            if (method.equals("GET")) {
                   this.doGet(req, resp);
               } else if (method.equals("HEAD")) {
                   this.doHead(req, resp);
               } else if (method.equals("POST")) {
                   this.doPost(req, resp);
               } else if (method.equals("PUT")) {
                   this.doPut(req, resp);
               }
       3.在HttpServlet这个抽象类中，do方法都差不多
       protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
               String protocol = req.getProtocol();
               String msg = lStrings.getString("http.method_get_not_supported");
               if (protocol.endsWith("1.1")) {
                   resp.sendError(405, msg);
               } else {
                   resp.sendError(400, msg);
               }

           }
    3.小结
       1)继承关系:HttpServlet -> GenericServlet ->Servlet
       2)Servlet中的核心方法:init(),service(),destroy()
       3)service服务方法:当有请求过来时，service会自动响应(其实是Tomcat容器调用的)
            在HttpServlet中我们会去分析请求方式:到底是get.post,head还是delete等等
            然后再决定掉用的是哪个do开头的方法
            那么再HttpServlet中这些do方法默认都是405的实现风格-要我们子类去实现对应的方法，否则默认会报405错误
      4)因此，我们在新建servlet时，我们才会去考虑请求的方式，从而决定重写哪个do方法
[/note]

 [label color="blue"]我的个人理解：当客户端向服务器发送请求的时候。Servlet中的核心方法service会自动响应，在HttpServlet类中会去先调用service方法分析是哪种请求，然后先去找对应**继承**的**子类方法**中有没有**重写对应的请求**do方法；如果**没有重写**，则调用自己(HttpServlet)本类中的do方法，而HttpServlet所有do方法**默认都是405报错**；如果**重写**了，则会使用子类中的对应do方法。[/label] 


<!--more-->

##Servlet生命周期和Http协议


笔记


[note type="primary flat"]3.Servlet的声明周期
    1)生命周期：从出生到死亡的过程就是生命周期，对应Servlet中的三个方法：init(),service(),destroy()
    2)默认情况下：
        第一次接受请求时，这个Servlet会进行实例化(调用构造方法)、实例化(调用init())，然后服务(调用service方法)
        从第二次请求开始，每一次都是服务
        当容器关闭时，其中的所有servlet实例会被销毁，调用销毁方法
    3)通过案例我们发现:
        -Servlet实例tomcat只会创建一个,所有的请求都是这个实例去相应.
        -默认情况下，第一次请求时，tomcat才回去实例化，初始化，然后再服务.
        这样的好处是什么？提高系统的启动速度.
        这样的缺点时什么？第一次请求时,耗时较长。
        -因此得出结论：如果需要提高系统的启动速度，当前默认情况就是这样；如果需要提高响应速度，我们应该设置Servlet的初始化时机。
    4)Servlet的初始化时机
        -默认时第一次接收请求时，实例化，初始化
        -我们可以通过<load-on-startup>来设置servlet启动的先后顺序，数字越小，启动越靠前，最小值0
    5)Servlet在容器中是：单例的、线程不安全的
         - 单例：所有的请求都是同一个实例去响应
         - 线程不安全：一个线程需要根据这个实例中的某个成员变量值去做逻辑判断。但是在中间某个时机，另一个线程改变了这个成员变量的值，从而导致了第一个线程的执行路径发生了变化
         - 我们已经知道了Servlet是线程不安全的，给我们的启发是：尽量不要在Servlet中定义成员变量，
         如果不得不定义成员变量，那么不要去①不要去修改成员变量的值，②不要去根据成员变量的值做逻辑判断。

4.Http协议
    1)Http称之为 超文本传输协议
    2)Http是无状态的
    3)Http请求响应包含两个部分：请求和响应
    -请求：
        请求包含三个部分：1.请求行；2.请求消息头; 3.请求主体;
        1）请求行包含三个信息：1.请求的方式;2.请求的URL（地址）;3.请求的协议（一般都是HTTP1.1）
        2）请求消息头中包含了很多信息，很多客户端需要告诉服务器的信息，比如：我的浏览器型号、版本、我能接收的内容的类型、我给你发的内容的类型...
        3）请求体，三种情况：
            get方式，没有请求体，但是有一个叫queryString
            post方式，有请求体，form data
            json格式，有请求体,request payload
    -响应:
        响应也包含三部分：1.响应行；2.响应头；3.响应体
        1)响应行包含三个信息：1.协议；2.响应状态码(200)；3.响应状态(OK)
        2)响应头:包含了服务器的信息；服务器发送给浏览器的信息，比如说（内容的媒体类型、编码、内容长度等）
        3)响应体:响应的实际内容(比如响应add.html页面时，响应的内容就是<html><head><body><form>...)[/note]



```java
//演示Servlet的生命周期
public class Demo02Servlet extends HttpServlet {
    private Demo02Servlet(){
        System.out.println("正在实例化");
    }



    @Override
    public void init() throws ServletException {
        //重写init()方法
        System.out.println("正在初始化...");

    }

    @Override
    protected void service(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        //重写service()方法
        System.out.println("正在服务...");
    }

    @Override
    public void destroy() {

        //重写destroy()方法
        System.out.println("正在销毁...");
    }
}
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    <servlet>
        <servlet-name>Demo01Servlet</servlet-name>
        <servlet-class>com.atguigu.servlets.Demo01Servlet</servlet-class>
        
    </servlet>

    <servlet>
        <servlet-name>Demo02Servlet</servlet-name>
        <servlet-class>com.atguigu.servlets.Demo02Servlet</servlet-class>
        <!--不设置是第一次访问创建，设置了是随容器创建-->
        <load-on-startup>1</load-on-startup><!--数字越小，启动的时间越靠前,经量不要写负数-->

    </servlet>

    <servlet-mapping>
        <servlet-name>Demo01Servlet</servlet-name>
        <url-pattern>/demo01</url-pattern>
    </servlet-mapping>

    <servlet-mapping>
        <servlet-name>Demo02Servlet</servlet-name>
        <url-pattern>/demo02</url-pattern>
    </servlet-mapping>

</web-app>
```


<!--more-->

##会话
笔记：

[note type="info flat"]5.会话
    1)HTTP是无状态的
     -HTTP 无状态：服务器无法判断这两次请求是同一个客户端发过来的，还是不同的客户端发过来的
     -无状态带来的现实问题：第一次请求是添加商品到购物车，第二次请求是结账；如果这两次请求服务器无法区分是同一个用户的，那么就会导致混乱
     -通过会话跟踪技术来解决无状态问题。
    2)会话跟踪技术
    -客户端第一次会话给服务器，服务器获取session,获取不到，则创建新的，然后响应给客户端
    -下次客户端给服务器发送请求时，会把sessionID带给服务器，那么服务器就能获取到了，那么服务器就判断这一次请求和上次某次请求是同一个客户端，从而能够区分开客户端
    -常用的API：
        request.getSession() -> 获取当前的会话，没有则创建一个新的会话
        request.getSession(true) -> 效果和不带参数相同
        request.getSession(false) -> 获取当前会话，没有则返回null，不会创建新的

        session.getId() -> 获取sessionID
        session.isNew() -> 判断当前session是否是新的
        session.getMaxInactiveInterval() ->session的非激活间隔时长，默认1800秒
        session.setMaxInactiveInterval()
        session.invalidate() ->强制性让会话立即失效
        ....

    3) session保存作用域
     - session保存作用域是和具体的某一个session对应的
     - 常用的API：
      void session.setAttribute(k,v)
      Object session.getAttribute(k)
      void removeAttribute(k)
[/note]

![4.png][4]
![5.png][5]

```java
//演示向HttpSession保存数据
public class Demo04Servlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.getSession().setAttribute("uname","lina");
    }
}

```


```java
//演示从HttpSession保存作用域中获取数据
public class Demo05Servlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        Object unameObj = request.getSession().getAttribute("uname");
        System.out.println(unameObj);
    }
}

```

<!--more-->

##服务器内部转发以及客户端重定向

笔记

[note type="info flat"]6.服务器内部转发以及客户端重定向
    1)服务器内部转发:request.getRequestDispatcher("..").forward(request,response);
        -一次请求响应的过程，对于客户端而言，内部经过多少次转发，客户端是不知道的
        -地址栏没有变化
    2)客户端重定向:response.sendRedirect("..");
        -两次请求响应的过程，客户端肯定知道请求url有变化
        -地址栏有变化
[/note]
![reSend8.png][6]
![reSend81.png][7]
```java
//演示服务器端内部转发以及服务器重定向
public class Demo06Servlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("demo06...");

        //服务器端内部转发
        //request.getRequestDispatcher("demo07").forward(request,response);

        //客户端重定向
        response.sendRedirect("demo07");

    }
}
```


```java
public class Demo07Servlet extends HttpServlet {
    @Override
    protected void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        System.out.println("demo07......");

    }
}

```


<!--more-->

[note type="default flat"]review：
1.最初的做法是：一个请求对应一个Servlet，这样存在的问题是servlet太多了
2.把一系列的请求对应一个Servlet，IndexServlet/AddSerlvet/EditServlet/DelServlet/UpdateServlet   -> 合并成FruitServlet
 通过operate的值来决定调用FruitServlet中的哪个方法
 使用的是switch-case

3.在上一个版本中，Servlet中充斥着大量的switch-case，试想一下，随着我们的项目业务规模扩大，那么会有很多的Servlet，也就意味着会有很多的switch-case,这是一种代码冗余
因此，我们在Servlet中使用了反射技术，我们规定operate的值和方法名一致，那么接收到的operate的值是什么就表明我们需要调用对应的方法进行响应，如果找不到对应的方法，则抛出异常。
4.在上一个版本中，我们使用了反射技术，但是其实还是存在一定的问题，每一个Servlet中都有类似反射技术的代码。因此继续抽取，设计了中央控制器类：DispatcherServlet
DispatcherServlet这个类的工作分为两大部分：
    1.根据url定位到能够处理这个请求的controller组件:
    1)从url中提取servletPath: /fruit.do -> fruit
    2)根据fruit找到对应的组件:FruitController，这个对应的依据我们存储在applicationContext.xml中
    <bean id="fruit" class="com.atguigu.fruit.controllers.FruitController/>
    通过DOM技术我们去解析XML文件，在中央控制器中形成一个beanMap容器用来存放所有的Controller组件
    3)根据获取到的operate的值定位到我们FruitController中需要调用的方法

    2.调用Controller组件中的方法：
    1)获取参数
        获取即将要调用的方法的参数签名信息:Parameter[] parameters = method.getParameters();
        通过parameter.getName()获取参数的名称;通过parameter.getType()获取参数的类型
        准备了Object[] parameterValues 这个数组用来存放对应参数的参数值
        另外，我们需要考虑参数的类型问题，需要做类型转换的工作。通过parameter.getType()获取参数的类型

    2)执行方法
        Object returnObj = method.invoke(controllerBean,parameterValues);
    3)视图处理
        String returnStr = (String) returnObj;
        if(returnStr.startWith("redirect:"){
        ...
        }else if....

今日内容：
1.再次学习Servlet的初始化方法
1)Servlet生命周期：实例化，初始化，服务，销毁
2)Servlet中的初始化方法有两个:init(),init(config)
    其中带参数的方法代码如下：
    public void int (ServletConfig config) throws ServletException{
        this.config = config;
        init();
    }
    另外一个无参的init方法如下：
    public void init() throws ServletException{
    }
    如果我们想要在Servlet初始化时做一些准备工作，那么我们可以重写init方法
    我们可以通过如下步骤去获取初始化设置的数据
    -获取Config对象ServletConfig config = getServletConfig();
    -获取初始化参数值:config.getInitParameter(key);
3)在web.xml文件中配置Servlet
    <servlet>
        <servlet-name>Demo01Servlet</servlet-name>
        <servlet-class>com.atguigu.servlet.Demo01Servlet</servlet-class>
        <init-param>
            <param-name>hello</param-name>
            <param-value>world</param-value>
        </init-param>
        <init-param>
            <param-name>uname</param-name>
            <param-value>jim</param-value>
        </init-param>

    </servlet>
    <servlet-mapping>
        <servlet-name>Demo01Servlet</servlet-name>
        <url-pattern>/demo01</url-pattern>
    </servlet-mapping>
4)也可以通过注解的方式进行配置：
    @WebServlet(urlPatterns = {"/demo01"}
            , initParams = {
            @WebInitParam(name = "hello", value = "world"),
            @WebInitParam(name = "uname", value = "jim")
            }
            )


2.学习Servlet中的SerlvetContext和<context-param>
    1)获取ServletContext，有很多方法
    在初始化方法中:ServletContext servletContext = getServletContext();
    在服务方法中也可以通过request对象获取，也可月通过session获取
    req.getServletContext(); req.getSession().getServletContext();


    2)获取初始化值:
    servletContext.getInitParameter();
3.什么是业务层
    1)Model1 和 Model2
        MVC： Model(模型) , View(视图) , Controller(控制器)
        视图层：用于做数据展示以及和用户交互的一个界面
        控制层：能够接收客户端的请求，具体的业务功能还是需要借助于模型组件来完成
        模型层：模型分为很多种：有比较简单的pojo/vo(value object)，有业务模型组件，有数据访问层组件
        1)pojo/vo:值对象
        2)Dao：数据访问对象
        3)BO：业务对象
    2)区分业务对象和数据访问对象：
            1)DAO中的方法都是单精度方法或者称之为细粒度方法。什么叫单精度？一个方法只考虑一个操作，比如添加，那就是insert操作，查询那就是select操作
            2)BO中的方法属于业务方法，而实际的业务方法是比较复杂的，因此业务方法的粒度是比较粗的
            注册这个功能属于业务功能，也就是说注册这个方法属于业务方法。
            那么这个业务方法包含了多个DAO方法。也就是说注册这个功能通过多个Dao方法的组合调用，从而完成注册功能的开发。
        注册：
            1.检查用户名是否以及被注册 -DAO中的select操作
            2.向用户表新增一条新用户记录 -DAO中的insert操作
            3.向用户积分表新增一条记录(新用户默认初始化积分100分) -DAO中的insert操作
            4.向系统消息表新增一条记录(某某某新用户注册了，需要根据通讯录信息向他的联系人推送消息) -DAO中的insert操作
            5.向系统日志表新增一条记录(某用户在某IP在某年某月某日某时某分某秒注册) -DAO中的insert操作
            6...
    3.在库存系统中添加业务层组件[/note]


我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1490751353.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3989129412.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/3510677194.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/1488083738.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/1300203174.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/1712273327.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/3778309894.png