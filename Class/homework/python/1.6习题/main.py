import os
import turtle as t

'''
Author:徐惟康
update:2023-09-26

1.6 习题 
一、填空题
1．Python是面向对象的高级语言。
2．Python可以在多种平台运行，这体现了Python语言可移植的特性。
3. Python模块的本质是.py结尾的Python文件。
4．使用语句可以在当前程序中导入模块。
5．使用from...import语句可以将指定模块中的全部内容导入当前程序。

二、判断题
1．相比C＋＋程序，Python程序的代码更加简洁、语法更加优美，但效率较低。(x)
2. "from...import*" 语句与"import模块名"语句都能导入指定模块的全部内容，相比之下,from...import*导入的内容无需指定模块名,可直接调用，使用更加方便，因此更推荐在程序中通过这种方式导入指定模块的全部内容。（x）
3. Python 3.x版本完全兼容 Python 2.x。(x)
4．PyCharm是Python的集成开发环境。(v)
5．模块文件的后缀名必定是.py。(v)

三、选择题
1．下列选项中，不是Python语言特点的是（C）。
A.简洁
B.开源
C.面向过程
D.可移植性

2．下列哪个不是Python的应用领域？(D)
A.Web开发
B.科学计算
C.游戏开发
D.操作系统管理

3．下列关于Python的说法中，错误的是(D)。
A.Python是从ABC语言发展起来的。
B.Python是一门高级计算机语言。
C.Python 只能编写面向对象的程序
D.Python程序的效率比C程序的效率低

四、简答题。
1．简述Python的特点。
易学易用(简洁) 开源 跨平台 面向对象 可移植性
2．简单介绍如何导入与使用模块。
import 模块名
3．简述Python 中模块、包和库的意义。
模块:单个文件或者包含函数，类，变量和语句
包:一个包含多个模块的目录
库:一组模块和包
'''

def zhengshu():
    n = int(input("请输入一个整数:"))
    sum=0;
    for i in range(n+1):
        sum+=i;
    print("1~%d的求和结果为%d"%(n,sum))

def paixu():
    l = []
    for i in range(3):
        x = int (input('请输入整数:'))
        l.append(x)
    l.sort()
    print(l)

def jiujiu():
    for i in range(1,10):
        for j in range(1,i+1):
            print("%dx%d=%-2d"%(j,i,i*j),end = ' ')
        print('')

def wujiaoxing( leng ):
    count = 1
    while count <= 5:
        t.forward(leng)
        t.right(144)
        count += 1
    leng += 10
    if leng <= 100:
        wujiaoxing (leng)

def printf():
    x = input('请输人姓名:')
    y = input('请输人年龄:')
    z = input('请输人工作:')
    v = input('请输人爱好:')
    print("------------ info of Egon -----------\n"
    "Name: "+x+"\n"
    "Age: "+y+"\n"
    "Sex: "+z+"\n"
    "Job: "+v+"\n"
    "------------- end - ----------------")

def main():
    zhengshu()
    paixu()
    jiujiu()
    t.penup()
    t.backward(100)
    t.pendown()
    t.pensize(2)
    t.pencolor('red')
    segment = 50
    wujiaoxing (segment)
    t.exitonclick()
    printf()


if __name__ == '__main__':
    main()