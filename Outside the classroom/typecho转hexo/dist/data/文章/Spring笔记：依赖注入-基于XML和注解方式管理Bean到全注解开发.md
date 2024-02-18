---
title: Spring笔记：依赖注入-基于XML和注解方式管理Bean到全注解开发
date: 2023-07-29 11:33:00
categories: Spring6
tags: [Java,Maven,Spring6,注解,Bean,XML文件]
---
有关Spring6的学习笔记，从配置XML文件到最后使用全注解开发。


<!--more-->

[note type="primary flat"]IoC 是 Inversion of Control 的简写，译为“控制反转”.是一种设计思想，并不是一种技术。

Spring 通过 IoC 容器来管理

所有 Java 对象的实例化和初始化，控制对象与对象之间的依赖关系。

我们将由 IoC 容器管理的 Java 对象称为 Spring Bean，它与使用关键字 new 创建的 Java 对象没有任何区别。

对象从创建到销毁过程都是通过容器来管理的
容器放bean对象，使用map集合，存放方便。

在xml配置文件中定义相应的Bean信息BeanDefinition，通过接口BeanDefinitionReader读取加载,放入IoC容器中，存储Bean定义信息。
在IoC容器中实例化Bean的定义信息(当然这个信息可以修改)，创建通过BeanFactory工厂(模式) + 反射，目前(实例化)是一个空对象，然后进行初始化才可以使用。
通过context.getBean();可以使用。

依赖注入：

- 指Spring创建对象的过程中，将对象依赖属性通过配置进行注入

依赖注入常见的实现方式包括两种：

- 第一种：set注入
- 第二种：构造注入

Bean管理说的是：Bean对象的创建，以及Bean对象中属性的赋值（或者叫做Bean对象之间关系的维护）.
[/note]

##三种方式获取bean对象
获取bean对象前的操作省略，无非就是配置spring依赖，读取xml的配置文件
###方式一：根据id获取bean对象

```java
        //1.根据id获取bean对象
        User user = (User) context.getBean("user");//括号中加上xml文件中配置的id属性值
        System.out.println("1.根据id获取bean:" + user);

```

###方式二：根据类型获取bean对象

```java
        //2.根据类型来获取bean对象
        User user2 = context.getBean(User.class);
        System.out.println("2.根据类型获取bean:" + user2);

```
 [label color="red"]注意：这种方式获取bean，要求IOC容器中指定类型的bean有且只能有一个[/label] 
如果xml配置多个bean，使用这种方式报错。

```xml
    <bean id="user" class="com.atguigu.sping6.iocxml.User"></bean>

    <bean id="user1" class="com.atguigu.sping6.iocxml.User"></bean>
```

![1.png][1]

 - 如果是 [label color="blue"]接口 = 实现类对象[/label] 的形式，根据接口类型可以得到bean对象。
 - 如果一个接口有多个实现类，这些实现类都配置了bean，根据接口类型 [label color="red"]不可以[/label] 获取到bean。因为不唯一，一个接口有多个对象。


###方式三：根据 id + 类型 获取bean对象

```java
        //3.根据id和类型获取bean对象
        User user3 = context.getBean("user", User.class);
        System.out.println("3.根据id和类型:" + user3);

```


----------
##依赖注入
类有属性，创建对象的过程中，向属性(成员变量)设置值，有两种方法

###基于set方法完成注入

 1. **创建类，定义属性，生成属性set方法。**
准备类：

```java
package com.atguigu.sping6.iocxml.di;
public class Book {
    //一会，创建对象中完成属性设置
    private String bname;

    private String author;

    public Book() {
    }

    public Book(String bname, String author) {
        this.bname = bname;
        this.author = author;
    }
    public static void main(String[] args) {

        //set方法注入
        Book book = new Book();
        book.setBname("java");
        book.setAuthor("尚硅谷");

        //通过构造器方法注入
        Book book1 = new Book("C++","尚硅谷");

    }


    /**
     * 设置
     * @param bname
     */
    public void setBname(String bname) {
        this.bname = bname;
    }

    /**
     * 设置
     * @param author
     */
    public void setAuthor(String author) {
        this.author = author;
    }

    /**
     * 获取
     * @return bname
     */
    public String getBname() {
        return bname;
    }

    /**
     * 获取
     * @return author
     */
    public String getAuthor() {
        return author;
    }

    public String toString() {
        return "Book{bname = " + bname + ", author = " + author + "}";
    }
}

```

 2. **在spring的配置文件中配置。（配置对象、注入属性...）**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--基于set方法完成注入-->
    <bean id="book" class="com.atguigu.sping6.iocxml.di.Book">
        <!--name表示set方法后面对应的名字，首字母变成小写，value就是具体设置的值-->
        <property name="bname" value="前端开发"></property>
        <property name="author" value="尚硅谷"></property>
    </bean>
</beans>
```



###基于构造器完成注入

 1. **创建类，定义属性，生成 [label color="red"]有参数的构造方法[/label]** 
准备Book类同上
 2. **spring里面进行配置**

```xml
    <!--2.构造器注入-->
    <!--注意：bean中id唯一-->
    <bean id="bookCon" class="com.atguigu.sping6.iocxml.di.Book">
        <constructor-arg name="bname" value="java开发"></constructor-arg>
        <constructor-arg name="author" value="尚硅谷"></constructor-arg>
        <!--<constructor-arg index="1" value=""></constructor-arg>-->
    </bean>
```


![3.png][2]
实际上我们可以看到他调用的是类的有参构造。


----------
##特殊值处理
###字面量赋值

```xml
<property name="bname" value="前端开发"></property>
```
###null值

```xml
        <!--others成员变量 null值处理-->
        <property name="others">
            <null/>
        </property>
```
###XML实体

```xml
        <!--<>在XML文件中定义标签的，不能随便使用，需要做转义处理
        <   &lt;
        >   &gt;
        -->
        <property name="others" value="&lt;&gt;"></property>
```
###CDATA节

```xml
        <property name="others">
            <!--<![CDATA[]]]通过cdata区表示里面可以包含特殊符号,XML中一种特有的写法-->
            <value><![CDATA[a < b]]></value>
        </property>
```


----------

##特殊属性注入

###对象类型属性注入
####引用外部bean

```xml
    <!--
    第一种方式引入外部bean
        1.创建两个类的对象：dept 和 emp
        2.在员工emp bean标签里面，使用property引入dept的bean
    -->
    <bean id="dept" class="com.atguigu.sping6.iocxml.ditest.Dept">
        <property name="dname" value="安保部"></property>
    </bean>

    <bean id="emp" class="com.atguigu.sping6.iocxml.ditest.Emp">

        <!--普通类型注入-->
        <property name="ename" value="lucy"></property>
        <property name="age" value="50"></property>

        <!--注入对象类型的属性
        private Dept dept;
        -->
        <property name="dept" ref="dept"></property>


    </bean>

```
![4.png][3]


####内部bean

```xml
    <!--第二种方式：内部bean注入-->
    
    <bean id="emp2" class="com.atguigu.sping6.iocxml.ditest.Emp">
        <property name="ename" value="mary"></property>
        <property name="age" value="20"></property>

        <!--使用内部bean方式进行注入-->
        <property name="dept" >
            <bean id="dept2" class="com.atguigu.sping6.iocxml.ditest.Dept">
                <property name="dname" value="财务部"></property>
            </bean>
        </property>

    </bean>
```
![5.png][4]

####级联属性赋值

```xml
    <!--第三种方式:级联赋值-->
    <bean id="dept3" class="com.atguigu.sping6.iocxml.ditest.Dept">
        <property name="dname" value="技术研发部"></property>
    </bean>


    <bean id="emp3" class="com.atguigu.sping6.iocxml.ditest.Emp">
        <property name="ename" value="tom"></property>
        <property name="age" value="30"></property>
        <property name="dept" ref="dept3"></property>
        <property name="dept.dname" value="测试部"></property>
    </bean>
```
相当于emp3 [label color="orange"]bean标签[/label] 中给dept3单独赋值。


----------

##为数组类型属性赋值

```xml
        <!--此处注入数组类型的属性-->
        <property name="loves">
            <array>
                <value>吃饭</value>
                <value>睡觉</value>
                <value>敲代码</value>
            </array>
        </property>
        
```


----------
##为集合类型属性赋值
###List集合属性赋值

```xml
    <bean id="empone" class="com.atguigu.sping6.iocxml.ditest.Emp">
        <property name="ename" value="lucy"></property>
        <property name="age" value="20"></property>
    </bean>

    <bean id="emptwo" class="com.atguigu.sping6.iocxml.ditest.Emp">
        <property name="ename" value="mary"></property>
        <property name="age" value="30"></property>
    </bean>

    <bean id="dept" class="com.atguigu.sping6.iocxml.ditest.Dept">
        <property name="dname" value="技术部"></property>
        <property name="empList">
            <list>
                <!--使用value标签还是ref标签取决于List集合的类型(泛型)-->
                <ref bean="empone"></ref>
                <ref bean="emptwo"></ref>
            </list>

        </property>
    </bean>

```
###Map集合属性赋值

```xml
    <!--
        1.创建两个对象
        2.注入普通类型属性
        3.在学生bean里面注入map集合类型属性

        -->
    <bean id="teacherone" class="com.atguigu.sping6.iocxml.dimap.Teacher">
        <!--注入普通类型属性-->
        <property name="teacherid" value="100"></property>
        <property name="teachername" value="西门讲师"></property>

    </bean>
    <bean id="teachertwo" class="com.atguigu.sping6.iocxml.dimap.Teacher">
        <property name="teacherid" value="200"></property>
        <property name="teachername" value="上官讲师"></property>

    </bean>


    <bean id="student" class="com.atguigu.sping6.iocxml.dimap.Student">
        <!--注入普通类型属性-->
        <property name="sid" value="2000"></property>
        <property name="sname" value="张三"></property>
        <!--在学生bean里面注入map集合类型属性-->
        <property name="teacherMap">
            <map>
                <!--<entry>表示map集合里面的一个键值对-->
                <entry>
                    <!--key-->
                    <key>
                        <value>10010</value>
                    </key>
                    <!--value不是普通值，是一个对象，用ref引入teacher对象-->
                    <ref bean="teacherone"></ref>

                </entry>

                <entry>
                    <key>
                        <value>10086</value>
                    </key>
                    <ref bean="teachertwo"></ref>
                </entry>

            </map>
        </property>

    </bean>
```
###Properties属性赋值
[springMVC中异常处理器提及][5]

----------

##引用bean为集合类型属性赋值

相当于把使用过的集合放在util标签下，需要调整XML配置信息

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/util
       http://www.springframework.org/schema/util/spring-util.xsd
       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

```
**然后使用util标签**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:util="http://www.springframework.org/schema/util"
       xsi:schemaLocation="http://www.springframework.org/schema/util
       http://www.springframework.org/schema/util/spring-util.xsd
       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--
    1.创建3个对象
    2.注入普通类型属性
    3.使用标签 util:类型 定义
    4.在学生bean里面引入util:类型定义bean,完成list,map类型属性注入
     -->

    <bean id="student" class="com.atguigu.sping6.iocxml.dimap.Student">
        <property name="sid" value="10000"></property>
        <property name="sname" value="lucy"></property>
        <!--注入list和map属性-->
        <property name="lessonList" ref="lessonList"></property>
        <property name="teacherMap" ref="teacherMap"></property>

    </bean>

    <util:list id="lessonList">
        <!--设置list定义-->
        <ref bean="lessonone"></ref>
        <ref bean="lessontwo"></ref>
    </util:list>

    <util:map id="teacherMap">
        <!--设置map定义-->
        <entry>
            <key>
                <value>10010</value>
            </key>
            <ref bean="teacherone"></ref>
        </entry>
        <entry>
            <key>
                <value>10086</value>
            </key>
            <ref bean="teachertwo"></ref>
        </entry>


    </util:map>

    <bean id="lessonone" class="com.atguigu.sping6.iocxml.dimap.Lesson">
        <property name="lessonName" value="Java开发"></property>
    </bean>
    <bean id="lessontwo" class="com.atguigu.sping6.iocxml.dimap.Lesson">
        <property name="lessonName" value="前端开发"></property>
    </bean>
    <bean id="teacherone" class="com.atguigu.sping6.iocxml.dimap.Teacher">
        <property name="teacherid" value="100"></property>
        <property name="teachername" value="西门讲师"></property>
    </bean>

    <bean id="teachertwo" class="com.atguigu.sping6.iocxml.dimap.Teacher">
        <property name="teacherid" value="200"></property>
        <property name="teachername" value="欧阳讲师"></property>
    </bean>


</beans>
```
Lesson类:

```java
public class Lesson {
    private String lessonName;


    public Lesson() {
    }

    public Lesson(String lessonName) {
        this.lessonName = lessonName;
    }

    /**
     * 获取
     * @return lessonName
     */
    public String getLessonName() {
        return lessonName;
    }

    /**
     * 设置
     * @param lessonName
     */
    public void setLessonName(String lessonName) {
        this.lessonName = lessonName;
    }

    public String toString() {
        return "Lesson{lessonName = " + lessonName + "}";
    }
}

```
Student类:

```java
public class Student {
    private String sid;
    private String sname;

    private Map<String, Teacher> teacherMap;

    private List<Lesson> lessonList;


    public Student() {
    }

    public Student(String sid, String sname, Map<String, Teacher> teacherMap, List<Lesson> lessonList) {
        this.sid = sid;
        this.sname = sname;
        this.teacherMap = teacherMap;
        this.lessonList = lessonList;
    }

    public void run() {
        System.out.println("学生的编号:" + sid
                + "学生的名称:" + sname);

        System.out.println(teacherMap);
        System.out.println(lessonList);
    }

    /**
     * 获取
     * @return sid
     */
    public String getSid() {
        return sid;
    }

    /**
     * 设置
     * @param sid
     */
    public void setSid(String sid) {
        this.sid = sid;
    }

    /**
     * 获取
     * @return sname
     */
    public String getSname() {
        return sname;
    }

    /**
     * 设置
     * @param sname
     */
    public void setSname(String sname) {
        this.sname = sname;
    }

    /**
     * 获取
     * @return teacherMap
     */
    public Map<String, Teacher> getTeacherMap() {
        return teacherMap;
    }

    /**
     * 设置
     * @param teacherMap
     */
    public void setTeacherMap(Map<String, Teacher> teacherMap) {
        this.teacherMap = teacherMap;
    }

    /**
     * 获取
     * @return lessonList
     */
    public List<Lesson> getLessonList() {
        return lessonList;
    }

    /**
     * 设置
     * @param lessonList
     */
    public void setLessonList(List<Lesson> lessonList) {
        this.lessonList = lessonList;
    }

    public String toString() {
        return "Student{sid = " + sid + ", sname = " + sname + ", teacherMap = " + teacherMap + ", lessonList = " + lessonList + "}";
    }
}

```
Teacher类:

```java
public class Student {
    private String sid;
    private String sname;

    private Map<String, Teacher> teacherMap;

    private List<Lesson> lessonList;


    public Student() {
    }

    public Student(String sid, String sname, Map<String, Teacher> teacherMap, List<Lesson> lessonList) {
        this.sid = sid;
        this.sname = sname;
        this.teacherMap = teacherMap;
        this.lessonList = lessonList;
    }

    public void run() {
        System.out.println("学生的编号:" + sid
                + "学生的名称:" + sname);

        System.out.println(teacherMap);
        System.out.println(lessonList);
    }

    /**
     * 获取
     * @return sid
     */
    public String getSid() {
        return sid;
    }

    /**
     * 设置
     * @param sid
     */
    public void setSid(String sid) {
        this.sid = sid;
    }

    /**
     * 获取
     * @return sname
     */
    public String getSname() {
        return sname;
    }

    /**
     * 设置
     * @param sname
     */
    public void setSname(String sname) {
        this.sname = sname;
    }

    /**
     * 获取
     * @return teacherMap
     */
    public Map<String, Teacher> getTeacherMap() {
        return teacherMap;
    }

    /**
     * 设置
     * @param teacherMap
     */
    public void setTeacherMap(Map<String, Teacher> teacherMap) {
        this.teacherMap = teacherMap;
    }

    /**
     * 获取
     * @return lessonList
     */
    public List<Lesson> getLessonList() {
        return lessonList;
    }

    /**
     * 设置
     * @param lessonList
     */
    public void setLessonList(List<Lesson> lessonList) {
        this.lessonList = lessonList;
    }

    public String toString() {
        return "Student{sid = " + sid + ", sname = " + sname + ", teacherMap = " + teacherMap + ", lessonList = " + lessonList + "}";
    }
}
```
###p命名空间
我们可以添加一个p命名空间
 [label color="red"]准备：[/label] 修改XML配置信息
配置信息中添加一行： `xmlns:p="http://www.springframework.org/schema/p"` 位于 [label color="blue"]schemaLocation[/label] 之上。


[note type="flat"]xmlns:自定义="http://www.springframework.org/schema/自定义"
实际上在配置信息中声明，为了不重复，需要自定义一个名，然后再尾巴路径出修改即可。有点类似于Java的this关键字[/note]

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:util="http://www.springframework.org/schema/util"
       xmlns:p="http://www.springframework.org/schema/p"
       xsi:schemaLocation="http://www.springframework.org/schema/util
       http://www.springframework.org/schema/util/spring-util.xsd
       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--P命名空间注入-->
    <!--准备 xml配置xmlns:p="http://www.springframework.org/schema/p"-->
    <bean id="studentp" class="com.atguigu.sping6.iocxml.dimap.Student"
    p:sid="100" p:sname="mary" p:lessonList-ref="lessonList" p:teacherMap-ref="teacherMap">
    </bean>
```


----------
##引入外部属性文件
 [label color="red"]应用场景：[/label] 在一个文件中我们需要使用很多bean的值注入，要修改维护不方便。实际中把特定的**固定值**放到外部文件中，然后引入外部文件进行注入。这样好处就是只需要修改外部文件，不需要修改spring里面。

 1. 引入数据库相关依赖

```xml
        <!-- MySQL驱动 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.30</version>
        </dependency>
        <!-- 数据源 -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid</artifactId>
            <version>1.2.15</version>
        </dependency>

```


 2. 创建外部配置文件properties,定义数据信息，用户 密码 地址等。
**druid.properties**

```other
driverClassName=com.mysql.cj.jdbc.Driver
username=root
password=abc123
url=jdbc:mysql:///atguigu
initialSize=5
```


 3. 创建spring配置文件，引入context命名空间引入属性文件，使用表达式完成注入
这里的 `location="classpath:druid.properties"` **classpath读取时你自己的配置文件名**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="
       http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd
       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">

    <!--引入外部properties属性文件-->
    <context:property-placeholder location="classpath:druid.properties"></context:property-placeholder>
    
</beans>
```


**使用表达式完成注入**

```xml
    <!--完成数据库信息注入-->
    <bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <!--外部配置文件，根据key value取值-->
        <property name="url" value="${url}"></property>
        <property name="username" value="${username}"></property>
        <property name="password" value="${password}"></property>
        <property name="driverClassName" value="${driverClassName}"></property>
        <property name="initialSize" value="${initialSize}"></property>

    </bean>
```
这里的value值是通过读取properties文件中的key值，拿取对应的value值。
![7.png][6]
好处就是通过spring加载配置文件，而不用工具类或者硬编码的方式写成java程序
![6.png][7]

----------

##bean作用域

取值|含义|获取对象的时机
:--:|:--:|:--:
singleton（默认）|IOC容器中，这个bean的对象始终为单实例|**IOC容器初始化时**
prototype |这个bean在IOC容器中有多个实例|**获取bean时**
![8.png][8]


----------
##Bean的生命周期

 1. bean对象的创建（调用无参数构造）
 2. 给bean设置相关的属性（相关注入）
 3. 调用bean后置处理器（初始化之前）
 4. bean对象的初始化操作（调用指定初始化方法）
 5. 调用bean后置处理器（初始化之后）
 6. bean的对象创建完成了，可以使用了
 7. bean对象销毁（配置指定的销毁方法）
 8. IoC容器最终关闭
![9.png][9]


----------

##自动装配
我们在实际业务中，我们需要Controller层调用Service层的业务，而一个业务对应多个单精度Dao方法，通过自动装配的形式调用。
原生方法：创建Service和Dao的接口，然后创建实现类对象。从Controller层开始一层一层开始通过**多态**创建对象，调用里面方法。
![10.png][10]
###根据类型(byType)完成自动装配

 1. 在**需要调用其他类对象**的类中添加其他类的成员变量，通过变量调用方法
![12.png][11]
 2. 在该类中添加这个成员变量的 [label color="orange"]set方法[/label] 
 3. spring中配置 [label color="red"]autowire[/label] 
![11.png][12]

```xml
    <!--把三个对象创建出来-->
    <bean id="userController" class="com.atguigu.sping6.iocxml.auto.controller.UserController"
          autowire="byType">
    </bean>
    <!--这里需要class是实现类而不是接口-->
    <bean id="userService" class="com.atguigu.sping6.iocxml.auto.service.UserServiceImpl"
          autowire="byType">
    </bean>

    <bean id="userDao" class="com.atguigu.sping6.iocxml.auto.dao.UserDapImpl">
    </bean>

```

[note type="info flat"]**byType**根据类型自动装配，在Controller注入Service，注入类型（byType）找到类型对应的对象(在spring中找)，完成注入。 [label color="red"]需要注意的是接口对应的是实现类的对象必须是单个(单实现)，否则报错[/label] [/note]
###根据名称(byName)完成自动装配
[note type="info flat"]修改autowire就可。根据名称注入，需要保证添加其他类成员变量名要和对应bean标签id一致。[/note]
![13.png][13]

----------
##注解管理Bean(☆)
注解可以是代码中的一种特殊标记
 [label color="red"]格式 @注解名称( 属性名称 = 属性值...)[/label] 
**注解可以使用在类上面，属性上面，方法上面。**
通过注解实现自动装配，**简化SpringXML配置**，实际开发中 [label color="red"]基于注解做实现[/label]。 

###开启组件扫描

 1. 引入相关依赖
 2. 开启组件的扫描
Spring默认不适用注解装配Bean，我们需要在SpingXMl配置信息中开启 [label color="red"]自动扫描功能[/label] 。
添加context空间

```xml
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

```
开启组件扫描， `base-package="com.atguigu"` 会扫描当前包和他的子包下的所有类。
不考虑其他情况完整的XML文件是这样的

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/context
       http://www.springframework.org/schema/context/spring-context.xsd

       http://www.springframework.org/schema/beans
       http://www.springframework.org/schema/beans/spring-beans.xsd">
    <!--开启组件扫描-->
    <context:component-scan base-package="com.atguigu"></context:component-scan>
</beans>
```

还有其他的特殊情况

```xml
    <context:component-scan base-package="com.atguigu.spring6">
        <!--排除哪些内容不进行扫描-->
        <!-- context:exclude-filter标签：指定排除规则 -->
        <!--
        type：设置排除或包含的依据
        type="annotation"，根据注解排除，expression中设置要排除的注解的全类名
        type="assignable"，根据类型排除，expression中设置要排除的类型的全类名
        -->
        <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        <!--<context:exclude-filter type="assignable" expression="com.atguigu.spring6.controller.UserController"/>-->
    </context:component-scan>
    
    <context:component-scan base-package="com.atguigu" use-default-filters="false">
        <!-- context:include-filter标签：指定在原有扫描规则的基础上追加的规则 -->
        <!-- use-default-filters属性：取值false表示关闭默认扫描规则 -->
        <!-- 此时必须设置use-default-filters="false"，因为默认规则即扫描指定包下所有类 -->
        <!--
        type：设置排除或包含的依据
        type="annotation"，根据注解排除，expression中设置要排除的注解的全类名
        type="assignable"，根据类型排除，expression中设置要排除的类型的全类名
        -->
        <context:include-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        <!--<context:include-filter type="assignable" expression="com.atguigu.spring6.controller.UserController"/>-->
    </context:component-scan>
```
###用注解创建bean对象

注解|说明
:--:|:--:|
@Component|普通Bean定义
@Repository|一般用在Dao层
@Service|用在Service层
@Controller|一般用在Web层
![14.png][14]


----------
##@Autowired注入
单独使用@Autowired注解，**默认根据类型装配(byType)**。
流程见自动装配，必须开启**组件扫描**

###属性注入
 1. bean对象创建
 2. 定义相关属性，在属性上面添加注解
![15.png][15]
###set注入
为成员变量定义set方法，位于set方法之上添加注解
![16.png][16]
###构造方法注入
![17.png][17]
###形参上注入
![18.png][18]
###单构造方法省略注解
当类中只有**一个构造方法**的时候，可以 [label color="red"]省略@Autowired不写[/label] 。但是一个类中既有带参数构造，又有无参数构造(构造方法＞1) [label color="red"]报错[/label] 。
![19.png][19]

###@Autowired和@Qualifier通过名称联合注入
@Autowired默认使用类型注入，但是当 [label color="red"]一个接口对应两个或者多个实现类[/label] 的时候，就会报错。
Dao接口对应多个实现类的对象的时候，Service层调Dao层时使用@Autowired就会找到**多个同类型**。
![20.png][20]
此时我们需要 [label color="red"]根据名称注入[/label] ，找到**具体**的某个实现类对象，采取联合注入。
![21.png][21]


----------
##@Resource注入
Resource注解默认**根据名称**装配byName，未指定名称时，使用属性名作为name。通过
name找不到的话会自动启动通过类型byType装配(**下面会有三种方式的诠释**)。其余@Resource与@Autowired区别请自行百度
父工程中导依赖

```xml
<dependency>
<groupId>jakarta.annotation</groupId>
<artifactId>jakarta.annotation-api</artifactId>
<version>2.1.1</version>
</dependency>
```
###指定名称注入
![22.png][22]
###使用属性名称保持一致
不指定Resource用属性名称(成员变量名)进行匹配
![23.png][23]
###根据类型进行匹配
![24.png][24]

----------
##全注解开发
之前spring中添加了一个组件扫描，现在我们不需要书写spring配置文件,直接都用注解方式开发，不再编写任何spring配置文件。
采取 [label color="blue"]配置类[/label] 代替 [label color="orange"]配置文件[/label] ，最终实现全注解开发。

```java
@Configuration //表示一个类是配置类
@ComponentScan("com.atguigu.spring6")//扫描包的路径，和配置文件中组件扫描相同
public class SpringConfig {

}
```
测试类中原先使用
 `ApplicationContext context  = new ClassPathXmlApplicationContext("bean.xml");` 
读取XML配置文件，现在改为
 `ApplicationContext context  = new AnnotationConfigApplicationContext(SpringConfig.class);` 
加载配置类。
![25.png][25]

我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/2999684492.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3047687613.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/2623702920.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/817807502.png
  [5]: https://www.kaijavademo.top/337.html#cl-16
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/1449909810.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/1633520525.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/2112993926.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/07/731702870.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/07/3564155882.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/07/477384899.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/07/737586616.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/07/3278843964.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/07/168941135.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/07/1860917384.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/07/1617669814.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/07/2384114683.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/07/1278224897.png
  [19]: https://img.kaijavademo.top/typecho/uploads/2023/07/3047277108.png
  [20]: https://img.kaijavademo.top/typecho/uploads/2023/07/1590744248.png
  [21]: https://img.kaijavademo.top/typecho/uploads/2023/07/2562692589.png
  [22]: https://img.kaijavademo.top/typecho/uploads/2023/07/1479427709.png
  [23]: https://img.kaijavademo.top/typecho/uploads/2023/07/2192287431.png
  [24]: https://img.kaijavademo.top/typecho/uploads/2023/07/2772173873.png
  [25]: https://img.kaijavademo.top/typecho/uploads/2023/07/3827763530.png