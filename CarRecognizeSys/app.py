from flask import  Flask,render_template
from flask import redirect
from flask import  url_for
from flask import request
from  model.check_login import is_existed,is_null,exist_user
from model.regist_login import add_user,check_password
from model.create_database import create_db

app = Flask(__name__,template_folder='templates')

@app.route('/')
def login():
    return  redirect(url_for('user_login'))
@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if is_null(username,password):
            login_message="账号密码不能为空"
            return render_template('login.html',message=login_message)
        elif is_existed(username,password):
            return render_template('index.html')
        elif exist_user(username):
            login_message="密码错误，请输入正确密码"
            return render_template('login.html',message=login_message)
        else:
            login_message="不存在该用户，请先注册"
            return render_template('login.html',message=login_message)
    return render_template('login.html')

@app.route('/regist',methods=['GET','POST'])
def regist():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        password2=request.form['password2']
        if is_null(username,password):
            login_message="账号密码不能为空"
            return render_template('regist.html',message=login_message)
        elif exist_user(username):
            login_message = "用户已存在,请直接登录"
            # return redirect(url_for('user_login'),message=login_message)
            return render_template('login.html', message=login_message)
        else:
            if check_password(password,password2):
                add_user(request.form['username'],request.form['password'])
                login_message = "注册成功"
                # return render_template('login.html',message=login_message)
                return redirect(url_for('user_login'),Response=login_message)
            else:
                login_message = "两次输入密码不一致"
                return render_template('regist.html', message=login_message)
    return render_template('regist.html')

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

if __name__=="__main__":
    #create_db() # 创建数据库，创建完请注释掉
    app.run(debug=True)