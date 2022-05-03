#!venv/bin/python
import threading
import time

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URL
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)


BAUDRATES = {
    '512': 1,
    '1024': 2,
    '2048': 3,
}

FBITS = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
}

CODEPAGES = {
    'lat': 1,
    'cyr': 2,
    'linguist': 3,
}


class Baudrate(db.Model):
    __tablename__ = 'n_baudrates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(4), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Fbit(db.Model):
    __tablename__ = 'n_fbits'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(1), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Codepage(db.Model):
    __tablename__ = 'n_codepages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Transmitter(db.Model):
    __tablename__ = 'transmitters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    freq = db.Column(db.Integer, unique=True, nullable=False)
    baudrate = db.Column(db.Integer, db.ForeignKey('n_baudrates.id'), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


def timer_sender():
    """Таймер отправки"""
    cycle_period = 15
    while True:
        try:
            print('hello from thread')

            time.sleep(cycle_period)
        except Exception as ex_tm:
            time.sleep(cycle_period)


if __name__ == '__main__':
    TIMER_1MIN_THREAD = threading.Thread(target=timer_sender)
    TIMER_1MIN_THREAD.daemon = True
    TIMER_1MIN_THREAD.start()

    app.run(host='0.0.0.0', debug=True)
