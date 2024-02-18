---
title: JDBC笔记：Druid连接池技术
date: 2023-07-12 15:03:00
categories: JDBC
tags: [Java,JDBC优化,国货之光Druid]
---
 每次都使用DriverManager获取新连接，用完直接抛弃断开，连接的利用率太低；对于服务器来说压力太大了，数据库服务器和Java程序对连接数也无法控制，很容易导致数据库服务器崩溃。
 我们可以建立一个**连接池**，连接池是一套Java提供的标准，在Javax.sql.DataSource接口，规范了连接池获取连接的方法，也规范了连接池回收的方法。 [label color="red"]所有连接池获取连接的和回收连接方法都一样[/label] ，不同的有性能和扩展性能。在许多连接池中，我们考虑性能，扩展性选择了Druid。


<!--more-->

导入druid工具类jar包

采用**硬编码**方式在后期程序启动之后无法修改，采用**软编码**的方式在外部写一个 [label color="orange"]配置文件properties[/label] ，声明配置信息，读取配置文件创建连接池对象。好处就是： [label color="blue"]程序运行起来以后我们通过修改外部配置文件进而影响连接池相关属性[/label] 

首先我们需要书写一个配置文件以druid.properties命名，properties是map的形式存放数据

```other
# key = value ->被java中Properties读取(key | value)
#druid配置的key必须固定命名
driverClassName=com.mysql.cj.jdbc.Driver
username=root
password=abc123
url=jdbc:mysql://127.0.0.1/atguigu
```
通过软编码的形式获取连接池Druid

```java
    //采取软编码的方式，外部书写一个配置文件，后缀名必须是properties
    /*
    通过读取外部配置文件的方法，实例化druid连接池对象
    */
    @Test
    public void testSoft() throws Exception {
        //1.读取外部配置文件到   Properties
        Properties properties = new Properties();
        //src下的文件可以使用类加载器提供的方法
        InputStream ips = DruidUsePart.class.getClassLoader().getResourceAsStream("druid.properties");//在其它文件夹下面前面需要指明路径
        properties.load(ips);
        //2.使用连接池工具类的工厂模式,创建连接池
        DataSource dataSource = DruidDataSourceFactory.createDataSource(properties);
        Connection connection = dataSource.getConnection();

        //数据库curd

        connection.close();

    }
```
翻看DruidDataSourceFactory源码
![originalCode.png][1]
底层会拿到我们的**配置文件，固定读取，然后设置成对应的值**，这就是为什么配置文件中的**key必须固定命名**的原因。
 [label color="red"]通过load方法读取配置文件有两种方式[/label] 

 -  [label color="pink"]通过传递一个文件输入流的方式读取文件[/label] 
 -  [label color="pink"]通过类加载器指定文件夹下的文件[/label] 

后期会把连接池**封装**到类里，我们通过**工具类**只创建一遍连接池就可以了。


----------
源码：
Properties配置文件

```other
# key = value ->被java中Properties读取(key | value)
#druid配置的key必须固定命名
driverClassName=com.mysql.cj.jdbc.Driver
username=root
password=abc123
url=jdbc:mysql://127.0.0.1/atguigu
initialSize=5
```
DruidUsePart类

```java
/*
druid连接池实用类
*/
public class DruidUsePart {
    /*
    直接使用代码设置连接池连接参数方式！
    1.创建一个druid连接池对象
    2.设置连接池参数[ 必须 | 非必须 ]
    3.获取连接[通用方法，所有连接池都一样]
    4.回收连接[通用方法，所有连接池都一样]
    */
    public  void testHard() throws SQLException {
        //连接池对象，实现了java接口
        DruidDataSource dataSource = new DruidDataSource();
        //2.设置参数
        //必须 连接数据库驱动类的全限定符 [注册驱动]| url | user | password |
        //非必须 初始化连接数量，最大的连接数量....
        dataSource.setUrl("jdbc:mysql://localhost:3306/atguigu");
        dataSource.setUsername("root");
        dataSource.setPassword("abc123");
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");//帮助我们进行驱动注册和获取连接
        //非必须
        dataSource.setInitialSize(5);//初始化连接数量
        dataSource.setMaxActive(10);//如果初始化不够，最大到多少
        //获取连接
        Connection connection = dataSource.getConnection();//返回的是一个包装的connection，我们可以用Connection接收

        //数据库curd

        //回收连接
        connection.close();//连接池提供的连接，close，就是回收连接!


    }

    //采取软编码的方式，外部书写一个配置文件，后缀名必须是properties
    /*
    通过读取外部配置文件的方法，实例化druid连接池对象
    */
    @Test
    public void testSoft() throws Exception {
        //1.读取外部配置文件到   Properties
        Properties properties = new Properties();
        //src下的文件可以使用类加载器提供的方法
        InputStream ips = DruidUsePart.class.getClassLoader().getResourceAsStream("druid.properties");//在其它文件夹下面前面需要指明路径
        properties.load(ips);
        //2.使用连接池工具类的工厂模式,创建连接池
        DataSource dataSource = DruidDataSourceFactory.createDataSource(properties);
        Connection connection = dataSource.getConnection();

        //数据库curd

        connection.close();


    }


}

```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/2377366985.png