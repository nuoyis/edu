import sys
print(sys.argv)
li = []

for i in sys.argv:
    print(i)
    if len(i) >= 5:
        li.append(i)
print(li)


# sys.exit("执行失败，退出程序!")
# print("检查程序退出！！") 代码不可达

if len(li) >= 3:
    print("列表收集成功，达到3个以上。")
    exit(0)
else:
    try:
        exit("列表收集不足")
    except SystemExit as e:
        print(e)

