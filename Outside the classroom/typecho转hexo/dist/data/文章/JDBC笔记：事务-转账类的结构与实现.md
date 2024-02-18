---
title: JDBC笔记：事务-转账类的结构与实现
date: 2023-07-11 19:35:00
categories: JDBC
tags: [Java,JDBC,MySQL,JDBC优化]
---
数据库的事务是一种SQL语句可执行的缓存机制，事务允许我们在失败的情况下，让数据回归到业务之前的状态！
 [label color="red"]事务使用场景[/label] 
 [label color="red"]一个业务涉及多条修改数据库语句[/label] 
经典的转账案例，转账业务（加钱和减钱）

 [label color="blue"]事务的特性[/label] (ACID)
 - 原子性,事务是一个不可分割的工作单位，事务中的操作要么都发生，要么都不发生。
 - 一致性,事务必须使数据库从一个一致性状态变换到另外一个一致性状态。
 - 隔离性,并发事务访问的时候事务之间不受其他事务干扰。
 - 持久性,事务一旦提交，真的就会改变数据库数据的一种方式。

 [label color="orange"]事务的类型[/label] 

 - 自动提交:每条语句自动存储在一个事务中，执行成功自动提交，执行失败自动回滚(MySQL)
 - 列表项目:手动开启事物，添加语句，手动提交或手动回滚即可


<!--more-->


在Java中如何使用事务操作？使用try-catch。
通过转账案例演示事务。

**代码结构设计**

 [label color="orange"]测试类[/label] 

[note type="info flat"]BankService业务层
储存t_bank表的业务方法！先设计一个转账业务
成员方法：tansfer(String addAccount,String subAccount,int money) 通过方法调用dao类的加钱和减钱的方法[/note]

[note type="success flat"]BankDao
存储操作t_bank表的方法！通过Dao方法来调用数据库
add(String account,int money)加钱的jdbc动作
sub(String account,int money)减钱的jdbc动作
让业务层调用Dao层的这两个方法就可[/note]

 [label color="blue"]数据库表t_bank[/label] 
通过测试类调用service层然后调用dao层，dao层调用数据库。但是书写代码的时候先书写dao层


----------


先根据这个结构创建出代码
**BankDao类**

```java
/*
    表的数据库方法存储类
*/
public class BankDao {
    /*
    加钱的数据库操作方法(具体的JDBC动作)
    String account 加钱的符号
    int money 加钱的金额
    */
    public void add(String account,int money) throws Exception {
        //加钱就是所谓的修改
        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu?user=root&password=abc123");

        //3.编写SQL语句结构
        String sql = "update t_bank set money = money + ? where account = ?";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1,money);
        preparedStatement.setObject(2,account);
        //6.发送sql语句
        preparedStatement.executeUpdate();

        //7.关闭资源
        preparedStatement.close();
        connection.close();
        System.out.println("加钱成功！");
    }

    /*
    减钱的数据库操作方法(具体的JDBC动作)
    String account 减钱的符号
    int money 减钱的金额
    */
    public void sub(String account,int money) throws  Exception{

            //加钱就是所谓的修改
            //1.注册驱动
            Class.forName("com.mysql.cj.jdbc.Driver");
            //2.获取连接
            Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu?user=root&password=abc123");

            //3.编写SQL语句结构
            String sql = "update t_bank set money = money - ? where account = ?";

            //4.创建statement
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            //5.占位符赋值
            preparedStatement.setObject(1,money);
            preparedStatement.setObject(2,account);
            //6.发送sql语句
            preparedStatement.executeUpdate();

            //7.关闭资源
            preparedStatement.close();
            connection.close();
            System.out.println("减钱成功！");

    }
}

```
BankService类

```java
/*
银行卡业务方法，调用Dao方法
*/
public class BankService {
    @Test
    public void start() throws Exception {
        //直接在测试方法中调用Service层
        //二狗子 给驴蛋蛋转500
        transefer("lvdandan","ergouzi",500);
        //现在我们把减钱独立一个事务中，加钱独立在另一个事务中，它们两互不印象，会出现什么问题呢？


    }



    public void transefer(String addAccount,String subAccount,int money) throws Exception {
        //创建Dao类的对象

        BankDao bankDao = new BankDao();
        //调用里面的两个方法
        bankDao.add(addAccount,money);
        System.out.println("----------------------");
        bankDao.sub(subAccount,money);
    }
}

```
并且我在Service类中书写了一个测试方法，这样等效于书写一个测试类。
这样书写会导致加钱，减钱的方法互相独立，处于两个事务中，我们运行看看会发生什么？
![2.png][1]
![3.png][2]
我们不妨多运行几次看看会发生什么。注意，设计表的时候**account**字段的数据类型是**int unsigned**不可以为负数.
![4.png][3]
![addSuccessful.png][4]
我们发现在多次转账后，二狗子已经没钱了，程序报错，但是驴蛋蛋加钱成功。
查看数据库
![5.png][5]
我们会发现确实只有加钱成功，没有扣钱。
原因就是**出现在两个事务中**
我们之前出现了两个connect连接当然是有一定问题
我们需要调整我们的Service层，因为一个事务是转账，包括了加减钱。事务的开启是在业务层开启的

 1. 我们同时对add和sub方法提供一个连接，抽取 [label color="orange"]注册驱动[/label] 和 [label color="orange"]获取链接[/label] 到Service类中
 2. 然后再**Service**类补充**try-catch**方法
再**try-catch**方法中
 - 开启事务，关闭MySQL的自动事务提交
 - 执行数据库动作，把**Dao**层的加钱减钱方法放入
 - 手动提交
 - catch捕获异常，如果有异常，那么事务回滚
 - 我们对于异常不能隐藏，选择抛出
 - finally中关闭连接
 3. 修改**Dao**层，删除**add**和**sub**中的 [label color="orange"]注册驱动[/label] 和 [label color="orange"]获取连接[/label] ，在参数列表中加入**connection**，并在try中**补充形参**。
Service类

```java
    public void transefer(String addAccount,String subAccount,int money) throws Exception {
        //创建Dao类的对象
        BankDao bankDao = new BankDao();
        //一个事务的最基本要求，必须是同一个链接对象，connection
        //一个转账方法属于一个事务，(加钱 减钱)

        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu?user=root&password=abc123");

        try{
            //开启事务，关闭MySQL的自动事务提交
            //关闭事务提交
            connection.setAutoCommit(false);

            //执行数据库动作
            //执行加钱减钱
            bankDao.add(addAccount,money,connection);
            System.out.println("----------------------");
            bankDao.sub(subAccount,money,connection);
            //事务提交
            connection.commit();
        }catch (Exception e){
            //事务回滚
            connection.rollback();
            //我们捕捉异常为了做事务回滚，但是不能隐藏异常信息，我们选择抛出
            //抛出
            throw  e;
        }finally {
            connection.close();
        }


    }
```
Dao类

```java
public class BankDao {
    /*
    加钱的数据库操作方法(具体的JDBC动作)
    String account 加钱的符号
    int money 加钱的金额
    */
    public void add(String account,int money,Connection connection) throws Exception {
        //加钱就是所谓的修改
        //3.编写SQL语句结构
        String sql = "update t_bank set money = money + ? where account = ?";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1,money);
        preparedStatement.setObject(2,account);
        //6.发送sql语句
        preparedStatement.executeUpdate();

        //7.关闭资源
        preparedStatement.close();

        System.out.println("加钱成功！");
    }

    /*
    减钱的数据库操作方法(具体的JDBC动作)
    String account 减钱的符号
    int money 减钱的金额
    */
    public void sub(String account,int money,Connection connection) throws  Exception{
            //3.编写SQL语句结构
            String sql = "update t_bank set money = money - ? where account = ?";

            //4.创建statement
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            //5.占位符赋值
            preparedStatement.setObject(1,money);
            preparedStatement.setObject(2,account);
            //6.发送sql语句
            preparedStatement.executeUpdate();

            //7.关闭资源
            preparedStatement.close();
            System.out.println("减钱成功！");

    }
}

```
测试一下
![6.png][6]
这里报错后会被catch捕捉到，触发事务回滚
![7.png][7]
我们看见这里就并没有再进行加钱的操作了，这样事务就添加完毕了


----------
源码
Service + 测试类

```java
/*
银行卡业务方法，调用Dao方法
*/
public class BankService {
    @Test
    public void start() throws Exception {
        //直接在测试方法中调用Service层
        //二狗子 给驴蛋蛋转500
        transefer("lvdandan","ergouzi",500);
        //现在我们把减钱独立一个事务中，加钱独立在另一个事务中，它们两互不印象，会出现什么问题呢？


    }

        /*
        事务添加是在业务方法中！
        利用try—catch代码块，开启事务和提交事务，和事务回滚！
        将connection传入dao层即可，而dao只负责使用，不要close();
        */

    public void transefer(String addAccount,String subAccount,int money) throws Exception {
        //创建Dao类的对象
        BankDao bankDao = new BankDao();
        //一个事务的最基本要求，必须是同一个链接对象，connection
        //一个转账方法属于一个事务，(加钱 减钱)

        //1.注册驱动
        Class.forName("com.mysql.cj.jdbc.Driver");
        //2.获取连接
        Connection connection = DriverManager.getConnection("jdbc:mysql:///atguigu?user=root&password=abc123");

        try{
            //开启事务，关闭MySQL的自动事务提交
            //关闭事务提交
            connection.setAutoCommit(false);

            //执行数据库动作
            //执行加钱减钱
            bankDao.add(addAccount,money,connection);
            System.out.println("----------------------");
            bankDao.sub(subAccount,money,connection);
            //事务提交
            connection.commit();
        }catch (Exception e){
            //事务回滚
            connection.rollback();
            //我们捕捉异常为了做事务回滚，但是不能隐藏异常信息，我们选择抛出
            //抛出
            throw  e;
        }finally {
            connection.close();
        }


    }
}

```
Dao 类

```java
/*
    表的数据库方法存储类
*/
public class BankDao {
    /*
    加钱的数据库操作方法(具体的JDBC动作)
    String account 加钱的符号
    int money 加钱的金额
    */
    public void add(String account,int money,Connection connection) throws Exception {
        //加钱就是所谓的修改
        //3.编写SQL语句结构
        String sql = "update t_bank set money = money + ? where account = ?";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1,money);
        preparedStatement.setObject(2,account);
        //6.发送sql语句
        preparedStatement.executeUpdate();

        //7.关闭资源
        preparedStatement.close();

        System.out.println("加钱成功！");
    }

    /*
    减钱的数据库操作方法(具体的JDBC动作)
    String account 减钱的符号
    int money 减钱的金额
    */
    public void sub(String account,int money,Connection connection) throws  Exception{
            //3.编写SQL语句结构
            String sql = "update t_bank set money = money - ? where account = ?";

            //4.创建statement
            PreparedStatement preparedStatement = connection.prepareStatement(sql);

            //5.占位符赋值
            preparedStatement.setObject(1,money);
            preparedStatement.setObject(2,account);
            //6.发送sql语句
            preparedStatement.executeUpdate();

            //7.关闭资源
            preparedStatement.close();
            System.out.println("减钱成功！");

    }
}
```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/2086836999.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/3972218407.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/173766405.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/1874488352.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/2304229231.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/2064173797.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/1245315143.png