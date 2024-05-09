import re

class IsCellphone():
    def __init__(self,phone):
        self.p = re.compile(r"^1[3-8]\d{9}$")

    def IsCellphone(self,number):
        res = self.p.match(number)
        if res:
            return True
        else:
            return False

p = IsCellphone()
f = open("云1通讯录","r",encoding="utf-8")
data = f.read()
print(data)
contacts = re.findall("[0-9]{11}",data)
print(contacts)
for i in contacts:
    if p.IsCellphone(i):
        print("%s是正常号码!! "% i)
    else:
        print("%s 不是正常号码!!"% i)