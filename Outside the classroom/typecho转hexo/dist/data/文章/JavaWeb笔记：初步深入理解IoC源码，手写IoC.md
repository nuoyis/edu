---
title: JavaWeb笔记：初步深入理解IoC源码，手写IoC
date: 2023-07-23 04:28:00
categories: JavaWeb
tags: [JavaWeb,JavaWeb笔记,IoC]
---
 在软件系统中，层与层之间是存在依赖的。我们也称之为 [label color="purple"]耦合[/label] 。
我们系统架构或者是设计的一个原则是： [label color="red"]高内聚低耦合[/label] 。
层内部的组成应该是高度聚合的，而层与层之间的关系应该是 [label color="blue"]低耦合[/label] 的，最理想的情况是**0耦合**(就是没有耦合)
![01.MVC04.png][1]
如图所示，FruitController层依赖于FruitService层，Service依赖Dao层，上下层之间相互依赖，可以理解为层与层之间存在依赖的。我们希望把其中一层删掉，另一层不会报错。也就是所谓的下层的改动不会影响到上层。
![2.png][2]
这里我们发现这里new的是下层FruitService类，这样就会产生关系，如果单纯的改为 [label color="default"]null[/label] 不能解决问题。这一步改动没有错，我们需要思考怎么去解决后面空指针的问题。


<!--more-->

首先我们先要为三个组件(三层)配置一个 [label color="orange"]XML文件[/label] 

```xml
<?xml version="1.0" encoding="utf-8" ?>
<beans>
    <bean id="fruitDao" class="com.atguigu.fruit.FruitDao"/>
    <bean id="fruitService" class="com.atguigu.fruit.service.impl.FruitServiceImpl"/>
    <bean id="fruit" class="com.atguigu.fruit.controllers.FruitController"/>
</beans>

```

我们配置的目的就是想让程序一启动就将三个组件提前准备好，加载到一个容器中。

紧接着我们需要去写一个 [label color="green"]接口BeanFactory[/label] 
![3.png][3]
这个接口里面有一个 [label color="red"]getBean方法[/label] ，顾名思义**根据id就能获取到XML文件中的某一个bean对象对应的class类。**

```java
public interface BeanFactory {
    public abstract Object getBean(String id);
}

```
接口无法工作，我们需要书写对应 [label color="blue"]实现类**ClassPathXmlApplicationContext**[/label] 
需要一个Map容器来存放组件,那么重写的beanMap返回值就是把id放进去

```java
public class ClassPathXmlApplicationContext implements BeanFactory {
    private Map<String, Object> beanMap = new HashMap<>();
 @Override
    public Object getBean(String fid) {
        return beanMap.get(fid);
    }
}

```
重点我们就去考虑**beanMap容器**
在构造方法中，我们需要将原先在中央控制器处理的DispatcherServlet中的init方法剪切过来

```java
    public ClassPathXmlApplicationContext() {
        try {
            //通过类加载器的方式加载配置文件
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream("applicationContext.xml");
            //1.创建documentBuilderFactory对象
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            //2.创建DocumentBuilder对象
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            //3.创建Document对象
            Document document = documentBuilder.parse(inputStream);

            //4.获取所有的bean节点
            NodeList beanNodeList = document.getElementsByTagName("bean");

            for (int i = 0; i < beanNodeList.getLength(); i++) {
                Node beanNode = beanNodeList.item(i);
                //获取节点类型，如果是个元素节点
                if (beanNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element beanElement = (Element) beanNode;
                    String beanId = beanElement.getAttribute("id");
                    //className对应的是全类名，我要获取他的对象
                    String className = beanElement.getAttribute("class");
                    Class beanClass = Class.forName(className);
                    //创建bean对象并实例
                    Object beanObj = beanClass.newInstance();
                    //将bean实例对象保存到map容器中
                    beanMap.put(beanId, beanObj);
                    //到目前为止，此处需要注意的是，bean和bean之间的依赖关系没有设置


                }

            }
 }
```
这样beanMap中就有数据了，而在DispatcherServlet中就会报错，原先的beanMap没有了，在DispatcherServlet类构造方法中创建并传递beanFactory
![4.png][4]
![5.png][5]


----------
但是随之而来的问题又产生了，为了消除层与层之间的依赖，在FruitController类中和FruitServiceImpl类中成员变量都为null没有赋值
![6.png][6]
![7.png][7]
现在属于层与层之间的依赖，我们需要再次在 [label color="orange"]XML配置文件[/label] 中 [label color="red"]添加组件之间的依赖关系[/label] 

```xml
<beans>
    <bean id="fruitDao" class="com.atguigu.fruit.FruitDao"/>
    <bean id="fruitService" class="com.atguigu.fruit.service.impl.FruitServiceImpl">
        <!--property标签用来表示属性:name表示属性名;ref表示引用其他bean的id值-->
        <!--property中的name表示本bean标签中class参数类的成员变量，松耦合-->
        <!--这样我不仅描述了bean，还配置了bean与bean之间的依赖关系-->
        <property name="fruitDao" ref="fruitDao"/>
    </bean>
    <bean id="fruit" class="com.atguigu.fruit.controllers.FruitController">
        <property name="fruitService" ref="fruitService"/>
    </bean>
</beans>

```
对应关系
![8.png][8]


----------

到目前为止，ClassPathXmlApplicationContext类构造方法中，bean和bean之间的依赖关系没有设置，我们需要组装Bean之间的**依赖关系**

```java
            //5.组装bean之间的依赖关系
            for (int i = 0; i < beanNodeList.getLength(); i++) {
                Node beanNode = beanNodeList.item(i);
                //获取节点类型，如果是个元素节点
                if (beanNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element beanElement = (Element) beanNode;
                    String beanId = beanElement.getAttribute("id");
                    //获取它的子节点
                    NodeList beanChileNodeList = beanElement.getChildNodes();

                    for (int j = 0; j < beanChileNodeList.getLength(); j++) {
                        //获取里面的每一个子节点
                        Node beenChildNode = beanChileNodeList.item(j);
                        //只关心元素节点，并且只关心带有property的元素节点
                        if (beenChildNode.getNodeType() == Node.ELEMENT_NODE && "property".equals(beenChildNode.getNodeName())) {
                            Element propertyElement = (Element) beenChildNode;
                            String propertyName = propertyElement.getAttribute("name");
                            String propertyRef = propertyElement.getAttribute("ref");
                            //1.找到propertyRef对应的实例
                            Object refObj = beanMap.get(propertyRef);
                            //2.将refObj设置到当前bean对应的实例的property属性上去
                            Object beanObj = beanMap.get(beanId);
                            Class beanClazz = beanObj.getClass();
                            Field propertyField = beanClazz.getDeclaredField(propertyName);
                            propertyField.setAccessible(true);
                            propertyField.set(beanObj,refObj);
                            /*
                            理解：

                            我需要通过这个FruitController类创建fruitService对象

                            String propertyName = propertyElement.getAttribute("name");通过xml里面的name取出对象fruitService
                            起初fruit对应实例fruitService原本为空null，

                            Object refObj = beanMap.get(propertyRef);
                            我通过beanMap，去找对应的类fruitService并赋值为refObj,为FruitService类的实例

                             Object beanObj = beanMap.get(beanId);
                            我通过bean标签中的id找到了对应的class = FruitController类赋值为beanObj

                            通过反射给FruitController类中fruitService调整值
                            通过反射获取字节码文件信息，然后getDeclaredField找到成员变量fruitService

                            打破权限，使用set方法，对于当前FruitController类fruitService赋值为refObj
                            private FruitService fruitService = new FruitService();

                            */
                        }
                    }
                }
            }

```
源码:


```java
public class ClassPathXmlApplicationContext implements BeanFactory {
    private Map<String, Object> beanMap = new HashMap<>();

    public ClassPathXmlApplicationContext() {
        try {
            //通过类加载器的方式加载配置文件
            InputStream inputStream = getClass().getClassLoader().getResourceAsStream("applicationContext.xml");
            //1.创建documentBuilderFactory对象
            DocumentBuilderFactory documentBuilderFactory = DocumentBuilderFactory.newInstance();
            //2.创建DocumentBuilder对象
            DocumentBuilder documentBuilder = documentBuilderFactory.newDocumentBuilder();
            //3.创建Document对象
            Document document = documentBuilder.parse(inputStream);

            //4.获取所有的bean节点
            NodeList beanNodeList = document.getElementsByTagName("bean");

            for (int i = 0; i < beanNodeList.getLength(); i++) {
                Node beanNode = beanNodeList.item(i);
                //获取节点类型，如果是个元素节点
                if (beanNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element beanElement = (Element) beanNode;
                    String beanId = beanElement.getAttribute("id");
                    //className对应的是全类名，我要获取他的对象
                    String className = beanElement.getAttribute("class");
                    Class beanClass = Class.forName(className);
                    //创建bean对象并实例
                    Object beanObj = beanClass.newInstance();
                    //将bean实例对象保存到map容器中
                    beanMap.put(beanId, beanObj);
                    //到目前为止，此处需要注意的是，bean和bean之间的依赖关系没有设置


                }

            }
            //5.组装bean之间的依赖关系
            for (int i = 0; i < beanNodeList.getLength(); i++) {
                Node beanNode = beanNodeList.item(i);
                //获取节点类型，如果是个元素节点
                if (beanNode.getNodeType() == Node.ELEMENT_NODE) {
                    Element beanElement = (Element) beanNode;
                    String beanId = beanElement.getAttribute("id");
                    //获取它的子节点
                    NodeList beanChileNodeList = beanElement.getChildNodes();

                    for (int j = 0; j < beanChileNodeList.getLength(); j++) {
                        //获取里面的每一个子节点
                        Node beenChildNode = beanChileNodeList.item(j);
                        //只关心元素节点，并且只关心带有property的元素节点
                        if (beenChildNode.getNodeType() == Node.ELEMENT_NODE && "property".equals(beenChildNode.getNodeName())) {
                            Element propertyElement = (Element) beenChildNode;
                            String propertyName = propertyElement.getAttribute("name");
                            String propertyRef = propertyElement.getAttribute("ref");
                            //1.找到propertyRef对应的实例
                            Object refObj = beanMap.get(propertyRef);
                            //2.将refObj设置到当前bean对应的实例的property属性上去
                            Object beanObj = beanMap.get(beanId);
                            Class beanClazz = beanObj.getClass();
                            Field propertyField = beanClazz.getDeclaredField(propertyName);
                            propertyField.setAccessible(true);
                            propertyField.set(beanObj,refObj);
                            /*
                            理解：

                            我需要通过这个FruitController类创建fruitService对象

                            String propertyName = propertyElement.getAttribute("name");通过xml里面的name取出对象fruitService
                            起初fruit对应实例fruitService原本为空null，

                            Object refObj = beanMap.get(propertyRef);
                            我通过beanMap，去找对应的类fruitService并赋值为refObj,为FruitService类的实例

                             Object beanObj = beanMap.get(beanId);
                            我通过bean标签中的id找到了对应的class = FruitController类赋值为beanObj

                            通过反射给FruitController类中fruitService调整值
                            通过反射获取字节码文件信息，然后getDeclaredField找到成员变量fruitService

                            打破权限，使用set方法，对于当前FruitController类fruitService赋值为refObj
                            private FruitService fruitService = new FruitService();

                            */
                        }
                    }
                }
            }

        } catch (ParserConfigurationException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        } catch (SAXException e) {
            throw new RuntimeException(e);
        } catch (ClassNotFoundException e) {
            throw new RuntimeException(e);
        } catch (InstantiationException e) {
            throw new RuntimeException(e);
        } catch (IllegalAccessException e) {
            throw new RuntimeException(e);
        } catch (NoSuchFieldException e) {
            throw new RuntimeException(e);
        }

    }
    @Override
    public Object getBean(String fid) {
        return beanMap.get(fid);
    }
}

```


----------


 [label color="red"]总结笔记[/label] 

[note type="default flat"]    IOC- 控制反转 / DI - 依赖注入
控制反转：
1)之前在Servelt中，我们创建service对象,  `FruitService fruitServlet = new FruitServiceImpl();` 
这句话如果出现在servlet中的某个方法内部，那么这个fruitService 的作用域(生命周期)应该就是这个方法级别；
如果这句话出现在servet类中，也就是说fruitService是一个成员变量，那么这个fruitService的作用域(生命周期)应该就是这个servlet实例级别
2)之后我们在applicationContext.xml中定义了fruitService,然后通过解析XML，产生了fruitServiet实例,存放在beanMap中，这个beanMap在一个BeanFactory中
因此，我们转移(改变)了之前的service实例，dao实例等等他们的生命周期，控制权从程序员转移到BeanFactory。这个现象我们称之为叫 [label color="red"]控制反转[/label] 

依赖注入：
1)之前我们在控制层出现代码：是 `FruitService fruitServlet = new FruitServiceImpl();` 
那么，控制层和service存在 [label color="default"]耦合[/label] .
2）之后，我们将代码修改成 `FruitService fruitServlet = null;` 
然后在配置文件中配置
 `<bean id="fruit" class="FruitController">` 
 `<property name="fruitService" ref="fruitService"/>` 
 `</bean>` 
以前是主动获取绑定这一层关系，现在我们是靠配置文件解析，容器帮我们注入进去，使用的是反射技术。
[/note]
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1186429360.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/2475889753.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/3852197456.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/391151143.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/1882708244.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/2911601936.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/2329137863.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/1805943634.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/07/2709762154.png