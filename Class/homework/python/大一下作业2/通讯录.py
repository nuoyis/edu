class Contacts:
    def __init__(self, name, phonenumber):
        self.gather = name
        self.phonenumber = phonenumber


class database(Contacts):
    def __init__(self, name, phonenumber):
        super().__init__(name, phonenumber)
        self.gather = {}
        self.name = name
        self.phonenumber = str(phonenumber)

    def add(self):
        if self.name in self.gather:
            print("联系人已经存在,请输入其他联系人!!!")
        else:
            # 将联系人实例化保存在字典中
            self.gather[self.name] = self.phonenumber
            print("%s 联系人添加成功!!!" % self.name)

    def delete(self):
        if self.name not in self.gather:
            print("该联系人不存在")
        else:
            del self.gather[self.name]
            print("删除联系人成功")

    def update(self, updatename="Null", updatephonenumber="Null"):
        if self.name not in self.gather:
            print("该联系人不存在")
        else:
            if updatename == "Null":
                self.updatename = self.name
            else:
                self.updatename = updatename
            if updatephonenumber == "Null":
                self.updatephonenumber = self.phonenumber
            else:
                self.updatephonenumber = str(updatephonenumber)
            del self.gather[self.name]
            self.gather[self.updatename] = self.updatephonenumber
            self.name = self.updatename
            self.updatename = self.updatephonenumber
            print("更改联系人成功")

    def query(self):
        if self.name in self.gather:
            print(self.name, self.gather[self.name])
        else:
            return False


if __name__ == '__main__':
    use = database("nu", 1008611)
    use.add()
    use.query()
    user = database("nu", 1008611)
    user.add()
    user.update("nuoo", "10086")
    user.query()
