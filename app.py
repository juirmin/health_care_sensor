from flask import Flask, jsonify, render_template
from fdk300 import FDK300
from fdk400 import FDK400
from m170 import M170
from mtk_a1 import MTKA1
from read_mode import modeset
from flask_socketio import SocketIO  # 加上這行
import configs
import time
from TTS import playsound
import time

app = Flask(__name__)
app.config.from_object(configs)

socketio = SocketIO(app)  # 加上這行
start_time = 0
time_count = False
time_out = 0
@socketio.on('start')
def start():
    print('start')
    playsound('認證成功請開始良測')
    global start_time
    global time_count
    time_count = True
    start_time = int(time.time())
    while time_count:
        time.sleep(1)
        if(int(time.time())-start_time >= time_out):
            playsound('請開始良測')
            start_time = int(time.time())

@socketio.on('temperature')
def temperature():
    global time_out
    time_out = 30
    while True:
        try:
            fdk300 = FDK300()
            _temp = fdk300.get_sensor_data()
            sensor_data = {'temperature': _temp['temperature']}
            print(sensor_data)
            if sensor_data["temperature"]!=0:
                socketio.send(["temperature",sensor_data["temperature"]])
                break
        except:
            pass
@socketio.on('oxygen')
def m170():
    global time_out
    time_out = 40
    while True:
        try:
            m170 = M170()
            sensor_data = {'oxygen': 0, 'pulse': 0}
            _temp = m170.get_sensor_data()
            sensor_data['oxygen'] = _temp['oxygen']
            sensor_data['pulse'] = _temp['pulse']
            if(sensor_data['oxygen']!=0):
                socketio.send(["oxygen",sensor_data["oxygen"],sensor_data["pulse"]])
                break
        except:
            pass

@socketio.on('pressure_S')
def fdk400():
    global time_out
    time_out = 120
    while True:
        try:
            fdk400 = FDK400()
            _temp = fdk400.get_sensor_data()
            sensor_data = {'pressure_S': 0, 'pressure_D': 0}
            sensor_data['pressure_S'] = _temp['pressure_S']
            sensor_data['pressure_D'] = _temp['pressure_D']
            if(sensor_data['pressure_S']!=0):
                socketio.send(["pressure_S",sensor_data["pressure_S"],sensor_data["pressure_D"]])
                break
        except:
            pass

@socketio.on('weight')
def mtka1():
    global time_out
    time_out = 30
    while True:
        try:
            scale = MTKA1()
            sensor_data = {'weight': 0}
            _temp = scale.get_sensor_data()
            sensor_data['weight'] = _temp['weight']
            if sensor_data["weight"]!=0:
                socketio.send(["weight",sensor_data["weight"]])
                break
        except:
            pass

@socketio.on('end')
def the_end():
    global time_count
    time_count = False
    playsound('良測結束')
    time.sleep(5)
    print('end')
    socketio.send(["end"])
@app.route('/')
def index():
    return render_template(str(modeset())+'.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    socketio.run(app,debug=True, threaded=True)
