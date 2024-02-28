class Yun1Stu:
    school = "hbkj"
    class_name = "1班"
    grade = "2023"
    city = "wuhan"

    def learn(self):
        self.content = "python"
        print("学习")

    def eat(self):
        self.food = "KFC"
        print("吃")

    def sleep(self):
        self.situation = "家"
        print("睡觉")


stu1 = Yun1Stu()
stu1.learn()
stu1.eat()

stu2 = Yun1Stu()
print(Yun1Stu.class_name)
Yun1Stu.class_name = "云计算一班"
print(Yun1Stu.class_name)
stu2.school = "武汉大学"
print(stu1.school)
print(stu2.school)
stu2.sleep()

stu3 = Yun1Stu()
stu3.learn()
print(stu3.content)

ssq = Yun1Stu
yange = Yun1Stu()
ssq.eat()
yange.eat()
ssq.food = "广式早茶"
yange.food = "海底捞"
ssq.food = "热干面"
ssq.drink = "ice tea"
yange.drink = "ice tea"
