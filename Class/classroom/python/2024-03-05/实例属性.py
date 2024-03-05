# class YUn1Stu:
#     school = "湖北科技职业学院"
#     class_name = "1班"
#
#     def learn(self):
#         self.content = "python"
#         print("学习", self.content)
#
#
# ch = YUn1Stu()
# ch.learn()
# print(ch.content)
# ch.content = "Java"
# print(ch.content)
# ch.learn()
# print(ch.content)

# class Person:
#     def __init__(self, name):
#         self.name = name
#         self._age = 1
#
#     def set_age(self, new_age):
#         if 0 < new_age <= 120:
#             self._age = new_age
#
#     def get_age(self):
#         return self._age
#
#
# person = Person("小名")
# person.set_age(20)
# print("年龄为:"+str(person.get_age())+"岁")

# class MyClass:
#     def instance_method(self, name, other_args):
#         print(name, other_args)
#
#
# obj1 = MyClass()
# obj1.instance_method("name", "Hallo Python")

# class MyClass:
#     class_attr = "Initial Value"
#
#     @classmethod
#     def class_method_to_modify_attr(cls, new_value):
#         cls.class_attr = new_value
#
#     @classmethod
#     def class_method_to_print_attr(cls):
#         print(cls.class_attr)
#
#
# MyClass.class_method_to_modify_attr("KFC")
#
# MyClass.class_method_to_print_attr()

# obj2 = MyClass
# obj2.class_method_to_print_attr()
# obj2.class_method_to_modify_attr("麦当劳")
# obj2.class_method_to_print_attr()

# class MyClass3:
#
#     @staticmethod
#     def static_method(arg1, arg2):
#         print(arg1, arg2)
#
# MyClass3.static_method("hallo world", "python3")
# obj3 = MyClass3()
# obj3.static_method("Uzi", "male")

class Myclass3:
    class_attr = "类的属性"

    def instance_method(self):
        print("实例方法调用")

    @staticmethod
    def static_method():

        print("Myclass3.class_attr")
        obj3 = Myclass3()
        obj3.instance_method()

Myclass3.static_method()