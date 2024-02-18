---
title: Spring笔记：面向切面AOP的两种实现
date: 2023-08-01 15:04:00
categories: Spring6
tags: [Spring6,AOP,面向切面编程]
---
spring笔记，有关spring中另一个核心技术AOP的理解。


<!--more-->
涉及到代理设计模式(后面会更新)
静态代理中由于将某些代码写死，降低了一定的扩展性，所以说后来产生了动态代理，而AOP的底层就是基于动态代理.关于静态代理不做过多赘述，笔记中以AOP的实现为主延伸动态代理。
##动态代理
```java
public class ProxyFactory 
    //目标对象传递CalculatorImpl
    private Object target;

    //把目标对象传递进来
    public ProxyFactory(Object target) {
        this.target = target;
    }

    //创建一个方法，返回代理对象（动态）
    public Object getProxy() {
        //动态代理创建对象
        /*
        Proxy.newProxyInstance()方法有三个参数
        参数一：ClassLoader:加载动态生成代理类的类加载器
        参数二：Class[] interfaces:目标对象实现所有接口class类型数组(数组结构)
        参数三：InvocationHandler:设置代理对象实现目标对象目标方法的过程
        */

        //参数一：ClassLoader:加载动态生成代理类的类加载器
        ClassLoader classLoader = target.getClass().getClassLoader();

        //参数二：Class[] interfaces:目标对象实现所有接口class类型数组(数组结构)
        Class<?>[] interfaces = target.getClass().getInterfaces();

        //参数三：InvocationHandler:设置代理对象实现目标对象目标方法的过程
        InvocationHandler invocationHandler = new InvocationHandler() {
            //InvocationHandler是一个接口，使用匿名内部类来实现invoke方法

            //参数一：代理对象
            //参数二：需要重写的目标对象的方法
            //参数三：method方法里面的参数
            @Override
            public Object invoke(Object proxy,
                                 Method method,
                                 Object[] args) throws Throwable {
                //方法调用之前做输出
                System.out.println("[动态代理][日志] " + method.getName() + "，参数：" + Arrays.toString(args));

                //调用目标的方法
                Object result = method.invoke(target, args);


                //方法调用之后做个输出
                System.out.println("[动态代理][日志] " + method.getName() + "，结果：" + result);
                return result;
            }
        };

        return Proxy.newProxyInstance(classLoader, interfaces, invocationHandler);

    }
}

```


----------
##AOP
AOP是一种设计思想，**它以通过预编译的方式和运行期动态代理方式实现，在不修改原代码的情况下，给程序动态统一添加额外功能的技术**。使得各个业务逻辑各部分之间耦合度降低。
相关知识点
 - 横切关注点：我们在方法中抽取一些同样一类的非核心业务，比如：用户验证、事务处理
 - 通知(增强)：增强的功能，比如：用户的安全校验，事务，日志...通过方法进行实现的叫做通知方法。
 - 动态代理分类：**JDK的动态代理**(有接口的情况。生成一个接口实现类的代理对象，代理对象和目标对象**实现了相同的接口**)和**cglib的动态代理**(没有接口的情况。生成一个子类的代理对象，**继承**被代理目标类)
 - AspectJ：是AOP框架，Spring只是借用了AspectJ中的注解实现了AOP功能。

----------

###注解方式实现AOP
 1. 引入AOP相关依赖
父工程中添加依赖

```xml
<!--spring aop依赖-->
<dependency>
<groupId>org.springframework</groupId>
<artifactId>spring-aop</artifactId>
<version>6.0.2</version>
</dependency>
<!--spring aspects依赖-->
<dependency>
<groupId>org.springframework</groupId>
<artifactId>spring-aspects</artifactId>
<version>6.0.2</version>
</dependency>

```
子工程resources文件中添加xml文件，调整配置信息，开启组件扫描

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
http://www.springframework.org/schema/beans/spring-beans.xsd
http://www.springframework.org/schema/context
http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/aop
http://www.springframework.org/schema/aop/spring-aop.xsd">
    <!--开启组件扫描-->
    <context:component-scan base-package="com.atguigu.spring6.aop.annoaop"></context:component-scan>

    <!--开启AspectJ自动代理，为我们的目标对象生成一个代理,让Spring认识@Aspect注解-->
    <aop:aspectj-autoproxy></aop:aspectj-autoproxy>


</beans>
```


 2. 创建目标资源
 - 接口

```java
public interface Calculator {

    public abstract int add(int i, int j);

    public abstract int sub(int i, int j);

    public abstract int mul(int i, int j);

    public abstract int div(int i, int j);

}

```

 - 实现类

```java
//最基本的实现类，实现了加减乘除
@Component
public class CalculatorImpl implements Calculator {


    @Override
    public int add(int i, int j) {
        int result = i + j;
        System.out.println("方法内部 result = " + result);
        return result;
    }

    @Override
    public int sub(int i, int j) {
        int result = i - j;
        System.out.println("方法内部 result = " + result);
        return result;

    }

    @Override
    public int mul(int i, int j) {
        int result = i * j;
        System.out.println("方法内部 result = " + result);
        return result;
    }

    @Override
    public int div(int i, int j) {
        int result = i / j;
        System.out.println("方法内部 result = " + result);
        return result;
    }

}
```
 3. 创建一个切面类
 - 切入点
 - 通知类型

```java
//切面类
@Aspect //表示它是一个切面类
@Component//交给spring IoC容器进行管理
public class LogAspect {

    //设置切入点和通知类型
    //切入点表达式execution(访问修饰符 增强方法返回的类型 方法所在类型的全类名(增强方法所在类的全路径).方法名(参数列表))

    //通知类型：
    // @Before(value = "切入点表达式 配置切入点")前置通知
    //以前置为例

    @Before(value = "execution(public int com.atguigu.spring6.aop.annoaop.CalculatorImpl.add(..))")
    public void beforeMethod(){
        System.out.println("Logger-->前置通知");

    }

    // @AfterReturning返回通知
    // @AfterThrowing异常通知
    // @After()后置通知
    // @Around()环绕通知
    // 每种通知类型需要添加方法，添加注解
}
```
这里面有个最重要的切入点表达式
![2.png][1]
测试
![3.png][2]

然后完善剩下四种通知。

```java
//切面类
@Aspect  //表示它是一个切面类
@Component //交给spring IoC容器进行管理
public class LogAspect {

    //设置切入点和通知类型
    //切入点表达式execution(访问修饰符 增强方法返回的类型 方法所在类型的全类名(增强方法所在类的全路径).方法名(参数列表))

    //通知类型：
    // @Before(value = "切入点表达式 配置切入点")前置通知
    //以前置为例

    @Before(value = "execution(public int com.atguigu.spring6.aop.annoaop.CalculatorImpl.add(..))")
    public void beforeMethod(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        //用joinPoint里面获取前置通知里面的参数
        Object[] args = joinPoint.getArgs();
        System.out.println("Logger-->前置通知,增强方法名称:" + methodName + ",参数为:" + Arrays.toString(args));

    }

    // @After()后置通知
    @After(value = "execution(* com.atguigu.spring6.aop.annoaop.CalculatorImpl.*(..))")
    public void afterMethod(JoinPoint joinPoint) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->后置通知,增强方法名称:" + methodName);
    }


    // @AfterReturning返回通知
    //后置通知在返回之后执行
    //返回通知：它能得到增强目标方法的返回值
    @AfterReturning(value = "execution(* com.atguigu.spring6.aop.annoaop.CalculatorImpl.*(..))", returning = "result")
    public void afterReturningMethod(JoinPoint joinPoint, Object result) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->返回通知,增强方法名称:" + methodName + ",返回结果" + result);


    }


    // @AfterThrowing异常通知
    //目标方法执行过程中，出现了异常，这个通知会执行，能够获取到目标方法的异常信息

    @AfterThrowing(value = "execution(* com.atguigu.spring6.aop.annoaop.CalculatorImpl.*(..))", throwing = "ex")
    public void afterThrowingMethod(JoinPoint joinPoint, Throwable ex) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->异常通知,增强方法名称:" + methodName + ",异常信息：" + ex);
    }


    // @Around()环绕通知,可以呈现出上面四种效果，在之前之后都会执行
    @Around("execution(* com.atguigu.spring6.aop.annoaop.CalculatorImpl.*(..))")
    public Object aroundMethod(ProceedingJoinPoint joinPoint) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        String arg = Arrays.toString(args);
        Object result = null;
        try {
            System.out.println("环绕通知 == 目标方法之前执行");

            //调用目标方法

            result = joinPoint.proceed();

            System.out.println("环绕通知 == 目标方法返回值之后执行");
        } catch (Throwable throwable) {

            throwable.printStackTrace();
            System.out.println("环绕通知 == 目标方法出现异常执行");
        } finally {
            System.out.println("环绕通知 == 目标方法执行完毕执行");
        }

        return result;
    }
}
```
![4.png][3]
![5.png][4]

----------
###重用切入点表达式
考虑到上面切入点表达式每次使用都是同一种情况，重复书写，抽取。
实际上写成一个单独的方法，提供切入点表达式，需要加上 [label color="red"]@Pointcut[/label] ,括号中传递切入点表达式

```java
    //重用切入点表达式
    @Pointcut(value = "execution(* com.atguigu.spring6.aop.annoaop.CalculatorImpl.*(..))")
    public void pointCut(){
    }

```
在需要使用切入点表达式的时候，直接调用方法，当然还要考虑到是不是同一个切面。
![6.png][5]

----------
###基于XML的AOP
把之前**@Aspect**以及**通知注解**删除，调整对应切面类

```java
//切面类
@Component //交给spring IoC容器进行管理
public class LogAspect {

    //前置通知
    public void beforeMethod(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        //用joinPoint里面获取前置通知里面的参数
        Object[] args = joinPoint.getArgs();
        System.out.println("Logger-->前置通知,增强方法名称:" + methodName + ",参数为:" + Arrays.toString(args));

    }
    //后置通知
    public void afterMethod(JoinPoint joinPoint) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->后置通知,增强方法名称:" + methodName);
    }


    //返回通知,获取目标方法的返回值
    public void afterReturningMethod(JoinPoint joinPoint, Object result) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->返回通知,增强方法名称:" + methodName + ",返回结果" + result);


    }


    //异常通知
    public void afterThrowingMethod(JoinPoint joinPoint, Throwable ex) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        System.out.println("Logger-->异常通知,增强方法名称:" + methodName + ",异常信息：" + ex);
    }


    //环绕通知
    public Object aroundMethod(ProceedingJoinPoint joinPoint) {
        //通过省略的参数joinPoint可以获得相关信息
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();
        String arg = Arrays.toString(args);
        Object result = null;
        try {
            System.out.println("环绕通知 == 目标方法之前执行");

            //调用目标方法

            result = joinPoint.proceed();

            System.out.println("环绕通知 == 目标方法返回值之后执行");
        } catch (Throwable throwable) {

            throwable.printStackTrace();
            System.out.println("环绕通知 == 目标方法出现异常执行");
        } finally {
            System.out.println("环绕通知 == 目标方法执行完毕执行");
        }

        return result;
    }


    //重用切入点表达式
    @Pointcut(value = "execution(* com.atguigu.spring6.aop.xmlaop.CalculatorImpl.*(..))")
    public void pointCut() {
    }


}

```
补充spring的XML文件，在XML文件中配置五种通知类型

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd
    http://www.springframework.org/schema/context
    http://www.springframework.org/schema/context/spring-context.xsd
    http://www.springframework.org/schema/aop
    http://www.springframework.org/schema/aop/spring-aop.xsd">

    <!--开启组件扫描-->
    <context:component-scan base-package="com.atguigu.spring6.aop.xmlaop"></context:component-scan>

    <!--配置AOP五种通知类型-->
    <aop:config>
        <!--配置切面类，找到对应切面类，首字母小写作为ref值-->
        <aop:aspect ref="logAspect">
            <!--配置切入点 id表示给切入点起名，可随便；expression表示切入点表达式-->
            <aop:pointcut id="pointcut" expression="execution(* com.atguigu.spring6.aop.xmlaop.CalculatorImpl.*(..))"/>
            <!--配置五种通知类型，指定方法名作为对应通知-->

            <!--前置通知 pointcut-ref指定切入点id-->
            <aop:before method="beforeMethod" pointcut-ref="pointcut"></aop:before>
            <!--后置通知-->
            <aop:after method="afterMethod" pointcut-ref="pointcut"></aop:after>
            <!--返回通知-->
            <aop:after-returning method="afterReturningMethod" returning="result" pointcut-ref="pointcut"></aop:after-returning>
            <!--异常通知-->
            <aop:after-throwing method="afterThrowingMethod" throwing="ex" pointcut-ref="pointcut"></aop:after-throwing>
            
            <!--环绕通知-->
            <aop:around method="aroundMethod" pointcut-ref="pointcut"></aop:around>

        </aop:aspect>
    </aop:config>


</beans>
```
最后测试类中读取该xml文件即可。
![7.png][6]
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/08/1366368922.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/08/4280707642.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/08/4268811129.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/08/3890681685.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/08/936714672.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/08/4205508216.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/08/192368281.jpg