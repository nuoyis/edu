# 用户注册-面向对象案例
import json
# 用户信息输入
def interactive():
    name = input("请输入用户名:").strip()  # 去掉前后空格
    password = input("请输入密码:").strip()
    email = input("请输入邮箱").strip()

    user_info = {
        'name': name,
        'password': password,
        'email': email
    }
    return user_info


# 用户信息检查
def check(userinfo):
    is_valid = True
    # 检查用户名不为空
    if len(user_info['name']) == 0:
        print("用户名不能为空")
        is_valid = False
    # 检查密码不能少于6位
    if len(user_info['password']) <= 6:
        print("密码不能少于6位")
        is_valid = False
    #为了让用户知道哪里错了，应该定制更复杂的返回信息
    return {
        'userinfo': userinfo,
        'is_valid': is_valid
    }

# 用户信息注册
def register(check_info):
    if check_info['is_valid']:
        with open('test.json', 'w', encoding='utf-8') as f:
            json.dump(check_info['userinfo'], f)

if __name__ == "__main__":
    user_info = interactive()
    check_info = check(user_info)
    register(check_info)
