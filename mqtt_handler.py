# mqtt_handler.py
from flask_mqtt import Mqtt
from data_processing import eval_garage_door_state, GarageDoorState
from datetime import datetime
import threading

state_lock = threading.Lock()

# Initialize MQTT client
mqtt = Mqtt()

# Global variables to track the last state and timestamp
last_state: GarageDoorState = GarageDoorState.UNKNOWN
last_opened_timestamp = datetime.now()

def setup_mqtt(app):
    mqtt.init_app(app)
    register_callbacks(app)


def register_callbacks(app):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        print("MQTT-Connected with result code "+str(rc))
        mqtt.subscribe(app.config['MQTT_TOPIC'])

    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        global last_state, last_opened_timestamp
        if message.topic == app.config['MQTT_TOPIC']:
            msg_str = message.payload.decode("utf-8")
            state = eval_garage_door_state(msg_str)
            print("Handler", state)
            with state_lock:
                if last_state != state:
                    last_state = state
                if state == GarageDoorState.OPEN:
                    last_opened_timestamp = datetime.now()
                print(last_state)
