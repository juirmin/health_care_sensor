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
@socketio.on('start')
def start():
    global start_time
    global time_count
    time_count = True
    start_time = int(time.time())
    while time_count:
        if(int(time.time())-time.time() >= 10):
            playsound('請開始良測')

@socketio.on('temperature')
def temperature():
    playsound('請開始良測')
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

@socketio.on('end')
def the_end():
    global time_count
    time_count = False
    playsound('良測結束')
    time.sleep(5)
    socketio.send(["end"])
@ app.route('/')
def index():
    return render_template(str(modeset())+'.html')


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    socketio.run(app,debug=True, threaded=True)
