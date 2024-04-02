import os
dir_path = './test'
if not os.path.isdir(dir_path):
    os.makedirs(dir_path)
    print(f"已经创建目录:{os.path.abspath(dir_path)}")
else:
    print(f"已存在目录:{os.path.abspath(dir_path)} {os.path.join(os.getcwd(), dir_path.split('/')[1])}")

if not os.path.isfile(os.path.join(os.getcwd(), dir_path.split('/')[1], "test.txt")):
    f = open(os.path.join(os.getcwd(), dir_path.split('/')[1], "test.txt"), mode='w+', encoding='utf-8')
    f.write("立德树人、笃学尚行")
else:
    f = open(os.path.join(os.getcwd(), dir_path.split('/')[1], "test.txt"), mode='r', encoding='utf-8')
    print(f.read()+f"{os.path.getsize(os.path.join(os.getcwd(), dir_path.split('/')[1], 'test.txt'))}")
f.close()


