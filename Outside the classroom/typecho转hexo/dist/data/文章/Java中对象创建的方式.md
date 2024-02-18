---
title: Java中对象创建的方式
date: 2023-07-05 06:28:00
categories: Java学习
tags: [Java练习,Java]
---
 java中的对象创建一共有几种方式？用学生类来举例说明并创建对象。


<!--more-->
 准备工作：在做之前我们需要创建一个学生的JavaBean类。

```java
public class Student {
    String name;
    int age;
    int score;

    public Student() {
    }

    public Student(String name, int age, int score) {
        this.name = name;
        this.age = age;
        this.score = score;
    }

    /**
     * 获取
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return score
     */
    public int getScore() {
        return score;
    }

    /**
     * 设置
     * @param score
     */
    public void setScore(int score) {
        this.score = score;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + ", score = " + score + "}";
    }
}

```
----------

方法一：**new 关键字**

```java
Student stud = new Student("zhangsan",19,96);
System.out.println(stud);
```


----------


方法二：**采用反射创建对象**
 1. 获取学生类构造器，指明构造器中的特征，成员变量
 2. 修改构造器权限
 3. 创建对象
 
```java
 //获取这个类的构造器
Constructor<Student> constructor = Student.class.getDeclaredConstructor(
                String.class,
                int.class,
                int.class
        );
        constructor.setAccessible(true);//调用它的私有方法
        Student s = constructor.newInstance("张三", 18, 100);
        System.out.println(s);
```
 [label color="red"]有构造器通过反射创建他的实例对象。好比创建对象后，传递参数 。反射和其他方法相比，还有一个好处是：如果构造方法用private修饰了,那正常其他类肯定是调用不了的这个私有的构造器[/label] 


----------


方法三：**克隆-浅克隆**
 所谓克隆，就是根据已有的对象创建出来一个新的对象
 1. 前提： [label color="blue"]类实现一个Cloneable的接口，并重写里面的clone方法[/label] 
 2. 注意点： 
[label color="red"]Ⅰ.根据一个原有的对象去克隆新对象，我们需要把属性也复制过去；对于基本类型会直接赋值，对于引用类型，只会赋值引用地址，并不会产生一个新的引用对象。因此这种克隆我们也称之为浅克隆。
Ⅱ.不会调用原始的构造方法[/label] 
![1.png][1]

```java
 Student s2 = (Student) s.clone();
System.out.println(s2);
```


----------


方法四：**反序列化生成对象** —并不会调用对象的构造方法，会调用父类的构造方法
 1. 前提： [label color="red"]要求类实现Serializable序列化接口[/label] 
 2. 书写一个对象转换成二进制的方法

```java
 private static byte[] serialize(Student s1) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        //如果序列化主要用到这个类
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(s1);
        byte[] bytes = baos.toByteArray();
        return bytes;

    }

```
![2.png][2]
创建一个ByteArrayOutputStream，关联序列化流ObjectOutputStream，我们把学生对象传递进去，会序列化，ByteArrayOutputStream的作用就是把得到的学生序列化数据写入一个字节数组中，方法作为二进制字节数组作为返回。
 3. 如果再来一次反序列化操作，可以根据二进制形式生成一个新的学生对象，书写一个反序列化操作的方法。

```java
 private static Object deserialize(byte[] bytes) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(bytes));
        return ois.readObject();
    }
```
创建ObjectInputStream 对象关联ByteArrayInputStream，读取字节数组反序列化，最后将反序列化的对象作为方法的返回值

 4. 通过反序列化创建对象

```java
        byte[] bytes = serialize(s);
        //当然这样的方法生成出来的学生对象,和原来的学生对象并不是同一个
        Student s3 = (Student) deserialize(bytes);
        System.out.println(s3);
        System.out.println(s3 == s);//false
```


----------
方法五：**MethodHandle API**-执行到构造方法内部

```java
        //找一个类型的构造器
        //参数二MethodType.methodType主要告诉构造器，它的特征,返回值是什么
        //我们可以设置为空参构造，然后有三个成员变量，姓名年龄学分
        //找到构造器方法返回MethodHandle构造器
        //invoke本身就是调用构造方法
        MethodHandle constructor1 = MethodHandles.lookup().findConstructor(Student.class, MethodType.methodType(void.class, String.class, int.class, int.class));
        Student s4 = (Student) constructor1.invoke("李四", 30, 98);
        System.out.println(s4);
```


----------
源码：Student类

```java
public class Student implements  Cloneable, Serializable {
     String name;
     int age;
     int score;

    public Student() {
    }

    public Student(String name, int age, int score) {
        this.name = name;
        this.age = age;
        this.score = score;
        System.out.println("我是一个构造方法");
    }

    @Override
    protected Object clone() throws CloneNotSupportedException {
        //调用object继承过来克隆
        return super.clone();
    }

    /**
     * 获取
     *
     * @return name
     */
    public String getName() {
        return name;
    }

    /**
     * 设置
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    /**
     * 获取
     * @return score
     */
    public int getScore() {
        return score;
    }

    /**
     * 设置
     * @param score
     */
    public void setScore(int score) {
        this.score = score;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + ", score = " + score + "}";
    }
}

```
测试类：

```java
public class CreateObj {
    public static void main(String[] args) throws Throwable {
        Student stud = new Student("zhangsan",19,96);
        System.out.println(stud);
        //获取这个类的构造器
        Constructor<Student> constructor = Student.class.getDeclaredConstructor(
                String.class,
                int.class,
                int.class
        );
        constructor.setAccessible(true);//调用它的私有方法
        Student s = constructor.newInstance("张三", 18, 100);
        System.out.println(s);
        System.out.println("------------------------------------------");
        Student s2 = (Student) s.clone();
        System.out.println(s2);
        System.out.println("-------------------------------------------");
        //把对象转换成二进制形式
        byte[] bytes = serialize(s);
        Student s3 = (Student) deserialize(bytes);
        System.out.println(s3);
        System.out.println(s3 == s);//false
        System.out.println("-------------------------");
        //invoke本身就是调用构造方法
        MethodHandle constructor1 = MethodHandles.lookup().findConstructor(Student.class, MethodType.methodType(void.class, String.class, int.class, int.class));
        Student s4 = (Student) constructor1.invoke("李四", 30, 98);
        System.out.println(s4);
        System.out.println("--------------------------------------");


    }

    private static byte[] serialize(Student s1) throws IOException {
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        ObjectOutputStream oos = new ObjectOutputStream(baos);
        oos.writeObject(s1);
        byte[] bytes = baos.toByteArray();
        return bytes;

    }

    private static Object deserialize(byte[] bytes) throws IOException, ClassNotFoundException {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(bytes));
        return ois.readObject();
    }
}
```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/1032997144.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/2107681476.png