---
title: Maven笔记：初步解读pom文件-IDEA集成-添加依赖-依赖继承-项目搭建
date: 2023-07-27 16:27:00
categories: Maven
tags: [IDEA,Maven,pom文件,mavenweb工程,继承依赖,项目搭建]
---
对于Maven核心文件pom初步认知;命令行中使用不方便，我们还是需要放到图形化界面IDEA中来使用。


<!--more-->

##解读pom的xml文件
Maven工程的核心配置文件

```xml
<!--project标签:根标签,表示对当前工程进行配置、管理-->
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <!--modelVersion 标签：从Maven2开始就固定是4.0.0-->
  <!--代表当前pom.xml所采用的标签结构-->
  <modelVersion>4.0.0</modelVersion>

  <!--坐标信息 -->
  <!--groupId 标签：坐标的三个向量之一，代表公司或组织，开发的某一个项目-->
  <groupId>com.atguigu.maven</groupId>
  
  <!--artifactId 标签：坐标向量之一：代表项目下的某一个模块-->
  <artifactId>pro01-maven-java</artifactId>
  
  <!--version标签：坐标向量之一：代表当前模块的版本-->
  <version>1.0-SNAPSHOT</version>
  <!--packaging 标签：打包的方式-->
  <!--取值jar：生成jar包，说明这是一个Java工程-->
  <!--取值war：生成war包，说明这是一个Web工程-->
  <!--取值pom：说明这个工程是用来管理其他工程的工程。将来创建父工程，管理子工程-->
  <packaging>jar</packaging>

  <name>pro01-maven-java</name>
  <!--maven官网地址-->
  <url>http://maven.apache.org</url>

  <!--properties标签：在Maven 中定义属性值；可以是Maven提供，也可以是自己自定义-->
  <properties>
  <!--在构建过程中读取源码使用的字符集，采用UTF-8-->
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>
  <!--dependencies中可以包含好多dependency-->
  <!--dependencies标签：配置具体依赖信息，可以包含多个dependency子标签-->
  <dependencies>
    <!--dependency标签：配置一个具体的依赖信息-->
    <dependency>
      <!--坐标信息：导入哪个jar包,配置他的坐标信息即可-->
	  <groupId>junit</groupId>
      <artifactId>junit</artifactId>
      <version>4.12</version>
	  
      <!--scope(范围)标签：配置当前依赖的范围,对于导入jar包有一定影响-->
	  <scope>test</scope>
    </dependency>
  </dependencies>
</project>

```


----------
##创建父工程(在IDEA中创建Java工程)
各个不同版本的IDEA版本略有差异，高版本自动化程度高一点。
###创建一个Maven工程的步骤
![1.png][1]
###配置本地仓库和本地Maven版本
第一次创建，需要指定配置本地的Meven版本，并指定本地仓库。
最好配全局配置一下，这样很麻烦。
![9.png][2]

![2.png][3]
创建子工程后IDEA会自动添加 [label color="blue"]packaging pom[/label] 
创建子工程之后，在main文件夹中添加java文件夹书写java类
在src下添加test文件夹，测试类。

----------
##三种方式执行Maven命令
###第一种方式：侧边栏Maven单击命令
![3.png][4]
可以执行Maven的一些maven命令
###第二种方式：命令行手动输入
第二种方式的**好处**就是可以**一次性运行多个命令**
![4.png][5]
如果有需要，还可以给命令后面附加参数：
 `mvn clean install -Dmaven.test.skip=true` 可以 [label color="red"]跳过测试[/label] 

```xml
# -D 表示后面要附加命令的参数，字母 D 和后面的参数是紧挨着的，中间没有任何其它字符
# maven.test.skip=true 表示在执行命令的过程中跳过测试
mvn clean install -Dmaven.test.skip=true
```
###命令行环境下运行命令
![5.png][6]


----------
##在IDEA中创建Web工程
我是用的是2022版本，相对于之前版本来说更只能，只需要选择模板创建web工程并补充需要的文件就可以了。
![6.png][7]
![7.png][8]
如果 [label color="blue"]webapp[/label] 没有激活，可以重新添加Web项目，放在对应路径 `\src\main\webapp\` 下就可以了
![8.png][9]

----------
###使用插件快速创建
在学习到ssm整合框架的时候，我知道有一款非常好的插件可以快速搭建web工程
JBLJavaToWeb
![15.png][10]
搜索下载即可
![16.png][11]


----------
##基于**SpringMVC**手动添加web工程
web工程需要在pom文件中添加打包方式为war
![10.png][12]
![11.png][13]
在main路径下添加**webapp**和**web.xml**,先添加webapp
![12.png][14]
注意手动添加web.xml需要调整 [label color="orange"]WEB-INF[/label] 前路径为 `当前工程\src\main\webapp\` 
![13.png][15]
![14.png][16]


----------
##第三方依赖信息
第三方信息如何获取，有两种思路
 - maven提供的查询官网 https://mvnrepository.com
查询需要寻找的依赖jar包，复制依赖就可以
 - maven插件 maven-search
在插件市场中下载安装即可
然后再Tools中找到使用就可以
![17.png][17]



----------
借由SSM框架整合，发现之前学习Maven自己认识到很多地方知识掌握不够全面，针对于本篇Maven，我已经做了一定的修改，但是基于内容，不方便再多添加一篇文章了，所以说补一补之前没有补充完整的地方。


<!--more-->

##依赖继承
我们再当前模块下再创建一个模块，**pom文件**中会自动生成 `<parent>` 指明我们的父工程。子工程的**gv**属性也继承于**父工程**。
如果我们让父工程导入依赖，那么子工程继承后会继承一些并不适用的依赖，导致jar包增大。我们可以让父工程中声明依赖，但是不导入依赖，对应的子工程中使用依赖就导入依赖。
父工程中声明依赖
 [label color="orange"]父工程pom.xml[/label] 

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.atguigu</groupId>
    <artifactId>maven-pom-parent-06</artifactId>
    <version>1.0-SNAPSHOT</version>
    <!--父工程：不打包，也不写代码 ;声明打包方式为pom-->
    <packaging>pom</packaging>
    <modules>
        <module>shop-user</module>
        <module>shop-order</module>
    </modules>

    <!--
    选择该模块作为父工程，父工程主要来做配置的继承信息，父工程中是不写代码的
    -->

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!--声明版本信息-->
    <!--dependencies导入依赖，所有子工程都有相应的依赖-->
    <dependencies></dependencies>

    <!--dependencyManagement 声明依赖信息，不会下载依赖！可以被子工程继承版本号-->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-core</artifactId>
                <version>2.15.2</version>
            </dependency>

            <dependency>
                <groupId>mysql</groupId>
                <artifactId>mysql-connector-java</artifactId>
                <version>8.0.27</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

</project>
```
对应子工程继承后导入需要使用的依赖。
 [label color="orange"]子工程pom.xml[/label] 

```xml
    <!--子工程中想要继承父工程的core信息,子工程中如果还写版本会覆盖-->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-core</artifactId>
        </dependency>
    </dependencies>

```
需要注意的是父工程中只需要声明，所以需要使用 `<dependencyManagement>` 包裹若干个依赖，而不是直接使用`<dependencies>` 。
![18.png][18]

----------
##实战项目搭建
附上视频，提供我的搭建思路

[video title="项目构建思路 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-26%2000-35-46.mkv " container="bg5bjtlc03u" subtitle=" " poster=" "] [/video]


----------


我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1047471532.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3564992635.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/361861843.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/746868720.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/3082518451.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/212024582.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/2933908118.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/721127822.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/07/1797319191.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/08/2278309181.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/100872235.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/3784392431.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/08/3887818874.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/2857784003.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/08/3011238879.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/08/1401810059.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/08/776051616.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/08/3035542563.png