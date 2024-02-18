---
title: Spring笔记：实现手写核心IoC步骤
date: 2023-07-31 14:29:00
categories: Spring6
tags: [Spring6,手写IoC]
---
通过手写代码，写出spring框架最核心的部分
之前在**JavaWeb**中的学习里一段初步手写**IoC**可供参考和跳转[初步学习][1]

<!--more-->

实现过程

 1. 创建子模块()引入依赖
 2. 创建测试类和接口（service dao）
 3. 创建(手写)两个注解，实现IoC功能
 - **@Bean** 创建对象
 - **@Di** 属性注入
 4. 创建Bean容器接口 [label color="blue"]ApplicationContext[/label] ,定义方法，返回对象
 5. 实现Bean容器接口，实现类中功能
 - 返回对象
 - 根据包的扫描规则，加载bean
扫描规则:
比如包是**com.atguigu**
扫描com.atguigu这个包，和他的**子包**里面的所有类，扫描这个上面是否有@Bean注解，如果有，那就把这个类通过**反射**进行**实例化**。

----------
###准备工作
简单来说就是通过手写代码的方式实现两个注解(对应第三步)
![1.png][2]
创建两个注解类，配置方式如下
![2.png][3]
创建bean容器接口并实现(第四步)
![3.png][4]
###实现容器接口(第五步：实现第一个注解)
**@Bean创建对象**
我们创建一个集合，重写接口中的方法，通过getBean方法，在集合中获取，返回我们需要的对应类的对象。
在有参数的构造当中，我们需要编写对应的扫描规则。
首先我们需要获取对应包的绝对路径，同时添加一个简化路径的变量**rootPath**方便后面扫描，根据路径添加一个扫描包的方法 [label color="blue"]loadBean[/label] 随后我们具体实现扫描包的方法。

```java
public class AnnotationApplicationContext implements ApplicationContext {

    //创建map集合，放bean实例对象
    private Map<Class, Object> beanFactory = new HashMap<>();

    //简化路径
    private static String rootPath;

    //此方法用于返回我们创建的对象
    @Override
    public Object getBean(Class clazz) {
        //根据key返回对象
        return beanFactory.get(clazz);
    }

    //设置包的扫描规则
    //当前包及其子包里面，哪个类有@Bean注解，把这个类通过反射进行实例化
    //创建有参数构造，传递包的路径basePackage，设置扫描规则
    //public AnnotationApplicationContext(String basePackage) throws IOException {
    public static void pathdemo1(String basePackage) {
        try {
            //设置包的扫描规则 com.atguigu.spring6
            //找到这个包所在的路径，找到绝对路径，看一下文件夹中是否有子文件夹和文件
            //1.把.替换成\
            String packagePath = basePackage.replaceAll("\\.", "\\\\");

            //2.获取包的绝对路径
            Enumeration<URL> urls = Thread.currentThread().getContextClassLoader().getResources(packagePath);
            while (urls.hasMoreElements()) {
                //遍历，得到里面的每一个具体值
                URL url = urls.nextElement();
                //转码
                String filePath = URLDecoder.decode(url.getFile(), "utf-8");

                //获取包前面的路径部分，用作字符串截取
                rootPath = filePath.substring(0, filePath.length() - packagePath.length());

                //根据路径进行包扫描过程
                loadBean(new File(filePath));

            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


    }

    public static void main(String[] args) {
        pathdemo1("com.atguigu");

    }
}
```
###@Bean创建对象
实现loadBean方法的大致思路如下

```java
    //包扫描过程，实例化
    private static void loadBean(File file) {
        //1.判断当前文件是否文件夹

        //2.是文件夹，获取文件夹中里面的所有内容

        //3.判断文件夹里面内容为空，直接返回


        //4.如果文件夹里面不为空，遍历文件夹里面的所有内容

        //4.1遍历得到每部分内容file对象，继续判断，如果还是文件夹，递归


        //4.2如果遍历得到的file对象，不是一个文件夹，是文件
        
        //4.3得到包路径 + 类名称部分 --->字符串截取


        //4.4判断当前文件的类型是否是.class类型

        //是，反射

        //4.5如果是.class类型，把路径中的\替换成.  把.class去掉
        //com.atguigu.service.UserServiceImpl

        
        //4.6判断类上面是否有注解@Bean，如果有，进行实例化过程

        //4.7把对象实例化之后，放到Map集合中beanFactory去
        
        //4.7.1判断当前类有接口，让接口作为key
        
        //4.7.2判断当前类没有接口，让自己作为key

        

    }

```

----------
 [label color="red"]实现包扫描过程，用反射进行实例化，按照步骤完成。[/label] 


```java
    //包扫描过程，实例化
    private void loadBean(File file) throws Exception {
        //1.判断当前文件是否文件夹
        if (file.isDirectory()) {
            //2.是文件夹，获取文件夹中里面的所有内容
            File[] childrenFiles = file.listFiles();

            //3.判断文件夹里面内容为空，直接返回
            if (childrenFiles == null || childrenFiles.length == 0) {
                return;
            }

            //4.如果文件夹里面不为空，遍历文件夹里面的所有内容
            for (File child : childrenFiles) {
                //4.1遍历得到每部分内容file对象，继续判断，如果还是文件夹，递归
                if (child.isDirectory()) {
                    //递归的方式
                    loadBean(child);
                } else {
                    //4.2如果遍历得到的file对象，不是一个文件夹，是文件
                    //4.3得到包路径 + 类名称部分 --->字符串截取

                    String pathWithClass = child.getAbsolutePath().substring(rootPath.length() - 1);

                    //4.4判断当前文件的类型是否是.class类型
                    if (pathWithClass.contains(".class")) {

                        //4.5如果是.class类型，把路径中的\替换成.  把.class去掉
                        //com.atguigu.service.UserServiceImpl
                        String allName = pathWithClass.replaceAll("\\\\", ".")
                                .replace(".class", "");

                        //4.6判断类上面是否有注解@Bean，如果有，进行实例化过程
                        //4.6.1得到了类的全路径，获取类的class对象
                        Class<?> clazz = Class.forName(allName);

                        //4.6.2判断不是接口，才进行实例化
                        if (!clazz.isInterface()) {
                            //4.6.3判断类上面是否有注解@Bean
                            Bean annotation = clazz.getAnnotation(Bean.class);
                            if (annotation != null) {
                                //表示类有注解
                                //4.6.4对象 进行实例化
                                Object instance = clazz.getDeclaredConstructor().newInstance();
                                //4.7把对象实例化之后，放到Map集合中beanFactory去
                                //4.7.1判断当前类有接口，让接口class作为key
                                if (clazz.getInterfaces().length > 0) {
                                    beanFactory.put(clazz.getInterfaces()[0], instance);

                                } else {
                                    //4.7.2判断当前类没有接口，让自己class作为key
                                    beanFactory.put(clazz, instance);
                                }


                            }
                        }
                    }
                }
            }
        }
    }
```
 [label color="red"]最终源码，实现@Bean创建对象 + 扫描[/label] 

```java
package com.atguigu.bean;

import com.atguigu.anno.Bean;

import java.io.File;
import java.net.URL;
import java.net.URLDecoder;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;

public class AnnotationApplicationContext implements ApplicationContext {

    //创建map集合，放bean实例对象

    private Map<Class, Object> beanFactory = new HashMap<>();

    //简化路径
    private static String rootPath;


    //此方法用于返回我们创建的对象
    @Override
    public Object getBean(Class clazz) {
        //根据key返回对象
        return beanFactory.get(clazz);
    }

    //设置包的扫描规则
    //当前包及其子包里面，哪个类有@Bean注解，把这个类通过反射进行实例化
    //创建有参数构造，传递包的路径basePackage，设置扫描规则
    public AnnotationApplicationContext(String basePackage) {
        try {
            //设置包的扫描规则 com.atguigu.spring6
            //找到这个包所在的路径，找到绝对路径，看一下文件夹中是否有子文件夹和文件
            //1.把.替换成\
            String packagePath = basePackage.replaceAll("\\.", "\\\\");

            //2.获取包的绝对路径
            Enumeration<URL> urls = Thread.currentThread().getContextClassLoader().getResources(packagePath);
            while (urls.hasMoreElements()) {
                //遍历，得到里面的每一个具体值
                URL url = urls.nextElement();
                //转码
                String filePath = URLDecoder.decode(url.getFile(), "utf-8");

                //获取包前面的路径部分，用作字符串截取

                rootPath = filePath.substring(0, filePath.length() - packagePath.length());


                //根据路径进行包扫描过程
                loadBean(new File(filePath));

            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }


    }


    //包扫描过程，实例化
    private void loadBean(File file) throws Exception {
        //1.判断当前文件是否文件夹
        if (file.isDirectory()) {
            //2.是文件夹，获取文件夹中里面的所有内容
            File[] childrenFiles = file.listFiles();

            //3.判断文件夹里面内容为空，直接返回
            if (childrenFiles == null || childrenFiles.length == 0) {
                return;
            }

            //4.如果文件夹里面不为空，遍历文件夹里面的所有内容
            for (File child : childrenFiles) {
                //4.1遍历得到每部分内容file对象，继续判断，如果还是文件夹，递归
                if (child.isDirectory()) {
                    //递归的方式
                    loadBean(child);
                } else {
                    //4.2如果遍历得到的file对象，不是一个文件夹，是文件
                    //4.3得到包路径 + 类名称部分 --->字符串截取

                    String pathWithClass = child.getAbsolutePath().substring(rootPath.length() - 1);

                    //4.4判断当前文件的类型是否是.class类型
                    if (pathWithClass.contains(".class")) {

                        //4.5如果是.class类型，把路径中的\替换成.  把.class去掉
                        //com.atguigu.service.UserServiceImpl
                        String allName = pathWithClass.replaceAll("\\\\", ".")
                                .replace(".class", "");

                        //4.6判断类上面是否有注解@Bean，如果有，进行实例化过程
                        //4.6.1得到了类的全路径，获取类的class对象
                        Class<?> clazz = Class.forName(allName);

                        //4.6.2判断不是接口，才进行实例化
                        if (!clazz.isInterface()) {
                            //4.6.3判断类上面是否有注解@Bean
                            Bean annotation = clazz.getAnnotation(Bean.class);
                            if (annotation != null) {
                                //表示类有注解
                                //4.6.4对象 进行实例化
                                Object instance = clazz.getDeclaredConstructor().newInstance();
                                //4.7把对象实例化之后，放到Map集合中beanFactory去
                                //4.7.1判断当前类有接口，让接口class作为key
                                if (clazz.getInterfaces().length > 0) {
                                    beanFactory.put(clazz.getInterfaces()[0], instance);

                                } else {
                                    //4.7.2判断当前类没有接口，让自己class作为key
                                    beanFactory.put(clazz, instance);
                                }


                            }
                        }
                    }
                }
            }
        }
    }
    
}

```
浅浅的测试一下。
![4.png][5]

----------
###@Bi属性注入
 [label color="red"]进行@Di注解的注入属性实现，添加一个方法loadDi()[/label] 

```java
    //进行属性的注入
    private void loadDi() {
        //实例化对象在beanFactory的map集合中里面
        //1.遍历beanFactory的map集合


        //2.获取map集合的每个对象(value)，每个对象中的属性获取到


        //3.遍历得到的每个对象属性的数组，得到里面的每个属性


        //4.判断属性上面是否有@Di注解
        //如果私有属性，设置可以设置值


        //5.如果有@Di注解，把对象进行设置(注入)



    }
```

根据注解完成对应的核心实现。

```java
    //进行属性的注入
    private void loadDi() {
        //实例化对象在beanFactory的map集合中里面
        //1.遍历beanFactory的map集合

        Set<Map.Entry<Class, Object>> entries = beanFactory.entrySet();
        for (Map.Entry<Class, Object> entry : entries) {
            //2.获取map集合的每个对象(value)，每个对象中的属性获取到
            Object obj = entry.getValue();

            //获取对象的class
            Class<?> clazz = obj.getClass();

            //获取每个对象中的属性
            Field[] declaredFields = clazz.getDeclaredFields();
            //3.遍历得到的每个对象属性的数组，得到里面的每个属性
            for (Field field : declaredFields) {
                //4.判断属性上面是否有@Di注解
                Di annotation = field.getAnnotation(Di.class);
                if(annotation != null){
                    //如果私有属性，设置可以设置值
                    field.setAccessible(true);

                    //5.如果有@Di注解，把对象进行设置(注入)
                    try {
                        field.set(obj,beanFactory.get(field.getType()));
                        //表示向obj设置值
                        //field.getType()获得变量的类型，通过map容器找到该类的一个实例对象注入。
                    } catch (IllegalAccessException e) {
                        throw new RuntimeException(e);
                    }


                }

            }

        }
        

    }
```
测试一下
![5.png][6]


----------
最终IoC核心源码

```java
package com.atguigu.bean;

import com.atguigu.anno.Bean;
import com.atguigu.anno.Di;
import java.io.File;
import java.lang.reflect.Field;
import java.net.URL;
import java.net.URLDecoder;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

public class AnnotationApplicationContext implements ApplicationContext {

    //创建map集合，放bean实例对象

    private Map<Class, Object> beanFactory = new HashMap<>();

    //简化路径
    private static String rootPath;


    //此方法用于返回我们创建的对象
    @Override
    public Object getBean(Class clazz) {
        //根据key返回对象
        return beanFactory.get(clazz);
    }

    //设置包的扫描规则
    //当前包及其子包里面，哪个类有@Bean注解，把这个类通过反射进行实例化
    //创建有参数构造，传递包的路径basePackage，设置扫描规则
    public AnnotationApplicationContext(String basePackage) {
        try {
            //设置包的扫描规则 com.atguigu.spring6
            //找到这个包所在的路径，找到绝对路径，看一下文件夹中是否有子文件夹和文件
            //1.把.替换成\
            String packagePath = basePackage.replaceAll("\\.", "\\\\");

            //2.获取包的绝对路径
            Enumeration<URL> urls = Thread.currentThread().getContextClassLoader().getResources(packagePath);
            while (urls.hasMoreElements()) {
                //遍历，得到里面的每一个具体值
                URL url = urls.nextElement();
                //转码
                String filePath = URLDecoder.decode(url.getFile(), "utf-8");

                //获取包前面的路径部分，用作字符串截取

                rootPath = filePath.substring(0, filePath.length() - packagePath.length());


                //根据路径进行包扫描过程
                loadBean(new File(filePath));

            }
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
        //完成属性的注入
        loadDi();


    }


    //包扫描过程，实例化
    private void loadBean(File file) throws Exception {
        //1.判断当前文件是否文件夹
        if (file.isDirectory()) {
            //2.是文件夹，获取文件夹中里面的所有内容
            File[] childrenFiles = file.listFiles();

            //3.判断文件夹里面内容为空，直接返回
            if (childrenFiles == null || childrenFiles.length == 0) {
                return;
            }

            //4.如果文件夹里面不为空，遍历文件夹里面的所有内容
            for (File child : childrenFiles) {
                //4.1遍历得到每部分内容file对象，继续判断，如果还是文件夹，递归
                if (child.isDirectory()) {
                    //递归的方式
                    loadBean(child);
                } else {
                    //4.2如果遍历得到的file对象，不是一个文件夹，是文件
                    //4.3得到包路径 + 类名称部分 --->字符串截取

                    String pathWithClass = child.getAbsolutePath().substring(rootPath.length() - 1);

                    //4.4判断当前文件的类型是否是.class类型
                    if (pathWithClass.contains(".class")) {

                        //4.5如果是.class类型，把路径中的\替换成.  把.class去掉
                        //com.atguigu.service.UserServiceImpl
                        String allName = pathWithClass.replaceAll("\\\\", ".")
                                .replace(".class", "");

                        //4.6判断类上面是否有注解@Bean，如果有，进行实例化过程
                        //4.6.1得到了类的全路径，获取类的class对象
                        Class<?> clazz = Class.forName(allName);

                        //4.6.2判断不是接口，才进行实例化
                        if (!clazz.isInterface()) {
                            //4.6.3判断类上面是否有注解@Bean
                            Bean annotation = clazz.getAnnotation(Bean.class);
                            if (annotation != null) {
                                //表示类有注解
                                //4.6.4对象 进行实例化
                                Object instance = clazz.getDeclaredConstructor().newInstance();
                                //4.7把对象实例化之后，放到Map集合中beanFactory去
                                //4.7.1判断当前类有接口，让接口class作为key
                                if (clazz.getInterfaces().length > 0) {
                                    beanFactory.put(clazz.getInterfaces()[0], instance);

                                } else {
                                    //4.7.2判断当前类没有接口，让自己class作为key
                                    beanFactory.put(clazz, instance);
                                }


                            }
                        }
                    }
                }
            }
        }
    }

    //进行属性的注入
    private void loadDi() {
        //实例化对象在beanFactory的map集合中里面
        //1.遍历beanFactory的map集合

        Set<Map.Entry<Class, Object>> entries = beanFactory.entrySet();
        for (Map.Entry<Class, Object> entry : entries) {
            //2.获取map集合的每个对象(value)，每个对象中的属性获取到
            Object obj = entry.getValue();

            //获取对象的class
            Class<?> clazz = obj.getClass();

            //获取每个对象中的属性
            Field[] declaredFields = clazz.getDeclaredFields();
            //3.遍历得到的每个对象属性的数组，得到里面的每个属性
            for (Field field : declaredFields) {
                //4.判断属性上面是否有@Di注解
                Di annotation = field.getAnnotation(Di.class);
                if(annotation != null){
                    //如果私有属性，设置可以设置值
                    field.setAccessible(true);

                    //5.如果有@Di注解，把对象进行设置(注入)
                    try {
                        field.set(obj,beanFactory.get(field.getType()));
                        //表示向obj设置值
                        //field.getType()获得变量的类型，通过map容器找到该类的一个实例对象注入。
                    } catch (IllegalAccessException e) {
                        throw new RuntimeException(e);
                    }


                }

            }

        }
        
    }
    

}

```

我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://www.kaijavademo.top/124.html
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/1777678065.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/4278323342.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/882079687.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/3027038386.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/1618573429.png