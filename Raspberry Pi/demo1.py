import io
import logging
import socketserver
import pathlib
from http import server
import uuid
from urllib.parse import parse_qs
import time
from matplotlib import cm
import board, busio
import numpy as np
import adafruit_mlx90640 as ada
from model import Model
from commands import Commander
import digitalio
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7735

MOTOR_OFF = not True

i2c = busio.I2C(board.SCL, board.SDA, frequency = 400000)
mlx = ada.MLX90640(i2c)
mlx.refresh_rate = ada.RefreshRate.REFRESH_2_HZ

MAX_TEMP = 30
MIN_TEMP = 25

## Display Setup ##
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

BAUDRATE = 24000000

spi = board.SPI()
disp = st7735.ST7735R(spi, rotation=90,cs=cs_pin,dc=dc_pin,rst=reset_pin,baudrate=BAUDRATE)
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

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
function run() {
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.status == 200) {
        // Typical action to be performed when the document is ready:
        document.getElementById("left_conf").innerHTML = xhttp.responseText;
        }
    };
    xmlHttp.open("GET", "/run", false);
    xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xmlHttp.send();
    if (xmlHttp.status != 201) alert("Failed to save");
    else alert("classified!");
    return xmlHttp.responseText;
}

function stop() {
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.status == 200) {
        // Typical action to be performed when the document is ready:
        document.getElementById("left_conf").innerHTML = xhttp.responseText;
        }
    };
    xmlHttp.open("GET", "/stop", false);
    xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xmlHttp.send();
    if (xmlHttp.status != 201) alert("Failed to save");
    else alert("classified!");
    return xmlHttp.responseText;
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
        <div width="20%" height="5%"><button id = "classify" onClick="run()">RUN</button></div>
        <div width="20%" height="5%"><button id = "stop" onClick="stop()">STOP</button></div>

    </center>
</body>
</html>
"""

DURATION_THRESH = {
    'F' : 0,
    'L' : 1.5,
    'R' : 1.5,
    'S' : 0
}

global im
im = None
model = Model('model-7.tflite')
commander = Commander()
global running
global last_inference_time
global last_inference
running = False

last_inference_time = time.time()
last_inference = 'S'

labels = ['L', 'R', 'F', 'S']
led_pose = {
    'L' : [commander.gon],
    'R' : [commander.ron],
    'F' : [commander.gon, commander.ron],
    'S' : []
}

def print_image(image):
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.Resampling.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    image = image.crop((x, y, x + width, y + height))

    # Display image.
    disp.image(image)

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
    im = Image.fromarray(np.uint8(cm.jet(frame)*255)).convert('RGB').rotate(180)
    im.save(buf, format='jpeg')
    print_image(Image.fromarray(np.uint8(cm.jet(frame)*255)[:,:,:3][:,:,::-1]).convert('RGB'))


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
            global model
            global labels
            global last_inference
            global last_inference_time
            global running
            global im

            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            commander.setSpeed(175, 175, 175)
            l_count = 0
            while True:
                try:
                    
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

                    if running:
                        commander.roff()        
                        commander.goff()        
                        commander.bon()
                        print(f"Distance close: {commander.getDistC()}")
                        print(f"Distance far: {commander.getDistF()}")

                        label = model.classifyImage(im)
                        commander.boff()
                        print("Left confidence level: " + str(round(label[0]*100, 1)) + "%")
                        print("Right confidence level: " + str(round(label[1]*100, 1)) + "%")
                        print("Straight confidence level: " + str(round(label[2]*100, 1)) + "%")
                        print("Unknown confidence level: " + str(round(label[3]*100, 1)) + "%")
                        print()

                        confidence = np.argmax(label)
                        if ((label[confidence] > 0.85 and labels[confidence] == 'L')
                            or (label[confidence] > 0.70 and labels[confidence] != 'L')):
                            print('Difference in time:' + str(-last_inference_time + time.time()))
                            if (labels[confidence] == 'L' and (l_count % 2 == 1)):
                                confidence = 1
                                l_count += 1
                            elif (labels[confidence] == 'L' and last_inference != 'L'):
                                l_count += 1
                            if last_inference == 'S':
                                print("moving " + labels[confidence])
                                if (not MOTOR_OFF):
                                    commander.move(labels[confidence])
                                last_inference_time = time.time()
                                last_inference = labels[confidence]

                                for led_func in led_pose[labels[confidence]]:
                                    led_func()
                            elif (-last_inference_time + time.time()) > DURATION_THRESH[last_inference]:
                                if (not MOTOR_OFF):
                                    commander.move(labels[confidence])
                                print("moving " + labels[confidence])
                                last_inference_time = time.time()
                                last_inference = labels[confidence]

                                for led_func in led_pose[labels[confidence]]:
                                    led_func()
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
        elif self.path == '/save':
            try:
                self.log_message("Saving")                
                im.save(f"{DATASET_DIR}/CAPTURE_{uuid.uuid4().hex}.jpeg")
                self.send_response(201)
            except Exception as e:
                self.log_error("Failed to save")
                logging.warning('Could not save: %s', self.client_address, str(e))
                self.send_response(201)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/run':
            print("got classify endpoint")

            running = True
            print('Running...')

        elif self.path == '/stop':
            print("got classify endpoint")
            running = False
            commander.move('S')
            print('Got stop')
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
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

try:
    address = ('', 8000)
    commander.setSpeed(162, 158, 100)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    print('stop')
