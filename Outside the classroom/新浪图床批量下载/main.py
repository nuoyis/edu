import os
import requests

j = 0
path = os.getcwd() + '\\pictures'
# https: // blog.csdn.net / zzddada / article / details / 102786354
# 去除首位空格
path = path.strip()
# 去除尾部 \ 符号
path = path.rstrip("\\")
# 判断路径是否存在
# 存在     True
# 不存在   False
isExists = os.path.exists(path)
# 判断结果
if not isExists:
    os.makedirs(path)
with open(os.getcwd() + "\\ACG.txt", "r",encoding='utf-8') as f:
    for i in f.read().splitlines():
        Download_addres = 'https://i0.wp.com/tva4.sinaimg.cn/large/' + i + '.jpg'
        print(Download_addres)
        # r = requests.get(Download_addres)
        # with open(str(j)+".ipg", "wb") as code:
        #     code.write(r.content)
        j += 1