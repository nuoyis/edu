import os

# os.getcwd()函数和用于查看程序当前工作目录
# os.chdir(path)函数用于更改程序的当前工作目录
# print(os.getcwd())
# print(os.chdir(".."))
# print(os.getcwd())
# print(os.chdir("C:\\Program Files\\MySQL"))
# print(os.getcwd())

# os.listdir(path)函数:用于以列表的方式返回目录path下的所有目录和文件，当path为空时返回当前目录下的文件和目录
# fileDirs = os.listdir()
# for item in fileDirs:
#     if os.path.isdir(item):
#         print("文件:", item)
#     else:
#         print("目录:", item)
#
# print(os.listdir("C:\\Program Files\\MySQL"))
# os.chdir("F:\\python-project")
# print(os.listdir())


# os.mkdir(path,mode=0o777)函数:创建单目录，不递归，父目录不在会报错
# os.mkdir()函数用于创建目录path,类似与Linux中的mkdir命令，其中mode为目录权限的数字模式，为可选参数
# os.chdir("F:\\python-project\\3-os和sys模块")
# os.mkdir("2023yun1", 777)
# os.mkdir("2023\\yun1\\tiansheng", 777)
# print(os.listdir())

# os.makedirs(path,mode=0o777,exist_ok=False)函数：创建多级目录
# os.mkdi()函数只能在当前工作目录创建目录，如果需要递归创建目录就需要用到os.makedirs函数
# os.makedirs("2023\\yun1\\tiansheng")
print(os.listdir())
os.chdir("2023")
print(os.listdir())

os.listdir("C:\\Users\\wkkjo\\Documents\\GitHub\\edu\\Class\\classroom\\python\\日期记录\\2024-04-03")
os.rmdir("2023\\")

os.removedirs("2023\\yun1\\tiansheng")