import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1, stopbits=serial.STOPBITS_TWO)
ser.flush()

print("Initializing Pi...")
cur_incr = 1

while True:
    sent = str(cur_incr) + '\n'
    print("Sent " + sent)
    ser.write(sent.encode('ascii'))

    print("Waiting for response...")
    line = ser.readline().decode('utf-8')
    print("Got response: " + line)

    try:
        cur_incr = int(line) + 1
    except: 
        print("Failed to cast response to int")

    time.sleep(1)