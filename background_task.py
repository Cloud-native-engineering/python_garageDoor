import threading
import time
from datetime import datetime, timedelta
from mqtt_handler import last_state, last_opened_timestamp, GarageDoorState

last_state: GarageDoorState = GarageDoorState.OPEN
last_opened_timestamp = datetime.now()
notification_sent = False



def check_garage_door_state():
    global notification_sent, last_state
    if (last_state == GarageDoorState.OPEN
            and datetime.now() - last_opened_timestamp > timedelta(seconds=5)
            and not notification_sent):
        print("Sending notification", last_state)
        notification_sent = True
    if last_state != GarageDoorState.OPEN:
        notification_sent = False
    return last_state


def start_background_task():
    def run_task():
        while True:
            check_garage_door_state()
            time.sleep(1)
    thread = threading.Thread(target=run_task)
    thread.daemon = True
    thread.start()