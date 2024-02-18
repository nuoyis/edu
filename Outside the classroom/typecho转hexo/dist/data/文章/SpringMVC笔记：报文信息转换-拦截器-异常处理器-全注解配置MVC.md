---
title: SpringMVC笔记：报文信息转换-拦截器-异常处理器-全注解配置MVC
date: 2023-08-17 16:58:00
categories: SpringMVC
tags: [springMVC,json,ajax,拦截器,异常处理器,全注解配置MVC]
---
springMVC笔记包括报文信息转换器，拦截器源码分析，异常处理器，通过注解配置springMVC代替web.xml和springMVC.xml


<!--more-->
##HttpMessageConverter
报文信息转换器，报文包含有两个方面，请求报文和响应报文。
**请求报文**就是从浏览器发送到服务器，属于request对象，把请求报文转换成java中的一个对象。
**响应报文**是由服务器响应给浏览器的 ，服务器中使用java语言，将java对象转换成响应报文。

 - @RequestBody
 - RequestEntity
 - @ResponseBody(☆)
 - ResponseEntity

###@RequestBody
在控制器方法中设置形参，并用@RequestBody进行标识，形参所表示的就是当前请求的请求体

```java
    //在控制器中处理该请求
    @RequestMapping("/testRequestBody")
    //@RequestBody表示当前的请求参数
    public String testRequestBody(@RequestBody String requestBody) throws UnsupportedEncodingException {
        System.out.println("requestBody : " + URLDecoder.decode(requestBody,"UTF-8"));
        return "success";
    }

```
![1.png][1]


###RequestEntity
将所有的浏览器请求信息封装成一个对象，在形参中可以添加，获取请求信息。

```java
    @RequestMapping("/testRequestEntity")
    public String testRequestEntity(RequestEntity<String> requestEntity){
        //当前requestEntity表示整个请求报文的信息
        System.out.println("获取请求头信息:" + requestEntity.getHeaders());
        System.out.println("获取请求体信息:" + requestEntity.getBody());
        return "success";
    }
```
![2.png][2]


----------

要想对浏览器进行响应，可以实现一个页面跳转，然后响应浏览器一个完整的页面(转发或重定向)；或者是使用HttpServletResponse中的 `response.getWriter().print(");` 。
回顾原生方法

```java
    @RequestMapping("/testResponse")
    public void testResponse(HttpServletResponse response) throws IOException {
        /*不需要返回值，不需要返回视图名称实现页面跳转，要么return null
        要么设置为void
        将print直接作为响应报文的响应体响应到浏览器
        响应体是什么我们在浏览器中看到的就是什么
        */
        response.getWriter().print("hello,response");
    }
```


###@ResponseBody(☆)
在springMVC中实现响应浏览器的功能,为我们提供了一个注解@ResponseBody

```java
    @RequestMapping("/testResponseBody")
    @ResponseBody     /*@RequestBody用来标识当前的控制器方法，添加注解之后，
                        返回值不再是视图名称了，而是当前响应的响应体*/
    public String testResponseBody(){
        return "success";
    }

```
通过**注解**明显发现比原生API要简单一些。
![3.png][3]

----------

现在我需要响应回去一个对象，而不是一个字符串或文本之类的，就需要使用到JSON，那么就需要导入jackson的依赖
pom.xml

```xml
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.12.1</version>
        </dependency>

```

json有两种格式，一种叫**对象**，一种叫**数组**。最外层是大括号就是json对象，如果最外层是[]是json数组。
![4.png][4]
要想实现自动将 [label color="red"]java对象转换为json[/label] ，需要以下步骤：
 1. 导入jackson的**依赖**
 2. springMVC.xml中开启**mvc注解驱动**
 `<mvc:annotation-driven/>` 
 3. 处理器方法上添加@ResponseBody标识
 4. 将java对象直接作为控制器方法返回值返回，就会自动转换为**json格式的字符串** [label color="red"]不是json对象[/label] 


[note type="primary flat"]补充json信息：
①json是javascript中的一种数据格式，json是一种数据交互格式(xml也是)，现在xml最多作为配置文件，而json由于数据结构比较简单、解析简单、生成的数据量少...xml解析上和dom4j有关，**dom4j(文档对象模型)**在解析的时候将当前整个xml当成一个document然后先读取根标签，再获取子标签，一层层解析。json两种格式，都非常方便获取里面的数据。
②经常把java对象转换成json数据，实体类转换为json对象，map集合转换为json对象，list集合转换为json数组。[/note]


----------
###springMVC处理ajax
ajax本身就是不刷新(页面不发生跳转的情况下)与服务器进行交互。
index.html

```html
    <!--通过超链接发送ajax请求-->
    <div id="root">
        <a @click="testAxios" th:href="@{/testAxios}">SpringMVC处理ajax</a>
    </div>
    <!--引入文件-->
    <script type="text/javascript" th:src="@{/static/js/vue.js}"></script>
    <script type="text/javascript" th:src="@{/static/js/axios.min.js}"></script>
    <script type="text/javascript">
        new Vue({
            el:"#root",
            methods:{
                testAxios(event){
                    axios({
                        method:"post",
                        //就是触发事件的超链接的href属性
                        url:event.target.href,
                        //传输到服务器中的数据
                        params:{
                            username:"admin",
                            password:"123456"
                        }
                    }).
                    then(function(response){ //ajax请求处理成功之后要执行的函数
                        //表示响应的数据
                        alert(response.data);
                    });
                    event.preventDefault();
                }
            }
        })
    </script>
```


```java
    @RequestMapping("/testAxios")
    @ResponseBody   //当前方法返回值就是响应浏览器的数据
    public String testAxios(String username,String password){
        System.out.println("username = " + username + ",password=" + password);
        return "hello,axios";
    }

```
[video title="springMVC处理ajax " url="https://img.kaijavademo.top/typecho/uploads/2023/08/videos/2023-08-16%2015-17-53.mkv " container="bvza650muge" subtitle=" " poster=" "] [/video]
仅仅是把ajax和springMVC响应浏览器数据一起使用了。只有要把java对象响应到浏览器的时候才需要使用jackson。


----------
###@RestController注解(☆)

 - 以后浏览器和服务器之间的交互使用的都是json，在SpringBoot和SpringCloud的微服务中，微服务中就是以业务逻辑为边界，将完整工程分成一个一个单独运行、单独部署的小工程中。每个小工程中都是一个微服务，微服务之间使用json + http数据交互。
微服务里面**每一个控制器方法**都要加 [label color="red"]@ResponseBody [/label] ，注解将使用非常之多，所以说mvc为我们提供了一个派生注解 [label color="blue"]@RestController注解[/label]当前控制器中所有的控制器方法，所有的返回值都是作为响应浏览器数据的响应体存在的。
 - 使用此注解相当于同时为当前方法提供了**@Controller**和**@ResponseBody注解**


----------

###ResponseEntity
可以将ResponseEntity属于一个**自定义的响应报文**，此控制器方法返回值就是响应到浏览器的响应报文。
可以配合下面的文件上传下载使用。

----------

##文件下载和上传
###文件下载
通过ResponseEntity实现下载
```java
@Controller
public class FileUpAndDownController {

    @RequestMapping("/testDown")
    //控制器方法 ResponseEntity
    public ResponseEntity<byte[]> testResponseEntity(HttpSession session) throws IOException {
        //获取ServletContext对象(表示当前整个工程)
        ServletContext servletContext = session.getServletContext();
        //获取服务器中文件的真实路径
        String realPath = servletContext.getRealPath("/static/img/1.png");
        //创建输入流
        InputStream is = new FileInputStream(realPath);
        //创建字节数组 is.available() 获取当前输入流对应文件的所有字节数
        byte[] bytes = new byte[is.available()];
        //将输入流所有的字节读到字节数组中,把数组响应到浏览器，就是要下载的文件
        is.read(bytes);
        //创建HttpHeaders对象设置响应头信息，接口，使用实现类创建对象HttpHeaders
        MultiValueMap<String, String> headers = new HttpHeaders();
        /*设置要下载方式以及下载文件的名字，只有=后面的文件名可以修改。
        attachment以附件的方式下载 filename为下载文件设置默认名*/
        headers.add("Content-Disposition", "attachment;filename=1.png");
        //设置响应状态码
        HttpStatus statusCode = HttpStatus.OK;
        //转换成ResponseEntity,创建ResponseEntity对象，有三个参数(响应报文)
        /*
        参数一：bytes存放了要下载到文件中所有字节(响应体)
        参数二：响应头
        参数三：状态码
        */
        ResponseEntity<byte[]> responseEntity = new ResponseEntity<>(bytes, headers, statusCode);
        //关闭输入流
        is.close();
        //responseEntity响应到浏览器
        return responseEntity;
    }
}

```
对于下载来说，可改动的地方很少，格式比较固定。
###文件上传
对于文件上传来说，是不可以使用get请求
首先需要写一个上传的form表单，然后写具体的控制器方法
控制器中方法的书写流程

 - pom文件中导入jackson依赖
 - 导入上传功能的依赖jar包 `commons-fileupload` 
pom.xml
```xml
<dependency>
<groupId>commons-fileupload</groupId>
<artifactId>commons-fileupload</artifactId>
<version>1.3.1</version>
</dependency>

```

 - 添加MultipartFile以及对应input标签名(name)photo
 - 上传的文件不能直接转换成MultipartFile，设置文件上传解析器（配置bean标签）
springMVC.xml

```xml
    <!--配置文件上传解析器,将上传的文件封装为MultipartFile对象
    springIoC容器将自动访问，实现转换的过程,
    class = 对应接口MultipartFile的实现类CommonsMultipartResolver
    CommonsMultipartResolver是通过id获取的(bean标签必须要配置id要记住啊)
    id="multipartResolver" 必须得是，不然获取不到bean
    -->
    <bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver"></bean>
```
这里一定要**配置bean**，我差点把bean标签忘记配置id属性了(555，还没反应过来被老师骂了)

 - 获取对应的文件名
 - 获取项目运行目录的路径
 - 判断
 - 最终路径拼接
 - 上传到服务器

```java
    @RequestMapping("/testUp")
    public String testUp(MultipartFile photo,HttpSession session) throws IOException {
        //实现上传功能
        /*
        导入jackson依赖，和jar包.添加形参名和上传的input标签中的name保持一致，
        在mvc中将上传文件封装到了一个MultipartFile,跟我们上传文件的信息
        已经操作已经封装好了，当前上传的文件不能直接转换成MultipartFile
        获取服务器路径需要有session
        */
        String fileName = photo.getOriginalFilename();//获取所上传的文件名
        ServletContext servletContext = session.getServletContext();//根据session获取到servletContext对象
        //servletContext.getRealPath("photo");获取项目运行目录的路径。获取到photo的路径
        String photoPath = servletContext.getRealPath("photo");
        File file = new File(photoPath);
        //判断photoPath所对应路径是否存在
        if(!file.exists()){
            //若不存在创建目录
            file.mkdir();
        }

        //最终路径 = photoPath + 路径分隔符(不知道使用哪个斜线使用File.separator替代) + 上传文件名
        String finalPath = photoPath +File.separator + fileName;
        photo.transferTo(new File(finalPath));//上传/转移到服务器
        //上传成功后跳转到success页面
        return "success";
    }

```
当前程序会有一个问题，文件名同名的情况下，会覆盖掉其他人上传的同名文件。
使用****UUID****这样一个32位的随机序列作为文件名，对文件名处理替换，将当前文件名采用UUID替换，但是文件后缀还需要保留。对当前的控制层方法略加修改完善

```java
    @RequestMapping("/testUp")
    public String testUp(MultipartFile photo, HttpSession session) throws IOException {

        //获取上传的文件的文件名
        //实现上传功能
        /*
        导入jackson依赖，和jar包.添加形参名和上传的input标签中的name保持一致，
        在mvc中将上传文件封装到了一个MultipartFile,跟我们上传文件的信息
        已经操作已经封装好了，当前上传的文件不能直接转换成MultipartFile
        获取服务器路径需要有session
        */
        String fileName = photo.getOriginalFilename();//获取所上传的文件名

        //获取上传的文件的后缀名
        String suffixName = fileName.substring(fileName.lastIndexOf("."));

        //将UUID作为文件名
        String uuid = UUID.randomUUID().toString().replaceAll("-","");
        //将uuid和后缀名拼接后的结果作为最终的文件名
        fileName = uuid + suffixName;

        //根据session获取到servletContext对象
        ServletContext servletContext = session.getServletContext();
        //通过servletContext获取服务器中photo目录的路径
        String photoPath = servletContext.getRealPath("photo");
        File file = new File(photoPath);
        //判断photoPath所对应路径是否存在
        if (!file.exists()) {
            //若不存在创建目录
            file.mkdir();
        }

        //最终路径 = photoPath + 路径分隔符(不知道使用哪个斜线使用File.separator替代) + 上传文件名
        String finalPath = photoPath + File.separator + fileName;
        photo.transferTo(new File(finalPath));//上传/转移到服务器
        //上传成功后跳转到success页面
        return "success";
    }

```

----------

##拦截器
 -->|Request|A[Filter] --> B(DispatcherServlet) -->C|拦截器1|[preHandle] --> D(拦截器2) --> E[postHandle]

除了preHandle、postHandle以外，还有一个**afterComplation**，是在我们渲染视图之后执行的。
![5.png][5]
扩展一下mvc的注解驱动，主要是添加配置拦截器
springMVC.xml

```xml
    <!--开启MVC的注解驱动-->
    <mvc:annotation-driven>
        <mvc:message-converters>
            <!--处理响应中文内容乱码-->
            <bean class="org.springframework.http.converter.StringHttpMessageConverter">
                <property name="defaultCharset" value="UTF-8"/>
                <property name="supportedMediaTypes">
                    <list>
                        <value>text/html</value>
                        <value>application/json</value>
                    </list>
                </property>
            </bean>
        </mvc:message-converters>
    </mvc:annotation-driven>

    <!--配置拦截器-->
    <mvc:interceptors>
        <!--可以配置多个拦截器-->
        <!--将bean配置在里面，表示当前某一个类型的对象就是一个拦截器
        不用加id，因为mvc靠全类名就能找到
        -->
        <bean class="com.atguigu.mvc.interceptors.FirstInterceptor"></bean>
    </mvc:interceptors>

```

 - [label color="red"]此时配置的拦截器是对DispatcherServlet所处理的所有的请求进行拦截 [/label]
  
FirstInterceptor类
```java
@Component
public class FirstInterceptor implements HandlerInterceptor {
    /*拦截器的两种方式
    ①让该类实现HandlerInterceptor接口
    ②让该类继承HandlerInterceptorAdapter类(已过时)
    接口中是有方法体的默认方法，我们选择重写
    按住ctrl + o 进行重写*/

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        /*此方法有当前是否进行放行，false表示拦截，true表示放行*/
        System.out.println("FirstInterceptor --->preHandle");
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("FirstInterceptor --->postHandle");
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        System.out.println("FirstInterceptor --->afterCompletion");
    }
}
```

![6.png][6]
我们可以使用[MVC支持ant风格的路径][7]，所谓的模糊查询，来进行测试

 - 当然也有另外一种方式给FirstInterceptor设置普通层组件(注解)，并且在springMVC.xml中添加ref标签



```xml
    <!--配置拦截器-->
    <mvc:interceptors>
        <ref bean="firstInterceptor"></ref>
    </mvc:interceptors>
```

实际上这两种方式是**一致**的，因为无法对于bean标签设置一定的拦截规则，所以这两种方式 [label color="red"]都默认对所有请求进行拦截[/label] 。

###手动配置拦截器
当然interceptors标签中我们可以配置多个interceptor，第三种拦截方式就是这样编写的，我们可以手动编写拦截规则。
我们可以编写一个访问首页不会被拦截，而点击按钮跳转到对应页面触发拦截器的规则。
 -  `<mvc:mapping path="/*"/>` 表示拦截表示我们访问上下文路径下面的一层目录。我们可以使用 [label color="red"]/**[/label] 拦截多级路径
springMVC.xml
```xml
    <!--配置拦截器-->
    <mvc:interceptors>
        <!--<bean class="com.atguigu.mvc.interceptors.FirstInterceptor"></bean>-->
        <!--<ref bean="firstInterceptor"></ref>-->
        <!--第三种方式-->
        <mvc:interceptor>
            <!--通过mapping设置拦截路径 /*表示我们访问上下文路径下面的一层目录
            /**表示拦截多级路径-->
            <mvc:mapping path="/*"/>
            <!--设置把哪个请求映射排除掉-->
            <mvc:exclude-mapping path="/"/>
            <!--指定bean-->
            <ref bean="firstInterceptor"></ref>
        </mvc:interceptor>
    </mvc:interceptors>

```


----------
###多个拦截器的执行顺序

[note type="primary flat"]preHandle()会按照配置的顺序执行，而postHandle()和afterComplation()会按照配置的反序执行[/note]
通过书写两个拦截器，来进行测试
![7.png][8]
翻看源码：
![8.png][9]

如果说我在preHandle这个布尔方法中传递false，那么在底层源码中postHandle一定一个都不会执行，而afterCompletion会执行，而afterCompletion执行的时候，遍历几个拦截器和interceptorIndex(拦截器返回false之前的拦截器索引)有关。也就是说
假设有多个拦截器，第三个拦截器返回false。那么 `interceptor.preHandle(request, response, this.handler)` 返回false取反执行if中的语句，然后从第二个拦截器倒着遍历（执行 `this.triggerAfterCompletion(request, response, (Exception)null);` ），遍历到第一个拦截器。

 - preHandle返回false**和**之前的拦截器一定会执行
 - postHandle一个都不会执行
 - afterCompletion中**preHandle返回false之前的拦截器**会执行，根据索引执行，索引最大 = 返回false之前的拦截器索引


源码
```java
    boolean applyPreHandle(HttpServletRequest request, HttpServletResponse response) throws Exception {
        for(int i = 0; i < this.interceptorList.size(); this.interceptorIndex = i++) {
            HandlerInterceptor interceptor = (HandlerInterceptor)this.interceptorList.get(i);
            if (!interceptor.preHandle(request, response, this.handler)) {
                this.triggerAfterCompletion(request, response, (Exception)null);
                return false;
            }
        }

        return true;
    }

```

----------
##异常处理器
springMVC提供了一套异常处理器HandlerExceptionResolver，它有多个实现类
![9.png][10]
我们可以通过**配置文件**或者是**注解**的方式来实现自定义配置异常处理，将可能会出现的异常配置到异常映射中，出现指定异常就会跳转到对应页面。
###基于配置的异常处理
在bean标签中为 [label color="blue"]properties属性赋值[/label] 
springMVC.xml

```xml
    <!--配置异常处理-->
    <bean class="org.springframework.web.servlet.handler.SimpleMappingExceptionResolver">
        <property name="exceptionMappings">
            <props>
                <!--prop表示其中的一个键值对
                key 写的就是指定的异常的全类名，标签体中(双标签中写的是value)写一个新的视图名称,
                跳转到指定页面
                -->
                <prop key="java.lang.ArithmeticException">error</prop>
            </props>
        </property>

        <!-- 设置将异常信息共享在请求域中的键，value=""配置，默认存储到当前的请求域中的键-->
        <property name="exceptionAttribute" value="ex"></property>
    </bean>
```
![10.png][11]

----------
###基于注解的异常处理
springMVC也为我们提供了一套注解，通过注解也可以来实现异常处理

```java
@ControllerAdvice //说明注解包含了@Component的功能,也具有将类标识为组件的功能
public class ExceptionController {
    @ExceptionHandler(value = {
            //书写当前可能会出现的异常,书写某个类型的Class对象
            ArithmeticException.class,
            NullPointerException.class
            //如果当前出现了上述异常，就会通过注解所标识的方法来作为新的控制器方法执行
    })
    public String testException(Exception ex, Model model) {
        /*控制器出现了指定异常，执行我们当前指定的方法作为新方法
        通过添加形参Exception可以获得异常信息,然后往请求域中共享数据*/
        model.addAttribute("ex",ex);
        return "error";
    }
}
```

----------
##通过注解配置SpringMVC(☆)
通过配置类和注解代替web.xml和SpringMVC配置文件(springMVC.xml)功能。
###初始化类代替web.xml
web.xml是作为当前web工程的描述符，每当启动Tomcat服务器，web.xml第一个作为加载的配置文件。

> Spring3.2引入了一个便利的WebApplicationInitializer基础实现，名为
AbstractAnnotationConfigDispatcherServletInitializer，当我们的类扩展了
AbstractAnnotationConfigDispatcherServletInitializer并将其部署到Servlet3.0容器的时候，容器会自
动发现它，并用它来配置Servlet上下文。

###创建初始化类WebInit

```java
/**
 * TODO web工程的初始化类
 * 用来代替web.xml
 * 除了注册DispatcherServlet以外还需要注册过滤器
 */
public class WebInit extends AbstractAnnotationConfigDispatcherServletInitializer {

    @Override
    protected Class<?>[] getRootConfigClasses() {
        /*
        此方法来获取当前的一个根配置，指定的就是spring的配置类
        在没有对应配置类的情况下创建一个长度为0Class数组
        有对应SpringConfig配置类的情况下，将配置类放在数组中返回

        */
        return new Class[]{SpringConfig.class};
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        /*
        此方法是来指定SpringMVC的配置类
        */
        return new Class[]{WebConfig.class};
    }

    @Override
    protected String[] getServletMappings() {
        /*
        此方法是来获取DispatcherServlet的映射路径(<url-pattern>)
        */
        return new String[]{"/"};
    }


    @Override
    protected Filter[] getServletFilters() {
        /*此方法发是用来注册过滤器的，两个过滤器*/
        CharacterEncodingFilter characterEncodingFilter = new CharacterEncodingFilter();
        characterEncodingFilter.setEncoding("UTF-8");
        characterEncodingFilter.setForceResponseEncoding(true);
        HiddenHttpMethodFilter hiddenHttpMethodFilter = new HiddenHttpMethodFilter();
        
        return new Filter[]{characterEncodingFilter,hiddenHttpMethodFilter};
    }
}

```
![11.png][12]

----------
###配置视图解析器
这里我们基于之前所学将一个最完整的springMVC.xml配置出来,一个完整的配合文件不光需要视图模板，也需要配置其他的很多组件。我在注释中一 一列举出来，之后使用原生配置xml也是一个比较完整的配置思路。
在我们创建出的 [label color="blue"]WebConfig类[/label] 中配置

```java
package com.atguigu.mvc.config;

import com.atguigu.mvc.interceptor.TestInterceptor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.context.ContextLoader;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.multipart.MultipartResolver;
import org.springframework.web.multipart.commons.CommonsMultipartResolver;
import org.springframework.web.servlet.HandlerExceptionResolver;
import org.springframework.web.servlet.ViewResolver;
import org.springframework.web.servlet.config.annotation.*;
import org.springframework.web.servlet.handler.SimpleMappingExceptionResolver;
import org.thymeleaf.spring5.SpringTemplateEngine;
import org.thymeleaf.spring5.view.ThymeleafViewResolver;
import org.thymeleaf.templatemode.TemplateMode;
import org.thymeleaf.templateresolver.ITemplateResolver;
import org.thymeleaf.templateresolver.ServletContextTemplateResolver;

import java.util.List;
import java.util.Properties;

/**
 * TODO 代替SpringMVC的配置文件(springMVC.xml)
 * 1.扫描组件 2.视图解析器 3，view-controller对首页的访问 4.default-servlet-handler开放对静态资源的访问
 * 5.mvc注解驱动 6.文件上传解析器 7.异常处理 8.拦截器
 * */
//将当前类标识为一个配置类
@Configuration
//1.开启MVC的自动扫描组件
@ComponentScan("com.atguigu.mvc.controller")
//5.开启MVC的注解驱动
@EnableWebMvc
public class WebConfig implements WebMvcConfigurer {//添加接口，实现除了thymeleaf的其他组件

    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        /*4.default-servlet-handler开放对静态资源的访问*/
        configurer.enable();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        /*8.拦截器
        创建一个拦截器，实现HandlerInterceptor接口，并重写.(可以参照上面文章拦截器)
        创建对象，添加一定的拦截规则
        addPathPatterns()添加拦截路径(可写多个)
        excludePathPatterns()排除拦截路径(可写多个)
        */
        TestInterceptor testInterceptor = new TestInterceptor();
        registry.addInterceptor(testInterceptor).addPathPatterns("/**");
    }

    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        /*3，view-controller对首页的访问
            addViewController("") 设置路径
            setViewName           设置视图名称
        */
        registry.addViewController("/hello").setViewName("hello");
    }

    @Bean
    public MultipartResolver multipartResolver(){
        /*
        6.文件上传解析器
        因为是MultipartResolver一个接口，所以说使用返回它的实现类对象
        平时是在bean标签中配置，所以说要添加@Bean注解
        */
        CommonsMultipartResolver commonsMultipartResolver = new CommonsMultipartResolver();
        return commonsMultipartResolver;
    }

    @Override
    public void configureHandlerExceptionResolvers(List<HandlerExceptionResolver> resolvers) {
        /*7.异常处理
        可以配置成Bean的形式，也可以使用这个方法实现
        创建异常处理解析器，并添加到形参的集合中
        创建Properties对象，使用setProperty/getProperty
        setExceptionAttribute设置异常信息请求域中的键
        */
        SimpleMappingExceptionResolver exceptionResolver = new SimpleMappingExceptionResolver();
        Properties prop = new Properties();
        prop.setProperty("java.lang.ArithmeticException","error");
        exceptionResolver.setExceptionMappings(prop);

        exceptionResolver.setExceptionAttribute("exception");

        resolvers.add(exceptionResolver);
    }

    /*
          配置视图解析器
        */
    //配置生成模板解析器thymeleaf(可复制，比起jsp比较麻烦)
    @Bean//加上该注解返回值就是IoC容器中的一个Bean
    public ITemplateResolver templateResolver() {
        WebApplicationContext webApplicationContext = ContextLoader.getCurrentWebApplicationContext();
        // ServletContextTemplateResolver需要一个ServletContext作为构造参数，可通过WebApplicationContext 的方法获得
        ServletContextTemplateResolver templateResolver = new ServletContextTemplateResolver(
                webApplicationContext.getServletContext());
        templateResolver.setPrefix("/WEB-INF/templates/");
        templateResolver.setSuffix(".html");
        templateResolver.setCharacterEncoding("UTF-8");
        templateResolver.setTemplateMode(TemplateMode.HTML);
        return templateResolver;
    }

    //生成模板引擎并为模板引擎注入模板解析器 ,
    //同下面viewResolver方法一致的是形参位置使用了自动装配@Autowired
    @Bean
    public SpringTemplateEngine templateEngine(ITemplateResolver templateResolver) {
        SpringTemplateEngine templateEngine = new SpringTemplateEngine();
        templateEngine.setTemplateResolver(templateResolver);
        return templateEngine;
    }

    //生成视图解析器并未解析器注入模板引擎
    @Bean
    public ViewResolver viewResolver(SpringTemplateEngine templateEngine) {
        ThymeleafViewResolver viewResolver = new ThymeleafViewResolver();
        viewResolver.setCharacterEncoding("UTF-8");
        viewResolver.setTemplateEngine(templateEngine);
        return viewResolver;
    }
    
}

```

----------
##SpringMVC的常用组件

 - DispatcherServlet：前端控制器，不需要工程师开发，由框架提供
统一处理请求响应，**整个流程的控制中心**，通过它调用其他组件处理用户请求。
 - HandlerMapping：处理器映射器，不需要工程师开发，由框架提供
请求的url、方法与控制器之间**创建映射**。 [label color="blue"]找[/label] 
 - Controller(Handler)：控制器(处理器)，需要工程师开发
在**DispatcherServlet**的控制下**控制器**对用户请求进行处理。
 - HandlerAdapter：处理器适配器，不需要工程师开发，由框架提供
处理器适配器，来调用对应的**控制器**方法。 [label color="blue"]执行[/label] 
 - ViewResolver：视图解析器，不需要工程师开发，由框架提供
页面跳转，得到对应的视图，视图就是由**视图解析器解析**，不同的视图名称，创建不同的视图，进行渲染。有[三种MVC视图][13]
 - View：视图
视图解析器解析**视图名称**得到的视图，为用户展示模型数据。

----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。



  [1]: https://img.kaijavademo.top/typecho/uploads/2023/08/4188229586.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/233617547.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/1037918313.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/993652465.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/3051769476.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/1468886383.png
  [7]: https://www.kaijavademo.top/259.html#cl-16
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/08/2459309173.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/08/2079516676.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/08/3039863265.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/08/3594125855.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/08/4026853463.png
  [13]: https://www.kaijavademo.top/296.html#cl-12
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/08/1002034034.png