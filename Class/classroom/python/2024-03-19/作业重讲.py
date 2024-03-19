# 模拟《王者荣耀》中的英雄系统，可以创建一个基础的 Hero 类（名字、攻击力、防御力、生命值、攻击、技能等），
# 然后通过继承来实现不同类型的英雄类，例如坦克、刺客、法师等。再根据各自英雄类创建英雄对象。
class Hero:
    """docstring for Hero"""

    def __init__(self, name: str, attack_power: int, defense: int, health: int, skills: list):
        """
        英雄初始化属性
        :param name: 名称
        :param attack_power: 攻击力
        :param defense: 防御力
        :param skill: 技能
        """
        self.name = name
        self.attack_power = attack_power
        self.defense = defense
        self.health = health
        self.skills = skills

    def attack(self, target):
        """
        英雄攻击，每个子类应该都重新要定义
        :param target: 攻击目标
        :return: 攻击结果
        """
        pass

    def display_info(self):
        print("英雄名称:", self.name)
        print("攻击力:", self.attack_power)
        print("防御力:", self.defense)
        print("生命值:", self.health)
        print("生命列表:")
        for skill in self.skills:
            print(skill)


class PysicalHero(Hero):
    """docstring for PysicalHero"""
    def __init__(self,  name: str, attack_power: int, defense: int, health: int, skills: list):
        super().__init__(name, attack_power, defense, health, skills)

    def attack(self, target):
        # 伤害要基于公式计算
        damage = self.cal_damage(target)
        print(f"{self.name}对{target}造成物理伤害,造成了{damage}点伤害!")

    def cal_damage(self, target):
        # 针对对象计算伤害
        if self.attack_power > self.defense:
            return self.attack_power - self.defense
        else:
            return 1

class MagicHero(Hero):
    def __init__(self,  name: str, attack_power: int, defense: int, health: int, skills: list):
        super().__init__(name, attack_power, defense, health, skills)

    def attack(self, target):
        magical_damage = self.cal_damage(target)
        print(f"{self.name}对{target.name}造成了魔法伤害,造成了{magical_damage}点魔法伤害!!!")

    def cal_damage(self, target):
        if self.attack_power * 1.2 > target.defense:
            return self.attack_power * 1.2 - target.defense
        else:
            return 1

guanyu = PysicalHero("guanyu", 90, 50, 300, ["横扫千军", "一马当先", "无敌斩"])
guanyu.display_info()
simayi = MagicHero("simayi", 67, 40, 280, ["烈火燎原", "火炷"])
simayi.display_info()




# class liubei(Hero):
#     def __init__(self, name, attack1, defense, life, attack2, skill):
#         Hero.__init__(self, name, attack1, defense, life, attack2, skill)
#         print(f"""这里是{self.name} \n
#                 攻击力:{self.attack1} \n
#                 防御力:{self.defense} \n
#                 生命值:{self.life} \n
#                 攻击:{self.attack2} \n
#                 技能:{self.skill} \n
#         """)
#
#
# class guanyu(Hero):
#     def __init__(self, name, attack1, defense, life, attack2, skill):
#         Hero.__init__(self, name, attack1, defense, life, attack2, skill)
#         print(f"""这里是{self.name} \n
#                 攻击力:{self.attack1} \n
#                 防御力:{self.defense} \n
#                 生命值:{self.life} \n
#                 攻击:{self.attack2} \n
#                 技能:{self.skill} \n
#         """)
#
#
# class zhangfei(Hero):
#     def __init__(self, name, attack1, defense, life, attack2, skill):
#         Hero.__init__(self, name, attack1, defense, life, attack2, skill)
#         print(f"""这里是{self.name} \n
#                 攻击力:{self.attack1} \n
#                 防御力:{self.defense} \n
#                 生命值:{self.life} \n
#                 攻击:{self.attack2} \n
#                 技能:{self.skill} \n
#         """)
#
#
# liubei("liubei", 1, 2, 3, 4, "法师")
# zhangfei("zhangfei", 6, 7, 8, 9, "坦克")
# guanyu("guanyu", 11, 12, 13, 14, "刺客")
