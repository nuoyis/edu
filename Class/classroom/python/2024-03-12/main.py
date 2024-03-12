#构造方法

#无参构造
#没有参数的构造方法，常用于给对象设置默认值

class Dog:
    def __init__(self):
        self.name = 'kog'
        print('无参构造方法被默认调用')

#无参构造方法创建对象
dog1 = Dog()
print(dog1.name)

# 有参构造
# 构造方法中定义参数，常用于创建对象时给对象初始化属性
# class Stu():
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         print("有参构造方法被调用，创建了名为{name}，年龄为{age}的人".format(name=self.name, age=self.age))
#
# # 有参构造方法创建对象
# stu1 = Stu("陈昱菲", 19)
# stu2 = Stu("陈欣怡", 20)
#
# # 练习:mysqL远程连接处理,定义属性:host port db charset字符集
# #                     定义方法:conn连接数据库,execute执行数据库
# class MySQLHandler:
#     def __init__(self, host, post, db, charset="utf-8"):
#         self.host = host
#         self.post = post
#         self.db = db
#         self.conn = connect(host, post, db, charset)
#
#
#     def execute1(self, sql):
#         return self.conn.execult(sql)
#
#     def execute2(self, sql):
#         return self.conn.execult(sql)

# import time
# # 结构方法
# class Myclass:
#     def __init__(self, name):
#         self.name = name
#         print(f"对象{name}创建")
#
#     def __del__(self):
#         print(f"对象{self.name}销毁")
#
# # 创建一个对象
# obj = Myclass("text")
#
# print("111111")
# time.sleep(3)
# #删除对象，使其可以垃圾回收
# del obj
# time.sleep(3)
# print("222222")

class ParentClass:
    pass
class ParentClass2():
    pass

class SubClass1(ParentClass):
    pass

class SubClass2(ParentClass, ParentClass2):
    pass

class School_Member:
    def __init__(self, name, sex, age):
        self.name = name
        self.sex = sex
        self.age = age
    def describe(self):
        print(f"""我是一个学校成员，\n
              我的名字是{self.name}，\n
              我的性别是{self.sex}，\n
              我的年龄是{self.name}""")
sm1 = School_Member('yg', "female", 19)
sm1.describe()

class Teacher(School_Member):
    def __init__(self, name, sex, age, salary):
        # 显示调用，复用代码
        School_Member.__init__(self, name, sex, age)
        self.salary = salary
    def describe(self):
        School_Member.describe(self)
        print(f"我的薪水是{self.salary}")
#创建对象
tc1 = Teacher('wjf', "male", 20, 8000)
tc1.describe()

print(ParentClass.__bases__, type(ParentClass.__bases__))
print(ParentClass2.__bases__, type(ParentClass2.__bases__))