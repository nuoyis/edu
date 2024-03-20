num = input("num>>:")
try:
    int(num)
    l = []
    l[11]
    1/0
    dic = {"k":'v'}
    dic["k2"]
    print("************************************")
except ValueError:
    print("请输入一个数字!!")
except IndexError as name_e:
    print(name_e)
except ZeroDivisionError as zero_e:
    print(zero_e)
else:
    print("else被执行")
finally:
