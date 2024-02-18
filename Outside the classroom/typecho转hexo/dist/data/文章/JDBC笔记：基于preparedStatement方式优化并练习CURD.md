---
title: JDBC笔记：基于preparedStatement方式优化并练习CURD
date: 2023-07-11 10:11:00
categories: JDBC
tags: [Java,JDBC,MySQL]
---
通过JDBC从java访问数据库，通过用户在控制台输入数据的方式,查询MySQL数据库中是否有无信息的练习来熟悉**JDBC的操作流程**
 [label color="red"]总结笔记(API)[/label] 

[note type="primary flat"]

 1. 注册驱动​
方案一：调用静态方法，但是会注册两次​
**DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());​**

方案二：反射触发类静态代码块完成一次注册​
**Class.forName(“com.mysql.cj.jdbc.Driver”);​**

 2. 获取连接
**Connection connection = DriverManager.getConnection();**
[label color="blue"]​3 (String url,String user,String password)​ 
2 (String url,Properties info(String user,String password)) ​
1 (String url?user=账号&password=密码)[/label] 
 
 3. 创建statement 
静态    **Statement statement = connection.createStatement();**    

预编译  **PreparedStatement preparedstatement = connection.preparedStatement(SQL语句结构);**

 4. 占位符赋值
**preparedstatement.setObject**  **(参数一：?的位置，从左到右，从1开始；参数二：值)** ;​​

 5. 发送SQL语句，并且获取结果
**int rows = executeUpdate();**//非DQL
**Resultset = executeQuery();**//DQL

 6. 查询结果集解析​

 - 移动光标指向行数据 **next(); 单行：if(next())  多行：while(next())**
 - 获取行的数据即可 **get**类型(**int** 列的下角标,从**1**开始|**int**列的 **label** （别名或者列名）)
 - 获取列的信息**getMetaData()**; 获取一个**ResultsetMetaData**对象，包含的就是列的信息
     [label color="green"]getColumnCount(); | getColumnLebal(index);[/label] 

 7. 关闭资源
  **close();**[/note]


<!--more-->
前提：导入对应jar包
笔记如下：

```java
/*
使用预编译statement完成用户登录
防止注入攻击 | 演示ps的使用流程
*/
public class PSUserLoginPart {
    public static void main(String[] args) throws ClassNotFoundException, SQLException {
        //1.搜集用户信息
        Scanner sc = new Scanner(System.in);
        System.out.println("请输入账号");
        String account = sc.nextLine();
        System.out.println("请输入密码");
        String password = sc.nextLine();

        //2.ps数据库流程
        //1.注册驱动,通过反射技术触发静态代码块，完成一次注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取链接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //DriverManager.getConnection("jdbc:mysql:///atguigu?user=root&password=root");

        /*
        statement
            1.创建statement
            2.拼接SQL语句
            3.发送SQL语句，并且获取返回结果

         preparedstatement
            1.编写SQL语句结果 不包含动态值部分的语句，动态值部分使用占位符？替代 注意：？只能替代动态值
            2.创建preparedstatement，并且传入动态值
            3.动态值 占位符 赋值？ 单独赋值即可
            4.发送SQL语句即可，并获取返回结果
        */

        //3.编写SQL语句结构
        String sql = "select * from t_user where account = ? and password = ?;";//如果没有动态值就不用写？了
        //4.创建预编译的statement并且设置SQL语句结果
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.单独的占位符进行赋值
        /*
        参数1：index 占位符的位置 从左向右数 从1开始 账号 ？1
        参数2：object 占位符的值 可以设置任何类型的数据，避免了我们拼接和类型更加丰富！
        */
        preparedStatement.setObject(1,account);
        preparedStatement.setObject(2,password);

        //6.发送SQL语句，并获取返回结果！executeUpdate非查询 | executeQuery查询
        //statement.executeUpdate | executeQuery(String sql);原先需要传递SQL语句
        //prepareStatement.executeUpdate | executeQuery();不需要传递sql，因为它已经知道语句，知道语句动态值
        ResultSet resultSet = preparedStatement.executeQuery();
        //7.结果集解析

        if(resultSet.next()){
            System.out.println("登陆成功");
        }else {
            System.out.println("登陆失败");
        }
        //8.关闭资源
        resultSet.close();
        preparedStatement.close();
        connection.close();

    }
}

```   
  [label color="blue"]JDBC书写的流程大致如下[/label] 
 - 1.注册驱动
 - 2.获取连接
 - 3.编写SQL语句结果，动态值部分使用？代替
 - 4.创建preparedStatement并且传入SQL语句结构
 - 5.占位符赋值
 - 6.发送SQL语句
 - 7.输出结果
 - 8.关闭资源


<!--more-->

  
我们开始练习**DML增删改查**每一部分
**插入数据：**

```java
    //书写四个测试方法
    //测试方法：public开头，没有返回值,不能有形参列表
    //测试方法需要导入一个junit的测试包,Java自带
    @Test
    public void testInsert() throws ClassNotFoundException, SQLException {
        /*
        t_user表插入一条数据
        account  test
        password test
        nick     二狗子
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu", "root", "abc123");
        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "insert into t_user(account,password,nickname) values( ? , ? , ? )";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1,"test");
        preparedStatement.setObject(2,"test");
        preparedStatement.setObject(3,"二狗子");
        //6.发送SQL语句
        //DML类型
        int rows = preparedStatement.executeUpdate();//返回的是一个行数，如果大于0表示有插入成功
        //7.输出结果
        if(rows > 0){
            System.out.println("数据插入成功");
        }else {
            System.out.println("数据插入失败！");
        }
        //8.关闭资源
        preparedStatement.close();
        connection.close();

    }
```
![1.png][1]
![2.png][2]


----------

**修改数据：**

```java
    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {
        /*
        修改id = 3 的用户昵称 nickname = 三狗子
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");

        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu", "root", "abc123");

        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "update t_user set nickname = ? where id = ?";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        preparedStatement.setObject(1,"三狗子");
        preparedStatement.setObject(2,3);

        //6.发送SQL语句
        int i = preparedStatement.executeUpdate();//还是属于DML操作
        //7.输出结果
        if(i > 0){
            System.out.println("修改成功");
        }else {
            System.out.println("修改失败");
        }

        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }

```
![3.png][3]
![4.png][4]


----------

**删除数据：**

```java
    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {
        /*
        修改id = 3 的用户昵称 nickname = 三狗子
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");

        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu", "root", "abc123");

        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "update t_user set nickname = ? where id = ?";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        preparedStatement.setObject(1,"三狗子");
        preparedStatement.setObject(2,3);

        //6.发送SQL语句
        int i = preparedStatement.executeUpdate();//还是属于DML操作
        //7.输出结果
        if(i > 0){
            System.out.println("修改成功");
        }else {
            System.out.println("修改失败");
        }

        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }

```
![5.png][5]
![6.png][6]

----------

**查询数据：**
 需求：查询所有用户数据，并封装到一个List<Map> list集合中
 [label color="red"]数据库数据给我一个resultSet，作为一个原始封装结果，我在java中用起来不方便，我将它转换成一个java数据结构，考虑一行有多个字段，考虑放到一个Map中，key作为列名，value列的内容作为值。这样我有多个Map，我将每行map放入list中，集合里面放map。最后我们只需要使用List就等同于使用数据库的数据了。[/label] 

初步实现：

```java
    @Test
    public void testSelect() throws Exception {
        Class.forName("com.mysql.cj.jdbc.Driver");//可以抛出最大异常省事
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1/atguigu","root","abc123");
        String sql = "select id,account,passsword,nickname from t_user";
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //省略占位符赋值
        ResultSet resultSet = preparedStatement.executeQuery();
        //优先定义List<Map>集合
        List<Map> list = new ArrayList<>();
        while (resultSet.next()){
            Map map = new HashMap();
            //一行数据对应一个map
            
            //1.纯手动取值！如果修改列名就会变得很麻烦，看起来不太智能
            map.put("id",resultSet.getInt("id"));
            map.put("account",resultSet.getString("account"));
            map.put("password",resultSet.getString("password"));
            map.put("nickname",resultSet.getString("nickname"));
            //一行数据的所有列全部存到了map中！
            //将map存储到集合中即可
            list.add(map);
        }
        System.out.println("list = " + list);//soutv快捷键
        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
```
 [label color="default"]弊端：手动取，写法固定，只能解析当前结构语句。[/label] 

我可以先垂直向下移动遍历while行，移动水平遍历列。如何获取当前一共有多少列的信息呢？
 [label color="red"]优化代码，自动遍历列：[/label] 

```java
    /*
    目标：查询所有用户数据，并封装到一个List<Map> list集合中

    解释：
        行 id account nickname
        行 id account nickname
        行 id account nickname
     数据库 -> resultSet-> java ->一行数据->map(key = 列名，value = 列的内容)-> List<Map> list

     实现思路：
        遍历行数据，一行对应一个map！获取一行的列名和对应的列的属性，装配即可！
        最后将map装到一个集合就可以了！

     难点：
        如何获取列的名称？
    */
    @Test
    public void testSelect() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");//可以抛出最大异常省事
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1/atguigu","root","abc123");
        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "select id,account as ac from t_user";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //省略占位符赋值
        //6.发送SQL语句
        ResultSet resultSet = preparedStatement.executeQuery();//返回一个结果集

        //7.结果及解析
        /*
        回顾：
            resultSet :有行和有列！获取数据的时候，一行一行数据！
                        内部有一个游标，默认指向数据的第一行之前！
                        我们可以利用next()方法移动游标！指向数据行！
                        获取行中列的数据

        */
        //优先定义List<Map>集合
        List<Map> list = new ArrayList<>();

        //获取列的信息对象
        //metaData装的当前结果集列的信息对象！将列的信息和列的值分开存放（他可以获取列的名称根据下角标，可以获取列的数量）
        ResultSetMetaData metaData = resultSet.getMetaData();

        //获取列的数量
        //有了它以后，我们就可以水平遍历列！
        int columnCount = metaData.getColumnCount();

        while (resultSet.next()){
            Map map = new HashMap();
            //一行数据对应一个map
            //自动遍历列，注意，要从1开始，并且小于等于总列数！
            for (int i = 1; i <= columnCount; i++) {
                //获取指定列的下角标的值！resultSet
                Object value = resultSet.getObject(i);
                //key是列名，这里不能写死，我们要动态的获取列名

                //获取指定列下角标的列的名称！ResultSetMetaData

                //select * [列名] |xxx_xxx_xxx as name Label以别名优先可以获取到name
                //使用getColumnLabel：会获取列的别名，如果没有写别名才是列的名称 而不要使用 getColumnName：只会获取列的名称
                String columnLabel = metaData.getColumnLabel(i);//获取i对应列的标识

                map.put(columnLabel,value);
                //获取一行然后依次遍历列的顺序
            }

            //一行数据的所有列全部存到了map中！
            //将map存储到集合中即可
            list.add(map);
        }
        //全自动的解析复用性更高，修改查询语句不用调整其他部分，全自动
        System.out.println("list = " + list);//soutv快捷键


        //8.关闭资源
        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
```

![7select.png][7]
 [label color="blue"]这里的ac就是getColumnLabel的作用[/label] 
![7select2.png][8]


----------
源码：

```java
package com.atguigu.api.preparedstatement;

import org.junit.Test;

import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/*
使用preparedstatement进行t_user表的curd动作
*/
public class PSCURDPart {
    //书写四个测试方法
    //测试方法：public开头，没有返回值,不能有形参列表
    //测试方法需要导入一个junit的测试包,Java自带
    @Test
    public void testInsert() throws ClassNotFoundException, SQLException {
        /*
        t_user表插入一条数据
        account  test
        password test
        nick     二狗子
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu", "root", "abc123");
        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "insert into t_user(account,password,nickname) values( ? , ? , ? )";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1,"test");
        preparedStatement.setObject(2,"test");
        preparedStatement.setObject(3,"二狗子");
        //6.发送SQL语句
        //DML类型
        int rows = preparedStatement.executeUpdate();//返回的是一个行数，如果大于0表示有插入成功
        //7.输出结果
        if(rows > 0){
            System.out.println("数据插入成功");
        }else {
            System.out.println("数据插入失败！");
        }
        //8.关闭资源
        preparedStatement.close();
        connection.close();

    }

    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {
        /*
        修改id = 3 的用户昵称 nickname = 三狗子
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");

        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu", "root", "abc123");

        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "update t_user set nickname = ? where id = ?";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        preparedStatement.setObject(1,"三狗子");
        preparedStatement.setObject(2,3);

        //6.发送SQL语句
        int i = preparedStatement.executeUpdate();//还是属于DML操作
        //7.输出结果
        if(i > 0){
            System.out.println("修改成功");
        }else {
            System.out.println("修改失败");
        }

        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }

    @Test
    public void testDelete() throws ClassNotFoundException, SQLException {
        /*
        删除id = 3的用户数据！
        */
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "delete from t_user where id = ?";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        preparedStatement.setObject(1,3);
        //6.发送SQL语句
        int i = preparedStatement.executeUpdate();
        //7.输出结果
        if(i > 0){
            System.out.println("数据删除成功!");
        }else {
            System.out.println("数据删除失败");
        }
        //8.关闭资源
        preparedStatement.close();
        connection.close();//从里往外关闭

    }

    /*
    目标：查询所有用户数据，并封装到一个List<Map> list集合中

    解释：
        行 id account nickname
        行 id account nickname
        行 id account nickname
     数据库 -> resultSet-> java ->一行数据->map(key = 列名，value = 列的内容)-> List<Map> list

     实现思路：
        遍历行数据，一行对应一个map！获取一行的列名和对应的列的属性，装配即可！
        最后将map装到一个集合就可以了！

     难点：
        如何获取列的名称？
    */
    @Test
    public void testSelect() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");//可以抛出最大异常省事
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1/atguigu","root","abc123");
        //3.编写SQL语句结果，动态值部分使用？代替
        String sql = "select id,account as ac from t_user";
        //4.创建preparedStatement并且传入SQL语句结构
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //省略占位符赋值
        //6.发送SQL语句
        ResultSet resultSet = preparedStatement.executeQuery();//返回一个结果集

        //7.结果及解析
        /*
        回顾：
            resultSet :有行和有列！获取数据的时候，一行一行数据！
                        内部有一个游标，默认指向数据的第一行之前！
                        我们可以利用next()方法移动游标！指向数据行！
                        获取行中列的数据

        */
        //优先定义List<Map>集合
        List<Map> list = new ArrayList<>();

        //获取列的信息对象
        //metaData装的当前结果集列的信息对象！将列的信息和列的值分开存放（他可以获取列的名称根据下角标，可以获取列的数量）
        ResultSetMetaData metaData = resultSet.getMetaData();

        //获取列的数量
        //有了它以后，我们就可以水平遍历列！
        int columnCount = metaData.getColumnCount();

        while (resultSet.next()){
            Map map = new HashMap();
            //一行数据对应一个map

            //纯手动取值！如果修改列名就会变得很麻烦，看起来不太智能
           /* map.put("id",resultSet.getInt("id"));
            map.put("account",resultSet.getString("account"));
            map.put("password",resultSet.getString("password"));
            map.put("nickname",resultSet.getString("nickname"));*/

            //自动遍历列，注意，要从1开始，并且小于等于总列数！
            for (int i = 1; i <= columnCount; i++) {
                //获取指定列的下角标的值！resultSet
                Object value = resultSet.getObject(i);
                //key是列名，这里不能写死，我们要动态的获取列名

                //获取指定列下角标的列的名称！ResultSetMetaData

                //select * [列名] |xxx_xxx_xxx as name Label以别名优先可以获取到name
                //使用getColumnLabel：会获取列的别名，如果没有写别名才是列的名称 而不要使用 getColumnName：只会获取列的名称
                String columnLabel = metaData.getColumnLabel(i);//获取i对应列的标识

                map.put(columnLabel,value);
                //获取一行然后依次遍历列的顺序
            }

            //一行数据的所有列全部存到了map中！
            //将map存储到集合中即可
            list.add(map);
        }
        //全自动的解析复用性更高，修改查询语句不用调整其他部分，全自动
        System.out.println("list = " + list);//soutv快捷键


        //8.关闭资源
        resultSet.close();
        preparedStatement.close();
        connection.close();
    }
}

```


我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/2574405311.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3999367774.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/3667933217.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/1879435667.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/626169612.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/832397666.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/52180107.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/4272701474.png