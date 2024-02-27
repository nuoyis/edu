# import http.client
#
# conn = http.client.HTTPSConnection("api.v2.rainyun.com")
# payload = ''
# headers = {
#    'x-api-key': 'ctj5wSOCeUcb0ZzJXgaQBHL52uSJmd5c',
#    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
# }
# conn.request("GET", "/user/coupons/", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

i = ['nuoyis.com', 'dianji.space', 'iqiyi.ltd', 'nuoyis.xyz', 'nuoyis.space', 'folw.cn']
for j in i:
   print(j)
   print("www."+j)
   print("blog."+j)
   print("api."+j)
   print("status."+j)
   print("static." + j)
   print("\n")