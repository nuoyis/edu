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
    pass


class Riven(Hero):
    pass


g = Garen("草丛伦", 120, 30)
r = Riven("ww", 110, 33)

g.attack(r)
r.attack(g)

print("%s 当前生命值 %s" % (g.name, g.life_value))
print("%s 当前生命值 %s" % (r.name, r.life_value))
