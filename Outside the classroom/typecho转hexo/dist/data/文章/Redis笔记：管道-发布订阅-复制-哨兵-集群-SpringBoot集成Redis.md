---
title: Redis笔记：管道-发布订阅-复制-哨兵-集群-SpringBoot集成Redis
date: 2023-09-20 07:02:00
categories: Redis
tags: [Redis7,redis管道,redis发布订阅,主从复制,哨兵,集群,SpringBoot集成]
---
基于Redis7的学习笔记，包含有Redis管道，目前仍在持续更新。


<!--more-->

##Redis管道
Redis管道和Redis事务**截然不同**的两个东西。可以类比为Java和JavaScript之间的关系。把所有命令排成一行，像流水线一样去处理。
管道(pipeline)可以一次性发送多条命令给服务端，服务端依次处理完完毕后， [label color="red"]通过一条响应一次性将结果返回，通过减少客户端与redis的通信次数来实现降低往返延时时间[/label] 。pipeline实现的原理是队列，先进先出特性就保证数据的顺序性。
我们之前学过的批量添加无法一次性添加多种数据类型，这个也是我们出现的问题，用管道来解决。

 - 我们可以将一次性添加的命令放在myredis/下的一个新的txt文件。
 - 在服务器外部执行语句 `cat cmd.txt | redis-cli -a abc123 --pipe` 
服务器内部可以使用，如图。
![1.png][1]


[note type="primary flat"]管道小总结：
Ⅰ.Pipeline与原生批量命令对比
①原生的批量命令是原子性，**pipeline是非原子性**。
②pipeline支持批量执行不同的命令。
③原生批命令是服务器实现，而pipeline需要服务端与客户端共同完成。
Ⅱ.Pipeline与事务对比
①事务具有原子性，管道不具有原子性
②事务一条一发，只有在接收到exec命令后才会执行。而管道是一次性将多条命令发送到服务器。
③执行事务会阻塞其他命令执行，而执行管道中的命令不会。
Ⅲ.管道自身注意事项
①管道的缓冲指令只是会依次执行，不保证原子性，如果执行中指令发生异常，将会继续执行后续的指令
②使用pipeline组装的命令个数不能太多，不然数据量大客户端阻塞的时间可能过久，同时服务端此时也被迫回复一个队列答复，占用很多内存。[/note]

官方解释
> So if you need to send a lot of commands with pipelining, it is better to send them as batches each containing a reasonable number, for instance 10k commands, read the replies, and then send another 10k commands again, and so forth. 


----------
##发布订阅
类似于MQ消息中间件，了解即可，我们还是需要将专业的事情交给专业的人去干。pub|sub作为第一代消息中间件，stream作为第二代消息中间件(就是说可以理解为MQ的前身雏形)

是一种消息通信模式，发送者发送消息，订阅者接收消息，可以实现进程见的消息传递。Redis可以实现消息中间件的功能，即通过发布订阅实现消息的引导和分流。**专业的事情交给专业的中间件处理，redis做好分布式缓存的功能就够了**。

 - 开启三个客户端，演示客户端A、B订阅消息，客户端C发布消息
![2.png][2]
 - 演示批量订阅和发布
![3.png][3]
 - 取消订阅
![4.png][4]


[note type="warning flat"]存在的问题(缺点)：
①没有持久化，必须先订阅再发布。如果先发布消息没有订阅者，消息直接丢弃。
②没有ACK机制，无法保证消息的消费成功
③以上缺点导致该模式在生产结构中无用武之地，因此Redis5.0新增了Stream。
[/note]

----------
##Redis复制
Redis复制非常重要，生产工作中，redis不可能是单机，后面的**哨兵和集群**都要建立在这个基础之上。
主机(master)以写为主，从机(slave)以读为主。当主机(master)数据发生变化的时候，自动将新的数据异步同步到其他slave数据库。
能干嘛？
 1. **读写分离**
 2. **容灾恢复**，对之前持久化的一种更好的补充
 3. **数据备份**
 4. **水平扩容支撑高并发**
使用：
 - 配从库不配主库。
 - 主机配置了requirepass参数，需要密码登录；**从机要配置masterauth来设置校验密码**，否则主机就会拒绝主机的访问请求。
 - 基本操作命令

[note type="info flat"]主从复制:`replicaof 主库IP 主库端口`;配从库不配主库
改换门庭:`slave of 新主库IP 新主库端口`
自立为王:`slaveof no one`[/note]

案例需要使用三个虚拟机来模拟这个操作，配置，我用视频的形式来解释我只使用一个虚拟机来模拟三个不同的虚拟机的场景。实际上就是开三个进程，使用不同的配置文件，配置文件中配置好对应的信息和端口号什么的就可以。
[video title="主从复制配置准备 " url="https://img.kaijavademo.top/typecho/uploads/2023/09/videos/%E4%B8%BB%E4%BB%8E%E5%A4%8D%E5%88%B6%E5%87%86%E5%A4%87.mkv " container="b9u58112bu" subtitle=" " poster=" "] [/video]

后面启动的时候，从机一定要一边指定密码，一边指定端口号 
`redis-cli -a abc123 -p 6381` 

----------
###一主二仆
将其他两个从机打开，然后主机连接到服务器后，无论是主机还是从机，都可以输入 `info replication` 查看主从关系。
![5.png][5]

 - 从机可以执行写命令吗？

```Linux
127.0.0.1:6380> set k2 slave6380
(error) READONLY You can't write against a read only replica.

```
 [label color="red"]从机只可以读取，不可以写操作，没有写的权限，实现读写分离。[/label] 

 - 从机切入点问题
假设我的6381端口从机关机了，之后6379端口主机执行写操作。6380从机可以正常执行读操作。而再次启动6381端口的从机，**仍然存在之前6379所写的内容**。
 - 主机shutdown后，从机会上位吗？
**从机不动，原地待命**，从机数据可以正常使用；等待主机从重启动归来。
![6.png][6]

 - 主机shutdown后，重启后主从关系还在吗？从机能否顺利复制？
主从关系仍然存在，并且从机可以顺利复制。

 - 某台从机down后，master继续，从机重启后它能跟上大部队吗？
同第二种情况，从机切入点问题。仍然可以跟上大部队。

[note type="default flat"]命令操作手动指定：去掉从机配置文件中的配置项。使用`SLAVEOF 主库IP 主库端口`.让从机模拟重新找新的主机。仍然可以连上6379，数据也同步过来了。
命令指定：临时命令，单次生效。如果确定是主从关系，将其配置进入配置文件。[/note]

 [label color="red"]配置持久稳定，命令当次生效。[/label] 

###薪火相传
slave同样可以接收其他slaves的连接和同步请求，可以通过一个slave作为链条中下一个master，可以有效减轻主master的写压力。

中途变更转向，**会清除之前的数据，重新建立拷贝最新的**。
 `SLAVEOF 主库IP 主库端口` 
将6381 [label color="default"]改换门庭[/label] 改换为6380，这样类似于继承的关系。
 [label color="red"]而6380作为6379的从机，作为6381的主机，仍然无法进行写命令。[/label] 

###反客为主

使用 `SLAVEOF no one` 

```Linux
127.0.0.1:6381> SLAVEOF no one
OK
127.0.0.1:6381> info replication
# Replication
role:master
connected_slaves:0
master_failover_state:no-failover
master_replid:1b866515c61d3c90b2da31dc1356c6dc338514a7
master_replid2:54429140a07f7a5e5a15170ae290f36895038584
master_repl_offset:3371
second_repl_offset:3372
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:739
repl_backlog_histlen:2633
```

----------

[note type="warning flat"]复制的缺点：
①复制延时，信号衰减。
②master挂了怎么办？
默认情况下，不会在slave节点中重选一个master。如果没有master，系统几乎就是半瘫痪，只能读取，无法写入。
我们需要一个高可用的恢复机制。如果每次都要人工干预那么会很麻烦。无人值守变成了刚需。至此，就有Redis哨兵和Redis集群。
[/note]

----------
##Redis哨兵(☆)
主机shutdown后，长期宕机，我们只读不可写，无法满足系统高可用。我们达到的效果，我们需要寻找一个监控者，**在master宕机后，能够顺利把某个slave通过某个选举算法和机制，变成新的主机**。
吹哨人巡查监控后台master主机是否故障，如果故障了根据 [label color="red"]投票数[/label] 自动将某一个从库转换为新主库，继续对外服务。

[font size="16px" color="#ff69b4"]Redis Sentinel架构：前提说明
三个哨兵：自动监控和维护集群，不存放数据，只是吹哨人。
一主二从：用于数据读取和存放。[/font]
配置说明
[video title="使用一台虚拟机代替六台配置模拟哨兵 " url="https://img.kaijavademo.top/typecho/uploads/2023/09/videos/%E5%93%A8%E5%85%B5%E5%87%86%E5%A4%87.mkv " container="bkr2dtaf2m5" subtitle=" " poster=" "] [/video]

采用一台虚拟机，模拟三台 一主二从的关系，现在继续模拟三台哨兵在6379端口，修改哨兵的配置文件，调整哨兵认可客观下线等等的参数。
先开启一主二仆在当前这台虚拟机再开启一个终端，输入

```Linux
[root@redis100 myredis]# redis-sentinel sentinel26379.conf --sentinel
[root@redis100 myredis]# redis-sentinel sentinel26380.conf --sentinel
[root@redis100 myredis]# redis-sentinel sentinel26381.conf --sentinel
```
开启哨兵监控。
通过关闭主机，然后等待一会之后发现6381端口号已经变成了主机。当再次启动6379的时候，仍然是6381作为主机，6379降级为从机。

 `redis-cli -p 26379 shutdown` 关闭后台哨兵监控

[note type="primary flat"]①生成都是不同机房不同服务器，很少出现3个哨兵全挂掉的情况
②可以监控多个master，一行一个[/note]
###**哨兵的运行流程和选举原理**
[font size="17px" color="#ff0000"]三个哨兵监控一主二从，正常运行中...
Ⅰ.SDown主观下线：SDOWN(主观不可用)是单个sentinel自己主观上，如果发送了PING心跳后，在一定时间内没有收到合法的回复，就达到了SDOWN的条件。
Ⅱ.ODown客观下线：ODOWN需要一定数量的sentinel，多个哨兵达成一致意见,才能认为一个master客观上已经宕掉。
Ⅲ.选举出领导者哨兵：当主节点被判断客观下线以后，各个哨兵节点会进行协商，先选举出一个领导者哨兵节点（兵王）并由该领导者节点，也即被选举出的兵王进行failover（故障迁移）。（像神仙下凡）
**兵王如何选出？Raft算法。**
Ⅳ.由兵王(leader)开始推动故障切换流程并选出一个新master
①新主登基：选出新的master规则，即在剩余slave节点健康前提下，按照以下三个原则依次比较
 1. 在redis.conf文件中，优先级replica-priority最高的从节点(数字越小优先级越高)
 2. 复制偏移位置offset最大的从节点
 3. 最小Run ID的从节点(字典顺序,ASCII码)
②群臣俯首
 1. 执行`slaveof no one`命令让选出来的从节点成为新的主节点，并通过slaveof命令让其他节点成为其从节点
 2. **Sentinel leader**会对选举出的新master执行`slaveof no one`操作，将其提升为master节点
 3. **Sentinel leader**向其他slave发送命令，让剩余的slave成为新的master节点的slave
③旧主拜服
 1. 之前的master也回来认怂
 2. 将之前已下线的老master设置为新选出的新的master的从节点，当老master重新上线后，它会成为新的master的从节点
 3. **Sentinel leader**会让原来的master降级为slave并恢复正常工作[/font]


[note type="info flat"]上述的故障切换操作，均由sentinel自己独立完成，完全无需人工干预[/note]

[note type="default flat"]使用建议：
<1>哨兵节点的数量应为多个，哨兵本身应该集群，保证高可用
<2>哨兵节点的数量应该是奇数
<3>各个哨兵节点的配置应一致
<4>如果哨兵节点部署在Docker等容器里面，尤其要注意端口的正确映射
<5>哨兵集群+主从复制，并不能保证数据零丢失(实际生产中考虑到master宕机后，选举投票一系列操作)
之后我们会有集群，redis之父也推荐大家使用集群[/note]


----------
##Redis集群(☆)
Redis集群是一个提供在多个Redis节点间共享数据的程序集， [label color="red"]Redis集群可以支持多个Master[/label] 
 [label color="blue"]由于Cluster自带Sentinel的故障转移机制，内置了高可用的支持，[/label]  [label color="red"]无需再去使用哨兵功能[/label] 

###分片|槽位slot
 1. Redis集群没有使用一致性哈希算法，而是引入了哈希槽的概念。
集群有16384个哈希槽，每个key通过CRC16校验后对16384取模来决定放置哪个槽，集群的每个节点负责一部分哈希槽，将16384经可能平均分摊。

> The cluster's key space is split into 16384 slots, effectively setting an upper limit for the cluster size of 16384 master nodes (however, the suggested max size of nodes is on the order of ~ 1000 nodes).

官网建议最大节点约为1000个节点(槽)。

slot槽位映射，这里只记录了哈希槽分区，一致性hash分区的做法，实际上有其他两种做法。
####一致性Hash算法分区
目的是当服务器个数发生变动时，尽量减少影响客户端到服务器的映射关系
 - **算法构建一致性哈希环**
一致性Hash算法是对2^32取模，简单来说，一致性Hash算法将整个哈希值空间组织成一个虚拟的圆环
 - **服务器IP节点映射**
将各个服务器使用Hash进行一个哈希，具体可以选择服务器的IP或主机名作为关键字进行哈希，这样每台机器就能确定其在哈希环上的位置。
 - **key落到服务器的落键规则**
当我们需要存储一个kv键值对时，首先计算key的hash值，hash(key)，将这个key使用相同的函数Hash计算出哈希值并确定此数据在环上的位置， [label color="red"]从此位置沿环顺时针“行走”[/label] ，第一台遇到的服务器就是其应该定位到的服务器，并将该键值对存储在该节点上。

 [label color="red"]优点：加入和删除节点只影响哈希环中顺时针方向的相邻的节点，对其他节点无影响。[/label]
 [label color="green"]缺点：数据倾斜。服务节点太少，容易因为节点分布不均匀而造成数据倾斜[/label]  

####哈希槽分区
解决均匀分配的问题， [label color="red"]在数据和节点之间又加入了一层，把这层称为哈希槽（slot），用于管理数据和节点之间的关系[/label] ，现在就相当于节点上放的是槽，槽里放的是数据。

[font size="18px" color="#ff0000"]为什么redis集群的最大槽数是16384个？[/font]
redis的作者在他的官网有所解释
[原址][7]
![7.png][8]
 [label color="blue"]一.如果槽位为65536，发送心跳信息的消息头达8k，发送的心跳包过于庞大。[/label] 
在消息头中最占空间的是myslots[CLUSTER_SLOTS/8]。 当槽位为65536时，这块的大小是: 65536÷8÷1024=8kb 
在消息头中最占空间的是myslots[CLUSTER_SLOTS/8]。 当槽位为16384时，这块的大小是: 16384÷8÷1024=2kb 
因为每秒钟，redis节点需要发送一定数量的ping消息作为心跳包，如果槽位为65536，这个ping消息的消息头太大了，浪费带宽。
 [label color="blue"]二.redis的集群主节点数量基本不可能超过1000个。[/label] 
集群节点越多，心跳包的消息体内携带的数据越多。如果节点过1000个，也会导致网络拥堵。因此redis作者不建议redis cluster节点数量超过1000个。 那么，对于节点数在1000以内的redis cluster集群，16384个槽位够用了。没有必要拓展到65536个。
 [label color="blue"]三.槽位越小，节点少的情况下，压缩比高，容易传输[/label] 
Redis主节点的配置信息中它所负责的哈希槽是通过一张bitmap的形式来保存的，在传输过程中会对bitmap进行压缩，但是如果bitmap的填充率slots / N很高的话(N表示节点数)，bitmap的压缩率就很低。 如果节点数很少，而哈希槽数量很多的话，bitmap的压缩率就很低。

Redis不保证强一致性。


 2. 分片
集群中的每个Redis实例都被认为是整个数据的一个分片。

[note type="info flat"]为了找到给定key的分片，我们对key进行CRC16(key)算法处理并通过对总分片数量取模。然后，使用确定性哈希函数，这意味着给定的key将多次始终映射到同一个分片，我们可以推断将来读取特定key的位置。[/note]

分片 + 槽位 这种结构容易添加或者删除节点

###案例模拟
先将6台redis主机启动

```Linux
redis-server /myredis/cluster/redisCluster6381.conf
.....
redis-server /myredis/cluster/redisCluster6386.conf
```

使用一台虚拟机配置6份配置文件的形式，模拟三主机三从机

```redis
redis-cli -a abc123 --cluster create --cluster-replicas 1 192.168.29.12x:6381 192.168.29.12x:6382 192.168.29.12x:6383 192.168.29.12x:6384 192.168.29.12x:6385 192.168.29.12x:6386
```
 `--cluster-replicas 1 表示为每个master创建一个slave节点 ` 
表示以6381端口号创建slave节点6382，但是在执行后，还需要以**实际的分配**为主。

![8.png][9]
连接进入6381为切入点，查看节点状态。
 -  `info replication` 查看当前节点的主从关系
 -  `cluster info` 查看当前集群相关环境
 -  `cluster nodes` 查看所有集群的主从关系，还有哈希槽
![9.png][10]
####注意事项
以后连集群，启动需要使用 `redis-cli -a abc123 -p 6381 -c ` 这样在添加数据的时候，直接可以理解为重定向到对应端口。
**-c可以避免路由失效**
```Linux
[root@redis100 cluster]# redis-cli -a abc123 -p 6381 -c 
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
127.0.0.1:6381> keys *
(empty array)
127.0.0.1:6381> set k1 v1
-> Redirected to slot [12706] located at 192.168.29.128:6383
OK
192.168.29.128:6383> 

```
 - 查看某个key 属于对应的槽位值
 `CLUSTER KEYSLOT 键名称` 

 - 如果6381宕机了，那么6384能否作为从机上位成功？
![10.png][11]
6384成功上位，并可以正常使用。
 - 随后，6381原来的主机回来了，是否会上位？
![11.png][12]
6381不会上位， [label color="red"]并且以从节点的形式回归[/label] 。

我们也可以手动调整，节点从属调整，将原先的6381作为master，6384作为从机的结构调整回来。
 `CLUSTER FAILOVER` 节点从属调整
![12.png][13]


###扩容|缩容
埋个坑，回来填。ToT~~~


----------
##SpringBoot集成Redis
类比JDBC，我们需要使用一个中间件来控制Redis。
###Jedis
JedisClient是Redis官网推荐的一个面向java客户端，库文件实现了对各类API进行封装调用。

 - pom文件中导入**jedis依赖**

```xml
<!--jedis-->
        <dependency>
            <groupId>redis.clients</groupId>
            <artifactId>jedis</artifactId>
            <version>4.3.1</version>
        </dependency>
```
 - 修改redis配置文件(之前修改过)，更改防火墙配置，放行6379端口

需要在虚拟机上修改。
 `firewall-cmd --zone=public --add-port=6379/tcp --permanent` 
 `systemctl restart firewalld` 

```Linux
[root@redis100 ~]# firewall-cmd --zone=public --add-port=6379/tcp --permanent
success
[root@redis100 ~]# systemctl restart firewalld

```

 - 连接

在 [label color="default"]boot工程[/label] 原有的基础上，单独书写一个类，如果显示结果为**PONG**，那么就表示当前客户端连接成功。

```java
public class JedisDemo {
    public static void main(String[] args) {
        //连接，创建，告诉Jedis客户端访问哪台机器上面的，端口号是多少的服务器
        //1.connnection通过执行ip和端口号
        //这里并不规范，要么提出去书写，要么写配置文件
        Jedis jedis = new Jedis("192.168.29.xxx", 6379);

        //2.指定访问服务器的密码
        jedis.auth("abc123");

        //3.获得了jedis客户端，可以像jdbc一样,访问我们的redis
        System.out.println(jedis.ping());
```

###lettuce

 - pom文件中导入依赖

```xml
        <!--lettuce-->
        <dependency>
            <groupId>io.lettuce</groupId>
            <artifactId>lettuce-core</artifactId>
            <version>6.2.0.RELEASE</version>
        </dependency>
```

 - 测试

```java
public class LettuceDemo {
    public static void main(String[] args) {

        //1.使用构建器链式编程来builder我们的RedisURI
        //构建器模式
        RedisURI uri = RedisURI.builder()
                .redis("192.168.29.xxx")
                .withAuthentication("default","abc123")
                .build();
        
        //2.创建连接客户端
        RedisClient redisClient = RedisClient.create(uri);
        StatefulRedisConnection conn = redisClient.connect();
        
        //3.创建操作的command,通过conn创建command
        RedisCommands commands = conn.sync();
        //=====================业务逻辑=========================

        //=====================================================
        
        //4.各种关闭释放资源
        conn.close();
        redisClient.shutdown();

    }
}
```
###RedisTemplate(☆)
 [label color="red"]务必掌握[/label] 

####连接单机

[video title="连接单机 " url="https://img.kaijavademo.top/typecho/uploads/2023/09/videos/%E8%BF%9E%E6%8E%A5%E5%8D%95%E6%9C%BA.mkv " container="bzqxtcczz3c" subtitle=" " poster=" "] [/video]


 - 第一种解决乱码问题
使用**RedisTemplate**的子类**StringRedisTemplate**，并在启动redis的时候指定使用指令
 `redis-cli -a abc123 -p 6379 --raw` 
 - 第二种解决乱码问题
配置一个配置类 [label color="red"]@Configuration[/label] **RedisConfig**,并在其中配置序列化的方式，覆盖默认的JDK序列化。在启动的时候依然使用
 `redis-cli -a abc123 -p 6379 --raw` 指令
配置类**RedisConfig**配置

```java
@Configuration
public class RedisConfig {
    //用默认确实将程序写进去了，但是由于序列化问题，在redis中显示出现了问题
    /**
     * redis序列化的工具配置类，下面这个请一定开启配置
     * 127.0.0.1:6379> keys *
     * 1) "ord:102"  序列化过
     * 2) "\xac\xed\x00\x05t\x00\aord:102"   野生，没有序列化过
     * this.redisTemplate.opsForValue(); //提供了操作string类型的所有方法
     * this.redisTemplate.opsForList(); // 提供了操作list类型的所有方法
     * this.redisTemplate.opsForSet(); //提供了操作set的所有方法
     * this.redisTemplate.opsForHash(); //提供了操作hash表的所有方法
     * this.redisTemplate.opsForZSet(); //提供了操作zset的所有方法
     * @param lettuceConnectionFactory
     * @return
     */
    @Bean
    public RedisTemplate<String, Object> redisTemplate(LettuceConnectionFactory lettuceConnectionFactory)
    {
        RedisTemplate<String,Object> redisTemplate = new RedisTemplate<>();

        redisTemplate.setConnectionFactory(lettuceConnectionFactory);
        //设置key序列化方式string
        redisTemplate.setKeySerializer(new StringRedisSerializer());
        //设置value的序列化方式json，使用GenericJackson2JsonRedisSerializer替换默认序列化
        redisTemplate.setValueSerializer(new GenericJackson2JsonRedisSerializer());

        redisTemplate.setHashKeySerializer(new StringRedisSerializer());
        redisTemplate.setHashValueSerializer(new GenericJackson2JsonRedisSerializer());

        redisTemplate.afterPropertiesSet();

        return redisTemplate;
    }

}
```

####连接集群
启动六台redis集群环境下，修改YML配置文件，启动微服务端口。
注意使用这样的指令连接，指定端口，还有重定向并显示中文。
 `redis-cli -a abc123 -p 6381 -c --raw` 
修改yml配置文件。改成redis集群那一套使用就可以了。

```properties
server.port=7777

spring.application.name=redis7_study

# ========================logging=====================
logging.level.root=info
logging.level.com.atguigu.redis7=info
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger- %msg%n 

logging.file.name=D:/mylogs2023/redis7_study.log
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger- %msg%n

# ========================swagger=====================
spring.swagger2.enabled=true
#在springboot2.6.X结合swagger2.9.X会提示documentationPluginsBootstrapper空指针异常，
#原因是在springboot2.6.X中将SpringMVC默认路径匹配策略从AntPathMatcher更改为PathPatternParser，
# 导致出错，解决办法是matching-strategy切换回之前ant_path_matcher
spring.mvc.pathmatch.matching-strategy=ant_path_matcher

# ========================redis单机=====================
#spring.redis.database=0
# 修改为自己真实IP
#spring.redis.host=192.168.29.128
#spring.redis.port=6379
#spring.redis.password=abc123
#spring.redis.lettuce.pool.max-active=8
#spring.redis.lettuce.pool.max-wait=-1ms
#spring.redis.lettuce.pool.max-idle=8
#spring.redis.lettuce.pool.min-idle=0
# ========================redis集群=====================
spring.redis.password=abc123
# 获取失败 最大重定向次数
spring.redis.cluster.max-redirects=3
spring.redis.lettuce.pool.max-active=8
spring.redis.lettuce.pool.max-wait=-1ms
spring.redis.lettuce.pool.max-idle=8
spring.redis.lettuce.pool.min-idle=0
#支持集群拓扑动态感应刷新,自适应拓扑刷新是否使用所有可用的更新，默认false关闭
spring.redis.lettuce.cluster.refresh.adaptive=true
#定时刷新(自适应时间)
spring.redis.lettuce.cluster.refresh.period=2000
spring.redis.cluster.nodes=192.168.29.12x:6381,192.168.29.12x:6382,192.168.29.12x:6383,192.168.29.12x:6384,192.168.29.12x:6385,192.168.29.12x:6386
```

----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。

  [1]: https://img.kaijavademo.top/typecho/uploads/2023/09/1133733863.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/09/498611805.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/09/509641957.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/09/1094831621.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/09/1469942289.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/09/3807472881.png
  [7]: https://github.com/redis/redis/issues/2576
  [8]: https://img.kaijavademo.top/typecho/uploads/2023/09/3404335116.png
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/09/648862780.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/09/2683497102.png
  [11]: https://img.kaijavademo.top/typecho/uploads/2023/09/1683979174.png
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/09/2873374631.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/09/2191754425.png