import re

# 两种正则表达式方法：字符串方法、正则表达式对象方法

pattern = '[a-z]*' #小写字母匹配任意次
print(re.match(pattern, 'hello123!!')) #<re.Match object; span=(0, 5), match=匹配第0-第5位
print(re.match(pattern, 'hello123').group(0))

print(re.match('.', 'abc').group(0))

# python专门为正则表达式提供了一个内置的conpile()函数用来生成pattern对象
# compile()函数可以将正则表达式字符串编译成正则表达式对象并返回
pattern = re.compile(r"^1[3|4|5|6|7|8][0-9]\d{8}$",re.I)
print(type(pattern))
print(re.match(pattern,'13574895612'))

# re.match()函数
# 功能是从字符串的起始位置开始寻找匹配正则表达式的字符串，如果匹配成功，则返回一个匹配对象；如果从起始位置就匹配不成功，则返回None;
# match函数的定义方法: re.match(pattern,string,flags=0)
# pattern为匹配的正则表达式，string为待匹配的字符串，flags为匹配模式，他是一个可选值，即在使用match()函数时可以不加入flags参数。
# match()函数匹配成功会返回一个匹配的对象，要访问其匹配出的值可以使用group(num)函数或groups()函数
str1 = "my name i Wang Jianfei"
print(re.match("(my)",str1).group(0))
print(re.match("my",str1).group(0))
print(re.match("^\D{4}",str1).group(0))
print(re.match("\D{4}",str1).group(0))
# pattern = re.compile(r"[A-Za-z]{4}$",str1)
# print(re.match("\D{4}",str1).group(0))
# print(re.match("\D{4}",str1).group(0))

str2 = "Wang Jianfei is 20 years old!"
print(re.match(f".*(\d{2}).*",str2).group(0))
print(re.match(f".*(\d{2}).*",str2).group(1))

str3 = "我是王杰克，今年23岁"
print(re.match(f"[\u4e00-\u9fa5]*",str3).group(0))
print(re.match(f"[\u4e00-\u9fa5]*",str3).group(0))