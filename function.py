from flask import Flask, request, session
import pymysql
from random import randint
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

def connect_mysql():
    # 连接数据库
    connection = pymysql.connect(
        host='localhost', user='root', password='jn123528', charset='utf8'
    )
    return connection

def get_information(sql):
    # 从数据库中获取信息
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return data

def insert_information(sql):
    # 往数据库中插入信息
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.commit()
    connection.close()

def find_information(sql):
    # 从数据库中查找信息
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return data

def get_user():
    # 获取session中的用户信息
    if 'Username' in session:
        name = session.get('Username')
        ID = session.get('ID')
        Email = session.get('Email')
        user = {'Username': name, 'Email': Email, 'ID': ID}
        return user
    else:
        return False

def get_flim_page(page):
    # 按页获取电影资源
    if not page:
        page = 1
    sql = 'select * from flim.information limit %d,12;'%(page*12)
    flims = get_information(sql)
    one = []
    for content in flims:
        name = content[0]
        link = content[1]
        image_url = content[4]
        flim_id = content[7]
        flag = content[8]
        flim = {'name':name, 'link':link, 'image_url':image_url, 'id':flim_id, 'flag':flag}
        one.append(flim)
    pages = {'first':1, 'end':36, 'one':page+1, 'two':page+2, 'three':page+3, 'pre':page-1, 'next':page+1}
    return one, pages

def get_flim(flim_id):
    # 获取电影信息
    sql = "select * from flim.information where id={};".format(flim_id)
    data = get_information(sql)[0]
    name = data[0]
    link = data[1]
    info = data[2]
    describe = data[3]
    image_url = data[4]
    flag = data[8]
    infor = {'name': name, 'info': info, 'image_url': image_url, 'link': link, 'describe': describe, 'flag': flag}
    return infor

def get_book_page(page):
    # 按页获取书籍信息
    if not page:
        page = 1
    sql = 'select * from book.book limit %d,12;' % (page * 12)
    books = get_information(sql)
    one = []
    for content in books:
        name = content[0]
        info = content[1]
        image_url = content[2]
        book_id = content[5]
        flag = content[6]
        book = {'name': name, 'info': info, 'image_url': image_url, 'id': book_id, 'flag': flag}
        one.append(book)
    pages = {'first': 1, 'end': 19, 'one': page + 1, 'two': page + 2, 'three': page + 3, 'pre': page - 1,
             'next': page + 1}
    return one, pages

def get_book(book_id):
    # 获取书籍信息
    sql = "select * from book.book where id={};".format(book_id)
    data = get_information(sql)[0]
    name = data[0]
    info = data[1]
    image_url = data[2]
    star = data[3]
    describe = data[4]
    flag = data[6]
    infor = {'name': name, 'info': info, 'image_url': image_url, 'star': star, 'describe': describe, 'flag': flag}
    return infor

def get_music_page(page):
    # 按页获取音乐信息
    if not page:
        page = 1
    sql = 'select * from music.music limit %d,12;' % (page * 12)
    musics = get_information(sql)
    one = []
    for content in musics:
        name = content[0]
        info = content[1]
        image_url = content[4]
        music_id = content[6]
        flag = content[5]
        music = {'name': name, 'info': info, 'image_url': image_url, 'id': music_id, 'flag': flag}
        one.append(music)
    pages = {'first': 1, 'end': 20, 'one': page + 1, 'two': page + 2, 'three': page + 3, 'pre': page - 1,
             'next': page + 1}
    return one, pages

def get_music(music_id):
    # 获取音乐信息
    sql = "select * from music.music where id={};".format(music_id)
    data = get_information(sql)[0]
    name = data[0]
    info = data[1]
    image_url = data[4]
    star = data[3]
    describe = data[2]
    flag = data[6]
    infor = {'name': name, 'info': info, 'image_url': image_url, 'star': star, 'describe': describe, 'flag': flag}
    return infor

def search_information(keyword):
    # 链接数据库查找信息，返回列表
    sql = "select id,flim_name,flim_info,flag from flim.information where flim_name like '%{}%';".format(keyword)
    data1 = get_information(sql)
    sql = "select id,flim_name,flim_info,flag from flim.information where flim_info like '%{}%';".format(keyword)
    data2 = get_information(sql)
    sql = "select id,name,info,flag from book.book where name like '%{}%';".format(keyword)
    data3 = get_information(sql)
    sql = "select id,name,info,flag from book.book where info like '%{}%';".format(keyword)
    data4 = get_information(sql)
    sql = "select id,name,info,flag from music.music where name like '%{}%';".format(keyword)
    data5 = get_information(sql)
    sql = "select id,name,info,flag from music.music where info like '%{}%';".format(keyword)
    data6 = get_information(sql)
    info = set(data1 + data2 + data3 + data4 + data5 + data6)
    return info

def change_information():
    # 修改用户信息
    ID = session.get('ID')
    new_name = request.form.get('name')
    new_email = request.form.get('email')
    new_password = request.form.get('password')
    connection = connect_mysql()
    cursor = connection.cursor()
    if new_name != '':
        sql = "update user.user set name='{}' where id={};".format(new_name, ID)
        print(sql)
        cursor.execute(sql)
        connection.commit()
    elif new_email != '':
        sql = "update user.user set email='{}' where id={};".format(new_email, ID)
        cursor.execute(sql)
        connection.commit()
    elif new_password != '':
        sql = "update user.user set pwd='{}' where id={};".format(new_password, ID)
        cursor.execute(sql)
        connection.commit()
    sql = "select * from user.User where id='%s';" % (ID)
    info = get_information(sql)
    return info

def login_user():
    # 从前端获取信息查询数据库
    email = request.form.get('Email')
    pwd = request.form.get('Password')
    sql = "select * from user.User where email='%s';" % (email)
    info = find_information(sql)
    if info == ():
        check = '此邮箱无效!'
        return check
    elif info[0][2] != pwd:
        check = '密码输入错误!'
        return check
    else:
        session['Username'] = info[0][1]
        session['ID'] = info[0][0]
        session['Email'] = info[0][3]
        user = {'Username': session['Username'], 'Email': session['Email'], 'ID': session['ID']}
        return user

def create_user():
    # 从前端获取数据插入数据库
    name = request.form.get('Username')
    email = request.form.get('Email')
    pwd = request.form.get('Password2')
    sql = "select * from user.User where email='%s';" % (email)
    info = find_information(sql)
    if info != ():
        check = '同一邮箱只能注册一个账号!'
        return check
    else:
        while True:
            number = str(randint(1, 100000))
            id = number.zfill(6)
            sql = "select * from user.User where id='%s';" % (id)
            if find_information(sql) == ():
                break
        info = {'Username': name, 'Email': email, 'password': pwd, 'ID': id}
        sql = "insert into user.User(id, name, email, pwd) values('%s' ,'%s', '%s', '%s');" % (
        info['ID'], info['Username'], info['Email'], info['password'])
        insert_information(sql)
        session['Username'] = info['Username']
        session['ID'] = info['ID']
        session['Email'] = info['Email']
        user = {'Username': session['Username'], 'Email': session['Email'], 'ID': session['ID']}
        return user