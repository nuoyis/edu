class Shape:
    def draw(self):
        pass

    def cal_area(self):
        pass

    def cal_perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        self.pi = 3.14159

    def draw(self):
        print("绘制一个圆形半径为:", self.radius)

    def cal_area(self):
        return self.pi * (self.radius ** 2)

    def cal_perimeter(self):
        return 2 * self.pi * self.radius


# 矩形面积: 长*宽

c1 = Circle(5)
c1.draw()
print(f"半径为{c1.radius}的圆面积{c1.cal_area()}")
print(f"半径为{c1.radius}的圆周长{c1.cal_perimeter()}")
