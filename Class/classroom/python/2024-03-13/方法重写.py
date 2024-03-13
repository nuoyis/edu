# 在父类的基础上产生子类,产生的子类也叫做派生类
# 派生类可以重用父类的代码,可以添加新的属性和方法,实现特定的行为
class Hero:
    def __init__(self, name, life_value, aggressivity):
        self.name = name
        self.life_value = life_value
        self.aggressivity = aggressivity

    def attack(self, enemy):
        enemy.life_value = enemy.life_value - self.aggressivity


class Garen(Hero):
    def attack(self, enemy):
        enemy.life_value = enemy.life_value - self.aggressivity * 2
        print("来自盖伦的双倍伤害")


class Riven(Hero):
    def fly(self):
        # 在子类定义新的方法
        print("%s 正在飞!!!" % self.name)


g = Garen("草丛伦", 120, 30)
r = Riven("玮", 110, 33)

g.attack(r)
r.attack(g)
r.fly()
print("%s 当前生命值 %s" % (g.name, g.life_value))
print("%s 当前生命值 %s" % (r.name, r.life_value))
