class Animal:
    def speak(self):
        pass


class Dog(Animal):
    def speak(self):
        print("狗在吠叫!!!")


class Cat(Animal):
    def speak(self):
        print("猫在喵喵叫!!!")


class People(Animal):
    def speak(self):
        print("有人在聊天!!!")

def animal_speak(animal):
        animal.speak()

d1 = Dog()
c1 = Cat()
p1 = People()
d1.speak()
c1.speak()
p1.speak()