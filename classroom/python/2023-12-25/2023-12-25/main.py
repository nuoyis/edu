# #1.
# s = "AbcDeFGhIJ"
# sum = 0
# for i in s:
#     if 'a' <= i <= 'z':
#         sum+=1
# print(sum)
#
# #2.
# s = "Life is short.I use python"
# j = "python"
# if j in s:
#     print(s.replace("python","Python"))
# else:
#     print(s)
#
# #3.71
# li_num = [4, 5, 2, 7]
# li_num2 = [3, 6]
# print(sorted(list(set(li_num+li_num2)),reverse=True))
#
# #4.
# tu_num1= ('p','y','t',['o','n'])
# tu_num1[-1].append('h')
# print(tu_num1)
#
# #5.
# str = "skdaskerkjsalkj"
# str1 = list(set(str))
# for i in str1:
#     sum = 0
#     for j in str:
#         if j == i:
#             sum += 1
#     print(i+" is",sum)

#6.
li_one = [1, 2, 1, 2, 3, 5, 4, 3, 5, 7, 4, 7, 8]
print(list(set(li_one)))

huiwen = input("please enter:")
huiwenshu = len(huiwen)

i = 0
none = 0
while i <= (huiwenshu / 2):
    if huiwen[i] != huiwen[huiwenshu-i-1]:
        print("none")
        none = 1
        break
    i+=1
if not none:
    print("ok")





