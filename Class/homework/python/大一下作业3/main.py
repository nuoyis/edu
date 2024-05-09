import re


# 验证邮箱地址
#
# 编写一个函数 validate_email(email)，接收一个字符串参数 email，并使用正则表达式检查该字符串是否符合有效的电子邮件地址格式。电子邮件地址应满足以下条件：
#
# 以字母、数字、下划线 _ 或点号 . 开头。
#
# 可包含字母、数字、下划线、点号或减号 -。
#
# 必须包含 @ 符号，且 @ 符号前面必须至少有一个字符。
#
# @ 符号后面必须跟至少一个点号 .，且点号前后都应有至少一个字符。
#
# 点号后面应有至少两个字符组成的顶级域名（如 .com、.net）。
#
#
#
# 检查如下邮箱地址并输出结果：
#
# 133123@qq.com
#
# wdasd@13.ad.asdw
#
# asddwa@adwd.adww
#
# adwwd2@12313.sadw
#
# asdwd2133@dedewd3
#
# asdwd2@dadwdw.dww
#
# adwdadw@dwdw..wda
#
# asdwd2@de13.d23*


# def validate_email(email):
#     if not re.compile("^[a-zA-Z0-9_.]*@\w{2,14}\.\w+").match(email):
#         return False
#     return True
#
#
# print(validate_email("133123@qq.com"))
# print(validate_email("asddwa@adwd.adww"))
# print(validate_email("wdasd@13.ad.asdw"))
# print(validate_email("adwwd2@12313.sadw"))
# print(validate_email("asdwd2133@dedewd3"))
# print(validate_email("asdwd2@dadwdw.dww"))
# print(validate_email("adwdadw@dwdw..wda"))
# print(validate_email("asdwd2@de13.d23*"))


# 编写一个函数 extract_urls(text)，接收一个字符串参数 text，并使用正则表达式从文本中找出所有HTTP或HTTPS开头的网址链接。

def extract_urls(text):
    print(re.compile(r"https?://\w+\.[\w.]+").findall(text))

sample_text = "Visit https://www.example.com and check out http://anotherexample.net for more info."
extract_urls(sample_text)

