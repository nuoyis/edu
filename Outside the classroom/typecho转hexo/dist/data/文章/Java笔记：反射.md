---
title: Java笔记：反射
date: 2023-07-19 17:39:00
categories: Java学习
tags: [Java,Java反射]
---
考虑到后期学习Sping框架，和现在接触到的Spingmvc和Sping中的ioc。使用**反射**的频率大大增加，为了方便查阅资料，在此将反射做一个详细的笔记。


<!--more-->

反射允许对封装类的 [label color="red"]字段[/label] 、 [label color="red"]方法[/label] 和 [label color="red"]构造函数[/label] 的信息进行编程访问。
反射的学习大体上可以分为两类， [label color="blue"]获取[/label] 和 [label color="orange"]使用[/label] 。
##获取Class对象的三种方式

 1.  [label color="blue"]Class.forName("全类名");[/label] 
 2.  [label color="purple"]类名.class[/label] 
 3.  [label color="orange"]对象.getClass();[/label] 

[note type="primary flat"]三种方式的 [label color="red"]使用场景[/label] ：
1.第一种方式最为常用
2.第二种方式一般更多的是当作一个 [label color="blue"]参数[/label] 进行传递，比如说同步代码块中的 [label color="blue"]synchronized ()[/label] 传递锁对象的时候。
3.第三种方式有一定的 [label color="pink"]局限性[/label] ，当我们已经有了这个类的对象的时候，才可以使用[/note]




###第一种方式

```java
//全类名：包名 + 类名   com.itheima.newMyreflect1.Student
        Class clazz1 = Class.forName("com.itheima.newMyreflect1.Student");
        //打印
        System.out.println(clazz1);
```

**全类名可以不用通过书写的形式**
![2.png][1]

###第二种方式


```java
//2.第二种方式
        Class clazz2 = Student.class;
        //第一种方式和第二种方式获取的其实是一个对象
        System.out.println(clazz2 == clazz1);
```

###第三种方式
第三种方式需要通过一个对象来进行调用，首先我们准备一个Student类
**Student类**

```java
public class Student {
    private String name;
    private int age;


    public Student() {
    }

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
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

    public String toString() {
        return "Student{name = " + name + ", age = " + age + "}";
    }
}
```
**测试类**

```java
        //3.第三种方式
        Student s = new Student();
        Class clazz3 = s.getClass();

        //这三种方式获取到字节码文件对象是一样的
        System.out.println(clazz1 == clazz2);
        System.out.println(clazz2 == clazz3);


```


----------


##利用反射获取构造方法
**准备：Student类，编写了四个参数不同的构造方法**
Student类

```java
public class Student {
    private String name;
    private int age;


    public Student() {
    }

    public Student(String name) {
        this.name = name;
    }

    protected Student(int age){
        this.age = age;

    }
    private Student(String name, int age) {
        this.name = name;
        this.age = age;
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

    public String toString() {
        return "Student{name = " + name + ", age = " + age + "}";
    }
}

```
![1.png][2]
###获取公共的构造方法


```java
        //2.获取(公共)构造方法
        Constructor[] cons = clazz.getConstructors();
        for (Constructor con : cons) {
            System.out.println(con);
        }
```

![3.png][3]
###获取所有的构造方法

```java
        //3.获取到所有的，包括私有的构造方法。
        Constructor[] cons2 = clazz.getDeclaredConstructors();
        for (Constructor con : cons2) {
            System.out.println(con);
        }

```
![4.png][4]

###获取单个的构造方法

```java
        //4.获取单个的
        //获取空参的构造
        Constructor con1 = clazz.getDeclaredConstructor();
        System.out.println(con1);

        //获取带参数的构造，括号里的参数要和Student里面的参数类型保持一致
        Constructor con2 = clazz.getDeclaredConstructor(String.class);
        System.out.println(con2);

        //获取protected权限修饰符修饰,需要加上Declared
        Constructor con3 = clazz.getDeclaredConstructor(int.class);
        System.out.println(con3);

        //获取全部参数的构造，()里面保持一致
        Constructor con4 = clazz.getDeclaredConstructor(String.class,int.class);
        System.out.println(con4);
```
![5.png][5]
###获取构造方法里面的详细信息


```java
        //获取全部参数的构造，()里面保持一致
        Constructor con4 = clazz.getDeclaredConstructor(String.class, int.class);

        //通过构造方法获取想要的参数
        //获取权限修饰符，返回值以整数的形式返回,
        int modifiers = con4.getModifiers();
        System.out.println(modifiers);

        //获取构造方法中所有的参数
        Parameter[] parameters = con4.getParameters();
        for (Parameter pr : parameters) {
            System.out.println(pr);
        }


        con4.setAccessible(true);//暴力反射
        //通过构造方法创建Student对象
        //创建对象需要给Student赋值，这里属性要和构造方法里面参数保持一致
        Student stu = (Student) con4.newInstance("张三", 23);
        //权限修饰符是私有的无法使用，getDeclaredConstructor只能让你看见构造无法创建对象
        //如果想要创建对象还需要加一个con4.setAccessible(true);校验，可以私有构造方法创建对象
        System.out.println(stu);

```

**权限修饰符**的 [label color="default"]返回值整数[/label] 可以查阅API帮助文档里面的**常量字段值**获取。
![6.png][6]


源码：

```java
public class MyreflectDemo2 {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {
        /*
        Class类中用于获取构造方法的方法
            Constructor<?>[] getConstructors()
            Constructor<?>[] getDeclaredConstructors()
            Constructor<T> getConstructor()(Class<?> ... parameterTypes)
            Constructor<T> getDeclaredConstructor()(Class<?> ... parameterTypes)

            Constructor类中用于创建对象的方法
            T newInstance(Object...initargs)
            serAccessible(boolean flag)

        */

        //1.获取Class字节码文件的对象
        Class clazz = Class.forName("com.itheima.newMyreflect2.Student");

        //2.获取(公共)构造方法
        /*Constructor[] cons1 = clazz.getConstructors();
        for (Constructor con : cons1) {
            System.out.println(con);
        }*/

        //3.获取到所有的，包括私有的构造方法。
        /*
        Constructor[] cons2 = clazz.getDeclaredConstructors();
        for (Constructor con : cons2) {
            System.out.println(con);
        }/*

        //4.获取单个的
        //获取空参的构造
       /* Constructor con1 = clazz.getDeclaredConstructor();
        System.out.println(con1);

        //获取带参数的构造，括号里的参数要和Student里面的参数类型保持一致
        Constructor con2 = clazz.getDeclaredConstructor(String.class);
        System.out.println(con2);

        //获取protected权限修饰符修饰,需要加上Declared
        Constructor con3 = clazz.getDeclaredConstructor(int.class);
        System.out.println(con3);*/

        //获取全部参数的构造，()里面保持一致
        Constructor con4 = clazz.getDeclaredConstructor(String.class, int.class);

        //通过构造方法获取想要的信息
        //获取权限修饰符，返回值以整数的形式返回,
        int modifiers = con4.getModifiers();
        System.out.println(modifiers);

        //获取构造方法中所有的参数
        Parameter[] parameters = con4.getParameters();
        for (Parameter pr : parameters) {
            System.out.println(pr);
        }


        con4.setAccessible(true);//暴力反射
        //通过构造方法创建Student对象
        //创建对象需要给Student赋值，这里属性要和构造方法里面参数保持一致
        Student stu = (Student) con4.newInstance("张三", 23);
        //权限修饰符是私有的无法使用，getDeclaredConstructor只能让你看见构造无法创建对象
        //如果想要创建对象还需要加一个con4.setAccessible(true);校验，可以私有构造方法创建对象
        System.out.println(stu);




    }
}

```
 [label color="red"]注意：通过创建字节码对象clazz直接调用newInstance在JDK17中已经过时，可以使用另一种空参构造创建对象的方式.[/label] 
![7.png][7]

```java
        //clazz调用方法创建对象
        //Object o = clazz.newInstance();//利用空参构造创建对象，方法已经过时
        User user = (User) clazz.getDeclaredConstructor().newInstance();
```
![8.png][8]

----------


##利用反射获取成员变量(字段)
**准备：学生类**
Student类

```java
public class Student {
    private String name;
    private int age;
    public String gender;


    public Student() {
    }

    public Student(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
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
     * @return gender
     */
    public String getGender() {
        return gender;
    }

    /**
     * 设置
     * @param gender
     */
    public void setGender(String gender) {
        this.gender = gender;
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + ", gender = " + gender + "}";
    }
}
```

###获取公共的成员变量

```java
       //2.获取到成员变量的对象
        //获取公共的成员变量
        Field[] fields = clazz.getFields();
        for (Field field : fields) {
            System.out.println(field);
        }

```

###获取所有的成员变量

```java
        //获取所有的成员变量
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            System.out.println(field);
        }
```
###获取单个的成员变量

```java
        //3.获取单个的成员变量
        Field gender = clazz.getField("gender");
        System.out.println(gender);

        Field name = clazz.getDeclaredField("name");
        System.out.println(name);
```


###获取成员变量的信息

```java
        //4.获取成员变量的信息

        //获取权限修饰符,可以查阅API
        int modifiers = name.getModifiers();
        System.out.println(modifiers);

        //获取成员变量名
        String n = name.getName();
        System.out.println(n);

        //获取变量的数据类型
        Class<?> type = name.getType();
        System.out.println(type);

        //获取成员变量记录的值
        Student s = new Student("zhangsan", 23, "男");
        name.setAccessible(true);
        //表示我要获取s对象所记录的名字name
        String value = (String) name.get(s);
        //name变量私有，需要暴力反射name.setAccessible(true);
        System.out.println(value);


        //修改对象里面记录的值
        /*
        set方法
        参数一：我要修改哪个对象?  s
        参数二：我要修改成什么?   lisi
        */
        name.set(s,"lisi");
        System.out.println(s);
```

源码：

```java
public class MyReflectDemo {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchFieldException, IllegalAccessException {
        /*
            Class类中用于获取成员变量的方法
            Field[] getFields():                    返回所有公共成员变量对象的数组
            Field[] getDeclaredFields():            返回所有成员变量对象的数组
            Field getField(String name):            返回单个公共成员变量对象
            Field getDeclaredField(String name):    返回单个成员变量对象
            Field类中用于创建对象的方法
                void set(Object obj, Object value): 赋值
                Object get(Object obj):             获取值
        */
        //1.获取Class字节码文件对象
        Class clazz = Class.forName("com.itheima.newMyreflect3.Student");
        //2.获取到成员变量的对象
        //获取公共的成员变量
        /*Field[] fields = clazz.getFields();
        for (Field field : fields) {
            System.out.println(field);
        }*/

        //获取所有的成员变量
        /*Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            System.out.println(field);
        }*/

        //3.获取单个的成员变量
        Field gender = clazz.getField("gender");
        System.out.println(gender);

        Field name = clazz.getDeclaredField("name");
        System.out.println(name);

        //4.获取成员变量的信息

        //获取权限修饰符,可以查阅API
        int modifiers = name.getModifiers();
        System.out.println(modifiers);

        //获取成员变量名
        String n = name.getName();
        System.out.println(n);

        //获取变量的数据类型
        Class<?> type = name.getType();
        System.out.println(type);

        //获取成员变量记录的值
        Student s = new Student("zhangsan", 23, "男");
        name.setAccessible(true);
        //表示我要获取s对象所记录的名字name
        String value = (String) name.get(s);
        //name变量私有，需要暴力反射name.setAccessible(true);
        System.out.println(value);


        //修改对象里面记录的值
        /*
        set方法
        参数一：我要修改哪个对象?  s
        参数二：我要修改成什么?   lisi
        */
        name.set(s,"lisi");
        System.out.println(s);
    }
}

```


----------

##利用反射获取成员方法
**准备：学生类**
学生类

```java
public class Student {
    private String name;
    private int age;

    public Student() {
    }

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
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
     *
     * @param name
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * 获取
     *
     * @return age
     */
    public int getAge() {
        return age;
    }

    /**
     * 设置
     *
     * @param age
     */
    public void setAge(int age) {
        this.age = age;
    }

    public void sleep() {
        System.out.println("睡觉");
    }

    private String eat(String something) throws IOException,NullPointerException,ClassCastException {
        System.out.println("在吃" + something);
        return "奥利给";
    }

    private void eat(String something, int a) {
        System.out.println("在吃" + something);
    }

    public String toString() {
        return "Student{name = " + name + ", age = " + age + "}";
    }
}

```

###获取公共的成员方法

```java
        //2.获取里面所有公共的方法对象
        //这里面包括了父类中所有的公共方法
        Method[] methods = clazz.getMethods();
        for (Method method : methods) {
            System.out.println(method);
        }
```
###获取所有的成员方法

```java
        //3.获取所有的成员方法(不能获取父类的，但是可以获取本类中私有的方法)
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println(method);
        }
```

###获取单个的成员方法

```java
        //4.获取指定的单一成员方法
        /*
        参数一：方法的名字
        参数二：方法的形参,为了方法的重载
        */
        Method m = clazz.getDeclaredMethod("eat", String.class);
        //单个成员方法私有
        System.out.println(m);

```
###获取对应成员方法中所有的数据

```java
        //获取对应方法中所有的数据
        //获取eat方法中所有的数据

        //获取方法的修饰符
        int modifiers = m.getModifiers();
        System.out.println(modifiers);

        //获取到方法的名字
        String name = m.getName();
        System.out.println(name);

        //获取方法的形参(个数、类型、对象)
        //获取方法的形参对象,放在数组当中
        Parameter[] parameters = m.getParameters();
        for (Parameter parameter : parameters) {
            //依次表示方法中每一个参数
            System.out.println(parameter);
        }




        //获取方法抛出的异常
        Class[] exceptionTypes = m.getExceptionTypes();
        for (Class exceptionType : exceptionTypes) {
            System.out.println(exceptionType);
        }

        //方法运行
        /*Object invoke(Object obj,Object...args)：运行方法
        参数一：用obj对象调用该方法(调用者)
        参数二：调用方法的传递的参数（如果没有就不写）
        返回值：方法的返回值（如果没有就不写）*/

        Student s = new Student();
        //参数一：表示方法的调用者
        //参数二："汉堡包"表示在调用方法的时候传递的实际参数

        m.setAccessible(true);//当前方法私有，临时取消访问权限
        //运行
        m.invoke(s,"汉堡包");


        //获取方法的返回值(方法运行后)
        String result = (String) m.invoke(s, "汉堡包");
        System.out.println(result);

```
源码：

```java
public class MyReflectDemo {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        /*
            Class类中用于获取成员变量的方法
                Method[] getMethods():  返回所有公共成员方法对象的数组
                Method[] getDeclaredMethods():返回所有成员方法对象的数组
                Method[] getMethod(String name,Class<?>...parameterTypes)
                Method[] getDeclaredMethod(String name,Class<?>...parameterTypes)
            Method类中用于创建对象的方法
            Object invoke(Object obj,Object...args)：运行方法
            参数一：用obj对象调用该方法
            参数二：调用方法的传递的参数（如果没有就不写）
            返回值：方法的返回值（如果没有就不写）

           获取方法的修饰符
           获取方法的名字
           获取方法的形参
           获取方法的返回值
           获取方法的抛出的异常
        */

        //1.获取class字节码文件对象
        Class clazz = Class.forName("com.itheima.newMyreflect4.Student");

        //2.获取里面所有公共的方法对象
        //这里面包括了父类中所有的公共方法
        /*Method[] methods = clazz.getMethods();
        for (Method method : methods) {
            System.out.println(method);
        }*/

        //3.获取所有的成员方法(不能获取父类的，但是可以获取本类中私有的方法)
        /*Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            System.out.println(method);
        }*/


        //4.获取指定的单一成员方法
        /*
        参数一：方法的名字
        参数二：方法的形参,为了方法的重载
        */
        Method m = clazz.getDeclaredMethod("eat", String.class);
        //单个成员方法私有
        System.out.println(m);

        //获取对应方法中所有的数据
        //获取eat方法中所有的数据

        //获取方法的修饰符
        int modifiers = m.getModifiers();
        System.out.println(modifiers);

        //获取到方法的名字
        String name = m.getName();
        System.out.println(name);

        //获取方法的形参(个数、类型、对象)
        //获取方法的形参对象,放在数组当中
        Parameter[] parameters = m.getParameters();
        for (Parameter parameter : parameters) {
            //依次表示方法中每一个参数
            System.out.println(parameter);
        }




        //获取方法抛出的异常
        Class[] exceptionTypes = m.getExceptionTypes();
        for (Class exceptionType : exceptionTypes) {
            System.out.println(exceptionType);
        }

        //方法运行
        /*Object invoke(Object obj,Object...args)：运行方法
        参数一：用obj对象调用该方法(调用者)
        参数二：调用方法的传递的参数（如果没有就不写）
        返回值：方法的返回值（如果没有就不写）*/

        Student s = new Student();
        //参数一：表示方法的调用者
        //参数二："汉堡包"表示在调用方法的时候传递的实际参数

        m.setAccessible(true);//当前方法私有，临时取消访问权限
        //运行
        m.invoke(s,"汉堡包");


        //获取方法的返回值(方法运行后)
        String result = (String) m.invoke(s, "汉堡包");
        System.out.println(result);

    }
}

```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/07/2649534437.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/07/853399248.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/07/3454913626.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/07/2565792530.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/07/2354184509.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/07/1105472033.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/07/3418173485.png
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/07/3152043330.png