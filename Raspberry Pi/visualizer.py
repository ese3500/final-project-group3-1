import io
import logging
import socketserver
import pathlib
from http import server
import uuid
from urllib.parse import parse_qs
from PIL import Image
from matplotlib import cm
import board, busio
import numpy as np
import adafruit_mlx90640 as ada
from model import Model
from commands import Commander

i2c = busio.I2C(board.SCL, board.SDA, frequency = 400000)
mlx = ada.MLX90640(i2c)
mlx.refresh_rate = ada.RefreshRate.REFRESH_4_HZ

MAX_TEMP = 30
MIN_TEMP = 25

IP_ADDR = "192.168.200.134"
DATASET_DIR = '/home/pi/nightowl/dataset'

PAGE="""\
<html>
<head>
<title>NightOwl Stream</title>
</head>
<script>
function save() {
    var xmlHttp = new XMLHttpRequest();
    var label = document.getElementById("label_input").value
    if (label == "") {
        alert("Please input label");
        return "err:no label";
    }
    xmlHttp.open("POST", "/save", false);
    xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xmlHttp.send("label=" + label);
    if (xmlHttp.status != 201) alert("Failed to save");
    else alert("Saved at " + label);
    return xmlHttp.responseText;
}
function classify() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", "/classify", false);
}
</script>

<body>
    <center><h1>NightOwl Stream</h1></center>
    <center><img src="stream.jpeg" width="70%" height="70%"></center>
    <center>
        <br>Enter label:<br>
        <textarea id="label_input" name="label_input" rows="2" cols="30" placeholder="Example: right" onkeydown="if(event.keyCode == 13) {save();return false;}"></textarea>
        <br><br>
        <div width="20%" height="5%"><button id="save" onClick="save()">SAVE</button></div>
        <br><br>
        <div width="20%" height="5%><button id = "classify" onClick="classify">CLASSIFY</button></div>
    </center>
</body>
</html>
"""

im = None
model = Model()
commander = Commander()

labels = ['L', 'R', 'U']

def get_image(buf):
    global im
    frame = np.zeros((24*32,))

    # Get frame
    while True:
        try:
            mlx.getFrame(frame)
            break
        except ValueError:
            continue

    # Rescale according to the 25th lowest temperature
    MIN_TEMP = np.quantile(frame, .25)
    MAX_TEMP = MIN_TEMP + 4
    frame = ((frame - MIN_TEMP) / (MAX_TEMP - MIN_TEMP))

    # Save image into buffer
    frame = frame.reshape((24,32,))
    im = Image.fromarray(np.uint8(cm.jet(frame)*255)).convert('RGB')
    im.save(buf, format='jpeg')

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.jpeg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    buffer = io.BytesIO()
                    buffer.seek(0)
                    buffer.truncate()
                    get_image(buffer)
                    frame = buffer.getvalue()

                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/save':
            try:
                global im
                self.log_message("Saving")                
                im.save(f"{DATASET_DIR}/CAPTURE_{uuid.uuid4().hex}.jpeg")
                self.send_response(201)
            except Exception as e:
                self.log_error("Failed to save")
                logging.warning('Could not save: %s', self.client_address, str(e))
                self.send_response(201)
            self.send_header('Location', '/index.html')
            self.end_headers()
        else:
            self.send_error(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/save':
            try:
                global im
                self.log_message("Saving")                
                content_length = int(self.headers['Content-Length'])
                body = parse_qs(self.rfile.read(content_length).decode(), strict_parsing=True)
                if (body.get("label") is None):
                    self.log_message("Could not get label")
                    self.send_response(401)
                    self.end_headers()
                else:
                    self.log_message(f"Label found: {body['label'][0]}") 
                    pathlib.Path(f"{DATASET_DIR}/{body['label'][0]}").mkdir(parents=True, exist_ok=True)
                    im.save(f"{DATASET_DIR}/{body['label'][0]}/{body['label'][0]}_{uuid.uuid4().hex}.jpeg")
                    self.send_response(201)
            except Exception as e:
                self.log_error("Failed to save")
                logging.warning('Could not save: %s', self.client_address, str(e))
                self.send_response(201)
            self.end_headers()
        elif self.path == '/classify':
            global model
            global labels
            label = model.classifyImage(im)
            print("Left confidence level: " + str(label[0]*100) + "%")
            print("Right confidence level: " + str(label[0]*100) + "%")
            print("Tpose confidence level: " + str(label[0]*100) + "%")
            print()

            confidence = np.argmax(label)
            if (label[confidence] > 0.95):
                commander.move(labels[confidence])

        else:
            if self.path == '/classify':
                global im
                global model
                global labels
                label = model.classifyImage(im)
                print("Left confidence level: " + str(label[0]*100))
                print("Right confidence level: " + str(label[0]*100))
                print("Tpose confidence level: " + str(label[0]*100))
                print()

                confidence = np.argmax(label)
                if (label[confidence] > 0.95):
                    commander.move(labels[confidence])
                else:
                    commander.move('')

            else:
                self.send_error(404)
                self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    print('stop')