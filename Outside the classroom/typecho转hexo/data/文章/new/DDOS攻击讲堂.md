---
title: DDOS攻击讲堂
date: 2021-05-13 14:29:00
categories: 教程类
tags: []
---
DDOS是一种分布式拒绝攻击，在我们计算机这类科目中，会发现它对我们的服务器或者工作站以及主机威胁十分巨大，毕竟它是伪装成正常访问，然后大量访问你服务器的资源，造成其他用户无法使用。

对于DDOS来说，我将其分为八大类：

**1、基于自动化程度分类**

（1）手工的DDoS攻击。

早期的DDoS攻击全是采用手动配置的，即发动DDoS攻击时，扫描远端有漏洞的计算机，侵入它们并且安装代码全是手动完成的。

（2）半自动化的DDoS攻击。

在半自动化的攻击中，DDoS攻击属于主控端一代理端的攻击模型，攻击者用自动化的Scripts来扫描，主控端的机器对主控端和代理端之间进行协商攻击的类型、受害者的地址、何时发起攻击等信息由进行详细记录。

（3）自动化的DDoS攻击。

在这类攻击中。攻击者和代理端机器之间的通信是绝对不允许的。这类攻击的攻击阶段绝大部分被限制用一个单一的命令来实现，攻击的所有特征，例如攻击的类型，持续的时间和受害者的地址在攻击代码中都预先用程序实现。

**2、基于系统及协议的弱点分类**

（1）洪水攻击。

在洪水攻击中。傀儡机向受害者系统发送大量的数据流为了充塞受害者系统的带宽，影响小的则降低受害者提供的服务，影响大的则使整个网络带宽持续饱和，以至于网络服务瘫痪。典型的洪水攻击有UDP洪水攻击和ICMP洪水攻击。

（2）扩大攻击。

扩大攻击分为两种，一种是利用广播lP地址的特性，一种是利用反射体来发动攻击。前一种攻击者是利用了广播IP地址的特性来扩大和映射攻击，导致路由器将数据包发送到整个网络的广播地址列表中的所有的广播IP地址。这些恶意的流量将减少受害者系统可提供的带宽。典型的扩大攻击有Smurf和Fraggle攻击。

（3）利用协议的攻击。

该类攻击则是利用某些协议的特性或者利用了安装在受害者机器上的协议中存在的漏洞来耗尽它的大量资源。典型的利用协议攻击的例子是TCP SYN攻击。

（4）畸形数据包攻击。

攻击者通过向受害者发送不正确的IP地址的数据包，导致受害系统崩溃。畸形数据包攻击可分为两种类型：IP地址攻击和IP数据包属性攻击。

**4、基于攻击速率分类**

DDoS攻击从基于速率上进行分类，可以分为持续速率和可变速率的攻击。持续速率的攻击是指只要开始发起攻击，就用全力不停顿也不消减力量。像这种攻击的影响是非常快的。可变速率的攻击，从名字就可以看出，用不同的攻击速率，基于这种速率改变的机制，可以把这种攻击分为增加速率和波动的速率。 \[4\]

**5、基于影响力进行分类**

DDoS攻击从基于影响力方面可以分为网络服务彻底崩溃和降低网络服务的攻击。服务彻底崩溃的攻击将导致受害者的服务器完全拒绝对客户端提供服务。降低网络服务的攻击，消耗受害者系统的一部分资源，这将延迟攻击被发现的时间，同时对受害者造成一定的破坏。 \[4\]

**6、基于入侵目标分类**

DDoS攻击从基于入侵目标，可以将DDoS攻击分为带宽攻击和连通性攻击，带宽攻击通过使用大量的数据包来淹没整个网络，使得有效的网络资源被浪费，合法朋户的请求得不到响应，大大降低了效率。而连通性攻击是通过发送大量的请求来使的计算机瘫痪，所有有效的操作系统资源被耗尽，导致计算机不能够再处理合法的用户请求。 \[4\]

**7、基于攻击路线分类**

（1）直接攻击：攻击者和主控端通信，主控端接到攻击者的命令后，再控制代理端向受害者发动攻击数据流。代理端向受害者系统发送大量的伪IP地址的网络数据流，这样攻击者很难被追查到。

（2）反复式攻击通过利用反射体，发动更强大的攻击流。反射体是任何一台主机只要发送一个数据包就能收到一个数据包，反复式攻击就是攻击者利用中间的网络节点发动攻击。

**8、基于攻击特征分类**

从攻击特征的角度，可以将DDoS攻击分为攻击行为特征可提取和攻击行为特征不可提取两类。攻击行为特征可提取的DDoS攻击又可以细分为可过滤型和不可过滤型。可过滤型的DDoS攻击主要指那些使用畸形的非法数据包。不可过滤型DDoS攻击通过使用精心设计的数据包，模仿合法用户的正常请求所用的数据包，一旦这类数据包被过滤将会影响合法用户的正常使用。

对于这种情况，我想了三个应对措施。

**1、**在一些发布平台上面不要用直接套着服务器IP进行访问，毕竟这样永远是无法成功拦截这些伪装访问者。

**2、**服务器请求与服务器资源分布式发送数据（例如内容分发网络cdn），即使被DDOS了，打的也是一个节点，能暂时正常运行网站。

**3、不要做对不起别人的事情，避免自己遭殃。**

今天知识的普及到这里，感谢大家
