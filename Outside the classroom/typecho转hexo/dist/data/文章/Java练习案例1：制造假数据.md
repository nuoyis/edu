---
title: Java练习案例1：制造假数据
date: 2023-06-18 12:41:00
categories: Java学习
tags: [Java练习,IO流]
---
 学习IO流的学习让我对Java有了更加深刻的认识，Java中的很多练习是基于大量数据完成的。我们可以通过网站爬取，从而获得大量数据。通过IO流爬取百家姓，以及男生女生的名的相关网址来获取大量的假数据。


<!--more-->
 获取姓氏：https://hanyu.baidu.com/shici/detail?from=kg1&highlight=&pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&srcid=51369
        获取男生名字：http://www.haoming8.cn/baobao/8920.html
        获取女生名字：http://www.haoming8.cn/baobao/7641.html


----------
 1.我们定义三个字符串变量来记录这三个网址

```java
String familyNameNet = "https://hanyu.baidu.com/shici/detail?from=kg1&highlight=&pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&srcid=51369";
String boyNameNet = "http://www.haoming8.cn/baobao/8920.html";
String girlNameNet = "http://www.haoming8.cn/baobao/7641.html";
```
 2.爬取数据，把这三个网址上的数据爬取出来拼接成一个字符串，我们可以定义一个方法，然后分别传入三次字符串对象，获取到当前网站的内容通过字符串返回。
 
```java
public static String webCrawler(String net) throws IOException {}
```
 这里我们开始书写webCrawler的逻辑，首先我们定义一个StringBuilder容器拼接爬取到的数据，然后创建一个url对象，将net传递进去作为网址，调用openConnection方法进行连接。这里有两个细节：①是需要确保你的网络是连通的，而且这个网址有效可以连接上。②可以打开你的浏览器，可以访问即可。

```java
StringBuilder sb = new StringBuilder();
URL url = new URL(net);
URLConnection con = url.openConnection();
```
 然后我们开始调用con中的getInputStream()方法，变成字节流，但是考虑到字节流中文无法正常显示的问题，我们需要运用转换流的知识。

```java
InputStreamReader isr = new InputStreamReader(con.getInputStream());
```

 把字节流转化成字符流，我们运用字符流的知识去读取，我们采用while循环读取。并把读到的结果放入StringBuilder容器中，最后方法返回我们调用StringBuilder中的toString方法做个返回就可以了。需要注意的细节就是：这里获取到的字符流我们要强制转换成字符char的形式存入容器中。

```java
 int ch;
        while ((ch = isr.read()) != -1) {
            sb.append((char) ch);
        }
        //释放资源
        isr.close();
```

 现在我们把百家姓网址传递进去测试一下。

```java
String familyNameStr = webCrawler(familyNameNet);
        System.out.println(familyNameStr);
```
![1.png][1]
 我们发现运行之后，控制台显示的是这个网站的信息，包括一些前端的知识，而我们的目的只是需要其中的百家姓。
![2.png][2]
 这样的方式显然不能满足我们的需求，可想而知其他两个网址也是同样的结果，好在我们能够获取到网址的上的信息，我们需要编写一个方法传递正则表达式来有规则的爬取我们需要的数据，那么考虑到复用性，我们依然编写一个能够传递三个参数的方法getData。

```java
 private static ArrayList<String> getData(String str, String regex, int index) {
        ArrayList<String> list = new ArrayList<>();
        Pattern pattern = Pattern.compile(regex);
        Matcher matcher = pattern.matcher(str);
        while (matcher.find()) {
            list.add(matcher.group(index));
        }

        return list;
    }
```
 3.使用正则表达式获取真正需要的数据
 方法中第一个参数作为传递的网址，第二个参数作为我想要书写的对应正则表达式。
 我先创建一个集合，将有效的数据收录到其中，对应最后做一个返回。方法中我获取一个正则表达式的对象并且调用matcher方法将我爬取的网站放进来，然后通过find方法循环找到其中的数据，将按照规则的有效数据放入list集合中有效返回。这里的第三个参数index是我们在初步正则表达式获取到数据之后，我们需要再次筛选一下数据。我们将需要的部分作为参数传入group方法中。下面我会解释这个index的作用。
 接下来我们需要给方法传递参数

```java
ArrayList<String> familyNameTempList = getData(familyNameStr, "(.{4})(，|。)", 1);
```
 第二个参数作为正则表达式，我想让百家姓中四个词为一组，结尾可以是中文模式下的逗号或者是句号。"."表示可以是任意字符，{4}表示出现四次，而后面的(|)表示其中的逗号句号二选一。之所以将前面也括起来，是因为最后要传递1，代表索引，表示我只需要四个词就可以，后面标点符号不要。将1作为index传递给上面的group方法。如果这里传递2就表示我们需要第二组括起来的数据也就是，或者是。会被我们放到集合中。
![3.png][3]
观察男生名字，我们会发现真正需要的是两个词，中间是顿号或者是句号的这种，编写正则表达式。

```java
ArrayList<String> boyNameTempList = getData(boyNameStr, "([\\u4E00-\\u9FA5]{2})(、|。)", 1);
```
 这里第一个参数和第三个参数不做解释，第二个参数是为了都表示数字{2}表示至少出现两次，前面如果说用"."可能会爬取到异常的数据，所以说要使用中文的正则表达式。下载一个AnyRule的插件，然后右键进去之后搜索中文，这里我是用的是第二个正则表达式。
![4.png][4]
![5.png][5]
 观察女生名字，我们发现我们真正需要的是一个词 空格 一个词的这样形式，但是正则表达式里面不能直接这么写，这样可以爬取到的数据多了去了。

```java
ArrayList<String> girlNameTempList = getData(girlNameStr, "(.. ){4}..", 0);
```
 这里我们将一行看作一个元素，(.. ){4}表示将一行前四个词，都是以一个词+空格的形式出现四次。然后一行的结尾也是两个字，第三个参数传递0，表示我们获取到的数据我们全部需要。
 4.处理数据，我们需要对有效的数据再进行一次处理，处理的目的是为了姓氏最终变成一个姓代表一个元素，两个字代表名作为一个元素。

```java
 ArrayList<String> familyNamelist = new ArrayList<>();
        for (String str : familyNameTempList) {
            for (int i = 0; i < str.length(); i++) {
                char c = str.charAt(i);
                familyNamelist.add(c + "");//变成一个字符串

            }
        }
        ArrayList<String> boyNameList = new ArrayList<>();
        for (String str : boyNameTempList) {
            if (!boyNameList.contains(str)) {
                boyNameList.add(str);

            }

        }
        ArrayList<String> girlNameList = new ArrayList<>();
        for (String str : girlNameTempList) {
            String[] arr = str.split(" ");
            for (int i = 0; i < arr.length; i++) {
                girlNameList.add(arr[i]);
            }
        }

```
 遍历familyNameTempList，用增强for循环获得当中的每一个元素str，此时str是四个字为一个词一组的形式，遍历字符串，然后使用字符串中的charAt方法，获取str中的每一个元素，最后放入familyNamelist，此时就表示的每一个姓氏。

 对于boyList，考虑假数据之间有可能重复，我们做了一个去重处理。想到去重①我们可以利用HashSet集合本身的不重复性。②当然，还有另外一种方法就是使用List集合中，调用contains方法。对于从boyNameTempList获取到的数据做一个判断，如果boyNameList中没有这个元素，那么就添加进来。我觉得这个方法也很好，我觉得好处在于三个集合的处理统一使用了list集合。

 获取到的女生的名字是五个词为一个元素的情况，增强for循环获取每一组，然后通过字符串中的split方法分割，然后对于分割后的每一个元素从数组中遍历获取到集合中。
 5.生成数据，我们需要写一个方法，把最后的数据拼接出来，用ArrayList集合作为返回。


```java
public static ArrayList<String> getInfos(ArrayList<String> familyNamelist, ArrayList<String> boyNameList, ArrayList<String> girlNameList, int boyCount, int girlCount) {}
```
 这里方法我传递了三个集合，以及最后两个是我想要生成男生姓名和女生姓名的个数

```java

        HashSet<String> boyhs = new HashSet<>();
        while (true) {
            if (boyhs.size() == boyCount) {
                break;
            }
            Collections.shuffle(familyNamelist);
            Collections.shuffle(boyNameList);


            boyhs.add(familyNamelist.get(0) + boyNameList.get(0));

        }
```
 我用生成男生名字的逻辑说明，女生也一样。我选择HashSet集合作为男生姓名拼接完成添加到集合中，可以避免生成名字相同的元素。我写了一个while死循环，判断我此时集合中男生的个数和我方法需要的个数是否一致，如果一致，那么跳出循环，也就意味着不再添加。

 那么在方法中我选择打乱姓氏和男生名集合。打乱也有两种思路，一种是Random获取到一个集合的随机索引，然后get方法获取随机索引对应的元素。另一种方法是通过Collections特有的方法shuffle，可以打乱数据，那么我们只需要获取到0索引上的元素，拼接起来添加到boyhs中即可。
 
```java
 ArrayList<String> list = new ArrayList<>();
        Random r = new Random();
        for (String boyName : boyhs) {
            int age = r.nextInt(10) + 18;
            list.add(boyName + "-男-" + age);
        }
        for (String girlName : girlhs) {
            int age = r.nextInt(8) + 18;
            list.add(girlName + "-女-" + age);


        }

        return list;
```
 然后现在的我一共有两个Set集合，分别是已经生成好的男生姓名和女生姓名，我们只需要最后做一个拼接，放入同一个数组中就可以了。注意年龄是随机生成的，我想生成18~27的岁，那么应该怎么传递 r.nextInt();的范围呢？流程如下：
 Ⅰ.先两边同时减去-18，让前面对其为0~9
 Ⅱ.然后尾巴加1(因为考虑到random类范围包左不包右的情况)，也就是0~10，那么10写入括号中r.nextInt(10);
 Ⅲ.然后把第Ⅰ步减去的18加上即可，最终r.nextInt(10) + 18；
 返回集合，方法返回处我用ArrayList集合作为接收，情况是前70个是男生后面50个是女生，打乱集合。
 6.写入数据

```java

        BufferedWriter bw = new BufferedWriter(new FileWriter("E:\\工具\\JDK\\IDEA\\myiotest\\names.txt"));
        for (String str : list) {
            bw.write(str);
            bw.newLine();
        }
        bw.close();
```
 调用字符缓冲输出流，使用字符缓冲输出流大概有两点原因：
 ①里面有特有方法newLine对于每次写完一个数据方便换行，这个方法最强大的好处就是跨平台。
 ②效率更高（不是主要原因，如果数据更大那可能比较明显。）关联基本流。使用流之后记得释放资源。
![6.png][6]
 我们可以观察到数据已经生成，小小检查一下。
![7.png][7]

 这样我们需要多少男生和多少女生就可以在boyCount/girlCount中写入数据生成了，这样我们就可以拿到足够多的假数据了。
 写这个练习原因是我觉得练习的非常全面，不光练习了IO流，还练习了前面的随机数，集合，还有方法书写的逻辑。

 练习中还有一些亮点，比如说随机数据我可以使用集合也可以随机数打乱，去重我不光可以考虑到HashSet集合，还可以使用本身List集合中的contians方法。
 源码：

```java
public class Test1 {
    public static void main(String[] args) throws IOException {
        /*
        制造假数据
        获取姓氏：https://hanyu.baidu.com/shici/detail?from=kg1&highlight=&pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&srcid=51369
        获取男生名字：http://www.haoming8.cn/baobao/8920.html
        获取女生名字：http://www.haoming8.cn/baobao/7641.html
        */
        //1.定义变量用来记录网址
        String familyNameNet = "https://hanyu.baidu.com/shici/detail?from=kg1&highlight=&pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&srcid=51369";
        String boyNameNet = "http://www.haoming8.cn/baobao/8920.html";
        String girlNameNet = "http://www.haoming8.cn/baobao/7641.html";

        //2.爬取数据,把这个网址上的数据拼接成一个字符串
        //定义一个方法调用三次
        String familyNameStr = webCrawler(familyNameNet);//以字符串形式装的姓氏
        String boyNameStr = webCrawler(boyNameNet);
        String girlNameStr = webCrawler(girlNameNet);
        //System.out.println(familyNameStr);
        //System.out.println(boyNameStr);
        //System.out.println(girlNameStr);
        //3.通过正则表达式，把其中符合要求的数据获取出来
        //从三个网址中都要获取，所以说写一个方法调用三次,每个方法只需要修改正则表达式里面的内容就可以了
        //.{4}(，|。)但是我不要，和。如何操作？

        //四个字出现的后面是，或者是。注意这里是中文姓氏，然后我只需要前面的所以说传递1索引。
        ArrayList<String> familyNameTempList = getData(familyNameStr, "(.{4})(，|。)", 1);
        //中文形势下的两个字，后面可以是、可以是。
        ArrayList<String> boyNameTempList = getData(boyNameStr, "([\\u4E00-\\u9FA5]{2})(、|。)", 1);
        //这里作为一个整体传递一行五个单词，不要把一个词两个字外加回车和空格看作一个整体。
        ArrayList<String> girlNameTempList = getData(girlNameStr, "(.. ){4}..", 0);
        //System.out.println(familyNameTempList);
        //System.out.println(boyNameTempList);
        //System.out.println(girlNameTempList);
        //4.处理数据
        //familyNameTempList(姓氏)
        //处理方案：把每一个姓氏拆开并添加到一个新的集合当中
        ArrayList<String> familyNamelist = new ArrayList<>();
        for (String str : familyNameTempList) {
            //str 赵钱孙李 周吴郑王 冯陈褚卫
            for (int i = 0; i < str.length(); i++) {
                char c = str.charAt(i);
                familyNamelist.add(c + "");//变成一个字符串

            }
        }
        //boyNameTempList(男生的名字)
        //处理方案：去除其中的重复元素
        //可以用集合。也可以用HashSet
        ArrayList<String> boyNameList = new ArrayList<>();
        for (String str : boyNameTempList) {
            //表示你当前的str在boyNameList中是否存在吗？
            if (!boyNameList.contains(str)) {
                boyNameList.add(str);

            }

        }
        //girlNameTempList(女生的名字)
        //处理方案：把里面的每一个元素用空格进行切割，得到每一个女生的名字

        ArrayList<String> girlNameList = new ArrayList<>();
        for (String str : girlNameTempList) {
            //str表示每一组信息
            //依莹 瑶馨 曼珍 逸云 微婉
            String[] arr = str.split(" ");
            for (int i = 0; i < arr.length; i++) {
                girlNameList.add(arr[i]);
            }
        }

        //System.out.println(girlNameList);

        //5.生成数据
        //姓名(唯一)-性别-年龄
        ArrayList<String> list = getInfos(familyNamelist, boyNameList, girlNameList, 70, 50);
        Collections.shuffle(list);
        System.out.println(list);

        //6.写出数据
        BufferedWriter bw = new BufferedWriter(new FileWriter("E:\\工具\\JDK\\IDEA\\myiotest\\names.txt"));
        for (String str : list) {
            bw.write(str);
            //调用字符缓冲流特有的换行方法
            bw.newLine();
            //循环完毕写入
        }
        bw.close();



    }

    /*
    作用：
        获取男生和女生的信息：姓名(唯一)-性别-年龄 张三-男-23
    形参：
        参数一：装着姓氏的集合
        参数二：装着男生名字的集合
        参数三：装着女生名字的集合
        参数四：男生的个数
        参数五：女生的个数
    */
    public static ArrayList<String> getInfos(ArrayList<String> familyNamelist, ArrayList<String> boyNameList, ArrayList<String> girlNameList, int boyCount, int girlCount) {
        //1.生成不重复的名字
        HashSet<String> boyhs = new HashSet<>();
        //在两个集合之间随机抽取，然后拼接起来放到hashset集合当中
        //如果我生成了和boyCount数值一样，表示我已经生成了足够的男生姓名了
        while (true) {
            if (boyhs.size() == boyCount) {
                break;
            }
            //不相等，男生名字不够，继续生成
            //随机
            //两种方式：一种是Random，另一种是Collections中的shuffle
            Collections.shuffle(familyNamelist);
            Collections.shuffle(boyNameList);


            boyhs.add(familyNamelist.get(0) + boyNameList.get(0));

        }
        //System.out.println(boyhs);
        //如果只是为了单个测试，方法不报错的情况下查看方法，可以传递null

        //生成女生不重复的名字
        HashSet<String> girlhs = new HashSet<>();
        while (true) {
            if (girlhs.size() == girlCount) {
                break;
            }
            Collections.shuffle(familyNamelist);
            Collections.shuffle(girlNameList);

            girlhs.add(familyNamelist.get(0) + girlNameList.get(0));

        }
        //3.张三-男-23
        ArrayList<String> list = new ArrayList<>();
        Random r = new Random();
        //[18~27]
        //-18 0 ~9
        //尾巴+1 9 + 1 = 10;
        //记得加+1
        for (String boyName : boyhs) {
            //boyName依次表示每一个男生的名字
            int age = r.nextInt(10) + 18;
            list.add(boyName + "-男-" + age);


        }
        //4.生成女生的信息并添加到集合当中
        //[18~25]
        for (String girlName : girlhs) {
            //girlName依次表示每一个女生的名字
            int age = r.nextInt(8) + 18;
            list.add(girlName + "-女-" + age);


        }

        return list;
    }

    /*
    作用：根据正则表达式获取字符串中的数据
    参数一：
        完整的字符串
    参数二：
        正则表达式
    参数三：
        ？？？

    返回值：
        真正想要的数据
    */
    private static ArrayList<String> getData(String str, String regex, int index) {
        //1.创建集合用来存放数据
        ArrayList<String> list = new ArrayList<>();
        //2.按照正则表达式的规则获取数据
        Pattern pattern = Pattern.compile(regex);//获取一个正则表达式的对象
        //pattern正则表达式的对象，读取的规则
        //从str进行读取
        //按照pattern的规则到str当中获取数据
        Matcher matcher = pattern.matcher(str);
        while (matcher.find()) {

            //String group = matcher.group(index);//把满足要求的数据进行获取
            //获取到的数据不想要打印
            list.add(matcher.group(index));
        }

        return list;
    }

    //拼接成一个字符串返回
    /*
        作用：
            从网络中爬取数据，并把数据拼接成字符串返回
        形参：
            网址
        返回值：
        爬取到的所有数据
    */
    public static String webCrawler(String net) throws IOException {
        //1.定义StringBuilder拼接爬取到的数据
        StringBuilder sb = new StringBuilder();
        //2.创建一个URL对象
        URL url = new URL(net);
        //3.链接上这个网址
        //细节：保证你的网络是畅通的，而且这个网址是可以链接上的。
        //打开你的浏览器，可以访问即可

        URLConnection con = url.openConnection();
        //4.读取数据
        //也是用IO流来读取
        //con.getInputStream();//字节流  这个网址上可能会有中文转换成  字符流
        InputStreamReader isr = new InputStreamReader(con.getInputStream());//转换成字符流
        int ch;
        while ((ch = isr.read()) != -1) {
            sb.append((char) ch);
        }

        //5.释放资源
        isr.close();
        //6.把读取到的数据进行返回
        return sb.toString();

    }
}

```

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/06/2149585246.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/06/1381036173.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/06/875870014.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/06/968740105.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/06/3764010467.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/06/1513440483.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/06/1755862237.png