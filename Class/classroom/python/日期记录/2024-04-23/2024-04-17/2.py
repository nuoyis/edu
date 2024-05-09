"""
上一个例子的一个衍生版本，其主要功能有：
（1）利用上一个例子中的方法获取并显示指定路径下所有的文件信息和目录信息；
（2）通过OS模块的os.open()函数和os.mkdir()函数创建文件和目录；
（3）通过OS模块的os.remove()函数删除文件和shutil模块的shutil.rmtree()函数删除目录；
（4）通过OS模块的os.rename()函数重命名文件和目录；
（5）通过OS模块的os.rename()函数移动文件和目录。
"""
import os
import sys
import time

filelist = []
dirlist = []
otherlist = []


def get_file_dir_info(path):
    # 获取path路径下的所有文件和目录信息
    for item in os.listdir(os.path.abspath(path)):
        if os.path.isfile(item):  # 判断是文件
            filelist.append(item)
        elif os.path.isdir(item):  # 判断是否目录
            dirlist.append(item)
        else:
            otherlist.append(item)


def print_file_dir_info(path):
    # 打印path路径下所有文件和目录的信息
    print("路径 %s 下的所有文件和目录信息: \n 名称 类型 绝对路径 创建时间 文件大小\n" % os.path.abspath(path))
    for item in dirlist:
        print("%s 目录 %s %s %.2fKB \n" % (
            item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024))
    for item in filelist:
        print("%s 文件 %s %s %.2fKB \n" % (
            item, os.path.abspath(item), time.ctime(os.path.getctime(item)), os.path.getsize(item) / 1024))
    for item in otherlist:
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
    abs_path = os.path.abspath(path)  # 统一转化为绝对路径
    name = os.path.basename(abs_path)  # 返回路径path中的文件名
    # 删除文件或目录
    try:
        if name in dirlist:
            dirlist.remove(name)
            os.removedirs(path)
            return True
        elif name in otherlist:
            otherlist.remove(name)
            os.remove(path)
            return True
        else:
            print("找不到对应的文件和目录")
            return False
    except Exception as e:
        print(e)
        return False


def rename_file_dir(path, new_path):
    """
    重命名或移动文件或目录
    :param path: 源路径
    :param new_path: 新路径
    :return:
    """
    try:
        os.rename(path, new_path)
        return True
    except Exception as e:
        return False


def clear_list():
    # 清空文件、目录、其他文件
    filelist.clear()
    dirlist.clear()
    otherlist.clear()


def menu(path):
    # 菜单函数，调用相关函数执行操作
    clear_list()

    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        os.system("clear")
    get_file_dir_info(path)  # 获取路径下文件目录信息
    print_file_dir_info(path)  # 打印路径下信息

    tips = """
    ******* 请输入要进行的操作编号 *******
    1.创建文件或目录
    2.删除文件或目录
    3.重命名文件或目录
    4.移动文件或目录
    5.重新输入路径
    6.退出
    """
    operation = input(tips)
    if operation == '1':
        tip1 = """
        请选择创建类型：
        1.文件
        2.目录
        """
        flietype = input(tip1)
        if flietype == '1':
            filename = input("请输入创建文件的文件名：")
            if create_file_dir(filename, "file"):
                print("创建文件 %s 成功！！" % filename)
            else:
                print("创建文件 %s 失败！！" % filename)

        elif flietype == '2':
            dirname = input("请输入要创建目录的名称：")
            if create_file_dir(dirname, "dir"):
                print("创建文件 %s 成功！！" % dirname)
            else:
                print("创建文件 %s 失败！！" % dirname)

    elif operation == '2':
        delete_path = input('请输入要删除的文件名或目录名：')
        if delete_path in filelist or dirlist or otherlist:
            if delete_file_dir(delete_path):
                print("删除成功！！")
            else:
                print('删除失败!!')
        elif not os.path.exists(delete_path):
            print("文件或目录 %s 不存在" % delete_path)

    elif operation == '3':
        kepy_file = input("请输入要修改的文件名或目录名")
        if kepy_file in filelist or dirlist or otherlist:
            rename_file = input("请输入新文件名或目录名")
            print(os.path.abspath(kepy_file), os.path.abspath(rename_file))
            if rename_file_dir(os.path.abspath(kepy_file), os.path.abspath(rename_file)):
                print("修改成功！！")
            else:
                print("修改失败！！")
        elif not os.path.exists(kepy_file):
            print("文件或目录 %s 不存在" % kepy_file)

    elif operation == '4':
        rename_obc = input("请输入要移动的文件名或目录名:")
        if rename_obc in filelist or dirlist or otherlist:
            rename_file = input("请输入新目录名")
            print(os.path.abspath(rename_obc), os.path.abspath(rename_file+'/'+rename_obc))
            if rename_file_dir(os.path.abspath(rename_obc), os.path.abspath(rename_file+'/'+rename_obc)):
                print("移动成功！！")
            else:
                print("移动失败！！")
        elif not os.path.exists(rename_obc):
            print("文件或目录 %s 不存在" % rename_obc)

    elif operation == '5':
        try:
            new_path = input("请输入新路径：")
            if os.path.isabs(path):
                path = os.path.normpath(new_path)
            else:
                input("路径不正确，按任意键返回主菜单！！")
        except Exception as e:
            print(e)
            input("路径不正确，按任意键返回主菜单！！")
    elif operation == '6':
        return False  # 退出，结束程序
    else:
        print("输入错误，请重新选择！！")

    input('按任意键返回主菜单！！')
    return True


if __name__ == '__main__':
    # get_file_dir_info('.')
    # print_file_info('.')
    # # create_file_dir("yun1","dir")
    # delete_file_dir('./yun1')
    # print(filelist)
    # print(dirlist)
    # print(otherlist)
    #
    # try:
    #     path = input('请输入路径:')
    #     if os.path.isabs(path):
    #         path = os.path.abspath(path)
    #         print(path)
    #     else:
    #         path = os.path.abspath(path)
    #         print(path)
    # except Exception as e:
    #     print(e)
    #     sys.exit(0)
    try:
        path = input("请输入路径：")
        if os.path.isabs(path):
            path = os.path.normpath(path)
            print(path)
        else:
            path = os.path.abspath(path)
            print(path)
    except Exception as e:
        print(e)
        sys.exit(0)  # 结束程序

    while True:
        if not menu(path):
            break
    print("程序运行结束")
