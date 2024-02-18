---
title: SpringBoot3笔记：数据访问-基础特性-场景整合
date: 2023-10-25 09:24:00
categories: SpringBoot
tags: [SpringBoot3,基础特性,数据访问,场景整合,远程调用]
---
在有了Web开发的前提下，如果对数据访问场景进行开发，那么就是一个非常完整的业务流程了。

<!--more-->

##通过SpringBoot整合SSM
使用 [label color="green"]Spring Initializr[/label] 创建向导快速构建boot工程。以后使用这样的方式。在向导中勾选对应需要的启动器，比如新版的数据库驱动、mybatis场景、web场景...

###SpringBoot整合MyBatis
在 [label color="green"]application.properties[/label] 中配置对应的基本数据源参数

```properties
#1.三大框架整合，最先配置数据源信息
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.type=com.zaxxer.hikari.HikariDataSource
#配置对应的数据库信息
spring.datasource.url=jdbc:mysql://localhost:3306/test
spring.datasource.username=
spring.datasource.password=
```
继续在此文件中，配置**整合MyBatis**。
 1. 在启动类的子包创建Bean包，添加对应Bean类和**@Data注解**，根据对应的数据库，来封装表的数据。
 2. 在启动类的子包创建Mapper包，添加一个接口，用来查表数据的，与此还需要有一个XML文件与之对应。
 3. 在resources(类路径)创建一个mapper包，用来存放XML文件。单机UserMapper接口类使用插件快速创建XML文件。
![1.png][1]
安装MyBatisX插件，帮我们生成Mapper接口的XML文件即可。
我们在Mapper接口中书写方法，使用 [label color="red"]alt + enter[/label] 快速识别生成XML标签，我们需要手动在标签体书写对应的SQL语句。为了方便传参(**#{}**)，我们需要在对应的接口形参位置添加 [label color="pink"]@Param("")[/label] 注解。
 4. UserMapper接口

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-25 15:38
 * @description: 接口，用来查t_user表数据的，还需要有个xml文件与之对应
 **/
public interface UserMapper {

    /**
     * 1.每个方法都在Mapper文件中有一个SQL标签对应，
     * 2.所有参数都应该用@Param进行签名，以后使用指定的名字在SQL中取值
     * @param id
     * @return
     */
    //使用插件给形参添加@Param注解，以后XML文件中就用 #{}来取,这是一个良好的习惯
    public TUser getUserById(@Param("id") Long id);
}
```
 5. 启动类中添加注解@MapperScan

```java
/**
 * 1.使用@MapperScan 告诉MyBatis，扫描哪个包下面的所有接口
 * 2.通过properties文件配置配置项，使用mybatis.mapper-locations告诉MyBatis，每个接口的XML文件都在哪里。
 * 3.MyBatis自动关联绑定
 */
@MapperScan(basePackages = "com.atguigu.boot3.ssm.mapper")
@SpringBootApplication
public class Boot305SsmApplication {

    public static void main(String[] args) {
        SpringApplication.run(Boot305SsmApplication.class, args);
    }

}
```
 6. 修改配置文件
**配置文件properties**中需要指定，扫描类路径下对应的包文件 `mybatis.mapper-locations=classpath:/mapper/*.xml` 
那么实际上就会从当前包中寻找XML文件，然后对应再文件的**命名空间**，在找到实际的Mapper接口。实现接口和XML文件的关联。打开对应的驼峰命名规则，这样可以不用在SQL中起别名。

```properties
# 2.配置整合MyBatis
#指定接口的XML文件为类路径下mapper中的所有文件
mybatis.mapper-locations=classpath:/mapper/*.xml
#开启驼峰命名规则
mybatis.configuration.map-underscore-to-camel-case=true
```
 7. 写Controller、(Service）测试

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-25 16:11
 * @description: 测试MyBatis的整合
 **/
@RestController
public class UserController {

    //理论上还有一层Service,这里直接跳过
    @Autowired
    UserMapper userMapper;//如果有报错，本质IDEA不知道UserMapper是容器中的组件
    /**
     * 返回User的json数据
     * @param id
     * @return
     */
    @GetMapping("/user/{id}")
    public TUser getUser(@PathVariable("id") Long id){
        TUser user = userMapper.getUserById(id);
        return user;
    }
}

```
![2.png][2]


流程看上去有点复杂，没事我录视频用于复习回顾了捏:)
[video title="SpringBoot整合MyBatis " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E6%95%B4%E5%90%88MyBatis.mkv " container="by3aau4du5w" subtitle=" " poster=" "] [/video]


----------
##基础特性
###SpringApplication
**SpringApplication**程序的主入口有一些特性。
```java
package com.atguigu.boot3features;

import org.springframework.boot.Banner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;

@SpringBootApplication //主程序类
public class Boot306FeaturesApplication {

	public static void main(String[] args) {
		//1.SpringApplication:Boot应用的核心API入口
		/*
		run方法
		参数一：注解标注的主程序类
		参数二：main中的参数args
		*/
		//SpringApplication.run(Boot306FeaturesApplication.class, args);
		//我们可以拆成两步来写，这样的好处是自定义Spring应用
		//1.自定义SpringApplication的底层设置
		//SpringApplication application = new SpringApplication(Boot306FeaturesApplication.class);

		//调整SpringApplication的参数
		//application.setDefaultProperties();

		//以Banner为例,之前我们以配置文件来配置，现在我们以程序来配置
		/*
		这个配置不优先.【配置文件优先级高于程序化调整的优先级】
		表明我们既可以通过配置文件来调整底层行为，也可以通过程序化调整底层参数
		*/
		//application.setBannerMode(Banner.Mode.OFF);

		//2.SpringApplication运行起来
		//application.run(args);
		//------------------------------------------------
		//2.通过Builder的方式，来构建出Spring应用,通过FluentBuilder API进行链式调用
		new SpringApplicationBuilder()
				//告诉SpringBoot的主程序是哪个
				.main(Boot306FeaturesApplication.class)
				//除了主程序外还需要启动源
				.sources(Boot306FeaturesApplication.class)
				.bannerMode(Banner.Mode.CONSOLE)
				//.listeners(null)
				//.environment(null)
				.run(args);

	}
}
```

----------
###Profiles
Spring Profiles 提供一种隔离配置的方式，使其仅在特定环境生效；Profiles提供了环境的隔离能力，便于我们快速切换开发、测试、生产环境。

**使用步骤**：

 - **标识环境**：指定哪些组件、配置在哪个环境下生效

```java
package com.atguigu.boot3.features;

/**
 * Profiles
 * 1.标识环境
 *      1)、区分出几个环境：dev(随便起,这里我们认为是开发环境)、test(测试环境)、prod(生产环境)
 *      2)、指定每个组件在哪个环境下生效：default环境:默认环境
 *          通过：@Profile({"test"})标注
 *          标注在类上，只有指定环境被激活，整个类的所有配置才能生效
 *          如果组件没有标注@Profile 代表任意时候都生效
 *      3)、通过测试得知：默认只有激活指定的环境，这些组件才会生效
 * 2.激活环境
 *      配置文件激活：spring.profiles.active=dev;
 *      命令行激活:java -jar xxx.jar --spring.profiles.active=dev
 *      在Edit Configurations中找到Programs arguments 然后Build ans run 设置--spring.profiles.active=dev
 *
 */
@Slf4j
@SpringBootApplication //主程序类
public class Boot306FeaturesApplication {

    public static void main(String[] args) {
        //1.SpringApplication:Boot应用的核心API入口
		/*
		run方法
		参数一：注解标注的主程序类
		参数二：main中的参数args
		*/
        //SpringApplication.run(Boot306FeaturesApplication.class, args);
        //我们可以拆成两步来写，这样的好处是自定义Spring应用
        //1.自定义SpringApplication的底层设置
        //SpringApplication application = new SpringApplication(Boot306FeaturesApplication.class);

        //调整SpringApplication的参数
        //application.setDefaultProperties();

        //以Banner为例,之前我们以配置文件来配置，现在我们以程序来配置
		/*
		这个配置不优先.【配置文件优先级高于程序化调整的优先级】
		表明我们既可以通过配置文件来调整底层行为，也可以通过程序化调整底层参数
		*/
        //application.setBannerMode(Banner.Mode.OFF);

        //2.SpringApplication运行起来
        //application.run(args);
        //------------------------------------------------
        //2.通过Builder的方式，来构建出Spring应用,通过FluentBuilder API进行链式调用
        ConfigurableApplicationContext context = new SpringApplicationBuilder()
                //告诉SpringBoot的主程序是哪个
                .main(Boot306FeaturesApplication.class)
                //除了主程序外还需要启动源
                .sources(Boot306FeaturesApplication.class)
                .bannerMode(Banner.Mode.CONSOLE)
                //.listeners(null)
                //.environment(null)
                .run(args);

        //测试环境标识检查组件中是否有这几个对象
        try {
            Cat cat = context.getBean(Cat.class);
            log.info("组件Cat:{}", cat);
        } catch (Exception e) {

        }

        try {
            Dog dog = context.getBean(Dog.class);
            log.info("组件Dog:{}", dog);
        } catch (Exception e) {

        }

        try {
            Pig pig = context.getBean(Pig.class);
            log.info("组件Pig:{}", pig);
        } catch (Exception e) {

        }
        try {
            Sheep sheep = context.getBean(Sheep.class);
            log.info("组件Sheep:{}", sheep);
        } catch (Exception e) {

        }
    }
}
```
这里写了好多类，以某个类为例。

```java
package com.atguigu.boot3.features.bean;


/**
 * @author: TangZhiKai
 * @create: 2023-09-30 17:22
 * @description: 组件多环境识别能力 ：标识Cat在测试环境下才有
 **/
@Profile({"dev"}) //标注dev环境下生效，数组可以写多个
//@Component
public class Cat {
    private Long id;
    private String name;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Cat(Long id, String name) {
        this.id = id;
        this.name = name;
    }

    public Cat() {
    }
}

```
当然，这里指定环境也可以使用**配置类中添加Bean组件的方式提供Bean类对象**，并在其方法上添加@Profile注解。但是需要注意类上的注解和方法上注解的区别。

 - **切换环境**：这个环境对应的所有组件和配置就应该生效
激活环境两种方式，在上面的 [label color="green"]Boot306FeaturesApplication[/label] 中提到了，具体自行查阅
 1. 配置文件激活： `spring.profiles.active=dev` 
 2. 命令行激活: `java -jar xxx.jar --spring.profiles.active=dev` 
####包含环境

```properties
#包含指定的环境，不管激活哪个环境，这个都要有,总是要生效的环境
spring.profiles.include=dev,test
```

[note type="primary flat"]1.**最佳实战**：
生效的环境 = 激活的环境 /默认的环境 + 包含的环境
2.项目里面这么用
①基础的配置`mybatis`、`log`、`xxx`写到包含环境中
②需要动态切换变化的用`database`、`redis`、`mq`写到激活的环境中[/note]
####环境分组

```properties
#指定激活指定的一个或多个环境
spring.profiles.active=haha

#profiles分组，需要使用的时候激活整个组就行
spring.profiles.group.haha=dev,test
spring.profiles.group.hehe=prod,abc
#也可以写成这种形式
#spring.profiles.group.haha[0]=dev
#spring.profiles.group.haha[1]=test
```
####profile配置文件

```java
/**
 * Profiles
 * 1.标识环境
 *      1)、区分出几个环境：dev(随便起,这里我们认为是开发环境)、test(测试环境)、prod(生产环境)
 *      2)、指定每个组件在哪个环境下生效：default环境:默认环境
 *          通过：@Profile({"test"})标注
 *          标注在类上，只有指定环境被激活，整个类的所有配置才能生效
 *          如果组件没有标注@Profile 代表任意时候都生效
 *      3)、通过测试得知：默认只有激活指定的环境，这些组件才会生效
 * 2.激活环境
 *      配置文件激活：spring.profiles.active=dev;
 *      命令行激活:java -jar xxx.jar --spring.profiles.active=dev
 *      在Edit Configurations中找到Programs arguments 然后Build ans run 设置--spring.profiles.active=dev
 * 3.配置文件如何使用Profile功能
 *      1)、application.properties：主配置文件，任何情况下都生效
 *      2)、其他profile环境下命名规范：application-{profile标识}.properties/yaml:
 *          比如：application-dev.properties
 *      3)、激活指定环境即可：配置文件、命令行激活
 *      4)、效果：
 *          项目的所有生效配置项 = 激活环境配置文件的所有项 + 主配置文件和激活文件不冲突的所有项
 *          如果发生了配置冲突，以激活的环境配置文件为准。
 *          application-{profile标识}.properties 优先级 application.properties
 *          
 *          主配置和激活的配置都生效，优先以激活的配置为准
 */
```
![3.png][3]


----------
##核心原理


```java
package com.atguigu.boot3.core.listener;

/**
 * @author: TangZhiKai
 * @create: 2023-10-29 17:48
 * @description: 应用监听器，监听SpringBoot应用生命周期
 * 启动的顺序就是这些方法默认调用的顺序
 **/

/**
 * 生命周期的流程分为引导、启动、运行
 * Listener先要从 META-INF/spring.factories 读到
 * 1.引导：
 *      利用BootstapContext 引导整个项目启动
 *      starting:               应用开始，SpringApplication的run方法一调用，只要有了BootstrapContext 就直接就执行
 *      environmentPrepared:    环境准备好(把启动参数等绑定到环境变量中), 但是IoC容器还没有创建；【调一次】
 * 2.启动：
 *      contextPrepared：        IoC容器创建并准备好，但是sources(主配置类)还没有加载。并关闭引导上下文；组件都没有创建【调一次】
 *      contextLoaded：          IoC容器加载，主配置类加载进去了。但是IoC还没刷新(我们的Bean没创建).
 *      ==============截止以前，IoC容器里面还没造bean呢==============
 *      started：                IoC容器刷新了(所有Bean造好了)，但是runner没调用。
 *      ready：                  IoC容器刷新了(所有Bean造好了),runner调用完成了。context.isRunning()
 * 3.运行：
 *      如果以前步骤都正确执行，代表容器running。
 */
public class MyAppListener implements SpringApplicationRunListener {

    /**
     * @param bootstrapContext 传入的是启动上下文
     * 先是启动，把基本的东西给启动起来后， 才启动后面的ConfigurableApplicationContext IoC容器
     */
    @Override
    public void starting(ConfigurableBootstrapContext bootstrapContext) {
        System.out.println("========starting=======正在启动=============");
    }

    @Override
    public void environmentPrepared(ConfigurableBootstrapContext bootstrapContext, ConfigurableEnvironment environment) {
        System.out.println("========environmentPrepared======环境准备完成===========");
    }

    @Override
    public void contextPrepared(ConfigurableApplicationContext context) {
        System.out.println("========contextPrepared======上下文(IoC容器)准备完成===========");
    }

    @Override
    public void contextLoaded(ConfigurableApplicationContext context) {
        System.out.println("========contextLoaded======IoC容器加载完成===========");
    }

    @Override
    public void started(ConfigurableApplicationContext context, Duration timeTaken) {
        System.out.println("========started======启动完成===========");
    }

    @Override
    public void ready(ConfigurableApplicationContext context, Duration timeTaken) {
        System.out.println("========ready======准备就绪===========");
    }

    @Override
    public void failed(ConfigurableApplicationContext context, Throwable exception) {
        System.out.println("========failed======应用启动失败===========");
    }
}

```


----------
###自定义starter
我们可以通过自定义starter的方式，让别人导入我们的starter，就实现对应的功能，并且对于我们提供的启动器具有一定的可扩展性。

[note type="primary flat"]场景：抽取聊天机器人场景，它可以打招呼。
效果：任何项目导入此starter都具有打招呼功能，并且问候语中的人名需要可以在配置文件中修改[/note]


----------
##场景整合
###整合Redis
导入场景启动器，然后 [label color="orange"]配置文件[/label] 中配置主机和密码，然后使用@Autowired注入就可以使用

```xml
 <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
            <!--让Redis不用lettuce作为底层客户端-->
            <!--<exclusions>
                <exclusion>
                    <groupId>io.lettuce</groupId>
                    <artifactId>lettuce-core</artifactId>
                </exclusion>
            </exclusions>-->
        </dependency>

        <!--切换Jedis作为操作redis的底层客户端,无需添加版本号，底层已经控制好了版本-->
        <!--<dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
        </dependency>-->
```
我录了一段视频，来记录，主要是过程还是有点复杂，单纯两句话说不明白。
[video title="整合Redis " url="https://img.kaijavademo.top/typecho/uploads/2023/11/%E6%95%B4%E5%90%88Redis.mkv " container="bkzab6to3" subtitle=" " poster=" "] [/video]


----------
###接口文档
前后分离的方式，后台人员写好功能以后。需要给前端暴漏接口文档，描述我们的功能，前端应该如何发请求，带什么参数，如何响应...传统的方式是写成一个word交给前端，可维护性太差了，联调不方便。我们通过整合**Swagger**，生成一个实时的接口文档，方便整个前后的沟通，而且**Swagger**遵循 [label color="blue"]OpenAPI[/label] 规范，适配性、跨平台非常好。


----------
###远程调用
无论是哪种远程调用，都需要使用响应式的包来支持

```xml
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-webflux</artifactId>
        </dependency>
```

####WebClient
除了使用postman来测试，我们可以使用WebClient模拟远程调用，**WebClient是一个非阻塞、响应式的HTTP客户端**，我们只需要创建一个WebClient，然后配置请求方式、请求路径等向服务器发送请求，并接收请求即可。

 - 通过远程调用阿里云天气控制API
 [label color="blue"]WeatherController[/label] 

```java
package com.atguigu.boot3.rpc.controller;

import com.atguigu.boot3.rpc.service.WeatherService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 14:25
 * @description: 天气控制器
 **/
@RestController
public class WeatherController {

    @Autowired
    WeatherService weatherService;

    /**
     * 测试远程
     * @param city
     * @return
     */
    //@GetMapping("/weather/{city}")
    @GetMapping("/weather")
    public Mono<String> weather(@RequestParam("city") String city){//PathVariable路径变量，或者用请求参数RequestParam来传递
        //查询天气
        Mono<String> weather = weatherService.weather(city);
        return weather;
    }
}

```

 [label color="green"]WeatherService [/label] 
```java
package com.atguigu.boot3.rpc.service;

import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.Map;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 14:27
 * @description:
 **/
@Service
public class WeatherService {

    /**
     * 使用非阻塞、响应式HTTP客户端WebClient 调用阿里云API
     * @param city
     * @return
     */
    public Mono<String> weather(String city){
        //远程调用阿里云API
        //1.创建WebClient,得到客户端
        //WebClient client = WebClient.create("https://ali-weather.showapi.com/area-to-weather-date?");
        WebClient client = WebClient.create();
        //2.准备数据
        Map<String,String> params = new HashMap<>();
        params.put("area",city);

        //3.定义发请求的行为,如果接收者是一个Mono代表非阻塞的方式 CompletableFuture
        Mono<String> mono = client.get()
                //定义发送请求路径信息 {}代表变量的方式
                .uri("https://ali-weather.showapi.com/area-to-weather-date?area={area}", params)
                //定义响应的内容类型
                .accept(MediaType.APPLICATION_JSON)
                //定义请求头
                .header("Authorization", "APPCODE xxx") //定义请求头
                //如果是POST请求，还需要定义请求体
                //.body()
                //调用查询方法
                .retrieve()
                //接收响应数据,响应体里面的数据转换成想要的类型，json->String
                .bodyToMono(String.class);

        //使用响应式编程
        //mono相当于一个发布者，我们可以使用subscribe来订阅数据
        /*Mono<String> mono = client.get()
                .uri("https://ali-weather.showapi.com/area-to-weather-date?area={area}", params)
                .accept(MediaType.APPLICATION_JSON)
                .header("Authorization", "APPCODE xxxx")
                .retrieve()
                .bodyToMono(String.class);

        mono.subscribe(val->{
            System.out.println();
        })*/

        //返回字符串的天气数据
        return mono;
    }
}

```
发送对应请求，测试，返回到页面上的都是json数据。
![4.png][4]

----------
####HttpInterface
上面的远程调用写起来感觉并不是很方便，Spring还为我们提供一种更抽象的方式。
我们只需要写一个接口，并定义好这个接口，然后**为接口创建好代理对象**，调用代理对象就行。


 [label color="green"]WeatherInterface [/label] 
```java
package com.atguigu.boot3.rpc.service;

import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.service.annotation.GetExchange;
import reactor.core.publisher.Mono;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 15:18
 * @description: 天气查询接口
 **/
public interface WeatherInterface {

    /**
     * 在接口中定义好，发什么请求，要什么东西
     * @param city
     * @return
     * @GetExchange 参数url代表给哪里发送请求，基本路径
     *              参数accept表明接收什么类型的数据 application/json
     */
    @GetExchange(url = "/area-to-weather-date",accept = "application/json") //发送Get请求，所以使用GetExchange
    //使用@RequestParam注解，谁给我传递的city参数，未来我给某个地方发送请求，我给某个值以area的参数名发送出去
    Mono<String> getWeather(@RequestParam("area") String city,
                            //定义请求头
                            @RequestHeader("Authorization") String auth);

}

```
 [label color="green"]WeatherService [/label] 
```java
@Service
public class WeatherService {

    //未来我们可以把接口写这里直接自动注入进来
    //WeatherInterface weatherInterface;
    /**
     * 使用HTTP Interface
     * @param city
     * @return
     */
    public Mono<String> weather(String city){
        //Mono<String> mono = getByWebClient(city);

        //使用接口来调用
        //1、创建客户端
        WebClient client = WebClient.builder()
                .baseUrl("https://ali-weather.showapi.com")
                .codecs(clientCodecConfigurer -> {
                    clientCodecConfigurer
                            .defaultCodecs()
                            .maxInMemorySize(256*1024*1024);
                    //响应数据量太大有可能会超出BufferSize，所以这里设置的大一点
                })
                .build();
        //2、创建工厂 HttpServiceProxyFactory接口代理工厂
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
                .builder(WebClientAdapter.forClient(client)).build();

        //3、获取代理对象
        WeatherInterface weatherAPI = factory.createClient(WeatherInterface.class);

        Mono<String> weather = weatherAPI.getWeather(city, "APPCODE xxxx");
        //返回字符串的天气数据,如果是String需要封装成一个Mono.just(weather)
        return weather;
    }
}
```
这样的方式我们还可以进行一定升级，方便我们可以把接口写好，直接自动注入进来。我们可以写一个配置类

[note type="primary flat"]抽取[/note]

WeatherConfiguration 
```java
package com.atguigu.boot3.rpc.config;

import com.atguigu.boot3.rpc.service.WeatherInterface;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 15:58
 * @description: 配置类，负责容器中放组件
 **/
@Configuration
public class WeatherConfiguration {

    @Bean
    WeatherInterface weatherInterface(){
        //1、创建客户端
        WebClient client = WebClient.builder()
                .baseUrl("https://ali-weather.showapi.com")
                .codecs(clientCodecConfigurer -> {
                    clientCodecConfigurer
                            .defaultCodecs()
                            .maxInMemorySize(256*1024*1024);
                    //响应数据量太大有可能会超出BufferSize，所以这里设置的大一点
                })
                .build();
        //2、创建工厂 HttpServiceProxyFactory接口代理工厂
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
                .builder(WebClientAdapter.forClient(client)).build();

        //3、获取代理对象
        WeatherInterface weatherInterface = factory.createClient(WeatherInterface.class);
        //以后自动注入的就是weatherInterface代理对象
        return weatherInterface;
    }
}

```
![5.png][5]

[note type="primary flat"]进一步更通用的抽取[/note]
假设我这里不止一个功能，比如我还有发短信和其他的功能，我可以将工厂抽取成一个Bean对象，放到容器中，提供一个工厂。
 [label color="green"]WeatherConfiguration[/label] 
```java
package com.atguigu.boot3.rpc.config;

import com.atguigu.boot3.rpc.service.WeatherInterface;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 15:58
 * @description: 配置类，负责容器中放组件
 **/
@Configuration
public class WeatherConfiguration {

    @Bean
    HttpServiceProxyFactory httpServiceProxyFactory(){
        //1、创建客户端
        WebClient client = WebClient.builder()
                .codecs(clientCodecConfigurer -> {
                    clientCodecConfigurer
                            .defaultCodecs()
                            .maxInMemorySize(256*1024*1024);
                    //响应数据量太大有可能会超出BufferSize，所以这里设置的大一点
                })
                .build();
        //2、创建工厂 HttpServiceProxyFactory接口代理工厂
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
                .builder(WebClientAdapter.forClient(client)).build();
        return factory;
    }
    @Bean
    WeatherInterface weatherInterface(HttpServiceProxyFactory httpServiceProxyFactory){
        //3、获取代理对象
        WeatherInterface weatherInterface = httpServiceProxyFactory.createClient(WeatherInterface.class);
        //以后自动注入的就是weatherInterface代理对象
        return weatherInterface;
    }
}

```
[note type="primary flat"]最后抽取，请求头相同的部分，我们可以抽取出来，写成一个默认的[/note]
 [label color="green"]WeatherConfiguration[/label] 
```java
package com.atguigu.boot3.rpc.config;

import com.atguigu.boot3.rpc.service.ExpressApi;
import com.atguigu.boot3.rpc.service.WeatherInterface;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

/**
 * @author: TangZhiKai
 * @create: 2023-11-29 15:58
 * @description: 配置类，负责容器中放组件
 **/
@Configuration
public class WeatherConfiguration {

    @Bean
    HttpServiceProxyFactory httpServiceProxyFactory(){
        //1、创建客户端
        WebClient client = WebClient.builder()
                //如果我需要使用阿里云的APIcode我可以在此处传递一个默认头
                .defaultHeader("Authorization","APPCODE xxxx")
                .codecs(clientCodecConfigurer -> {
                    clientCodecConfigurer
                            .defaultCodecs()
                            .maxInMemorySize(256*1024*1024);
                    //响应数据量太大有可能会超出BufferSize，所以这里设置的大一点
                })
                .build();
        //2、创建工厂 HttpServiceProxyFactory接口代理工厂
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
                .builder(WebClientAdapter.forClient(client)).build();
        return factory;
    }
    @Bean
    WeatherInterface weatherInterface(HttpServiceProxyFactory httpServiceProxyFactory){
        //3、获取代理对象
        WeatherInterface weatherInterface = httpServiceProxyFactory.createClient(WeatherInterface.class);
        //以后自动注入的就是weatherInterface代理对象
        return weatherInterface;
    }

    /**
     * <h3>模拟直接使用工厂帮他创建出代理对象，放在容器中</h3>
     * @param httpServiceProxyFactory 工厂
     * @return
     */
    @Bean
    ExpressApi expressApi(HttpServiceProxyFactory httpServiceProxyFactory){
        ExpressApi client = httpServiceProxyFactory.createClient(ExpressApi.class);
        return client;
    }
}

```
实际生产中，因为账号不一样，自然不能直接简单抽取成默认请求头中放入appcode，我们可以在 [label color="green"]配置文件[/label] 中配置， [label color="green"]aliyun.appcode=xxx[/label] ,我们可以通过字符串拼接来形成默认的请求头。
![6.png][6]
**项目一启动，我们创建好代理工厂，工厂帮我们创建好每个HttpInterface代理对象，以后所有的Controller自动注入代理对象，就能远程调用。每个接口声明了远程调用的地址，什么样的数据媒体类型，发送什么样的参数**

 [label color="green"]WeatherInterface [/label] 
```java
public interface WeatherInterface {

    /**
     * 在接口中定义好，发什么请求，要什么东西
     * @param city
     * @return
     * @GetExchange 参数url代表给哪里发送请求，基本路径
     *              参数accept表明接收什么类型的数据 application/json
     */
    @GetExchange(url = "https://ali-weather.showapi.com/area-to-weather-date",accept = "application/json") //发送Get请求，所以使用GetExchange
    //使用@RequestParam注解，谁给我传递的city参数，未来我给某个地方发送请求，我给某个值以area的参数名发送出去
    Mono<String> getWeather(@RequestParam("area") String city);

}
```


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/10/3851615313.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/10/571255085.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/10/3328242765.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/11/3544244782.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/11/1759924690.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/11/3809875083.png