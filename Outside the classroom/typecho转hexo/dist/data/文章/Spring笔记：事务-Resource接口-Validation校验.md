---
title: Spring笔记：事务-Resource接口-Validation校验
date: 2023-08-02 06:38:00
categories: Spring6
tags: [Spring6,事务,Resource类,Validation]
---
笔记基于Spring6演示CURD操作，不同于以前JDBC，现在的事务操作时基于注解和Spring技术完成
之前有过对于JDBC的介绍和工具类的封装[JDBC工具类封装][1]


<!--more-->
准备工作：
父工程中添加依赖

```xml
<dependencies>
    <!--spring jdbc  Spring 持久化层支持jar包-->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-jdbc</artifactId>
        <version>6.0.2</version>
    </dependency>
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
</dependencies>
```
创建配置文件jdbc.properties

```other
jdbc.user=root
jdbc.password=abc123
jdbc.url=jdbc:mysql://localhost:3306/spring?characterEncoding=utf8&useSSL=false
jdbc.driver=com.mysql.cj.jdbc.Driver
```
在新建的模块类路径下添加bean.xml，调整配置信息

 - 引入外部配置文件，创建**数据源**对象
 - 创建 [label color="red"]jdbcTemplate[/label] 对象，注入**数据源**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context.xsd">

    <!--引入外部属性文件，创建数据源对象-->
    <context:property-placeholder location="classpath:jdbc.properties"></context:property-placeholder>


    <bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="url" value="${jdbc.url}"></property>
        <property name="driverClassName" value="${jdbc.driver}"></property>
        <property name="username" value="${jdbc.user}"></property>
        <property name="password" value="${jdbc.password}"></property>
    </bean>


    <!--创建jdbcTemplate对象，注入数据源-->
    <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
        <property name="dataSource" ref="druidDataSource"></property>
    </bean>



</beans>
```
在JDBCTemplateTest 测试类中完成数据库的**CRUD**，通过**整合Junit5**通过注解完成xml文件的读取和对象jdbcTemplate的属性注入。
通过`@SpringJUnitConfig(locations = "classpath:beans.xml")` 
代替 
 ~~  `ApplicationContext context = new ClassPathXmlApplicationContext(".xml");`  ~~ 
 ~~  `XXX xxx = context.getBean("xxx", xxx.class);`  ~~ 
**@Autowired**用于属性注入

```java
@SpringJUnitConfig(locations = "classpath:beans.xml")
public class JDBCTemplateTest {
    @Autowired
    private JdbcTemplate jdbcTemplate;
}

```

准备数据库表

```sql
CREATE DATABASE `spring`;
use `spring`;
CREATE TABLE `t_emp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL COMMENT '姓名',
  `age` int(11) DEFAULT NULL COMMENT '年龄',
  `sex` varchar(2) DEFAULT NULL COMMENT '性别',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

----------

在该方法中添加测试类进行CRUD增删改查。
###使用JdbcTemplate类CRUD

```java
@SpringJUnitConfig(locations = "classpath:beans.xml")
public class JDBCTemplateTest {


    @Autowired
    private JdbcTemplate jdbcTemplate;

    //添加，修改，删除
    @Test
    public void testUpdate() {
        /*

        //1.添加操作
        //编写sql语句
        String sql = "INSERT INTO t_emp VALUES(null,?,?,?)";
        //第二步，调用jdbcTemplate方法,传入相关参数

        //Object[] params = {"东方不败", 20, "未知"};
        //int rows = jdbcTemplate.update(sql, params);

        int rows = jdbcTemplate.update(sql, "林平之", 20, "未知");
        System.out.println(rows);

         */


        //2.修改操作
        /*String sql = "UPDATE t_emp SET NAME =? where id =?";
        int rows = jdbcTemplate.update(sql, "林平之atguigu",3);
        System.out.println(rows);*/

        //3.删除操作
        String sql = "DELETE FROM t_emp where id=?";
        int rows = jdbcTemplate.update(sql, 3);
        System.out.println(rows);


    }

    //4.查询操作
    @Test
    public void testSelectObject() {
        //写法一
        //String sql = "SELECT * FROM t_emp WHERE id=?";

        //查询：返回对象
        //RowMapper此时采用手动封装,采用lambda表达式封装
        //rs表示结果集
        //rowNum
/*        Emp empResult = jdbcTemplate.queryForObject(sql,
                (rs, rowNum) -> {
                    Emp emp = new Emp();
                    emp.setId(rs.getInt("id"));
                    emp.setName(rs.getString("name"));
                    emp.setAge(rs.getInt("age"));
                    emp.setSex(rs.getString("sex"));
                    return emp;
                }, 1);
        System.out.println(empResult);*/


        //写法二
        String sql = "SELECT * FROM t_emp WHERE id=?";

        Emp emp = jdbcTemplate.queryForObject(sql,
                new BeanPropertyRowMapper<>(Emp.class), 1);

        System.out.println(emp);

    }


    //查询：返回list集合
    @Test
    public void testSelectList() {
        String sql = "SELECT * FROM t_emp";
        List<Emp> list = jdbcTemplate.query(sql,
                new BeanPropertyRowMapper<>(Emp.class));
        System.out.println(list);
    }

    //查询：返回单个值
    @Test
    public void testSelectValue(){
        String sql = "SELECT COUNT(*) FROM t_emp";
        //参数二：表示返回类型的class
        //参数三：占位符赋值
        Integer count = jdbcTemplate.queryForObject(sql, Integer.class);
        System.out.println(count);
    }

}

```

[note type="success flat"]这里我要做一定解释，之前学习**JDBC**的时候写过[工具类封装][2]，分为**DQL语句和非DQL语句**，在使用**JdbcTemplate类**完成数据库的**增删改查**的时候我非常激动，因为我看到了**JdbcTemplate**中**query**和**update方法**的形参列表和我当初写的[工具类封装][3]几乎一模一样，尤其是query在查询返回list集合的时候我深有体会，传递的是一个字节码对象，当时通过传递一个类的字节码对象，进行反射。对比当初写的JDBC工具类封装和现在使用JdbcTemplate感到非常亲切，翻看源码的时候我却看的不太懂，我认为实现的核心思路没有变，只不过Spring站在了更加全面的角度去编写，代码看上去非常复杂，对比我写的工具类封装可能复用性更好，功能更多，给了我学下去的巨大动力。[/note]


----------
###基于注解的声明式事务
我在之前有写过[编程式事务][4]，但是编程式事务不太灵活。这里实现**基于注解**的声明式事务。
通过用户买书的过程演示事务操作。
创建表

```sql
CREATE TABLE `t_book` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `book_name` varchar(20) DEFAULT NULL COMMENT '图书名称',
  `price` int(11) DEFAULT NULL COMMENT '价格',
  `stock` int(10) unsigned DEFAULT NULL COMMENT '库存（无符号）',
  PRIMARY KEY (`book_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
insert  into `t_book`(`book_id`,`book_name`,`price`,`stock`) values (1,'斗破苍穹',80,100),(2,'斗罗大陆',50,100);
CREATE TABLE `t_user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(20) DEFAULT NULL COMMENT '用户名',
  `balance` int(10) unsigned DEFAULT NULL COMMENT '余额（无符号）',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
insert  into `t_user`(`user_id`,`username`,`balance`) values (1,'lucy',500);
```
调整springxml配置文件
首先添加一个tx命名空间

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xmlns:context="http://www.springframework.org/schema/context"
xmlns:tx="http://www.springframework.org/schema/tx"
xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/tx
http://www.springframework.org/schema/tx/spring-tx.xsd">
```
添加配置

```xml
    <!--
    开启事务的注解驱动
    通过注解@Transactional所标识的方法或标识的类中所有的方法，都会被事务管理器管理事务
    -->
    <!-- transaction-manager属性的默认值是transactionManager，如果事务管理器bean的id正好就
    是这个默认值，则可以省略这个属性 -->
    <tx:annotation-driven transaction-manager="transactionManager" />
```
在对应的Service层类/方法上面添加 [label color="red"]@Transactional[/label] 会有事务影响。
如果事务操作失败，基于事务的原子性，方法会有回滚。
![1.png][5]

----------
###事务的属性
 `@Transactional()` 
 - **只读**：设置只读，只能查询，不能修改添加删除操作
 `@Transactional(readOnly = true)` 
![2.png][6]

 - **超时**：默认-1，设置超时时间之内没有完成，直接抛出异常，回滚。
**超时时间单位为秒**
![3.png][7]
 - **回滚策略**：设置哪些异常不回滚，哪些回滚
可以提前设置好对应的异常，在发生异常后控制台报错，但是事务**不会**回滚。
![4.png][8]
 - **隔离级别**：读问题
事务之间存在隔离性，即事物之间不产生影响，不考虑隔离性会产生三个读问题。**脏读，不可重复读，虚读**(幻读)
问题|解释
:--:|:--:
脏读|两个事务没有提交，但是互相修改数据，可以看到
不可重复读|一个事务没有提交，另一个事务修改已经提交，它能读到事务修改之后的数据。
幻读|一个事务没有提交，一个事务提交但是做了添加，可以读到添加的数据。
设置数据库的隔离级别可以避免，不同数据库对于四种隔离级别支持程度不同（自行百度），MySQL全部支持。
各个隔离级别解决并发问题的能力见下表：

**隔离级别**|**脏读**|**不可重复读**|**幻读**
:--:|:--:|:--:|:--:
**READ UNCOMMITTED**|有 |有 |有 
**READ COMMITTED**|无 |有 |有 
**REPEATABLE READ(MySQL默认)**|无|无|有
**SERIALIZABLE**|无|无|无

 [label color="blue"]使用方式[/label] 
```java
@Transactional(isolation = Isolation.DEFAULT)//使用数据库默认的隔离级别
@Transactional(isolation = Isolation.READ_UNCOMMITTED)//读未提交
@Transactional(isolation = Isolation.READ_COMMITTED)//读已提交
@Transactional(isolation = Isolation.REPEATABLE_READ)//可重复读
@Transactional(isolation = Isolation.SERIALIZABLE)//串行化

```
 - **事务的传播行为**：事务方法之间的调用，事务该如何使用？
一共有七种事务的传播行为，这里只关注REQUIRED REQUIRES_NEW
**REQUIRED**：支持当前事务，如果不存在就新建一个(默认)
 `@Transactional(propagation = Propagation.REQUIRED) ` 
**REQUIRES_NEW**：开启一个新的事务，如果一个事务已经存在，则将这个存在的事务挂起。
如果lucy想要同时买两本书，而刚好只有买前一本的钱，编写一个买多本书的Service方法调用给买单个书的方法，实际上处于一个事务中调用另一个事务。如果是REQUIRED，那么第二本钱不够交易失败，整个操作都会回滚。也就是说只要有操作失败，整体都会回滚。而REQUIRES_NEW会开启一个新事务，将原先事务挂起，实际上就是能买几本书就会买几本书。而不会整体回滚。

----------
####全注解配置事务
想要实现全注解开发，那么要使用配置类取代配置文件，我们可以添加一个配置类，将原先所有的配置文件中的获取放在类中获取。
创建一个SpringConfig类

```java
@Configuration //通过配置类替代配置文件
@ComponentScan("com.atguigu.spring6.tx")//开启组件扫描
@EnableTransactionManagement //表示开启事务管理
public class SpringConfig {
    @Bean
    public DataSource getDataSource(){
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
        dataSource.setUsername("root");
        dataSource.setPassword("abc123");
        dataSource.setUrl("jdbc:mysql://localhost:3306/spring?characterEncoding=utf8&useSSL=false");

        return dataSource;
    }

    @Bean(name = "jdbcTemplate")
    public JdbcTemplate getJdbcTemplate(DataSource dataSource){
        JdbcTemplate jdbcTemplate = new JdbcTemplate();
        jdbcTemplate.setDataSource(dataSource);
        return jdbcTemplate;

    }

    @Bean
    public DataSourceTransactionManager getDataSourceTransactionManager(DataSource dataSource){
        DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager();
        dataSourceTransactionManager.setDataSource(dataSource);
        return dataSourceTransactionManager;
    }
    
}

```
它与XML文件中的对应关系是这样的
![5.png][9]


----------
###基于XML文件实现声明式事务管理

 1. 环境准备
 2. 创建Spring配置文件
 - 开启组件扫描
 - 创建数据源**DataSource**
 - 创建**JdbcTemplate**,注入数据源
 - 创建事务管理器，注入数据源
 - 配置事务通知
 - 通过**切入点表达式**，把事务通知添加到方法上，配置事务通知，设置事务中一些相关的**属性**。


```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:tx="http://www.springframework.org/schema/tx" xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/tx
http://www.springframework.org/schema/tx/spring-tx.xsd http://www.springframework.org/schema/aop https://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--开启组件扫描-->
    <context:component-scan base-package="com.atguigu.spring6.xmltx"></context:component-scan>

    <!--引入外部属性文件，创建数据源对象-->
    <context:property-placeholder location="classpath:jdbc.properties"></context:property-placeholder>
    <bean id="druidDataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="url" value="${jdbc.url}"></property>
        <property name="driverClassName" value="${jdbc.driver}"></property>
        <property name="username" value="${jdbc.user}"></property>
        <property name="password" value="${jdbc.password}"></property>
    </bean>
    
    <!--JdbcTemplate对象-->
    <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
        <property name="dataSource" ref="druidDataSource"></property>
    </bean>

    <!--创建事务管理器-->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="druidDataSource"></property>
    </bean>

    <!--配置事务的增强-->

    <tx:advice id="txAdvice" transaction-manager="transactionManager">
        <tx:attributes>
            <!--设置事务的方法的规则,并设置相关的属性
            get*表示以get方法开头的方法的规则
            -->
            <tx:method name="get*" read-only="true"/>

            <tx:method name="update*" read-only="false" propagation="REQUIRED"></tx:method>

            <!--配置buybook事务Service层,要配置到Service层-->
            <tx:method name="buy*" read-only="false" propagation="REQUIRED"></tx:method>
        </tx:attributes>
    </tx:advice>

    <!--配置切入点和通知使用的方法-->
    <aop:config>
        <aop:pointcut id="pt" expression="execution(* com.atguigu.spring6.xmltx.service.*.*(..))"/>
        <!--advice-ref对应通知id；pointcut-ref对应切入点表达式的id名；完成添加，把我们的通知用在对应方法上，通过切入点表达式设置在哪个方法上用到事务-->
        <aop:advisor advice-ref="txAdvice" pointcut-ref="pt"></aop:advisor>
    </aop:config>
    
</beans>
```
![6.png][10]

----------
###ResourceLoader总结
Spring将采用和ApplicationContext相同的策略来访问资源。也就是说，
如果**ApplicationContext**是 [label color="orange"]FileSystemXmlApplicationContext[/label] ，**res**就是 [label color="orange"]FileSystemResource[/label] 实例；
如果**ApplicationContext**是 [label color="purple"]ClassPathXmlApplicationContext[/label] ，**res**就是 [label color="purple"]ClassPathResource[/label] 实例

当Spring应用需要进行资源访问时，实际上并不需要**直接使用Resource实现类**，而是调用
**ResourceLoader**实例的**getResource()**方法来获得资源，**ReosurceLoader**将会负责选择Reosurce实现
类，也就是确定**具体的资源访问策略**。
![7.png][11]
我们把资源每次写入代码中，我们可以使用配置文件对于资源的引用和代码进行解耦合。
配置XML文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">


    <bean id="resourceBean" class="com.atguigu.spring6.di.ResourceBean">
        <property name="resource" value="classpath:atguigu.txt"></property>
    </bean>
</beans>
```
![8.png][12]
创建对应ResourceBean类，提供resource成员变量，并提供对应get和set方法，最终测试类测试即可。
![9.png][13]


----------
###Validation
实际开发中会频繁用到数据校验，Spring Validation可以把**校验**和**业务**分离出来，降低耦合度。让代码编写更加简单。
####通过Validator接口实现

 1. 引入依赖
在对应子工程中引入依赖

```xml
<dependencies>
<dependency>
<groupId>org.hibernate.validator</groupId>
<artifactId>hibernate-validator</artifactId>
<version>7.0.5.Final</version>
</dependency>
<dependency>
<groupId>org.glassfish</groupId>
<artifactId>jakarta.el</artifactId>
<version>4.0.1</version>
</dependency>
</dependencies>
```

 2. 创建实体类，定义属性，创建对应的set和get方法
Person类

```java
public class Person {
    private String name;
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}

```

 3. 创建类，实现接口，实现接口的方法，编写校验逻辑
PersonValidator类

```java
public class PersonValidator implements Validator {

    /*
    supports方法表示校验用在哪个类型上
    validate方法就是具体的校验逻辑
    */
    @Override
    public boolean supports(Class<?> clazz) {
        //表示对哪个类型校验
        return Person.class.equals(clazz);
    }

    //校验规则
    @Override
    public void validate(Object target, Errors errors) {
        //name不能为空
        //ValidationUtils.rejectIfEmpty()方法判断非空
        //参数一：errors表示为空出现错误。
        //参数二：属性(成员变量)
        //参数三：错误的编码，可随意
        //参数四：提示信息
        ValidationUtils.rejectIfEmpty(
                errors,
                "name",
                "name.empty",
                "name is null");


        //age不能小于0，不能大于200
        //先做一个强制转换
        Person p = (Person) target;
        if(p.getAge() < 0){
            /*
            errors.rejectValue()
            参数一：属性
            参数二：错误编码，同上可以随意
            参数三：提示信息
            */
            errors.rejectValue("age","age.value.error","age < 0");

        }else if(p.getAge() > 200){
            errors.rejectValue("age","age.value.error.old","age > 200");
        }


    }
}

```


 4. 完成测试

```java
//完成最终的校验测试
public class TestPerson {
    public static void main(String[] args) {
        //创建person对象
        Person person = new Person();

        //创建person对应databinder
        DataBinder binder = new DataBinder(person);

        //设置校验器
        binder.setValidator(new PersonValidator());

        //调用方法执行校验
        binder.validate();

        //输出校验结果
        BindingResult result = binder.getBindingResult();

        //输出所有信息
        System.out.println(result.getAllErrors());
    }
}

```
![10.png][14]


----------
####注解实现Validation

 1. 创建配置类，配置LocalValidatorFactoryBean

```java
@Configuration
@ComponentScan("com.atguigu.spring6.validator.two")
public class ValidationConfig {

    @Bean
    public LocalValidatorFactoryBean validator(){
        return  new LocalValidatorFactoryBean();
    }

}
```

 2. 创建实体类，定义属性，生成get和set方法，在属性上面使用 [label color="blue"]注解[/label] 设置校验规则
User类

```java
public class User {
    @NotNull
    private String name;
    
    @Min(0)
    @Max(150)
    private int age;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
    
}

```

[note type="primary flat"]常用注解说明
@NotNull 限制必须不为null
@NotEmpty 只作用于字符串类型，字符串不为空，并且长度不为0
@NotBlank 只作用于字符串类型，字符串不为空，并且trim()后不为空串
@DecimalMax(value) 限制必须为一个不大于指定值的数字
@DecimalMin(value) 限制必须为一个不小于指定值的数字
@Max(value) 限制必须为一个不大于指定值的数字
@Min(value) 限制必须为一个不小于指定值的数字
@Pattern(value) 限制必须符合指定的正则表达式
@Size(max,min) 限制字符长度必须在min到max之间
@Email 验证注解的元素值是Email，也可以通过正则表达式和flag指定自定义的email格式[/note]

 3. 创建校验器
校验器有两种，分别编写类完成。
#####第一种校验器

```java
import jakarta.validation.ConstraintViolation;
import jakarta.validation.Validator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Set;

//第一种校验器:注意导包，使用原生校验器
@Service //或者是@Component

public class MyValidation1 {

    @Autowired
    private Validator validator;


    public boolean validatorByUserOne(User user){
        Set<ConstraintViolation<User>> validate = validator.validate(user);
        //表示是否有校验信息
        return validate.isEmpty();

    }
}
```
#####第二种校验器

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.validation.BindException;
import org.springframework.validation.ObjectError;
import org.springframework.validation.Validator;

import java.util.List;


//第二种校验器：使用Spring中
@Service
public class MyValidation2 {

    @Autowired
    private Validator validator;

    public boolean validatorByUserTwo(User user){
        BindException bindException = new BindException(user,user.getName());
        validator.validate(user,bindException);
        List<ObjectError> allErrors = bindException.getAllErrors();

        //输出错误信息
        System.out.println(allErrors);

        //表示是否有错误信息，hasErrors()没有错误信息显示false，有错误信息输出true
        return bindException.hasErrors();
    }
}
```

 4. 完成测试
基于两种校验器编写两个测试类

```java
import org.junit.jupiter.api.Test;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

public class TestUser {
    //两个校验器分别测试

    @Test
    public void testValidationOne() {
        //加载配置类创建容器
        ApplicationContext context = new AnnotationConfigApplicationContext(ValidationConfig.class);
        MyValidation1 validation1 = context.getBean(MyValidation1.class);

        User user = new User();
        user.setName("lucy");
        user.setAge(-1);
        boolean message = validation1.validatorByUserOne(user);
        System.out.println(message);//为空(不符合编写要求是false)是false
                                    //有值(符合编写要求就是true)true

    }

    @Test
    public void testValidationTwo() {
        //Spring中原生写法
        ApplicationContext context = new AnnotationConfigApplicationContext(ValidationConfig.class);
        MyValidation2 validation2 = context.getBean(MyValidation2.class);

        User user = new User();
        user.setName("lucy");
        user.setAge(70);
        boolean message = validation2.validatorByUserTwo(user);
        System.out.println(message);

    }
}
```

----------
####基于方法实现校验

 1. 创建配置类，配置 [label color="blue"]MethodValidationPostProcessor[/label] 

```java
@Configuration
@ComponentScan("com.atguigu.spring6.validator.three")
public class ValidationConfig {


    @Bean
    public MethodValidationPostProcessor validationPostProcessor(){
        return new MethodValidationPostProcessor();
    }
    
}

```

 2. 创建实体类，使用注解设置校验规则


```java
public class User {
    @NotNull
    private String name;

    @Min(0)
    @Max(150)
    private int age;

    @Pattern(regexp = "^1(3|4|5|7|8)\\d{9}$",message = "手机号码格式错误")//以1开头，一共有11位数
    @NotBlank(message = "手机号码不能为空")
    private String phone;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }
}
```

 3. 定义**Service**类，通过注解操作对象

```java
@Service
@Validated
public class MyService {
    
    public String testMethod(@NotNull @Valid User user){
        return user.toString();

    }
}
```

 3. 完成测试

```java
public class TestUser {
    public static void main(String[] args) {
        ApplicationContext context = new AnnotationConfigApplicationContext(ValidationConfig.class);

        MyService service = context.getBean(MyService.class);

        User user  = new User();
        user.setName("lucy");
        user.setPhone("234356");
        service.testMethod(user);

    }
}

```


----------
####自定义校验
如果注解不能满足规则，可以实现自定义注解
![11.png][15]

 1. 加上注解类，里面添加相关属性，这些可以参考其他注解实现，在里面加上校验器的类

```java
//创建一个注解类，实现不能有空格的校验
@Target({ElementType.METHOD, ElementType.FIELD, ElementType.ANNOTATION_TYPE, ElementType.CONSTRUCTOR, ElementType.PARAMETER, ElementType.TYPE_USE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Constraint(validatedBy = {CannotBlankValidation.class})//指定校验器类名，并创建对应类
public @interface CannotBlank {
    //默认提示错误信息
    String message() default "不能包含空格";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};

    @Target({ElementType.METHOD, ElementType.FIELD, ElementType.ANNOTATION_TYPE, ElementType.CONSTRUCTOR, ElementType.PARAMETER, ElementType.TYPE_USE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    //指定多个的时候使用
    public @interface List {
        CannotBlank[] value();
    }
}
```

 2. 校验器中添加校验规则

```java
//实现一个接口,泛型一：自定义注解名。泛型二：值的类型
public class CannotBlankValidation implements ConstraintValidator<CannotBlank,String> {


    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        //实现真正校验规则
        if(value != null && value.contains(" ")){
            //获取默认提示信息
            String defaultConstraintMessageTemplate = context.getDefaultConstraintMessageTemplate();
            System.out.println("default message :" + defaultConstraintMessageTemplate);
            //禁用默认提示信息
            context.disableDefaultConstraintViolation();
            //设置提示语
            context.buildConstraintViolationWithTemplate("can not contains blank").addConstraintViolation();
            return  false;//表示包含空格
        }
        return true;
    }
}
```

 3. 测试
![12.png][16]

----------
###AOT提前编译

[note type="info flat"]1.JIT(JUST IN TIME),动态编译(实时编译)，边运行边编译。
在程序运行时候，进行JIT动态编译，可以进行**性能优化，动态生成代码**，会造成启动比较慢，编译的时候需要占用运行时的资源。**JIT在程序运行过程中，把字节码文件转换成硬盘上直接运行机器码，部署到环境过程。**
2.AOT(AHEAD OF TIME),运行前编译，提前编译
可以把源代码转换成机器码，好处就是**直接启动，速度快**，都编译好后直接运行，内存占用很低，运行的时候无法优化，程序的安装时间变长。**在程序运行之前，就把字节码转换成机器码。**[/note]

> 现在正处于云原生，降本增效的时代，Java 相比于 Go、Rust 等其他编程语言非常大的弊端就是启动编
译和启动进程非常慢，这对于根据实时计算资源，弹性扩缩容的云原生技术相冲突，Spring6 借助 AOT
技术在运行时内存占用低，启动速度快，逐渐的来满足 Java 在云原生时代的需求，对于大规模使用 Java
应用的商业公司可以考虑尽早调研使用 JDK17，通过云原生技术为公司实现降本增效。

> Spring6 支持的 AOT 技术，这个 GraalVM 就是底层的支持，Spring 也对 GraalVM 本机映像提供了一
流的支持。


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://www.kaijavademo.top/51.html
  [2]: https://www.kaijavademo.top/51.html
  [3]: https://www.kaijavademo.top/51.html
  [4]: https://www.kaijavademo.top/36.html
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/3051350172.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/3220687592.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/535541672.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/08/3617968495.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/08/2980372504.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/08/559371584.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/2276137587.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/1027502838.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/08/3845200256.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/427690082.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/08/2212976455.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/08/2622830989.png