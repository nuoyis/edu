class Car:
    __wheels = 4
    def __drive(self):
        print("驾驶")
    def test(self):
        print(f"轿车有{self.__wheels}个车轮")
        self.__drive()

car1 = Car()
# 私有成员在类的外部不能直接访问
# print(car1.__wheels)