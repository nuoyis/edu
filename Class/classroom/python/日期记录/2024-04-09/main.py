# 创建一个新目录  D:\2023yun1\名字首字母
# 切换新目录为当前路径
# 创建文件 test.py
# 打印当前路径信息，打印目录下所有文件
# 删除新文件和新目录
# 力扣
# cnblogs.com/xiugeng
import os

dir = "D:\\2023yun1\\名字首字母"

if not os.path.exists(dir):
    os.makedirs(dir)
os.chdir(dir)
if not os.path.exists(os.path.join(dir, 'test.py')):
    # f = os.open(filename, os.O_RDWR | os.O_CREAT)
    # os.write(f, str.encode("we are hbkj 2023 yun1!!!"))
    # os.close(f)
    with open(os.path.join(dir, 'test.py'), 'w') as f:
        f.write('test')
print(os.getcwd())
fileDirs = os.listdir(dir)
for item in fileDirs:
    if os.path.isfile(item):
        print("文件:", item)
os.remove(os.path.join(dir, 'test.py'))
os.removedirs(dir)
