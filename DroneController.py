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
        self.throttleDead = 1100
    def updateDead(self, change):
        self.throttleDead += change
    def move(self, y, r ,p, t):
        self.data[self.yaw] = 1500 + (y*500)
        self.data[self.roll] = 1500 + (r*500)
        self.data[self.pitch] = 1500 + (p*500)
        if(self.throttleDead + (t*500) > 10):
            self.data[self.throttle] = self.throttleDead + (t * 500)
        else:
            self.data[self.throttle] = 1000
        print(self.data[self.throttle])
        if(self.armed == True):
            self.data[self.arm] = 2000
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
        data[self.arm] = 2000
        data[self.throttle] = 800.0
        self.armed = True
        self.sbus.sendUDP(data)
    def disarm(self):
        data = [1500] * 16
        data[self.arm] = 1200
        self.armed = False
        self.sbus.sendUDP(data)
