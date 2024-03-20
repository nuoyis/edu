class Contacts:
    def __init__(self, name, phonenumber):
        self.name = name
        self.phonenumber = phonenumber


class update(Contacts):
    def __init__(self, name, phonenumber):
        super().__init__(name, phonenumber)
        self.name = {}

    def add(self, name, phonenumber):
        if name in self.name:
            print("联系人已经存在,请输入其他联系人!!!")
        else:
            # 将联系人实例化保存在字典中
            self.name[name] = Contacts(name, phonenumber)
            print("%s 联系人添加成功!!!" % name)

    def delete(self, name, phonenumber):
        if name not in self.name:
            print("该联系人不存在")
        else:
            self.name.pop(Contacts(name, phonenumber))
            print("删除联系人成功")

    def update(self, name, phonenumber):
        if name not in self.name:
            print("该联系人不存在")
        else:
            self.name[name] = Contacts(name, phonenumber)
            print("更改联系人成功")

    def query(self, name, phonenumber):
        if name in name:
            print(self.name[name], self.name[phonenumber])
        else:
            return False


if __name__ == '__main__':
    use = update("nu", 1008611)
    use.add