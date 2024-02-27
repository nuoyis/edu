from PIL import Image  # Pillow                    9.0.0
import pillow_avif  # pillow-avif-plugin        1.2.2
import os

# 以上只是其中一个可用版本，并非必须
# 必须先安装pip install pillow-avif-plugin才能使用
# https://blog.csdn.net/vioshine/article/details/125949655
i = 0
path = input("请输入地址，我们将在你的地址进行转换:")
filelist = os.listdir(path)
newfilelist = os.path.join(path, 'new')
if not os.path.exists(newfilelist):
    os.makedirs(newfilelist)
for file in filelist:
    i = i + 1
    print('\r正在执行:' + os.path.join(path, file) + "\n已执行:" + str(i) + "个", end='')
    JPGfilename = os.path.join(path, file)
    if os.path.isdir(JPGfilename):  # 如果是文件夹则跳过
        continue
    JPGimg = Image.open(JPGfilename)
    JPGimg.save(os.path.join(newfilelist, file.replace("jpg", 'avif')), 'AVIF')
