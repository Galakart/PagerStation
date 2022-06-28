#!venv/bin/python
import datetime
import logging
import logging.handlers as loghandlers
import os
from distutils.util import strtobool

from dotenv import load_dotenv
# from flask_restful import Api, Resource
from flask import Flask, request
from flask_apscheduler import APScheduler
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from charset_encoder import CharsetEncoder

load_dotenv()

IS_TEST = strtobool(os.getenv('IS_TEST'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# api = Api(app)
engine = create_engine(DB_URL, pool_size=5)
db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

charset_encoder = CharsetEncoder()

scheduler = APScheduler()
scheduler.api_enabled = IS_TEST
scheduler.init_app(app)


if not os.path.exists('logs'):
    os.makedirs('logs')
formatter = logging.Formatter(
    '%(asctime)s  %(filename)s  %(funcName)s  %(lineno)d  %(name)s  %(levelname)s: %(message)s')
log_handler = loghandlers.RotatingFileHandler(
    './logs/botlog.log',
    maxBytes=1000000,
    encoding='utf-8',
    backupCount=50
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


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

ROLES = {
    'admin': 10,
}


class Baudrate(db.Model):
    __tablename__ = 'n_baudrates'
    __table_args__ = {"comment": "Скорости передачи данных"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(4), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Fbit(db.Model):
    __tablename__ = 'n_fbits'
    __table_args__ = {"comment": "Источники (функциональные биты)"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(1), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Codepage(db.Model):
    __tablename__ = 'n_codepages'
    __table_args__ = {"comment": "Кодировки текста"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(8), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class Transmitter(db.Model):
    __tablename__ = 'transmitters'
    __table_args__ = {"comment": "Передатчики"}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    freq = db.Column(db.Integer, unique=True, nullable=False)
    id_baudrate = db.Column(db.Integer, db.ForeignKey('n_baudrates.id'), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


user_pagers = db.Table(
    "user_pagers",
    db.Column("id_user", db.Integer, db.ForeignKey("users.id")),
    db.Column("id_pager", db.Integer, db.ForeignKey("pagers.id")),
)


class Pager(db.Model):
    __tablename__ = 'pagers'
    __table_args__ = {"comment": "Пейджеры"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=False, comment='Абонентский номер')
    capcode = db.Column(db.Integer, nullable=False)
    id_fbit = db.Column(db.Integer, db.ForeignKey('n_fbits.id'), nullable=False)
    id_codepage = db.Column(db.Integer, db.ForeignKey('n_codepages.id'), nullable=False)
    id_transmitter = db.Column(db.Integer, db.ForeignKey('transmitters.id'), nullable=False)
    users = db.relationship('User', secondary=user_pagers, back_populates='pagers')

    def __repr__(self):
        return "<{}>".format(self.id)


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {"comment": "Пользователи пейджеров"}

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(200), nullable=False)
    datar = db.Column(db.Date)
    pagers = db.relationship('Pager', secondary=user_pagers, back_populates='users')

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.fio)


class Role(db.Model):
    __tablename__ = 'n_role'
    __table_args__ = {"comment": "Список доступных дополнительных ролей пользователй"}

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(25), unique=True, nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.name)


class ServiceRole(db.Model):
    __tablename__ = 'service_roles'
    __table_args__ = {"comment": "Дополнительные роли пользователей"}

    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_role = db.Column(db.Integer, db.ForeignKey('n_role.id'), primary_key=True)

    def __repr__(self):
        return "<{}:{}>".format(self.id_user,  self.id_role)


class MessagePrivate(db.Model):
    __tablename__ = 'messages_private'
    __table_args__ = {"comment": "Сообщения - личные"}

    id = db.Column(db.Integer, primary_key=True)
    id_pager = db.Column(db.Integer, db.ForeignKey('pagers.id'), nullable=False)
    message = db.Column(db.String(950), nullable=False)
    sent = db.Column(db.Boolean, nullable=False, default=False)
    date_create = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.id_pager)


# class ToAdmin(Resource):
#     def get(self):
#         return "<h1>ololo</h1>"


# api.add_resource(ToAdmin, '/toadmin/')

@app.route('/toadmin/', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        mes_text = request.form.get('mes_text')[:950]
        if not mes_text:
            return f"""
                <CENTER>
                    <p><b>Введите сообщение!!!</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

        admins_lst = User.query.join(ServiceRole, ServiceRole.id_user == User.id).filter(
            ServiceRole.id_role == ROLES['admin']).all()
        if admins_lst:
            for admin_item in admins_lst:
                for pager_item in admin_item.pagers:
                    new_mes = MessagePrivate(
                        id_pager=pager_item.id,
                        message=mes_text
                    )
                    db.session.add(new_mes)
            db.session.commit()
        else:
            return f"""
                <CENTER>
                    <p><b>Админов в сервисе не зарегистрировано</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

        return f"""
                <CENTER>
                    <p><b>Сообщение отправлено</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

    return """
            <CENTER>
                <H2>Отправь сообщение админу на пейджер</H2>
                <form method="POST">
                    <p><b>Текст сообщения:</b></p>
                    <textarea name="mes_text" rows=10 cols=80 maxlength=950 required></textarea>
                    <br /><br />
                    <input type="submit" value="Отправить">
                </form>
            </CENTER>
            """


@scheduler.task('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
def job_pocsag_sender():
    session = scoped_session(db_session)
    unsent_messages_tuple = session.query(MessagePrivate).filter(MessagePrivate.sent == 0).limit(10).all()
    if unsent_messages_tuple:
        for unsent_message_item in unsent_messages_tuple:
            pager_item = Pager.query.get(unsent_message_item.id_pager)
            transmitter_item = Transmitter.query.get(pager_item.id_transmitter)
            baudrate_item = Baudrate.query.get(transmitter_item.id_baudrate)
            message_to_air(pager_item.capcode, pager_item.id_fbit, transmitter_item.freq,
                           baudrate_item.name, unsent_message_item.message)
            unsent_message_item.sent = 1
            session.add(unsent_message_item)
        session.commit()
    session.close()


scheduler.start()


def message_to_air(capcode: int, fbit: int, freq: int, baudrate: int, message: str) -> bool:
    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message)
    if not os.path.exists('./pocsag'):
        # print(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
        return False
    os.system(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8095, debug=IS_TEST)
