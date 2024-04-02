# 切换目录 os.chdir()
# os.chdir("E:\python-project\3-os和sys模块")
import os

os.chdir(os.path.join(os.getcwd(), 'test'))
print("切换后的当前目录:", os.getcwd())

# os.path.normpath(path)函数:用于将不规范的路径分割符转换成规范的形式（不太实用)
print(os.path.normpath("C:\\Users/1//test.txt"))
print(os.path.normpath("E:\\python-project\\3-os和sys模块\2023yun1/名册.xls"))
