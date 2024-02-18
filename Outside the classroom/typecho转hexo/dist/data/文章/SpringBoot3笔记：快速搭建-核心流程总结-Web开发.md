---
title: SpringBoot3笔记：快速搭建-核心流程总结-Web开发
date: 2023-10-01 08:19:00
categories: SpringBoot
tags: [SpringBoot集成,SpringBoot3,核心流程总结,YML,函数式Web]
---
基于JDK17 + SpringBoot3的入门笔记，


<!--more-->
##快速搭建 + 常用注解

[video title="快速搭建 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E5%BF%AB%E9%80%9F%E6%90%AD%E5%BB%BA.mkv " container="beu1prgsiin" subtitle=" " poster=" "] [/video]



![1.png][1]

###常用注解
[video title="常用注解 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E5%B8%B8%E7%94%A8%E6%B3%A8%E8%A7%A3.mkv " container="baqik9157t" subtitle=" " poster=" "] [/video]


```java
/**
 * @author: TangZhiKai
 * @create: 2023-09-30 17:24
 * @description: 配置类
 **/
@Import(FastsqlException.class) //导入第三方类进入IoC容器，给容器中放指定类型的组件，组件的名字默认是全类名
@SpringBootConfiguration //这是一个配置类，替代以前的配置文件.配置类本身也是容器中的组件
//@Configuration //这是一个配置类，替代以前的配置文件.配置类本身也是容器中的组件
public class AppConfig {

    /**
     * 1.组件默认是单实例的
     * @return
     */
    @Scope("prototype") //可以修改为多实例
    @Bean("userHaha") //替代以前的Bean标签.组件在容器中的名字默认是方法名
    //可以直接修改注解的值在Bean标签中
    public User user(){
        User user = new User();
        user.setId(1L);
        user.setName("张三");
        return  user;
    }

    /*@Bean
    public FastsqlException fastsqlException(){
        return  new FastsqlException();
    }*/
}

```
###条件注解

如果注解指定的条件成立，则触发指定行为

 - @ConditionalOnClass：如果类路径中存在这个类，则触发指定行为
 - @ConditionalOnMissingClass：如果类路径中不存在这个类，则触发指定行为
 - @ConditionalOnBean：如果容器中存在这个Bean(组件)，则触发指定行为
 - @ConditionalOnMissingBean：如果容器中不存在这个Bean(组件)，则触发指定行为
....

```java
//@ConditionalOnClass可以直接标到类上，当系统中存在这个类，以下所有东西全部生效
//放在类级别，如果注解判断生效，则整个配置类才生效
@ConditionalOnClass(name = "com.alibaba.druid.FastsqlException")
@SpringBootConfiguration
public class AppConfig2 {

    //当类路径中存在这个FastsqlException类，则生效
    //放在方法级别，只是单独对这个方法进行注解判断
    @ConditionalOnClass(name = "com.alibaba.druid.FastsqlException")
    @Bean
    public Cat cat01() {
        return new Cat();
    }

    @ConditionalOnMissingClass(value = "com.alibaba.druid.FastsqlException")
    @Bean
    public Dog dog01() {
        return new Dog();
    }

    //当容器中有dog的对象，就向容器中添加一个张三
    @ConditionalOnBean(value = Dog.class)
    @Bean
    public User zhangsan() {
        return new User();

    }

    //当容器中没有dog对象，就向容器中添加一个李四
    @ConditionalOnMissingBean(value = Dog.class)
    @Bean
    public User lisi() {
        return new User();

    }
}
```

###属性绑定
将容器中任意组件(Bean)的属性值和配置文件的配置项进行绑定
 - @ConfigurationProperties： 声明组件的属性和配置文件哪些前缀开始项进行绑定
![2.png][2]
 - @EnableConfigurationProperties：快速注册注解,也用于导入第三方写好的组件进行属性绑定。(=@Import + @ConfigurationProperties)SpringBoot默认只扫描自己主程序所在的包，如果导入第三方包，即使组件标注了**@Component、@ConfigurationProperties**注解也没用，因为组件扫描不进来。
**使用方法：**
 1. 给容器中注册组件(@Component、@Bean)
 2. 使用 [label color="purple"]@ConfigurationProperties声明组件和配置文件的哪些配置项进行绑定[/label] 

[video title="属性绑定 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E5%B1%9E%E6%80%A7%E7%BB%91%E5%AE%9A.mkv " container="bbbqtqjhwcw" subtitle=" " poster=" "] [/video]


----------
##核心流程总结
对于自动配置流程的一个核心流程总结：
 1. 导入`starter` 场景启动器 ,就会导入`autoconfigure`包。
 2. `autoconfigure`包里面有一个文件`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`，里面指定所有启动要加载的自动配置类。
 3. @EnableAutoConfiguration 会自动的把上面的文件里面写的所有**自动配置类都导入进来**。`xxxAutoConfiguration`**是有条件注解进行按需加载**。
 4. `xxxAutoConfiguration`给容器中导入一堆组件，组件都是从`xxxProperties`中提取属性值
 5. `xxxProperties`又是和**配置文件**进行了绑定
**效果**：导入`starter`、修改配置文件，就能修改底层行为。

###自我的角度谈谈如何学好

下面是我自己对于springboot学习的一个流程小总结，留有视频以便回顾。
[video title="浅谈 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E6%B5%85%E8%B0%88%E7%90%86%E8%A7%A3%E5%AD%A6%E4%B9%A0.mkv " container="bl0yl656oip" subtitle=" " poster=" "] [/video]


----------
##Web开发

 - 最佳实践：**给容器中写一个配置类@Configuration实现 WebMvcConfigurer但是不要标注 @EnableWebMvc注解(此注解表示禁用自动配置效果)，实现手自一体的效果。**

###自定义静态资源的配置规则
自定义静态资源路径、自定义缓存规则
####配置方式
 - spring.mvc:静态资源访问前缀路径
 - spring.web:①静态资源目录②静态资源缓存策略

```properties
# 一.spring.web:
# 1.配置国际化的区域信息
# 2.配置静态资源策略(是否功能开启、处理链、缓存)

#开启静态资源映射规则
spring.web.resources.add-mappings=true

# 设置缓存
spring.web.resources.cache.period=3600
# 缓存详细合并项控制，覆盖period配置：浏览器第一次请求服务器，服务器告诉浏览器此资源缓存7200秒，浏览器就会把它放到本地7200秒
# 7200秒以内的所有此资源访问不用发给服务器请求，7200秒以后发请求给服务器
spring.web.resources.cache.cachecontrol.max-age=7200
# 设置共享缓存，表明这些静态资源是共享缓存
spring.web.resources.cache.cachecontrol.cache-public=true
# 使用资源last-modified 最后一次修改时间，来对比服务器和浏览器的资源是否相同没有发生变化 ,如果相同返回304
spring.web.resources.cache.use-last-modified=true

#spring.web下面专门负责静态资源的规则配置，缓存时间...
#spring.web.

# 自定义静态资源文件夹，会扫描当前静态资源文件夹下的文件
spring.web.resources.static-locations=classpath:/a/,classpath:/b/,classpath:/static/

#2. spring.mvc
## 2.1 自定义webjars访问路径前缀
spring.mvc.webjars-path-pattern=/wj/**
## 2.2 静态资源通用的访问路径前缀
spring.mvc.static-path-pattern=/static/**

```
####代码方式
 [label color="red"]容器中只要有一个 WebMvcConfigurer 组件。配置的底层行为都会生效[/label] 

 - 第一种实现方式
采用手动挡+自动挡的实现方式，在主程序下面书写一个配置类，然后添加**@Configuration**,并实现 [label color="blue"]WebMvcConfigurer[/label] 接口，重写接口中的方法。

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-06 14:12
 * @description: 配置类
 **/
//@EnableWebMvc //禁用boot的默认配置，慎用，注意这里不要添加
@Configuration //告诉SpringBoot这是一个配置类，采用手自一体的方式
public class MyConfig implements WebMvcConfigurer {
    /*配置类最好在主程序下面，因为SpringBoot默认一启动，会扫描主程序下面的包以及子包*/

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        //保留以前规则，可不写
        WebMvcConfigurer.super.addResourceHandlers(registry);

        //自己添加一些静态资源规则，也就是在默认配置的情况下添加了许多其他配置
        //添加一个addResourceHandler，指明访问路径 类似于localhost:8080/static/**
        registry.addResourceHandler("/static/**")
                //访问static路径下的所有，就来到 a文件夹，b文件夹
                .addResourceLocations("classpath:/a/","classpath:/b/")
                //设置缓存设置，指定最大存储时间，存储时间单位
                .setCacheControl(CacheControl.maxAge(1180, TimeUnit.SECONDS));
    }
}
```
 - 第二种实现方式
给容器中放一个WebMvcConfigurer组件，就能自定义底层。

```java
//@EnableWebMvc //禁用boot的默认配置，慎用，注意这里不要添加
@Configuration //告诉SpringBoot这是一个配置类，采用手自一体的方式

public class MyConfig /*implements WebMvcConfigurer*/ {
    /*配置类最好在主程序下面，因为SpringBoot默认一启动，会扫描主程序下面的包以及子包*/

    @Bean //或者是给容器中放一个WebMvcConfigurer组件，就能自定义底层。
    public WebMvcConfigurer webMvcConfigurer(){
        //采用适配器思路，只实现我们需要实现的方法即可
        return  new WebMvcConfigurer() {
            @Override
            public void addResourceHandlers(ResourceHandlerRegistry registry) {
                registry.addResourceHandler("/static/**")
                        //访问static路径下的所有，就来到 a文件夹，b文件夹
                        .addResourceLocations("classpath:/a/","classpath:/b/")
                        //设置缓存设置，指定最大存储时间，存储时间单位
                        .setCacheControl(CacheControl.maxAge(1180, TimeUnit.SECONDS));

            }
        };
    }

  /*  @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        //保留以前规则，可不写
        WebMvcConfigurer.super.addResourceHandlers(registry);

        //自己添加一些静态资源规则，也就是在默认配置的情况下添加了许多其他配置
        //添加一个addResourceHandler，指明访问路径 类似于localhost:8080/static/**
        registry.addResourceHandler("/static/**")
                //访问static路径下的所有，就来到 a文件夹，b文件夹
                .addResourceLocations("classpath:/a/","classpath:/b/")
                //设置缓存设置，指定最大存储时间，存储时间单位
                .setCacheControl(CacheControl.maxAge(1180, TimeUnit.SECONDS));
                }
   */

}

```

[note type="primary flat"]为什么容器中放一个`WebMvcConfigurer`就能配置底层行为(生效)?
1.WebMvcAutoConfiguration是一个自动配置类，它里面有一个`EnableWebMvcConfiguration`。
2.`EnableWebMvcConfiguration`继承于`DelegatingWebMvcConfiguration`,这两个都生效。
3.`DelegatingWebMvcConfiguration`利用DI(依赖注入)把容器中所有`WebMvcConfigurer`注入进来。
4.别人调用`DelegatingWebMvcConfiguration`的方法配置底层规则，而它调用所有`WebMvcConfigurer`的配置底层的方法。[/note]

流程优点麻烦，视频讲两句啦:)

[video title="静态资源配置 " url="https://img.kaijavademo.top/typecho/uploads/2023/10/videos/%E7%BC%96%E5%86%99%E9%9D%99%E6%80%81%E8%B5%84%E6%BA%90%E9%85%8D%E7%BD%AE.mkv " container="bgm9fbu7tb" subtitle=" " poster=" "] [/video]

----------
###路径匹配
以前MVC中我们使用[Ant的风格路径][3]，现在新版使用**PathPatternParser**

[note type="info flat"]总结：
Ⅰ.直接使用默认的路径匹配规则，是由 `PathPatternParser`提供的；
Ⅱ.如果路径中间需要有**，在配置文件中替换成ant风格路径[/note]

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-06 15:02
 * @description:
 **/
@RestController
@Slf4j
public class HelloController {

    /**
     * 默认使用新版本的路径匹配器PathPatternParser
     * 优点：性能极高
     * 缺点：不能适配ant风格路径 ** 在中间的，剩下的都可以和antPathMatcher语法兼容
     *
     * @param request
     * @param path
     * @return
     */
    @GetMapping("/a*/b?/{p1:[a-f]+}/**")//所谓的ant风格路径
    public String hello(HttpServletRequest request , @PathVariable("p1") String path){
        //* 很多字符 ?一个字符 [a-f]限定范围
        log.info("路径变量p1: {}" ,path);
        String url = request.getRequestURI();
        return url;
    }
}
```
当然我们可以手动在配置文件中修改
application.properties

```properties
#改变路径匹配策略：
# ant_path_matcher 老版策略；
# path_pattern_parser 新版策略；
spring.mvc.pathmatch.matching-strategy=ant_path_matcher
```

----------
##Thymeleaf整合
关于对于Thymeleaf的学习，我将Springboot整合，并写在thymeleaf的文章中了，[点我跳转][4]

----------
##错误处理
SpringMVC的错误处理机制依然保留，MVC处理不了的，才会交给boot进行处理。
**SpringBoot对于错误处理有一套自己的机制：**

[note type="info flat"]**1.解析一个错误页**：
a.如果发生了**500、404、503、403**这些错误
①如果有**模板引擎**，默认在`classpath:/templates/error/精确码.html`寻找
②如果没有模板引擎，在静态资源文件夹static下找`精确码.html`
b.如果匹配不到`精确码.html`这些精确的错误页，就去找模糊码对应的错误页，就去找`5xx.html`,`4xx.html`**模糊匹配**
①如果有模板引擎，默认在`classpath:/templates/error/5xx.html`寻找
②如果没有模板引擎，在静态资源文件夹static下找`5xx.html`
2.如果模板引擎templates下有`error.html`页面，就直接渲染，如果没有就自动提供一个error的页面。[/note]

大体来说就是能精确匹配就精确匹配，有模板引擎就找对应模板引擎目录下面的页面，没有就去找静态资源。


----------
##函数式Web
以前我们需要通过 [label color="blue"]@Controller + @RequestMapping[/label] 这种方式，而SpringMVC认为这种是 耦合式 的方式敲代码。所谓耦合，就是路由、业务耦合，所有的路由匹配，和业务，都写到Controller层里面。而SpringMVC推荐一种 [label color="red"]函数式[/label] 写法。将路由业务抽离出来，业务集中写道一个地方，路由抽离出来写到另外一个地方，这样路由如果出问题，不需要翻各个Controller类，集中在一处看我们的路由定义就行。

[note type="flat"]场景：实现Restful的CRUD案例来对用户user进行增删改查[/note]

 - GET /user/1  获取1号用户
 - GET /users   获取所有用户
 - POST /user  请求体携带JSON，新增一个用户
 - PUT /user/1 请求体携带JSON，修改1号用户
 - DELETE /user/1 删除1号用户
以前就是在Controller层中写对应请求的Mapping注解，然后写对应的业务逻辑的实现。
WebFunctionConfig.controller
```java

/**
 * @author: TangZhiKai
 * @create: 2023-10-20 18:01
 * @description: 实现Restful的对于用户的CRUD功能
 **/

/**
 * ● GET /user/1  获取1号用户
 * ● GET /users   获取所有用户
 * ● POST /user  请求体携带JSON，新增一个用户
 * ● PUT /user/1 请求体携带JSON，修改1号用户
 * ● DELETE /user/1 删除1号用户
 */
@Configuration
public class WebFunctionConfig {
    //定义路由信息
    /**
     * 函数式Web的步骤：
     * 1.给容器中放一个Bean: 类型是RouterFunction<ServerResponse>
     *     userRoute用户的路由定义信息，所谓的路由定义就是什么请求跳到哪里
     * 2.每个业务准备一个自己的Handler，抽取成一个biz文件夹
     *
     * 核心四大对象
     * 1.RouterFunction: 定义路由信息，发什么请求，谁来处理？
     * 2.RequestPredicate：请求谓语。请求方式(GET、POST、DELETE..）、请求参数
     * 3.ServerRequest：封装请求完整数据
     * 4.ServerResponse：服务器响应，封装响应完整数据
     * */

    @Bean
    public RouterFunction<ServerResponse> userRoute(){

        //RouterFunction的工具类，构建RouterFunction
        RouterFunctions.route() //开始定义路由信息
                /*
                参数一pattern： 路径 /user/{id} 我希望id是动态的
                参数二predicate：由谁处理,启用RequestPredicates工具类帮我们构建请求谓语，accept()表示接收什么样的类型
                    如果是 MediaType.ALL表示接收任意的媒体类型的参数
                参数三HandlerFunction:函数式接口，接收request返回ServerResponse
                    使用lambda表达式，接收请求，做方法体内部做 业务处理，构造响应
                    ServerResponse.ok()通过build构建器方法返回。
                因为要查一个用户，就模拟有一个person，如果想要将查到的用户以Json的形式响应,
                通过.body(person)传递
                这只是一个Get请求,如果真的写这个，业务处理非常长，优化的写法我们专门写一个处理器handler专门来做参数三的事情
                抽取出来，请看biz文件夹
                */
                .GET("/user/{id}", RequestPredicates.accept(MediaType.ALL),request -> {
                    //业务处理
                    Person person = new Person(1L,"haha","aa@qq.com",18,"admin");
                    //构造响应
                    return ServerResponse
                            .ok()
                            .body(person);
                });

        return null;
    }

}

```

[note type="primary flat"]这样写比较冗长，我们把参数三的**业务处理和响应部分抽取**出来，抽取成一个方法，然后加入到IOC容器中，通过形参注入，然后使用**方法引用**简化格式。[/note]

完整的CRUD
WebFunctionConfig

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-20 18:01
 * @description: 实现Restful的对于用户的CRUD功能
 **/

/**
 * ● GET /user/1  获取1号用户
 * ● GET /users   获取所有用户
 * ● POST /user  请求体携带JSON，新增一个用户
 * ● PUT /user/1 请求体携带JSON，修改1号用户
 * ● DELETE /user/1 删除1号用户
 */
@Configuration
public class WebFunctionConfig {
    //定义路由信息
    /**
     * 函数式Web的步骤：
     * 1.给容器中放一个Bean: 类型是RouterFunction<ServerResponse>,集中所有路由信息
     *     userRoute用户的路由定义信息，所谓的路由定义就是什么请求跳到哪里
     * 2.每个业务准备一个自己的Handler(业务处理器)，抽取放在一个biz文件夹
     *     业务处理器中对应的方法格式同HandlerFunction接口一致，然后我们需要在userRoute形参处传递处理器
     *     表明如果方法里面参数是一个对象，默认就会从容器中拿取(这就是为什么处理器要添加Component注解，这样写就自动注入进来了)
     *
     * 核心四大对象
     * 1.RouterFunction: 定义路由信息，发什么请求，谁来处理？
     * 2.RequestPredicate：请求谓语。请求方式(GET、POST、DELETE..)、请求参数
     * 3.ServerRequest：封装请求完整数据
     * 4.ServerResponse：服务器响应，封装响应完整数据
     * */

    @Bean
    public RouterFunction<ServerResponse> userRoute(UserBizHandler userBizHandler/*这个会被自动注入进来*/){
            //RouterFunction的工具类，构建RouterFunction
        return RouterFunctions.route() //开始定义路由信息
                        /*
                        参数一pattern： 路径 /uer/{id} 我希望id是动态的
                        参数二predicate：由谁处理,启用RequestPredicates工具类帮我们构建请求谓语，accept()表示接收什么样的类型
                            如果是 MediaType.ALL表示接收任意的媒体类型的参数
                        参数三HandlerFunction:函数式接口，接收request返回ServerResponse
                            使用lambda表达式，接收请求，做方法体内部做 业务处理，构造响应
                            ServerResponse.ok()通过build构建器方法返回。ServerResponse.ok().build();
                        因为要查一个用户，就模拟有一个person，如果想要将查到的用户以Json的形式响应,
                        通过.body(person)构造响应
                        这只是一个Get请求,如果真的写这个，业务处理非常长，优化的写法我们专门写一个处理器handler专门来做参数三的事情
                        抽取出来，请看biz文件夹
                        */
                        .GET("/user/{id}", RequestPredicates.accept(MediaType.ALL),userBizHandler::getUser/*调用当前实例的getUser方法*/)
                        .GET("/users",userBizHandler::getUsers)
                        //因为这里是需要请求体需要携带JSON数据，所以需要指定媒体类型APPLICATION_JSON
                        .POST("/user",RequestPredicates.accept(MediaType.APPLICATION_JSON),userBizHandler::saveUser)
                        .PUT("/user/{id}",RequestPredicates.accept(MediaType.APPLICATION_JSON),userBizHandler::updateUser)
                        .DELETE("user/{id}",userBizHandler::deleteUser)
                        //构建好所有路由信息.build(); ,而这样最后就会是一个RouterFunction<ServerResponse>
                        //直接添加到方法返回值的位置就可以了
                        .build();
    }
    //未来其他的增删改查.....
    @Bean
    public RouterFunction<ServerResponse> groupRoute(UserBizHandler userBizHandler/*这个会被自动注入进来*/){
        return RouterFunctions.route()
                .GET("/user/{id}", RequestPredicates.accept(MediaType.ALL)
                        //请求谓语
                        //这里可以拓展请求规则，通过and，不仅接收json类型的数据，而且请求参数里面还得是aa的值为bb才给予处理
                                .and(RequestPredicates.param("aa","bb"))
                        ,userBizHandler::getUser/*调用当前实例的getUser方法*/)
                .GET("/users",userBizHandler::getUsers)
                .POST("/user",RequestPredicates.accept(MediaType.APPLICATION_JSON),userBizHandler::saveUser)
                .PUT("/user/{id}",RequestPredicates.accept(MediaType.APPLICATION_JSON),userBizHandler::updateUser)
                .DELETE("user/{id}",userBizHandler::deleteUser)
                .build();
    }
}

```
/biz/UserBizHandler

```java
/**
 * @author: TangZhiKai
 * @create: 2023-10-20 18:24
 * @description: 用户的业务处理器，专门处理User有关的业务,提供一个方法来专门做这件事(代替路由信息的参数三)
 **/
@Slf4j
@Component //Service也可以
public class UserBizHandler {

    /**
     * 查询指定id的用户
     * 该方法是要替换路由信息参数三位置的lambda表达式
     * 参数三需要HandlerFunction，我们也需要返回ServerResponse，接收ServerRequest
     */
    public ServerResponse getUser(ServerRequest request) throws Exception {

        /*
        形参中request封装了所有的请求数据
        这里我们获取路径变量，日志输出查询的几号用户。除此之外可以获取请求路径，请求头
        */
        String id = request.pathVariable("id");
        log.info("查询用户[{}]信息完成,数据库正在检索", id);

        log.info("查询某个用户信息完成");
        //业务处理
        Person person = new Person(1L, "haha", "aa@qq.com", 18, "admin");
        //构造响应
        return ServerResponse
                .ok()
                .body(person);
    }

    /**
     * 获取所有用户
     *
     * @param request
     * @return
     * @throws Exception
     */
    public ServerResponse getUsers(ServerRequest request) throws Exception {
        log.info("查询所有用户信息完成");
        //业务处理
        //模拟所有用户
        List<Person> list = Arrays.asList(new Person(1L, "haha", "aa1@qq.com", 18, "admin"),
                new Person(2L, "哈哈2", "aa2@qq.com", 12, "admin2"));

        //构造响应
        return ServerResponse
                .ok()
                //查询到的所有用户写出去
                .body(list);//凡是body中的对象，就是以前的@ResponseBody原理，利用HttpMessageConverter写出为json

    }

    /**
     * 保存用户
     *
     * @param request
     * @return
     */
    public ServerResponse saveUser(ServerRequest request) throws ServletException, IOException {
        //提取请求体：请求体中body数据封装成json返回
        Person body = request.body(Person.class);
        //使用@Slf4j日志记录，没必要真连接数据库
        log.info("保存用户信息:{}", body);
        //响应成功
        return ServerResponse.ok().build();
    }


    /**
     * 更新用户
     *
     * @param request
     * @return
     */
    public ServerResponse updateUser(ServerRequest request) throws ServletException, IOException {
        Person body = request.body(Person.class);
        log.info("用户信息更新:{}", body);
        return ServerResponse.ok().build();
    }

    /**
     * 删除用户
     * @param request
     * @return
     */
    public ServerResponse deleteUser(ServerRequest request) {
        String id = request.pathVariable("id");
        log.info("删除[{}]用户信息",id);
        return ServerResponse.ok().build();
    }
}
```

----------


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/10/627071249.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/10/2024873568.png
  [3]: https://www.kaijavademo.top/259.html#cl-17
  [4]: https://www.kaijavademo.top/261.html#cl-1