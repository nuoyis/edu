import re

key = "javaphppythonc++golang"
# 从上面字符串中提取python
print(re.findall("python", key))
print(re.findall("python", key)[0])

key2 = "<html><h1> hallo world!! </h1></html>"
# 从上面提取hello world
print(re.findall("<h1>.*</h1>", key2))
print(re.findall("<h1>(.*?)</h1>", key2))

key3 = "女生喜欢身高180，体重150，成绩90以上的男生！！"
# 从上面提取数字
print(re.findall("\d*", key3))
print(re.findall("\d+", key3))
# 注意+匹配前面一次或多次

"""
['', '', '', '', '', '', '180', '', '', '', '150', '', '', '', '90', '', '', '', '', '', '', '', '']
['180', '150', '90']
"""

key4 = "http://www.baidu.com and https://www.xunlei.com"

print(re.findall("https?", key4))  # ['http', 'https']
print(re.findall("https?\W{3}", key4))  # ['http://', 'https://']   \W 匹配任意非单词字符

key5 = "hejia@hbkj.edu.com"
# 从上面获取邮箱名
print(re.findall("^(.*)@", key5))

key6 = "saaas and sas and saas"

print(re.findall("sa{1,2}s", key6))

# re.split()函数和字符串中的str.split()函数有点类似，都可以用来切割字符串
# 不同的是str.split()函数不支持正则表达式以及多个切割符号，并且str.split()函数不能感知空格的数量
# re.split()函数弥补了str.split()函数的缺点，它可以通过正则表达式去切割字符串，并且支持使用多个分隔符

text = "apple,Orange,banana,kiwi;group"
# 获取上面的字符串
# \s:不包含;和,
print(re.split("[;,]\s*", text))  # 匹配分号或逗号，还有可能跟随的任意数量空白，来分割字符串
# ['apple','Orange','banana','kiwi','group']

# 分割时保留分隔符
print(re.split("[;,]", text))

print(re.split("[;,]\s*", text, maxsplit=2))

text2 = "2024-04-30 11:13:04"
print(re.findall("[:-]\s*", text2))

text3 = "I'm 20 years old#this is a comment"
# 把20岁改成30岁
re.sub("\d+", "30", text3)
#I'm 30 years old#this is a comment