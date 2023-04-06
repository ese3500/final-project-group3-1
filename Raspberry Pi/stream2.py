# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import logging
import socketserver
from threading import Condition
from http import server
import uuid

from PIL import Image
from matplotlib import cm
import time, board, busio
import numpy as np
import adafruit_mlx90640 as ada

i2c = busio.I2C(board.SCL, board.SDA, frequency = 400000)
mlx = ada.MLX90640(i2c)
mlx.refresh_rate = ada.RefreshRate.REFRESH_4_HZ

MAX_TEMP = 30
MIN_TEMP = 25

IP_ADDR = "192.168.200.134"

PAGE="""\
<html>
<head>
<title>NightOwl Stream</title>
</head>
<body>
<center><h1>NightOwl Stream</h1></center>
<center><img src="stream.jpeg" width="50%" height="50%"></center>
<form action="http://{IP_ADDR}:8000/api/save" method="get">
   <button type='submit' name='state'>SAVE</button>
  </form></p>
</body>
</html>
"""

im = None

def get_image(buf):
    frame = np.zeros((24*32,))

    while True:
        try:
            mlx.getFrame(frame)
            break
        except ValueError:
            continue
    MIN_TEMP = np.quantile(frame, .25)
    MAX_TEMP = MIN_TEMP + 4

    frame = ((frame - MIN_TEMP) / (MAX_TEMP - MIN_TEMP))

    frame = frame.reshape((24,32,))
    im = Image.fromarray(np.uint8(cm.jet(frame)*255)).convert('RGB')
    im.save(buf, format='jpeg')

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        self.buffer.truncate()

        # if buf.startswith(b'\xff\xd8'):
        #     # New frame, copy the existing buffer's content and notify all
        #     # clients it's available
        with self.condition:
            get_image(self.buffer)
            self.frame = self.buffer.getvalue()
            self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

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
        elif self.path == '/api/save':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            if im is not None:
                print("SAVING")
                im.save(f"captures/CAPTURE_{uuid.uuid4().hex}.jpeg")
            else:
                print("No image")
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
#camera.start_recording(output, format='mjpeg')
try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    print('stop')