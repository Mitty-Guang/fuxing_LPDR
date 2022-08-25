 # -*- coding: utf-8 -*-
from templates.extension import db

class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    license_plate = db.Column(db.String(255), nullable=False)
    in_time = db.Column(db.String(255), nullable=False)
    out_time = db.Column(db.String(255))
    province = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    vehicle_model = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255))

    @staticmethod
    def init_db():
        rets = [
            (1, '皖H12345', '2022-08-08 08:08:34', '2022-08-22 10:07:23', '安徽省', '安庆市', '蓝牌', '338 时 1 分 2 秒'),
            (2, '津A654321', '2022-03-03 03:03:45', '2022-03-05 13:45:45', '天津市', '天津市', '绿牌', '222 时 44 分 12 秒'),
            (3, '京D3f475', '2021-03-04 14:23:21', '2021-07-16 21:21:34', '北京市', '北京市', '蓝牌', '123 时 34 分 34 秒')
        ]
        for ret in rets:
            car = Car()
            car.id = ret[0]
            car.license_plate = ret[1]
            car.in_time = ret[2]
            car.out_time = ret[3]
            car.province = ret[4]
            car.city = ret[5]
            car.vehicle_model = ret[6]
            car.duration = ret[7]
            db.session.add(car)
        db.session.commit()
