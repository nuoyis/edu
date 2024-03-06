class Shoppingcart:
    def __init__(self):
        self.items = {}

    def add(self, name, money):
        self.items[name] = money

    def remove(self, name):
        del self.items[name]

    def num(self):
        return len(self.items)

    def viewall(self):
        if not self.items:
            print("No items")
        else:
            for i in self.items:
                print(i, self.items[i])

    def allprice(self):
        self.price = 0
        for i in self.items:
            self.price += int(self.items[i])
        print(self.price)


Shop = Shoppingcart()
Shop.add('Banana', '20')
Shop.add('applephone', '10000')
Shop.add('apple', '10')
print(Shop.num())
Shop.remove('apple')
print(Shop.num())
Shop.viewall()
Shop.allprice()
