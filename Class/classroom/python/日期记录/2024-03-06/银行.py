class bank:
    def __init__(self):
        self.balance = 0.00
        self.user = "user"

    def bank_user(self, user):
        if user == "user":
            return True
        else:
            return False

    def bank_get(self, money):
        self.balance += money
        return True

    def bank_out(self, money):
        if money >= self.balance:
            self.errormsg = "You don't have enough money"
            return self.errormsg, False
        else:
            self.balance -= money

    def bank_balance(self):
        return self.balance


bank = bank()
userok = bank.bank_user(input("请输入用户名:"))
if userok:
    cunorqu = input("请输入存款还是取款还是查询余额:")
    if cunorqu == "存款":
        bank.bank_get(float(input("请输入存款金额")))
        print(bank.bank_balance())
    elif cunorqu == "取款":
        bank.bank_out(float(input("请输入取款金额")))
        print(bank.bank_balance())
    elif cunorqu == "查询余额":
        print(bank.bank_balance())
else:
    print("用户名输入错误，请重试")
