from flask import render_template
from function import *
from random import randint
from flask_session import Session
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

@app.route('/')
def home():
    if get_user(): # 判断是否有用户信息
        user = get_user() # 得到用户信息，字典类型
        return render_template('home.html', title='主页', user=user)
    else:
        return render_template('home.html', title='主页')

@app.route('/flim_<int:page>')
def flim(page):
    # 按页呈现电影信息
    flims, pages = get_flim_page(page)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('contents.html', title='电影', contents=flims, page=pages, user=user)
    else:
        return render_template('contents.html', title='电影', contents=flims, page=pages)

@app.route('/flim-<int:flim_id>')
def one_flim(flim_id):
    # 一部电影页面信息
    infor = get_flim(flim_id)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)

@app.route('/music_<int:page>')
def music(page):
    # 音乐页面
    one, pages = get_music_page(page)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('contents.html', title='音乐', contents=one, page=pages, user=user)
    else:
        return render_template('contents.html', title='音乐', contents=one, page=pages)

@app.route('/music-<int:music_id>')
def one_music(music_id):
    # 单个音乐信息
    infor = get_music(music_id)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)

@app.route('/book_<int:page>')
def book(page):
    #书籍页面
    one, pages = get_book_page(page)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('contents.html', title='书籍', contents=one, page=pages, user=user)
    else:
        return render_template('contents.html', title='书籍', contents=one, page=pages)

@app.route('/book-<int:book_id>')
def one_book(book_id):
    # 单个书籍信息页面
    infor = get_book(book_id)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('content.html', title=name, user=user, infor=infor)
    else:
        return render_template('content.html', title=name, infor=infor)

@app.route('/search', methods={'GET', 'POST'})
def search():
    # 查找页面
    keyword = request.form.get('keyword')
    info = search_information(keyword)
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
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
    check = login_user()
    if isinstance(check, dict):
        return render_template('home.html', title='主页', user=check)
    else:
        return render_template('login.html', title='登陆', check=check)

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
    check = create_user()
    if isinstance(check, dict):
        return render_template('home.html', title='主页', user=check)
    else:
        return render_template('register.html', title='注册', check=check)


@app.route('/user')
def user():
    #用户信息页面
    if get_user():  # 判断是否有用户信息
        user = get_user()  # 得到用户信息，字典类型
        return render_template('user.html', title='个人主页', user=user)
    else:
        return '<h1>404</h1>', 404

@app.route('/change', methods={'POST', 'GET'})
def change():
    #修改信息
    info = change_information()
    session['Username'] = info[0][1]
    session['ID'] = info[0][0]
    session['Email'] = info[0][3]
    user = {'Username':session['Username'], 'Email':session['Email'], 'ID':session['ID']}
    return render_template('user.html', title='个人主页', user=user)


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port='5000')