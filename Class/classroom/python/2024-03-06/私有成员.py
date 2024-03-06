# class Car:
#     __wheels = 4
#     def __drive(self):
#         print("驾驶")
#     def test(self):
#         print(f"轿车有{self.__wheels}个车轮")
#         self.__drive()
#
# car1 = Car()
# # 私有成员在类的外部不能直接访问
# # print(car1.__wheels)

# class MyClass:
#     def __init__(self):
#         self.__private_member = "这是一个私有属性"
#
#     def get_private_member(self):
#         return self.__private_member
#
# obj1 = MyClass()
# #报错,不能从外部直接访问私有成员
# # print(obj1.__private_member)

class MyClass:
    def __init__(self):
        pass

    def __private_method(self):
        print("这是一个私有方法")

    def public_method(self):
        print("这是一个公有方法")
        # 内部调用私有方法
        self.__private_method()


obj2 = MyClass()
# 私有调用失败
# obj2.__private_method
obj2.public_method()
