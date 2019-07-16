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
        self.alignMod = 0
    def updateDead(self, change):
        self.throttleDead += change
    def move(self, y, r ,p, t):
        self.data[self.yaw] = 1500 + (y*500)
        self.data[self.roll] = 1500 + (r*500) + self.alignMod
        self.data[self.pitch] = 1500 + (p*500)

        # self.data[self.throttle] = int(t * 500 + 1500)
        # print(self.data[self.throttle])

        if(self.throttleDead + (t*500) > 900):
            self.data[self.throttle] = self.throttleDead + (t * 500)
        else:
            self.data[self.throttle] = 900


        if(self.armed == True):
            self.data[self.arm] = 2000
        else:
            self.data[self.arm] = 1200
        self.sbus.sendUDP(self.data)
    def moveRaw(self, y, r ,p, t):
        self.data[self.yaw] = y
        self.data[self.roll] = r
        self.data[self.pitch] = p
        self.data[self.throttle] = t
        if(self.armed == True):
            self.data[self.arm] = 2000
        else:
            self.data[self.arm] = 1200

    def enableAlignment(self):
        data = bytearray(4)
        data[0] = ord('F')
        data[1] = ord('A')
        data[2] = ord('C')
        data[3] = ord('E')
        try:
            self.sbus.client_socket.sendto(data, (self.sbus.ip, 6666))
            self.sbus.client_socket.settimeout(0.01)
            data = self.sbus.client_socket.recvfrom(256)
        except:
            None

    def send(self,channel):
        data = channel
        self.sbus.sendUDP(data)
    def sendSame(self,val):
        data = [val] * 16
        self.sbus.sendUDP(data)
    def arming(self):
        data = [1500] * 16
        data[self.arm] = 2000
        self.armed = True
    def disarm(self):
        data = [1500] * 16
        data[self.arm] = 1200
        self.armed = False
