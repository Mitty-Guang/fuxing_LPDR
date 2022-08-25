import shutil
from datetime import timedelta
import datetime
import logging as rel_log
import math
import os
from flask import Flask, request, jsonify, send_from_directory
from flask.views import MethodView
from extension import db, cors
from mymodels import Car
from sqlalchemy import func
import funcs
from itertools import groupby
import a2
from flask import  Flask,render_template
from flask import redirect
from flask import  url_for
from flask import request
from  models.check_login import is_existed,is_null,exist_user
from models.regist_login import add_user,check_password

from models.create_database import create_db


UPLOAD_FOLDER = r'./data/images/ccpd'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'avi'])

# app = Flask(__name__,template_folder='templates')
app = Flask(__name__,
            static_folder='templates',
            template_folder='templates',
            static_url_path='')
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

# werkzeug_logger = rel_log.getLogger('werkzeug')
# werkzeug_logger.setLevel(rel_log.ERROR)

db.init_app(app)
cors.init_app(app, supports_credentials=True)



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
            index_url = url_for('index')
            return redirect(index_url)
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
                return redirect(url_for('user_login'))
            else:
                login_message = "两次输入密码不一致"
                return render_template('regist.html', message=login_message)
    return render_template('regist.html')

@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.cli.command()
def create():
    db.drop_all()
    db.create_all()
    Car.init_db()

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow_Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Hesders'] = 'Content-Type, X-Requested-With'
    return response


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    print(datetime.datetime.now(), file.filename)
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        shutil.copy(src_path, './tmp/ct')
        # image_path = os.path.join('./tmp/ct', file.filename)
        # image_info = a2.mytest(file.filename)
        # print(a2.mytest(file.filename))
        return jsonify({
            'filename': file.filename
            # 'image_url': 'http://127.0.0.1:5000/tmp/' + file.filename,
            # 'image_info': image_info
        })
    return jsonify({'filename': file.filename})



@app.route('/download/<filename>', methods=["GET"])
def get_file(filename):
    # return send_from_directory(UPLOAD_FOLDER, filename)  # 前端访问时需要返回的数据
    answer = a2.mytest(filename)
    print(answer)
    return jsonify({
        'answer': answer
    })



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class CarApi(MethodView):
    def get(self, car_id):
        if not car_id:
            cars: [Car] = Car.query.all()
            results = [
                {
                    'id': car.id,
                    'license_plate': car.license_plate,
                    'in_time': car.in_time,
                    'out_time': car.out_time,
                    'province': car.province,
                    'city': car.city,
                    'vehicle_model': car.vehicle_model,
                    'duration': car.duration,
                } for car in cars
            ]
            return {
                'status': 'success',
                'message': '数据查询成功',
                'results': results
            }
        car: Car = Car.query.get(car_id)
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': {
                'id': car.id,
                'licen_plate': car.license_plate,
                'in_time': car.in_time,
                'out_time': car.out_time,
                'province': car.province,
                'city': car.city,
                'vehicle_model': car.vehicle_model,
                'duration': car.duration,
            }
        }

    def post(self):
        form = request.json
        car = Car()
        car.license_plate = form.get('license_plate')
        car.in_time = form.get('in_time')
        car.out_time = form.get('out_time')
        car.province = funcs.getProvince(car.license_plate)
        # car.province = '北京市'
        car.city = funcs.getCity(car.license_plate)
        car.vehicle_model = funcs.getModel(car.license_plate)
        car.duration = funcs.getDuration(car.in_time, car.out_time)
        db.session.add(car)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }

    def delete(self, car_id):
        car = Car.query.get(car_id)
        db.session.delete(car)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }

    def put(self, car_id):
        car: Car = Car.query.get(car_id)
        car.license_plate = request.json.get('license_plate')
        car.in_time = request.json.get('in_time')
        car.out_time = request.json.get('out_time')
        car.province = funcs.getProvince(car.license_plate)
        car.city = funcs.getCity(car.license_plate)
        car.vehicle_model = funcs.getModel(car.license_plate)
        car.duration = funcs.getDuration(car.in_time, car.out_time)
        db.session.commit()
        return {
            'status': 'success',
            'message': '数据修改成功'
        }

class ProApi(MethodView):
    def get(self):
        cars: [Car] = Car.query.with_entities(
            Car.province,
            func.count('*').label('num')
        ).group_by(Car.province).all()
        for car in cars:
            print(car.province)
            print(car.num)

        results = [
            {
                'province': car.province,
                'num': car.num,

            } for car in cars
        ]

        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': results
        }

class CityApi(MethodView):
    def get(self, curl):
        province = funcs.getProvinceUrl(curl)
        cars: [Car] = Car.query.filter_by(province=province).all()
        results = [{
            'id': car.id,
            'city': car.license_plate[:2] + ' ' + car.city
        } for car in cars]
        # print(results)
        car_sort = sorted(results, key=lambda x: x["city"])
        car_group = groupby(car_sort, key=lambda x: x["city"])
        result = [
            {
                'name': key,
                'value': len(list(group))
            }for key, group in car_group
        ]
        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': result
        }

# 车型
class ModelApi(MethodView):
    def get(self):
        cars: [Car] = Car.query.with_entities(
            Car.vehicle_model,
            func.count('*').label('num')
        ).group_by(Car.vehicle_model).all()
        results = [
            {
                'name': car.vehicle_model,
                'value': car.num,

            } for car in cars
        ]
        print(results)

        return {
            'status': 'success',
            'message': '数据查询成功',
            'results': results
        }

car_view = CarApi.as_view('car_api')
app.add_url_rule('/cars/', defaults={'car_id': None}, view_func=car_view, methods=['GET', ])
app.add_url_rule('/cars', view_func=car_view, methods=['POST', ])
app.add_url_rule('/cars/<int:car_id>', view_func=car_view, methods=['GET', 'PUT', 'DELETE'])

pro_view = ProApi.as_view('pro_api')
app.add_url_rule('/pros/select', view_func=pro_view, methods=['GET', 'PUT', 'DELETE'])

city_view = CityApi.as_view('city_api')
app.add_url_rule('/city/<string:curl>', view_func=city_view, methods=['GET', 'PUT', 'DELETE'])

model_view = ModelApi.as_view('model_api')
app.add_url_rule('/model', view_func=model_view, methods=['GET', 'PUT', 'DELETE'])



if __name__ == '__main__':
    files = [
        'uploads', 'tmp/ct', 'tmp/draw', 'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)

    app.run(debug=True)