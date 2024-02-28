# class 类名:
#     属性名 = 属性值
#
#     def __init__(self):
#         self.对象属性1 = 参数1
#         self.对象的属性2 = 参数2
#
#     def 方法名(self):pass
#
#     def 方法名2(self):pass

class student:
    country = "China"

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex

    def print_info(self):
        info = """
        国籍: %s
        姓名: %s
        年龄: %s
        性别: %s
        """% (self.country, self.name, self.age, self.sex)

cl = student("程龙", "19", "男")
yg = student("严格", "19", "女")

cl.print_info()
yg.print_info()