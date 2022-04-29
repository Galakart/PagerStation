#!venv/bin/python
import threading
import time

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


def timer_1min():
    """Таймер отправки"""
    cycle_period = 15
    while True:
        try:
            print('hello from thread')

            time.sleep(cycle_period)
        except Exception as ex_tm:
            time.sleep(cycle_period)


if __name__ == '__main__':
    TIMER_1MIN_THREAD = threading.Thread(target=timer_1min)
    TIMER_1MIN_THREAD.daemon = True
    TIMER_1MIN_THREAD.start()

    app.run(host='0.0.0.0', debug=True)
