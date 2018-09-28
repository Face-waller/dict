from socket import *
import sys

s = socket()

# 登录
def login(s):
    while True:
        print('''

        ------Welcome-------
        --------登录--------

        ''')
        name = input('请输入用户名:')
        passw = input('请输入密码:')
        if name == '' or passw == '':
            print('用户名及密码不能为空!')
        else:
            s.send('#L'.encode())
            s.send((name+'/'+passw).encode())
            data = s.recv(1024)
            if data.decode() == 'OK':
                print('登录成功!')
                return name
            else:
                print(data.decode())

# 注册
def register(s):
    while True:
        print('''

        -------Welcome------
        --------注册--------

        ''')
        rname = input('输入注册用户名:')
        rpassw = input('输入注册密码:')
        if rname == '' or rpassw == '':
            print('用户名及密码不能为空!')
        else:
            s.send('#R'.encode())
            s.send((rname+'/'+rpassw).encode())
            data = s.recv(1024)
            if data.decode() == 'OK':
                print('注册成功!')
                return rname
            else:
                print(data.decode())

#----------------------------------------------


# 查词
def find(s, user):
    ci = input('请输入要查询的单词:')
    s.send('#F'.encode())
    s.send((ci+'/'+user).encode())
    data = s.recv(1024)
    print()
    print(data.decode())


# 查询历史
def history(s, user):
    s.send('#H'.encode())
    s.send((user+'/'+'##').encode())
    data = s.recv(1024)
    print(data.decode())




#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



# 字典功能界面
def dictmain2(s, user):
    while True:
        print('''

        -----------Welcome--------
        --------1. 查询单词--------
        --------2. 查询历史--------
        --------3. 退出词典--------

        ''')

        choice = input('输入选择的操作1/2/3:')

        if choice == '1':
            find(s, user)

        elif choice == '2':
            history(s, user)

        elif choice == '3':
            s.close()
            sys.exit()

        else:
            print('请输入正确操作!')



# 软件启动界面
def main():

    # 连接服务器网络
    try:
        s.connect(('127.0.0.1',9999))
    except:
        print('无法连接服务器，请检查网络!')
        s.close()
        sys.exit()

    while True:
        print('''

        --------Welcome-------
        --------1. 登录--------
        --------2. 注册--------
        --------3. 退出词典----

    ''')

        choi = input('输入选择的操作1/2:')
        if choi == '1':
            # 进入登录界面
            user = login(s)
            # 登录成功进入第二界面
            dictmain2(s, user)

        elif choi == '2':
            # 进入注册界面
            user = register(s)
            # 注册成功进入第二界面
            dictmain2(s, user)

        elif choi == '3':
            s.close()
            sys.exit()

        else:
            print('请输入正确操作!')

#----------------------------------------------------------
    
if __name__ == '__main__':
    main()




