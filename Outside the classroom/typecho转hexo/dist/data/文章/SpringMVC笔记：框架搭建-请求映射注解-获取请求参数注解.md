---
title: SpringMVC笔记：框架搭建-请求映射注解-获取请求参数注解
date: 2023-08-08 09:14:00
categories: SpringMVC
tags: [springMVC,框架搭建,@RequestMapping注解,请求参数注解]
---
基于SpingMVC的学习笔记，包括框架的基本搭建，请求于请求映射，还有请求参数的注解，以及通过过滤器解决了乱码问题。

> 2023/11/29 更新@RequestParam解释

<!--more-->
##配置web.xml
手动创建maven工程的操作在[基于SpringMVC手动添加web工程中][1]
添加之后我们需要配置SpringMVC的web.xml
有关servlet配置可以查看[让请求对应类的配置][2]
如果使用JDK17+Tomcat8要注意导入mvc为5.3.17(之前我使用5.3.1报错，我在这里找了好久问题，还换了一个模块重写。。)

```xml
        <!-- SpringMVC -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>5.3.17</version>
        </dependency>
```
采用**默认的配置方式**需要放在WEBINF下，位置默认，名称默认，这样不好，学完maven工程应该统一将文件放在resources文件下.
web.xml
```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <!--配置springMVC的前端控制器，对浏览器发送的请求进行统一处理-->
    <!--<servlet>里面<servlet-name>和<servlet-mapping>里面的<servlet-name>保持一致-->
    <servlet>
        <servlet-name>SpringMVC</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>

    </servlet>
    <servlet-mapping>
        <servlet-name>SpringMVC</servlet-name>
        <!--对浏览器发送的请求进行统一处理，不能乱写，写对应的处理请求
        /   (斜线)表示当前浏览器发送的所有请求，但是不包括.jsp的请求路径
        为什么不能匹配.jsp的请求路径？
        .jsp的本质其实就是一个servlet，需要经过当前服务器中特殊的servlet(指定的)来处理，
        不需要当前DispatcherServlet来处理，所以不需要处理。
        如果所写可以收到.jsp请求出现的问题就是.jsp请求也会被SpringMVC进行处理，SpringMVC就会把他当成普通的请求来处理，
        而不会找到相对应的jsp页面，再访问jsp页面就找不到了
        写/目的就是排除.jsp请求，其他请求都要交给前端控制器处理
        如果是/*代表了也是所有请求,包括.jsp请求路径？
        -->
        <url-pattern>/</url-pattern>
    </servlet-mapping>
    
</web-app>
```
###扩展配置方式

对web.xml进行扩展配置
```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

    <!--配置springMVC的前端控制器，对浏览器发送的请求进行统一处理-->
    <!--<servlet>里面<servlet-name>和<servlet-mapping>里面的<servlet-name>保持一致-->
    <servlet>
        <servlet-name>SpringMVC</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <!--添加<init-param>标签，初始化参数，伴随当前servlet的初始化来初始化的-->
        <!--配置SpringMVC配置文件的位置和名称-->
        <init-param>
            <!--contextConfigLocation上下文配置路径-->
            <param-name>contextConfigLocation</param-name>
            <!--param-value设置两个内容，位置名称-->
            <!--classpath:对应类路径resources-->
            <param-value>classpath:springMVC.xml</param-value>
        </init-param>
        <!--servlet第一次访问会初始化,初始化中会执行很多内容，都放在第一次访问.会严重影响第一次访问的速度,
        添加标签<load-on-startup>将SpringMVC的前端控制器DispatcherServlet初始化时间提前到服务器启动时
        -->
        <!--将前端控制器DispatcherServlet初始化时间提前到服务器启动时-->
        <load-on-startup>1</load-on-startup>


    </servlet>
    <servlet-mapping>
        <servlet-name>SpringMVC</servlet-name>
        <!--对浏览器发送的请求进行统一处理，不能乱写，写对应的处理请求
        /   (斜线)表示当前浏览器发送的所有请求，但是不包括.jsp的请求路径
        为什么不能匹配.jsp的请求路径？
        .jsp的本质其实就是一个servlet，需要经过当前服务器中特殊的servlet(指定的)来处理，
        不需要当前DispatcherServlet来处理，所以不需要处理。
        如果所写可以收到.jsp请求出现的问题就是.jsp请求也会被SpringMVC进行处理，SpringMVC就会把他当成普通的请求来处理，
        而不会找到相对应的jsp页面，再访问jsp页面就找不到了
        写/目的就是排除.jsp请求，其他请求都要交给前端控制器处理
        如果是/*代表了也是所有请求,包括.jsp请求路径？
        -->
        <url-pattern>/</url-pattern>
    </servlet-mapping>

</web-app>
```

实际上添加了一个 `<init-param>` 和 `<load-on-startup>` 

开启组件扫描
![1.png][3]
SpringMVC还有一个**Thymeleaf视图解析器**，负责视图跳转。
springMVC.xml配置文件配置

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--扫描组件-->
    <context:component-scan base-package="com.atguigu.mvc.controller"></context:component-scan>

    <!-- 配置Thymeleaf视图解析器 -->
    <bean id="viewResolver" class="org.thymeleaf.spring5.view.ThymeleafViewResolver">
        <!--视图解析器的优先级，如果有多个视图解析器，优先有谁解析-->
        <property name="order" value="1"/>
        <!--解析视图所用编码-->
        <property name="characterEncoding" value="UTF-8"/>
        <!--当前模板-->
        <property name="templateEngine">
            <bean class="org.thymeleaf.spring5.SpringTemplateEngine">
                <property name="templateResolver">
                    <bean class="org.thymeleaf.spring5.templateresolver.SpringResourceTemplateResolver">

                        <!-- 视图前缀 -->
                        <property name="prefix" value="/WEB-INF/templates/"/>

                        <!-- 视图后缀 -->
                        <property name="suffix" value=".html"/>
                        <!--templateMode模板模型-->
                        <property name="templateMode" value="HTML5"/>
                        <!--页面中的编码-->
                        <property name="characterEncoding" value="UTF-8" />
                    </bean>
                    <!--视图解析器，每当我们实现页面跳转，视图名称复合当前条件，就会被视图解析器解析实现页面跳转-->
                </property>
            </bean>
        </property>
    </bean>

</beans>
```


补充HelloController类

```java
/*
SpringMVC不认识
要将当前类作为SpringIoC容器中一个组件的时候进行管理
有两种方式，一种是bean标签配置。第二种注解+扫描
通过注解+扫描的方式配置控制器
注解有四个component controller service repository
表示之后需要扫描才能作为bean进行管理
*/
@Controller
//@ComponentScan
public class HelloController {
    //请求路径
    // "/" -->/WEB-INF/tmplates/index.html

    //控制器里的方法才是处理请求的方法
    //方法名无关，处理请求匹配到这个方法与方法名无关
    //value = / 表示当前文件的上下文路径
    // localhost:8080/springMVC/
    @RequestMapping(value = "/") //请求映射注解，将我们当前的请求和控制器方法床创建对应关系
    public String index() {
        /*
         返回值：返回视图名称，视图名称决定了要跳转的页面，
         因为当前HTML无法直接访问，最终跳转的页面由视图名称决定，
         当我们返回一个视图名称，就会被我们刚配置的视图解析器解析
         在视图解析器中通过加上视图前缀和后缀就是我们最终要访问的页面
         /WEB-INF/tmplates/index.html   去掉视图前缀和后缀
         index
         最后还需要加上注解
         */

        return "index";
        /*
        最后真实情况就是
        @RequestMapping(value = "/")
        当我们浏览器发送的请求是/ ，也就是上下文路径的时候，
        就会执行我们当前注解中所标识的方法，这个方法返回的视图名称index
        被视图解析器解析，加上前后缀就可以跳转到我们的页面
        */

    }
```


 `@RequestMapping(value = "/")` 非常重要，当然里面不只有value这一个属性，除了通过请求地址配置请求控制器方法index之外，我们还可以通过请求方式、请求参数、请求报文等。当然只对value属性赋值的时候也可以省略直接写成`@RequestMapping("/")` 
配置Tomcat访问当前的工程即可。
![2.png][4]
![3.png][5]
访问指定页面
通过index.html访问其他页面的方式。
首先需要添加一个thymeleaf渲染的超链接标签

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>首页</title>
</head>
<body>
<h1>首页</h1>
<!--这里单独写/target对应的就是localhost:8080/target
    是没有上下文路径的所以说要修改成 /springMVC(我的Tomcat中配置的上下文路径)/target
    这样路径相对来说写死了，不好修改，使用thymeleaf修改
    通过thymeleaf解析某一个属性，我们可以在属性前加上th:
    th:href="@{/target(绝对路径)}"          th:href="@{绝对路径}"
    这个时候检测到使用的是一个绝对路径，它可以帮助我们添加上下文路径
-->
<a th:href="@{/target}">访问目标页面target.html</a>

</body>
</html>
```
然后创建一个target.html在HelloController类中实现跳转的方法即可。

```java
    /*
    想要跳转到target.html控制台中处理，写对应的方法
    和方法名无关，但是起的时候最好见名知意
    */
    @RequestMapping("/target")
    public String toTarget(){
        /*
        返回值：视图名称
        视图名称就是去掉 视图前缀，和 视图后缀 剩下的部分
        视图名称会被视图解析器解析
        最后加上注解@RequestMapping
        value值一定要和当前请求地址(<a th:href="@{/target}">访问目标页面target.html</a>)
        保持一致    /target
        */
        return "target";
    }

```
###总结
![4.png][6]

----------
##搭建框架(☆)
快速搭建一个springMVC框架的流程
![5.png][7]
相关依赖(pom文件)
```xml
    <dependencies>
        <!-- SpringMVC -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>5.3.17</version>
        </dependency>
        <!-- 日志 -->
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
        </dependency>
        <!-- ServletAPI -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>
        <!-- Spring5和Thymeleaf整合包 -->
        <dependency>
            <groupId>org.thymeleaf</groupId>
            <artifactId>thymeleaf-spring5</artifactId>
            <version>3.0.12.RELEASE</version>
        </dependency>
    </dependencies>

```

 - 这依赖相对来说写的比较简单，在之后的学习中发现了并不完善补充在这里，主要是添加了package，可以在maven中重新打包项目

```xml
    <dependencies>
        <!-- SpringMVC -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>5.3.17</version>
        </dependency>
        <!-- 日志 -->
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>1.2.3</version>
        </dependency>
        <!-- ServletAPI -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>3.1.0</version>
            <scope>provided</scope>
        </dependency>
        <!-- Spring5和Thymeleaf整合包 -->
        <dependency>
            <groupId>org.thymeleaf</groupId>
            <artifactId>thymeleaf-spring5</artifactId>
            <version>3.0.12.RELEASE</version>
        </dependency>

        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.12.1</version>
        </dependency>


        <dependency>
            <groupId>commons-fileupload</groupId>
            <artifactId>commons-fileupload</artifactId>
            <version>1.3.1</version>
        </dependency>

    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.2.0</version>

                <!--要在下面添加以下配置-->
                <configuration>
                    <failOnMissingWebXml>false</failOnMissingWebXml>
                </configuration>

            </plugin>
        </plugins>
    </build>
```


在main路径下部署webapp文件中的web.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    
    <!--注册前端控制器DispatcherServlet-->
    <servlet>
        <servlet-name>DispatcherServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springMVC.xml</param-value>
        </init-param>
        <load-on-startup>1</load-on-startup>
    </servlet>

    <servlet-mapping>
        <servlet-name>DispatcherServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
    
</web-app>
```
 `<param-value>classpath:springMVC.xml</param-value>` <param-value>中指定了对应初始化的对应文件springMVC.xml,在**类路径**下寻找，所以说在**resources**中创建。
 `<load-on-startup>1</load-on-startup>` 将控制器DispatcherServlet初始化时间提前到服务器启动时候，这样**大大加快第一次请求执行速度**。
为了处理[乱码问题][8]，我们需要为xml添加一部分内容，让它更加完善。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">

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

    <!--配置MVC的前端控制器DispatcherServlet-->
    <servlet>
        <servlet-name>DispatcherServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <!--如果这样配置MVC是有默认的位置和名称，要想自定义位置和名称，设置初始化参数<init-param>-->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springMVC.xml</param-value>
        </init-param>
        <!--将DispatcherServlet初始化时间提前服务器启动时-->
        <load-on-startup>1</load-on-startup>
    </servlet>
    

    <servlet-mapping>
        <servlet-name>DispatcherServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>


</web-app>
```
###一个标配的web.xml的写法
所谓标配就是，配置两个过滤器+一个前端控制器
在学习到MVC后面之后，最固定的还需要加上一个 [label color="blue"]HiddenHttpMethodFilter[/label] 过滤器，调整编码顺序，这是web.xml的固定写法。**web.xml**应该这样书写才完整。


```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
         version="4.0">
    
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
    
    <!--配置MVC的前端控制器DispatcherServlet-->
    <servlet>
        <servlet-name>DispatcherServlet</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <!--如果这样配置MVC是有默认的位置和名称，要想自定义位置和名称，设置初始化参数<init-param>-->
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:springMVC.xml</param-value>
        </init-param>
        <!--将DispatcherServlet初始化时间提前服务器启动时-->
        <load-on-startup>1</load-on-startup>
    </servlet>


    <servlet-mapping>
        <servlet-name>DispatcherServlet</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
    
</web-app>
```
###配置springMVC.xml
一会我们需要创建控制层，对应添加**@Controller注解**，有注解就需要在springMVC.xml文件中开启自动扫描的功能，需要修改**包的位置**，对应的包就是控制类的前一层。
我们写@(四个)注解就需要对应开启**多个自动扫描**，而开启多个自动扫描需要使用**,(逗号)**隔开,如同
 `<context:component-scan base-package="com.atguigu.rest.controller,com.atguigu.rest.dao"></context:component-scan>` 
同时描绘dao层和controller层，当然也可以跳出一层路径如同
 `<context:component-scan base-package="com.atguigu.rest"></context:component-scan>` 
在 [label color="orange"]springMVC.xml[/label] 文件中需要配置context命名空间，添加扫描对应包下的组件，并添加**Thymeleaf**视图解析器。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">


    <!--扫描组件-->
    <context:component-scan base-package="com.atguigu.mvc.controller"></context:component-scan>

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
    
</beans>
```
在后面有视图控制器，对应不添加@RequestMapping注解了，需要配置完整的mvc的命名空间。

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
```
这里只补充命名空间，如果想要看完整的，就跳到[视图控制器][9]去翻看**全部源码**。在我书写[RESTFul案例][10]完后我也发现了更加详细的xml写法，包括一定的静态资源访问和注解驱动，我提供了跳转，也可以参考案例完整的源码。


视图前缀在现有包中不存在，添加一个**templates目录**，并在里面存放对应的**需要渲染的页面(html页面)**index.html

![6.png][11]
index.html

```html
<!DOCTYPE html>
<html lang="en" xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  <h1>首页</h1>

</body>
</html>
```


###创建控制层
现在需要有一个返回**index视图名称**加载当前**templates**中的这个**html文件**。

 `<context:component-scan base-package="com.atguigu.mvc.controller"></context:component-scan>` 没有当前包，在java包下创建对应路径，在Controller层中添加一个控制类(TestController)，添加方法返回对应的视图名称，交给视图解析器渲染。
 [label color="red"]注意：TestController需要添加@Controller注解，控制器是一个普通的类，要想让SpringMVC找到我们的控制器，那么我们的控制器必须是IoC容器中的组件。[/label] 
注意这里的 `@RequestMapping("/")` 之前有注解有解释，对应出来就是上下文路径后面加上的内容**/**

```java
@Controller
public class TestController {

    @RequestMapping("/")
    public String index() {
        return "index";
    }
}

```
基础的框架搭建成功
![7.png][12]


----------

###全注解配置MVC
在学习到后期发现一个MVC实际上没有太固定的格式，每次需要去调整xml文件，每次需要来扩展xml配置文件的内容，以此来达到比较完整的效果，我在后面一篇文章中有提到全注解配置MVC，通过**配置类 + 注解**的形式主要完成了**web.xml**和**springMVC.xml**这两个文件的配置，其中**springMVC.xml**的注解我写的也很详细，里面几乎包含了**所有需要配置的部分**，就算是使用xml文件也可以参考，里面的内容基本不变可能会比上面的注解中的要详细一点，请见谅，[跳转查看][13]。

----------
##@RequestMapping注解
###@RequestMapping注解位置
 - @RequestMapping标识一个类：设置映射请求的请求路径的初始信息
 - @RequestMapping标识一个方法：设置映射请求请求路径的具体信息

```java
@Controller
@RequestMapping("/hello")
public class RequestMappingController {
    /*
    有两个类，都写@RequestMapping("/")，处理的请求地址，请求路径是一样的，
    当前的springMVC就不知道该找谁处理问题了，就会报错
    在我们所有的控制器里面保证@RequestMapping("/")匹配的请求地址是唯一的
    */
/*    @RequestMapping("/")
    public String index() {
        return "target";
    }*/

    /*
    @RequestMapping源码
    @Target({ElementType.TYPE, ElementType.METHOD})表示注解可以使用在类上，方法上
    使用在类上的情况：设置映射请求的请求路径的初始信息
    使用在方法上的情况：设置映射请求请求路径的具体信息.和当前浏览器发送的请求创建关联，来匹配我们浏览器所发送的请求
    如果说一个类中，方法上也有@RequestMapping注解，而类本身也有RequestMapping注解。
    根据对应情况，应该先访问请求路径的初始信息，才能访问到访问具体信息

    */

    @RequestMapping(value = "/testRequestMapping")
    public String success(){
        return "success";
    }

}

```
 [label color="red"]如果说一个类中，方法上也有@RequestMapping注解，而类本身也有RequestMapping注解。     根据对应情况，应该先访问请求路径的初始信息，才能访问到访问具体信息[/label] 
![8.png][14]
 [label color="red"]当前多个控制器中不能有多个@RequestMapping属性(value)注解是一样的!!![/label] 
也就是说**一个请求映射**不能对应**多个控制器**,但是实现这种方法，就需要在不同的控制器(**当前类**上)加上一层路径，再在方法上加一层路径，相当于加一层文件夹，防止文件名冲突。

###@RequestMapping注解的value属性
![9.png][15]

```java
    @RequestMapping(
            /*
            value属性是一个String类型的数组，可以赋给多个值,表示多个请求地址，
            一个请求只会对应一个请求地址
            表示当前请求映射可以处理多个请求，只要请求地址满足其中任何一个，就能让请求映射匹配上*/
            value = {"/testRequestMapping","/test"}
    )
```
[label color="red"]@RequestMapping注解的value属性必须设置，至少通过请求地址匹配请求映射[/label] 
![10.png][16]

----------
###@RequestMapping注解的method属性

```java
    @RequestMapping(
            value = {"/testRequestMapping","/test"},
            /*
            不设置method属性，表明不以请求方式为条件，任何请求方式都可以匹配
            method属性也是一个String(字符串)类型的数组
            一个请求映射可以处理多个请求方式的请求，前提是value必须匹配成功，必须要有value
            会先匹配value属性，然后匹配其他属性
            */
            method = {RequestMethod.GET,RequestMethod.POST} //数组中的方式只要满足其一即可
            //method = {RequestMethod.GET} //  Request method 'POST' not supported 请求方式不被支持不是当前请求映射支持


    )

```
----------

SpringMVC中提供了@RequestMapping的**派生注解**
可以不用设置参数，即添加注解的方式添加。

 - 处理get请求的映射-->@GetMapping
 - 处理post请求的映射-->@PostMapping
 - 处理put请求的映射-->@PutMapping
 - 处理delete请求的映射-->@DeleteMapping


```java
    /*
    只需要设置value属性即可，
    只需要设置value属性，那么可以直接写
    */
    @GetMapping("/testGetMapping")
    public String testGetMapping(){
        return "success";
    }

```
![11.png][17]

----------
###@RequestMapping注解的其他属性
####@RequestMapping注解的params属性

```java
    @RequestMapping(
            value = "/testParamsAndHeaders",
            /*
            "username"当前匹配的请求参数中一定需要username参数 =后面可以设置值(如果加!，表示一定不能是该值)
            "!username"当前匹配的请求参数中一定不需要username参数
             params中所设置的条件必须同时满足
            */
            params = {"username","password=123456"}
    )
    public String testParamsAndHeaders(){
        return "success";
    }

```


```html
   <!--通过(name = value, name=value)传播参数，而？会报红线
        admin是字符串所以说加上''
        thymeleaf会自动解析这个变成一个GET请求
    -->
    <a th:href="@{/testParamsAndHeaders(username='admin',password=123456)}">测试RequestMapping注解的params属性-->testParamsAndHeaders</a>

```

----------
####@RequestMapping注解的headers属性

```java
    @RequestMapping(
            value = "/testParamsAndHeaders",
            params = {"username","password!=123456"},
            /*
            {"header"}
            {"!header"}
            {"header = xxx"}
            {"header != xxx"}
            headers = {"Host=localhost:8080"}表名当前请求头中的一个键值对，表示要求请求映射请求头必须携带Host键值为8081
            */
            headers = {"Host=localhost:8081"}//404
    )
    public String testParamsAndHeaders(){
        return "success";
    }
```

----------
###几种报错情况

 1. **404**：①如果当前请求没有和任何一个Requestmethod和value匹配；②如果请求头信息匹配不成功；
 2. **405**：如果请求方式匹配不了，表明请求方式不被支持。
 3. **400**：如果当前的请求参数匹配不成功。

----------
##MVC支持ant风格的路径
所谓ant风格就是模糊查询，给@RequestMapping传递value值的时候可以使用类似于通配符一样的属性进行路径的分配。

```java
    @RequestMapping("/a?a/testAnt")
    /*只写value表示不通过请求方式，请求头信息，请求参数进行匹配。
    只会根据请求地址匹配

    ?可以表示任意的单个字符,必须要有任意的单个字符(/ ? 除外)
    a?a表示类似于a1a都能匹配这个请求路径

    */
    public String testAnt(){
        return "success";
    }

```
![12.png][18]

 - ？：表示任意的**单个字符**
 - *：表示任意的**0个**或**多个字符**
 - **：表示任意的**一层**或**多层目录**
 [label color="red"]在使用**时，只能使用/**/xxx的方式[/label] 

----------
###MVC路径中占位符赋值(☆)
通过 [label color="blue"]@PathVariable[/label] 注解，简化传参形式，在**RESTful风格**中常用。

```java
    /*
    复制请求地址，表示请求参数里面用大括号表示当前的参数，
    大括号表示路径中的占位符表示路径中的1
    */
    @RequestMapping("/testPath/{id}/{username}")

    public String testPath(@PathVariable("id") Integer id, @PathVariable("username") String username) {
        System.out.println("id:" + id + ",username:" + username);
        /*
        用占位符表示路径中有占位符，请求地址中也必须要有这一层路径
        只能通过@PathVariable注解获取，将我们的占位符代表的值和形参进行绑定
        当我们程序解析之后，就会将我们占位符对应的值复制给它所对应的形参
        */
        return "success";
    }

```
![13.png][19]

----------
##获取请求参数
通过请求映射注解匹配到对应请求，接下来就需要通过请求获取一些参数。

[note type="default flat"]原生servlet中获取请求参数有两种方式：getParameter 来获取请求参数
请求参数如果有多个同名，只能获取第一个。参考复选框
要想获取所有的getParameterValues，返回的是一个字符串类型的数组[/note]
###ServletAPI获取
原生方法，相对麻烦，属于基础

```java
@Controller
public class ParamController {
    //测试获取请求参数功能的类
    /*
    DispatcherServlet里面为我们封装了很多的数据，
    调用我们当前的控制器方法的时候，根据控制器方法参数，来为方法注入参数(赋值)

    */
    @RequestMapping("/testServletAPI")
    //形参位置的request表示当前请求
    public String testServletAPI(HttpServletRequest request){
        /*
        可以直接使用request，为当前参数赋值
        现在DispatcherServlet根据控制器方法注入不一样的值
        如果检测到当前方法形参HttpServletRequest对象，
        将当前DispatcherServlet里面所获得的表示当前请求的request对象复制给形参

        */
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        System.out.println("username:" + username + ",password:" + password);
        return "success";
    }
}
```
![14.png][20]

----------
###控制器方法形参获取请求参数
通过请求中 [label color="blue"]传递参数[/label] ，在对应控制器方法中添加**形参**与 [label color="blue"]请求参数[/label] 保持一致即可。相比于原生Servlet非常方便。

```java
    @RequestMapping("/testParam")
    public String testParam(String username,String password){
        /*
        保证控制器方法的形参和我们当前的请求参数名保持一致
        @{/testParam(username='admin',password=123456)}
        可以自动将我们请求参数赋值给对应形参
        */
        System.out.println("username:" + username + ",password:" + password);
        return "success";
    }

```
![15.png][21]

如果传递过来有多个同名的请求参数，可以使用字符串，也可以使用字符串数组写入形参上。
![16.png][22]

```java
    @RequestMapping("/testParam")
    public String testParam(String username, String password, String[] hobby) {
        /*
        多个同名的请求参数如何获取，复选框模拟
        如果在原生Servlet中需要使用getParameterValues返回字符串数组来获取全部信息
        如果使用getParameter只会获取到第一个值信息
        SpringMVC中也可以使用一个字符串类型的数组来获取，放在形参上
        */
        //若请求参数中出现多个请求参数，可以在控制器方法的形参位置设置字符串类型，或字符串数组来接受此请求参数
        //若使用字符串类型的形参，最终结果为请求参数的每一个值之间使用逗号(,)进行拼接的结果
        System.out.println("username:" + username + ",password:" + password + ",hobby:" + Arrays.toString(hobby));
        return "success";
    }

```
![17.png][23]


----------
###@RequestParam
控制器方法的形参和我们当前的请求参数名不一致，可以通过注解@RequestParam来关联。
简单来说@RequestParam为我们的请求参数和控制器方法的形参创建映射关系。
**意思就是谁给我传递的是username参数，未来我给某个地方发送请求，以我在@RequestParam中规定的名称发送出去。**
**如果我在Controller里面写的@RequestParam注解，代表我需要接收一个user_name名的参数，如果我在Service中使用@RequestParam注解写的代表我要发出的参数叫user_name。一个注解用在两套不同的API上，产生的方式不同**
```java
    @RequestMapping("/testParam")
    public String testParam(
            @RequestParam("user_name") String username,
            String password,
            String[] hobby) {
        System.out.println("username:" + username + ",password:" + password + ",hobby:" + Arrays.toString(hobby));
        /*
        控制器方法的形参和我们当前的请求参数名如果不一致，获取不到数据
        SpringMVC中为我们提供请求参数的注解@RequestParam()括号里书写对应的请求参数
        @RequestParam()注解中有个方法required
        自动装配设置成true的时候找不到就报错，false的时候找不到就用默认值给赋值
        required指明@RequestParam请求参数是必须传输的，如果不传输就会报错400默认值为true.
        */

        return "success";
    }
```
![18.png][24]

[note type="info flat"]@RequestParam注解中的required()默认值为true，如同[Spring自动装配][25]的设置一样，指明了括号中必须传递参数，如果没有参数传递，默认报错**400**。而如果required()修改为**false**，如同 `@RequestParam(value = "user_name" ,required = false) String username` 可以**不用传递，不会报错**，没有值情况下设置**null**(默认值)。[/note]

[note type="primary flat"]@RequestParam注解中还有一个参数就是**defaultValue**，不管**required**的属性值为**true**还是**false**。defaultValue设置了一个初始值，可以减少判断或者三元运算符。有了这个注解，可以解决**请求参数**和**形参**之间的关系，也可以在**没有传递**的情况下，或者**传递空字符串**的情况下，来设置默认值。
[/note]
![19.png][26]

----------
###@RequestHeader和@CookieValue
@RequestHeader注解通过处理**请求头信息**和控制器方法形参的创建映射关系
类比于RequestParam，该注解属性值也有三个**value,required,defaultValue**。
```java
    @RequestMapping("/testParam")
    public String testParam(
            @RequestParam(value = "user_name", required = false, defaultValue = "hehe") String username,
            String password,
            String[] hobby,
            //通过形参host获取当前请求的请求头信息
            @RequestHeader(value = "Host", required = false, defaultValue ="") String host  //请求头localhost:8080
    ) {
        System.out.println("username:" + username + ",password:" + password + ",hobby:" + Arrays.toString(hobby));
        System.out.println("host = " + host);
        return "success";
    }
```
----------
两种会话技术：**Session**和**Cookie**
session**依赖于**cookie,cookie是客户端的会话技术，而session是服务器端的会话技术

[note type="default flat"]Cookie会话技术，默认的声明周期是浏览器开启到浏览器关闭，只要浏览器不关闭Cookie将一直存在。
在方法中添加 `HttpSession session = request.getSession();` 第一次访问方法，Cookie应该存在于当前的响应报文中。当前第一次执行getSession方法的时候，会先检测一下请求报文中是否会携带JSESSIONID的Cookie。如果没有，说明当前会话是第一次会话，会创建一个HttpSession对象。将Session放在服务器所维护的Map集合中，并且创建一个Cookie，Cookie的键值固定，键是JSESSIONID，值是一个随机序列(和UUID很像)。并且将我们的HttpSession对象存储到我们当前的服务器维护的Map集合中，以及JSESSIONID值(**随机序列**)作为Map集合的键，把**Session对象**作为Map集合的值。存储在服务器内部，再把咱们的Cookie响应到浏览器。所以第一次执行getSession方法的时候，**Cookie会存在于响应报文**中，从此之后将存在于**请求报文**中。[/note]
![20.png][27]
[note type="default flat"]@CookieValue是将cookie数据和控制器方法的形参创建映射关系
@CookieValue注解一共有**三个属性：value、required、defaultValue，用法同@RequestParam**
[/note]

```java
    @RequestMapping("/testParam")
    public String testParam(
            //defaultValue默认值
            @RequestParam(value = "user_name", required = false, defaultValue = "hehe") String username,
            String password,
            String[] hobby,
            //通过形参host获取当前请求的请求头信息
            @RequestHeader(value = "Host", required = false, defaultValue ="") String host  ,
            @CookieValue("JSESSIONID") String JSESSIONID
            //请求头localhost:8080
    ) {
        /*
        保证控制器方法的形参和我们当前的请求参数名保持一致
        @{/testParam(username='admin',password=123456)}
        可以自动将我们请求参数赋值给对应形参
        */
        //若请求参数中出现多个请求参数，可以在控制器方法的形参位置设置字符串类型，或字符串数组来接受此请求参数
        //若使用字符串类型的形参，最终结果为请求参数的每一个值之间使用逗号(,)进行拼接的结果
        System.out.println("username:" + username + ",password:" + password + ",hobby:" + Arrays.toString(hobby));
        System.out.println("host : " + host);
        System.out.println("JSESSIONID : " + JSESSIONID);
        /*
        控制器方法的形参和我们当前的请求参数名如果不一致，获取不到数据
        SpringMVC中为我们提供请求参数的注解@RequestParam()括号里书写对应的请求参数
        @RequestParam()注解中有个方法required
        自动装配设置成true的时候找不到就报错，false的时候找不到就用默认值给赋值
        required指明@RequestParam请求参数是必须传输的，如果不传输就会报错400默认值为true.
        */

        return "success";
    }
```
![21.png][28]

----------
###通过实体类(POJO)获取请求参数
数据库同样对应实体类对象，在页面中添加的数据跟实体类添加的属性也是对应的。
直接在形参位置书写一个实体形参，保证请求参数的名字和实体类对象的属性名保持一致，就可以自动通过实体类对象收集请求参数。
User类

```java
public class User {
    private Integer id;
    private String username;
    private String password;
    private Integer age;
    private String sex;
    private String email;

    /*
    通过反射创建一个类，默认使用无参构造，建议生成有参构造的同时加上无参构造
    这里使用PTG插件一键生成
    */
    public User() {
    }

    public User(Integer id, String username, String password, Integer age, String sex, String email) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.age = age;
        this.sex = sex;
        this.email = email;
    }

    /**
     * 获取
     * @return id
     */
    public Integer getId() {
        return id;
    }

    /**
     * 设置
     * @param id
     */
    public void setId(Integer id) {
        this.id = id;
    }

    /**
     * 获取
     * @return username
     */
    public String getUsername() {
        return username;
    }

    /**
     * 设置
     * @param username
     */
    public void setUsername(String username) {
        this.username = username;
    }

    /**
     * 获取
     * @return password
     */
    public String getPassword() {
        return password;
    }

    /**
     * 设置
     * @param password
     */
    public void setPassword(String password) {
        this.password = password;
    }

    /**
     * 获取
     * @return age
     */
    public Integer getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(Integer age) {
        this.age = age;
    }

    /**
     * 获取
     * @return sex
     */
    public String getSex() {
        return sex;
    }

    /**
     * 设置
     * @param sex
     */
    public void setSex(String sex) {
        this.sex = sex;
    }

    /**
     * 获取
     * @return email
     */
    public String getEmail() {
        return email;
    }

    /**
     * 设置
     * @param email
     */
    public void setEmail(String email) {
        this.email = email;
    }

    public String toString() {
        return "User{id = " + id + ", username = " + username + ", password = " + password + ", age = " + age + ", sex = " + sex + ", email = " + email + "}";
    }
}

```
ParamController层

```java
    @RequestMapping("/testBean")
    public String testBean(User user){
        /*
        通过实体类获取参数
        直接通过实体类JavaBean对象(POJO)作为形参
        */
        System.out.println(user);
        return "success";
    }
```
![22.png][29]
####乱码问题
在上面图中的sex性别出现了乱码问题，这里予以解决。
把**设置编码**代码放在具体处理请求的方法中来设置，没有任何效果。
如果设置编码之前已经**获取了某个请求参数**， [label color="red"]获取编码没有任何作用[/label] 。
**获取请求参数出现的乱码问题有两种：**

 - get请求的乱码
如果form表单中将method请求方式修改为get方式，在使用Tomcat8.x情况下，那么不会出现乱码。get请求的乱码实际上是由Tomcat造成的，get请求乱码，需要去找到Tomcat的配置文件，在修改端口号的旁边添加对应属性 `URlEncoding="UTF-8"` 。(Tomcat8.x已经解决了该问题，有需自行百度)
 - post请求的乱码
如果form表单中将method请求方式修改为post方式，出现乱码，此时是真正需要添加**设置编码**的代码。
如果需要设置响应编码，必须在xml文件中添加**<init-param>**给**forceResponseEncoding**传递值true，因为该方法if判断中只有一个。
![23.png][30]
添加**web.xml**中过滤器中添加编码

```xml
    <!--最早初始化的顺序ServletContextListener > Filter > Servlet
    Filter的书写顺序再web.xml中无关
    -->
    <filter>
        <filter-name>CharacterEncodingFilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <init-param>
            <param-name>encoding</param-name>
            <param-value>UTF-8</param-value>
        </init-param>
        <!--手动设置响应编码-->
        <init-param>
            <param-name>forceResponseEncoding</param-name>
            <param-value>true</param-value>
        </init-param>
    </filter>
    <filter-mapping>
        <filter-name>CharacterEncodingFilter</filter-name>
        <!--/* 表示所有请求。所有请求都有可能是post方式发送-->
        <url-pattern>/*</url-pattern>
    </filter-mapping>

```
翻看参考的**CharacterEncodingFilter源码的关键过滤方法**我也放这里

```java
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        String encoding = this.getEncoding();
        if (encoding != null) {
            if (this.isForceRequestEncoding() || request.getCharacterEncoding() == null) {
                request.setCharacterEncoding(encoding);
            }

            if (this.isForceResponseEncoding()) {
                response.setCharacterEncoding(encoding);
            }
        }

        filterChain.doFilter(request, response);
    }
```
![24.png][31]

----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://www.kaijavademo.top/171.html
  [2]: https://www.kaijavademo.top/85.html#cl-1
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/2039007525.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/193349230.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/835005344.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/1660835224.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/296065269.png
  [8]: https://www.kaijavademo.top/259.html#cl-21
  [9]: https://www.kaijavademo.top/296.html#cl-15
  [10]: https://www.kaijavademo.top/296.html#cl-21
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/2633831878.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/1819397589.png
  [13]: https://www.kaijavademo.top/337.html#cl-18
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/2351037049.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/08/2728393249.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/08/4028891927.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/08/2132184533.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/08/2413538205.png
  [19]: https://img.kaijavademo.top/typecho/uploads/2023/08/4122361827.png
  [20]: https://img.kaijavademo.top/typecho/uploads/2023/08/3359589323.png
  [21]: https://img.kaijavademo.top/typecho/uploads/2023/08/1991250786.png
  [22]: https://img.kaijavademo.top/typecho/uploads/2023/08/1347429620.png
  [23]: https://img.kaijavademo.top/typecho/uploads/2023/08/3988128079.png
  [24]: https://img.kaijavademo.top/typecho/uploads/2023/08/652758874.png
  [25]: https://www.kaijavademo.top/185.html#cl-27
  [26]: https://img.kaijavademo.top/typecho/uploads/2023/08/918990981.png
  [27]: https://img.kaijavademo.top/typecho/uploads/2023/08/3739579996.png
  [28]: https://img.kaijavademo.top/typecho/uploads/2023/08/74078524.png
  [29]: https://img.kaijavademo.top/typecho/uploads/2023/08/82056898.png
  [30]: https://img.kaijavademo.top/typecho/uploads/2023/08/576870474.png
  [31]: https://img.kaijavademo.top/typecho/uploads/2023/08/347660263.png