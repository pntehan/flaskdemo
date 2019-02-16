from flask import Flask, request, session
from flask import render_template
import pymysql
from random import randint
from flask_session import Session
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

def connect_mysql():
    connection = pymysql.connect(
        host='localhost', user='root', password='jn123528', charset='utf8'
    )
    return connection

def get_information(sql):
    #连接数据库，num是指网页页数，返回一个含有12个电影信息的列表
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return data

def insert_information(sql):
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.commit()
    connection.close()

def find_information(sql):
    connection = connect_mysql()
    cursor = connection.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    connection.commit()
    connection.close()
    return data

@app.route('/')
def home():
    if 'Username' in session:
        name = session.get('Username')
        ID = session.get('ID')
        Email = session.get('Email')
        user = {'Username':name, 'Email':Email, 'ID':ID}
        return render_template('home.html', title='主页', user=user)
    else:
        return render_template('home.html', title='主页')

@app.route('/flim_<int:page>')
def flim(page):
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
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('contents.html', title='电影', contents=one, page=pages, user=user)
    else:
        return render_template('contents.html', title='电影', contents=one, page=pages)

@app.route('/flim-<int:flim_id>')
def one_flim(flim_id):
    #电影信息
    sql = "select * from flim.information where id={};".format(flim_id)
    data = get_information(sql)[0]
    name = data[0]
    link = data[1]
    info = data[2]
    describe = data[3]
    image_url = data[4]
    flag = data[8]
    infor = {'name':name,'info':info,'image_url':image_url,'link':link,'describe':describe,'flag':flag}
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)

@app.route('/music_<int:page>')
def music(page):
    #音乐页面
    if not page:
        page = 1
    sql = 'select * from music.music limit %d,12;'%(page*12)
    musics = get_information(sql)
    one = []
    for content in musics:
        name = content[0]
        info = content[1]
        image_url = content[4]
        music_id = content[6]
        flag = content[5]
        music = {'name':name, 'info':info,'image_url':image_url, 'id':music_id, 'flag':flag}
        one.append(music)
    pages = {'first':1, 'end':20, 'one':page+1, 'two':page+2, 'three':page+3, 'pre':page-1, 'next':page+1}
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('contents.html', title='音乐', contents=one, page=pages, user=user)
    else:
        return render_template('contents.html', title='音乐', contents=one, page=pages)

@app.route('/music-<int:music_id>')
def one_music(music_id):
    sql = "select * from music.music where id={};".format(music_id)
    data = get_information(sql)[0]
    name = data[0]
    info = data[1]
    image_url = data[4]
    star = data[3]
    describe = data[2]
    flag = data[6]
    infor = {'name':name,'info':info,'image_url':image_url,'star':star,'describe':describe,'flag':flag}
    # print(infor)
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)

@app.route('/book_<int:page>')
def book(page):
    #书籍页面
    if not page:
        page = 1
    sql = 'select * from book.book limit %d,12;'%(page*12)
    books = get_information(sql)
    one = []
    for content in books:
        name = content[0]
        info = content[1]
        image_url = content[2]
        book_id = content[5]
        flag = content[6]
        book = {'name':name, 'info':info,'image_url':image_url, 'id':book_id, 'flag':flag}
        one.append(book)
    pages = {'first':1, 'end':19, 'one':page+1, 'two':page+2, 'three':page+3, 'pre':page-1, 'next':page+1}
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('contents.html', title='书籍', contents=one, page=pages, user=user)
    else:
        return render_template('contents.html', title='书籍', contents=one, page=pages)

@app.route('/book-<int:book_id>')
def one_book(book_id):
    sql = "select * from book.book where id={};".format(book_id)
    data = get_information(sql)[0]
    name = data[0]
    info = data[1]
    image_url = data[2]
    star = data[3]
    describe = data[4]
    flag = data[6]
    infor = {'name':name,'info':info,'image_url':image_url,'star':star,'describe':describe,'flag':flag}
    if 'Username' in session:
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        print(user)
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)


@app.route('/search', methods={'GET', 'POST'})
def search():
    keyword = request.form.get('keyword')
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
    info = set(data1+data2+data3+data4+data5+data6)
    print(keyword)
    if 'Username' in session:
        name = session.get('Username')
        ID = session.get('ID')
        Email = session.get('Email')
        user = {'Username':name, 'Email':Email, 'ID':ID}
        return render_template('search.html', title='查找结果', keyword=keyword, info=info, user=user)
    else:
        return render_template('search.html', title='查找结果', keyword=keyword, info=info)

@app.route('/login')
def login():
    #登录页面端口
    return render_template('login.html', title='登陆')

@app.route('/logindo', methods={'POST', 'GET'})
def logindo():
    #登录判断页面
    email = request.form.get('Email')
    pwd = request.form.get('Password')
    sql = "select * from user.User where email='%s';"%(email)
    info = find_information(sql)
    if info == ():
        check = '此邮箱无效!'
        return render_template('login.html', title='登陆', check=check)
    elif info[0][2] != pwd:
        check = '密码输入错误!'
        return render_template('login.html', title='登陆', check=check)
    else:
        session['Username'] = info[0][1]
        session['ID'] = info[0][0]
        session['Email'] = info[0][3]
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        return render_template('home.html', title='主页', user=user)

@app.route('/loginout')
def loginout():
    #退出登录
    session.clear()
    return render_template('home.html', title='主页')        

@app.route('/register')
def register():
    #注册页面
    return render_template('register.html', title='注册')

@app.route('/registerdo', methods={'POST', 'GET'})
def registerdo():
    #注册判断页面
    name = request.form.get('Username')
    email = request.form.get('Email')
    pwd = request.form.get('Password2')
    sql = "select * from user.User where email='%s';"%(email)
    info = find_information(sql)
    if info != ():
        check = '同一邮箱只能注册一个账号!'
        return render_template('register.html', title='注册', check=check)
    else:
        while True:
            number = str(randint(1,100000))
            id = number.zfill(6)
            sql = "select * from user.User where id='%s';"%(id)
            if find_information(sql) == ():
                break
        info = {'Username':name, 'Email':email, 'password':pwd, 'ID':id}
        print(info)
        sql = "insert into user.User(id, name, email, pwd) values('%s' ,'%s', '%s', '%s');"%(info['ID'], info['Username'], info['Email'], info['password'])
        insert_information(sql)
        session['Username'] = info['Username']
        session['ID'] = info['ID']
        session['Email'] = info['Email']
        user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
        return render_template('home.html', title='主页', user=user)

@app.route('/user')
def user():
    #用户信息页面
    name = session.get('Username')
    ID = session.get('ID')
    Email = session.get('Email')
    user = {'Username':name, 'Email':Email, 'ID':ID}
    return render_template('user.html', title='个人主页', user=user)

@app.route('/change', methods={'POST', 'GET'})
def change():
    #修改信息
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
    sql = "select * from user.User where id='%s';"%(ID)
    info = get_information(sql)
    session['Username'] = info[0][1]
    session['ID'] = info[0][0]
    session['Email'] = info[0][3]
    user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
    return render_template('user.html', title='个人主页', user=user)
    

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='5000')