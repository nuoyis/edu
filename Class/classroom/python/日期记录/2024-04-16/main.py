import os, sys, time


def store_file_dir_info(path):
    storeFileName = "example1.txt"  # 用来存储信息的文件名
    # 假设目录中有很多文件和目录，用列表保存
    fileList = []
    dirList = []
    otherList = []

    # 更改当前的目录
    os.chdir(path)
    # 打开文件
    f = os.open(storeFileName, os.O_WRONLY | os.O_CREAT)
    # 写入表头信息
    os.write(f, str.encode("名称 类型 绝对路径 创建时间 文件大小\n"))
    # 遍历当前路径下的文件和目录
    for item in os.listdir('.'):
        if os.path.isfile(item):
            # abspath:返回路径path的绝对路径;getctime:返回文件的创建时间;getsize:获取文件的大小，单位为字节，除以1024后转为KB
            string = "%s 文件 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024)
            dirList.append(string)
        elif os.path.isdir(item):  # 当是目录时
            string = "%s 目录 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024)
        else:  # 其他文件
            string = "%s 其他 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024)
            otherList.append(string)
    # 依次以目录、文件、其他文件的顺序写入信息
    for dir in dirList:
        os.write(f, str.encode(dir))
    for file in fileList:
        os.write(f, str.encode(file))
    for other in otherList:
        os.write(f, str.encode(other))
    os.close(f)  # 关闭文件


if __name__ == '__main__':
    store_file_dir_info("./")
