# 错误:
# 1.语法错误:代码不符合python语法
# print("asd")
# print("asda)
# 12 ==== 14

#2.逻辑错误: 代码执行结果和预期不符。
# if 1 < 3:
#     print("1比3大")
#
# ts = {"name": "田盛", "birth_year": 2001}
# ly = {"name": "刘阳", "birth_year": 2003}
#
# if ts['birth_year'] > ly['birth_year']:
#     print("田盛年龄大")
# else:
#     print("刘阳年龄大")
# 异常(Execption):在编程中程序运行时发生的不正当或意外强开。当程序遇到无法处理的错误或预定义条件不满足时，会抛出异常对象表示这种情况。
try:
    7/0
except Exception as e:
    print(e)

s1 = input("请输入你的年龄")
try:
    int(s1)
except Exception as e:
    s2 = ""
    for i in s1:
        if i.isdigit():
            print(i)
            s2 += i
    print("你输入的数字有问题，输入值为:",s1)
    print("过滤字符串得到:", s2)
    print("过滤得到我的年龄是:", int(s2))
else:
    print("我的年龄是:",s1)
finally:
    print(s1)

