import glob
import os

print(os.path.split("sys_modle.py"))

print(os.path.split("/User/hqs/Python3/yun1-project"))

print(os.path.split("C:\\Users\\wkkjo\\Desktop\\寝室卫生执勤表.xlsx"))

# os.path.splitext(path)函数是将path切割成路径和文件扩展名，同样是以元组的形式返回
print(os.path.splitext("sys_modle.py"))

print(os.path.splitext("/User/hqs/Python3/yun1-project"))

print(os.path.splitext("C:\\Users\\wkkjo\\Desktop\\寝室卫生执勤表.xlsx"))

# os.path.dirname():获取当前路径名
print(os.path.dirname("/home/yun1/zz"))
print(os.path.dirname(""))

print(glob.glob("*.py"))
print(glob.glob("test/*.txt"))
print(glob.glob("F:\\python-project\\1-面向对象\\*.py"))

print(glob.iglob(r"[a-z0-9]*.txt"))
for item in glob.iglob(r"[a-z0-9]*.py"):
    print(item)