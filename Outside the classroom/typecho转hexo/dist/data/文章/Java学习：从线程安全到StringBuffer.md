---
title: Java学习：从线程安全到StringBuffer
date: 2023-06-19 03:45:00
categories: Java学习
tags: [多线程,线程安全,StringBuffer]
---
 多线程中关于线程安全的案例到解决方案到StringBuffer与StringBuilder的初辨


<!--more-->

有这样一个需求

```java
 /*
        需求：
            某电影院目前正在上映国产大片，共有100张票，而它有3个窗口卖票，请设计一个程序模拟该电影院卖票

  */
```
 针对于多线程的练习，我们可以考虑到卖票之间的窗口互相独立，就是多线程问题，考虑到如果说只是简单实现多线程，创建线程对象，然后启动三个线程，可能会有以下问题：

 1. 如果是第一种实现多线程的方式，也就是继承Thread类，将成员方法ticket没有设置成静态的，在创建三个线程对象后，会出现最后卖了三百张票的情况。
 2. 仅仅调整1出现的问题，不能满足需求，此时我们会发现可能出现几个窗口再卖同一张票售出，意味着一个座位将坐多个人。
 3. 我们还会发现当运行到100张票之后有超出的票，使得多出的人没有办法坐的尴尬情况。


----------

 这实际上是多线程中的线程安全，如果一个线程进入循环中，睡眠的情况下稍作停留，同时会有其他线程进入。那么就需要我们同步代码块，同步代码块相当于只允许一个线程进去，其他线程抢占到了权也不能立马进入，要等里面的线程执行完毕后才能进入。重点解决如何书写同步代码块的方法。
 
```java
synchronized(){}
```
 我们使用synchronized关键字，将需要循环内部的代码块放入，使用synchronized需要注意两个细节

 - synchronized不能写在循环的外面，如果写在循环的外面，就表示当前的那个进入的线程，全部执行完循环之后才能出来，其他线程没有进入循环的机会。
 - synchronized()括号中的参数表示锁对象，锁对象可以随意起，是Object类也可以。但是锁对象一定要是唯一的，如果用Object类来写，那么创建对象前要加上static表示成员共享。

```java
static Object obj = new Object(); //MyThread不管创建多少对象，这里的obj都是共享的，都是同一个
```
 这里括号中的参数通常使用当前类的字节码文件对象，我当前类叫做MyThread，那么就是MyThread.class，因为它唯一，拿过来当作锁对象。这样就可以初步解决问题了。
初步解决问题的源码：
MyThread类：

```java
public class MyThread extends Thread{
    static int ticket = 0;//0~99


    //表示这个类所有的对象都共享ticket这个数据
    /*
    细节1：
        synchronized不能写在循环的外面
    细节2：
        synchronized锁对象一定要是唯一的
        一般我们会写当前类的字节码文件对象 MyThread.class 唯一，拿过来当作锁对象
    */

    //锁对象，一定要是唯一的
    //static Object obj = new Object(); //MyThread不管创建多少对象，这里的obj都是共享的，都是同一个

    @Override
    public void run() {
        //卖票的代码逻辑
        while (true){
            //已经把操作共享的数据锁起来了，不管有的多少条线程，这里面的代码都是轮流执行
           synchronized (MyThread.class){  //锁对象,解决线程安全的问题
               //this   表示当前线程本身，放到锁对象就是不一样的,又会有不一样和重复的
               //一般我们会写当前类的字节码文件对象 MyThread.class 唯一，拿过来当作锁对象
               //同步代码块
               if(ticket < 100){
                   //让当前线程停顿一会
                   try {
                       Thread.sleep(100);
                   } catch (InterruptedException e) {
                       e.printStackTrace();//父类中run方法没有抛，子类就不能抛
                       //只能自己Try
                   }
                   ticket++;
                   System.out.println(getName() + "正在卖第" + ticket + "票!!!" );
               }else {
                   break;
               }
           }
        }
    }
}
```


----------
ThreadDemo类代码：

```java
public class ThreadDemo {
    public static void main(String[] args) {
        /*
            需求：
                某电影院目前正在上映国产大片，共有100张票，而它有3个窗口卖票，请设计一个程序模拟该电影院卖票
        */
        //三个窗口互相对立，三个线程
        //三个窗口执行同样的逻辑，所以把ticket写在MyThread中
        //创建三个线程执行相同的代码
       MyThread t1 = new MyThread();
       MyThread t2 = new MyThread();
       MyThread t3 = new MyThread();

        //起名字
        t1.setName("窗口1");
        t2.setName("窗口2");
        t3.setName("窗口3");
        //开启线程
        t1.start();
        t2.start();
        t3.start();
        //现在的问题就是窗口1，2，3总共卖了300张票
        //我们要在ticket的前面加一个static
        //这样三个窗口总共卖100张票
        //相同的票出现了多次，还有超出范围的票
        //解决，同步代码块

    }
}
```


----------
 先理一下同步代码块的书写步骤：

 1. 循环
 2. 书写同步代码块
 3. 判断共享数据是否到了末尾，如果到了末尾
 4. 判断共享数据是否到了末尾，如果没有到末尾

接下来我们需要重新改写为同步方法，
 书写同步方法的步骤如下：

 1. 先写同步代码块
 2. 选中要同步方法的方法体，在IDEA中按住ctrl+alt+M快速创建方法，修改名称...
 3. 然后删去原来方法外层synchronized(){}，然后在修饰符private(IDEA默认帮我们创建的方法修饰符)后加上synchronized关键字。
 这样就可以很好的改写为同步方法了，源码我会放到最底下。
 由线程安全我想到StringBuilder，和StringBuffer，它们有什么区别呢？
 首先查阅JavaAPI帮助文档
![1.png][1]

我们会发现它们的成员方法高度一致，在翻阅文档的时候，我看到了一句话
![2.png][2]

指出StringBuilder是有线程安全问题的，那么为什么呢？我们可以翻看源码来解释。
![3.png][3]
对比两个类的成员方法，我们会发现左边StringBuffer方法有synchronized关键字修饰作为同步方法，而右边没有。
启示：
如果说将来我们只需要单线程，那么我们可以使用StringBuilder，而涉及到多线程问题，我们需要使用StringBuffer。
同步代码块的源码：
MyRunnable类：

```java
public class MyRunnable implements Runnable {
    //这里没必要加static
    int ticket = 0;

    //第一种方式有可能创建多个对象，我想让它们共享一个成员变量的值，所以加static
    //第二种方式实现多线程，MyRunnable作为一个参数让线程执行，我只会创建一次，ticket没有必要加static
    @Override
    public void run() {

        //1.循环
        while (true) {

            //当前类的字节码文件作为锁对象
            //2.同步代码块（同步方法）
            //同步方法的书写步骤：
            //①按住ctrl+ alt + M抽取成一个方法，修改名字...
            //②然后删去synchronized(){}然后在方法修饰符private后面加上synchronized

                if (method()) break;

        }
    }

    //this,此时方法非静态，锁对象为this ，对应ThreadDemo中mr唯一，锁对象唯一
    private synchronized boolean method() {
        //3.判断共享数据是否到了末尾，如果到了末尾
        if (ticket == 100) {
            return true;

        } else {
            //4.判断共享数据是否到了末尾，如果没有到末尾
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            ticket++;
            System.out.println(Thread.currentThread().getName() + "在卖第" + ticket + "张票");

        }
        return false;
    }
}
```


----------
ThreadDemo类：

```java
public class ThreadDemo {
    public static void main(String[] args) {
        /*
        需求：
            某电影院目前正在上映国产大片，共有100张票，而它有3个窗口卖票，请设计一个程序模拟该电影院卖票
            利用同步方法完成
            哪些代码写在同步当中？
                技巧：同步代码块
                      抽取成一个方法
        */
       MyRunnable mr = new MyRunnable();
       Thread t1 = new Thread(mr);
       Thread t2 = new Thread(mr);
       Thread t3 = new Thread(mr);

       t1.setName("窗口1");
       t2.setName("窗口2");
       t3.setName("窗口3");

       t1.start();
       t2.start();
       t3.start();

    }
}
```
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/06/1017492649.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/06/2344826280.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/06/2008943227.png