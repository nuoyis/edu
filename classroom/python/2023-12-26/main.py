# f = open(file="test.txt" , mode="w+", encoding="utf-8")
# print(f, type(f))
# f.write("wwwww")
# data = f.read()
# f.close()
# print(data)
#
# f = open(file="test.txt" , mode="a", encoding="utf-8")
# f.write("wwwww")
# f.close()
#
# f = open(file="E:\\python\\2023-12-26\\test.txt" , mode="r", encoding="utf-8")
# print(f, type(f))
# data = f.read()
# f.close()
# print(data)
#
# #seek 0:开头 1：当前位置 2.文件位置
# f = open(file="test.txt" , mode="a+", encoding="utf-8")
# f.write("wwwww")
# f.seek(0,0)
# data2 = f.read()
# print(data2)

with open(file="test.txt" , mode="r", encoding="utf-8") as f:
    li = f.readlines()
    li2 = []
    for i in li:
        li2.append(i.split(" ")[0])
    print(li2)