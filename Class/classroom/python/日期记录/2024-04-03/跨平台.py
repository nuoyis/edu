import os
#windows平台
print(os.name)
print(os.sep)
print(f"{os.linesep}asda")

#linux



# 用上面三个函数实现跨平台
#!/usr/bin/env python3
import os
path = '.' + os.sep + 'testCode' + os.sep + 'test.txt'
if not os.path.exists('testCode'):
    # 目录不存在需创建
    os.mkdir("testCode")
f = os.open(path, os.O_WR0NLY | os.O_CREAT)
os.write