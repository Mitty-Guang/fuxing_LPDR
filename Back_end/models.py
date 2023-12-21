# -*- coding: utf-8 -*-
import datetime
import math
from funcs import getDuration, getProvince, getCity, getModel
from extension import db


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
            (1, '皖H12345', '2022-08-08 08:08:34', '2022-08-22 10:07:23'),
            (2, '津A654321', '2022-03-03 03:03:45', '2022-03-05 13:45:45'),
            (3, '京D3f475', '2021-03-04 14:23:21', '2021-07-16 21:21:34'),
            (4, '皖H333333', '2011-02-02 12:12:12', ''),
            (5, '皖H333333', '2011-02-02 12:12:12', '2022-08-08 08:08:08'),
        ]
        for ret in rets:
            car = Car()
            car.id = ret[0]
            car.license_plate = ret[1]
            car.in_time = ret[2]
            car.out_time = ret[3]
            car.province = getProvince(car.license_plate)
            car.city = getCity(car.license_plate)
            car.vehicle_model = getModel(car.license_plate)
            car.duration = getDuration(car.in_time, car.out_time)
            db.session.add(car)
        db.session.commit()

# class provinceAnalysis(db.Model):
#     __table__ = 'provinceAnalysis'
#     province = db.Column(db.String(255))
