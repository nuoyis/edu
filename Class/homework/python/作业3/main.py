class Hero:
    def __init__(self, name, attack1, defense, life, attack2, skill):
        self.name = name
        self.attack1 = attack1
        self.defense = defense
        self.life = life
        self.attack2 = attack2
        self.skill = skill

class liubei(Hero):
    def __init__(self, name, attack1, defense, life, attack2, skill):
        Hero.__init__(self, name, attack1, defense, life, attack2, skill)
        print(f"""这里是{self.name} \n
                攻击力:{self.attack1} \n
                防御力:{self.defense} \n
                生命值:{self.life} \n
                攻击:{self.attack2} \n
                技能:{self.skill} \n
        """)

class guanyu(Hero):
    def __init__(self, name, attack1, defense, life, attack2, skill):
        Hero.__init__(self, name, attack1, defense, life, attack2, skill)
        print(f"""这里是{self.name} \n
                攻击力:{self.attack1} \n
                防御力:{self.defense} \n
                生命值:{self.life} \n
                攻击:{self.attack2} \n
                技能:{self.skill} \n
        """)

class zhangfei(Hero):
    def __init__(self, name, attack1, defense, life, attack2, skill):
        Hero.__init__(self, name, attack1, defense, life, attack2, skill)
        print(f"""这里是{self.name} \n
                攻击力:{self.attack1} \n
                防御力:{self.defense} \n
                生命值:{self.life} \n
                攻击:{self.attack2} \n
                技能:{self.skill} \n
        """)

liubei("liubei", 1, 2, 3, 4, "法师")
zhangfei("zhangfei", 6, 7, 8, 9, "坦克")
guanyu("guanyu", 11, 12, 13, 14, "刺客")