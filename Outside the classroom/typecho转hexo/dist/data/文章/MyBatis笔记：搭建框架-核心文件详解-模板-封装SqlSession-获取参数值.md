---
title: MyBatis笔记：搭建框架-核心文件详解-模板-封装SqlSession-获取参数值
date: 2023-08-20 15:51:00
categories: MyBatis
tags: [工具类封装,MyBatis,SqlSession,核心文件解读,获取参数]
---
作为java最流行的持久层技术，即学习完JDBC之后的另一门技术，以轻量级和性能出色的半自动成为了核心三大技术SSM中的之一。
本篇文章是基于Mybatis的基础学习，包括框架的搭建，优化，还有工具类的封装和模板的添加。

<!--more-->

##搭建MyBatis

 - 在pom依赖文件中添加打包方式为**jar**包
 `    <packaging>jar</packaging>` 
 - 在依赖文件中导入依赖
因为我的SQL版本是8+版本，所以导入对应版本的依赖,并添加log4j的日志文件(下面的文章中有提及，引入依赖还需要导入配置文件xml在resources下)


```xml
    <dependencies>
        <!-- Mybatis核心 -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>3.5.7</version>
        </dependency>
        <!-- junit测试 -->
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
            <scope>test</scope>
        </dependency>
        <!-- MySQL驱动 -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.30</version>
        </dependency>

        <!-- log4j日志 -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>

    </dependencies>
```

###核心配置文件

 - 创建核心配置文件

对于一个框架，本质上来说就是 [label color="blue"]jar包 + 配置文件[/label] 
文件没有默认的名字，但是建议是**mybatis-config.xml**,在整合SSM后，核心文件可以写可以不写，之后会交给Spring管理。
 [label color="orange"]mybatis-config.xml[/label] ，核心配置文件应该创建在**resources**下

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!--xml文件都有的内容，声明版本号，和编码-->

<!--mybatis中的文件约束 configuration根标签-->
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--配置连接数据库的环境-->
    <environments default="development">
        <environment id="development">
            <!--设置事务管理器的类型是JDBC-->
            <transactionManager type="JDBC"/>
            <!--事务管理方式，以最原始的JDBC的方式管理，
            事务的提交回滚都需要手动处理-->
            <!--数据库连接池进行保存，下次在使用缓存中取-->
            <dataSource type="POOLED">
                <!--输入链接库中的信息-->
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/mybatis"/>
                <property name="username" value="root"/>
                <property name="password" value="abc123"/>
            </dataSource>
        </environment>
    </environments>
    <!--映入映射文件-->
    <mappers>
        <mapper resource="org/mybatis/example/BlogMapper.xml"/>
    </mappers>
</configuration>
```
###创建mapper接口(实现添加功能)
Mybatis中的mapper接口相当于之前的DAO，以前的DAO有接口和实现类，而mapper只需要一个接口就可以，所谓面向接口编程。当我们通过mybatis中的方式去mapper创建接口对象，调用接口中的方法，就可以对应某个SQL语句。在接口中只需要添加操作数据库的方法即可。

我们可以创建mapper接口，同DAO的命名，参考数据库表和实体类命名。

![1.png][1]
###映射文件
尽量和我们的mapper接口名保持一致，只不过是一个xml文件。

 - 一个DAO类对应一个数据库表，一个mapper对应一个数据库表，一个mapper的映射文件对应一个mapper。
 [label color="red"]MyBatis面向接口编程的两个一致：通过Mapper接口对应映射文件[/label] 
 1. 映射文件的namespace要和mapper接口的全类名保持一致
 2. 映射文件中SQL语句的id要和mapper接口中的方法名一致
UserMapper.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.atguigu.mybatis.mapper.UserMapper">
    <!--创建映射关系，namespace要和mapper接口的全类名保持一致 -->

    <!--int insertUser();-->
    <insert id="insertUser">
        <!-- id作为唯一标识，方法名和SQL语句的id一致,在标签体中添加SQL语句 -->
        insert into t_user values(null,'admin','123456',23,'男','12345@qq.com')
    </insert>

</mapper>
```
UserMapper接口

```java
public interface UserMapper {

    /**
        MyBatis面向接口编程的两个一致：通过Mapper接口对应映射文件
        1.映射文件的namespace要和mapper接口的全类名保持一致
        2.映射文件中SQL语句的id要和mapper接口中的方法名一致

     一个表 --- 实体类 --- mapper接口 --- 映射文件
     */

     /*
     添加用户信息
     */
    public abstract  int insertUser();
}
```

修改核心配置文件**mybatis-config.xml**与对于**配置文件**产生关系
 `<mapper resource="mappers/UserMapper.xml"/>` 
![2.png][2]
在测试类中测试
###使用SQL在测试类中流程

```java
    @Test
    public void testMyBatis() throws IOException {
        /*MyBatis为我们提供了一个数据库的操作对象SqlSessionFactoryBuilder*/
        //通过字节/字符输入流加载核心配置文件
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        //获取SqlSessionFactoryBuilder
        SqlSessionFactoryBuilder sqlSessionFactoryBuilder = new SqlSessionFactoryBuilder();
        //获取sqlSessionFactoryBuilder的工厂对象,使用工厂模式
        SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(is);
        //获取SqlSession,代表Java程序和数据库之间的会话
        SqlSession sqlSession = sqlSessionFactory.openSession();
        //获取mapper接口对象。而现在mapper只有接口，如何获取实现类对象？
        /*当我们传递进入一个类的class的对象，方法将获取该类型的实例化对象
         getMapper底层帮助我们创建了该接口的实现类，并且返回了接口实现类对象
         使用的是代理模式，帮助我们返回一个接口的实现类对象
         */
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);

        //测试功能
        int result = mapper.insertUser();
        System.out.println("result = " + result);//result = 1   受影响的行数是1

        //根据配置文件中事务管理方式，需要手动设置提交事务
        sqlSession.commit();
        
    }
```
###框架优化
 - 每次实现增删改查的时候都需要手动提交事务显得比较麻烦，可以把事务的提交设置成自动的。JDBC中事务就是自动提交，如果需要手动管理，才会关闭。
 `SqlSession sqlSession = sqlSessionFactory.openSession(true);` 

 - 添加日志功能
使用的是 [label color="blue"]log4j[/label] ，添加依赖
pom.xml

```xml
<!-- log4j日志 -->
        <dependency>
            <groupId>log4j</groupId>
            <artifactId>log4j</artifactId>
            <version>1.2.17</version>
        </dependency>

```
添加配置文件
log4j的配置文件名固定，大多数日志配置文件名都是固定的
log4j.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE log4j:configuration SYSTEM "log4j.dtd">
<log4j:configuration xmlns:log4j="http://jakarta.apache.org/log4j/">
    <appender name="STDOUT" class="org.apache.log4j.ConsoleAppender">
        <param name="Encoding" value="UTF-8" />
        <layout class="org.apache.log4j.PatternLayout">
            <param name="ConversionPattern" value="%-5p %d{MM-dd HH:mm:ss,SSS}
%m (%F:%L) \n" />
        </layout>
    </appender>
    <logger name="java.sql">
        <level value="debug" />
    </logger>
    <logger name="org.apache.ibatis">
        <!---->
        <level value="info" />
    </logger>
    <root>
        <level value="debug" />
        <appender-ref ref="STDOUT" />
    </root>
</log4j:configuration>
```

[note type="default flat"]日志的级别
FATAL(致命)>ERROR(错误)>WARN(警告)>INFO(信息)>DEBUG(调试)
从左到右级别**越来越低**，日志级别越高，输出信息越少；日志级别越低，输出信息越多；所选用的日志文件的级别**输出信息≥本身级别信息**。[/note]


----------
##设置配置模板
###配置核心配置文件的模板
通过设置**IDEA配置模板**的方式，可以增加我们开发的效率，不用每次核心配置文件去官方文档中或者是笔记里cv。
spring-config.xml模板内容

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--引入对应配置文件properties-->
    <properties resource="jdbc.properties"/>
    <!--以包为单位添加类型别名-->
    <typeAliases>
        <package name=""/>
    </typeAliases>
    <!--连接数据库的环境-->
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
    </environments>
    <!--以包为单位映入映射文件-->
    <mappers>
        <package name=""/>
    </mappers>
</configuration>
```
![4.png][3]
###创建映射文件模板
mybatis-mapper.xml模板内容
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper
        PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!--命名空间namespace和某一个接口的全类名保持一致-->
<mapper namespace="">
    <!--添加SQL语句，和接口中的方法对应-->
    
</mapper>
```
以上两种模板在添加完成之后，以后的操作中只需要**添加文件名**，并在模板中补充对应的*自定义*的部分，附一张文件的存放位置。
![5.png][4]


----------
##修改和删除功能
在上面框架搭建过程中以及实现了**添加功能**，可以翻看。
实际上我们书写增删改最好都使用这样的流程
 1. 在接口(UserMapper)中添加对应抽象方法。

```java
    /*
    修改用户信息
    返回值可以写int 也可以不用传递返回值
     */

    public abstract void updateUser();

    /*
    删除用户信息*/
    public abstract void deleteUser();


```

 2. 复制返回值+方法名，在xml文件中添加注释并书写sql语句
UserMapper.xml

```xml
    <!--void updateUser();-->
    <update id="updateUser">
        update t_user set username = '张三' where id = 4
    </update>

    <!--void deleteUser();-->
    <delete id="deleteUser">
        delete from t_user where id = 5
    </delete>
```

 3. 书写对应的测试类/类，创建对象，调用对应方法。

```java
    @Test
    public void testCRUD() throws IOException {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
        SqlSession sqlSession = sqlSessionFactory.openSession(true);
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        //修改功能
        //mapper.updateUser();

        //删除功能
        mapper.deleteUser();

    }
```

----------
##查询功能
查询功能不像是增删改，返回值固定。查询必定有返回值，考虑查询结果是什么？是一条数据，还是多条数据的实体类对象集合？单行单列？...
###查询一条数据|多条数据
一条数据对应实体类对象，多条数据对应实体类集合
UserMapper接口
```java
    /*
    根据id查询用户信息
    */
    public abstract User getUserById();

    /*查询所有的用户信息*/
    public abstract List<User> getAllUser();

```
UserMapper.xml
```xml
    <!--User getUserById();
    查询功能的标签必须设置resultType或resultMap
    resultType:设置默认的映射关系：
    设置实体类类型，就会自动把查询出来的结果的字段名作为属性名赋值
    resultMap:设置自定义的映射关系：
    如果字段名和属性名不一致的情况，需要使用(多对一 一对多)

    我们需要指定数据所对应的结果类型，必须要设置
    将查询出来的结果转换成实体类对象返回
    -->
    <select id="getUserById" resultType="com.atguigu.mybatis.pojo.User">
        select * from t_user where id = 3
    </select>

    <!--List<User> getAllUser();-->
    <select id="getAllUser" resultType="com.atguigu.mybatis.pojo.User">
        select * from t_user
    </select>
```

测试类

```java
    @Test
    public void testCRUD() throws IOException {
        InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
        SqlSession sqlSession = sqlSessionFactory.openSession(true);
        UserMapper mapper = sqlSession.getMapper(UserMapper.class);
        //修改功能
        //mapper.updateUser();

        //删除功能
        //mapper.deleteUser();

        //查询一条语句
       /* User user = mapper.getUserById();
        System.out.println(user);*/

        List<User> list = mapper.getAllUser();
        //使用lambda遍历集合进行输出
        list.forEach(user -> System.out.println(user));
        
    }
```

----------
##核心配置文件解读
###核心配置文件注释

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!--xml文件都有的内容，声明版本号，和编码-->

<!--mybatis中的文件约束 configuration根标签-->
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--
    environments:配置多个连接数据库的环境
    属性：
        default：表示默认使用的环境的id，与某一个环境的id对应
    -->
    <environments default="development">
        <!--
            environment：配置某个具体的环境
            属性：
                id：表示连接数据库的环境的唯一标识，不能重复
        -->
        <environment id="development">
            <!--设置事务管理器的类型是JDBC-->
            <transactionManager type="JDBC"/>
            <!--transactionManager：设置事务管理方式
            属性：
                type= "JDBC|MANAGED"
                JDBC：表示当前环境中，执行SQL时，使用的是JDBC中原生的事务管理方式，事务的提交或回滚需要手动处理
                MANAGED：被管理，例如spring。通过Spring中的声明式事务管理mybatis的事务
            -->
            <!--
                dataSource:配置数据源
                属性:
                    type:设置数据源的类型
                    type="POOLED|UNPOOLED|JNDI"
                    POOLED:表示使用数据库连接池缓存数据库连接
                    UNPOOLED：表示不使用数据库连接池
                    JNDI：表示使用上下文的数据源
            -->
            <dataSource type="POOLED">
                <!--设置连接数据库的驱动-->
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <!--设置连接数据库的连接地址-->
                <property name="url" value="jdbc:mysql://localhost:3306/mybatis"/>
                <!--设置连接数据库的用户名-->
                <property name="username" value="root"/>
                <!--设置连接数据库的密码-->
                <property name="password" value="abc123"/>
            </dataSource>
        </environment>
    </environments>
    <!--映入映射文件,写在resource下面应该以路径的方式引入-->
    <mappers>
        <mapper resource="mappers/UserMapper.xml"/>
    </mappers>
</configuration>
```
----------
##核心配置文件properties
我们可以通过properties标签引入 [label color="orange"]properties文件[/label] ，通过 [label color="red"]${}[/label] 访问properties文件中的内容。
jdbc.properties

```properties
jdbc.driver=com.mysql.cj.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/mybatis
jdbc.username=root
jdbc.password=abc123

```


对于核心配置文件稍作修改

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--引入核心配置文件properties-->
    <properties resource="jdbc.properties"/>

    <environments default="development">
        <environment id="development">
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="mappers/UserMapper.xml"/>
    </mappers>
</configuration>
```

----------
###类型别名及标签顺序
每次配置查询语句的时候，都需要写 `<select id="getUserById" resultType="com.atguigu.mybatis.pojo.User">` 这样的标签，resultType后要加上全类名，很麻烦。而mybatis中为我们提供了类型别名的功能。

```xml
    <!--MyBatis核心配置文件中标签的顺序:
    The content of element type "configuration" must match
    "(properties?,settings?,typeAliases?,typeHandlers?,
    objectFactory?,objectWrapperFactory?,reflectorFactory?,
    plugins?,environments?,databaseIdProvider?,mappers?)".
    -->
    
    <!--引入核心配置文件properties-->
    <properties resource="jdbc.properties"/>

    <!--设置类型别名-->
    <typeAliases>
        <!--typeAliases:设置某个类型的别名
        属性:
            type:设置需要设置别名的类型
            alias：来设置某个类型的别名
        如果设置了alias，以设置的为准
        如果不设置alias，将拥有默认的别名，别名就是对应类名，且不区分大小写
        -->
        <!--<typeAlias type="com.atguigu.mybatis.pojo.User" alias="User"></typeAlias>-->

        <!--以包为单位，将包下所有的类设置默认的类型别名(即类名且不区分大小写)-->
        <package name="com.atguigu.mybatis.pojo"/>
    </typeAliases>
```

----------
###核心配置文件mappers映射文件
mybatis中支持**以包为单位**引入映射文件

```xml
    <!--映入映射文件,写在resource下面应该以路径的方式引入-->
    <mappers>
        <!--<mapper resource="mappers/UserMapper.xml"/>-->
        <!--当前包下的所有xml文件都会被引入核心配置文件中
        resources下面不能直接创建package
        一次性创建包的话需要使用 / 分隔才能创建为一个包的格式
        以包为单位，引入映射文件
        要求：
        1.mapper接口所在的包要和映射文件所在的包一致
        2.mapper接口要和映射文件的名字一致
        -->
        <package name="com.atguigu.mybatis.mapper"/>

    </mappers>
```
![3.png][5]

----------
##封装SqlSession工具类
我们发现，添加了模板之后，在测试类中创建SqlSession尤为关键，那么创建SqlSession过程比较麻烦，我们可以封装一个工具类
SqlSessionUtils类
```java
public class SqlSessionUtils {
    /*工具类中的方法一般都是静态方法,私有化构造方法*/
    private SqlSessionUtils() {
    }

    public static SqlSession getSqlSession() {
        //读取核心配置文件，获取当前配置文件对应的字节输入流,用try-catch处理
        SqlSession sqlSession = null;
        try {
            InputStream is = Resources.getResourceAsStream("mybatis-config.xml");
            SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(is);
            //通过创建出来的sqlSession实现增删改可以自动提交
            sqlSession = sqlSessionFactory.openSession(true);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        return sqlSession;
    }
}
```
然后可以在测试类中使用，直接就可以得到sqlSession.
![6.png][6]

----------

##获取参数值的两种方式(☆☆)

观察到语句都是自己手动输入的值，以后mybatis会放到ssm中一块使用，需要去创建一个web工程，浏览器发送请求之后到服务器，服务器接收请求参数调用service处理业务逻辑，service调用dao(现在通过mapper接口代替dao)，service调用的mapper方法将当前浏览器获取的数据传输到映射文件中。映射文件该如何获取所传输的**参数**(获取的参数值是我们所调用的mapper接口中方法的参数，我们需要在映射文件中获取)，实现SQL语句的拼接？
 [label color="blue"]MyBatis获取参数值的两种方式：${} 和 #{}[/label] 
分别对应了JDBC中的两种方式
 - ${} 本质就是字符串拼接，有sql注入的问题，有一些sql必须使用。
 - \#{} 本质就是占位符赋值。
根据不同情况参数值的获取也不同。
我将这五种情况对应的总结笔记放置在最上面，下面是对应的书写案例


[note-ico type="flat" ico=""]MyBatis获取参数值的各种情况：
 1. mapper接口方法的参数为单个的字面量类型：
可以通过${}和#{}以任意的字符串获取参数值，但是需要注意${}的单引号问题
 2. 如果当前的mapper接口方法的参数为多个时：
此时MyBatis会将这些参数放在一个map集合中，以两种方式进行存储
**a>** 以arg0，arg1...为键，以参数为值
**b>** 以param1，param2...为键，以参数为值
因此只需要通过#{}和 ${}以键的方式访问值即可，需要注意${}的单引号问题
 3. 若mapper接口方法的参数是一个map集合，可以手动将这些参数放在一个map中来存储
因此只需要通过#{}和 ${}以键的方式访问值即可，需要注意${}的单引号问题
 4. mapper接口方法的参数是一个实体类类型的参数
只需要通过#{}和 ${}以属性的方式访问属性值即可，但是需要注意${}的单引号问题
 5. 使用@Param注解命名参数
此时MyBatis会将这些参数放在一个map集合中，以两种方式进行存储
**a>** 以@Param注解的值为键，以参数为值
**b>** 以param1，param2...为键，以参数为值
因此只需要通过#{}和 ${}以键的方式访问值即可，需要注意${}的单引号问题
[/note-ico]

[font size="16" color="#ff0000"]实际上还有很多情况，包括数组集合，一共是七种情况，建议归结为两种[/font]
 - 实体类对象/map集合 的情况
 - 除实体类对象/map集合情况，手动添加 [label color="orange"]@Param注解[/label] 的情况
###获取单个字面量类型的参数
ParameterMapper.xml
```xml
    <!--User getUserByUsername(String username);-->
    <select id="getUserByUsername" resultType="User">
        <!--select * from t_user where username = #{username}-->
        select * from t_user where username = '${username}'
    </select>

```


```java
    @Test
    public void testGetUserByUsername() {
        SqlSession sqlSession = SqlSessionUtils.getSqlSession();
        //通过接口获取到一个mapper实体类的对象
        ParameterMapper mapper = sqlSession.getMapper(ParameterMapper.class);
        User user = mapper.getUserByUsername("admin");
        System.out.println(user);
    }

```
![7.png][7]
###获取多个字面量类型的参数

```xml
    <!--User checkLogin(String username,String password);-->
    <select id="checkLogin" resultType="User">
        <!--select * from t_user where username = #{param1} and password = #{param2}-->
        select * from t_user where username = '${param1}' and password = '${param2}'
    </select>

```
###获取Map类型的参数

```xml
    <!--User checkLoginByMap(Map<String, Object> map);-->
    <select id="checkLoginByMap" resultType="User">
        select * from t_user where username = #{username} and password = #{password}
    </select>

```
###获取实体类类型参数
此处的**username、password、age、sex、email**均属于set方法后对应名称的小写。
```xml
    <!--int insertUser(User user);-->
    <insert id="insertUser">
        insert into t_user values (null,#{username},#{password},#{age},#{sex},#{email})
    </insert>

```
###@Param命名参数注解
自定义当前mybatis把参数存储在map集合的键
ParameterMapper接口
```java
    /*
    验证登录（使用@Param注解）
    当我们在参数前添加@Param注解，Mybatis会帮我们把参数放在一个map集合中，
    以@Param中的参数为键，以形参为值。

    */
    public abstract User checkLoginByParam(@Param("username") String username, @Param("password") String password);
```

```xml
    <!--User checkLoginByParam(@Param("username") String username, @Param("password") String password);-->
    <select id="checkLoginByParam" resultType="User">
        select * from t_user where username = #{username} and password = #{password}
    </select>
```

----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

 - 列表项目

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/08/2448519793.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/2244957684.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/3248875674.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/1660751839.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/2161571356.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/3648445938.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/1387427739.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/08/4020397042.jpg