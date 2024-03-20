# 实现重点处理和统一处理相结合
try:
    print("===========》1")
    print("===========》2")
    print("===========》3")
    d = {'name': 'jack'}
    print("===========》4")
    l = [1, 2, 3]
    l[5] = 3
    # name
except NameError as e:
    print("变量名异常:", e)

except ZeroDivisionError as e:
    print("除数为0异常:", e)
except KeyError as e:
    print("键异常", e)
except Exception as e:
    print("统一处理的异常", e)
else:
    print("被检测代码没有发生异常时执行")
finally:
    print("不管是否发生异常均执行")
