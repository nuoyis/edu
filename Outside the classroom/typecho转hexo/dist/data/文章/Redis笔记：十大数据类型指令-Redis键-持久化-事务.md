---
title: Redis笔记：十大数据类型指令-Redis键-持久化-事务
date: 2023-09-10 09:12:00
categories: Redis
tags: [事务,Redis7,数据库,十大数据类型,Linux,消息队列,持久化]
---
Redis是一种键值对类型的缓存数据库，在Linux下使用，基于Redis7的入门笔记,写的很入门,已完结。包括Redis键，value中所对应的所有数据结构，以及持化双雄AOF + RDB，还有Redis的事务。


<!--more-->
##初始化

 - 启动redis

 `-a 密码`  -a后面跟在redis.config中设置的密码 **-p**默认不写端口号就是**6379**.
```Linux
redis-server /myredis/redis7.conf
redis-cli -a abc123
```

 - 关闭

如果是在服务器内部直接使用 `SHUTDOWN` 关闭即可
如果是在远程可以使用单实例关闭

```Linux
redis-cli -a abc123 shutdown
```

 - 退出
 `quit` 


----------

##十大数据类型
这里我们所说的数据类型是指的是**value**的数据类型，key的数据类型都是字符串。
命令不区分大小写，**key是区分大小写**的。
###String
Redis中用的最频繁的，最重要，绝绝对对的一号男神。String类型是 [label color="red"]二进制安全[/label] 的，支持序列化。相当于String可以包含任何数据，一个key对应一个value，是最重要最基本的数据类型，一个redis中字符串value最多是512M。

```Redis
set key value [...] # 这里面有五个关键参数，留意keepttl
get key
# 同时设置/获取多个值
mset key value [key value...] 
mget key [key...]
getrange key 0 -1# 获取指定区间范围内的值(0 -1 表示获取所有值，以后不再赘述)
setrange key index abc # 将abc开始赋值给key对应value的下标index
incr key # 递增数字，等同于++
incrby key number #为key的value值递增指定的数字number
decr key # 递减数字，等同于--
strlen key # 获取key的对应的值的长度
append key value # 将value追加到key对应值之后
setnx key value # 当key不存在的时候创建
setex key secounds value # 创建key的时候设置过期时间secounds
getset # 等同于set key value GET

```
 [label color="blue"]应用场景：抖音的无限点赞某个视频[/label] 


----------

###List(列表)
类比Java，Redis列表是简单的字符串列表，可以添加元素到 [label color="blue"]头部[/label] 或者 [label color="blue"]尾部[/label] ，底层是一个**双端链表**。

```Redis
lpush/rpush list(key) 1 2 3 4 # 从左边添加数据/从右边添加数据，注意从左边添加数据的时候数据会像进栈一样，先进入的在右边
lrange list(key) 0 -1 #从左侧遍历
lpop/rpop  list(key) #从左端点弹出数据/从右端点弹出数据
lindex list(key) 0 # 按照索引下标获得元素
llen list(key) # 返回当前list集合的长度，相当于Java中的size
lrem list(key) N v1 # 删除N个值等于v1的元素
ltrim list  startIndex endIndex # 删除起始到终止索引的元素
rpoplpush list1 list2 # 将list1的第一个元素(尾部)弹出，压入list2中。
lset list(key) index value # 将某个集合(key)的index下标对应的元素替换为value值 
linsert list(key) before/after  value1 value2 # 在某个集合value1的前面/后面插入value2
```
 [label color="blue"]应用场景：微信号订阅的消息[/label] 


----------


###Hash哈希表
类比Java `Map<String,Map<Object,Object>>` 
[note type="default flat"]以前 key1 value1
现在 key1 field value1[/note]

```Redis
hset key field value [field value...] # 添加一个数据
hget key field # 查询某个数据
hmset key field value... # 一次性添加多个数据
hmget key field field ..# 一次性查询某个key的多个数据
hgetall key # 遍历key的值所有数据，包括field 和 value
hdel key field # 删除key中值的field属性
hlen key # 返回当前key中的所有属性个数
hexists key field # 查询当前属性存不存在，如果存在返回1，不存在返回0
hkeys key # 遍历当前key的值的所有属性(field)
hvals key # 遍历当前key的值的所有属性值(value)
hincrby/hincrbyfloat key field number(value) # 为某个属性值添加任意大小的整数或者是浮点数
hsetnx key field value # 为某个不存在的key设置某个属性，如果已经存在返回0

```
 [label color="blue"]应用场景：早期JD购物车[/label] 


----------

###Set
Redis中Set是String类型的无序集合，**无序无重复**，集合对象的编码可以是intset或者是hashtable。

```Redis
sadd key member [member...] # 添加元素(自动去重)
smembers key(set) # 遍历集合中的所有元素
sismember key member # 判断元素member是否在集合key中
srem key member [member...] # 删除元素
scard key # 获取集合里面元素个数
srandmember key number #从集合中随机展示number个元素个数，元素不删除
spop key number # 从集合中随机弹出number个元素，并删除。
smove key1 key2  number # 将key1中存在的number赋给key2集合
sdiff key1  key 2 [key3...] # 做集合的差集运算  (key1-key2)
sunion key1  key 2 [key3...]# 做集合的并集运算
sinter key1 key2  # 做集合的交集运算
sintercard numkeys key1  key2 [key3] [LIMIT limit] # 显示numkeys个集合的交集中的元素个数(基数)，并可以限制展示数limit。
```
 [label color="blue"]应用场景：微信抽奖小程序，朋友圈点赞查看同赞朋友，猜你喜欢，QQ推荐你可能认识的人[/label] 


----------


###ZSet(Sorted Set)
可排序的Set，同Set也是String类型，不允许重复。 [label color="red"]不同的是每个元素都会关联一个double类型的分数，zset的成员是唯一的，但是分数却可以重复。[/label] ,通过分数为集合中的成员进行从小到大的排序。

[note type="flat"]k1 v1
k1 score v1 score v2[/note]

```Redis
zadd key score member(value) [score member ...] # 添加元素
zrange key start end [withscores] # 按照元素分数从小到大的顺序，返回索引从start到end之间的元素
zrevrange key start end [withscores]# 按照元素分数逆序(从大到小)排序
zrangebyscore key min max [ ( ][withscores] [limit offset count] # 获取指定分数范围内的元素，(代表不包含，limit限制返回条数。
zscore key member # 获取member元素在key中的分数
zcard key # 获取集合中的元素数量
zrem key value(member) # 删除集合中的某个value元素。
zincrby key increment member # 往对应集合元素member中添加increment的分数
zcount key min max # 获取指定分数范围内的元素个数
zmpop numkeys key min/max count number # 弹出多个key中的最高或者是最低的元素number个。他们是成员分数对。
zrank key values #获得value在key中的下标
zrevrank key values # 逆序获得value在key中的下标
```
 [label color="blue"]应用场景：根据商品销售队商品进行排序显示[/label] 


----------

###地理空间GEO
就是经纬度，主要存储地理位置信息，对存储的信息进行操作，包括添加计算。

> 高德地图附近的酒店..

```Redis
geoadd key latitude  longitude name [latitude  longitude name] # 为当前key添加name的经纬度坐标
geopos key name  [name...] # 返回name的经纬度坐标
geohash key name [name...] #返回name的经纬度坐标用geohash算法生成的base32编码值
geodist key name1 name2 m/km... # 返回name1和name2位置之间的距离，用m/km...单位表示
georadius key latitude  longitude distance(10km/..)
[withdist withcoord withhash ]count number desc/asc #以半径为中心，查找当前经纬度附近的其他点
georadiusbymember key name  distance(10km/..)
[withdist withcoord withhash ] count number # 通过名称查找指定范围内的元素
```


----------

###基数统计HyperLogLog
在输入元素的数量或者体积非常大的时候，计算基数所需的空间固定往往是很小的。
统计某个网站的UV、统计某个文章的UV(需要去重考虑),用户搜索网站关键词的数量。对于大型网站，UV大概是亿级别的，为了不需要占用太多内存。就出现了这样一种**去重统计功能的基数估计算法**HyperLogLog。

> 淘宝，京东，天猫的每天访问量很大，记录每天的访问量就需要有一种基数(不重复的ip，不重复的数字)，我们要想在节约内存的情况下，还要统计的尽量精确，就要使用**HyperLogLog**。

```Redis
pfadd key element[element...] # 添加指定元素到HyperLogLog中(去重)
pfcount #返回对应key中的基数估计值
prmerge key sourcekey [sourcekey...] # 将多个HyperLogLog sourcekey合并为一个key
```


----------

###Bitmap位图
由0和1状态表现的二进制位的bit数组，比如每日签到，钉钉打卡...

```Redis
setbit key offset value # 在offset的偏移位上赋值0/1
getbit key offset # 查询offset的偏移位上的数值
strlen key # 查询key的字节数(8bit为一个字节)占用多少
bitcount # 统计key里面含有1的有多少个
bitop and key key1 key2 # 将key1和key2中共有的偏移量相同且同时为1的结果赋值给key

```
 [label color="blue"]应用场景：签到，按照全年天天登录[/label] 
![1.png][1]


----------

###Bitfield位域
可以一次性操作比特位域，对比特位域进行值的替换，实行实时数据的替换和查找。
所用不多，了解即可
 - 位域修改
 

```Redis
bitfield key get type offset # 从第offset位开始，获取type类型的二进制数并以十进制返回
bitfield key set type offset value# 从第offset位开始，获取type类型，并设置value。
bitfield key incrby type offset increment # 从第offset位开始，获取type类型，并自增increment 
#溢出控制第二种案例
BITFIELD test overflow sat set i8 0 128
#溢出控制第三种案例
BITFIELD test overflow fail set i8 0 888
```
- 溢出控制
 1. WRAP：默认，使用回绕方法处理有符号整数和无符号整数的溢出情况
 2. SAT：使用饱和计算方法处理溢出，即下溢计算的结果为最小的整数值(-128)，而上溢计算的结果为最大的整数值(127)。
 3. FAIL：命令将拒绝那些会导致上下溢出的情况出现的计算，向用户返回空值表示计算未被执行。

----------

###Redis流(Stream)
Redis版本的**消息队列，消息中间件(MQ) + 阻塞队列**。
**消息队列的两种方案**

 - List实现消息队列
 **点对点模式**，[label color="red"]常用来做异步队列使用[/label] ，将需要延后处理的任务结构体序列化成字符串塞进Redis的列表，另一个线程从这个列表中轮询数据进行处理。
![2.png][2]

 - Pub/Sub
基于以上两种各有痛点，5.0版本新增了一个强大的数据结构Stream。

 - 队列+生产者指令

```Redis
xadd key id/*  key value # 添加消息到队列末尾，*表示让系统自动生成id
xrange key - + [count number] #获取消息列表，可以指定范围,-代表最小值，+代表最大值
xrevrange key + - [count number] #获取消息列表的元素是相反的，是从大到小的。
xdel key id # 通过id删除一条消息
xlen key # 查看队列中消息的个数
xtrim key maxlen  number # 允许最大长度，队流进行限制长度。
xtrim key minid # 允许最小的id ，从某个id开始比它小的将会被抛弃

#用于获取消息
#count表示最多读取多少条消息
#block表示是否以阻塞的方式读取消息，默认不阻塞，0为永远阻塞
#非阻塞
xread count number streams key $ # $代表特殊ID，表示以当前Stream已经存储的最大的ID作为最后一个ID，当前Stream中不存在大于当前最大ID的消息，因此此时返回nil
xread count number streams key 0-0 # 表示从最小的id开始获取stream中的消息，不指定count，返回所有消息。
#阻塞
xread count 1 block 0 streams key $ #获取比当前队列中已经存储的最大消息还要大(新) 的消息
```
 - 消费组指令

```redis
xgroup create stream group $/0 # 用于创建消费者组
$表示从stream尾部开始消费，0表示从stream头部开始消费。
xreadgroup group  groupname consumer stream streamname > # 指定消费组中的消费者，从第一条消息未被消费的消息开始读取，将会读取消息队列中所有消息。但是，不同消费组消费者可以消费同一条消息。
xreadgroup group  groupname consumer  count countNumber stream streamname > # 消费者将从未被消费的消息开始按照指定的行数读取。
xpending stream group # 查看消费组内所有消费者的读取，但未确认的信息；并查看某个消费者具体读取了哪些数据。 
xack stream group id # 根据id向消息队列确认消息已经处理完成
xinfo stream streamName # 用于打印Stream\Consumer\Group的详情信息

```
![3.png][3]

----------
##Redis键(key)

 - 常用key命令

```Redis
keys * # 查看当前库所有的key
exists key # 判断某个key是否存在
type key # 查看key是什么类型
del key # 删除指定的key数据
unlink key # 非阻塞删除，仅仅将keys从keyspace元数据中删除，真正的删除会在后续的异步中操作。
expire key 秒数 # 为给定的key设置过期时间
ttl key # 查看还有多少秒过期，-1表示永不过期，-2表示已经过期
move key dbindex 0-15 # 将当前数据库的key移动到指定数据库的db(16个 0-15)中
select dbindex 0-15 # 切换数据库[0-15] ，默认为0数据库
dbsize # 查看当前所在的数据库中key数量
flushdb # 清空当前库，慎用
flushall # 通杀全部库，慎用
```


----------
##持久化
我们需要Redis的缓存里面的**数据长期持有**，宕机后还是可以从硬盘中读回之前保存的数据。
###RDB
在指定的时间间隔以内，执行数据集的时间点快照。将内存数据整体打包形成快照文件，写进磁盘上，让数据可靠性得到保证。
全称**dump.rdb**
在7以后，RDB变化频率和6相比有所不同
6的快照Snapshotting
![4.png][4]
7的快照
![5.png][5]

官网上，RDB分为手动触发和自动触发
####自动触发

> You can configure Redis to have it save the dataset every N seconds if there are at least M changes in the dataset, or you can manually call the SAVE or BGSAVE commands.

 1. 案例5秒2次修改
配置文件433行下设置
 `save 5 2` 
 2. 修改dump文件保存路径
505行中书写
 `dir /myredis/dumpfiles` 
 3. 修改dump文件名称
建议配置上端口号
 `dbfilename dump6379.rdb` 
 4. 触发备份
**情况一**
![6.png][6]
**情况二**
![7.png][7]

 5. 恢复
 [label color="red"]执行flushall/flushdb命令也会产生dump.rdb文件，但里面是空的，无意义。[/label] 
 [label color="red"]将redis服务关闭也会产生一个dump.rdb文件。[/label] 
物理恢复，**一定要将有正确数据的rdb文件进行备份迁移，将服务和备份进行分机隔离**。

当redis启动的时候，会按照我们的配置，将会在指定路径下面读取dump文件进行数据恢复，已达到数据一致性。

####手动触发
实际生产中对于配置多少分钟多少次修改是写死的，将重要数据读取读取进来的时候，我需要保存，就需要手动触发，将手动触发覆盖自动触发，以最新的命令进行保存。
 - SAVE
主程序执行会阻塞当前的redis服务器，直到持久化工作完成，在执行此命令期间，redis不能处理其他命令， [label color="red"]线上禁止使用[/label] 。
 - BGSAVE
Redis会在后台异步进行快照操作，不阻塞快照的同时还可以响应客户端请求，该触发方式会fork一个子进程由子进程复制持久化的过程。Redis会使用bgsave对当前内存中的所有数据做快照，这个操作是在子进程在后台完成的，这就允许主进程同时可以修改数据。
开启
 `bgsave` 
可以通过lastsave命令获取最后一次成功执行的快照的时间,显示时间戳。可以使用指令转化为具体时间。

```linux
date -d @1694676572
```

[note type="warning flat"]RDB优缺点
优点：
①是Redis数据的一个非常紧凑的单文件时间点表示。RDB非常适合备份，非常适合在发生灾难的时候轻松恢复不同版本的数据集。
②RDB非常适合灾难恢复，可以传输到远程数据中心。
③RDB最大程度提高了Redis的性能，因为Redis父进程为了持久化而需要做的唯一工作就是派生一个将完成其余工作的子进程，父进程永远不会执行磁盘IO类似的操作
简言之：适合大规模的数据恢复；按照业务定时备份；对数据完整性和一致性要求不高；RDB文件在内存中的加载速度要比AOF快得多。
缺点：
①一定间隔时间作为备份，如果意外宕机，就会丢失从当前最近的一次快照期间的数据， [label color="red"]快照之间的数据会丢失[/label] 
②内存数据的全量同步，如果数据量太大，就会导致I/O严重影响服务器性能。
③RDB依赖于主进程的fork，在更大的数据集中，这可能会导致服务请求的瞬间延迟。fork的时候内存中的数据被克隆了一份，大致两倍的膨胀性，需要考虑。

[/note]

----------
###AOF
持久化的第二种技术，**以日志的形式来记录每个写操作**，将执行过的所有指令记录下来(读操作不记录)，只许追加文件，不可以改写文件。redis重启的话就根据日志文件的内容将写指令从前到后执行一次以完成数据的恢复工作。默认情况下，redis没有开启AOF的功能，需要在配置文件中设置。AOF保存的是**appendonly.aof**文件。(AOF好像作为一名学渣抄学霸的作业啊)
[官网解释][8]

> Snapshotting is not very durable. If your computer running Redis stops, your power line fails, or you accidentally kill -9 your instance, the latest data written to Redis will be lost. While this may not be a big deal for some applications, there are use cases for full durability, and in these cases Redis snapshotting alone is not a viable option.

写回策略appendfsync
 - Always 同步写回，每个写命令执行完立刻同步地将日志写回磁盘。(持续的磁盘IO降低了服务器的性能)
 - no 操作系统控制的写回，每个写命令执行完，只是先把日志写到AOF文件的内存缓冲区，由操作系统决定何时将缓冲区的内容写回磁盘。
以上两个属于两种极端，第二种直接躺平了哈哈，很容易丟取数据。
 - everysec 每秒写回，每个写命令执行完，只是先把日志写到AOF文件的内存缓冲区，每隔一秒把缓冲区中的内容写入磁盘。也是磁盘默认的写入策略。

配置项|写回时机|优点|缺点
:--:|:--:|:--:|:--:
Always|同步写回|可靠性高，数据基本不丢失|每个写命令都要落盘，性能影响较大
Everysec|每秒写回|性能适中|宕机时丢失1秒内的数据
No|操作系统控制的写回|性能好|宕机时丢失数据较多

####正常恢复

 - 开启AOF
在配置文件1380行 `appendonly yes` 
 - 重新调整保存路径
![8.png][9]
开启AOF功能后，写操作继续，生成AOF文件到指定的目录
重启redis，然后重新加载。
![9.png][10]

####异常恢复
在高并发中，有可能出现内容写一小半，没有写完整，突然redis挂了，怎么样修复AOF文件完成数据的恢复。
在appendonly路径下输入改行对于incr.aof文件进行修复，命令中一定要添加 `--fix` 

```Linux
[root@XXX appendonlydir] # redis-check-aof --fix appendonly.aof.1.incr.aof
```
该异常修复命令，将文件不符合语法规则的统统清空，再重新启动。

####重写机制
AOF重写不仅降低了文件的占用空间，同时更小的AOF也可以更快地被Redis加载。
 - [开启aof][11]
 - 修改重写峰值1k
 - 自动触发AOF重写机制(瘦身计划)
![10.png][12]
 - 手动触发AOF重写机制
使用 `BGREWRITEAOF` 手动写入，直接更新文件名。
![11.png][13]

**也就是说，AOF文件重写并不是对原文件进行重新整理，而是直接读取服务器现有的键值对，然后用一条命令去代替之前记录的这个键值对的多条命令，生成一个新的文件后去替换原来的AOF文件。**

[note type="info flat"]总结
1.AOF文件是一个只进行追加的日志文件
2.Redis可以在AOF文件体积变得过大时，自动地在后台对AOF进行重写
3.AOF文件有序的保存了对数据库执行的所有写操作，这些写入操作以Redis协议的格式保存，因此AOF的文件内容非常容易被人读懂，对文件进行分析也很轻松
4.对于相同的数据集来说，AOF文件的体积通常要大于RDB文件的体积
5.根据所使用的fsync策略，AOF的速度可能会慢于RDB。
[/note]


----------
###RDB+AOF混合持久化
官方文档

> The general indication you should use both persistence methods is if you want a degree of data safety comparable to what PostgreSQL can provide you.

告诉我们RDB和AOF可以共存。数据恢复流程和加载流程。
如果同时开启rdb和aof持久化时，重启时只会加载aof文件，不会加载rdb文件
![12.png][14]
 1. 开启混合方式设置
 [label color="red"]设置aof-use-rdb-preamble的值为 yes[/label]    yes表示开启，设置为no表示禁用
 2. RDB + AOF的混合方式
RDB镜像做全量持久化，AOF做增量持久化。
先使用RDB进行快照存储，然后使用AOF持久化记录所有的写操作，当重写策略满足或手动触发重写的时候，**将最新的数据存储为新的RDB记录**。重启服务的时候会从RDB和AOF两部分恢复数据，既保证了数据的完整性，又提高了恢复数据的性能。简单来说混合持久化方式产生的文件一部分是RDB格式，一部分是AOF格式。


----------
##Redis事务

[note type="flat"]回顾：事务：在一次与数据库的连接会话中，所有执行的sql要么一起成功，要么一起失败。这是传统的数据库事务。[/note]
redis事务本质是一组命令的集合。一个事务中的所有命令都会序列化， [label color="red"]按照顺序地串化执行而不会被其他命令插入，不许加塞[/label] 。
在一个**队列**中，一次性、顺序性、排他性的执行一系列操作
###正常执行

将 `MULTI` 和 `EXEC` 中间插入事务的相关语句，在输入`EXEC`同时一起执行。
```Linux
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379(TX)> set k1 v1
QUEUED
127.0.0.1:6379(TX)> set k2 v2
QUEUED
127.0.0.1:6379(TX)> set k3 v3
QUEUED
127.0.0.1:6379(TX)> incr count
QUEUED
127.0.0.1:6379(TX)> EXEC
1) OK
2) OK
3) OK
4) (integer) 2
127.0.0.1:6379> get k3
"v3"

```
![13.png][15]
###放弃事务
将 `MULTI` 和 `DISCARD` 中间插入事务的相关语句，在输入`DISCARD`后将不再执行该队列中的事务。

```Linux
127.0.0.1:6379> MULTI
OK
127.0.0.1:6379(TX)> set k1 v1
QUEUED
127.0.0.1:6379(TX)> set k2 v22
QUEUED
127.0.0.1:6379(TX)> incr count
QUEUED
127.0.0.1:6379(TX)> DISCARD
OK
127.0.0.1:6379> get count
"2"

```
![14.png][16]
###全体连坐
假设四条命令一条命令出错，将全部打回。
在事务语句中出现错误，在执行exec之前，会返回所有命令，均不执行。

###冤头债主
表示对的指令将放行，错的将打回。
编译通过，运行出现错误，就会导致问题。出错了对于传统数据库可以rollback，但是Redis事务不支持**事务回滚**。
![15.png][17]

###Watch监控
Watch命令是一种乐观锁的实现。
Redis在修改的时候会检测数据是否被更改，如果更改了，则执行失败。
举例：给一个key增加监控，开启事务，然后另一个线程优先修改了这个key的value值。那么事务将修改失败，key的value值以另一个线程的优先修改为主。事务中的其他指令将执行失败
![16.png][18]
####unwatch放弃监控
依然监控一个key，但是我发现另一个线程优先修改了它的value值，那么我可以采用放弃监控 `unwatch` 策略，并在此线程开启事务中可以再次修改这个key。提交后以当前线程修改的key值为主，并且不会报**nil**(修改失败)。

[note type="flat"]总结
①一旦执行了exec之前加的监控锁都会被取消掉了
②客户端退出连接，或连接丢失，所有东西都会被取消监视[/note]


[note type="success flat"]事务总结：
开启：以MULTI开启一个事务
入队：将多个命令入队到事务中，**接到这些命令并不会立即执行**，而是放到等待执行的事务队列里面
执行：由EXEC命令触发事务提交，执行事务队列里的所有命令[/note]


----------
我书写这篇文章的初衷就是总结学习的进度，遗忘之际可以拿出来翻看，如有不对的地方还望指正，多多海涵。


  [1]: https://img.kaijavademo.top/typecho/uploads/2023/09/1203197247.png
  [2]: https://img.kaijavademo.top/typecho/uploads/2023/09/1373410993.png
  [3]: https://img.kaijavademo.top/typecho/uploads/2023/09/2507374282.png
  [4]: https://img.kaijavademo.top/typecho/uploads/2023/09/2275519188.png
  [5]: https://img.kaijavademo.top/typecho/uploads/2023/09/192978406.png
  [6]: https://img.kaijavademo.top/typecho/uploads/2023/09/4156134368.png
  [7]: https://img.kaijavademo.top/typecho/uploads/2023/09/3232536427.png
  [8]: https://redis.io/docs/management/persistence/#append-only-file
  [9]: https://img.kaijavademo.top/typecho/uploads/2023/09/784761122.png
  [10]: https://img.kaijavademo.top/typecho/uploads/2023/09/1421270384.png
  [11]: https://www.kaijavademo.top/400.html#cl-20
  [12]: https://img.kaijavademo.top/typecho/uploads/2023/09/4106533966.png
  [13]: https://img.kaijavademo.top/typecho/uploads/2023/09/898272188.png
  [14]: https://img.kaijavademo.top/typecho/uploads/2023/09/143508311.png
  [15]: https://img.kaijavademo.top/typecho/uploads/2023/09/1965791205.png
  [16]: https://img.kaijavademo.top/typecho/uploads/2023/09/4239860190.png
  [17]: https://img.kaijavademo.top/typecho/uploads/2023/09/1256023190.png
  [18]: https://img.kaijavademo.top/typecho/uploads/2023/09/2061084565.png