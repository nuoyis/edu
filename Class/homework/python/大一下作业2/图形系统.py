# 创建一个简单的图形系统，基类为Shape，以及子类 Circle、Rectangle和 Triangle等，每个图形都有绘制draw方法、面积计算方法、周长计算方法。
import math
import string


class Shape:
    # 矩形是4条边，三角形3条边，圆形需要半径

    # 圆的定义方法 半径
    def Circle(self, radius):
        self.radius = radius

    # 矩形的定义方法 长大于宽
    def Rectangle(self, width, height):
        self.width = width
        self.height = height

    # 三角形的定义方法 三边关系:勾股弦 两边大于第三边
    def Triangle(self, hook, share, string):
        self.hook = hook
        self.share = share
        self.string = string


class Rectangle(Shape):
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            print("两边中均不得为0，请重新输入")
            exit(1)
        super().Rectangle(width, height)

    # 长 x 宽
    def mianji(self):
        return self.width * self.height

    # (长 + 宽 )x 2
    def zhouchang(self):
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius):
        if radius <= 0:
            print("半径不得为0，请重新输入")
            exit(1)
        super().Circle(radius)
        self.pai = 3.14

    # S=πr²
    def mianji(self):
        return self.radius ** 2 * self.pai

    # C=2*π*r
    def zhouchang(self):
        return 2 * self.radius * self.pai


class Triangle(Shape):
    def __init__(self, hook, share, string):
        if hook <= 0 or share <= 0 or string <= 0:
            print("三边中均不得为0，请重新输入")
            exit(1)
        if hook + share <= string and share + share <= string:
            print("两边之和应大于第三边，请重新输入")
            exit(1)
        super().Triangle(hook, share, string)

    def mianji(self):
        self.s = (self.hook + self.share + self.string) / 2.0
        return math.sqrt(self.s * (self.s - self.hook) * (self.s - self.share) * (self.s - self.string))

    def zhouchang(self):
        return self.hook + self.share + self.string


Rectangle = Rectangle(5, 10)
print(Rectangle.mianji())
print(Rectangle.zhouchang())
Circle = Circle(5)
print(Circle.mianji())
print(Circle.zhouchang())
Triangle = Triangle(3, 4, 5)
print(Triangle.mianji())
print(Triangle.zhouchang())
