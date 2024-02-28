from flask import Flask, render_template, jsonify
from mqtt_handler import setup_mqtt
import os
import global_variables

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config')

# Initialize MQTT
setup_mqtt(app)


# Start the background task
#start_background_task()


@app.route('/')
def index():
    print("FLASK Door-Status: ", global_variables.last_state)
    return render_template('index.html', door_status=str(global_variables.last_state))


@app.route('/api')
def api():
    data = [
        {"name": "Garage1", "state": str(global_variables.last_state), "last_updated": str(global_variables.last_state.time)}
    ]
    return jsonify(data)

# Start the Flask application
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=app.config['DEBUG'])