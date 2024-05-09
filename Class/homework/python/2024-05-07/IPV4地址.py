"""
IPv4地址:四组数字和符号"."构成。

"""
import re

# \d:匹配数字字符  {1,3}:匹配1位-3位
pattern = re.compile(r"^10|172|192\.\d{1,3}\.\d{1,3}\.\d{1,3}")
ip = input("请输入IP地址:")
while ip!= "0":
    if pattern.match(ip):
        print("%s 是正常的ip地址!!!"% ip)
    else:
        print("%s 不是正常的ip地址!!!" % ip)
    ip = input("请输入IP地址")
print("ip地址校验成功!!")