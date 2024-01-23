from flask import Flask, render_template
import config
from mqtt_handler import setup_mqtt
from background_task import start_background_task, last_state
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config')

# Initialize MQTT
setup_mqtt(app)

# Start the background task
start_background_task()


@app.route('/')
def index():
    # You can add logic here to check the actual status of the garage door
    current_state = last_state
    print("Door status in route:", current_state)
    return render_template('index.html', door_status=str(current_state))

# Start the Flask application
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=app.config['DEBUG'])