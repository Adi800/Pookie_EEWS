from flask import Flask, request
from flask_socketio import SocketIO
import numpy as np
import mysql.connector
import tensorflow as tf

app = Flask(__name__)
socketio = SocketIO(app)

# Load the trained CNN model
model = tf.keras.models.load_model('cnn_model.h5')  # Replace with your model path

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",  # Change this to your MySQL root password
    database="seismic_data"
)
cursor = db.cursor()

@socketio.on('seismic_data')
def handle_seismic_data(data):
    # Assume data is a dictionary with keys: 'latitude', 'longitude', 'magnitude', 'depth'
    X = np.array([[data['magnitude'], data['depth'], data['latitude'], data['longitude']]])
    prediction = model.predict(X)
    alert_level = np.argmax(prediction, axis=1)[0]

    # Store the data in the MySQL database
    cursor.execute("""
        INSERT INTO events (latitude, longitude, magnitude, depth, epicenter, affected_range)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (data['latitude'], data['longitude'], data['magnitude'], data['depth'], 'Predicted Location', 10))  # Affected range is just an example
    db.commit()

    # Emit alert to front-end (optional)
    socketio.emit('alert', {'alert_level': alert_level})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
