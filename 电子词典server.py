import pymysql,os,sys,signal
import multiprocessing as mg
from socket import *
import time

#------------------------------------------------------------
def login(connfd,user,passwd):

    #创建数据库连接对象
    db = pymysql.connect(host='localhost',user='root',
    password='123456',database='dict',
    charset='utf8',port=3306)
    #创建游标对象
    cursor = db.cursor()

    try:
        # 执行SQL命令查看用户名和密码是否对应
        sqlselect = 'select passwd from user where name = "%s";'%user
        cursor.execute(sqlselect)
        data1 = cursor.fetchone()
        if data1[0] == passwd:
            connfd.send('OK'.encode())
        else:
            connfd.send('用户名或密码错误'.encode())
    except Exception as e:
        print('Failed',e)
    


def register(connfd,user,passwd):
    #创建数据库连接对象
    db = pymysql.connect(host='localhost',user='root',
    password='123456',database='dict',
    charset='utf8',port=3306)
    #创建游标对象
    cursor = db.cursor()

    #  执行SQL命令查看用户名是否存在，不存在正常执行，存在返回给客户端失败原因
    sqselect = 'select * from user where name = "%s";'%user
    cursor.execute(sqselect)
    data1 = cursor.fetchone()
    if data1 != None:
        connfd.send('用户名已存在!'.encode())
    else:
        try:
            sqinsert = 'insert into user(name,passwd) value("%s","%s");'%(user,passwd)
            cursor.execute(sqinsert)
            db.commit()
        except Exception as e:
            db.rollback()
            cursor.close()
            db.close()
            print('Failed',e)
        connfd.send('OK'.encode())
    cursor.close()
    db.close()


#-------------------------------------------------------


def find(connfd,ci,user):
    f = open('D:\python笔记\正则表达式\dict.txt','r')
    f.seek(0,0)
    while True:
        line = f.readline().strip()

        count = 16
        while True:
            if line[count] == ' ':
                count -= 1
            else:
                word = line[0:count+1]
                break

        if ci == word:
            connfd.send(line[17::].encode())

            #将用户历史记录插入数据库
            #创建数据库连接对象
            db = pymysql.connect(host='localhost',user='root',
            password='123456',database='dict',
            charset='utf8',port=3306)
            #创建游标对象
            cursor = db.cursor()
            try:
                sqinsert = 'insert into hist(name,word,time) value("%s","%s","%s");'%(user,ci,time.ctime())
                cursor.execute(sqinsert)
                db.commit()
            except Exception as e:
                db.rollback()
                cursor.close()
                db.close()
                print('Failed',e)
            f.seek(0,0)
            break

        elif ci > word:
            continue

        elif ci < word:
            connfd.send('查询不到这个单词!'.encode())
            f.seek(0,0)
            break
    f.close()



def history(connfd,user):
    #创建数据库连接对象
    db = pymysql.connect(host='localhost',user='root',
    password='123456',database='dict',
    charset='utf8',port=3306)
    #创建游标对象
    cursor = db.cursor()
    sqselect = 'select * from hist where name = "%s";'%user
    cursor.execute(sqselect)
    data1 = cursor.fetchmany(6)
    connfd.send(str(data1).encode())
 

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# 主客户端处理函数
def main2(connfd,addr):
    while True:
        data = connfd.recv(1024)
        time.sleep(0.1)
        data1 = connfd.recv(1024).decode()
        i = data1.index('/')
        user = data1[0:i]
        passwd = data1[i+1::]

        if data.decode() == '#L':
            login(connfd,user,passwd)

        elif data.decode() == '#R':
            register(connfd,user,passwd)

        elif data.decode() == '#F':
            ci = user
            user = passwd
            find(connfd,ci,user)

        elif data.decode() == '#H':
            history(connfd,user)


    os._exit()


# 服务器启动函数
def main():
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(('0.0.0.0',9999))
    s.listen(5)


    while True:
        try:
            connfd,addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            connfd.close()
            sys.exit('服务器退出')
        except Exception as err:
            print(err)

        p = mg.Process(target=main2,args=(connfd,addr))
        p.start()

    

if __name__ == '__main__':
    main()






