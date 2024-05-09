import re

str1 = "You are reading the documentation for Vue 3!"

print(re.search("Vue", str1).group(0))

print(re.search("\s", str1).start())

print(re.search("[A-Z]", str1).end())

# 匹配d开头的单词
print(re.search("\s(d)[a-z]*", str1))

# 匹配任意字符
print(re.search("......", str1).group(0))

# ^匹配字符串行首
print(re.search("is", "history"))
print(re.search("^is", "history"))

print(re.search("y$", "history"))

print(re.search("b*", "bosojb"))
print(re.search("bo*", "boooooojb"))

print(re.search("o+", "boooooojb"))

print(re.search(".*", "boooooojb"))

print(re.search("ab?", "boooooojabbb"))
print(re.search("jb?", "boooooojb"))

# {n}匹配前一个字符N次
print(re.search("ab{3}", "boooooojabbb"))
print(re.search("[0-9]{3}", "boo99ooj2023abbb"))

# {n,m}:匹配一个字符n-m次
print(re.search("[0-9]", "boo99ooj2023abbb"))

print(re.search("[0-9]{3,5}", "boo99ooj2023abbb"))
print(re.search("[a-z]{4,5}", "boo99ooj2023abbb"))

print(re.search("Kobe|kobe|KOBE", "Kobe"))
print(re.search("[k|K]obe]", "kobe"))

# ();将括号内地内容定义为组，分组匹配
print(re.search("[a-z]+", "2023yun1class"))
print(re.search("([a-z]+)([0-9]+)", "2023yun1class"))
print(re.search("([a-z]+)([0-9]{3,})", "2023yun1class588").groups())

# \A:匹配字符串结束，等同于"^"
# \Z:匹配字符串结束，等同于"$"
# \d:匹配数字字符
print(re.search("\d+", "2023yun1class"))

# \w:匹配包括下划线的任意单词字符
# 比p[A-Za-z0-9]还多一个下划线
print(re.search("[A_Za-z0-9]+""2023yun1_class588", ""))
print(re.search("\w", "2023yun1class"))

print(re.search("\w+", "test%$#@^&*()<>{}[]-=+?test"))
print(re.search("\w+", "test%$#@^&*()<>{}[]-=+?test"))

str2 = "Docker Builds:\nNow you can build\r\nFast"
print(re.search("\s{2,}"))


# match 和 search的对比
# match()函数和search()函数的使用方法对比如下：
str1 = "My num is 8008208820"
pattern = re.compile(r"(\d).*")
m0bj = pattern.match(str1)
s0bj = pattern.search(str1)
if m0bj:
    print(m0bj.group())
else:
    print("no match")
if s0bj:
    print(s0bj.group())
else:
    print("no match")

"""

"""