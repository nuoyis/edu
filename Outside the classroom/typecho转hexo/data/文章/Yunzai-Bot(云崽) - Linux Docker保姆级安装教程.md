---
title: Yunzai-Bot(云崽) - Linux Docker保姆级安装教程
date: 2023-01-25 18:14:00
categories: 教程类
tags: []
---
>看了很多网上讲解的云崽,都感觉没有完全讲清楚Linux用户使用docker方法(windows我没咋用过,这里windows怎么套娃我就不说了)

而且官方文档内的docker脚本中gitee内部三个js文件均没有同步成功,显示[session-a24140b4] Repository or file not found,难怪会报错三个js内容。
以下内容如果你觉得麻烦,我的云盘里面有配置好的(插件有些,gitee版本少几个插件,data已经删掉需要重新执行后面指令)
-----------视频教程-----------
[#BV#](https://www.bilibili.com/video/BV1t24y1z7Wp)

-----------文字教程-----------
服务器(或家里小主机、电脑)要求:2核2G(推荐配置) 硬盘60-100GB
推荐系统:alios
目前还没服务器(不想折腾家里)?点击[这里](https://www.rainyun.com/NDEwMzk=_)获取nat低价服务器(有增值营业执照)
环境要求:有docker运行
docker安装两种
1.脚本
```shell
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun
```
2.手动配置
Centos/Openanolis/OpenCloudOS适用以下代码
```shell
yum install docker-ce -y
(#代表下面适用于检测不到软件包使用)
#yum install -y yum-utils device-mapper-persistent-data lvm2
#yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
#sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
#yum makecache
#yum install docker-ce -y
```
Debian 和 Ubuntu适用

```shell
apt update
apt upgrade -y
apt install curl vim wget gnupg dpkg apt-transport-https lsb-release ca-certificates
curl -sS
https://download.docker.com/linux/debian/gpg | gpg --dearmor > /usr/share/keyrings/docker-ce.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-ce.gpg] https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/debian $(lsb_release -sc) stable" > /etc/apt/sources.list.d/docker.list
apt update
apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
上述安装完毕后，执行下方代码
```shell
status status docker//检测是否存在docker
status start docker//存在则启动docker服务
status enable docker//开机自启
```
------------我的配置好的安装方式------------
yunzai-bot资源下载链接:https://caiyun.139.com/m/i?135Ce8H2tpZTS
提取码:qHeX
下载完我配置好的压缩包,然后上传(建议宝塔云控)
```other
cd /(建议装主目录宝塔管理轻松)
wget (获取云盘下载链接粘贴在这里)
```

解压
```other
unzip yunzai-bot.zip
```

再执行下载容器并配置容器
```other
cd /yunzai-bot && docker-compose up -d && docker exec -it yunzai-bot node app login
```
配置完成,如果出现登录异常可看官方文档进行修改
------------手动安装方式------------
1.执行辅助脚本
```shell
cd / && bash <(curl -sSL http://yunzai.org/install_v3)
```
2.脚本执行完后,不要先启动容器
3.配置yunzai-bot插件后(cd /yunzai-bot/yunzai/plugins)
```
cd /yunzai-bot/yunzai (大型插件可在这里clone)
cd ./plugins/example (js插件)
```
三个js报错可复制以下内容到js中
一言.js
```other
import plugin from '../../lib/plugins/plugin.js'
import fetch from 'node-fetch'

export class example extends plugin {
  constructor () {
    super({
      /** 功能名称 */
      name: '一言',
      /** 功能描述 */
      dsc: '简单开发示例',
      /** https://oicqjs.github.io/oicq/#events */
      event: 'message',
      /** 优先级，数字越小等级越高 */
      priority: 5000,
      rule: [
        {
          /** 命令正则匹配 */
          reg: '^#一言$',
          /** 执行方法 */
          fnc: 'hitokoto'
        }
      ]
    })
  }

  /**
   * #一言
   * @param e oicq传递的事件参数e
   */
  async hitokoto (e) {
    /** e.msg 用户的命令消息 */
    logger.info('[用户命令]', e.msg)

    /** 一言接口地址 */
    let url = 'https://v1.hitokoto.cn/'
    /** 调用接口获取数据 */
    let res = await fetch(url).catch((err) => logger.error(err))

    /** 判断接口是否请求成功 */
    if (!res) {
      logger.error('[一言] 接口请求失败')
      return await this.reply('一言接口请求失败')
    }

    /** 接口结果，json字符串转对象 */
    res = await res.json()
    /** 输入日志 */
    logger.info(`[接口结果] 一言：${res.hitokoto}`)

    /** 最后回复消息 */
    await this.reply(`一言：${res.hitokoto}`)
  }
}
```
主动复读.js
```other
import plugin from '../../lib/plugins/plugin.js'

export class example2 extends plugin {
  constructor () {
    super({
      name: '复读',
      dsc: '复读用户发送的内容，然后撤回',
      /** https://oicqjs.github.io/oicq/#events */
      event: 'message',
      priority: 5000,
      rule: [
        {
          /** 命令正则匹配 */
          reg: '^#复读$',
          /** 执行方法 */
          fnc: 'repeat'
        }
      ]
    })
  }

  /** 复读 */
  async repeat () {
    /** 设置上下文，后续接收到内容会执行doRep方法 */
    this.setContext('doRep')
    /** 回复 */
    await this.reply('请发送要复读的内容', false, { at: true })
  }

  /** 接受内容 */
  doRep () {
    /** 复读内容 */
    this.reply(this.e.message, false, { recallMsg: 5 })
    /** 结束上下文 */
    this.finish('doRep')
  }
}
```
进群退群通知.js
```other
import plugin from '../../lib/plugins/plugin.js'
import { segment } from 'oicq'
export class newcomer extends plugin {
  constructor () {
    super({
      name: '欢迎新人',
      dsc: '新人入群欢迎',
      /** https://oicqjs.github.io/oicq/#events */
      event: 'notice.group.increase',
      priority: 5000
    })
  }

  /** 接受到消息都会执行一次 */
  async accept () {
    /** 定义入群欢迎内容 */
    let msg = '欢迎新人！'
    /** 冷却cd 30s */
    let cd = 30

    if (this.e.user_id == Bot.uin) return

    /** cd */
    let key = `Yz:newcomers:${this.e.group_id}`
    if (await redis.get(key)) return
    redis.set(key, '1', { EX: cd })

    /** 回复 */
    await this.reply([
      segment.at(this.e.user_id),
      // segment.image(),
      msg
    ])
  }
}

export class outNotice extends plugin {
  constructor () {
    super({
      name: '退群通知',
      dsc: 'xx退群了',
      event: 'notice.group.decrease'
    })

    /** 退群提示词 */
    this.tips = '退群了'
  }

  async accept () {
    if (this.e.user_id == Bot.uin) return

    let name, msg
    if (this.e.member) {
      name = this.e.member.card || this.e.member.nickname
    }

    if (name) {
      msg = `${name}(${this.e.user_id}) ${this.tips}`
    } else {
      msg = `${this.e.user_id} ${this.tips}`
    }
    logger.mark(`[退出通知]${this.e.logText} ${msg}`)
    await this.reply(msg)
  }
}
```
clone完大型插件或者配置好损坏的三个js后执行以下代码
```shell
cd /yunzai-bot && vim docker-compose.yaml
```
docker-compose.yaml文件配置(看你有啥插件就咋配置)
```other
version: "3.9"
services:
  yunzai-bot:
    container_name: yunzai-bot
    image: swr.cn-south-1.myhuaweicloud.com/sirly/yunzai-bot:v3plus
    restart: always
    volumes:
      - ./yunzai/config:/app/Yunzai-Bot/config/config/ # 配置文件
      - ./yunzai/genshin_config:/app/Yunzai-Bot/plugins/genshin/config # 配置文件
      - ./yunzai/logs:/app/Yunzai-Bot/logs # 日志文件
      - ./yunzai/data:/app/Yunzai-Bot/data # 数据文件
      - ./yunzai/plugins/example:/app/Yunzai-Bot/plugins/example # js 插件
      # 以下目录是插件目录，安装完插件后需要手动添加映射
      - ./yunzai/plugins/miao-plugin:/app/Yunzai-Bot/plugins/miao-plugin                  # 喵喵插件
      - ./yunzai/plugins/py-plugin:/app/Yunzai-Bot/plugins/py-plugin                      # 新py插件
      - ./yunzai/plugins/xiaoyao-cvs-plugin:/app/Yunzai-Bot/plugins/xiaoyao-cvs-plugin    # 图鉴插件
      - ./yunzai/plugins/guoba-plugin:/app/Yunzai-Bot/plugins/guoba-plugin                # 锅巴插件
      - ./yunzai/plugins/TRSS-Plugin:/app/Yunzai-Bot/plugins/TRSS-Plugin
      - ./yunzai/plugins/xianxin-plugin:/app/Yunzai-Bot/plugins/xianxin-plugin
      - ./yunzai/plugins/yenai-plugin:/app/Yunzai-Bot/plugins/yenai-plugin
    ports:
      - 50831:50831#锅巴插件映射端口
      
    depends_on:
      redis: { condition: service_healthy }

  redis:
    container_name: yunzai-redis
    image: redis:alpine
    restart: always
    volumes:
      - ./redis/data:/data
      - ./redis/logs:/logs
    healthcheck:
      test: ["CMD", "redis-cli", "PING"]
      start_period: 10s
      interval: 5s
      timeout: 1s
```
配置完后即可使用以下指令
```other
cd /yunzai-bot && docker-compose up -d && docker exec -it yunzai-bot node app login
```
然后如果机器人私聊你消息,则配置成功
每次上传完插件,需修改docker-compose.yaml
并执行以下命令
```other
cd /yunzai-bot && docker-compose up -d
```
