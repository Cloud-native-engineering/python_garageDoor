# mqtt_handler.py
from flask_mqtt import Mqtt
from data_processing import eval_garage_door_state, GarageDoorState
from datetime import datetime
import global_variables


# Initialize MQTT client
mqtt = Mqtt()

# Global variables to track the last state and timestamp
last_state = GarageDoorState.UNKNOWN
last_opened_timestamp = datetime.now()


def setup_mqtt(app):
    mqtt.init_app(app)
    register_callbacks(app)


def register_callbacks(app):
    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected successfully to MQTT broker.')
            mqtt.subscribe(app.config['MQTT_TOPIC'])
        else:
            print('MQTT Bad connection. Code:', rc)



    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        global last_state
        if message.topic == app.config['MQTT_TOPIC']:
            mqtt_message = message.payload.decode("utf-8")
            print("RAW MQTT-Message:", mqtt_message)
            global_variables.last_state = eval_garage_door_state(mqtt_message)
            global_variables.last_state.time = datetime.now()
            print("DOOR STATE:", global_variables.last_state)
