import serial

MIN_SPEED = 0
MAX_SPEED = 200
VALID_MOVE = ['F', 'B', 'R', 'L', 'U', 'S']

class Commander:
    def __init__(self, baud=9600, port='/dev/ttyACM0'):
        self.ser = serial.Serial(port=port, baudrate=baud, timeout=0.1, stopbits=serial.STOPBITS_TWO)
        self.ser.flush()
        self.ser.flushInput()

    def setSpeed(self, leftSpeed, rightSpeed, dur):
        leftSpeed = inRange(int(leftSpeed), MIN_SPEED, MAX_SPEED)
        rightSpeed = inRange(int(rightSpeed), MIN_SPEED, MAX_SPEED)
        dur = int(dur)
    
        self.ser.write(f"SPEED {leftSpeed} {rightSpeed} {dur}\n".encode('ascii'))
        return 0
    
    def move(self, dir):
        if dir not in VALID_MOVE:
            print("Invalid inputs to move")
            return -1
        
        self.ser.write(f"MOVE {dir}\n".encode('ascii'))
        return 0
    
    def ron(self):
        self.ser.write(f"RON\n".encode('ascii'))
        return 0
    
    def roff(self):
        self.ser.write(f"ROFF\n".encode('ascii'))
        return 0
    
    def gon(self):
        self.ser.write(f"GON\n".encode('ascii'))
        return 0
    
    def goff(self):
        self.ser.write(f"GOFF\n".encode('ascii'))
        return 0
    
    def bon(self):
        self.ser.write(f"BON\n".encode('ascii'))
        return 0
    
    def boff(self):
        self.ser.write(f"BOFF\n".encode('ascii'))
        return 0
    
    def flush(self):
        self.ser.flush()
        self.ser.flushInput()

        return 0
    
    def getDistF(self):        
        self.ser.write(f"DISTF\n".encode('ascii'))
        line = self.ser.readline().decode('utf-8')
        
        try:
            dist = int(line)
        except: 
            print("Failed to cast dist to int")
            print(f"Got line: {line}")
            return -1
        return dist

    
    def getDistC(self):        
        self.ser.write(f"DISTC\n".encode('ascii'))
        line = self.ser.readline().decode('utf-8')
        
        try:
            dist = int(line)
        except: 
            print("Failed to cast dist to int")
            print(f"Got line: {line}")
            return -1
        return dist

    
    def test(self):        
        self.ser.write(f"TEST\n".encode('ascii'))
        line = self.ser.readline().decode('utf-8')
        
        try:
            dist = str(line)
        except: 
            print("Failed to cast dist to int")
            print(f"Got line: {line}")
            return -1
        return dist

    
    def noPerson(self):        
        self.ser.write(f"NOPERSON\n".encode('ascii'))
        return 0
    
    def person(self, angle):
        try:
            if not (0 <= int(angle) <= 180) :
                print("Invalid angle to person")
                return -1
        except:
            print("Invalid angle to person")

        
        self.ser.write(f"PERSON {int(angle)}\n".encode('ascii'))
        return 0
    
    def waitUntilDone(self):
        line = self.ser.readline().decode('utf-8')
        
        while "DONE" not in line:
            line = self.ser.readline().decode('utf-8')

        return 0

def inRange(val, lower, upper):
   return min(upper, max(lower, val))
