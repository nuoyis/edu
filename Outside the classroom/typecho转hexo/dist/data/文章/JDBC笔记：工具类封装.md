---
title: JDBC笔记：工具类封装
date: 2023-07-12 18:10:00
categories: JDBC
tags: [Java,JDBC优化,工具类封装]
---
基于druid连接池的学习，如果每次都要创建连接池并没有减少麻烦，我们需要封装成一个工具类来彻底优化。


<!--more-->

##工具类封装v1.0
我们封装一个工具类，内部包含连接池对象，同时对外提供连接的方法和回收连接的方法。
总结

[note type="info flat"]    v1.0版本工具类
        内部包含一个连接池对象，并且对外提供获取连接和回收连接方法！

    小建议：
        工具类的方法，推荐写成静态，外部调用会更加方便！
    实现：
    属性 连接池对象 [实例化一次]
         单例模式
         static{
            全局实例化调用一次
         }
    方法
        对外提供连接的方法
        回收外部传入连接的方法[/note]


----------


 [label color="red"]封装流程[/label] 

 1. 创建一个成员属性 [label color="orange"]dataSource[/label] 设定为私有化且静态的，初始化值为null

```java
    private static DataSource dataSource = null;//连接池对象，全局的静态的
```

 2. 书写 [label color="blue"]对外提供连接[/label] 的成员方法，返回值**先设置为null**

```java
    public static Connection getConnection() throws SQLException {

        return  null;
    }

```

 3. 书写 [label color="blue"]对外提供回收[/label] 的成员方法，**无返回值**，有参数列表，方法体只用关闭参数中传递进来的连接池就可

```java
    public static void freeConnnection(Connection connection) throws SQLException {

        connection.close();//连接池的连接，调用close就是回收！
    }

```

 4. 书写一个 [label color="red"]静态代码块[/label] ，置于成员方法上，成员属性下。方法中完成创建连接池对象的流程，创建**Properties**对象，通过类加载器的方式加载**properties文件**，**调用load方法**。
 
```java
public class JdbcUtils {

    private static DataSource dataSource = null;//连接池对象，全局的静态的

    static {
        //初始化连接对象
        Properties properties = new Properties();
        InputStream ips = JdbcUtils.class.getClassLoader().getResourceAsStream("druid.properties");
        try {
            properties.load(ips);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        //实例化连接池
        try {
            dataSource = DruidDataSourceFactory.createDataSource(properties);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }

    }

```

 5. 继续静态代码块，给成员变量dataSource赋值 `DruidDataSourceFactory.createDataSource(properties);` ，修改对外提供连接的方法，把返回值改为 `dataSource.getConnection();` 这样调用方法就可以获取一个连接池了。

```java

    public static Connection getConnection() throws SQLException {

        return  dataSource.getConnection();
    }

```
下面是演示工具类使用案例
![test1.png][1]


<!--more-->
##工具类封装v2.0

 我们每次调用**getConnection**这样就又会使得**事务**中 [label color="green"]Service层[/label] 和 [label color="green"]Dao层[/label] 使用不同连接。我们明确知道当前的Service层和Dao层是**同一线程**，我们能不能再同一个线程中不同位置的方法，获取相同连接，Service层以后就不用再参数列表中传递连接。 
 [label color="red"]考虑事务的情况下！如何一个线程的不同方法获取同一个连接[/label] 
 这里我们是需要使用 [label color="red"]ThreadLocal线程本地变量[/label] 。ThreadLocal可以为同一个线程存储共享变量。
 ThreadLocal用于保存某个线程共享变量，原因是在Java中，每一个线程对象中都有一个 `ThreadLocalMap<ThreadLocal,Object>` ,其key就是一个ThreadLocal，而Object即为该线程的共享变量。而这个map是通过ThreadLocald的 [label color="purple"]set[/label] 和 [label color="purple"]get方法[/label] 操作的。对于同一个static ThreadLocal,不同线程只能从**get，set,remove**自己的变量，而不会影响其他变量。

 1.  [label color="blue"]ThreadLocal对象.get[/label] :获取ThreadLocal中当前线程共享变量的值。

 2.  [label color="blue"]ThreadLocal对象.set[/label] :设置ThreadLocal中当前线程共享变量的值。

 3.  [label color="blue"]ThreadLocal对象.remove[/label] :移除ThreadLocal中当前线程共享变量的值

改写工具类

 1. 全局声明一个线程本地变量

```java
   private static ThreadLocal<Connection> tl = new ThreadLocal<>();
```
 2. **改写**对外提供连接的方法
  - 通过 [label color="red"]get方法[/label] 得到连接
  - 如果是第一次没有的情况判断。如果没有连接池获取，在用 [label color="red"]set方法[/label] 存放到线程本地变量中
  - 返回连接

```java
       //先去查看线程本地变量中是否存在
        Connection connection = tl.get();//通过get方法获取线程本地变量连接

        //第一次没有
        if(connection == null){
            //线程本地变量没有，连接池获取
            connection = dataSource.getConnection();
            //获取出来的连接存入线程本地变量
            tl.set(connection);
        }
        return  connection;
```


 3. **改写**对外提供回收连接的方法
  - **删除**参数列表， [label color="red"]因为get方法和回收方法一定在统一个连接[/label] 
  - 通过 [label color="red"]get方法[/label] 得到连接
  - 判断不是空，那么remove()清空本地变量数据
  -  [label color="red"]事务状态回归，因为连接池可能被开启事务了false，要回到默认的状态[/label] 
  - 回收到连接池


```java
 //不需要传回，因为get方法和回收方法一定在统一个连接
    public static void freeConnnection() throws SQLException {
        Connection connection = tl.get();
        if(connection != null){
            tl.remove();//清空线程本地变量数据
            connection.setAutoCommit(true);//事务状态回归 为什么？因为连接池可能被开启事务了false，要回到默认的状态
            connection.close();//回收到连接池即可
        }

    }
```
最终源码：

```java
public class JdbcUtilsV2 {
    //1.声明一个连接池

    private static DataSource dataSource = null;

    //2.创建一个线程本地变量
    private static ThreadLocal<Connection> tl = new ThreadLocal<>();
    //3.静态代码块实例化连接池对象，同v1.0

    static {
        Properties properties = new Properties();
        InputStream ips = JdbcUtilsV2.class.getClassLoader().getResourceAsStream("druid.properties");
        try {
            properties.load(ips);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try {
            dataSource = DruidDataSourceFactory.createDataSource(properties);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }


    }

    //4.书写对外提供连接的方法
    public static Connection getConnection() throws SQLException {
        Connection connection = tl.get();
        //第一此获取连接池对象的判断
        if (connection == null) {
            connection = dataSource.getConnection();
            tl.set(connection);
        }

        return connection;
    }

    //5.对外回收连接的方法
    public static void freeConnecion() throws SQLException {
        Connection connection = tl.get();
        if(connection != null){
            //把连接从线程本地变量移除
            tl.remove();
            //事务状态回归
            connection.setAutoCommit(true);
            //关闭线程
            connection.close();

        }
    }


}

```



----------
我们重新调整Dao和Service层

 1. 删除Dao层中的创建连接，全部添加 `Connection connection = JdbcUtilsV2.getConnection();` ，并删去参数列表中的connnection。
 2. 在Service中transfer中改写创建连接的方式 ` Connection connection = JdbcUtilsV2.getConnection();` ，并删去参数列表中的connnection， [label color="blue"]finally[/label] 中调用 `JdbcUtilsV2.freeConnnection();`


[note type="primary flat"]在第一次运行Service层中首先会通过工具类找到线程本地变量，返回一个连接并存入线程本地变量；然后设置事务提交变量为false，开启事务。然后执行Dao层的方法，使用的同一个连接。最后执行finally方法回收[/note]
Service层：

```java
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

        Connection connection = JdbcUtilsV2.getConnection();

        try{
            //开启事务，关闭MySQL的自动事务提交
            //关闭事务提交
            connection.setAutoCommit(false);

            //执行数据库动作
            //执行加钱减钱
            bankDao.add(addAccount,money);
            System.out.println("----------------------");
            bankDao.sub(subAccount,money);
            //事务提交
            connection.commit();
        }catch (Exception e){
            //事务回滚
            connection.rollback();
            //我们捕捉异常为了做事务回滚，但是不能隐藏异常信息，我们选择抛出
            //抛出
            throw  e;
        }finally {
            JdbcUtilsV2.freeConnnection();
        }
    }
}

```
Dao层：

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
    public void add(String account, int money) throws Exception {

        Connection connection = JdbcUtilsV2.getConnection();

        //加钱就是所谓的修改
        //3.编写SQL语句结构
        String sql = "update t_bank set money = money + ? where account = ?";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1, money);
        preparedStatement.setObject(2, account);
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
    public void sub(String account, int money) throws Exception {
        Connection connection = JdbcUtilsV2.getConnection();
        //3.编写SQL语句结构
        String sql = "update t_bank set money = money - ? where account = ?";

        //4.创建statement
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        preparedStatement.setObject(1, money);
        preparedStatement.setObject(2, account);
        //6.发送sql语句
        preparedStatement.executeUpdate();

        //7.关闭资源
        preparedStatement.close();
        System.out.println("减钱成功！");

    }
}

```
 [label color="red"]工具类最终写法[/label] 

```java
public class JdbcUtilsV2 {
    //1.声明一个连接池

    private static DataSource dataSource = null;

    //2.创建一个线程本地变量
    private static ThreadLocal<Connection> tl = new ThreadLocal<>();
    //3.静态代码块实例化连接池对象，同v1.0

    static {
        Properties properties = new Properties();
        InputStream ips = JdbcUtilsV2.class.getClassLoader().getResourceAsStream("druid.properties");
        try {
            properties.load(ips);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try {
            dataSource = DruidDataSourceFactory.createDataSource(properties);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }


    }

    //4.书写对外提供连接的方法
    public static Connection getConnection() throws SQLException {
        Connection connection = tl.get();
        //第一此获取连接池对象的判断
        if (connection == null) {
            connection = dataSource.getConnection();
            tl.set(connection);
        }

        return connection;
    }

    //5.对外回收连接的方法
    public static void freeConnecion() throws SQLException {
        Connection connection = tl.get();
        if(connection != null){
            //把连接从线程本地变量移除
            tl.remove();
            //事务状态回归
            connection.setAutoCommit(true);
            //关闭线程
            connection.close();

        }
    }


}

```

<!--more-->

##高级应用层封装
针对于 [label color="blue"]注册驱动[/label] ， [label color="pink"]获取连接[/label] ， [label color="orange"]回收资源[/label] 我们在上面进行了一定程度的**优化**，但是还有剩下其他步骤我们使用 [label color="red"]BaseDao[/label] 再次进行优化。

思路：我们把**增删改查**重复度很高的代码抽取成一个父类**BaseDao**然后父类中添加前面的工具类**JdbcUtilsV2**即可。
 [label color="red"]注意：需要将BaseDao设置为抽象类[/label] ，抽象类可以包含具体的方法实现，子类可以直接继承这些方法，从而避免了代码的重复编写。抽象类的主要目的是为了被子类继承和扩展，而不是被直接使用。
 [label color="red"]我们只需要把封装两类，一类是DQL(查询)语句，一类是非DQL(增删改)语句[/label] 

###非DQL(增删改)语句封装


```java
    /*
    封装简化DQL语句 参数一：sql语句 参数二：可变参数代替占位符 可变参数必须存在参数列表的最后一位
    sql：    带占位符的SQL语句
    params   占位符赋值 注意，传入占位符的值，必须等于SQL语句？位置！
    return   返回影响的行数
    */

    public int executeUpdate(String sql,Object...params) throws SQLException {

        //获取连接
        Connection connection = JdbcUtilsV2.getConnection();//工具类是不捕获异常
        PreparedStatement preparedStatement = connection.prepareStatement(sql);

        //5.占位符赋值
        //可变参数可以当作数组使用
        //从1开始 到params.length的长度
        if(params != null && params.length != 0){
            for (int i = 1; i <= params.length; i++) {
                preparedStatement.setObject(i, params[i-1]);
            }
        }

        //6.发送SQL语句
        //DML类型
        int rows = preparedStatement.executeUpdate();

        preparedStatement.close();

        //是否回收连接，需要考虑是不是事务!
        if (connection.getAutoCommit()) {
            //没有开启事务
            //没有开启事务，正常回收连接，Dao层管
            JdbcUtilsV2.freeConnnection();
        }
        //connection.setAutoCommit(false);//开启事务了，不要管连接即可！业务层处理
        return rows;

    }

```
这里需要注意 `preparedStatement.setObject(i,params[i-1]);`  [label color="red"]赋值i，最后取值要-1.防止越界[/label] 

在对应实现类中，我们需要完成**以下步骤**

 1. 让该类 [label color="red"]继承BaseDao类[/label] ，拥有父类的抽象方法
 2. **保留sql语句**删除jdbc流程中的其他操作
 3. 调用executeUpdate方法传入sql语句，然后盯着**占位符**一个一个给**占位符复制**
 4. 返回int结果

改写后的PSCURDPart部分代码

```java
public class PSCURDPart extends BaseDao {

    @Test
    public void testInsert() throws ClassNotFoundException, SQLException {
        String sql = "insert into t_user(account,password,nickname) values( ? , ? , ? )";
        int i = executeUpdate(sql, "测试333", "3333", "ergouzi");
        System.out.println("i = " + i);//返回影响函数

    }

    @Test
    public void testUpdate() throws ClassNotFoundException, SQLException {

        String sql = "update t_user set nickname = ? where id = ?";
        int rows = executeUpdate(sql, "新的nickname", 3);
    }

    @Test
    public void testDelete() throws ClassNotFoundException, SQLException {
        String sql = "delete from t_user where id = ?";
        int i = executeUpdate(sql, 3);

    }
}
```

----------

###DQL(查询)语句封装

```java
        /*
        非DQL语句封装方法 —>返回值 固定为int
         DQL语句封装方法 —>返回值 是什么类型呢？是某一个类型的实体类集合

                            并不是List<Map> map  key和value自定义！不用先设定好
                                            map  没有数据校验机制
                                            map  不支持反射操作
                            数据库中的数据 -> java实体类
                          table
                             t_user
                             id
                             account
                             password
                             nickname
                          java
                            User
                              id
                             account
                             password
                             nickname
                   表中 -> 一行 -> java类的一个对象 -> 多行 -> List<Java实体类> list;

        DQL -> List<Map> -> 一行 -> map -> List<Map>

        <T> 声明一个方法泛型，不确定类型
                1.确定泛型User.class T = User
                2.要使用反射技术属性赋值,实例化对象装值
        第一个<T>声明一个泛型是<T>
        第二个<T>表示我声明一个集合返回值类型是一个<T>
        第三个<T>用于代表class泛型对应的值
        public <T> List<T> executeQuery(Class<T> clazz,String sql,Object...params){
        //书写反射代码实现具体类
        }
        */
    /*
    
    将查询结果封装到一个实体类集合
    clazz   要接值的实体类集合的模板对象
    sql     查询语句，要求列名或者别名等于实体类的属性名！ u_id as uId -> uId
    params  占位符的值，要和？位置对应传递
    return  查询的实体类集合
    <T>     声明的结果泛型
    
    */
    public <T> List<T> executeQuery(Class<T> clazz, String sql, Object... params) throws SQLException, InstantiationException, IllegalAccessException, NoSuchFieldException {

        //获取连接
        Connection connection = JdbcUtilsV2.getConnection();
        PreparedStatement preparedStatement = connection.prepareStatement(sql);


        //占位符赋值
        //为了程序的兼容性 做一个非空判断
        if (params != null && params.length != 0) {
            for (int i = 1; i <=params.length; i++) {
                preparedStatement.setObject(i,params[i - 1]);
            }
        }
        
        //6.发送SQL语句,返回一个结果集
        ResultSet resultSet = preparedStatement.executeQuery();

        //7.结果及解析

        List<T> list = new ArrayList<>();
        
        //获取列的信息对象
        //metaData装的当前结果集列的信息对象！将列的信息和列的值分开存放（他可以获取列的名称根据下角标，可以获取列的数量）
        ResultSetMetaData metaData = resultSet.getMetaData();
        //获取列的数量
        //有了它以后，我们就可以水平遍历列！
        int columnCount = metaData.getColumnCount();

        while (resultSet.next()) {
            //调用类的无参构造函数实例化对象，所以说类必须要有无参构造
            T t = clazz.newInstance();
            
            //一行数据,对应一个 T 类型对象
            
            //自动遍历列，注意，要从1开始，并且小于等于总列数！
            for (int i = 1; i <= columnCount; i++) {
                //对象的属性值
                Object value = resultSet.getObject(i);
                //获取指定列下角标的列的名称！ResultSetMetaData
                //对象的属性名
                String propertyName = metaData.getColumnLabel(i);//获取i对应列的标识
                
                //反射，给对象的属性值进行赋值
                Field field = clazz.getDeclaredField(propertyName);
                field.setAccessible(true);//属性可以设置，打破private私有化修饰限制
                
                /*
                参数1：要赋值的对象 如果属性是静态，第一个参数可以为空
                参数2：具体的属性值
                */
                
                field.set(t,value);
            }

            //一行数据的所有列全部存到了map中！
            //将map存储到集合中即可
            list.add(t);
        }

        //关闭资源
        resultSet.close();
        preparedStatement.close();
        if(connection.getAutoCommit()){
            //没有事务，可以关闭
            JdbcUtilsV2.freeConnnection();
        }
       
        return list;
    }

```

[note type="info flat"]在项目中我们 [label color="red"]改造JDBC[/label] 需要四步操作

 1. 导入依赖的jar包(配置文件) [label color="blue"]druid和mysql8+驱动[/label] 
 2. 编写配置文件 [label color="blue"]druid.properties[/label] 根据需要去调整对应value值。配置文件必须写在 [label color="red"]src[/label] 下方(类加载器)

```properties
# key = value  => java Properties读取 (key | value)
# durid配置的key固定命名
# druid连接池需要的配置参数,key固定命名
driverClassName=com.mysql.cj.jdbc.Driver
username=root
password=abc123
url=jdbc:mysql:///atguigu
initialSize=5
```

 3. 创建util文件夹，导入 [label color="green"]工具类JdbcUtilsV2[/label] [label color="orange"]BaseDao类[/label]。
 4. 创建dao文件夹，创建 [label color="default"]Dao类[/label] ，针对于**Service层**进行一定的修改，根据参数调**Dao层方法**(没有就**alt+回车**创建)，在 [label color="default"]Dao类[/label] 中写**增删改查**的数据库操作，并且继承 [label color="orange"]BaseDao类[/label]。相当于把 [label color="pink"]Service(业务)层[/label] 的方法全部调 [label color="default"]Dao层[/label] 的实现， [label color="default"]Dao层[/label] 实现**数据库**的操作。 [/note]


我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/582252484.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/2774101646.jpg