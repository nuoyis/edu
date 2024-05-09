import os, sys, time

fileList = []
dirList = []
otherList = []

def get_file_dir_info(path):
    # 获取path路径下的所有文件和目录信息
    for item in os.listdir(os.path.abspath(path)):
        if os.path.isdir(item):
            fileList.append(item)
        elif os.path.isfile(item):
            fileList.append(item)
        else:
            otherList.append(item)

def print_file_info(path):
    # 打印path路径下所有文件和目录的信息
    print("路径 %s 下的所有文件和目录信息: \n 名称 类型 绝对路径 创建时间 文件大小\n" % os.path.abspath(path))
    for item in dirList:
        print("%s 目录 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024))
    for item in fileList:
        print("%s 文件 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024))
    for item in otherList:
        print("%s 其他 %s %s %.2fKB \n" % (
                item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024))


def create_file_dir(name, type):
    # 创建文件或目录 type分类为:file dir
    if type == 'file':
        try:
            f = os.open(name, os.O_CREAT)
            os.close(f)
            return True
        except Exception as e:
            print(e)
            return False
    elif type == 'dir':
        try:
            # 在当前路径创建文件
            os.mkdir(name)
            return True
        except Exception as e:
            print("请选择正确的文件/目录类型")
            return False
    else:
        print("请选择正确的文件")
        return False


def delete_file_dir(path):
    abs_path = os.path.abspath(path)
    name = os.path.basename(abs_path)
    # 删除文件或目录
    try:
        if name in dirList:
            dirList.remove(name)
            os.removedirs(path)
            return True
        elif name in otherList:
            otherList.remove(name)
            os.remove(path)
            return True

def rename_file_dir(path, new_path):
    """
    重命名或移动文件或目录
    :param path: 源路径
    :param new_path: 新路径
    :return:
    """
    pass


def clear_list():
    # 清空文件、目录、其他文件
    pass


def menu(path):
    # 菜单函数，调用相关函数执行操作
    pass
