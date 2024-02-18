# -*- coding: utf-8 -*-
# 原作者:https://github.com/zhourongyu/Typecho2Hexo
# 新数据库借鉴作者:https://www.jianshu.com/p/4e72faebd27f
import os
import re
import pymysql
import arrow
from flask import Flask
import urllib
import codecs
import traceback

host = input("请输入数据库地址:")
port = input("请输入数据库端口(回车即默认3306):")
db = input("请输入数据库名称:")
user = input("请输入数据库用户名称:")
password = input("请输入数据库用户密码:")
qianzhui = input("请输入表前缀(默认为typecho_,可直接回车):")

if port == "":
    port = 3306
elif qianzhui == "":
    qianzhui = "typecho_"

port = int(port)

if host == "" or db == "" or host == "" or password == "":
    print("你的参数未输入完毕，请重新启动程序输入")
    input("按任意键继续")
    exit(1)

print("操作正在处理中，稍安勿躁~")

def main():

    try:
        conn = pymysql.connect(host=host, port=port, db=db, user=user, password=password)
    except Exception as e:
        print("检测发生错误，请重新检查:\n"
              "1.数据库用户密码等内容输入是否正确\n"
              "2.是否打开数据库端口\n"
              "请重新启动程序输入\n"
              "错误日志:"+str(e))
        input("按任意键继续")
        exit(1)

    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 创建分类和标签
        cursor.execute("select type, slug, name from "+qianzhui+"metas")
        for cate in cursor.fetchall():
            path = 'data/分类/%s' % urllib.parse.unquote(cate['slug'])
            if not os.path.exists(path):
                os.makedirs(path)
            f = codecs.open('%s/index.md' % path, 'w', "utf-8")
            f.write("title: %s\n" % urllib.parse.unquote(cate['slug']))
            f.write("date: %s\n" % arrow.now().format('YYYY-MM-DD HH:mm:ss'))
            # 区分分类和标签
            if cate['type'] == 'category':
                f.write('type: "categories"\n')
            elif cate['type'] == 'tags':
                f.write('type: "tags"\n')
            # 禁止评论
            f.write("comments: false\n")
            f.write("---\n")
            f.close()

        # 创建文章
        cursor.execute("select cid, title, slug, text, created from "+qianzhui+"contents where type='post'")
        for e in cursor.fetchall():
            title = re.sub('[\\/:*?"<>|]','-',e['title'].encode('raw_unicode_escape').decode("unicode-escape"))
            content = str(e['text'].replace('<!--markdown-->', ''))
            tags = []
            category = ""
            # 找出文章的tag及category
            cursor.execute(
                "select type, name, slug from `"+qianzhui+"relationships` ts, "+qianzhui+"metas tm where tm.mid = ts.mid and ts.cid = %s",
            e['cid'])
            for m in cursor.fetchall():
                if m['type'] == 'tag':
                    tags.append(m['name'])
                if m['type'] == 'category':
                    category = urllib.parse.unquote(m['slug'])
            path = 'data/文章/'
            if not os.path.exists(path):
                os.makedirs(path)
            f = codecs.open('%s%s.md' % (path, title), 'w', "utf-8")
            f.write("---\n")
            f.write("title: %s\n" % title)
            f.write("date: %s\n" % arrow.get(e['created']).format('YYYY-MM-DD HH:mm:ss'))
            f.write("categories: %s\n" % category)
            f.write("tags: [%s]\n" % ','.join(tags))
            f.write("---\n")
            f.write(content)
            f.close()
        conn.close()
        print("操作完毕，请检查同目录下生成的文件")
    except Exception as e:
        print("发生错误，请重新检查数据库内是否有正确的表项，请重新启动程序运行\n"
              "错误日志:"+str(e))
        exit(1)

if __name__ == "__main__":
    main()
    input("请按任意键继续")