import os
import re

path = input("请输入目录(windows需要G:\\开头文件):")
oldurl = input("请输入旧图床链接(仅需前缀):")
newurl = input("请输入新图床链接(仅需前缀):")
files= os.listdir(path) #得到文件夹下的所有文件名称
newfile = path+'\\new'
os.makedirs(newfile)
for file in files: #遍历文件夹
    a = ""
    position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
    print("正在读取: "+position)
    with open(position, "r",encoding='utf-8') as f:    #打开文件
        for ss in f.readlines():
            a += re.sub(oldurl, newurl, ss)
    with open(newfile+'\\'+ file, "w",encoding='utf-8') as f:
        f.write(a)
    print(position + " 替换完毕")