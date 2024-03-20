def GetAge(age):
    try:
        if age <= 0:
            raise ValueError("你输出的年龄不符合规则")
        return age
    except ValueError:
        print('年龄必须大于0')
        raise ZeroDivisionError("除数必须大于0！")

GetAge(0)
