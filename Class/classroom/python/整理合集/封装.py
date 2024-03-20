class Person:
    def __init__(self, name):
        self.name = name
        self.__age = 1

    def set_age(self, new_age):
        if 0 < new_age <= 120:
            self.__age = new_age

    def get_age(self):
        return self.__age


person1 = Person("kobe")
print(f"{person1.name}的年龄是{person1.get_age()}")
