from PIL import Image
from matplotlib import cm
import time, board, busio
import numpy as np
import adafruit_mlx90640 as ada

i2c = busio.I2C(board.SCL, board.SDA, frequency = 400000)
mlx = ada.MLX90640(i2c)
mlx.refresh_rate = ada.RefreshRate.REFRESH_2_HZ

MAX_TEMP = 40
MIN_TEMP = 10

frame = np.zeros((24*32,))

while True:
	try:
		mlx.getFrame(frame)
		break
	except ValueError:
		continue

print (frame)
print("quantile: ", np.quantile(frame, .25))


frame = ((frame - MIN_TEMP) / (MAX_TEMP - MIN_TEMP))


frame = frame.reshape((24,32,))

im = Image.fromarray(np.uint8(cm.jet(frame)*255))
im.save('heatmap.png')

