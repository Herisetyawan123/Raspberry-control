from flask import Flask, render_template, Response
import cv2
from gpiozero import Servo
from time import sleep

# Inisialisasi Flask dan Servo
app = Flask(__name__)
servo = Servo(17)  # Ubah GPIO sesuai pin yang Anda gunakan
camera = cv2.VideoCapture(0)

# Fungsi untuk mengontrol pergerakan servo ke kanan/kiri
def move_servo(direction):
    if direction == 'left':
        servo.min()  # Gerakkan ke kiri
    elif direction == 'right':
        servo.max()  # Gerakkan ke kanan
    sleep(1)  # Tunda agar servo sempat bergerak
    servo.value = 0  # Kembali ke tengah

# Streaming video dari webcam
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route untuk kontrol pergerakan
@app.route('/move/<direction>')
def move(direction):
    move_servo(direction)
    return f"Moved {direction}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
