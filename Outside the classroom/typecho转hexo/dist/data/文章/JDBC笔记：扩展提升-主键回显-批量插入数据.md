---
title: JDBC笔记：扩展提升-主键回显-批量插入数据
date: 2023-07-11 18:40:00
categories: JDBC
tags: [Java,JDBC,JDBC优化]
---
在有些场景中，我们需要获取数据库自增长的主键，这就是主键回显


<!--more-->
##主键回显



**使用总结**
[label color="red"]1.创建prepareStatement的时候，不光传递对应sql语句，还需告知携带会数据库自增长的主键[/label] 
**(sql, Statement.RETURN_GENERATED_KEYS)** Statement.RETURN_GENERATED_KEYS = 1
[label color="red"]2.获取司机装主键值的结果集对象，一行一列，获取对应的数据即可 [/label] 
 [label color="orange"]在第七步结果集解析中[/label] 
 - 获取装主键的结果集对象
  **ResultSet resultSet = preparedStatement.getGeneratedKeys();**
 - 因为是一行一列，移动一下光标就可
  **resultSet.next();**
 - 取值
  **int id = resultSet.getInt(1);**

![1.png][2]
![2.png][3]
![3.png][4]


----------


源码：

```java
package com.atguigu.api.preparedstatement;

import org.junit.Test;

import java.sql.*;

/*
练习ps的特殊使用情况
*/
public class PSotherpart {

    /*
    需求
    t_user表插入一条数据，并且获取数据库自增长的主键

    使用总结
    1.创建prepareStatement的时候，告知携带会数据库自增长的主键(sql, Statement.RETURN_GENERATED_KEYS) Statement.RETURN_GENERATED_KEYS = 1
    2.获取司机装主键值的结果集对象，一行一列，获取对应的数据即可 ResultSet resultSet = preparedStatement.getGeneratedKeys();
    */
    @Test
    public void  returnPrimaryKey() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //3.编写SQL语句
        String sql = "insert into t_user(account,password,nickname) values(?,?,?);";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
        //5.占位符赋值
        preparedStatement.setObject(1,"test1");
        preparedStatement.setObject(2,"123456");
        preparedStatement.setObject(3,"驴蛋蛋");//盗墓笔记的一只狗
        //6.发送SQL语句，并且获取结果
        int i = preparedStatement.executeUpdate();
        //7.结果集解析
        if(i > 0){
            System.out.println("数据插入成功！");
            //可以获取回显的主键
            //获取司机装主键的结果集对象， 一行一列  id = 值
            ResultSet resultSet = preparedStatement.getGeneratedKeys();

            resultSet.next();//移动下光标！

            int id = resultSet.getInt(1);//取值

            System.out.println("id = " + id);
        }else {
            System.out.println("数据插入失败");
        }
        //8.关闭资源
        preparedStatement.close();
        connection.close();


    }
}

```


<!--more-->
##批量数据插入优化

我们使用普通方法插入10000条数据

```java
    /*
    使用普通的方式插入10000条数据
    */
    @Test
    public void  testInsert() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //3.编写SQL语句
        String sql = "insert into t_user(account,password,nickname) values(?,?,?);";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //执行前后获取时间差
        long start = System.currentTimeMillis();
        //遍历
        for (int i = 0; i < 10000; i++) {
            preparedStatement.setObject(1,"dd" + i);
            preparedStatement.setObject(2,"dd" + i);
            preparedStatement.setObject(3,"驴蛋蛋" + i);
            //6.发送SQL语句，并且获取结果
            preparedStatement.executeUpdate();
        }

        long end = System.currentTimeMillis();

        //7.结果集解析
        System.out.println("执行10000次数据插入消耗的时间:" + (end - start));//计算毫秒值就可以了
        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }

```
结果

![insert1.png][5]

 [label color="blue"]使用批量插入的方式插入10000条数据[/label] 
   总结**批量插入**：
 1. 路径后面添加 [label color="pink"]?rewriteBatchedStatements=true [/label] 允许批量插入
 2. insert into语句后面 values [必须写] 语句不能添加分号 [label color="red"];[/label] 结束
 3. 不是执行语句每条，是批量添加  [label color="orange"]addBatch()[/label] 
 4. 遍历添加完毕以后，统一批量执行 [label color="orange"]executeBatch()[/label] 


```java
   @Test
    public void  testBatchInsert() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        //需要让对应MySQL支持这样的效果
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu?rewriteBatchedStatements=true", "root", "abc123");
        //3.编写SQL语句
        //批量插入这里一定要写values
        String sql = "insert into t_user(account,password,nickname) values(?,?,?)";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //执行前后获取时间差
        long start = System.currentTimeMillis();
        //遍历
        for (int i = 0; i < 10000; i++) {
            preparedStatement.setObject(1,"ddd" + i);
            preparedStatement.setObject(2,"ddd" + i);
            preparedStatement.setObject(3,"驴蛋蛋" + i);


            preparedStatement.addBatch();//不执行，追加到values后面！

        }
        preparedStatement.executeBatch();//执行批量操作！上方批量添加完毕后统一执行


        long end = System.currentTimeMillis();

        //7.结果集解析 普通插入：6729
        System.out.println("执行10000次数据插入消耗的时间:" + (end - start));//计算毫秒值就可以了
        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }


```
结果，批量插入数据速度提升明显
![insert2优化.png][6]


----------


源码：

```java
package com.atguigu.api.preparedstatement;

import org.junit.Test;

import java.sql.*;

/*
练习ps的特殊使用情况
*/
public class PSotherpart {

    /*
    需求
    t_user表插入一条数据，并且获取数据库自增长的主键

    使用总结
    1.创建prepareStatement的时候，告知携带会数据库自增长的主键(sql, Statement.RETURN_GENERATED_KEYS) Statement.RETURN_GENERATED_KEYS = 1
    2.获取司机装主键值的结果集对象，一行一列，获取对应的数据即可 ResultSet resultSet = preparedStatement.getGeneratedKeys();
    */
    @Test
    public void  returnPrimaryKey() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //3.编写SQL语句
        String sql = "insert into t_user(account,password,nickname) values(?,?,?);";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);
        //5.占位符赋值
        preparedStatement.setObject(1,"test1");
        preparedStatement.setObject(2,"123456");
        preparedStatement.setObject(3,"驴蛋蛋");//盗墓笔记的一只狗
        //6.发送SQL语句，并且获取结果
        int i = preparedStatement.executeUpdate();
        //7.结果集解析
        if(i > 0){
            System.out.println("数据插入成功！");
            //可以获取回显的主键
            //获取司机装主键的结果集对象， 一行一列  id = 值
            ResultSet resultSet = preparedStatement.getGeneratedKeys();

            resultSet.next();//移动下光标！

            int id = resultSet.getInt(1);//取值

            System.out.println("id = " + id);
        }else {
            System.out.println("数据插入失败");
        }
        //8.关闭资源
        preparedStatement.close();
        connection.close();


    }

    /*
    使用普通的方式插入10000条数据
    */
    @Test
    public void  testInsert() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu", "root", "abc123");
        //3.编写SQL语句
        String sql = "insert into t_user(account,password,nickname) values(?,?,?);";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //执行前后获取时间差
        long start = System.currentTimeMillis();
        //遍历
        for (int i = 0; i < 10000; i++) {
            preparedStatement.setObject(1,"dd" + i);
            preparedStatement.setObject(2,"dd" + i);
            preparedStatement.setObject(3,"驴蛋蛋" + i);
            //6.发送SQL语句，并且获取结果
            preparedStatement.executeUpdate();
        }

        long end = System.currentTimeMillis();

        //7.结果集解析 普通插入：6729
        System.out.println("执行10000次数据插入消耗的时间:" + (end - start));//计算毫秒值就可以了
        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }

   /*
   使用批量插入的方式插入10000条数据
   总结批量插入：
    1.路径后面添加?rewriteBatchedStatements=true 允许批量插入
    2.insert into语句后面 values [必须写] 语句不能添加分号;结束
    3.不是执行语句每条，是批量添加 addBatch();
    4.遍历添加完毕以后，统一批量执行executeBatch()
  */
    @Test
    public void  testBatchInsert() throws Exception {
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        //需要让对应MySQL支持这样的效果
        Connection connection = DriverManager.getConnection("jdbc:mysql://127.0.0.1:3306/atguigu?rewriteBatchedStatements=true", "root", "abc123");
        //3.编写SQL语句
        //批量插入这里一定要写values
        String sql = "insert into t_user(account,password,nickname) values(?,?,?)";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);
        //5.占位符赋值
        //执行前后获取时间差
        long start = System.currentTimeMillis();
        //遍历
        for (int i = 0; i < 10000; i++) {
            preparedStatement.setObject(1,"ddd" + i);
            preparedStatement.setObject(2,"ddd" + i);
            preparedStatement.setObject(3,"驴蛋蛋" + i);


            preparedStatement.addBatch();//不执行，追加到values后面！

        }
        preparedStatement.executeBatch();//执行批量操作！上方批量添加完毕后统一执行


        long end = System.currentTimeMillis();

        //7.结果集解析 普通插入：6729
        System.out.println("执行10000次数据插入消耗的时间:" + (end - start));//计算毫秒值就可以了
        //8.关闭资源
        preparedStatement.close();
        connection.close();
    }



}

```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1518042219.jpg
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/2603553294.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/2286831324.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/456104891.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/1005317150.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/2940871438.png