import DroneComms
class droneCont:
    def __init__(self,ip):
        self.yaw = 3
        self.roll = 0
        self.pitch = 1
        self.throttle = 2
        self.arm = 4
        self.sbus = DroneComms.SBUSUDP(ip)
        self.armed = False
        self.data = [1500] * 16
    def move(self, y, r ,p, t):
        self.data[self.yaw] = 1500 + (y*500)
        self.data[self.roll] = 1500 + (r*500)
        self.data[self.pitch] = 1500 + (p*500)
        self.data[self.throttle] = 1400 + (t*500)
        if(self.armed == True):
            self.data[self.arm] = 1800
        else:
            self.data[self.arm] = 1200
        self.sbus.sendUDP(self.data)
    def send(self,channel):
        data = channel
        self.sbus.sendUDP(data)
    def sendSame(self,val):
        data = [val] * 16
        self.sbus.sendUDP(data)
    def arming(self):
        data = [1500] * 16
        data[self.arm] = 1800
        self.armed = True
        self.sbus.sendUDP(data)
    def disarm(self):
        data = [1500] * 16
        data[self.arm] = 1200
        self.armed = False
        self.sbus.sendUDP(data)
