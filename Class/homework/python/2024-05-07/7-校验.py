# 从html文件中提取url 超链接
import re

html = """
<a href='http://www.baidu.com'></a>
<a href='http://www.360.com/index'></a>
<a href='http://www.img.com/2256.txt'></a>
"""

url = re.findall(r'<a[^>]+href["\'](.*?)["\']', html)
print(url)

# 1
with open("test.txt", "r", encoding="utf-8") as f:
    print("单词cat出现了 %s 次"% len(re.findall(r'cat+', f.read())))

# 2
html2 = "+86 800-820-8820"
print(re.sub("-","",re.sub("\+86\s", "", html2)))
# 3
html3 = "1*3*0%Fc3$ac4*cs6滴+3=F哈8ssa5*cs2*1"
r = re.findall("\d+", html3)
for i in r:
    print(i,end="")
