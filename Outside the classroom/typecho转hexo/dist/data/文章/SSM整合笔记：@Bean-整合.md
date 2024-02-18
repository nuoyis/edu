---
title: SSM整合笔记：@Bean-整合
date: 2023-08-28 18:36:00
categories: SSM整合
tags: [SSM整合,@Bean]
---
在单独学习完SSM的三个部分后，需要对于三个部分做一个整合，整合过程中我发现了自己很多的不足。一方面我更新了之前的内容，由于之前的内容太长，不方便在原有基础上再添加一些补充一些自己的遗漏，特写一篇文章，发现整合过程中的不足。

 - 看上去比较简短，博主想了好久最终还是决定发出来了。然后现在要开学了，博主目前也在学习springboot3和算法，平时将一些有意义的算法题在对应博客继续更新，由于springboot3的版本太新问题有点多(已经踩了不少坑了，心痛)，暂时不做boot的笔记，往后会学习redis，后面的更新会比较慢,等到假期就会恢复回来，敬请期待~


<!--more-->
##@Bean注解
谈到这个注解，一定和配置类有关系，顺便熟悉一下配置类
pom文件中依赖还是导一下，需要使用对应的spring组件


```xml
    <dependencies>
        <!--spring context依赖-->
        <!--当你引入Spring Context依赖之后，表示将Spring的基础依赖引入了-->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>6.0.6</version>
        </dependency>
        <!--junit5测试-->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>5.3.1</version>
        </dependency>

        <!--阿里数据库连接池 -->
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid-spring-boot-starter</artifactId>
            <version>1.1.14</version>
        </dependency>

        <!-- Spring-jdbc的依赖，JdbcTemplate依赖的jar包 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jdbc</artifactId>
            <version>4.2.4.RELEASE</version>
        </dependency>

    </dependencies>
```


我们先创建配置类代替xml配置文件
[video title="配置类 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-26%2019-32-21.mkv " container="b3unv1gktx" subtitle=" " poster=" "] [/video]

然后我们使用@Bean标签
[video title="@Bean详解 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-26%2021-02-00.mkv " container="btgzcxwab3t" subtitle=" " poster=" "] [/video]

配置类源码
JavaConfiguration
```java
package com.atguigu.config;

import com.alibaba.druid.pool.DruidDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.beans.factory.config.ConfigurableBeanFactory;
import org.springframework.context.annotation.*;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.sql.DataSource;
import javax.xml.crypto.Data;

/**
 * @author: TangZhiKai
 * @create: 2023-08-26 19:05
 * @description: Java的配置类，替代xml配置文件
 * 配置类中可以做三件事
 * 1.包扫描注解配置
 * 2.引用外部配置文件
 * 3.声明第三方依赖的bean组件
 *
 * 步骤一：添加@Configuration 代表我们是配置类
 * 步骤二：实现上面的三个功能注解
 **/

@ComponentScan(value = "com.atguigu.ioc_01")
@PropertySource(value = "classpath: jdbc.properties")
@Configuration
public class JavaConfiguration {
    /*
    第三方Bean标签 ——>一个方法
    方法的返回值类型 = Bean组件的类型或者他的接口和父类
    方法的名字 = Bean的id值(标识)

    方法体可以自定义实现过程即可！
    最重要一步：@Bean，会真正让配置类方法创建的对象存储到IoC容器。

    问题一：beanName的问题
            默认：方法名
            指定：name/value 属性起名字，覆盖方法名
    问题二：周期方法如何指定
            方法一：
            原有注解方案:PostConstruct+PreDestroy 注解指定
            方法二：
            bean属性指定 通过initMethod/ destoryMethod属性指定
    问题三：作用域
            和以前还是一样@Scope注解，默认是单实例SCOPE_SINGLETON
    问题四：如何引用其他的IoC容器组件
            1.直接调用对方的Bean方法即可
            2.直接形参变量进行引用，要求必须有对应的组件，如果有多个，形参名= 组件id表示即可

    */

    //声明在全局使用，如果只想在对应方法中使用，声明在方法的形参列表
    //@Value外部文件属性赋值
    @Value("${atguigu.url}")
    private String url;

    @Value("${atguigu.driver}")
    private String driver;

    @Value("${atguigu.username}")
    private String username;

    @Value("${atguigu.password}")
    private String password;

    @Scope(scopeName = ConfigurableBeanFactory.SCOPE_SINGLETON)
    @Bean(name = "ergouzi",initMethod ="",destroyMethod = "")
    public DruidDataSource dataSource(){
        //实现具体的实例化过程
        DruidDataSource dataSource = new DruidDataSource();
        /*
        属性来自于外部的配置文件,定义在成员方法*/
        dataSource.setUrl(url);
        dataSource.setDriverClassName(driver);
        dataSource.setUsername(username);
        dataSource.setPassword(password);
        return  dataSource;
    }
    //JdbcTemplate ->DataSource

    @Bean
    public JdbcTemplate jdbcTemplate1(){
        JdbcTemplate jdbcTemplate = new JdbcTemplate();

        //需要DataSource 需要IoC容器中的其他组件
        //方案一：如果其他组件也是@Bean方法，可以直接调用,看着在调用方法，本质上从IoC容器中获取组件
        jdbcTemplate.setDataSource(dataSource());
        return jdbcTemplate;
    }

    @Bean
    public JdbcTemplate jdbcTemplate2(DataSource dataSource){
        JdbcTemplate jdbcTemplate = new JdbcTemplate();

        /*方案二：直接使用形参列表传值,IoC容器自动帮我们进行装配
          形参列表直接声明想要的组件类型，IoC容器也会注入；
          使用形参变量注入，要求必须要有对应的类型组件，如果没有，抛异常！
          如果有多个类型(IoC容器中假设有多个datasource)：可以使用形参名=Bean的id标识即可
          */
        jdbcTemplate.setDataSource(dataSource);
        return jdbcTemplate;
    }
    
}

```




----------
##框架整合
父工程中导入依赖，子工程中书写对应的配置类信息

 - 父工程中导入依赖

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.atguigu</groupId>
    <artifactId>ssm-integration-part</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>
    <modules>
        <module>ssm-integration-01</module>
    </modules>
    <!--导入SSM整合需要的所有依赖-->
    <properties>
        <!--<thymeleaf-spring5.version>3.0.12.RELEASE</thymeleaf-spring5.version>-->
        <!--<javax.servlet-api.version>3.1.0</javax.servlet-api.version>-->
        <spring.version>6.0.6</spring.version>
        <jakarta.annotation-api.version>2.1.1</jakarta.annotation-api.version>
        <jakarta.jakartaee-web-api.version>9.1.0</jakarta.jakartaee-web-api.version>
        <jackson-databind.version>2.15.0</jackson-databind.version>
        <hibernate-validator.version>8.0.0.Final</hibernate-validator.version>
        <mybatis.version>3.5.11</mybatis.version>
        <mysql.version>8.0.25</mysql.version>
        <pagehelper.version>5.1.11</pagehelper.version>
        <druid.version>1.2.8</druid.version>
        <mybatis-spring.version>3.0.2</mybatis-spring.version>
        <jakarta.servlet.jsp.jstl-api.version>3.0.0</jakarta.servlet.jsp.jstl-api.version>
        <logback.version>1.2.3</logback.version>
        <lombok.version>1.18.26</lombok.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
    <!--
       需要依赖清单分析:
          spring
            ioc/di
              spring-context / 6.0.6
              jakarta.annotation-api / 2.1.1  jsr250
            aop
              spring-aspects / 6.0.6
            tx
              spring-tx  / 6.0.6
              spring-jdbc / 6.0.6

          springmvc
             spring-webmvc 6.0.6
             jakarta.jakartaee-web-api 9.1.0
             jackson-databind 2.15.0
             hibernate-validator / hibernate-validator-annotation-processor 8.0.0.Final

          mybatis
             mybatis  / 3.5.11
             mysql    / 8.0.25
             pagehelper / 5.1.11

          整合需要
             加载spring容器 spring-web / 6.0.6
             整合mybatis   mybatis-spring x x
             数据库连接池    druid / x
             lombok        lombok / 1.18.26
             logback       logback/ 1.2.3
    -->

    <dependencies>
        <!--spring pom.xml依赖-->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>jakarta.annotation</groupId>
            <artifactId>jakarta.annotation-api</artifactId>
            <version>${jakarta.annotation-api.version}</version>
        </dependency>

        <!-- ServletAPI -->
        <!--<dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <scope>provided</scope>
        </dependency>-->


        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aop</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-aspects</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-tx</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-jdbc</artifactId>
            <version>${spring.version}</version>
        </dependency>
        
        <!--
           springmvc
               spring-webmvc 6.0.6
               jakarta.jakartaee-web-api 9.1.0
               jackson-databind 2.15.0
               hibernate-validator / hibernate-validator-annotation-processor 8.0.0.Final
        -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-webmvc</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>jakarta.platform</groupId>
            <artifactId>jakarta.jakartaee-web-api</artifactId>
            <version>${jakarta.jakartaee-web-api.version}</version>
            <scope>provided</scope>
        </dependency>

        <!-- jsp需要依赖! jstl-->
        <dependency>
            <groupId>jakarta.servlet.jsp.jstl</groupId>
            <artifactId>jakarta.servlet.jsp.jstl-api</artifactId>
            <version>${jakarta.servlet.jsp.jstl-api.version}</version>
        </dependency>

        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>${jackson-databind.version}</version>
        </dependency>
        
        <!-- https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator -->
        <dependency>
            <groupId>org.hibernate.validator</groupId>
            <artifactId>hibernate-validator</artifactId>
            <version>${hibernate-validator.version}</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.hibernate.validator/hibernate-validator-annotation-processor -->
        <dependency>
            <groupId>org.hibernate.validator</groupId>
            <artifactId>hibernate-validator-annotation-processor</artifactId>
            <version>${hibernate-validator.version}</version>
        </dependency>
        <!--
          mybatis
               mybatis  / 3.5.11
               mysql    / 8.0.25
               pagehelper / 5.1.11
        -->
        <!-- mybatis依赖 -->
        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis</artifactId>
            <version>${mybatis.version}</version>
        </dependency>

        <!-- MySQL驱动 mybatis底层依赖jdbc驱动实现,本次不需要导入连接池,mybatis自带! -->
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>${mysql.version}</version>
        </dependency>

        <dependency>
            <groupId>com.github.pagehelper</groupId>
            <artifactId>pagehelper</artifactId>
            <version>${pagehelper.version}</version>
        </dependency>

        <!-- 整合第三方特殊依赖 -->
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-web</artifactId>
            <version>${spring.version}</version>
        </dependency>

        <dependency>
            <groupId>org.mybatis</groupId>
            <artifactId>mybatis-spring</artifactId>
            <version>${mybatis-spring.version}</version>
        </dependency>

        <!-- 日志 ， 会自动传递slf4j门面-->
        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>${logback.version}</version>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>${lombok.version}</version>
        </dependency>

        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>druid</artifactId>
            <version>${druid.version}</version>
        </dependency>

        <!--配置thymeleaf视图模板解析器-->
        <!-- Spring5和Thymeleaf整合包 -->
        <!--<dependency>
            <groupId>org.thymeleaf</groupId>
            <artifactId>thymeleaf-spring5</artifactId>
        </dependency>-->

    </dependencies>


</project>
```

 - 业务层书写
ServiceJavaConfig

```java
/**
 * @description: 业务层配置类：service,aop,tx
 * @author: TangZhiKai
 * @create: 2023-08-26 18:07
 * 1.service
 * 2.开启aop注解支持 aspect:@Before @After @AfterReturning @AfterThrowing @Around @Aspect @Order
 * 3.声明式事务管理：1.对应的事务管理器实现[TransactionManager DataSource... Hibernate...Jpa] 2.开启事务注解的支持@Transactional
 **/
@Configuration
@EnableAspectJAutoProxy//开启注解支持
@EnableTransactionManagement//开启事务注解支持
@Transactional
@ComponentScan("com.atguigu.service")//扫描包
public class ServiceJavaConfig {

    //需要项目的连接池
    @Bean
    public TransactionManager transactionManager(DataSource dataSource){
        DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager();
        dataSourceTransactionManager.setDataSource(dataSource);
        return  dataSourceTransactionManager;
    }
}

```


 - 控制层书写
对应控制层的配置不是很完全，详情可见，而且这里用了过时的jsp，可以使用thymeleaf[配置视图解析器][1]
WebMvcJavaConfig

```java
/**
 * @description: 配置控制层的配置类(controller, springmvc)
 * @author: TangZhiKai
 * @create: 2023-08-26 17:33
 *
 * 1.Controller
 * 2.全局异常处理
 * 3.handlerMapping handlerAdapter
 * 4.静态资源处理
 * 5.jsp视图解析器前后缀
 * 6.json转化器
 * 7.拦截器
 **/
//3.handlerMapping handlerAdapter|6.json转化器
@EnableWebMvc
//声明当前类为一个配置类
@Configuration
//开启MVC的自动扫描
@ComponentScan("com.atguigu.controller")
public class WebMvcJavaConfig implements WebMvcConfigurer {


    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        //开启静态资源处理
        configurer.enable();
    }



   /*
   配置拦截器
   @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new )
    }
*/
   /*配置jsp视图解析器*/

    @Override
    public void configureViewResolvers(ViewResolverRegistry registry) {
        registry.jsp("/WEB-INF/views/","jsp");
    }
}
```


 - 持久层组件
提供**不需要配置**mapper-config.xml的写法
MapperJavaConfigNew

```java
package com.atguigu.config;

import com.alibaba.druid.support.logging.SLF4JImpl;
import com.github.pagehelper.PageInterceptor;
import org.apache.ibatis.logging.slf4j.Slf4jImpl;
import org.apache.ibatis.session.AutoMappingBehavior;
import org.mybatis.spring.SqlSessionFactoryBean;
import org.mybatis.spring.mapper.MapperScannerConfigurer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;

import javax.sql.DataSource;
import java.util.Properties;

/**
 * @author: TangZhiKai
 * @create: 2023-08-27 16:28
 * @description: 持久层配置类：连接池信息，以及sqlSessionFactory,Mapper代理对象
 * 方式二：不保留外部配置文件，全部mybatis的属性都在代码中设置!
 *
 * 
 **/
@Configuration
public class MapperJavaConfigNew {

    @Bean
    public SqlSessionFactoryBean sqlSessionFactory(DataSource dataSource){
        SqlSessionFactoryBean sqlSessionFactoryBean = new SqlSessionFactoryBean();
        //指定配置文件的信息
        //1.指定数据库连接池对象
        sqlSessionFactoryBean.setDataSource(dataSource);

        org.apache.ibatis.session.Configuration configuration = new org.apache.ibatis.session.Configuration();

        //设置驼峰式映射
        configuration.setMapUnderscoreToCamelCase(true);

        //开启日志输出
        configuration.setLogImpl(Slf4jImpl.class);
        //开启resultMap的自动映射
        configuration.setAutoMappingBehavior(AutoMappingBehavior.FULL);

        //2.指定mybatis配置文件的功能，使用代码的形式
        sqlSessionFactoryBean.setConfiguration(configuration);//存储setting的配置文件

        //设置类型别名
        sqlSessionFactoryBean.setTypeAliasesPackage("com.atguigu.pojo");

        //设置分页插件
        PageInterceptor pageInterceptor = new PageInterceptor();

        Properties properties = new Properties();
        properties.setProperty("helperDialect","mysql");

        pageInterceptor.setProperties(properties);
        sqlSessionFactoryBean.addPlugins(pageInterceptor);

        return  sqlSessionFactoryBean;
    }

    //mapper代理对象加入到ioc
    @Bean
    public MapperScannerConfigurer mapperScannerConfigurer(){
        //Mapper代理对象的factoryBean ->指定一个包 -> mapper接口->sqlSessionFactory->getMapper-> mapper代理对象->ioc
        MapperScannerConfigurer mapperScannerConfigurer = new MapperScannerConfigurer();
        //mapper接口和mapperxml文件所在的共同包
        mapperScannerConfigurer.setBasePackage("com.atguigu.mapper");

        return  mapperScannerConfigurer;
    }
}

```
DataSourceJavaConfig

```java
/**
 * @author: TangZhiKai
 * @create: 2023-08-27 16:48
 * @description: 连分开配置,接池配置类
 **/
@Configuration
@PropertySource("classpath:jdbc.properties")
public class DataSourceJavaConfig {

    @Value("${jdbc.user}")
    private String user;

    @Value("${jdbc.password}")
    private String password;
    @Value("${jdbc.url}")
    private String url;
    @Value("${jdbc.driver}")
    private String driver;

    @Bean
    public DataSource dataSource(){
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setUsername(user);
        dataSource.setUrl(url);
        dataSource.setPassword(password);
        dataSource.setDriverClassName(driver);

        return dataSource;
    }

}

```


最后在SpringIoCInit中初始化即可
![1.png][2]

----------
附上最后的整合
[video title="整合流程 " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-27%2018-48-56.mkv " container="bi95otagsy" subtitle=" " poster=" "] [/video]

> 9月8日，我做出来了SSM终极实战项目，微头条，我放在了[博主日志][3]中留于纪念，代表学习的一个阶段。


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://www.kaijavademo.top/337.html#cl-21
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/2338261685.png
  [3]: https://www.kaijavademo.top/journal.html